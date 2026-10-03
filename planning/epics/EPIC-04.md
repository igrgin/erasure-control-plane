# EPIC-04: Accountable owner decisions

Type: epic. Milestone: v0.1 end-to-end demonstration. Status: proposed.

Delivery and acceptance owner: project owner. This epic groups four coupled implementation issues into one application capability.

## Application capability

The internal authorization and review workflow that turns a proposal into permission to execute.

## Why these issues belong together

Owner grants, decision concurrency, stale-plan checks, review UI, and withdrawal rules must agree on exactly what is authorized. An individual child issue can be integrated and reviewed independently, but the epic is complete only when all four issues and the combined demonstration pass.

## Start prerequisites and external blockers

Required completed epics: [EPIC-01](EPIC-01.md), including its shared contract acceptance.

Additional entry issue prerequisites: [ERA-005](../issues/ERA-005.md).

External dependencies used by child issues: [ERA-005](../issues/ERA-005.md), [ERA-010](../issues/ERA-010.md). Dependencies listed above as entry prerequisites gate this epic's start. Other dependencies block only the specific child issue listed in its record, without requiring the dependency's entire epic to finish.

Start this epic when its required epics and entry issues are accepted and at least one unfinished child issue is ready. If every remaining child issue is waiting, record the actual blocking issue and resume when it is accepted. Use the [dependency schedule](../../docs/development-plan.md) for concrete overlap examples.

## Coupled child issues

- [ ] [ERA-013: Enforce source-owner authority and concurrent decisions](../issues/ERA-013.md)
- [ ] [ERA-014: Invalidate stale approval and revalidate before source effects](../issues/ERA-014.md)
- [ ] [ERA-015: Provide an owner review queue with explicit decisions and reasons](../issues/ERA-015.md)
- [ ] [ERA-016: Serialize overlapping cleanup and define cancellation races](../issues/ERA-016.md)

## Integration boundaries

Primary ownership: proposals-decisions and owner review UI; public dispatch-authorization contract.

Consume the accepted EPIC-01 public contracts. Coordinate a versioned contract change before downstream work relies on it. Claim specific files when starting a task; a shared module or directory does not permit simultaneous conflicting edits. Use distinct files or interfaces for concurrent work and serialize integration of shared migrations, OpenAPI, module APIs, and workflow configuration.

## Epic acceptance

- [ ] Every child issue is accepted against the integrated candidate.
- [ ] All external child-issue dependencies are accepted and integration checks pass with their real implementations.
- [ ] Demonstrate the complete capability: Only an authorized owner approves; changes invalidate approval; competing decisions and withdrawal behave consistently.
- [ ] Record owner UAT, candidate revision, relevant checks, and remaining limits; never count a contract fixture as final integration evidence.

Requirements: REQ-04, REQ-05, REQ-06, REQ-07, REQ-08, REQ-11, REQ-12. Product behavior stays governed by the [requirements](../../docs/specification.md) and [architecture](../../docs/architecture.md).
