# Erasure

Erasure is an internal control plane for deleting or anonymizing business-account data across registered sources. One company operates a shared installation, with each customer business account treated as a tenant. Source owners approve cleanup operations before adapters execute them. Erasure records the adapters' reported results but does not independently verify deletion.

## Planned stack

- Control plane: Java, Spring Boot, PostgreSQL.
- UI: React, TypeScript.
- Independent source adapters: Java, outbound authenticated API connections.
- Synthetic demo sources: two PostgreSQL source databases and Elasticsearch.

## Workflow

1. Each source adapter publishes counts of records associated with each business account, grouped by time interval. The count unit depends on the source, such as rows, messages, documents, or cache entries. The adapter also publishes its retention rules and supported cleanup operations.
2. An employee creates a cleanup request for a business account and time range.
3. Each adapter proposes a deletion or anonymization operation and estimates how much data it will affect. The proposal identifies data excluded from cleanup and any conditions that prevent execution.
4. The accountable source owner reviews the proposal and its estimated impact, then approves or rejects that specific version of the operation.
5. The adapter executes the approved operation and reports its result. Erasure keeps an audit history of owner decisions, blockers, execution attempts, and the outcome for each source.

## Setup

TODO

## Documentation

- [Architecture and adapter contract](docs/architecture.md): modules, isolation, protocol, recovery.
- [Demo](docs/demo-plan.md): synthetic fixtures, scenarios, resets, hosting.
- [Deployment](docs/deployment.md): topology, identity, backups, release checks.
- [Scaling](docs/scaling.md): workload targets, capacity, multiple API/worker instances.
- [Specification](docs/specification.md): requirements and acceptance criteria.
- [Domain model](CONTEXT.md): terminology and entity boundaries.
- [GitHub issues](https://github.com/igrgin/erasure-control-plane/issues): implementation backlog.
- [Git workflow](docs/git-workflow.md): branches, prerequisites, PR checks.
