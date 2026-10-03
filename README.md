# Erasure

Erasure is an internal, multi-tenant control plane for cleaning up business-account data across registered sources. One company operates it; its customer business accounts are the tenants. Source owners approve specific cleanup proposals before adapters execute them. Erasure records what was proposed, decided, blocked, and reported by each adapter.

This directory currently contains a development plan, not an application. The first release will demonstrate the complete workflow with synthetic data, a Java/Spring Boot backend, a React frontend, independent adapters, and a deployable environment.

Start with [the development plan](docs/development-plan.md). Supporting documents:

- [Product requirements](docs/specification.md)
- [Domain glossary](CONTEXT.md)
- [Architecture and adapter contract](docs/architecture.md)
- [Synthetic demo and hosting feasibility](docs/demo-plan.md)
- [Deployment plan](docs/deployment.md)
- [Scaling plan and evidence](docs/scaling.md)
- [GitHub-ready epics and child issues](planning/README.md)
- [Planning provenance and gates](docs/planning-handoff.md)

Run `python3 scripts/validate_plan.py` to check planning links, issue dependencies, and requirement coverage. No repository, GitHub issues, application code, or deployment has been created yet.
