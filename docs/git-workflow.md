# Git and issue workflow

## Start work

1. Read the GitHub issue, its parent epic, and acceptance criteria.
2. Run `python3 scripts/issue_workflow.py check NUMBER`. All native blockers must be closed as completed. Epic integration also requires completed children.
3. When the issue is assigned to you or you take it for implementation, run `python3 scripts/issue_workflow.py branch NUMBER` from a clean working tree. The helper checks prerequisites, fetches main, and creates or updates the issue branch without discarding commits.
4. Implement the issue and run its acceptance checks.
5. Open a PR targeting main with `Closes #NUMBER` and wait for the project owner's review. Only the owner approves PRs. Agents must never submit approving reviews, including through the owner's GitHub account. Merge only after the owner approves the result, explicitly instructs you to merge, and required checks pass.

The helpers require Git, Python 3, and authenticated GitHub CLI access. GitHub issues and native sub-issue/blocking relationships are the backlog source of truth.

## Branches

- Create a branch when an issue is assigned or taken for implementation and its prerequisites are accepted. Issue creation does not create a branch. Keep backlog issues without branches until work is taken.
- One branch per issue, including epic integration work.
- Name: `<github-issue-number>-<issue-title-in-kebab-case>`. Strip `[ERA-xxx]` or `[EPIC-xx]` title prefixes.
- Use flat names. Namespaces require an explicit user instruction.
- Base: latest `origin/main`, unless the user specifies otherwise.
- Refresh existing issue branches before implementation and preserve existing commits.
- Merged issue branches are deleted automatically.

## Dependencies and checks

Use exactly one issue type: `bug`, `spike`, `implement`, or `epic`. Parent/sub-issue relationships group work; native blocked-by links define prerequisites. Close prerequisites as completed only after their acceptance criteria pass. A `not_planned` closure does not unblock work.

The `issue-policy` status checks the PR's closing issue, canonical branch, type, open state, native blockers, and completed epic children. It runs trusted default-branch code after `Repository checks`, on issue events, and on scheduled/manual refresh. `Repository checks` runs policy tests with read permissions.

## Main protection

Main requires PRs for administrators too, successful `Repository checks` and `issue-policy` statuses, an up-to-date branch, resolved review threads, and linear history. Force pushes and deletion are disabled.

GitHub's required approving-review count is zero because the solo owner cannot approve a PR authored through their own account. The owner reviews and approves the result directly. This setting does not authorize agents to approve or merge PRs on their own.
