# Scaling plan and evidence

The first release represents a larger installation because it keeps the same boundaries and safety rules: one shared control plane, account isolation, independently deployed adapters, owner-approved immutable proposals, durable commands, and source-side recovery. Increasing replica counts must preserve those rules.

It is not a small high-availability production cluster. The demo shares a host, uses synthetic sources, and cannot establish real-world capacity or source-specific deletion safety.

## Growth paths

| Pressure | Demonstrated foundation | Next change | Evidence required before adopting it |
| --- | --- | --- | --- |
| More customer accounts | Tenant-scoped keys, authorization, database policies, paginated views | Index by tenant/source/time, enforce ingestion and dispatch quotas | Query plans and adversarial tenant-isolation tests |
| More inventory buckets | Batch publications, dedupe, revisions, source-specific granularity | Bulk ingestion, bounded staging, time partitioning and approved retention/downsampling | Measured ingest lag, index size, maintenance cost, and completeness after resync |
| More web users | Multiple-capable API with shared sessions; state in PostgreSQL | API replicas behind a load balancer; managed PostgreSQL HA | Concurrent decision tests and session continuity under instance loss |
| More jobs | Durable leased queue with fencing and stable operation keys | Additional workers; source/tenant fairness and separate pools | Duplicate-delivery, lease-expiry, starvation, and crash tests |
| More source systems | Versioned protocol and independent adapters | Adapter SDK, conformance suite, credential rotation, per-source rate limits | Compatibility tests and source-owner review of each adapter |
| Queue contention | Indexed queue and bounded transactions | Partition work by source or tenant; then introduce a broker if measurements justify it | Contention profile; preserved outbox, ordering, and dedupe semantics |
| More audit history | Append-only events and separate export read path | Time partitions, authorized archive/export jobs, read replica | Audit completeness, export isolation, archive/restore drill |
| Source blast radius | Per-source bulkheads and retry budgets | Dedicated source pools, shard large source workloads, circuit breakers | A failing source does not stall unrelated tenants/sources |
| Organizational growth | Explicit grants and source-owner groups | Corporate identity federation, delegated administration, approval policies | Revocation latency and cross-team authorization tests |
| Multiple operating companies | One-company tenant semantics are explicit | Add an organization boundary above business accounts and re-scope sources/principals | New domain/security specification and migration; this is a product extension |

PostgreSQL supports [queue-like consumers using SKIP LOCKED](https://www.postgresql.org/docs/16/sql-select.html) and [table partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html). These are implementation options, not evidence of achieved throughput.

## Inventory economics

Account count alone is a poor sizing measure. Account/source pairs, bucket count, categories, revision rate, and retention dominate inventory storage.

For a deliberately high estimate, 10,000 accounts across 20 sources with one hourly measurement for 90 days means `10,000 × 20 × 24 × 90 = 432,000,000` current bucket rows before indexes, category dimensions, or history. Daily buckets would mean 18,000,000. Actual sources may be sparse; revisions add write volume. Do not provision based only on the number of accounts.

Keep exact detailed summaries only for a declared inventory horizon; allow source-specific coarser history where the UI discloses precision. Do not let inventory downsampling change request selection semantics. Use tombstones or authoritative replacements for retention changes and deletions. Separate current inventory from durable decision evidence so frequent refreshes do not bloat the audit with every bucket.

## Scale demonstration in EPIC-09

Define deterministic data seeds and three workload tiers: smoke with 2 tenants/3 sources, normal with 1,000 tenants/10 sources, and a storage-focused tier with 10,000 tenants/20 source identities using bounded history. State the chosen bucket horizon and sparse/dense distribution so the workload is reproducible. Extra source identities may use simulated adapters; the three real demonstrators still prove source behavior.

Provisional targets on a documented test environment:

- Account inventory and request-detail reads: p95 under 500 ms at 20 concurrent employee sessions.
- Inventory ingestion: 1,000 bucket updates per second sustained for 10 minutes, with observed query performance and write amplification recorded.
- Approval-to-command availability: p95 under 5 seconds for healthy adapters with a 1-second poll interval, excluding owner waiting time and source execution duration.
- A source outage does not cause unbounded retries or prevent an unrelated source from dispatching.
- Two workers safely compete for jobs; process termination and lease expiry cannot create duplicate uncontrolled effects.

These are engineering targets to test and revise with recorded reasons, not promises. Measure API latency, job age, database CPU/I/O, rows/index sizes, connection usage, retry count, adapter latency, and impact accuracy. Retain raw results and configuration. If a target fails, diagnose the bottleneck and repeat only the affected workload after repair.

## Larger deployment

Move the same images to a managed container platform with multiple API and worker replicas, load balancing, managed PostgreSQL failover/backups, enterprise identity, secrets management, centralized telemetry, and audited deployment approvals. Adapters remain near their source systems and use outbound connections.

Start by scaling replicas and improving storage. Extract inventory ingestion or execution workers into separate services only when workload isolation, deployment ownership, or database contention justifies the extra network boundary. Extraction requires an outbox/inbox or equivalent durable messaging, explicit contracts, and retained tenant/operation identities. A broker does not remove source-side dedupe or solve a lost execution result.

Scale acceptance includes fairness: one large account or misbehaving adapter cannot monopolize ingestion, queue slots, database connections, or export capacity. Test quotas and bulkheads alongside throughput. Growth to more operating companies would require a new organization boundary; it is not a switch that turns business-account IDs into SaaS organization IDs.
