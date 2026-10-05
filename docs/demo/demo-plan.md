# Demonstration plan

Status: DispatchWorks v1 blueprint candidate for owner/source-owner acceptance under #48, revised on 2026-10-04. The owner requested PostgreSQL and Elasticsearch, removed MongoDB/Redis, and asked for ownership resolution beyond a direct business-ID lookup. This revision implements that design direction; exact blueprint acceptance remains pending.

## Story and source catalog

DispatchWorks runs fulfillment and support for Northstar Supply and Harbor Analytics. A depot transfers between those accounts during the demo week. Fulfillment cleanup follows the depot's owner at shipment time, then deletes dependent parcels/scans while preserving invoice-held trees. Support tickets give a simpler direct-account example. Elasticsearch delivery events use daily selection and conditional document deletion.

Three independently registered sources use two engine types: PostgreSQL fulfillment, PostgreSQL support and Elasticsearch delivery search. Each has separate credentials and accountable source ownership. The control-plane database and durable search operation ledger are not business-data sources. The detailed [catalog and selection oracle](../../demo/catalog/README.md), [fulfillment schema](../../demo/catalog/fulfillment.sql), [support schema](../../demo/catalog/support.sql), [search mapping](../../demo/catalog/delivery-search.json) and [scenario blueprint](../../demo/scenarios/README.md) define `dispatchworks-v1`, the UTC reference instant, account mappings, exact expected counts and review gates.

Hourly PostgreSQL inventory has exact timestamp selection. Daily search inventory supports UTC whole-day selection. Retention horizons are synthetic 90/60/30-day policies; changed or recreated search documents replace cache expiry/recreation scenarios. Date requests exclude timeless metadata; whole-account cleanup requires separate explicit approval. Neither a current depot owner nor a bare overlapping local account ID is sufficient to select data.

## Correctness and scenarios

Source owners approve exact versioned plans with mapping/policy versions and preconditions. PostgreSQL deletes dependencies and commits its operation receipt transactionally. Search freezes concrete index identity and document sequence identity, persists write-ahead attempts and acknowledged results in durable storage, and preserves unknown effects after a lost response. It never retries an unresolved delete by running a fresh broad query. Upstream re-ingestion, unregistered sources and backups remain disclosed limits. Fixture inspection verifies test correctness; Erasure reports adapter outcomes and does not independently verify deletion.

The scenario blueprint covers healthy cleanup, held trees, precise/coarse boundaries, historical ownership, account isolation, inconsistent ownership, stale approval, response loss, partial/unknown search results, changed/recreated documents, retention progression, explicit empty versus unavailable coverage, whole-account preferences, audit/closure and safe reset. Each run records the candidate, blueprint version, reference instant, generation and expected per-category measures.

## Setup, reset and viewer access

ERA-038 implements pinned container profiles, deterministic seed/inspect commands and expected results from the accepted blueprint. ERA-001 may use a minimal support fixture after blueprint acceptance. Reset quiesces workers/adapters, retires prior approvals and commands, restores allowlisted demo databases/index generations and consistent ledgers, and creates a fresh generation before resume. Saved audit evidence and recordings stay outside reset stores.

The initial public experience is a read-only guided tour plus project-owner controlled live sessions using temporary synthetic employee-role grants. General visitors cannot mutate requests, access raw databases/credentials, administer sources or reset fixtures. The product remains internal employee software. Unattended concurrent visitor sandboxes are deferred. Show the ownership path, inventory, owner review, outcomes and final audit, plus an architecture view and a recording fallback.

## Hosting feasibility

A single paid Linux VM with Docker Compose is the preferred reference for this demonstration. It accommodates the proxy/frontend, API, worker, identity provider, PostgreSQL control plane/source databases and adapter ledger, Elasticsearch, and three Java adapters. Keep stores private and expose only the intended HTTPS/identity routes. Compare 8 GiB and 16 GiB configurations after measuring heap limits, database memory, disk, startup time, and steady-state usage. Run large benchmark tiers separately rather than competing with portfolio visitors.

The 8 GiB/4-vCPU DigitalOcean Basic configuration is listed at USD 48/month, and the 16 GiB/8-vCPU configuration at USD 96/month as checked on 2026-10-03. Those are compute-only list prices; include tax, domain, backups, extra storage, and any traffic/registry charges in the final quote. [DigitalOcean pricing](https://www.digitalocean.com/pricing/droplets). Hetzner is another VM candidate with European locations and Docker support, but this research could not extract an exact current plan price from its rendered price calculator, so no price comparison is asserted. [Hetzner cloud](https://www.hetzner.com/cloud/).

A managed multi-service platform is possible but introduces separate service/disk/database costs and more configuration for this many independent processes. Render documents its [service types](https://render.com/docs/service-types). Its free offering is a poor fit for a durable always-available reference: free PostgreSQL expires after 30 days, and free key-value state is not continuously persisted. [Render free-tier limits](https://render.com/docs/free). A static architecture page and recorded walkthrough can be hosted cheaply if continuous live hosting is not worth the measured cost.

ERA-041 owns the final decision record: dated provider quote, service topology, measured resource envelope, cost breakdown, uptime mode, domain/TLS, region, backup/restore, maintenance burden, and teardown. It can research and draft the comparison before application code exists. Provisioning waits for a concrete owner-approved provider/budget and uses measured values from the setup/deployment work. No infrastructure purchase, account creation, or deployment is authorized by this planning task.

Feasibility conclusion: hosting is technically plausible on a paid VM, but application capacity and recurring cost acceptance remain unverified. ERA-042 accepts a public HTTPS demo only after local scenarios, deployed recovery/UAT, and the hosting decision pass. If live hosting fails a resource or budget gate, retain local reproduction and the recorded tour; do not mark the live-demo requirement satisfied. The owner may explicitly revise that requirement to a static-only presentation.

## Ownership and dependencies

EPIC-10 starts with ERA-037 acceptance. ERA-038 setup and ERA-041 hosting research can then overlap foundation work. ERA-011 owns the Elasticsearch adapter in EPIC-03. ERA-039 owns the fulfillment ownership/hold extension of the initial PostgreSQL adapter in EPIC-10. ERA-040 integrates both PostgreSQL sources and search with real case/audit workflows. Existing worker, case, UI, deployment and UAT prerequisites remain in force; source replacement does not waive them.

ERA-032 includes the combined deployed walkthrough; ERA-042 requires actual public HTTPS/UAT evidence. ERA-036 records visibility and scale for final handoff. EPIC-05 owns shared recovery and EPIC-08 owns deployment mechanics. Coordinate source/deployment profiles with one integration owner. Optional future engines require explicit scope and recovery contracts.
