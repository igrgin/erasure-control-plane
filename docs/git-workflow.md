# Git and issue workflow

## Work sequence

1. Read the issue, any parent epic, and their acceptance criteria using `gh`. Confirm readiness under the rules below. For a new issue, require no assignees, assign it to the logged-in account with `gh issue edit NUMBER --add-assignee @me`, and verify the assignment. Resume an issue already assigned to that account; leave issues assigned to another account for their assignee.
2. From a clean working tree, run `git fetch origin`. Create the issue branch with `git switch -c ISSUE-BRANCH origin/main`. If it already exists locally or on origin, reuse it and rebase onto the latest `origin/main`, preserving its commits. Use another base only when the user explicitly selects it.
3. Implement the issue and run its acceptance checks.
4. Open a PR targeting `main` with `Closes #NUMBER`, closing exactly that issue from its dedicated branch. Record acceptance-check results in the PR and leave it open for owner review.
5. Before merging, recheck readiness and assignment, fetch origin, and rebase onto current `origin/main` if needed. Rerun checks affected by the rebase and confirm GitHub requirements pass. Follow the owner approval and explicit merge authorization gate in [AGENTS.md](../AGENTS.md).

## Branch naming

- One branch per issue, including epic integration work.
- Name it `<github-issue-number>-<issue-title-in-kebab-case>`, stripping `[ERA-xxx]` or `[EPIC-xx]` prefixes. Keep its original name if the issue title later changes.
- Use a flat name unless the user explicitly requests a namespace.

## Readiness

GitHub issues and native relationships are the backlog source of truth. An issue is ready when it is open, has exactly one type label among `bug`, `spike`, `implement`, and `epic`, and every blocking prerequisite is closed as `completed`. Close issues as `completed` only after their acceptance criteria pass. A `not_planned` closure does not satisfy a prerequisite. Confirm acceptance evidence for any issue or parent-epic entry gate before implementation. Epic membership does not sequence unrelated children; epic integration requires every child to be closed as `completed`.

Use `gh api user --jq .login` to identify the logged-in account. Inspect issue state, assignees, labels, and acceptance criteria with `gh issue view NUMBER`. Inspect native relationships with:

```sh
gh api --paginate repos/igrgin/erasure-control-plane/issues/NUMBER/parent
gh api --paginate repos/igrgin/erasure-control-plane/issues/NUMBER/dependencies/blocked_by
gh api --paginate repos/igrgin/erasure-control-plane/issues/NUMBER/sub_issues
```

For each prerequisite or epic child, check `state: closed` and `state_reason: completed`. A parent lookup reporting no parent is expected for a standalone issue; other lookup failures leave readiness unverified. Record the readiness conclusion and entry-gate evidence before implementation.
