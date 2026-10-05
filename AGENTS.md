# Repository instructions

## Issue and Git workflow

Before taking or resuming an issue, managing its branch, opening a PR, or merging, follow [the Git workflow](docs/git-workflow.md).

Only the project owner approves PRs. Agents must never submit approving reviews, including through the owner's GitHub account. Leave the PR open for owner review; merge only after owner approval and an explicit instruction to merge.

## Design and verification

Read [the domain glossary](CONTEXT.md) and [requirements](docs/specification.md) when changing behavior. Read [the architecture](docs/architecture.md) when changing a module boundary, persistence model, or adapter contract. Read [the demo plan](docs/demo-plan.md) when changing fixtures, source setup, resets, or public demonstration behavior.

Before concurrent edits, participating agents must agree on file ownership and changes to shared contracts or migrations. Accept an epic only after all its children and its combined real integration demonstration pass. Keep source-owner approval, tenant isolation, durable operation identity, and adapter-reported outcome limits intact.
