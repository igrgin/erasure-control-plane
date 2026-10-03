# Architecture and adapter contract

Status: proposed design. Keep the control plane as a modular Java/Spring Boot application with React/TypeScript, PostgreSQL, Flyway migrations, and independent Java adapters. Start with Maven and a Java LTS version supported by the selected stable Spring Boot release. Pin compatible versions and container digests in the first implementation issue rather than guessing version numbers in the plan.

## Runtime boundaries

The browser talks to the control-plane API. Adapters run beside their sources, hold the source credentials, and initiate outbound authenticated connections to Erasure. They publish inventory, poll commands, and report results. Erasure never needs general database credentials for registered sources and never accepts arbitrary SQL from the browser.

Use OpenID Connect employee login with a local Keycloak instance for the demonstration and an enterprise identity-provider boundary for later deployment. Use a backend session for the browser, CSRF protection for cookie-authenticated commands, and OAuth2 service credentials for adapters. Store shared sessions in PostgreSQL initially so multiple API instances work. Spring Security documents the underlying [OAuth2 support](https://docs.spring.io/spring-security/reference/servlet/oauth2/).

Use a relational current-state model, a durable job/command table, and append-only audit events. State changes, audit entries, and queued commands commit in the same PostgreSQL transaction. Workers claim leased jobs; they never hold database locks across an adapter network call. This is a durable workflow, not an in-memory scheduler or a promise of exactly-once delivery.

## Modules and ownership

| Module | Owns | Exposes |
| --- | --- | --- |
| accounts-access | Business-account references, source-local mapping versions, employee tenant grants | Authorized account resolution and grant checks |
| source-registry | Sources, owner assignments, principal bindings, capability/policy versions | Source metadata and scope snapshots |
| inventory | Bucket summaries, stream revisions, completeness and freshness | Account/source inventory queries and ingestion |
| cases | Requests, per-source cases, blockers, closure | Request and disposition transitions |
| proposals-decisions | Immutable proposals and owner decisions | Proposal validation and approval lookup |
| execution | Durable jobs, commands, attempts, leases, receipts | Dispatch/recovery and adapter command endpoints |
| audit | Append-only event records and authorized exports | Timeline and evidence queries |

Modules own their tables and repositories. Other modules call public interfaces, not each other's repositories or internal entities. A small orchestration service coordinates local atomic transitions through those interfaces; shared transaction context does not erase ownership. Verify module dependencies in CI. [Spring Modulith verification](https://docs.spring.io/spring-modulith/reference/verification.html) checks module cycles and access to internal packages. Extraction into separate services is a later decision driven by measured pressure.

## Tenant isolation

Every account-scoped entity carries `tenant_id`, including jobs, receipts, inventory, audit events, exports, and source-local mappings. Cross-references use composite tenant/entity constraints where applicable. Source definitions and adapter credentials are operating-company resources; each adapter principal has a source binding and an explicit tenant scope, which may span many accounts. Adapter credentials are a powerful grant and deserve separate controls from employee sessions.

Enforce tenant grants in application services and PostgreSQL row policies for account-scoped tables. Use distinct migration-owner and runtime roles; runtime roles must not have `BYPASSRLS`. Set tenant context per transaction, never as an unreset pooled connection property. Inventory batches that span tenants authenticate the adapter scope and process each authorized tenant in its own context. Cross-tenant administrative reads and job discovery use narrowly scoped control tables/services, not an all-powerful browser role. PostgreSQL notes that owners normally bypass row security; tests must use the actual runtime role. [Row security policies](https://www.postgresql.org/docs/18/ddl-rowsecurity.html).

Internal business references are canonical. The adapter resolves source-local IDs through its declared mapping version. Credentials and raw records stay outside proposals and audit payloads. Tenant-scoped identifiers in an export still require access control.

## Adapter protocol

Plan an OpenAPI contract and contract-test fixtures, with version negotiation and explicit compatibility errors. All account operations bind source, tenant, request, proposal version, command ID, and correlation ID.

| Exchange | Required content | Safety rule |
| --- | --- | --- |
| Capabilities and heartbeat | Protocol version, supported actions, retention/time rules, batch limits, availability | Administrator authorizes the source/principal binding; policy revisions invalidate affected proposals |
| Inventory publication | Publication ID, stream/revision, tenant, explicit bucket bounds, measure/unit, observed time, coverage/completeness | Dedupe and validate scope; support authoritative bucket replacement, tombstones, and initial resync |
| Proposal command/result | Request interval, source snapshot, mapping/policy versions; selection token, action, impact, exclusions, expiry | Counts alone never constitute a proposal; plans are immutable |
| Execution command | Approved proposal digest/version, approval reference, stable operation key | Validate all bindings and source preconditions before any effects |
| Operation status/receipt | Operation key, status, checkpoints, affected measures, exclusions, errors, adapter/source version | Durable source-side operation ledger returns the same outcome for duplicate commands |

Erasure polls neither raw source records nor source databases. Adapters poll a source-scoped control-plane command endpoint, acknowledge leases, and send receipts. The control plane may retry delivery of an existing command, but may not manufacture a new operation key to hide uncertainty. HTTP alone does not make a destructive request retry-safe; [HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110.html) requires knowing that retry semantics are safe.

For the transactional demo adapter, cleanup and its local operation receipt commit together. For the chunked adapter, durable per-chunk checkpoints and idempotent selection/actions make interrupted operations resumable. New adapter types must demonstrate an equivalent safe recovery mechanism or declare manual recovery. Status lookup reads the adapter's operation ledger. It is reconciliation of reported execution, not independent deletion verification.

## States and concurrency

A per-source case progresses through discovery/proposal, owner review, approval, queued execution, running execution, and disposition. Use `BLOCKED`, `REJECTED`, `RETAINED`, `NO_DATA`, `REPORTED_COMPLETED`, `PARTIAL`, `FAILED`, `UNKNOWN`, and `CANCELLED` as explicit outcomes or intervention states. Keep attempts separate from the per-source case so retries do not erase history.

Use optimistic versions for employee decisions. Exactly one of two conflicting owner actions succeeds. Execution leases have fencing tokens; stale workers cannot advance current state. Bound concurrent operations per source and per tenant. An account/source lock coordinates overlapping cleanup requests, but source preconditions remain necessary because external source changes can occur independently.

Before dispatch, re-check owner authority, approval expiry, capability/mapping versions, proposal digest, cancellation, and serialization. The adapter repeats the relevant checks before effects. A crash between a committed approval and dispatch leaves a recoverable queued job. A crash after cleanup but before receipt leaves an unknown attempt until the stable operation key resolves it.

## Repository layout to build later

Use `backend/` for the control plane, `frontend/` for React, `adapters/` for the three demonstrators and reusable protocol client, `contracts/` for OpenAPI/examples, `deploy/` for container configuration, `tests/` for cross-system scenarios/load harnesses, and `docs/` for architecture and runbooks. Share protocol types only where useful; do not share source-specific business rules with the control plane.

## Synthetic demonstration sources

The [demo plan](demo-plan.md) selects two PostgreSQL source databases and Elasticsearch as three separately registered first-release sources. PostgreSQL sources commit cleanup and local receipts together. Elasticsearch uses conditional deletes against a frozen document/index selection and a durable PostgreSQL adapter ledger. Unacknowledged search effects remain unknown because the ledger and search engine do not share a transaction. Demo setup/reset/public-tour code is separate from core case and execution modules. Public demo roles exercise synthetic employee grants; company operation remains internal.
