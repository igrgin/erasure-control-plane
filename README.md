# Erasure

Erasure is an internal, multi-tenant control plane for cleaning up business-account data across registered sources. One company operates it; its customer business accounts are the tenants. Source owners approve specific cleanup proposals before adapters execute them. Erasure records what was proposed, decided, blocked, and reported by each adapter.

This repository contains the accepted development plan and delivery workflow. Application implementation is tracked by the published issues. The first release will demonstrate the complete workflow with synthetic data, a Java/Spring Boot backend, a React frontend, independent adapters, and a deployable environment.

Start with [the development plan](docs/development-plan.md). Supporting documents:

- [Product requirements](docs/specification.md)
- [Domain glossary](CONTEXT.md)
- [Architecture and adapter contract](docs/architecture.md)
- [Synthetic demo and hosting feasibility](docs/demo-plan.md)
- [Deployment plan](docs/deployment.md)
- [Scaling plan and evidence](docs/scaling.md)
- [GitHub-ready epics and child issues](planning/README.md)
- [Planning provenance and gates](docs/planning-handoff.md)

Before issue work, follow [AGENTS.md](AGENTS.md) and [the Git workflow](docs/git-workflow.md). The [GitHub backlog](https://github.com/igrgin/erasure-control-plane/issues) contains native epic/sub-issue and blocker relationships. Main requires PRs and successful issue-policy/planning checks.

Run `python3 scripts/validate_plan.py` to check planning links, prerequisites, and requirement coverage. Application code and deployment remain future issue work.
