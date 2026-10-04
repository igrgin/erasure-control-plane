# Demonstration plan

Status: DispatchWorks v1 blueprint candidate for owner/source-owner acceptance under #48, revised on 2026-10-04. The owner requested PostgreSQL and Elasticsearch, removed MongoDB/Redis, and asked for ownership resolution beyond a direct business-ID lookup. This revision implements that design direction; exact blueprint acceptance remains pending.

## Story and source catalog

DispatchWorks runs fulfillment and support for Northstar Supply and Harbor Analytics. A depot transfers between those accounts during the demo week. Fulfillment cleanup follows the depot's owner at shipment time, then deletes dependent parcels/scans while preserving invoice-held trees. Support tickets give a simpler direct-account example. Elasticsearch delivery events use daily selection and conditional document deletion.

Three independently registered sources use two engine types: PostgreSQL fulfillment, PostgreSQL support and Elasticsearch delivery search. Each has separate credentials and accountable source ownership. The control-plane database and durable search operation ledger are not business-data sources. The detailed [catalog and selection oracle](../demo/catalog/README.md), [fulfillment schema](../demo/catalog/fulfillment.sql), [support schema](../demo/catalog/support.sql), [search mapping](../demo/catalog/delivery-search.json) and [scenario blueprint](../demo/scenarios/README.md) define `dispatchworks-v1`, the UTC reference instant, account mappings, exact expected counts and review gates.

Hourly PostgreSQL inventory has exact timestamp selection. Daily search inventory supports UTC whole-day selection. Retention horizons are synthetic 90/60/30-day policies; changed or recreated search documents replace cache expiry/recreation scenarios. Date requests exclude timeless metadata; whole-account cleanup requires separate explicit approval. Neither a current depot owner nor a bare overlapping local account ID is sufficient to select data.

## Correctness and scenarios

Source owners approve exact versioned plans with mapping/policy versions and preconditions. PostgreSQL deletes dependencies and commits its operation receipt transactionally. Search freezes concrete index identity and document sequence identity, persists write-ahead attempts and acknowledged results in durable storage, and preserves unknown effects after a lost response. It never retries an unresolved delete by running a fresh broad query. Upstream re-ingestion, unregistered sources and backups remain disclosed limits. Fixture inspection verifies test correctness; Erasure reports adapter outcomes and does not independently verify deletion.

The scenario blueprint covers healthy cleanup, held trees, precise/coarse boundaries, historical ownership, account isolation, inconsistent ownership, stale approval, response loss, partial/unknown search results, changed/recreated documents, retention progression, explicit empty versus unavailable coverage, whole-account preferences, audit/closure and safe reset. Each run records the candidate, blueprint version, reference instant, generation and expected per-category measures.

## Setup, reset and viewer access

ERA-038 implements pinned container profiles, deterministic seed/inspect commands and expected results from the accepted blueprint. ERA-001 may use a minimal support fixture after blueprint acceptance. Reset quiesces workers/adapters, retires prior approvals and commands, restores allowlisted demo databases/index generations and consistent ledgers, and creates a fresh generation before resume. Saved audit evidence and recordings stay outside reset stores.

The initial public experience is a read-only guided tour plus project-owner controlled live sessions using temporary synthetic employee-role grants. General visitors cannot mutate requests, access raw databases/credentials, administer sources or reset fixtures. The product remains internal employee software. Unattended concurrent visitor sandboxes are deferred. Show the ownership path, inventory, owner review, outcomes and final audit, plus an architecture view and a recording fallback.

## Hosting feasibility

The [dated hosting assessment](demo-hosting/README.md) compares a single paid Linux VM, paid managed multi-service hosting and static/recorded presentation for the complete DispatchWorks stack. The research candidate under #52 was checked on 2026-10-04. Its estimated monthly totals before tax/overages are USD 64.27 for an 8 GiB DigitalOcean Basic VM, USD 121.87 for 16 GiB, USD 321.67 for the explicit Render topology, and USD 6.67 for the static tour with recording storage/domain allowances. Domain and resource figures are estimates; owner budget/provider acceptance remains pending.

A paid VM in Frankfurt is the conditional recommendation. The estimated 5.45-9.65 GiB resident-memory range makes 8 GiB a measurement experiment; 16 GiB offers more room but is not proven capacity. Keep source stores/management private, expose intended HTTPS and identity routes, and retain approval, tenant isolation and durable operation semantics. Run large benchmark tiers separately.

The [full-stack validation protocol](demo-hosting/validation.md) requires pinned candidate evidence, peak resource measurements, guided/reset scenarios, backup/restore, restart/rollback, cost acceptance and external public-browser UAT before #53 launch. No application capacity, infrastructure purchase or deployed public demo is claimed by this research. Provisioning requires separate explicit owner authorization.

If the measured live stack cannot meet the owner-approved resource/budget constraints, record the blocker and preserve local reproduction plus a static tour/recording. Static visibility alone does not satisfy REQ-15's public HTTPS tour plus controlled live session; a static-only outcome requires an explicit owner scope revision. The [delivery record](demo-hosting/delivery.md) maps #52 acceptance criteria and remaining owner actions.

## Ownership and dependencies

EPIC-10 starts with ERA-037 acceptance. ERA-038 setup and ERA-041 hosting research can then overlap foundation work. ERA-011 owns the Elasticsearch adapter in EPIC-03. ERA-039 owns the fulfillment ownership/hold extension of the initial PostgreSQL adapter in EPIC-10. ERA-040 integrates both PostgreSQL sources and search with real case/audit workflows. Existing worker, case, UI, deployment and UAT prerequisites remain in force; source replacement does not waive them.

ERA-032 includes the combined deployed walkthrough; ERA-042 requires actual public HTTPS/UAT evidence. ERA-036 records visibility and scale for final handoff. EPIC-05 owns shared recovery and EPIC-08 owns deployment mechanics. Coordinate source/deployment profiles with one integration owner. Optional future engines require explicit scope and recovery contracts.
