# Git and issue workflow

AGENTS.md defines branch naming and PR rules. This document supplies the issue lifecycle and commands. GitHub issue numbers identify branches; ERA/EPIC IDs remain plan traceability identifiers. Use `planning/github-map.json` to look up their actual numbers and URLs.

## Start an issue

1. Read the GitHub issue, its parent epic, and acceptance criteria. Run `python3 scripts/issue_workflow.py check NUMBER`. Completion: the issue is open, has one regular type label or the epic label, and every effective prerequisite is closed as completed. An epic integration task also requires its children accepted.
2. Record file ownership for concurrent work. Run `python3 scripts/issue_workflow.py branch NUMBER`. It checks live prerequisites, fetches main, and creates or reuses the issue branch. Completion: the current branch matches the canonical issue name and its base includes current main; existing commits are preserved.
3. Implement and verify the issue's acceptance criteria. Completion: evidence identifies the exact candidate and all required checks pass.
4. Open a PR to main with the template's `Closes #NUMBER` line and verification details. Completion: the required `issue-policy` and `Planning integrity` checks pass, the issue remains ready, and the owner reviews the candidate.
5. Squash-merge the PR and record acceptance evidence. Completion: the issue closes as completed and the integrated behavior passes its checks. If merge alone does not establish acceptance, keep the issue open and use `Refs #NUMBER` only after an explicit workflow exception is agreed; the default required PR policy uses a closing reference.

The initial repository creation commit records the already accepted plan. Subsequent preparation changes use setup issue #1 and a PR. The same workflow applies to later bug fixes, spikes, implementation tasks, and epic integration work.

## Types and dependencies

Use exactly one type label per issue: `bug`, `spike`, `implement`, or `epic`. `bug` describes incorrect behavior; `spike` investigates a question with a concrete decision/evidence deliverable; `implement` is regular delivery work; `epic` groups coupled children into one application capability. The hosting investigation is a spike; other planned child tasks are implementation issues. Parent/sub-issue relationships provide grouping without extra type labels.

Native GitHub blocked-by links encode direct issue prerequisites plus each child's epic entry issues and required completed epics. Epic blocked-by links encode start gates only. Parent child progress and final acceptance criteria account for completion; treating all children as epic start blockers would prevent useful concurrent work.

A prerequisite qualifies as accepted only when closed with `state_reason=completed`. A discarded/not-planned issue does not unblock delivery. Reopening a prerequisite blocks dependent work again. Update native dependency links and the manifest together when approved scope changes alter the graph. The PR policy reads native links and checks that the planned blockers have not been omitted.

The required `issue-policy` status verifies the closing reference, branch/issue match, type, open state, native/planned blockers, and epic child acceptance. It reruns on PR changes and issue events; a periodic/manual refresh also handles dependency changes and missed events. An unblocked merge check does not authorize starting work without the live preflight check.

## Protection and maintenance

Main requires a PR, successful required statuses, an up-to-date branch, resolved review threads, and linear history. Rules apply to administrators; force pushes and branch deletion are disabled. An approving-review count of zero permits a solo project owner to use PRs without needing a second account. Review remains an attended owner responsibility.

The policy workflow runs from the trusted default branch after planning CI, on issue events, and on periodic/manual refresh. It reads PR metadata through the API and consumes no PR-produced artifacts. It never checks out or executes a PR head with its status-writing token. Planning CI runs separately with read permissions. Keep required status names synchronized with branch protection when changing workflow names.

Each open planned issue has a remote branch created from main during setup. Before work starts, refresh that branch through the helper. Merged issue branches are removed automatically. This avoids developing unrelated issues on an epic branch; the epic branch is reserved for its own integration/acceptance changes.
