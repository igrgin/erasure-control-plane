package com.dispatchworks.erasure.accountsaccess;

import java.util.List;
import java.util.function.Supplier;

import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.TransactionDefinition;
import org.springframework.transaction.support.TransactionTemplate;

/** Public read boundary for employee account access. This module owns its SQL and tables. */
@Service
public class AccountAccess {
    private final JdbcClient jdbc;
    private final TransactionTemplate transaction;

    public AccountAccess(JdbcClient jdbc, PlatformTransactionManager transactions) {
        this.jdbc = jdbc;
        transaction = new TransactionTemplate(transactions);
        // Read operations must neither inherit nor change another module's tenant context.
        transaction.setPropagationBehavior(TransactionDefinition.PROPAGATION_REQUIRES_NEW);
        transaction.setReadOnly(true);
    }

    public List<BusinessAccount> accounts(Employee employee) {
        return inContext(employee, "", () -> jdbc.sql("""
                SELECT tenant_id, display_name FROM accounts_access.business_account
                ORDER BY display_name
                """).query((row, index) -> new BusinessAccount(row.getString(1), row.getString(2))).list());
    }

    public BusinessAccount requireAccount(Employee employee, String reference) {
        return inContext(employee, reference, () -> authorizedAccount(reference));
    }

    public List<SourceMapping> mappings(Employee employee, String reference) {
        return inContext(employee, reference, () -> {
            authorizedAccount(reference);
            return jdbc.sql("""
                    SELECT tenant_id, source_id, mapping_version, realm, local_account_id
                    FROM accounts_access.source_mapping WHERE tenant_id = ?
                    ORDER BY source_id, mapping_version
                    """).param(reference).query((row, index) -> new SourceMapping(
                    row.getString(1), row.getString(2), row.getLong(3), row.getString(4), row.getString(5))).list();
        });
    }

    private BusinessAccount authorizedAccount(String reference) {
        // Explicit service grant check in addition to row policies. Never cache this in the session.
        boolean granted = jdbc.sql("""
                SELECT EXISTS (SELECT 1 FROM accounts_access.employee_grant WHERE tenant_id = ?)
                """).param(reference).query(Boolean.class).single();
        if (!granted) {
            throw new AccessDeniedException("Business account access denied");
        }
        return jdbc.sql("""
                SELECT tenant_id, display_name FROM accounts_access.business_account WHERE tenant_id = ?
                """).param(reference).query((row, index) -> new BusinessAccount(row.getString(1), row.getString(2)))
                .optional().orElseThrow(() -> new AccessDeniedException("Business account access denied"));
    }

    private <T> T inContext(Employee employee, String reference, Supplier<T> work) {
        if (reference == null || reference.length() > 100) {
            throw new AccessDeniedException("Business account access denied");
        }
        return transaction.execute(status -> {
            jdbc.sql("""
                    SELECT set_config('app.employee_issuer', ?, true),
                           set_config('app.employee_subject', ?, true),
                           set_config('app.tenant_id', ?, true)
                    """).params(employee.issuer(), employee.subject(), reference).query().singleRow();
            return work.get();
        });
    }
}
