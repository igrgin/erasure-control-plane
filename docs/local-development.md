# Employee login and account access

Issue #12 implements the REQ-01 / REQ-12 employee access foundation. The later proposal, approval, adapter, audit and public-demo workflows remain separate issues. The local environment uses synthetic DispatchWorks identities and the accepted `dispatchworks-v1` account mappings.

## Run locally

Install Docker with Compose and start the Docker daemon. The application build happens in pinned containers, so running the app does not require a host JDK, Maven or Node installation.

```sh
docker compose -f deploy/local/compose.yaml up -d --build --wait --wait-timeout 180
```

Open <http://localhost:18112>. Employee login redirects to local Keycloak at <http://localhost:18113>. Use `localhost` consistently because the OIDC issuer and callback have exact origins. Both ports bind to loopback. PostgreSQL is reachable only inside this Compose network. This is a local development environment with deliberately public synthetic credentials and HTTP. The default application profile requires secure cookies; only `local` disables that requirement and loads the demo grants.

| Username | Password | Explicit account grants |
| --- | --- | --- |
| `alice` | `demo-alice` | Northstar operator |
| `bob` | `demo-bob` | Northstar and Harbor operator |
| `auditor` | `demo-auditor` | Northstar auditor |
| `source-owner` | `demo-source-owner` | None, exercises login without account access |
| `admin` | `demo-admin` | Northstar platform administrator |

Employee identity uses the validated OIDC issuer and subject. Usernames are display labels, and neither usernames nor browser headers grant access. Each identity may list and select only its explicitly granted accounts. A source-owner identity alone cannot expand tenant access. Source ownership assignments belong to the later source-registry module.

Northstar is `biz-northstar`, with support mapping `(realm=north, account=7, version=1)`. Harbor is `biz-harbor`, with `(realm=harbor, account=7, version=1)`. These are control-plane mapping records. No support source database or adapter is created by this slice.

The UI keeps the account name and reference visible, lists only authorized accounts and displays the complete source-local mapping. Selecting an account writes only the account reference into the authenticated backend session. Every subsequent read checks current grants again. Removing a grant takes effect on the next protected request, and refreshing the session clears a revoked selection. Signing out invalidates the Erasure session. The local Keycloak SSO session remains active, so signing in again may reuse that identity. Use a separate browser profile to operate another employee.

```sh
docker compose -f deploy/local/compose.yaml logs -f application
docker compose -f deploy/local/compose.yaml stop
docker compose -f deploy/local/compose.yaml start
```

Stopping preserves the dedicated `erasure-accounts_accounts-db` volume, including identity data and sessions. These commands do not reset fixtures. Full demo generation/reset belongs to ERA-038. If another application occupies either loopback port, stop that application or coordinate a change to all issuer, callback and fixture values before starting.

## Pinned toolchain

| Component | Version / pin |
| --- | --- |
| Java language and runtime | Java 25 LTS, Temurin runtime `25.0.3_9-jre` |
| Spring Boot | `4.0.8`, dependency management controls Spring Security, Spring Session, JDBC and Flyway |
| Maven | `3.9.16`, container build with Temurin 25 |
| Node / npm | `24.14.1` / `11.11.0` |
| React / React DOM | `19.3.0` |
| TypeScript / Vite | `7.0.2` / `8.3.2` |
| Playwright | `1.63.0`, its Chromium revision |
| PostgreSQL | `18.4-bookworm` |
| Keycloak | `26.7.0` |
| Docker / Compose reference | Engine `29.6.2`, Compose `5.3.1` |

All application build/runtime images use immutable multi-platform digests in the [Dockerfile](../deploy/local/Dockerfile) and [Compose file](../deploy/local/compose.yaml). Node packages use exact versions plus `package-lock.json`. The Docker/Compose versions above identify the tested host tools; they are prerequisites, not downloads performed by the application.

The compatibility baseline comes from [Spring Boot's Java and Maven requirements](https://docs.spring.io/spring-boot/4.0/system-requirements.html). Login uses [Keycloak's container distribution](https://www.keycloak.org/server/containers), [Spring Security's session CSRF protection](https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html), and PostgreSQL [row security](https://www.postgresql.org/docs/18/ddl-rowsecurity.html).

For frontend development, use the version in `frontend/.nvmrc`, run `npm ci` inside `frontend`, then `npm run dev`. Vite proxies API requests to the running application. OIDC returns to the canonical application URL after login. The compiled frontend is packaged with the Spring application for acceptance checks.

For a standalone backend build with Java 25 and Maven 3.9.16:

```sh
mvn -B -f backend/pom.xml verify
```

## Acceptance checks

Use Python 3 and the pinned Node/npm versions, with Docker running:

```sh
python3 -m unittest discover -s scripts -p 'test_*.py'
bash scripts/check-accounts.sh
```

The account runner builds/starts the real Compose environment, runs eight storage tests, compiles the frontend and runs real Chromium login tests. It leaves the local environment running for inspection. CI installs Chromium's OS dependencies before running the same checks. Browser tests run serially, restart this Compose project's application and temporarily revoke Alice's grant, restoring it in a `finally` block. Run them only against this dedicated synthetic environment.

Storage checks connect as `erasure_runtime` over TCP with its actual credentials, never as an owner or `BYPASSRLS` role. They test missing and forged contexts, different issuers, overlapping IDs, explicit grants, pooled-connection context reset, denied grant expansion, authorized administrative mapping insertion, rejected cross-account writes and immutable composite mapping keys. Test writes roll back.

Browser checks exercise actual Keycloak OIDC redirects, unauthorized HTTP reads and selection writes, CSRF rejection, consistent account display, switching between two granted accounts, session-cookie properties, logout, no-grant identities, live revocation and session recovery after an API restart. Playwright retains traces and screenshots in ignored `frontend/test-results` on failure.

## Module and storage boundaries

`backend/accounts-access` owns account references, grants, versioned mappings and their SQL. Its public `AccountAccess` service exposes authorized account listing, resolution and mapping reads. `backend/application` owns HTTP, OIDC, CSRF and shared-session integration. Maven dependencies allow the application to use the access module; the access module does not depend on the HTTP application.

Account reads start a separate read transaction and set issuer, subject and tenant with transaction-local `set_config`. The connection never keeps account context beyond commit or rollback. This read boundary does not supply a cross-module write transaction. Future write workflows must coordinate their own transaction without changing another module's context.

All three account tables use forced row policies. Employee grants expose only the current identity's grants, and the account catalog exposes their corresponding accounts. Source mappings additionally require an exact selected tenant context. A browser account reference is a requested scope, not evidence of permission. Policies use the authenticated identity provided by the application; they do not protect against arbitrary execution under a stolen database runtime credential.

`erasure_migrator` owns migrations and has explicit maintenance policies. `erasure_runtime` cannot modify grants or account definitions, own tables or bypass row security. It can insert an immutable mapping version only with a current `PLATFORM_ADMIN` grant for that tenant. No mapping-write HTTP endpoint is exposed yet. Mapping keys include tenant, source and version, and the full source-local identity includes its realm. Account-scoped child entities added later must carry tenant in their composite references too.

Spring Session's shared tables hold authentication state and the selected account reference. They are employee-session infrastructure rather than tenant business records. Their runtime DML privileges are explicit. The local migration credential is used only by Flyway; JDBC account and session operations use the separate runtime role. Schema ownership and seed execution are not runtime authority.

The issue's owner review must identify the exact PR commit after automated checks pass. This foundation does not establish the parent epic's request-to-receipt integration, production deployment or public-demo acceptance.
