# Repository instructions

## Shared workflow

Use the shared skills in `.agents/skills/`, linked to
`~/Documents/home-repo/.agents/skills/`. For implementation, diagnosis, review,
coordination, and skill setup, read `~/Documents/home-repo/docs/agent-workflow.md`.
For GitHub work, use `~/Documents/home-repo/docs/github-workflow.md` as the
authority. The project owner reviews and authorizes merges.

## Work selection

Before starting an issue, run `python3 scripts/issue_workflow.py check NUMBER`.
Begin implementation when every issue prerequisite and epic entry gate is
accepted. Unrelated children within an epic may run independently.

## Design and verification

Read [the domain glossary](CONTEXT.md) and [requirements](docs/specification.md) when changing behavior. Read [the architecture](docs/architecture.md) when changing a module boundary, persistence model, or adapter contract. Read [the demo plan](docs/demo-plan.md) when changing fixtures, source setup, resets, or public demonstration behavior.

Implement and run the issue's listed acceptance checks. Use GitHub issues, native sub-issues, and blocking dependencies as the backlog source of truth.

Before concurrent work, claim concrete files and coordinate shared contracts/migrations with the integration owner. Accept an epic only after all its children and its combined real integration demonstration pass. Keep source-owner approval, tenant isolation, durable operation identity, and adapter-reported outcome limits intact.
