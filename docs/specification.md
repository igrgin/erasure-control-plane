# Product requirements

Status: proposed baseline for owner review. The user's stated intent governs this document; technical defaults below are planning decisions, not claims of completed implementation.

Erasure demonstrates architecture for business-account data cleanup within one operating company. Many business accounts share one system, and adapters connect to shared company sources. Employees operate Erasure. A business customer can ask the operating company to delete or anonymize its data through an existing external channel; an employee records the request and its reference internally. Erasure is not a service offered to customers. Customer self-service is outside the first release. A separate synthetic public demonstration offers a read-only tour and owner-controlled live employee-role sessions; it grants no access to real company systems.

Business-account cleanup is the product scope. It must not claim that legal persons have a GDPR erasure right. GDPR recital 14 distinguishes legal-person data from natural-person data. [Official regulation](https://eur-lex.europa.eu/eli/reg/2016/679/). Erasure does not decide legal eligibility or certify anonymization.

## Actors and authority

- An operator selects an authorized business account, creates a request, and coordinates blockers.
- A source owner reviews and approves, rejects, or asks for a revised proposal for sources they own.
- An auditor reads authorized request history and exports.
- A platform administrator registers sources and manages employee grants and adapter credentials.
- An adapter principal publishes summaries and receipts and consumes commands only for its registered source and permitted tenant scope.

Employees may have explicit grants across multiple business accounts. Tenant scope must come from authenticated grants, not merely a browser header. Source ownership alone does not grant access to every tenant. The same employee may hold multiple roles in the demo; authorization checks remain separate. Mandatory two-person approval is a later policy option.

## Observable requirements

| ID | Requirement | Acceptance evidence | Accountable owner |
| --- | --- | --- | --- |
| REQ-01 | Identify each business account with a stable internal reference and source-local mappings. | Two tenants with overlapping local identifiers cannot be mixed in reads, proposals, or execution. | Project owner |
| REQ-02 | Register sources, owners, adapter principals, and versioned capabilities. | An administrator adds a source through the UI; an unregistered principal cannot publish or execute. | Project owner |
| REQ-03 | Accept source-published, per-account inventory with time buckets and freshness. | Hourly and daily summaries display together without implying unknown periods contain no data. | Source owner |
| REQ-04 | Create an immutable request scope for one tenant and explicit time range. | Source coverage is snapshotted; later registration cannot silently alter an open request. | Operator |
| REQ-05 | Generate versioned, fresh proposals containing cleanup actions, estimates, exclusions, and constraints. | Summary data alone cannot authorize execution; the adapter generates a new proposal. | Source owner |
| REQ-06 | Bind approval to an exact proposal, tenant, source, operation, and time scope. | Expiry, changed policy, changed mapping, changed owner authority, or a changed plan blocks dispatch until revalidation or review. | Source owner |
| REQ-07 | Execute only approved operations through independent adapters. | Three source adapters demonstrate direct relational deletion, dated relational ownership joins, and conditional search-document deletion with receipts and explicit affected/uncertain counts. | Source owner |
| REQ-08 | Recover safely from duplicates, crashes, concurrency, partial results, and unknown outcomes. | Failure injection proves that a lost response never causes an uncontrolled second cleanup. | Project owner |
| REQ-09 | Respect source retention and selectable time precision. | An expired coverage window, a retained subset, and an unsupported time boundary are disclosed and require a decision. | Source owner |
| REQ-10 | Track every scoped source through blockers and a final disposition. | Closure enumerates every source, including rejected, retained, unavailable, and unknown results. | Operator |
| REQ-11 | Preserve attributable audit history and clearly label adapter-reported outcomes. | An auditor can reconstruct approval and attempts from an export; the UI never labels a result independently verified. | Auditor |
| REQ-12 | Enforce employee and adapter authorization throughout HTTP, jobs, exports, and storage. | Negative tests cover tenant, source, and role isolation with nonprivileged database roles. | Project owner |
| REQ-13 | Deploy and operate a small complete environment using synthetic data. | A clean target runs the walkthrough, backup/restore drill, restart recovery, and rollback exercise. | Project owner |
| REQ-14 | Demonstrate how the same semantics support more customers and sources. | Multi-worker tests, repeatable load measurements, and documented growth triggers accompany the release. | Project owner |
| REQ-15 | Reproduce and publicly demonstrate cleanup across relational and search sources with synthetic data. | Seed/reset and guided scenarios pass for two PostgreSQL source databases and Elasticsearch; hosting resources/cost are reviewed and a public HTTPS tour plus controlled live session has actual URL/UAT evidence. | Project owner |

## Time and inventory rules

A request uses a half-open UTC interval `[from, to)`, with second-level precision. The UI lets an operator choose dates or date-times and shows the time zone and normalized boundaries before submission. A calendar-day request becomes the instants bounding that day in the selected time zone; it need not last 24 hours across daylight-saving changes.

Inventory granularity is independent of request precision. A source declares hourly, daily, or another supported interval, a bucket alignment/time zone, the meaning of its timestamp field, and the unit of each measure. Counts and byte estimates remain separate; Erasure never adds incompatible measures. Daily buckets need not have a constant duration. Adapters publish explicit UTC bucket boundaries. Bucket overlap does not imply that every record in the bucket matches a request.

The first release demonstrates hourly PostgreSQL fulfillment/support summaries with exact timestamp selection and daily Elasticsearch summaries with UTC calendar-day selection. A request that cannot be represented by a source is blocked or receives an explicitly expanded proposal requiring new approval. Erasure never silently rounds outward. A source without a time dimension reports a whole-account operation, which requires explicit whole-account approval.

Inventory carries `observedAt`, coverage bounds, completeness, and a monotonic revision within a registered stream. Old, duplicate, missing, and out-of-order publications must be distinguishable. Empty data is an explicit complete observation, not the absence of a message. Retention updates can change summaries without any Erasure execution.

## Retention and execution rules

Capabilities declare each data category's retention window, time semantics, cleanup methods, legal/policy hold support, and limits. These declarations describe what the adapter knows; they are not proof of erasure. Retained subsets and backup/archive exclusions appear in proposals and closure.

A proposal either freezes the selected record set or binds a reproducible selection with a source revision/precondition. This contract belongs to the source. Before destructive work, the adapter validates the approved plan and relevant preconditions atomically with the cleanup where feasible. If the current selection or impact differs, it stops and proposes a new revision. Unsupported atomicity is a disclosed limitation with safe checkpoint behavior, not an implicit guarantee.

An approval authorizes automatic dispatch of that exact operation. Operators may withdraw a queued operation before dispatch; cancellation after dispatch is best effort and never means rollback. There is no global transaction across sources. Overlapping operations for one tenant/source serialize, then re-evaluate scope before the next one runs.

Closure has an outcome of `COMPLETED`, `CLOSED_WITH_EXCEPTIONS`, or `CANCELLED`. An adapter-reported success can support `COMPLETED`; it cannot support a claim of independently verified deletion. An unknown result can only be closed with an explicitly acknowledged exception. Unregistered sources remain outside coverage. Backups and downstream copies are covered only if registered and supported.

## First-release boundaries

Include three synthetic sources, two visible tenants plus generated tenants for load tests, employee login, source-owner review, adapter credentials, summaries, proposals, execution, failure recovery, closure, audit exports, container deployment, and scale evidence. Use separate PostgreSQL fulfillment and support databases plus Elasticsearch delivery events. Fulfillment ownership follows effective-dated depot assignments and child relationships; support ownership is direct. Search selection freezes document and index identity, with conditional deletion and explicit uncertainty after lost responses. The [demo plan](demo-plan.md) fixes fixture/setup, source ownership, safe reset, guided public access, and hosting feasibility.

Defer real customer data, public customer portals, discovery of unknown sources, legal eligibility automation, independently verified deletion, universal data-source plugins, billing, and deployment of a large production cluster. The demonstration models transformations; it does not assert that removing a few fields establishes legal anonymization.
