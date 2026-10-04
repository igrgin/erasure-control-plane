CREATE SCHEMA accounts_access;
REVOKE ALL ON SCHEMA accounts_access FROM PUBLIC;
GRANT USAGE ON SCHEMA accounts_access TO erasure_runtime;

CREATE TABLE accounts_access.business_account (
    tenant_id varchar(100) PRIMARY KEY,
    display_name varchar(200) NOT NULL
);
CREATE TABLE accounts_access.employee_grant (
    issuer text NOT NULL,
    subject text NOT NULL,
    tenant_id varchar(100) NOT NULL REFERENCES accounts_access.business_account(tenant_id),
    role varchar(30) NOT NULL CHECK (role IN ('OPERATOR', 'AUDITOR', 'SOURCE_OWNER', 'PLATFORM_ADMIN')),
    PRIMARY KEY (issuer, subject, tenant_id, role)
);
CREATE TABLE accounts_access.source_mapping (
    tenant_id varchar(100) NOT NULL REFERENCES accounts_access.business_account(tenant_id),
    source_id varchar(100) NOT NULL,
    mapping_version bigint NOT NULL CHECK (mapping_version > 0),
    realm varchar(100) NOT NULL,
    local_account_id varchar(100) NOT NULL,
    PRIMARY KEY (tenant_id, source_id, mapping_version),
    UNIQUE (source_id, mapping_version, realm, local_account_id)
);

ALTER TABLE accounts_access.business_account ENABLE ROW LEVEL SECURITY;
ALTER TABLE accounts_access.business_account FORCE ROW LEVEL SECURITY;
ALTER TABLE accounts_access.employee_grant ENABLE ROW LEVEL SECURITY;
ALTER TABLE accounts_access.employee_grant FORCE ROW LEVEL SECURITY;
ALTER TABLE accounts_access.source_mapping ENABLE ROW LEVEL SECURITY;
ALTER TABLE accounts_access.source_mapping FORCE ROW LEVEL SECURITY;

-- Owner operations are explicit and unavailable to the runtime role.
CREATE POLICY account_migration ON accounts_access.business_account TO erasure_migrator USING (true) WITH CHECK (true);
CREATE POLICY grant_migration ON accounts_access.employee_grant TO erasure_migrator USING (true) WITH CHECK (true);
CREATE POLICY mapping_migration ON accounts_access.source_mapping TO erasure_migrator USING (true) WITH CHECK (true);

GRANT SELECT ON accounts_access.business_account, accounts_access.employee_grant TO erasure_runtime;
-- Mappings are immutable versions. Administrative insertion needs an explicit tenant grant.
GRANT SELECT, INSERT ON accounts_access.source_mapping TO erasure_runtime;
CREATE POLICY employee_own_grants ON accounts_access.employee_grant FOR SELECT TO erasure_runtime
    USING (issuer = current_setting('app.employee_issuer', true)
       AND subject = current_setting('app.employee_subject', true));
CREATE POLICY account_catalog ON accounts_access.business_account FOR SELECT TO erasure_runtime
    USING (EXISTS (SELECT 1 FROM accounts_access.employee_grant g
                   WHERE g.tenant_id = business_account.tenant_id)
       AND (coalesce(current_setting('app.tenant_id', true), '') = ''
            OR tenant_id = current_setting('app.tenant_id', true)));
CREATE POLICY mapping_read ON accounts_access.source_mapping FOR SELECT TO erasure_runtime
    USING (tenant_id = current_setting('app.tenant_id', true)
       AND EXISTS (SELECT 1 FROM accounts_access.employee_grant g
                   WHERE g.tenant_id = source_mapping.tenant_id));
CREATE POLICY mapping_insert ON accounts_access.source_mapping FOR INSERT TO erasure_runtime
    WITH CHECK (tenant_id = current_setting('app.tenant_id', true)
       AND EXISTS (SELECT 1 FROM accounts_access.employee_grant g
                   WHERE g.tenant_id = source_mapping.tenant_id AND g.role = 'PLATFORM_ADMIN'));
