# Demonstration plan

Status: proposed design and hosting feasibility assessment, researched on 2026-10-03. EPIC-10 owns the demo blueprint, synthetic environment, cache adapter, guided scenarios, hosting decision, and visible launch. The public demonstration represents internal employee workflows; it does not turn Erasure into a customer-facing service.

## What the demo should prove

A viewer should understand how a single business account has data across heterogeneous stores, how those stores summarize their data, why their proposed cleanup differs, who approves it, how failures remain visible, and what closure actually means. Use three small real storage engines and adapters, not three names attached to a mocked endpoint.

Two mandatory business accounts, Northstar Supply and Harbor Analytics, demonstrate isolation. Reuse some source-local IDs across them deliberately. Each account has several dates of fixture data, with hourly and daily summaries, boundary records, explicit empty coverage, expired records, and one retained subset. Use generated names/identifiers and no imported customer data.

## Required source catalog

| Demo source | Storage | Business data | Summary and selection | Cleanup behavior | Architectural point |
| --- | --- | --- | --- | --- | --- |
| Business records | PostgreSQL, separate source database/user | Orders, account metadata, retained invoice references | Hourly summaries; exact UTC timestamp selection | Delete eligible order/detail rows in a transaction; disclose retained invoice references | Relational dependencies, policy exceptions, atomic cleanup/receipt |
| Usage documents | MongoDB | Daily usage/event documents with nested account labels and metadata | Daily buckets; UTC calendar-day selection for the demo | Remove defined account labels/identifiers or delete eligible documents in bounded chunks | Document relationships, residual data, checkpoints, source-specific time precision |
| Account cache | Redis | Account-keyed cached responses and derived lookup entries | Hourly summary of explicitly timestamped entries, with observed TTL and completeness | Invalidate only the approved account/key generations; record already-expired keys separately | Expiry, stale estimates, concurrent recreation, nontransactional recovery |

Policies are synthetic examples, not legal defaults. Begin with a 90-day relational horizon, a 30-day document horizon, and cache TTLs measured in minutes/hours; ERA-037 fixes category exceptions and exact test values. Keep time dimensions explicit. TTL alone cannot identify a record's event date, so cache values carry `tenantId`, `observedAt`, source category, and a generation/version. Global, timeless account metadata is a separately disclosed whole-account category.

