# EPIC-10: Synthetic demo environment and public visibility

Type: epic. Milestone: v0.1 end-to-end demonstration. Status: proposed.

Delivery and acceptance owner: project owner. Six coupled issues make the architecture tangible and visible to others.

## Application capability

A reproducible synthetic company environment with relational, document, and cache sources, plus a guided demonstration and a verified public hosting path. See the [demo plan](../../docs/demo-plan.md) for the source catalog and researched hosting assessment.

## Why these issues belong together

The story defines what to seed, the fixtures give adapters meaningful behavior, the cache adapter adds expiry/recreation semantics, and the guided scenarios make cleanup understandable. Hosting feasibility and launch turn that same environment into a visible portfolio demonstration. The epic is complete only when its sources, repeatable scenarios, and public experience work together.

## Start prerequisites and external blockers

Required completed epics: None. Additional entry issue prerequisites: None.

ERA-037 can start before application implementation. After its design is accepted, fixture setup and hosting research can proceed alongside the foundation. Later child issues wait for real source/case/audit/deployment capabilities.

External dependencies used by child issues: [ERA-006](../issues/ERA-006.md), [ERA-017](../issues/ERA-017.md), [ERA-024](../issues/ERA-024.md), [ERA-026](../issues/ERA-026.md), [ERA-031](../issues/ERA-031.md), [ERA-032](../issues/ERA-032.md). Each blocks only its named child issue. Public launch requires deployed UAT, but the blueprint and setup do not wait for the deployment epic.

## Coupled child issues

- [ ] [ERA-037: Define the demo source catalog, business story, and scenario blueprint](../issues/ERA-037.md)
- [ ] [ERA-038: Create the three-store environment and deterministic synthetic fixtures](../issues/ERA-038.md)
- [ ] [ERA-039: Implement the Redis cache adapter with safe expiry and recreation handling](../issues/ERA-039.md)
- [ ] [ERA-040: Build the guided three-source demo and repeatable scenario reset](../issues/ERA-040.md)
- [ ] [ERA-041: Assess demo hosting, recurring cost, and resource viability](../issues/ERA-041.md)
- [ ] [ERA-042: Launch and accept a publicly visible synthetic demo](../issues/ERA-042.md)

## Integration boundaries

Primary ownership: Demo blueprint, fixture/source infrastructure, Redis adapter, guided tour, hosting comparison and visible launch.

EPIC-03/ERA-011 owns the MongoDB adapter; EPIC-10 owns its source infrastructure and fixtures. EPIC-05 owns common recovery machinery, while ERA-039 owns cache-specific recovery. EPIC-08 owns deployment/promotion/restore; ERA-041/042 own the demo hosting choice, presentation, and visibility evidence. Use separate source/deployment profiles and concrete file claims for concurrent edits.

## Epic acceptance

- [ ] All six child issues and their real external dependencies are accepted.
- [ ] A clean environment reproduces two synthetic business accounts and all three required storage sources.
- [ ] The guided workflow demonstrates approved cleanup, exceptions, cache expiry/recreation, safe retry, tenant isolation, and attributable audit.
- [ ] A public HTTPS read-only tour and an owner-controlled live session pass external-browser UAT with recorded URL/candidate evidence.
- [ ] Measured resources and dated cost fit the owner-approved hosting decision; reset, maintenance, recovery, and teardown have an owner.

Requirements: REQ-01, REQ-03, REQ-05, REQ-07, REQ-08, REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-15. Public visibility is a demonstration of an internal product, not a customer self-service feature.
