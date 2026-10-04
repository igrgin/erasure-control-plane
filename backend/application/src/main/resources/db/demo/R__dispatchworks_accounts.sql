INSERT INTO accounts_access.business_account VALUES
    ('biz-northstar', 'Northstar Supply'), ('biz-harbor', 'Harbor Analytics')
ON CONFLICT DO NOTHING;
INSERT INTO accounts_access.employee_grant VALUES
    ('${demoIssuer}', '11111111-1111-4111-8111-111111111111', 'biz-northstar', 'OPERATOR'),
    ('${demoIssuer}', '22222222-2222-4222-8222-222222222222', 'biz-northstar', 'OPERATOR'),
    ('${demoIssuer}', '22222222-2222-4222-8222-222222222222', 'biz-harbor', 'OPERATOR'),
    ('${demoIssuer}', '33333333-3333-4333-8333-333333333333', 'biz-northstar', 'AUDITOR'),
    ('${demoIssuer}', '55555555-5555-4555-8555-555555555555', 'biz-northstar', 'PLATFORM_ADMIN')
ON CONFLICT DO NOTHING;
-- source-owner has an OIDC identity but deliberately has no account grant.
INSERT INTO accounts_access.source_mapping VALUES
    ('biz-northstar', 'support', 1, 'north', '7'),
    ('biz-harbor', 'support', 1, 'harbor', '7')
ON CONFLICT DO NOTHING;
