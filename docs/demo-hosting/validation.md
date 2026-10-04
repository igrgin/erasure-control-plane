# Full-stack launch validation

Status: proposed acceptance protocol for REQ-13/REQ-15, not executed by #52. Execution owners are the setup/deployment/guided-demo issues, with final acceptance in #53. Use the accepted `dispatchworks-v1` fixtures and [scenario blueprint](../../demo/scenarios/README.md). Never substitute a static page, toy database or one idle process for the complete stack.

## Record the candidate and measurements

Retain a timestamped evidence bundle outside reset stores. Record Git SHA, image digests, engine versions, Compose/platform configuration, region/SKU, CPU class, RAM/disk limits, JVM heaps, fixture generation/reference instant and all commands with exit status and outputs. Include provider billing preview, tax/domain renewal quote, approved ceiling/currency and uptime mode.

On the real target, collect per-container memory/CPU/restarts and host available RAM, CPU pressure, disk free space, I/O, swap activity and network traffic. Suggested observations include `docker stats --no-stream`, `docker inspect`, `free -h`, `df -h` and platform metrics. Sample continuously during each phase; a single idle snapshot is insufficient. Name the tool/version and duration so the run can be repeated. Redact secrets from retained output.

Run these phases with all services present:

1. Cold start from a clean target, migrations, source seed, login, adapter registration and complete inventory. Record time to readiness and peak resource usage.
2. At least 30 minutes idle, then the full healthy/held/isolation/stale-approval/partial-unknown walkthrough for both business accounts. Record API latency, throughput, queue lag, inventory freshness, receipt outcomes and memory peaks. Use one owner-controlled live session plus five simultaneous read-only tour browsers as the initial proposed workload. Record exact request mix; do not claim this establishes general customer capacity.
3. Reset after operations and failure injection. Confirm old approvals/commands cannot execute against the new generation, source counts match the oracle, and preserved audit evidence remains attributable.
4. Restart API, worker, adapters and stores; inject the lost-response case and reconcile via stable operation identity. No uncontrolled second cleanup is allowed. Unknown results remain explicit.
5. Perform daily application backup while the tour runs, then restore onto an isolated clean target. Start dispatch paused, reconcile restored control-plane state with source ledgers, and inspect identity/source/search consistency before resuming. Measure RPO/RTO. Test image rollback with compatible schema/protocol.
6. Test certificate renewal, identity redirects, secure session/CSRF handling, tenant/source/role isolation, external database denial and private management endpoints. Exercise resource, queue, backup and HTTPS alerts.
7. Run external-browser UAT for the public HTTPS read-only tour and a temporary owner-controlled employee session. Retain URL, timestamp, candidate and actor evidence. Revoke temporary grants afterwards.

## Proposed pass thresholds

Owner must accept these targets and the deployment evidence before launch. They are engineering gates for the small demonstration, not an SLA.

| Gate | Proposed acceptance |
| --- | --- |
| Coverage | Every required process, two PostgreSQL business sources, search, durable operation ledger and identity store present; guided scenarios pass |
| Memory | No OOM/restarts or swap pressure; at least 20% available host RAM through peak phases, with container headroom demonstrated |
| CPU | Sustained utilization below 70% during the stated tour workload; startup/reset peaks allowed only if readiness recovers and no commands/results are lost |
| Disk | At least 30% free after backup/reset scratch, with per-store growth/retention forecast |
| UX/readiness | Proposed API p95 below 2 seconds and complete cold readiness within 5 minutes; disclose maintenance/reset outage duration |
| Recovery | Restore/rollback and durable unknown-outcome reconciliation pass; measured RPO <=24 hours and RTO <=4 hours |
| Cost | Actual topology, retained resources, anticipated traffic, renewal, tax and currency fees fit the owner-approved ceiling |
| Public experience | Real HTTPS URL plus external tour/controlled-live UAT, no visitor mutation/reset or raw-store access |

If 8 GiB fails, repeat the exact workload on 16 GiB or change limits/topology with fresh evidence and quote. If 16 GiB fails or costs exceed the ceiling, stop launch, record the failure/next owner in #53, and offer the static/recorded fallback. A new provider or engine version requires refreshed bootstrap, persistence and recovery evidence. No measurement has been supplied yet; every execution gate is pending.

## Owner record to complete

Retain the owner's decision against the PR/candidate SHA in GitHub or the delivery conversation, then link it here in the launch work. Required fields are provider/SKU/region, monthly ceiling/currency/tax treatment, domain renewal, uptime mode, maintenance/billing/incident owner, approved validation targets, measured evidence bundle, purchase authorization and accepted fallback scope. Empty fields remain pending. This file grants none of those decisions by itself.
