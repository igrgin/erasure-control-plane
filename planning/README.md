# GitHub-ready backlog

The backlog contains ten epic tasks and 42 proposed implementation issues for one milestone, `v0.1 end-to-end demonstration`. [issues.json](issues.json) is the machine-readable index; [the development plan](../docs/development-plan.md) gives epic capabilities, start gates, and concurrent scheduling.

Each EPIC ID identifies a parent task and each ERA ID identifies a child implementation issue. These local IDs are not GitHub issue numbers. The [epic bodies](epics/EPIC-01.md) describe coupled capabilities and include child task lists. The issue Markdown files are ready to use as issue bodies. Preserve these IDs when publishing so dependencies and requirement coverage remain traceable.

## Later repository and issue creation

1. Review and accept the specification and plan revisions recorded in [candidate.json](candidate.json). Revise them first if needed.
2. Create the Git repository and GitHub remote when authorized. Commit README, CONTEXT, docs, planning, and scripts; `.pathfinder/` remains ignored local execution state.
3. Create the milestone and labels `type:epic`, `type:implementation`, and `epic:epic-01` through `epic:epic-10`.
4. Create ten parent epic tasks from `epics` and 42 child implementation issues from `issues` in the manifest. Use each body file and `[EPIC-xx] Title` or `[ERA-xxx] Title`. GitHub CLI supports creating issues from a body file. [GitHub issue creation](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue).
5. Save a local epic/issue ID → GitHub issue URL/number mapping in a committed tracking file. After all tasks exist, update dependency references and parent child-task lists with actual links. Replace local documentation links with committed repository URLs. The parent task list is the required portable grouping; a native parent/sub-issue relationship may also be added when available. Do not assume GitHub numbers will match ERA IDs.
6. Check existing tasks by EPIC/ERA ID before retrying publication so an interrupted import cannot create duplicates. Verify labels, milestone, bodies, and mappings after creation.
7. Optionally create a GitHub Project with Backlog, Ready, In progress, Review, and Done views. Group by epic and mark a child issue Ready only after its epic start gates, issue dependencies, design inputs, and file claims are satisfied. Track blocked children without falsely marking the entire epic blocked.

This step is deliberately future work. No repository or issue has been created, and the plan includes no tool that silently publishes it. A provider-specific deployment target and credentials are also selected at execution time.

## Local verification

Run `python3 scripts/validate_plan.py` from the project root. It verifies issue files, required issue sections, unique IDs, issue and epic dependency cycles, child membership, start prerequisites, concurrent readiness examples, local document links, requirement coverage, and the candidate's file hashes. It does not prove implementation correctness or owner acceptance.

Planning requirements checked by that command are PLAN-1, complete epic/child-issue records; PLAN-2, consistent dependency and requirement mapping; and PLAN-3, reviewable documents bound to a candidate revision.
