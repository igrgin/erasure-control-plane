# Accepted plan and repository handoff

Date: 2026-10-03, Europe/Zagreb. Product implementation and hosting remain backlog work.

## Accepted intent and artifact revision

The project owner accepted planning candidate `be081ef4cee596a5ae903f184eec1a87cfdb13d9efd5a98db9dffa174a9a95ae` in this conversation with the statement "I accept this plan." The original file hashes and attended acceptance provenance are preserved in planning/accepted-plan.json and initial commit `7676b01`.

That plan defines one operating company's internal cleanup control plane, customer business accounts as tenants, accountable source-owner approval, registered-source coverage, adapter-reported results, and no independent deletion verification. It includes ten epics, 42 issues, three synthetic source engines, deployment, scaling evidence, and public demo planning.

The same user message authorizes Git/GitHub setup, publication of the backlog, protected main, PR/issue linkage, four type labels, dedicated issue branches, and agent instructions. The later visibility reply explicitly selects public `igrgin/erasure-control-plane`. Repository preparation derives from the accepted plan and does not authorize application implementation, infrastructure purchase, or live deployment.

## Pathfinder configuration and observed integration

Lifecycle: artifact-delivery. Workflow/profile: milestone-phase/phase. Control policy: workflow-lite. Capability: development-only. The project owner owns delivery, release decisions, and feedback through GitHub issues.

The local configuration in ignored `.pathfinder/project.json` covers planning/governance paths and the planning-integrity and GitHub-policy test commands. Its finite review/repair bounds remain one repair pass, three rounds, and explicit command timeouts. Main's GitHub checks implement repository governance; application CI/UAT and deployment evidence must be added by the relevant issues.

Observed integrations are Git, the public GitHub repository, native issue/sub-issue and blocked-by APIs, GitHub Actions, and branch protection. Actual source systems, application runtime, deployment/identity credentials, and an authenticated Pathfinder gate dispatcher remain absent. Attended acceptance is recorded honestly; no dispatcher signature or production evidence is fabricated.

## Record mapping

| Record | Authority and use |
| --- | --- |
| planning/accepted-plan.json | Exact accepted original planning revision and conversation provenance |
| planning/candidate.json | Hash-bound current planning and authorized repository preparation |
| docs/specification.md and CONTEXT.md | Requirements and business vocabulary |
| docs/development-plan.md and planning/issues.json | Epic capabilities, prerequisites, checks, and concurrency |
| planning/github-map.json | Published issue IDs, URLs, blocker mapping, and dedicated branch names |
| AGENTS.md and docs/git-workflow.md | Agent Git rules and live issue-readiness procedure |
| scripts/validate_plan.py and scripts/test_github_policy.py | Planning consistency and policy behavior checks |
| .github/workflows/ | GitHub planning CI and trusted metadata-only issue-policy enforcement |
| docs/deployment.md, docs/scaling.md, docs/demo-plan.md | Future runtime acceptance and evidence requirements |
| docs/incident-template.md | Later incident intake linked to accepted revisions |

## Preparation verification

Local checks cover ten epics, 42 child issues, REQ-01 through REQ-15, native/planned dependency consistency, readiness examples, valid links, and candidate hashes. Policy tests cover missing/foreign issue references, incorrect branches, omitted planned blockers, pending/discarded prerequisites, type conflicts, and incomplete epic integration.

The publication verifier compares every remote task's title, body, label, milestone, parent, and blockers with the manifest/map. The initial accepted plan is the repository-creation commit. Remaining preparation changes are handled by issue #1 on its dedicated branch and through a PR. GitHub status/protection and issue-branch checks are observed before the final handoff in the conversation.

These are preparation checks. They establish no application behavior, customer-data cleanup, production capacity, or public live demo.

## Next owner actions

Select ready work using the live GitHub readiness helper. ERA-037 demo blueprint is initially eligible; downstream foundation, fixture, and hosting tasks unlock when its acceptance is recorded. Accept each issue and epic against its real integrated candidate and listed checks. Choose/authorize actual infrastructure and retain deployment, restore, UAT, scale, and public-visibility evidence when those issues run.

The GitHub issue policy uses completed closure as the prerequisite acceptance signal. The project owner must close issues as completed only after their criteria and required demonstrations pass. A discarded issue does not unblock implementation.
