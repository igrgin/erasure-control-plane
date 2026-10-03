# Erasure

Erasure coordinates owner-approved cleanup of business-account data held in registered sources. Its records describe the known scope and reported outcomes of that coordination.

## Language

**Operating company**:
The company that operates Erasure and the data sources connected to it.
_Avoid_: Tenant, customer

**Tenant**:
A customer business account whose data is isolated from other customer accounts and can be the target of cleanup.
_Avoid_: Operating company, person

**Business account reference**:
The operating company's stable identifier for a tenant. A source may also use its own local identifier for the same account.
_Avoid_: Person identifier, email identity

**Source**:
A registered database or other data store with an accountable owner and declared cleanup capabilities.

**Adapter**:
The component that understands a source's business-account relationships, summarizes its data, proposes cleanup, and executes approved operations.

**Source owner**:
The accountable employee or group authorized to decide whether a proposed operation for a source may run.

**Inventory summary**:
A source's dated report of the amount and categories of data it holds for a business account. Its freshness and completeness are part of the report.

**Request**:
A case asking for cleanup of one business account within an explicit time range and a recorded source scope.

**Proposal**:
A versioned description of the exact cleanup an adapter offers for one request and source, including estimated impact and exclusions.

**Approval**:
A source owner's authorization of one exact proposal version and its disclosed impact.

**Blocker**:
A recorded condition that prevents a source from proposing or completing cleanup, with a reason and an accountable next actor.

**Execution receipt**:
An adapter's report of an operation's outcome, including the outcome's certainty and any partial effects.

**Disposition**:
The recorded outcome for one source in a request, including completed cleanup, no matching data, retained data, rejection, unresolved failure, or unknown outcome.

**Closure**:
The decision to stop further work on a request with an explicit disposition for every source in its recorded scope. Closure can include exceptions.
