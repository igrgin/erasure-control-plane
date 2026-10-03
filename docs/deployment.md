# Deployment plan

Status: a plan to implement and verify in EPIC-08. No host, cloud account, domain, or running environment exists yet. The reference target is a Linux VM with Docker Compose; cloud-provider selection can wait until deployment without changing the architecture.

## Small complete environment

Run a reverse proxy serving React and routing API traffic, the control-plane API, a worker process using the same backend artifact in a worker profile, PostgreSQL, Keycloak, three independent adapters and their synthetic fulfillment/support PostgreSQL databases and Elasticsearch source store. Use distinct PostgreSQL databases/users for the control plane, each source and the search adapter ledger, plus a private Elasticsearch service. Keep source stores accessible only to their adapters. Expose HTTPS to the browser; the control plane, worker, identity provider, and adapter ingress use configured trusted internal routes.

Provide a local Compose environment and a deployment override. Docker documents [single-server Compose deployment](https://docs.docker.com/compose/how-tos/production/). This represents production process boundaries on one host; it provides no host-level high availability.

Begin with a measured demo resource envelope, for example 4 vCPU, 8 GiB RAM, and persistent SSD storage. This is a hypothesis for synthetic workloads, not a capacity guarantee or a hardware purchase recommendation. EPIC-08/EPIC-09 record actual consumption and adjust the envelope.

## Build and promotion

1. A PR runs backend tests, module checks, real-PostgreSQL integration tests, frontend checks, adapter contracts, and selected end-to-end scenarios.
2. A tagged candidate builds immutable backend, frontend, and adapter images; record digests, dependency inventory, test results, and source revision.
3. A project-owner approved GitHub Actions environment deploys those exact digests to staging first. Infrastructure secrets remain outside the repository.
4. Take a backup, run migrations once with the migration role, and deploy API/workers with health checks. Drain workers and preserve operation ledgers during replacement.
5. Run login, inventory, owner review, approved execution, receipt, and audit smoke checks on dedicated synthetic tenants. Record the deployed digests and results.
6. Promote the same candidate to the demonstration environment after review. Failed checks stop promotion.

Use expand/contract schema changes when old and new workers may overlap. Roll back application images only when the schema and protocol remain compatible. A rollback cannot reverse source cleanup. For destructive schema changes, use a forward repair plan rather than implying image rollback fixes the database.

## Configuration and security

Parameterize domain, TLS configuration, identity-provider endpoints, database URLs, session settings, adapter source/principal bindings, timeouts, job concurrency, and retention settings. Include `.env.example` without credentials. Use a deployment secret store or protected injected files; rotate adapter and database credentials through a tested runbook.

Restrict management/metrics endpoints to administrators. Configure log redaction, network allowlists, secure cookies, trusted proxy headers, CSRF, and export authorization. Back up control-plane state, identity-provider configuration, and adapter operation ledgers with encryption and access controls. Source backups retain their own declared policies and are not implicitly covered by cleanup.

## Operational acceptance

- A clean machine can deploy from documented prerequisites and image digests.
- Two business accounts and three source adapters complete the full walkthrough.
- Restarting API, worker, and adapter processes preserves queued commands and known outcomes.
- A lost execution response is resolved through the adapter operation ledger, without a second uncontrolled cleanup.
- A backup is restored to an isolated environment. Jobs start paused until source-side operation keys reconcile; stale restored state cannot replay already executed operations.
- Credential rotation and application rollback are exercised with recorded results.
- Operators can detect queue age, stale inventory, adapter outage, approval backlog, unknown outcomes, and database capacity pressure.

Proposed demonstration recovery objectives are RPO 24 hours for control-plane records and RTO 4 hours for restoration. They are targets to measure, not achieved promises. Adapter dedupe history must outlive retry and recovery windows. Losing that ledger makes automatic execution unsafe; recovery must stop until the owner resolves it.

A runbook identifies the project owner as deployment/incident owner, gives pause-dispatch and restore procedures, and describes escalations to source owners. Alerts are exercised locally; integration with a real paging service is future work. All demonstrated data is synthetic.

## Public demo coordination

EPIC-10 owns the [demo blueprint and hosting assessment](demo-plan.md). Initial packaging can use the baseline source; final deployed UAT includes all three required stores/adapters and ERA-040 guided scenarios. ERA-041 compares hosts and estimated recurring costs, then ERA-042 checks the measured full-stack envelope and owner-approved budget before publishing a URL through this deployment machinery.

The default public experience is a synthetic read-only tour plus owner-controlled live employee-role sessions. Source/configuration/reset administration remains private. Reset quiesces dispatch and rotates the demo run generation so old commands cannot affect freshly seeded data. The demo has its own maintenance/teardown owner and preserves recordings when temporarily offline. No live demo is claimed complete without external browser evidence.
