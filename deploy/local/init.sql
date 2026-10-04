-- Synthetic local credentials. Never use this bootstrap on a shared deployment.
CREATE ROLE erasure_migrator LOGIN PASSWORD 'local-migrator-only' NOSUPERUSER NOBYPASSRLS;
CREATE ROLE erasure_runtime LOGIN PASSWORD 'local-runtime-only' NOSUPERUSER NOBYPASSRLS;
CREATE DATABASE erasure OWNER erasure_migrator;
REVOKE ALL ON DATABASE erasure FROM PUBLIC;
GRANT CONNECT ON DATABASE erasure TO erasure_runtime;
CREATE ROLE keycloak LOGIN PASSWORD 'local-keycloak-only' NOSUPERUSER NOBYPASSRLS;
CREATE DATABASE keycloak OWNER keycloak;
REVOKE ALL ON DATABASE keycloak FROM PUBLIC;
