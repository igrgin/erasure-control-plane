package com.dispatchworks.erasure.accountsaccess;

public record SourceMapping(String businessAccountRef, String source, long version,
                            String realm, String localAccountId) {}
