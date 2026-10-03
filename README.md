# Erasure

Erasure coordinates deletion and anonymization of business-account data across a company's registered data sources. It is an internal system for employees handling customer cleanup requests. One company operates the system, and its customer business accounts are the tenants.

This personal project explores web application architecture through a workflow with real consequences: identifying data across different stores, approving exactly what will change, recovering from interrupted execution, and keeping an attributable audit history. The goal is a small, deployable implementation that demonstrates the same boundaries and failure handling needed in a larger organization.

## How it works

1. Source adapters publish account-level data summaries, including time buckets, retention rules, and coverage.
2. An employee creates a cleanup request for a business account and time range.
3. Each adapter proposes a source-specific operation with estimated impact and any exclusions or blockers.
4. The accountable source owner reviews and approves the exact proposal.
5. The adapter executes the approved operation and reports its outcome. Erasure records decisions, execution attempts, and each source's final disposition.

Coverage is limited to registered sources. Execution outcomes come from adapters; Erasure does not independently verify deletion afterward. Retained data, partial results, and unknown outcomes remain explicit in the audit history.

## Architecture

The planned implementation uses Java and Spring Boot for a modular control plane, React and TypeScript for the employee interface, and PostgreSQL for workflow state and audit records. Independent Java adapters run near their data sources, keep source credentials there, and initiate authenticated outbound connections to Erasure.

The design focuses on:

- Business-account isolation across inventory, requests, jobs, and audit exports.
- Versioned proposals and owner approvals that become invalid when their assumptions change.
- Durable jobs, worker leases, and stable operation identities for safe retries and recovery.
- Source-specific cleanup behavior behind a shared adapter protocol.
- Bounded concurrency and measurable scaling before introducing separate services.

Read the [architecture and adapter contract](docs/architecture.md) for module ownership, authentication, persistence, state transitions, and recovery rules. The [scaling plan](docs/scaling.md) explains how the small deployment extends to multiple API and worker instances, larger inventories, and more customer accounts, with workload targets to test those claims.

## Demonstration

The first release will use synthetic business accounts across three real source engines:

| Source | Example data | Cleanup behavior |
| --- | --- | --- |
| PostgreSQL | Orders, account metadata, invoice references | Transactional deletion with disclosed retention exceptions |
| MongoDB | Usage documents with account identifiers | Anonymization or deletion in recoverable chunks |
| Redis | Account caches and derived lookup entries | Invalidation that accounts for expiry and recreated keys |

The walkthrough will cover owner review, tenant isolation, retention blockers, interrupted execution, and closure with explicit source outcomes. Public visibility is planned as a read-only guided tour, with owner-controlled live sessions for real cleanup of synthetic data.

The [demo plan](docs/demo-plan.md) describes fixtures, scenarios, safe resets, viewer access, and hosting feasibility. The [deployment plan](docs/deployment.md) covers the intended container topology, HTTPS, identity, backups, and release checks.

## Run locally

The project is currently in the design and backlog stage. Application code, source containers, seed data, and deployment commands are still to be implemented, so there is no runnable application or hosted demo yet.

You can clone the repository and validate the current planning documents with Python 3, using only its standard library:

```sh
git clone https://github.com/igrgin/erasure-control-plane.git
cd erasure-control-plane
python3 scripts/validate_plan.py
```

The validator checks document links, issue prerequisites, and requirement coverage. Application startup and demo commands will be documented here when the corresponding implementation is available.

## Explore the design

| Document | What to look for |
| --- | --- |
| [Product specification](docs/specification.md) | Scope, requirements, and release acceptance criteria |
| [Domain glossary](CONTEXT.md) | Business accounts, sources, proposals, operations, and dispositions |
| [Architecture](docs/architecture.md) | Module boundaries, adapter protocol, tenant isolation, and execution recovery |
| [Demo plan](docs/demo-plan.md) | Three-source scenarios, synthetic fixtures, reset safety, and hosting options |
| [Deployment plan](docs/deployment.md) | Local and hosted topology, operations, and release validation |
| [Scaling plan](docs/scaling.md) | Capacity assumptions, measurement targets, and a path to larger deployments |
| [Development plan](docs/development-plan.md) | Vertical-slice epics, dependencies, and parallel delivery opportunities |

Implementation is tracked in the [GitHub backlog](https://github.com/igrgin/erasure-control-plane/issues). For repository work, follow the [Git workflow](docs/git-workflow.md) and [agent instructions](AGENTS.md).
