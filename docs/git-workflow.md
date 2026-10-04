# Git and issue workflow

## Start work

1. Read the GitHub issue, its parent epic, and acceptance criteria. Confirm acceptance evidence for any entry gate before implementation.
2. Check live readiness with `gh` as described below. Proceed only when the issue is open, has exactly one supported type, all native blockers are completed, and any epic integration children are completed.
3. When the issue is assigned to you or you take it for implementation, use Git from a clean working tree to fetch origin and create or update the dedicated issue branch under the branch rules below. Preserve existing commits.
4. Implement the issue and run its acceptance checks.
5. Open a PR targeting main with `Closes #NUMBER`. Verify that it closes exactly one open same-repository issue, uses its canonical branch, and implements that issue. Record acceptance-check results in the PR and leave it open for owner review.
6. Before merging, recheck live readiness, update the branch to include current main, and confirm all configured GitHub requirements pass. Apply the owner approval and explicit merge authorization gate in [AGENTS.md](../AGENTS.md).

Use Git and authenticated GitHub CLI access. GitHub issues and native sub-issue/blocking relationships are the backlog source of truth.

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

Issue references, branch names, prerequisites, and acceptance evidence are agent and owner review responsibilities. Check live prerequisites before work starts; these rules do not run as GitHub Actions. Epic membership groups work and does not sequence unrelated children.

Use `gh issue view NUMBER --repo igrgin/erasure-control-plane` to read the issue and its type labels. Inspect native relationships with:

```sh
gh api --paginate repos/igrgin/erasure-control-plane/issues/NUMBER/parent
gh api --paginate repos/igrgin/erasure-control-plane/issues/NUMBER/dependencies/blocked_by
gh api --paginate repos/igrgin/erasure-control-plane/issues/NUMBER/sub_issues
```

A parent endpoint 404 can mean there is no parent; confirm the issue itself is accessible. Other lookup failures leave readiness unverified. Read the parent epic's entry gates when present. For each blocker, require `state: closed` and `state_reason: completed`. For epic integration, apply that same criterion to every child. Record the readiness conclusion and any acceptance evidence before implementation.
