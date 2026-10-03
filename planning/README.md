# Published GitHub backlog

The accepted first-release backlog has ten epic tasks and 42 child issues, grouped under the `v0.1 end-to-end demonstration` milestone in [igrgin/erasure-control-plane](https://github.com/igrgin/erasure-control-plane/issues). Repository preparation is tracked separately as issue #1.

[issues.json](issues.json) defines the plan's capabilities and dependencies. [github-map.json](github-map.json) maps every ERA/EPIC ID to its actual GitHub issue number, URL, native blockers, and branch name. The [development plan](../docs/development-plan.md) explains concurrent readiness and epic acceptance.

## Relationships and issue types

GitHub parent/sub-issue links connect every child to its epic. Native blocked-by links encode direct issue prerequisites and inherited epic start gates. Epics require their entry gates, while child completion and the combined demonstration determine final epic acceptance. Use the live readiness helper in [the Git workflow](../docs/git-workflow.md) before implementation.

The four type labels are `bug`, `spike`, `implement`, and `epic`. ERA-041 hosting feasibility is a spike. The other planned children are implementation tasks. Each issue has exactly one type label. Extra epic-group labels are unnecessary because native parent relationships provide the grouping.

Published bodies link to actual GitHub issues and repository documentation. The Markdown body files remain the accepted planning sources; metadata in the manifest describes the live publication. Preserve ERA/EPIC IDs when revising tasks so acceptance and requirement links stay traceable.

## Maintenance and verification

`python3 scripts/publish_backlog.py verify` checks remote titles, bodies, labels, milestones, parents, and native blockers against the manifest/map. The explicitly invoked `publish` action reconciles approved backlog changes idempotently; its `branches` action creates missing issue branches from current main while preserving existing branches. External mutations still require authorization for the requested change.

`python3 scripts/validate_plan.py` checks local artifact hashes, issue/epic graph consistency, start prerequisites, concurrency examples, links, and requirement coverage. `python3 -m unittest discover -s scripts -p 'test_*.py'` verifies the GitHub policy's important failure cases. These checks do not establish application correctness or epic UAT.

The original accepted planning revision is preserved in [accepted-plan.json](accepted-plan.json) and initial commit `7676b01`. [candidate.json](candidate.json) binds the repository preparation files derived from that approved plan. PLAN-1 covers complete epic/child records; PLAN-2 covers consistent prerequisites and requirement links; PLAN-3 covers reviewable candidate artifacts.
