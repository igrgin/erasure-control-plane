# DispatchWorks source environment

Issue #49 implements the accepted `dispatchworks-v1` blueprint from commit `1afccbce2f932973c06f1efd5ff45482e90a3a01`. This environment runs independently of Erasure. Every record is synthetic. The source smoke checks execute fixture-admin operations; they do not create approvals or claim adapter-reported product outcomes.

## Run

Use Python 3.10 or later, Docker Engine/Desktop with Compose v2, and a Linux container runtime. From the repository root:

```sh
python3 demo/seed/demo.py start
python3 demo/seed/demo.py seed --reference 2026-10-04T00:00:00Z
python3 demo/seed/demo.py inspect
python3 demo/seed/demo.py advance --days 1
python3 demo/seed/demo.py reset --reference 2026-10-04T00:00:00Z
python3 -m unittest discover -s demo/seed -p 'test_*.py'
python3 demo/seed/demo.py smoke
python3 demo/seed/demo.py resources
```

`start` creates independent random credentials in `.local/` and waits for all three health checks. It preserves existing stores. `seed` initializes an unseeded environment; repeat population uses `reset` to retire the previous generation. The reference must be an explicit UTC midnight. Seed version `1` is fixed by `dispatchworks-v1`. Resetting with the same reference reproduces the same business records; generation and Elasticsearch index UUID intentionally change.

`inspect` returns actual source rows and documents, plus generation metadata. `advance` runs synthetic retention, respecting invoice-held trees, and reports revised coverage separately from Erasure execution. The baseline expectations remain in `.local/expected.json`; they are not relabeled as a current publication after a mutation. `smoke` is destructive within these demo stores, runs the scenarios below, and leaves a fresh baseline. Its result is `.local/smoke-result.json`.

