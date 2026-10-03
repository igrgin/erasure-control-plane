# Erasure

- Internal control plane for business-account data deletion and anonymization.
- Tenant boundary: customer business account; one operating company, shared installation.
- Status: design and backlog only; application and hosted demo pending.

## Planned stack

- Control plane: Java, Spring Boot, PostgreSQL.
- UI: React, TypeScript.
- Independent source adapters: Java, outbound authenticated API connections.
- Synthetic demo sources: PostgreSQL, MongoDB, Redis.

## Workflow

1. Adapters publish account inventory, time buckets, and source policies.
2. Employee selects an account and time range.
3. Adapters propose cleanup operations, estimated impact, and exclusions.
4. Source owners approve exact, versioned proposals.
5. Adapters execute; Erasure records decisions, blockers, attempts, and source dispositions.

- Recovery: durable jobs, worker leases, stable operation IDs, adapter deduplication.
- Coverage: registered sources only; adapter-reported outcomes, no independent deletion verification.

## Setup

- Requirements: Git, Python 3; no Python packages required.
- Current executable tooling: planning validation only.
- Application startup commands: pending implementation.

```sh
git clone https://github.com/igrgin/erasure-control-plane.git
cd erasure-control-plane
python3 scripts/validate_plan.py
```

## Documentation

- [Architecture and adapter contract](docs/architecture.md): modules, isolation, protocol, recovery.
- [Demo](docs/demo-plan.md): synthetic fixtures, scenarios, resets, hosting.
- [Deployment](docs/deployment.md): topology, identity, backups, release checks.
- [Scaling](docs/scaling.md): workload targets, capacity, multiple API/worker instances.
- [Specification](docs/specification.md): requirements and acceptance criteria.
- [Domain model](CONTEXT.md): terminology and entity boundaries.
- [Development plan](docs/development-plan.md): epics, dependencies, parallel work.
- [GitHub issues](https://github.com/igrgin/erasure-control-plane/issues): implementation backlog.
- [Git workflow](docs/git-workflow.md): branches, prerequisites, PR checks.
