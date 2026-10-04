# Git and issue workflow

## Start work

1. Read the GitHub issue, its parent epic, and acceptance criteria. Confirm acceptance evidence for any entry gate before implementation.
2. Run `python3 scripts/issue_workflow.py check NUMBER`. All native blockers must be closed as completed. Epic integration also requires completed children.
3. When the issue is assigned to you or you take it for implementation, run `python3 scripts/issue_workflow.py branch NUMBER` from a clean working tree. The helper checks prerequisites, fetches main, and creates or updates the issue branch without discarding commits.
4. Implement the issue and run its acceptance checks.
5. Open a PR targeting main with `Closes #NUMBER`. Verify that it closes exactly one open same-repository issue, uses its canonical branch, and implements that issue. Record acceptance-check results in the PR and leave it open for owner review.
6. Before merging, recheck live readiness, update the branch to include current main, and confirm all configured GitHub requirements pass. Apply the owner approval and explicit merge authorization gate in [AGENTS.md](../AGENTS.md).

The helpers require Git, Python 3, and authenticated GitHub CLI access. GitHub issues and native sub-issue/blocking relationships are the backlog source of truth.

## Branches

- Create a branch when an issue is assigned or taken for implementation and its prerequisites are accepted. Issue creation does not create a branch. Keep backlog issues without branches until work is taken.
- One branch per issue, including epic integration work.
- Name: `<github-issue-number>-<issue-title-in-kebab-case>`. Strip `[ERA-xxx]` or `[EPIC-xx]` title prefixes.
- Use flat names. Namespaces require an explicit user instruction.
- Base: latest `origin/main`, unless the user specifies otherwise.
- Refresh existing issue branches before implementation and preserve existing commits.
- Merged issue branches are deleted automatically.

## Issue readiness

Use exactly one issue type: `bug`, `spike`, `implement`, or `epic`. Parent/sub-issue relationships group work; native blocked-by links define prerequisites. Close prerequisites as completed only after their acceptance criteria pass. A `not_planned` closure does not unblock work.

Issue references, branch names, prerequisites, and acceptance evidence are agent and owner review responsibilities. The local helper checks live prerequisites before work starts; these rules do not run as GitHub Actions. Epic membership groups work and does not sequence unrelated children.

## Main ruleset

The active `main` branch ruleset requires pull requests, resolved review threads, and linear history, and blocks force pushes and deletion. It has no bypass actors, so administrators also follow it. There are no required workflow statuses. Inspect the live settings with `gh ruleset list` and `gh ruleset view ID`; GitHub is the source of truth for enforcement.

With no required status checks, GitHub does not enforce an up-to-date branch through a strict status-check setting. Updating the branch before merging remains a workflow requirement.

GitHub's required approving-review count is zero because the solo owner cannot approve a PR authored through their own account. Owner review and explicit merge authorization remain required by AGENTS.md.
