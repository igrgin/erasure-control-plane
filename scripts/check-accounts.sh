#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose -f deploy/local/compose.yaml up -d --build --wait --wait-timeout 180
python3 -m unittest discover -s tests -p 'test_account_*.py' -v
npm --prefix frontend ci --no-audit --no-fund
npm --prefix frontend run build
cd frontend
npx playwright install chromium
npm run test:browser
