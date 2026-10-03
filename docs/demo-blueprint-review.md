# Issue #48 candidate review

Review unit: DispatchWorks v1 catalog, two logical SQL schemas, Elasticsearch mapping, scenario blueprint, and the linked requirements/architecture/demo plan. Delivery is a blueprint only. The owner instructed the engine change and complex ownership examples in this conversation on 2026-10-04. The exact resulting design has not yet been accepted.

## Acceptance coverage

| Issue criterion | Candidate evidence | Gate |
| --- | --- | --- |
| Required source catalog revised to PostgreSQL/Elasticsearch | [Catalog](../demo/catalog/README.md) identifies fulfillment, support and delivery-search with separate credentials/owners | Owner/source-owner review pending |
| Two accounts, mappings, roles, inventory, precision, retention and whole-account categories | Catalog fixes overlapping local IDs, UTC clock, 90/60/30-day horizons and separate metadata approval | Defined; real source tests follow in #49 |
| Ownership beyond direct account lookup | [Fulfillment schema](../demo/catalog/fulfillment.sql) and catalog define dated assignments, shipment/parcel/scan dependencies, invoice holds and exact selection oracle | Defined; real join/locking tests follow in #50 |
| Simple deletion cases | [Support schema](../demo/catalog/support.sql) and [search mapping](../demo/catalog/delivery-search.json) define simpler ownership | Defined; real adapter conformance follows in foundation and ERA-011 |
| Scenarios with expected results | [Scenario blueprint](../demo/scenarios/README.md) specifies healthy/held, mismatch, isolation, lost responses, retention/recreation, unknown effects, audit and reset | Defined; execution follows in #51 |
| Initial visibility model | Read-only public tour and owner-controlled live employee sessions | Defined; public URL/UAT follows in #53 |
| Exact schemas/conventions/clock revision accepted | PR commit containing the blueprint and `dispatchworks-v1` is the acceptance unit | Pending explicit owner acceptance; do not unblock #12/#49 yet |

## Advisory review and verification limits

One implementation writer performed an advisory self-review under Pathfinder's adopted advisory policy. No independent reviewer was used. The selection oracle was reviewed by tracing the half-open request and assignment intervals: Northstar owns F-start/F-late; Harbor owns F-switch; F-held retains all descendants. Selected child timestamps do not alter parent ownership. Overlapping local account 7 requires a realm discriminator in each source. Search uses frozen sequence/index identity and explicitly cannot prove exact effects after an uncheckpointed response loss.

Run repository policy tests and local planning/candidate integrity checks against the frozen revision; retain actual command results in the PR and Pathfinder ledger. These checks verify repository/backlog coherence, not real-engine behavior. SQL files are logical contracts; downstream setup must add roles, nonoverlap constraints and the documented concurrency locks. Elasticsearch mapping types alone do not enforce UTC-midnight dates or immutable ownership fields; ingest and adapter validation must enforce those contracts. No application, source setup, combined integration, deployment or public UAT has been executed by #48.

The historical accepted planning digest remains unchanged. This candidate supersedes its source-engine decisions within the user's requested scope; it does not fabricate acceptance of the new blueprint. GitHub native issue relationships remain the source of truth and existing blockers are preserved.
