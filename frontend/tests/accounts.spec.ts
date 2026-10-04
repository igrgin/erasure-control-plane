import { test, expect, type Page, type APIRequestContext } from '@playwright/test';
import { execFileSync } from 'node:child_process';

async function login(page: Page, employee: string) {
  await page.goto('/');
  await page.getByRole('link', { name: 'Sign in with employee account' }).click();
  await page.getByRole('textbox', { name: 'Username', exact: true }).fill(employee);
  await page.getByLabel('Password', { exact: true }).fill(`demo-${employee}`);
  await page.getByRole('button', { name: 'Sign In', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Your business accounts' })).toBeVisible();
}

async function select(request: APIRequestContext, ref: string) {
  const csrf = await (await request.get('/api/csrf')).json();
  return request.post('/api/session/account', {
    headers: { [csrf.headerName]: csrf.token }, data: { businessAccountRef: ref },
  });
}

test('anonymous APIs and forged employee headers cannot bypass login', async ({ request }) => {
  expect((await request.get('/api/session', { headers: { 'X-Employee': 'alice', 'X-Tenant-ID': 'biz-northstar' } })).status()).toBe(401);
  expect((await request.get('/api/accounts/biz-northstar/mappings')).status()).toBe(401);
  expect((await select(request, 'biz-northstar')).status()).toBe(401);
});

test('Northstar employee cannot read or select Harbor, even with overlapping local IDs', async ({ page }) => {
  await login(page, 'alice');
  await expect(page.getByRole('button', { name: /Harbor Analytics/ })).toHaveCount(0);
  await page.getByRole('button', { name: /Northstar Supply/ }).click();
  await expect(page.getByRole('region', { name: 'Current business account' })).toContainText('Northstar Supply');
  await expect(page.getByRole('cell', { name: 'north', exact: true })).toBeVisible();
  await expect(page.getByRole('cell', { name: '7', exact: true })).toBeVisible();
  const request = page.request;
  expect((await request.get('/api/accounts/biz-harbor/mappings', { headers: { 'X-Tenant-ID': 'biz-harbor', 'X-Employee': 'bob' } })).status()).toBe(403);
  expect((await select(request, 'biz-harbor')).status()).toBe(403);
  expect((await select(request, 'unknown-account')).status()).toBe(403);
  expect((await select(request, "biz-northstar' OR '1'='1")).status()).toBe(403);
  expect((await select(request, '')).status()).toBe(403);
  expect((await request.post('/api/session/account', { data: { businessAccountRef: 'biz-northstar' } })).status()).toBe(403);
  expect((await request.get('/api/session')).headers()['cache-control']).toContain('no-store');
  expect((await (await request.get('/api/session')).json()).selectedAccount.reference).toBe('biz-northstar');
  await page.reload();
  await expect(page.getByRole('region', { name: 'Current business account' })).toContainText('Northstar Supply');
  const cookies = await page.context().cookies();
  expect(cookies.find(cookie => cookie.name === 'SESSION')?.httpOnly).toBe(true);
  expect(cookies.find(cookie => cookie.name === 'SESSION')?.sameSite).toBe('Lax');
  await page.getByRole('button', { name: 'Sign out' }).click();
  await expect(page.getByRole('link', { name: /Sign in with employee/ })).toBeVisible();
  expect((await request.get('/api/session')).status()).toBe(401);
});

test('multiple grants allow explicit switching without mixing identical local IDs', async ({ page }) => {
  await login(page, 'bob');
  await page.getByRole('button', { name: /Northstar Supply/ }).click();
  await expect(page.getByRole('cell', { name: 'north', exact: true })).toBeVisible();
  await page.getByRole('button', { name: /Harbor Analytics/ }).click();
  await expect(page.getByRole('region', { name: 'Current business account' })).toContainText('Harbor Analytics');
  await expect(page.getByRole('cell', { name: 'harbor', exact: true })).toBeVisible();
  await expect(page.getByRole('cell', { name: 'north', exact: true })).toHaveCount(0);
  await expect(page.getByRole('cell', { name: '7', exact: true })).toBeVisible();
  await page.reload();
  await expect(page.getByRole('cell', { name: 'harbor', exact: true })).toBeVisible();
  // A stopped API must recover both authentication and account selection from PostgreSQL.
  execFileSync('docker', ['compose', '-f', '../deploy/local/compose.yaml', 'restart', 'application'], { timeout: 90_000 });
  await expect.poll(async () => {
    try { return (await page.request.get('/api/session', { timeout: 2_000 })).status(); }
    catch { return 0; }
  }, { timeout: 60_000 }).toBe(200);
  await page.reload();
  await expect(page.getByRole('cell', { name: 'harbor', exact: true })).toBeVisible();
  await page.screenshot({ path: test.info().outputPath('account-workspace.png'), fullPage: true });
});

test('identity without account grants gets no tenant access', async ({ page }) => {
  await login(page, 'source-owner');
  await expect(page.getByText('You have no business account grants.', { exact: false })).toBeVisible();
  expect((await select(page.request, 'biz-northstar')).status()).toBe(403);
  expect((await page.request.get('/api/accounts/biz-northstar/mappings')).status()).toBe(403);
});

test('revoked grants take effect in an existing session', async ({ page }) => {
  await login(page, 'alice');
  await page.getByRole('button', { name: /Northstar Supply/ }).click();
  await expect(page.getByRole('cell', { name: 'north', exact: true })).toBeVisible();
  const psql = (sql: string) => execFileSync('docker', [
    'compose', '-f', '../deploy/local/compose.yaml', 'exec', '-T', '-e', 'PGPASSWORD=local-migrator-only',
    'postgres', 'psql', '-h', '127.0.0.1', '-U', 'erasure_migrator', '-d', 'erasure', '-v', 'ON_ERROR_STOP=1', '-c', sql,
  ], { timeout: 30_000 });
  try {
    psql("DELETE FROM accounts_access.employee_grant WHERE subject='11111111-1111-4111-8111-111111111111'");
    expect((await page.request.get('/api/accounts/biz-northstar/mappings')).status()).toBe(403);
    expect((await select(page.request, 'biz-northstar')).status()).toBe(403);
    const session = await (await page.request.get('/api/session')).json();
    expect(session.accounts).toEqual([]);
    expect(session.selectedAccount).toBeNull();
    await page.reload();
    await expect(page.getByText('You have no business account grants.', { exact: false })).toBeVisible();
    await expect(page.getByRole('region', { name: 'Current business account' })).toContainText('No account selected');
  } finally {
    psql("INSERT INTO accounts_access.employee_grant VALUES ('http://localhost:18113/realms/erasure','11111111-1111-4111-8111-111111111111','biz-northstar','OPERATOR') ON CONFLICT DO NOTHING");
  }
});
