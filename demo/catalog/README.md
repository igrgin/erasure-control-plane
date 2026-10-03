# DispatchWorks source blueprint v1

Candidate for owner acceptance under issue #48. No fixture environment or adapter is implemented by this blueprint. The project owner also acts as the synthetic source owner when accepting this revision. The required engines are PostgreSQL and Elasticsearch. Three separately registered sources use two PostgreSQL databases and one Elasticsearch index family. MongoDB and Redis are removed from the release scope.

DispatchWorks is the operating company. It manages deliveries and support for Northstar Supply (`biz-northstar`) and Harbor Analytics (`biz-harbor`). A depot changes customer assignment during the demonstration week. Its old shipments still belong to the customer that used it at dispatch time. Support tickets belong directly to an account. Delivery events are searchable copies with explicit account attribution at ingest time.

## Versions, clock and mappings

Blueprint, schema, mapping and scenario version: `dispatchworks-v1`. Default reference instant `R = 2026-10-04T00:00:00Z`; all relative days mean 24 hours in UTC. ERA-038 accepts a supplied UTC-midnight reference instant and generates all times relative to it. Every inventory, proposal, fixture expectation and scenario result records version, R, run generation, mapping version and policy version. Resets create a new generation. Engine versions and digests are pinned in ERA-038 after compatibility checks.

| Source ID | Store and owner | Northstar mapping | Harbor mapping | Time and retention |
| --- | --- | --- | --- | --- |
| fulfillment | Separate PostgreSQL `demo_fulfillment`; fulfillment owner | `(realm=north, account=7)` | `(realm=harbor, account=7)` | Shipment `dispatched_at`; hourly inventory, exact seconds; 90 days |
| support | Separate PostgreSQL `demo_support`; support owner | `(realm=north, account=7)` | `(realm=harbor, account=7)` | Ticket `opened_at`; hourly inventory, exact seconds; 60 days |
| delivery-search | Elasticsearch `demo-<generation>-delivery-v1-*`; search owner | `(realm=north, account_key=7)` | `(realm=harbor, account_key=7)` | `event_day`; daily UTC inventory and whole-day selection; 30 days |

The overlapping `7` is intentional. Bare local account IDs never authorize reads or deletion. Resolve the complete source-local mapping and its version. An operator granted Northstar cannot read Harbor even when the same employee owns a source. Use separate operator, each source-owner, auditor and fixture-admin grants. An adapter principal is bound to exactly one source and explicitly granted accounts. Source credentials stay with that adapter. The control-plane PostgreSQL database has different credentials from both source databases.

## Fulfillment: ownership through dated relationships

`fulfillment.sql` defines the logical schema for ERA-038. Account -> depot assignment -> shipment -> parcel -> scan is the ownership path. Shipments, parcels and scans have no business account column. A depot can change account assignment. Resolve the assignment whose half-open validity contains the shipment's `dispatched_at`, then apply the request interval to that same timestamp. Scan timestamps describe processing, not ownership or request eligibility. A scan logged later than the requested interval is still a dependent of its selected shipment.

The adapter rejects gaps and overlaps in ownership history for candidate shipments. It does not choose the newest assignment or silently skip an ambiguous shipment. ERA-038 enforces nonoverlapping assignment ranges and ERA-010 validates source consistency during proposal and execution. Within a transaction, freeze shipment IDs, lock/version the relevant assignment and hold records, lock selected parents, delete scans then parcels then eligible shipments, and commit the operation receipt. Concurrent writers must take the same parent locks for child changes; ERA-010 must prove this against the real store. Any changed selection, ownership mapping or hold state requires a new proposal. Never delete a depot or assignment because one shipment matches.

A shipment under an invoice hold keeps its whole dependency tree, including beyond the ordinary 90-day horizon. Retention purges also respect holds; coverage and retained exceptions are reported separately. The invoice reference and ownership history remain as disclosed exclusions. Timeless account/depot metadata is outside date-based cleanup; a separate whole-account proposal may remove metadata only when no remaining shipment, assignment or invoice depends on it. No cascading deletion of shared depots is offered.

Illustrative source-side selector, never SQL accepted from the UI:

```sql
SELECT s.shipment_id
FROM account a
JOIN depot_assignment da
  ON (da.realm, da.account_id) = (a.realm, a.account_id)
JOIN shipment s ON s.depot_id = da.depot_id
 AND s.dispatched_at >= da.valid_from
 AND (da.valid_to IS NULL OR s.dispatched_at < da.valid_to)
WHERE a.realm = :realm AND a.account_id = :account_id
 AND s.dispatched_at >= :from_utc AND s.dispatched_at < :to_utc
 AND NOT EXISTS (SELECT 1 FROM invoice_hold h WHERE h.shipment_id = s.shipment_id);
```

## Support: direct ownership and a small dependency

Select tickets by the full `(realm, account_id)` mapping and `opened_at` interval. Delete ticket messages then tickets transactionally with the receipt. Messages inherit the ticket's account and date even when written later. Account notification preferences are timeless and require a separately approved whole-account action. A date request never deletes preferences.

## Delivery search: coarse dates and concurrent changes

`delivery-search.json` fixes field types. Each document has one account owner, `realm`, `account_key`, immutable ingest attribution version, `event_day` at UTC midnight, `shipment_reference`, payload and run generation. The reference is informational; cleanup does not join to a PostgreSQL database whose shipment may already have been deleted. The ingest process must resolve ownership before indexing and quarantine unknown or ambiguous ownership. Shared multi-account documents are outside v1.

