# Repository instructions

## Issue and Git workflow

Before taking an issue, creating or updating its branch, opening a PR, or merging, follow [the Git workflow](docs/git-workflow.md). It defines live readiness checks, branch conventions, PR requirements, and owner approval. Begin implementation only after live GitHub data confirms readiness and any issue or epic entry criteria have acceptance evidence.

Only the project owner approves PRs. Agents must never submit approving reviews, including through the owner's GitHub account. Leave the PR open for owner review; merge only after owner approval and an explicit instruction to merge.

## Design and verification

Read [the domain glossary](CONTEXT.md) and [requirements](docs/specification.md) when changing behavior. Read [the architecture](docs/architecture.md) when changing a module boundary, persistence model, or adapter contract. Read [the demo plan](docs/demo-plan.md) when changing fixtures, source setup, resets, or public demonstration behavior.

Implement and run the issue's listed acceptance checks. Use GitHub issues, native sub-issues, and blocking dependencies as the backlog source of truth.

Before concurrent work, claim concrete files and coordinate shared contracts/migrations with the integration owner. Accept an epic only after all its children and its combined real integration demonstration pass. Keep source-owner approval, tenant isolation, durable operation identity, and adapter-reported outcome limits intact.
