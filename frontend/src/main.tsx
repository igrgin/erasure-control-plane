import { StrictMode, useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';

type Account = { reference: string; name: string };
type Session = { employee: string; accounts: Account[]; selectedAccount: Account | null };
type Mapping = { businessAccountRef: string; source: string; version: number; realm: string; localAccountId: string };

async function getSession(): Promise<Session | null> {
  const response = await fetch('/api/session', { cache: 'no-store' });
  if (response.status === 401) return null;
  if (!response.ok) throw new Error('Could not load your business accounts. Please try again.');
  return response.json();
}

async function command(path: string, body?: unknown) {
  const csrfResponse = await fetch('/api/csrf', { cache: 'no-store' });
  if (!csrfResponse.ok) throw new Error('Could not confirm your session. Please sign in again.');
  const csrf: { headerName: string; token: string } = await csrfResponse.json();
  const response = await fetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', [csrf.headerName]: csrf.token },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  if (!response.ok) throw new Error('Your session or account access has changed. Refresh and try again.');
}

function App() {
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [mappings, setMappings] = useState<Mapping[] | null>(null);
  const selected = session?.selectedAccount;

  useEffect(() => {
    let active = true;
    getSession().then(value => { if (active) setSession(value); })
      .catch(reason => { if (active) setError(String(reason.message)); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    setMappings(null);
    if (selected) {
      fetch(`/api/accounts/${encodeURIComponent(selected.reference)}/mappings`, { signal: controller.signal, cache: 'no-store' })
        .then(async response => {
          if (!response.ok) throw new Error('Account access changed. Refresh to see your current grants.');
          const rows: Mapping[] = await response.json();
          if (!controller.signal.aborted) setMappings(rows);
        })
        .catch(reason => {
          if (!controller.signal.aborted) {
            setError(String(reason.message));
            setSession(current => current ? { ...current, selectedAccount: null } : null);
          }
        });
    }
    return () => controller.abort();
  }, [selected?.reference]);

  async function select(account: Account) {
    setBusy(true);
    setError('');
    setMappings(null);
    try {
      await command('/api/session/account', { businessAccountRef: account.reference });
      setSession(await getSession());
    } catch (reason) {
      setError((reason as Error).message);
      setSession(current => current ? { ...current, selectedAccount: null } : null);
    } finally {
      setBusy(false);
    }
  }

  async function logout() {
    setBusy(true);
    try {
      await command('/logout');
      setSession(null);
      setMappings(null);
      setError('');
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return <div className="shell">
    <aside className="sidebar">
      <a className="brand" href="/" aria-label="Erasure home"><span className="mark">e</span>erasure</a>
      <p className="company">DISPATCHWORKS</p>
      <div className="nav-item"><span aria-hidden="true">▦</span> Business accounts</div>
      <div className="sidebar-bottom"><span className="status-dot"/> Synthetic environment<p>Employee access foundation</p></div>
    </aside>
    <div className="main-shell">
      <header className="topbar">
        <span>Control plane <span className="divider">/</span> Business accounts</span>
        {session && <div className="employee"><span>{session.employee}</span><button className="text-button" onClick={logout} disabled={busy}>Sign out</button></div>}
      </header>
      <main>
        {error && <div className="error" role="alert">{error} <button className="text-button" onClick={() => window.location.reload()}>Refresh</button></div>}
        {loading ? <p role="status">Loading your workspace…</p> : !session ? <section className="login-panel">
          <p className="eyebrow">EMPLOYEE WORKSPACE</p>
          <h1>Start with the right<br/>business account.</h1>
          <p className="intro">Sign in to see the accounts you are authorized to operate. Every account keeps its own data and source mappings.</p>
          <a className="primary-button" href="/oauth2/authorization/keycloak">Sign in with employee account <span aria-hidden="true">↗</span></a>
          <p className="fine-print">DispatchWorks demonstration · Synthetic data only</p>
        </section> : <>
          <p className="eyebrow">ACCOUNT WORKSPACE</p>
          <h1>Your business accounts</h1>
          <p className="intro">Choose the business account you want to work with.</p>
          <section className="selected-banner" aria-label="Current business account">
            <div><p className="eyebrow">SELECTED BUSINESS ACCOUNT</p><strong>{selected?.name ?? 'No account selected'}</strong></div>
            {selected ? <code>{selected.reference}</code> : <span>Select an account below to continue</span>}
          </section>
          <div className="section-heading"><h2>Authorized accounts</h2><span>{session.accounts.length} available</span></div>
          {session.accounts.length === 0 ? <div className="empty">You have no business account grants. Contact your platform administrator to request access.</div> :
            <div className="accounts">{session.accounts.map(account => <button key={account.reference}
              className={`account-card ${selected?.reference === account.reference ? 'active' : ''}`}
              disabled={busy || selected?.reference === account.reference} aria-pressed={selected?.reference === account.reference}
              onClick={() => select(account)}>
              <span className="account-symbol" aria-hidden="true">{account.name.charAt(0)}</span>
              <span className="account-label"><strong>{account.name}</strong><code>{account.reference}</code></span>
              <span className="account-action">{selected?.reference === account.reference ? 'Selected ✓' : 'Select →'}</span>
            </button>)}</div>}
          {selected && <section className="mapping-panel">
            <div className="section-heading"><h2>Source account mappings</h2><span>{selected.name}</span></div>
            <p className="helper">A local ID identifies an account only together with its source, realm and mapping version.</p>
            {mappings === null ? <p role="status">Loading account mappings…</p> :
              <div className="table-scroll"><table><caption>Mappings for {selected.name}</caption>
                <thead><tr><th>Source</th><th>Realm</th><th>Local account ID</th><th>Version</th></tr></thead>
                <tbody>{mappings.filter(mapping => mapping.businessAccountRef === selected.reference).map(mapping =>
                  <tr key={`${mapping.source}-${mapping.version}`}><td>{mapping.source}</td><td><code>{mapping.realm}</code></td><td><code>{mapping.localAccountId}</code></td><td>v{mapping.version}</td></tr>)}</tbody>
              </table></div>}
          </section>}
        </>}
      </main>
      <footer>Erasure <span>Account access follows your employee grants.</span></footer>
    </div>
  </div>;
}

createRoot(document.getElementById('root')!).render(<StrictMode><App/></StrictMode>);
