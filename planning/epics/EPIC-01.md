# EPIC-01: Safe end-to-end foundation

Type: epic. Milestone: v0.1 end-to-end demonstration. Status: proposed.

Delivery and acceptance owner: project owner. This epic groups four coupled implementation issues into one application capability.

## Application capability

The minimum secure request-to-receipt workflow and shared contracts used by every other epic.

## Why these issues belong together

Login, tenant access, one adapter, durable proposal/approval/execution, and initial audit are inseparable parts of the first working whole. An individual child issue can be integrated and reviewed independently, but the epic is complete only when all four issues and the combined demonstration pass.

## Start prerequisites and external blockers

Required completed epics: None.

Additional entry issue prerequisites: [ERA-037](../issues/ERA-037.md), the accepted demo blueprint. It does not require the full demo epic to finish.

External dependencies used by child issues: [ERA-037](../issues/ERA-037.md). Dependencies listed above as entry prerequisites gate this epic's start. Other dependencies block only the specific child issue listed in its record, without requiring the dependency's entire epic to finish.

Start this epic when its required epics and entry issues are accepted and at least one unfinished child issue is ready. If every remaining child issue is waiting, record the actual blocking issue and resume when it is accepted. Use the [dependency schedule](../../docs/development-plan.md) for concrete overlap examples.

## Coupled child issues

- [ ] [ERA-001: Bootstrap employee login and isolated business accounts](../issues/ERA-001.md)
- [ ] [ERA-002: Request a fresh proposal from one independent adapter](../issues/ERA-002.md)
- [ ] [ERA-003: Approve and execute the first proposal with durable evidence](../issues/ERA-003.md)
- [ ] [ERA-004: Make the thin workflow reproducible in CI and a local walkthrough](../issues/ERA-004.md)

## Integration boundaries

Primary ownership: Shared contracts and seeded workflow; integration owner coordinates changes.

Define and accept the shared public contracts in ERA-004. Coordinate later versioned contract changes before downstream work relies on them. Claim specific files when starting a task; a shared module or directory does not permit simultaneous conflicting edits. Use distinct files or interfaces for concurrent work and serialize integration of shared migrations, OpenAPI, module APIs, and workflow configuration.

## Epic acceptance

- [ ] Every child issue is accepted against the integrated candidate.
- [ ] All external child-issue dependencies are accepted and integration checks pass with their real implementations.
- [ ] Demonstrate the complete capability: Employee logs in, selects an account, requests a proposal, owner approves, adapter deletes fixture records, and audit shows its receipt.
- [ ] Record owner UAT, candidate revision, relevant checks, and remaining limits; never count a contract fixture as final integration evidence.

Requirements: REQ-01, REQ-04, REQ-05, REQ-06, REQ-07, REQ-08, REQ-11, REQ-12, REQ-13. Product behavior stays governed by the [requirements](../../docs/specification.md) and [architecture](../../docs/architecture.md).
