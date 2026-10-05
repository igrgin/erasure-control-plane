# Git and issue workflow

## Work sequence

1. Inspect the issue, any parent epic, and their acceptance criteria on GitHub. Record the readiness conclusion and entry-gate evidence.
2. Take or resume the issue.
3. Fetch the latest remote state and prepare the issue branch.
4. Implement the issue and run its acceptance checks.
5. Open the PR with acceptance-check results and submit it for owner review.
6. Address review feedback, refresh the branch, and rerun affected checks. Recheck issue readiness, assignment, and GitHub merge requirements.
7. Await the owner's review decision and merge instruction, then merge the PR.

## Issue readiness and assignment

GitHub issues and native relationships are the backlog source of truth. Work can start or resume when:

- The issue is open and has exactly one type label among `bug`, `spike`, `implement`, and `epic`.
- Every blocking prerequisite is closed as `completed`. A `not_planned` closure does not satisfy a prerequisite.
- Any issue or parent-epic entry gate has acceptance evidence.
- For epic integration, every child is closed as `completed`. Epic membership does not sequence unrelated children.

Take an unassigned eligible issue by assigning it to the logged-in GitHub account and verifying the assignment. Resume an eligible issue already assigned to that account. Issues assigned to another account remain with their assignee.

Readiness and assignment must remain valid through merge. Verify them against live GitHub data; lookup failures leave readiness unverified. A standalone issue may have no parent. Close issues as `completed` only after their acceptance criteria pass.

## Branch rules

- One branch per issue, including epic integration work. Create it only after assignment.
- Name it `<github-issue-number>-<issue-title-in-kebab-case>`, stripping `[ERA-xxx]` or `[EPIC-xx]` prefixes. Keep its original name if the issue title later changes.
- Use a flat name unless the user explicitly requests a namespace.
- Begin branch work from a clean working tree. Create new branches from the latest `origin/main`; reuse existing local or remote issue branches and rebase onto the latest `origin/main`, preserving their commits. Use another base only when the user explicitly selects it.
- Before merge, the branch must include current `origin/main`, with affected checks rerun after rebasing.

## PR rules

Each PR targets `main`, implements its dedicated branch's issue, and closes exactly that issue with a closing reference in its body. Record the issue's acceptance-check results in the PR. All configured GitHub merge requirements must pass.

Owner review and merge authorization are governed by [AGENTS.md](../AGENTS.md).
