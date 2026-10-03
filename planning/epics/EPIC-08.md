# EPIC-08: Deployment and release operations

Type: epic. Milestone: v0.1 end-to-end demonstration. Status: proposed.

Delivery and acceptance owner: project owner. This epic groups four coupled implementation issues into one application capability.

## Application capability

The repeatable deployment and recovery machinery for a complete demonstration release.

## Why these issues belong together

Packaging, promotion, restoration, credential rotation, and deployed UAT jointly make an operational release rather than a local-only application. An individual child issue can be integrated and reviewed independently, but the epic is complete only when all four issues and the combined demonstration pass.

## Start prerequisites and external blockers

Required completed epics: [EPIC-01](EPIC-01.md), including its shared contract acceptance.

Additional entry issue prerequisites: None beyond the epic prerequisite.

External dependencies used by child issues: [ERA-004](../issues/ERA-004.md), [ERA-018](../issues/ERA-018.md), [ERA-024](../issues/ERA-024.md), [ERA-026](../issues/ERA-026.md), [ERA-027](../issues/ERA-027.md), [ERA-028](../issues/ERA-028.md), [ERA-040](../issues/ERA-040.md). Dependencies listed above as entry prerequisites gate this epic's start. Other dependencies block only the specific child issue listed in its record, without requiring the dependency's entire epic to finish.

Start this epic when its required epics and entry issues are accepted and at least one unfinished child issue is ready. If every remaining child issue is waiting, record the actual blocking issue and resume when it is accepted. Use the [dependency schedule](../../docs/development-plan.md) for concrete overlap examples.

## Coupled child issues

- [ ] [ERA-029: Package the application topology for a clean HTTPS deployment](../issues/ERA-029.md)
- [ ] [ERA-030: Build immutable images and an approved promotion pipeline](../issues/ERA-030.md)
- [ ] [ERA-031: Prove safe backup, restore, credential rotation, and rollback](../issues/ERA-031.md)
- [ ] [ERA-032: Accept the deployed end-to-end release candidate](../issues/ERA-032.md)

## Integration boundaries

Primary ownership: deploy configuration, release workflows, recovery automation, deployed acceptance.

Consume the accepted EPIC-01 public contracts. Coordinate a versioned contract change before downstream work relies on it. Claim specific files when starting a task; a shared module or directory does not permit simultaneous conflicting edits. Use distinct files or interfaces for concurrent work and serialize integration of shared migrations, OpenAPI, module APIs, and workflow configuration.

## Epic acceptance

- [ ] Every child issue is accepted against the integrated candidate.
- [ ] All external child-issue dependencies are accepted and integration checks pass with their real implementations.
- [ ] Demonstrate the complete capability: A clean target runs the complete workflow and passes restore, rotation, rollback, and restart exercises.
- [ ] Record owner UAT, candidate revision, relevant checks, and remaining limits; never count a contract fixture as final integration evidence.

Requirements: REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, REQ-07, REQ-08, REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-15. Product behavior stays governed by the [requirements](../../docs/specification.md) and [architecture](../../docs/architecture.md).
