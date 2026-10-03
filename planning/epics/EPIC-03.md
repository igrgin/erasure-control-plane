# EPIC-03: Precise scope across heterogeneous sources

Type: epic. Milestone: v0.1 end-to-end demonstration. Status: proposed.

Delivery and acceptance owner: project owner. This epic groups four coupled implementation issues into one application capability.

## Application capability

Request intake and proposals that preserve intent across different source time and retention rules.

## Why these issues belong together

Request boundaries, source-specific selection, the MongoDB adapter, and multi-source presentation jointly define what an owner is approving. An individual child issue can be integrated and reviewed independently, but the epic is complete only when all four issues and the combined demonstration pass.

## Start prerequisites and external blockers

Required completed epics: [EPIC-01](EPIC-01.md), including its shared contract acceptance.

Additional entry issue prerequisites: [ERA-006](../issues/ERA-006.md).

External dependencies used by child issues: [ERA-006](../issues/ERA-006.md), [ERA-008](../issues/ERA-008.md), [ERA-038](../issues/ERA-038.md). Dependencies listed above as entry prerequisites gate this epic's start. Other dependencies block only the specific child issue listed in its record, without requiring the dependency's entire epic to finish.

Start this epic when its required epics and entry issues are accepted and at least one unfinished child issue is ready. If every remaining child issue is waiting, record the actual blocking issue and resume when it is accepted. Use the [dependency schedule](../../docs/development-plan.md) for concrete overlap examples.

## Coupled child issues

- [ ] [ERA-009: Capture immutable request scope and precise time boundaries](../issues/ERA-009.md)
- [ ] [ERA-010: Generate source-specific proposals with retention and selection preconditions](../issues/ERA-010.md)
- [ ] [ERA-011: Build a MongoDB adapter with different time and cleanup behavior](../issues/ERA-011.md)
- [ ] [ERA-012: Review a multi-source request and its time/retention differences](../issues/ERA-012.md)

## Integration boundaries

Primary ownership: Request intake/scope, proposal generation, MongoDB adapter, request-scope UI.

Consume the accepted EPIC-01 public contracts. Coordinate a versioned contract change before downstream work relies on it. Claim specific files when starting a task; a shared module or directory does not permit simultaneous conflicting edits. Use distinct files or interfaces for concurrent work and serialize integration of shared migrations, OpenAPI, module APIs, and workflow configuration.

## Epic acceptance

- [ ] Every child issue is accepted against the integrated candidate.
- [ ] All external child-issue dependencies are accepted and integration checks pass with their real implementations.
- [ ] Demonstrate the complete capability: One request spans two sources with different time/retention rules and exposes proposed actions, retained subsets, and incompatible boundaries.
- [ ] Record owner UAT, candidate revision, relevant checks, and remaining limits; never count a contract fixture as final integration evidence.

Requirements: REQ-03, REQ-04, REQ-05, REQ-07, REQ-09. Product behavior stays governed by the [requirements](../../docs/specification.md) and [architecture](../../docs/architecture.md).
