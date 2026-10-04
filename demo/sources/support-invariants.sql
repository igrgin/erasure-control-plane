CREATE INDEX ticket_account_time ON ticket (realm, account_id, opened_at);
CREATE INDEX message_ticket ON ticket_message (ticket_id);
