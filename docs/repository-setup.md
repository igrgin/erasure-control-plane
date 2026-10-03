# Repository preparation

Repository: [igrgin/erasure-control-plane](https://github.com/igrgin/erasure-control-plane), public, default branch `main`. Preparation is tracked by [issue #1](https://github.com/igrgin/erasure-control-plane/issues/1).

The accepted plan is initial commit `7676b01` at digest `be081ef4cee596a5ae903f184eec1a87cfdb13d9efd5a98db9dffa174a9a95ae`. Authorized repository preparation is delivered through issue #1's dedicated branch and PR.

## GitHub records

The first-release milestone contains ten native parent epics and 42 native sub-issues. The graph has 139 blocked-by links covering direct prerequisites and inherited epic entry gates. [The mapping](../planning/github-map.json) records every ID, URL, blocker, and canonical branch. The hosting assessment is labeled `spike`; other children use `implement`; parents use `epic`; `bug` is available for defects.

Every open planned task receives a remote branch from the prepared main revision. These branches are starting points, not authorization to implement blocked tasks. The readiness helper refreshes their main base before work. Closed/merged issue branches are removed automatically.

## Protection and PR checks

Main requires PRs for every actor, including administrators, with linear history and resolved review threads. Force pushes and branch deletion are disabled. Squash merge is the sole enabled merge method. Required checks are `Planning integrity` and `issue-policy`, with the PR branch kept up to date with main. Zero mandatory approving reviews allows a solo owner to use the PR workflow; owner acceptance remains necessary.

Planning CI checks artifact consistency and policy tests. The trusted issue-policy workflow reads metadata after planning CI and on issue events/periodic/manual refresh. It executes default-branch code, consumes no PR-produced artifacts, and posts the status to the actual PR head. It verifies the closing issue reference, canonical branch, issue type/state, planned/native blockers, and accepted epic children for epic integration PRs.

The initial workflow-installation PR is a bootstrap case: planning CI runs on GitHub, while the new policy is executed locally against its actual GitHub metadata and reports a verified `issue-policy` status. Once installed, the trusted workflow supplies that status for subsequent PRs. No administrator bypass is used to merge preparation.

## Verification evidence

- Planning validation covers 10 epics, 42 issues, 15 requirements, acyclic gates, readiness examples, document links, and candidate hashes.
- Ten policy tests cover valid PRs and failures for missing/foreign issue references, wrong branches, omitted native blockers, incomplete/discarded prerequisites, conflicting labels, and incomplete epic integration.
- The publication verifier compares all 52 remote task titles/bodies/labels/milestones, 42 child relationships, and 139 blockers with the manifest.
- Live preflight allows demo blueprint issue #48 and denies foundation issue #12 while #48 remains open.
- Final setup observes GitHub CI, protected-main configuration, and all dedicated issue branches before handoff.

These checks verify repository preparation. The application, adapters, deployed sources, infrastructure purchases, and live demo remain implementation work.