PostgreSQL remains the control-plane database as well as one separate demo source; credentials and data ownership stay distinct. MongoDB source behavior belongs in ERA-011, not a duplicate demo adapter. Configure MongoDB as a replica-set deployment when using multi-document transactions. Its documentation distinguishes replica-set transactions from unsupported standalone transactions. [MongoDB transaction considerations](https://www.mongodb.com/docs/manual/core/transactions-production-consideration/). The small demo setup does not establish production replica-set availability.

Redis is a source to clean, not Erasure's durable workflow store. Maintain source indexes keyed by tenant and time so the adapter can freeze a selection. If a scan is used, deduplicate it and account for a changing keyspace; Redis documents [SCAN behavior](https://redis.io/docs/latest/commands/scan/). Redis [TTL](https://redis.io/docs/latest/commands/ttl/) distinguishes expired/missing keys and keys without expiry. Never use `FLUSHDB`, `FLUSHALL`, or a broad wildcard to implement customer cleanup.

## Source-side execution correctness

Use the existing versioned adapter protocol and authorization boundaries. The PostgreSQL adapter commits its receipt with cleanup. The MongoDB adapter checkpoints bounded work with an approved generation/precondition. The Redis adapter persists its plan, operation key, and recovery state outside disposable cache entries and checks each selected key's generation before invalidation. A recreated key must not be deleted under an earlier approval.

Cache expiry between proposal and execution can produce an already-absent result. Distinguish deleted, expired/already absent, changed generation, and unknown effects. If a crash loses an exact count, preserve that uncertainty rather than inventing an affected count from the current cache. Demonstrate safe duplicate execution and stop automatic recovery if its durable operation ledger is unavailable.

The demo does not claim that cache invalidation prevents upstream services from repopulating data. Include one recreated key and show that new data falls outside the frozen operation. Record upstream re-ingestion and unregistered backups as limits. Verification tests may inspect synthetic stores to check adapter correctness; Erasure itself still does not independently verify deletion after execution.

## Reproducible setup and reset

ERA-038 creates container source profiles, deterministic seed generators, schemas/indexes, source-local account mappings, expected inventory, and expected cleanup results. ERA-001 may use a minimal PostgreSQL fixture after the blueprint is accepted; it does not have to wait for the complete three-store environment.

Provide documented commands to start sources, seed, inspect fixture expectations, quiesce dispatch, and reset. Seed data relative to an explicit reference instant so retention cases remain useful on a later demo day. Include the seed/version/reference instant in every scenario record. Use a controllable clock for deterministic tests and the actual current clock for the hosted TTL examples.

A reset is a demonstration administration operation, never a product erasure request. Drain/stop jobs, isolate the active run, reset only allowlisted demo databases/key prefixes, restore fixture state and consistent operation ledgers, and create a new run generation before resuming. Do not resurrect a source dataset while stale approvals or commands can still act on it. Keep a saved scenario result/recording outside the resettable store for portfolio evidence.

## Viewer experience and access

The default publicly visible experience is a read-only guided tour of inventory, proposals, owner decisions, execution attempts, and final audit evidence using synthetic tenants. Offer project-owner controlled live sessions with temporary demo operator/source-owner credentials to perform real cleanup. Demo role assignments represent company employees. General visitors receive no source-administration, credential, raw database, or deployment access.

This is the small baseline for public visibility. An unattended interactive sandbox with one isolated run per visitor can be a later extension. The first version must not pretend that a shared mutable scenario isolates concurrent visitors. Limit active guided runs, requests, payload sizes, and export volume. Keep reset/fixture admin endpoints private. The operating product remains employee-only.

The guided script should show a healthy deletion/transformation/cache invalidation, retention exception, account isolation attempt, precision mismatch, adapter outage/lost receipt, cache expiry/recreation, and closure with complete per-source dispositions. Show the registered-source and adapter-reporting limitations in the tour. Include an architecture view and a short recording as a fallback when live hosting is offline.

## Hosting feasibility

A single paid Linux VM with Docker Compose is the preferred reference for this demonstration. It accommodates the proxy/frontend, API, worker, identity provider, PostgreSQL control plane/source databases, MongoDB, Redis, and three Java adapters. Keep stores private and expose only the intended HTTPS/identity routes. Compare 8 GiB and 16 GiB configurations after measuring heap limits, database memory, disk, startup time, and steady-state usage. Run large benchmark tiers separately rather than competing with portfolio visitors.

The 8 GiB/4-vCPU DigitalOcean Basic configuration is listed at USD 48/month, and the 16 GiB/8-vCPU configuration at USD 96/month as checked on 2026-10-03. Those are compute-only list prices; include tax, domain, backups, extra storage, and any traffic/registry charges in the final quote. [DigitalOcean pricing](https://www.digitalocean.com/pricing/droplets). Hetzner is another VM candidate with European locations and Docker support, but this research could not extract an exact current plan price from its rendered price calculator, so no price comparison is asserted. [Hetzner cloud](https://www.hetzner.com/cloud/).

A managed multi-service platform is possible but introduces separate service/disk/database costs and more configuration for this many independent processes. Render documents its [service types](https://render.com/docs/service-types). Its free offering is a poor fit for a durable always-available reference: free PostgreSQL expires after 30 days, and free key-value state is not continuously persisted. [Render free-tier limits](https://render.com/docs/free). A static architecture page and recorded walkthrough can be hosted cheaply if continuous live hosting is not worth the measured cost.

ERA-041 owns the final decision record: dated provider quote, service topology, measured resource envelope, cost breakdown, uptime mode, domain/TLS, region, backup/restore, maintenance burden, and teardown. It can research and draft the comparison before application code exists. Provisioning waits for a concrete owner-approved provider/budget and uses measured values from the setup/deployment work. No infrastructure purchase, account creation, or deployment is authorized by this planning task.

Feasibility conclusion: hosting is technically plausible on a paid VM, but application capacity and recurring cost acceptance remain unverified. ERA-042 accepts a public HTTPS demo only after local scenarios, deployed recovery/UAT, and the hosting decision pass. If live hosting fails a resource or budget gate, retain local reproduction and the recorded tour; do not mark the live-demo requirement satisfied. The owner may explicitly revise that requirement to a static-only presentation.

## Ownership and dependencies

EPIC-10 can start before the foundation: ERA-037 defines the demo design, then ERA-038 setup and ERA-041 hosting research can run alongside EPIC-01. ERA-001 consumes the accepted blueprint. ERA-011 consumes the source environment when building the MongoDB adapter. ERA-039 builds the Redis adapter after registration/capability and worker contracts are available. ERA-040 integrates all three sources with the real case/audit workflows. ERA-032 includes that walkthrough in deployed UAT; ERA-042 makes the accepted candidate publicly visible. ERA-036 records public visibility alongside scale evidence for final handoff.

EPIC-03 owns heterogeneous proposal behavior and MongoDB adapter code. EPIC-05 owns the shared execution/recovery machinery. EPIC-08 owns deployment/promotion/restore mechanics. EPIC-10 owns fixture infrastructure, Redis source behavior, presentation, and demo hosting choices. Coordinate `deploy/` through separate profiles and one integration owner.

Required storage diversity is relational, document, and cache. Object storage, search indexes, file shares, and message archives are optional follow-up sources; they need their own version/versioned-object and retention semantics and should not delay this release without an explicit scope change.
