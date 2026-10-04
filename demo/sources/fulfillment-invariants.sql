CREATE EXTENSION IF NOT EXISTS btree_gist;
ALTER TABLE depot_assignment ADD CONSTRAINT nonoverlapping_ownership
  EXCLUDE USING gist (depot_id WITH =, tstzrange(valid_from, valid_to, '[)') WITH &&);
CREATE INDEX shipment_dispatch ON shipment (dispatched_at, depot_id);
CREATE INDEX parcel_shipment ON parcel (shipment_id);
CREATE INDEX scan_parcel ON scan (parcel_id);