The Compose `sources` profile runs two independent PostgreSQL 17.6 servers and Elasticsearch 9.1.5. Both images have pinned multi-platform manifest digests. These are a tested compatibility baseline, not a claim about the latest releases. Image upgrades require rerunning this smoke. The PostgreSQL [official image](https://hub.docker.com/_/postgres) supports password files; the Elasticsearch [Docker guide](https://www.elastic.co/docs/deploy-manage/deploy/self-managed/install-elasticsearch-docker-basic) describes the single-node setup.

All services use an internal Docker network and publish no host ports. The demo tool reaches only the fixed Compose project `erasure-demo-sources`, services `fulfillment`, `support`, `search`, databases `demo_fulfillment`, `demo_support`, and exact generated search index names. It accepts no database URL, project override or index deletion wildcard. Use one checkout/environment per Docker daemon. Administrative Docker access itself remains privileged.

PostgreSQL has a separate fixture administrator and non-superuser `demo_adapter` role in each server, with distinct passwords. Each source adapter is allowed both synthetic accounts and must resolve the full mapping. These are source credentials, not browser or control-plane grants. Search uses its independent fixture-admin password. Future adapters must provision their own narrowly scoped search identity. Passwords are ignored, stored under a private local directory, and never included in fixture manifests or results. The four files mounted as Compose secrets are readable inside their assigned containers; the host directory remains mode `0700`. This supports the Elasticsearch container UID on native Linux without exposing the host directory. Keep `.local/` with these volumes; do not copy only the generation file to another environment or delete it while stores/workers exist.

## Attached workers and reset

An attached local application must import `demo/seed/gate.py`, mount the same `.local/` directory if containerized, and use the same advisory-lock-capable filesystem. Before accepting commands, read the active generation. Store that generation on every proposal, approval, command, operation key and ledger entry. A worker must hold this lease throughout precondition checks, every source effect, child process completion, and receipt persistence:

```python
with Gate(shared_directory).lease(command.run_generation):
    execute_and_persist_receipt(command)
```

Reset closes worker admission, then takes the exclusive worker lock with a 30-second timeout. Active workers finish first; new workers wait. It persists a new `resetting` generation before modifying any source, which invalidates every old-generation approval and command. It recreates both schemas and empty source-local operation ledgers, deletes only recorded previous index names, seeds a fresh index, and publishes `active` only after all writes finish. Workers with old commands fail on acquiring a lease. A failed restore keeps the gate closed; rerun `reset` after fixing the store. Timeout while waiting for workers makes no source changes. Never manually mark a failed reset active.

External application ledgers must use the same generation fence and initialize a fresh namespace on generation change. They may retain old records as retired audit history. The source tool does not truncate application databases. Preserve exports and recordings outside the source stores; reset preserves local saved evidence too. All writers must cooperate with this lease. Unregistered processes using raw administrator credentials cannot be quiesced by this protocol. A distributed deployment needs its deployment coordinator and durable fencing contract before attaching remote workers.

The smoke runs a separate attached worker process that holds a lease and writes an operation entry, starts reset concurrently, proves reset waits, then verifies the restored ledger and rejects a queued old-generation command. This is an executable application integration contract harness. The actual control plane and adapters do not exist at this candidate; their combined integration remains #51 and its prerequisites.

## Fixtures and assertions

The generator uses the accepted catalog schemas and adds PostgreSQL ownership-range exclusion constraints. It includes both account realms with local ID `7`, exact boundaries around the depot transfer, late descendant timestamps, held shipment trees, timeless preferences, retention-horizon search documents, and pre-purge manifests. `F-old-held` extends the blueprint's hold policy with a tree at R minus 91 days; it is reported as a retained exception outside ordinary coverage.

[Expected output](../../demo/expected/dispatchworks-v1.json) uses symbolic generation `oracle`. Runtime expectations substitute a fresh generation. Inventory buckets inherit parent time and keep categories separate. The byte measure is canonical UTF-8 JSON length, not engine disk usage. Complete zero buckets, unknown pre-horizon coverage, and stale/unavailable publication examples are distinct. The fixture kit does not implement an inventory publisher.

The real-store smoke verifies exact fixture equality after repeated seeding, half-open selection, effective-dated ownership, both account mappings, overlap rejection, credential separation, nonprivileged roles, protected generation metadata, child-first cleanup with held trees, and preservation of all unselected records. Search checks freeze sequence numbers/primary terms, reject both changed and recreated documents, advance retention, and verify index UUID replacement on reset. SQL fixture cleanup has no product approval or retry protocol; those belong to the adapters.

## Measured source envelope

On 2026-10-04, a fresh source-volume boot on Docker Desktop 29.6.2, Linux ARM64 with about 7.65 GiB assigned to the VM, reached healthy status in 13.32 seconds after image download. The smoke passed against the pinned images. A post-smoke sample measured:

| Resource | Fulfillment | Support | Search |
| --- | ---: | ---: | ---: |
| Container memory | 38.36 MiB | 39.21 MiB | 905.7 MiB |
| Configured memory cap | 256 MiB | 256 MiB | 1536 MiB |
| Data directory allocation | 48,948 KiB | 47,396 KiB | 588 KiB |
| Database/index logical size | 9,735,315 bytes | 8,146,067 bytes | 8,867 bytes |

The PostgreSQL image is 269,913,120 bytes and Elasticsearch is 976,252,028 bytes on this platform. Both PostgreSQL services share the image layers. Allow at least 3 GiB free Docker VM memory and 4 GiB free disk for these small sources, image extraction, and test churn. The configured container caps total 2 GiB; the suggested headroom covers runtime overhead. Elasticsearch uses a 512 MiB heap and disables mmap for this small fixture, avoiding host `vm.max_map_count` changes.

These are source-only smoke measurements, not production sizing or a clean-machine certification across platforms. CI also boots fresh volumes on Linux. Application, identity provider, adapters, logs, backups, and load tiers must be measured later for the completed application envelope and hosting decision.