Use exact keyword filters on the complete mapping plus `[from,to)` over `event_day`. Reject boundaries outside UTC midnight or offer a separately disclosed expanded proposal with a fresh owner decision. Freeze concrete index UUID/name, document ID, routing if used, sequence number and primary term in a durable PostgreSQL adapter ledger outside the search index. This ledger is source execution state, not a fourth business-data source.

Execute bounded per-document conditional deletes with `if_seq_no` and `if_primary_term`. A changed document produces a conflict and survives the old approval. Reindexing into a replacement index changes its identity and blocks the old plan even if document IDs repeat. A new matching document after approval is outside the frozen set. A same-index recreated document has a different sequence identity and survives. The search adapter must validate index identity under coordinated index administration before each batch; reset/reindex administration quiesces it.

Elasticsearch supports these conditional deletes. Bulk operations require per-item results; successful items are not rolled back when another item fails. [Delete API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-delete), [bulk API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk). A newly run delete-by-query takes a new snapshot rather than preserving the approved set, and failures do not undo successful deletes. It is not the v1 execution method. [Delete-by-query API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-delete-by-query).

Persist a write-ahead attempt before sending each bounded batch, then checkpoint acknowledged per-item results. A lost HTTP response before checkpointing leaves those effects unknown. Status/absence cannot prove this adapter deleted an item. Stop automatic recovery for those items, preserve any acknowledged counts, and require source-owner reconciliation or closure with an explicit unknown exception. Duplicate completed commands return the durable receipt; never restart a query with a new operation key. This is intentionally weaker than the PostgreSQL cleanup/receipt transaction.

Retention is a synthetic scheduled document purge by `event_day < R-30d`, not a Redis TTL and not a claim that deleting a daily index is account-specific. A run freezes its clock; retention advancement is a separate scenario mutation. Expired coverage is disclosed, not reported as Erasure-deleted. Refresh lag is part of inventory freshness. ERA-038 refreshes before deterministic assertions; runtime summaries record their observed time and completeness.

## Fixture inventory and exact selection oracle

Each scenario starts from an independent fresh generation unless it explicitly specifies mutations. Main request `W = [R-7d, R-5d)` for Northstar. Depot `D-transfer` belongs to Northstar until `R-6d` and Harbor from that instant. Depot `D-north` stays with Northstar, and `D-harbor` with Harbor. Ownership assignment starts at `R-100d`. IDs below are generation-scoped.

| Shipment | Depot | Dispatched at | Owner | Hold | Expected in W |
| --- | --- | --- | --- | --- | --- |
| F-before | D-north | R-7d-1s | Northstar | no | excluded |
| F-start | D-transfer | R-7d | Northstar | no | delete |
| F-late | D-transfer | R-6d-1s | Northstar | no | delete |
| F-switch | D-transfer | R-6d | Harbor | no | preserve |
| F-held | D-north | R-6d+1h | Northstar | yes | retain |
| F-end | D-north | R-5d | Northstar | no | excluded |
| F-other | D-harbor | R-7d+1h | Harbor | no | preserve |

Every shipment has two parcels and each parcel has two scans. One scan per parcel arrives three days after dispatch. Expected fulfillment Northstar W inventory: 3 shipments, 6 parcels, 12 scans associated by dispatch date, with one held shipment. Approved deletion: 2 shipments, 4 parcels, 8 scans; retained: 1 shipment, 2 parcels, 4 scans plus 1 invoice hold. Report each category separately, never add shipment and scan counts as interchangeable units. Harbor W inventory is 2 shipments, 4 parcels, 8 scans and must remain unchanged.

Support tickets `S-start` at R-7d and `S-mid` at R-6d belong to Northstar. `S-end` at R-5d is excluded, and `S-other` at R-6d belongs to Harbor. Each has two messages, one after W. Delete 2 tickets and 4 messages. Preserve Northstar and Harbor notification preferences.

Search documents `E-start` at day R-7d and `E-mid` at R-6d belong to Northstar. `E-end` at R-5d is excluded; `E-other` at R-6d belongs to Harbor; `E-old` at R-31d has already been purged at baseline and lies outside complete coverage. Additional Northstar documents `E-horizon` at R-30d and `E-after-horizon` at R-29d are present initially and support the retention advancement scenario. Delete 2 documents for W. There is no invoice hold on these independent delivery-event copies, which is disclosed in the proposal.

Include pre-purge fixture manifests at F R-91d and S R-61d, absent at baseline. All sources report complete coverage from their respective horizon through R, an explicit zero bucket at R-2d, and unknown coverage before the horizon. Publish fulfillment/support hourly counts and search daily counts. Assign fulfillment descendants to the parent's dispatch bucket and support messages to the ticket's open bucket. ERA-038 derives byte estimates from actual serialized fixtures; this blueprint specifies count units only.

## Acceptance and downstream work

The owner must accept the exact commit containing this catalog, both SQL schemas, search mapping and scenario revision before #49 or #12 consumes it. Acceptance is pending; the instruction to invent a demo does not assert approval of the resulting design. Retain the review against that commit. ERA-001 can use a minimal support fixture. ERA-038 builds both PostgreSQL databases and the search index, seeds the oracle and supplies safe reset. ERA-011 builds the search adapter; ERA-039 builds fulfillment ownership/hold behavior on the initial PostgreSQL adapter. ERA-040 proves the combined tour.
