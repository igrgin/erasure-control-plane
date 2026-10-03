# EPIC-07: Audit evidence and operational visibility

Type: epic. Milestone: v0.1 end-to-end demonstration. Status: proposed.

Delivery and acceptance owner: project owner. This epic groups four coupled implementation issues into one application capability.

## Application capability

The evidence and management views needed to explain decisions and operate the system.

## Why these issues belong together

Audit events, authorized exports, health metrics, and intervention/retention drills jointly establish operational accountability. An individual child issue can be integrated and reviewed independently, but the epic is complete only when all four issues and the combined demonstration pass.

## Start prerequisites and external blockers

Required completed epics: [EPIC-01](EPIC-01.md), including its shared contract acceptance.

Additional entry issue prerequisites: None beyond the epic prerequisite.

External dependencies used by child issues: [ERA-004](../issues/ERA-004.md), [ERA-007](../issues/ERA-007.md), [ERA-017](../issues/ERA-017.md), [ERA-019](../issues/ERA-019.md), [ERA-022](../issues/ERA-022.md). Dependencies listed above as entry prerequisites gate this epic's start. Other dependencies block only the specific child issue listed in its record, without requiring the dependency's entire epic to finish.

Start this epic when its required epics and entry issues are accepted and at least one unfinished child issue is ready. If every remaining child issue is waiting, record the actual blocking issue and resume when it is accepted. Use the [dependency schedule](../../docs/development-plan.md) for concrete overlap examples.

## Coupled child issues

- [ ] [ERA-025: Harden attributable audit events and evidence retention](../issues/ERA-025.md)
- [ ] [ERA-026: Deliver tenant-authorized audit timeline and export](../issues/ERA-026.md)
- [ ] [ERA-027: Show operational health and actionable workflow metrics](../issues/ERA-027.md)
- [ ] [ERA-028: Exercise operational interventions and data-minimization policies](../issues/ERA-028.md)

## Integration boundaries

Primary ownership: audit, observability, audit/operations views, operational runbooks.

Consume the accepted EPIC-01 public contracts. Coordinate a versioned contract change before downstream work relies on it. Claim specific files when starting a task; a shared module or directory does not permit simultaneous conflicting edits. Use distinct files or interfaces for concurrent work and serialize integration of shared migrations, OpenAPI, module APIs, and workflow configuration.

## Epic acceptance

- [ ] Every child issue is accepted against the integrated candidate.
- [ ] All external child-issue dependencies are accepted and integration checks pass with their real implementations.
- [ ] Demonstrate the complete capability: Auditor reconstructs a case; operators detect stale sources and stuck work and apply safe evidence-retention rules.
- [ ] Record owner UAT, candidate revision, relevant checks, and remaining limits; never count a contract fixture as final integration evidence.

Requirements: REQ-03, REQ-08, REQ-09, REQ-11, REQ-12, REQ-13. Product behavior stays governed by the [requirements](../../docs/specification.md) and [architecture](../../docs/architecture.md).
