#!/bin/bash
set -euo pipefail

# Compose file secrets retain host ownership on Linux. The private host
# directory protects the readable mount; Elasticsearch requires an owned
# 0400/0600 password file, so copy it without printing its contents.
umask 077
secret_directory=$(mktemp -d)
cat /run/secrets/search_password > "$secret_directory/password"
export ELASTIC_PASSWORD_FILE="$secret_directory/password"
exec /usr/local/bin/docker-entrypoint.sh eswrapper
