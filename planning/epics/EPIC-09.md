# EPIC-09: Measured scaling and architecture handoff

Type: epic. Milestone: v0.1 end-to-end demonstration. Status: proposed.

Delivery and acceptance owner: project owner. This epic groups four coupled implementation issues into one application capability.

## Application capability

Repeatable evidence that the same architecture grows while preserving its safety and isolation rules.

## Why these issues belong together

Workload generation, multi-instance correctness, capacity/fairness measurements, and the architecture explanation jointly substantiate the scaling claims. An individual child issue can be integrated and reviewed independently, but the epic is complete only when all four issues and the combined demonstration pass.

## Start prerequisites and external blockers

Required completed epics: [EPIC-01](EPIC-01.md), including its shared contract acceptance.

Additional entry issue prerequisites: [ERA-007](../issues/ERA-007.md).

External dependencies used by child issues: [ERA-004](../issues/ERA-004.md), [ERA-007](../issues/ERA-007.md), [ERA-012](../issues/ERA-012.md), [ERA-017](../issues/ERA-017.md), [ERA-020](../issues/ERA-020.md), [ERA-027](../issues/ERA-027.md), [ERA-029](../issues/ERA-029.md), [ERA-032](../issues/ERA-032.md), [ERA-039](../issues/ERA-039.md), [ERA-042](../issues/ERA-042.md). Dependencies listed above as entry prerequisites gate this epic's start. Other dependencies block only the specific child issue listed in its record, without requiring the dependency's entire epic to finish.

Start this epic when its required epics and entry issues are accepted and at least one unfinished child issue is ready. If every remaining child issue is waiting, record the actual blocking issue and resume when it is accepted. Use the [dependency schedule](../../docs/development-plan.md) for concrete overlap examples.

## Coupled child issues

- [ ] [ERA-033: Generate repeatable inventory and workflow scale workloads](../issues/ERA-033.md)
- [ ] [ERA-034: Prove isolation and recovery with multiple API and worker instances](../issues/ERA-034.md)
- [ ] [ERA-035: Measure capacity, fairness, and failure isolation](../issues/ERA-035.md)
- [ ] [ERA-036: Publish the architecture portfolio and evidence-based scaling handoff](../issues/ERA-036.md)

## Integration boundaries

Primary ownership: Load/failure workloads, scale-demo configuration, benchmarks, final architecture evidence.

Consume the accepted EPIC-01 public contracts. Coordinate a versioned contract change before downstream work relies on it. Claim specific files when starting a task; a shared module or directory does not permit simultaneous conflicting edits. Use distinct files or interfaces for concurrent work and serialize integration of shared migrations, OpenAPI, module APIs, and workflow configuration.

## Epic acceptance

- [ ] Every child issue is accepted against the integrated candidate.
- [ ] All external child-issue dependencies are accepted and integration checks pass with their real implementations.
- [ ] Demonstrate the complete capability: Multiple APIs/workers preserve isolation and recovery; measured results and limitations support the growth path.
- [ ] Record owner UAT, candidate revision, relevant checks, and remaining limits; never count a contract fixture as final integration evidence.

Requirements: REQ-03, REQ-08, REQ-12, REQ-13, REQ-14, REQ-15. Product behavior stays governed by the [requirements](../../docs/specification.md) and [architecture](../../docs/architecture.md).
