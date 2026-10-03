# EPIC-06: Blockers and complete case disposition

Type: epic. Milestone: v0.1 end-to-end demonstration. Status: proposed.

Delivery and acceptance owner: project owner. This epic groups four coupled implementation issues into one application capability.

## Application capability

Case coordination from per-source state to accountable closure with exceptions.

## Why these issues belong together

Disposition rules, blocker intervention, closure decisions, and end-to-end cases jointly account for every scoped source. An individual child issue can be integrated and reviewed independently, but the epic is complete only when all four issues and the combined demonstration pass.

## Start prerequisites and external blockers

Required completed epics: [EPIC-01](EPIC-01.md), including its shared contract acceptance.

Additional entry issue prerequisites: None beyond the epic prerequisite.

External dependencies used by child issues: [ERA-004](../issues/ERA-004.md), [ERA-005](../issues/ERA-005.md), [ERA-009](../issues/ERA-009.md), [ERA-010](../issues/ERA-010.md), [ERA-012](../issues/ERA-012.md), [ERA-015](../issues/ERA-015.md), [ERA-019](../issues/ERA-019.md). Dependencies listed above as entry prerequisites gate this epic's start. Other dependencies block only the specific child issue listed in its record, without requiring the dependency's entire epic to finish.

Start this epic when its required epics and entry issues are accepted and at least one unfinished child issue is ready. If every remaining child issue is waiting, record the actual blocking issue and resume when it is accepted. Use the [dependency schedule](../../docs/development-plan.md) for concrete overlap examples.

## Coupled child issues

- [ ] [ERA-021: Define per-source disposition and request closure transitions](../issues/ERA-021.md)
- [ ] [ERA-022: Manage retention holds, blockers, and source-owner intervention](../issues/ERA-022.md)
- [ ] [ERA-023: Close requests with explicit coverage and acknowledged exceptions](../issues/ERA-023.md)
- [ ] [ERA-024: Demonstrate complete customer-request scenarios](../issues/ERA-024.md)

## Integration boundaries

Primary ownership: Case lifecycle/disposition, blockers, closure UI, customer-request scenarios.

Consume the accepted EPIC-01 public contracts. Coordinate a versioned contract change before downstream work relies on it. Claim specific files when starting a task; a shared module or directory does not permit simultaneous conflicting edits. Use distinct files or interfaces for concurrent work and serialize integration of shared migrations, OpenAPI, module APIs, and workflow configuration.

## Epic acceptance

- [ ] Every child issue is accepted against the integrated candidate.
- [ ] All external child-issue dependencies are accepted and integration checks pass with their real implementations.
- [ ] Demonstrate the complete capability: Operator resolves blockers or records exceptions; closure lists a disposition for every scoped source.
- [ ] Record owner UAT, candidate revision, relevant checks, and remaining limits; never count a contract fixture as final integration evidence.

Requirements: REQ-04, REQ-07, REQ-09, REQ-10, REQ-11. Product behavior stays governed by the [requirements](../../docs/specification.md) and [architecture](../../docs/architecture.md).
