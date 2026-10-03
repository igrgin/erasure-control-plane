-- Logical contract v1. Source database is separate from fulfillment/control plane.
CREATE TABLE account (
  realm text NOT NULL, account_id bigint NOT NULL,
  PRIMARY KEY (realm, account_id)
);
CREATE TABLE ticket (
  ticket_id text PRIMARY KEY, realm text NOT NULL, account_id bigint NOT NULL,
  opened_at timestamptz NOT NULL, revision bigint NOT NULL,
  FOREIGN KEY (realm, account_id) REFERENCES account
);
CREATE TABLE ticket_message (
  message_id text PRIMARY KEY, ticket_id text NOT NULL REFERENCES ticket,
  written_at timestamptz NOT NULL, body text NOT NULL
);
CREATE TABLE notification_preference (
  realm text NOT NULL, account_id bigint NOT NULL,
  channel text NOT NULL, enabled boolean NOT NULL, revision bigint NOT NULL,
  PRIMARY KEY (realm, account_id, channel),
  FOREIGN KEY (realm, account_id) REFERENCES account
);
