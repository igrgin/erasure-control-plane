CREATE TABLE demo_generation (
  singleton boolean PRIMARY KEY DEFAULT true CHECK (singleton),
  generation text NOT NULL,
  reference_time timestamptz NOT NULL,
  blueprint_version text NOT NULL
);
-- These are reserved for the future adapter, never presented as product receipts.
CREATE TABLE demo_operation_ledger (
  generation text NOT NULL, operation_key text NOT NULL, receipt jsonb NOT NULL,
  PRIMARY KEY (generation, operation_key)
);
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
