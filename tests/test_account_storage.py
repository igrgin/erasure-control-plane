"""REQ-01 / REQ-12 against the real, non-owner PostgreSQL runtime role."""
import os
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
ISSUER = "http://localhost:18113/realms/erasure"
ALICE = "11111111-1111-4111-8111-111111111111"
BOB = "22222222-2222-4222-8222-222222222222"
ADMIN = "55555555-5555-4555-8555-555555555555"


def sql(statement, role="erasure_runtime", check=True):
    password = "local-runtime-only" if role == "erasure_runtime" else "local-migrator-only"
    result = subprocess.run(
        ["docker", "compose", "-f", str(ROOT / "deploy/local/compose.yaml"),
         "exec", "-T", "-e", f"PGPASSWORD={password}", "postgres", "psql",
         "-h", "127.0.0.1", "-U", role, "-d", "erasure", "-X", "-qAt", "-v", "ON_ERROR_STOP=1"],
        input=statement, text=True, capture_output=True, timeout=30,
        env=os.environ,
    )
    if check and result.returncode:
        raise AssertionError(result.stderr)
    return result


def context(subject=ALICE, tenant="biz-northstar", issuer=ISSUER):
    return (f"SET LOCAL app.employee_issuer = '{issuer}'; "
            f"SET LOCAL app.employee_subject = '{subject}'; "
            f"SET LOCAL app.tenant_id = '{tenant}'; ")


class AccountStorageTest(unittest.TestCase):
    def query(self, statement, subject=ALICE, tenant="biz-northstar", issuer=ISSUER):
        return sql("BEGIN; " + context(subject, tenant, issuer) + statement + "; ROLLBACK;").stdout.strip()

    def test_runtime_is_not_owner_and_cannot_bypass_rls(self):
        self.assertEqual(sql("SELECT rolsuper, rolbypassrls FROM pg_roles WHERE rolname=current_user;").stdout.strip(), "f|f")
        self.assertEqual(sql("SELECT count(*) FROM pg_tables WHERE schemaname='accounts_access' AND tableowner=current_user;").stdout.strip(), "0")
        self.assertEqual(sql("SELECT count(*) FROM pg_class c JOIN pg_namespace n ON c.relnamespace=n.oid WHERE n.nspname='accounts_access' AND c.relkind='r' AND c.relrowsecurity AND c.relforcerowsecurity;").stdout.strip(), "3")

    def test_no_context_and_wrong_issuer_fail_closed(self):
        for table in ["business_account", "employee_grant", "source_mapping"]:
            self.assertEqual(sql(f"SELECT count(*) FROM accounts_access.{table};").stdout.strip(), "0")
        self.assertEqual(self.query("SELECT count(*) FROM accounts_access.business_account", issuer="https://other.example/realms/erasure"), "0")

    def test_catalog_only_lists_explicit_grants(self):
        self.assertEqual(self.query("SELECT tenant_id FROM accounts_access.business_account", tenant=""), "biz-northstar")
        self.assertEqual(self.query("SELECT count(*) FROM accounts_access.business_account", subject=BOB, tenant=""), "2")
        self.assertEqual(self.query("SELECT count(*) FROM accounts_access.business_account", subject="ungranted", tenant=""), "0")

    def test_overlapping_local_ids_require_full_authorized_tenant(self):
        self.assertEqual(self.query("SELECT realm, local_account_id FROM accounts_access.source_mapping"), "north|7")
        self.assertEqual(self.query("SELECT count(*) FROM accounts_access.source_mapping", tenant="biz-harbor"), "0")
        self.assertEqual(self.query("SELECT realm, local_account_id FROM accounts_access.source_mapping", subject=BOB, tenant="biz-harbor"), "harbor|7")
        self.assertEqual(self.query("SELECT count(*) FROM accounts_access.source_mapping", subject=BOB, tenant=""), "0")

    def test_transaction_context_does_not_survive_connection_reuse(self):
        for ending in ["COMMIT", "ROLLBACK"]:
            result = sql("BEGIN; " + context() + f"SELECT count(*) FROM accounts_access.source_mapping; {ending}; BEGIN; SELECT count(*) FROM accounts_access.source_mapping; ROLLBACK;")
            self.assertEqual(result.stdout.strip().splitlines(), ["1", "0"])

    def test_runtime_cannot_expand_grants(self):
        result = sql("BEGIN; " + context() + "INSERT INTO accounts_access.employee_grant VALUES ('" + ISSUER + "', '" + ALICE + "', 'biz-harbor', 'OPERATOR'); ROLLBACK;", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("permission denied", result.stderr)

    def test_mapping_write_requires_account_and_admin_role(self):
        statement = "INSERT INTO accounts_access.source_mapping VALUES ('biz-northstar', 'support', 2, 'north', '7')"
        denied = sql("BEGIN; " + context() + statement + "; ROLLBACK;", check=False)
        self.assertNotEqual(denied.returncode, 0)
        self.assertIn("row-level security", denied.stderr)
        auditor = sql("BEGIN; " + context("33333333-3333-4333-8333-333333333333") + statement + "; ROLLBACK;", check=False)
        self.assertNotEqual(auditor.returncode, 0)
        self.assertIn("row-level security", auditor.stderr)
        self.assertEqual(self.query(statement + "; SELECT count(*) FROM accounts_access.source_mapping", subject=ADMIN), "2")
        forged = sql("BEGIN; " + context(ADMIN) + statement.replace("biz-northstar", "biz-harbor") + "; ROLLBACK;", check=False)
        self.assertNotEqual(forged.returncode, 0)
        self.assertIn("row-level security", forged.stderr)
        # A tenant's admin cannot move an existing row to another tenant either.
        moved = sql("BEGIN; " + context(ADMIN) + "UPDATE accounts_access.source_mapping SET tenant_id='biz-harbor'; ROLLBACK;", check=False)
        self.assertNotEqual(moved.returncode, 0)
        self.assertIn("permission denied", moved.stderr)

    def test_mapping_identity_is_composite_and_versions_are_retained(self):
        self.assertEqual(self.query("INSERT INTO accounts_access.source_mapping VALUES ('biz-northstar', 'support', 2, 'north', '7'); SELECT count(*) FROM accounts_access.source_mapping", subject=ADMIN), "2")
        duplicate = sql("BEGIN; " + context(ADMIN) + "INSERT INTO accounts_access.source_mapping VALUES ('biz-northstar','support',1,'other','9'); ROLLBACK;", check=False)
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertIn("duplicate key", duplicate.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
