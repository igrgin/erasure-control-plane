# EPIC-02: Registered source coverage and account inventory

Type: epic. Milestone: v0.1 end-to-end demonstration. Status: proposed.

Delivery and acceptance owner: project owner. This epic groups four coupled implementation issues into one application capability.

## Application capability

The source catalog and reliable per-account view of what company sources report.

## Why these issues belong together

Registration and capabilities give inventory its identity and meaning; ingestion and the account view make that information usable. An individual child issue can be integrated and reviewed independently, but the epic is complete only when all four issues and the combined demonstration pass.

## Start prerequisites and external blockers

Required completed epics: [EPIC-01](EPIC-01.md), including its shared contract acceptance.

Additional entry issue prerequisites: None beyond the epic prerequisite.

External dependencies used by child issues: [ERA-004](../issues/ERA-004.md). Dependencies listed above as entry prerequisites gate this epic's start. Other dependencies block only the specific child issue listed in its record, without requiring the dependency's entire epic to finish.

Start this epic when its required epics and entry issues are accepted and at least one unfinished child issue is ready. If every remaining child issue is waiting, record the actual blocking issue and resume when it is accepted. Use the [dependency schedule](../../docs/development-plan.md) for concrete overlap examples.

## Coupled child issues

- [ ] [ERA-005: Register sources and bind owners and adapter principals](../issues/ERA-005.md)
- [ ] [ERA-006: Publish versioned time, retention, and account-mapping capabilities](../issues/ERA-006.md)
- [ ] [ERA-007: Ingest tenant inventory with revisions, completeness, and resync](../issues/ERA-007.md)
- [ ] [ERA-008: Show business-account inventory and source coverage](../issues/ERA-008.md)

## Integration boundaries

Primary ownership: source-registry and inventory; account-mapping public contract.

Consume the accepted EPIC-01 public contracts. Coordinate a versioned contract change before downstream work relies on it. Claim specific files when starting a task; a shared module or directory does not permit simultaneous conflicting edits. Use distinct files or interfaces for concurrent work and serialize integration of shared migrations, OpenAPI, module APIs, and workflow configuration.

## Epic acceptance

- [ ] Every child issue is accepted against the integrated candidate.
- [ ] All external child-issue dependencies are accepted and integration checks pass with their real implementations.
- [ ] Demonstrate the complete capability: Administrator registers a source; adapter reports dated summaries; operator sees amount, freshness, and coverage.
- [ ] Record owner UAT, candidate revision, relevant checks, and remaining limits; never count a contract fixture as final integration evidence.

Requirements: REQ-01, REQ-02, REQ-03, REQ-09, REQ-12. Product behavior stays governed by the [requirements](../../docs/specification.md) and [architecture](../../docs/architecture.md).
