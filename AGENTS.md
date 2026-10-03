# Repository instructions

## Work selection

Before starting an issue, read [the Git workflow](docs/git-workflow.md) and run its live readiness check. Begin implementation only when every issue prerequisite and epic entry gate is accepted. Epic membership groups work; it does not require unrelated children to run sequentially.

## Git rules

- Create an issue branch only when the issue is assigned or taken for implementation and its prerequisites are accepted. Creating an issue does not create a branch.
- Use one dedicated branch per issue, including epic integration work. Name it `<github-issue-number>-<issue-title-in-kebab-case>`, stripping any `[ERA-xxx]` or `[EPIC-xx]` title prefix. Example: `48-define-the-demo-source-catalog-business-story-and-scenario-blueprint`.
- Use a flat branch name. Add a namespace only when the user explicitly requests one.
- Start from the latest `origin/main` unless the user explicitly selects another base. Reuse an existing issue branch without discarding its commits; update its base before new work.
- Submit changes through a PR targeting `main`, with `Closes #<issue-number>` in its body. Each PR implements its branch's issue and passes the required checks before merge.
- Only the project owner approves PRs. Agents must never submit approving reviews, including through the owner's GitHub account. Open the PR and wait for the owner's review. Merge only after the owner approves the result and explicitly instructs you to merge.

## Design and verification

Read [the domain glossary](CONTEXT.md) and [requirements](docs/specification.md) when changing behavior. Read [the architecture](docs/architecture.md) when changing a module boundary, persistence model, or adapter contract. Read [the demo plan](docs/demo-plan.md) when changing fixtures, source setup, resets, or public demonstration behavior.

Implement and run the issue's listed acceptance checks. Use GitHub issues, native sub-issues, and blocking dependencies as the backlog source of truth.

Before concurrent work, claim concrete files and coordinate shared contracts/migrations with the integration owner. Accept an epic only after all its children and its combined real integration demonstration pass. Keep source-owner approval, tenant isolation, durable operation identity, and adapter-reported outcome limits intact.
