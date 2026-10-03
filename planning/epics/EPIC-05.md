# EPIC-05: Reliable execution and recovery

Type: epic. Milestone: v0.1 end-to-end demonstration. Status: proposed.

Delivery and acceptance owner: project owner. This epic groups four coupled implementation issues into one application capability.

## Application capability

The durable workflow that delivers authorized operations and preserves certainty about their outcomes.

## Why these issues belong together

Workers, adapter ledgers/checkpoints, outcome classification, and fault tests jointly prevent unsafe retry or false success. An individual child issue can be integrated and reviewed independently, but the epic is complete only when all four issues and the combined demonstration pass.

## Start prerequisites and external blockers

Required completed epics: [EPIC-01](EPIC-01.md), including its shared contract acceptance.

Additional entry issue prerequisites: None beyond the epic prerequisite.

External dependencies used by child issues: [ERA-004](../issues/ERA-004.md), [ERA-011](../issues/ERA-011.md), [ERA-016](../issues/ERA-016.md). Dependencies listed above as entry prerequisites gate this epic's start. Other dependencies block only the specific child issue listed in its record, without requiring the dependency's entire epic to finish.

Start this epic when its required epics and entry issues are accepted and at least one unfinished child issue is ready. If every remaining child issue is waiting, record the actual blocking issue and resume when it is accepted. Use the [dependency schedule](../../docs/development-plan.md) for concrete overlap examples.

## Coupled child issues

- [ ] [ERA-017: Run durable leased workers with bounded source and tenant concurrency](../issues/ERA-017.md)
- [ ] [ERA-018: Complete adapter deduplication and checkpoint recovery](../issues/ERA-018.md)
- [ ] [ERA-019: Expose partial, failed, and unknown execution outcomes](../issues/ERA-019.md)
- [ ] [ERA-020: Prove recovery with a deterministic cross-process failure harness](../issues/ERA-020.md)

## Integration boundaries

Primary ownership: execution engine, adapter operation ledgers, execution UI, failure harness.

Consume the accepted EPIC-01 public contracts. Coordinate a versioned contract change before downstream work relies on it. Claim specific files when starting a task; a shared module or directory does not permit simultaneous conflicting edits. Use distinct files or interfaces for concurrent work and serialize integration of shared migrations, OpenAPI, module APIs, and workflow configuration.

## Epic acceptance

- [ ] Every child issue is accepted against the integrated candidate.
- [ ] All external child-issue dependencies are accepted and integration checks pass with their real implementations.
- [ ] Demonstrate the complete capability: Crashes, duplicate delivery, partial cleanup, and lost responses remain visible and recover safely.
- [ ] Record owner UAT, candidate revision, relevant checks, and remaining limits; never count a contract fixture as final integration evidence.

Requirements: REQ-07, REQ-08, REQ-10, REQ-11, REQ-12, REQ-14. Product behavior stays governed by the [requirements](../../docs/specification.md) and [architecture](../../docs/architecture.md).
