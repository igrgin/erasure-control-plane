package com.dispatchworks.erasure.accountsaccess;

/** Identity from the validated OIDC principal, never from browser-supplied headers. */
public record Employee(String issuer, String subject) {
    public Employee {
        if (issuer == null || issuer.isBlank() || subject == null || subject.isBlank()) {
            throw new IllegalArgumentException("An employee requires both issuer and subject");
        }
    }
}
