package com.dispatchworks.erasure.web;

import java.util.List;

import com.dispatchworks.erasure.accountsaccess.AccountAccess;
import com.dispatchworks.erasure.accountsaccess.BusinessAccount;
import com.dispatchworks.erasure.accountsaccess.Employee;
import com.dispatchworks.erasure.accountsaccess.SourceMapping;
import jakarta.servlet.http.HttpSession;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.core.oidc.user.OidcUser;
import org.springframework.security.web.csrf.CsrfToken;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
class AccountController {
    private static final String SELECTED = "selectedBusinessAccount";
    private final AccountAccess access;

    AccountController(AccountAccess access) {
        this.access = access;
    }

    @GetMapping("/api/csrf")
    CsrfResponse csrf(CsrfToken token) {
        return new CsrfResponse(token.getHeaderName(), token.getParameterName(), token.getToken());
    }

    @GetMapping("/api/session")
    SessionResponse session(@AuthenticationPrincipal OidcUser principal, HttpSession session) {
        List<BusinessAccount> accounts = access.accounts(employee(principal));
        Object selectedReference = session.getAttribute(SELECTED);
        BusinessAccount selected = accounts.stream().filter(account -> account.reference().equals(selectedReference))
                .findFirst().orElse(null);
        if (selected == null) {
            session.removeAttribute(SELECTED);
        }
        return new SessionResponse(principal.getPreferredUsername(), accounts, selected);
    }

    @PostMapping("/api/session/account")
    BusinessAccount select(@AuthenticationPrincipal OidcUser principal, @RequestBody Selection selection,
                           HttpSession session) {
        BusinessAccount account = access.requireAccount(employee(principal), selection.businessAccountRef());
        session.setAttribute(SELECTED, account.reference());
        return account;
    }

    @GetMapping("/api/accounts/{reference}/mappings")
    List<SourceMapping> mappings(@AuthenticationPrincipal OidcUser principal, @PathVariable String reference) {
        return access.mappings(employee(principal), reference);
    }

    private Employee employee(OidcUser principal) {
        return new Employee(principal.getIssuer().toString(), principal.getSubject());
    }

    record CsrfResponse(String headerName, String parameterName, String token) {}
    record Selection(String businessAccountRef) {}
    record SessionResponse(String employee, List<BusinessAccount> accounts, BusinessAccount selectedAccount) {}
}
