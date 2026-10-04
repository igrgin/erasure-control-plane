# Git and issue workflow

## Start work

1. Read the GitHub issue, its parent epic, and acceptance criteria. Confirm acceptance evidence for any entry gate before implementation.
2. When receiving a new issue, check live GitHub data with `gh`. Take it only when it is open, has no assignees, and has no native blocked-by relationships. Confirm its supported type and any epic entry gates as described below.
3. Assign the eligible issue to the logged-in GitHub account with `gh issue edit NUMBER --repo igrgin/erasure-control-plane --add-assignee @me`. Re-read the issue to confirm the assignment before starting implementation.
4. After assignment, use Git from a clean working tree to fetch origin and create or update the dedicated issue branch under the branch rules below. Preserve existing commits.
5. Implement the issue and run its acceptance checks.
6. Open a PR targeting main with `Closes #NUMBER`. Verify that it closes exactly one open same-repository issue, uses its canonical branch, and implements that issue. Record acceptance-check results in the PR and leave it open for owner review.
7. Before merging, recheck that the issue is open, assigned to the logged-in account, and has no blockers. Update the branch to include current main and confirm all configured GitHub requirements pass. Apply the owner approval and explicit merge authorization gate in [AGENTS.md](../AGENTS.md).

Use Git and authenticated GitHub CLI access. GitHub issues and native sub-issue/blocking relationships are the backlog source of truth.

## Branches

- Create a branch after the issue is assigned to the logged-in account and its entry gates are accepted. Issue creation does not create a branch. Keep backlog issues without branches until work is taken.
- One branch per issue, including epic integration work.
- Name: `<github-issue-number>-<issue-title-in-kebab-case>`. Strip `[ERA-xxx]` or `[EPIC-xx]` title prefixes.
- Use flat names. Namespaces require an explicit user instruction.
- Base: latest `origin/main`, unless the user specifies otherwise.
- Refresh existing issue branches before implementation and preserve existing commits.
- Merged issue branches are deleted automatically.

## Issue readiness

Use exactly one issue type: `bug`, `spike`, `implement`, or `epic`. Parent/sub-issue relationships group work; native blocked-by links define prerequisites. Close prerequisites as completed only after their acceptance criteria pass. Remove a blocked-by relationship only after that prerequisite is accepted; a `not_planned` closure does not count as acceptance.

Issue references, branch names, prerequisites, and acceptance evidence are agent and owner review responsibilities. Check live prerequisites before work starts; these rules do not run as GitHub Actions. Epic membership groups work and does not sequence unrelated children.

Use `gh issue view NUMBER --repo igrgin/erasure-control-plane --json state,assignees,labels,body` to inspect the issue. Use `gh api user --jq .login` to identify the logged-in account. When resuming an issue already claimed by that account, keep its assignment and branch, and recheck its open state and blockers. An issue assigned to another account is unavailable for implementation. Inspect native relationships with:

```sh
gh api --paginate repos/igrgin/erasure-control-plane/issues/NUMBER/parent
gh api --paginate repos/igrgin/erasure-control-plane/issues/NUMBER/dependencies/blocked_by
gh api --paginate repos/igrgin/erasure-control-plane/issues/NUMBER/sub_issues
```

A parent endpoint 404 can mean there is no parent; confirm the issue itself is accessible. Other lookup failures leave readiness unverified. Read the parent epic's entry gates when present. The blocked-by query must return no issues before taking or resuming work. For epic integration, every child must have `state: closed` and `state_reason: completed`. Record the readiness conclusion and any acceptance evidence before implementation.
