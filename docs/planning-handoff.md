# Planning handoff and provenance

Planning date: 2026-10-03, Europe/Zagreb. Scope: development planning only.

## Accepted intent from this conversation

The project owner requested a personal architecture-focused project using Java/Spring Boot and React, a full end-to-end first release, GitHub-ready issue planning, deployment planning, and an explanation/evidence path for scaling. Subsequent clarification replaced persons with business accounts and selected one internal operating company. Customer business accounts are tenants in a shared system; this is not a service sold to customers. Customers can request deletion/transformation through existing channels, and employees enter the request.

Coverage remains limited to registered sources, execution requires accountable source-owner approval, and Erasure performs no independent post-execution deletion verification. The user described adapters reporting account data amounts over time and asked for source-specific retention/time behavior. The plan resolves that with precise request intervals and explicitly declared summary/selection precision per source.

## Pathfinder admission and adoption

Selected lifecycle: `artifact-delivery`. Selected workflow/profile: `milestone-phase` / `phase`. Control policy: `workflow-lite`. Review: advisory owner review for this planning run. Integration level: `development-only`.

The smallest fit is a retained spec and milestone roadmap with issue groups and human UAT for implementation. The source of truth is the written artifact candidate plus the owner's decisions in this conversation. Delivery, release, and feedback belong to the project owner; GitHub will become issue intake after repository creation. No connected release or production authority is assumed.

A proposed configuration was validated with the installed Pathfinder CLI before adoption into ignored `.pathfinder/project.json`. Adoption adds a local planning-integrity check, finite review/repair bounds, artifact-version acceptance before future implementation, and human UAT for epics. There was no previous configuration to replace. The user's invocation authorizes preparing this planning workflow; it does not approve the new specification/plan candidate or external publication.

Accessible capabilities: local files, planning validation, and official documentation research. Observed missing project integrations: Git repository, GitHub remote/issues, application code/test runtime, deployment environment, corporate identity/source connections, and authenticated gate dispatcher. No sub-agent or external message was used.

## Artifact mapping

| Contract role | Record | Observed status |
| --- | --- | --- |
| Intent | README and accepted intent above | User intent and clarifications recorded |
| Spec | specification.md | Proposed owner-review candidate |
| Context | CONTEXT.md | Resolved domain glossary |
| Roadmap and dependency waves | development-plan.md | Ten epics with start gates and issue-level integration prerequisites |
| Phase plans | planning/issues.json and planning/issues/ | 42 bounded issue definitions with acceptance/checks |
| Candidate | planning/candidate.json | SHA-256-bound planning files |
| Verification | scripts/validate_plan.py | Structural checker; result recorded below |
| Review | This handoff and issue acceptance instructions | Planning self-review; owner review pending |
| UAT | development-plan.md and ERA-032/ERA-036 | Defined future application UAT; not performed |
| Incident intake | incident-template.md | Template prepared for later execution |

Paths in this table are artifact roles, not a claim that a running implementation has passed those stages.

## Verification and self-review

The planning candidate passed the local planning-integrity check: 42 unique child issues, ten epic tasks, complete REQ-01 through REQ-15 coverage, acyclic issue/epic prerequisites, valid local links, and matching artifact hashes. Pathfinder configuration validation passed. These checks establish planning consistency; they do not prove application behavior.

Self-review checked that authorization/durable execution begin in the foundation epic, adapters stay independent, proposals do not inherit inventory authority, retention exceptions remain visible, lost responses are not blind retries, and restored control-plane state cannot replay destructive work without reconciliation. Scaling claims are separated from measurements to be gathered. Each epic has a user-visible exit demonstration and implementation checks.

The directory is not a Git repository. No `start` run or authenticated automated gate ledger has been created, because its candidate snapshot needs Git and repository creation was explicitly deferred. No approval signature or owner acceptance has been invented. This is a native planning handoff awaiting owner review, not an automated delivery completion.

## Remaining owner actions

1. Review the exact specification and plan candidate identified in planning/candidate.json. Proposed technical defaults include local Keycloak, PostgreSQL row policies, second-precision UTC intervals, hourly/daily sample inventory, and a single-VM Compose deployment.
2. Accept or revise that candidate before implementation. Revisions require a new candidate digest and affected review.
3. Authorize creation of the Git/GitHub repository and issue publication in a later task; retain ERA IDs and actual GitHub mappings.
4. Extend the planning-only Pathfinder scope/checks for implementation and initialize its run against the actual repository.
5. Choose deployment host/domain and provide the required credentials when deployment work begins. Record actual deployment, recovery, UAT, and scale evidence before release acceptance.

No further product decision blocks this planning candidate. Provider-specific infrastructure and exact dependency versions are implementation tasks with explicit verification, rather than unresolved product scope.

## Epic revision

The owner requested that coupled issue groups become explicit epic tasks and that unblocked epics support concurrent development. The revised candidate supersedes the previous planning digest. No application requirements or release boundaries changed.

The earlier epic revision introduced nine body files describing application capabilities, coupling, child task lists, start gates, external child dependencies, ownership, and combined UAT. Sequencing-only blockers were removed: closure/audit/deployment can begin on the accepted foundation, owner review can begin after registration, heterogeneous scoping after capabilities, and workload tooling after inventory ingestion. Real integration dependencies remain on the issue that needs them. The validator checks both dependency graphs and the published readiness examples.

The foundation's shared contract acceptance remains a common prerequisite. Parallel work uses task-level file claims and coordinated integration; it does not grant external publication/deployment authority. The updated plan awaits review at the exact revision in planning/candidate.json. Observed integration remains development-only.

## Demo revision

The owner requested source variety, dummy-data setup, an explicit demo plan, and assessment of visible hosting. EPIC-10 adds six issues, ERA-037 through ERA-042. The required sources are PostgreSQL, MongoDB, and Redis; optional storage extensions remain outside first-release acceptance. ERA-011 now explicitly owns the MongoDB adapter. Demo setup owns its source environment, not another duplicate implementation.

The blueprint can start immediately and feeds the foundation. Fixtures and hosting comparison can proceed alongside application work. The cache adapter consumes real worker/capability inputs. Three-source guided scenarios feed deployed UAT; public launch follows it and final architecture handoff consumes visibility evidence. The combined issue/epic gate graph remains acyclic.

REQ-15 adds reproducible synthetic sources and actual public-demo evidence to the first-release acceptance scope. Hosting research was completed from official provider documentation on 2026-10-03; it establishes a plausible paid-VM option, not measured capacity or a budget commitment. No infrastructure, public endpoint, repository, or GitHub task was created. Final provider/budget and deployment acceptance remain owner actions when those implementation issues run. Candidate hashes in planning/candidate.json supersede the previous epic-only revision.
