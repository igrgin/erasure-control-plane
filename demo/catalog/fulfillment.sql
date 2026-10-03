-- Logical contract v1. ERA-038 supplies migrations, roles and exclusion constraints.
CREATE TABLE account (
  realm text NOT NULL, account_id bigint NOT NULL,
  PRIMARY KEY (realm, account_id)
);
CREATE TABLE depot (depot_id text PRIMARY KEY);
CREATE TABLE depot_assignment (
  assignment_id text PRIMARY KEY,
  depot_id text NOT NULL REFERENCES depot,
  realm text NOT NULL, account_id bigint NOT NULL,
  valid_from timestamptz NOT NULL, valid_to timestamptz,
  revision bigint NOT NULL,
  FOREIGN KEY (realm, account_id) REFERENCES account,
  CHECK (valid_to IS NULL OR valid_to > valid_from)
);
-- Required migration invariant: no overlapping [valid_from,valid_to) per depot.
CREATE TABLE shipment (
  shipment_id text PRIMARY KEY, depot_id text NOT NULL REFERENCES depot,
  dispatched_at timestamptz NOT NULL, revision bigint NOT NULL
);
CREATE TABLE parcel (
  parcel_id text PRIMARY KEY, shipment_id text NOT NULL REFERENCES shipment
);
CREATE TABLE scan (
  scan_id text PRIMARY KEY, parcel_id text NOT NULL REFERENCES parcel,
  scanned_at timestamptz NOT NULL, payload text NOT NULL
);
CREATE TABLE invoice_hold (
  invoice_reference text PRIMARY KEY,
  shipment_id text NOT NULL UNIQUE REFERENCES shipment,
  reason text NOT NULL, revision bigint NOT NULL
);
-- No ON DELETE CASCADE. Explicit child-first deletion preserves held trees.
-- Mapping history and parent mutation locking form execution preconditions.
