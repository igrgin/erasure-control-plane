# Demo hosting assessment

Research date: 2026-10-04. Issue [#52](https://github.com/igrgin/erasure-control-plane/issues/52), requirements REQ-13 and REQ-15. Status: research candidate for owner review. No provider, budget, purchase or deployment has been approved. Prices below are public USD list prices checked on that date, before tax. Refresh the quote at purchase and again before #53 launch.

## Conditional recommendation and decision

Use a single paid Linux VM in Frankfurt for the first live demonstration, if the owner accepts the complete recurring bill and the [full-stack validation](validation.md) passes. Evaluate 8 GiB first; use 16 GiB if the measured peaks require it. Keep large scale benchmarks off the visitor host. A single host has a shared failure boundary and planned maintenance downtime.

Under the assumptions below, reserve about $65/month before tax for 8 GiB, or $122/month before tax for 16 GiB. These are rounded planning allowances, not approved budgets or guaranteed bills. A managed alternative starts around $322/month before traffic and tax with the explicit topology below. Its platform handles more infrastructure work, but Elasticsearch, identity and application recovery still need an owner.

| Owner decision | Recorded state on 2026-10-04 |
| --- | --- |
| Provider and region | Pending. DigitalOcean Basic in Frankfurt is the conditional reference; Render Frankfurt is the managed comparator. Verify SKU availability before purchase. |
| Budget, currency and tax-inclusive ceiling | Pending owner response. No ceiling supplied in the issue or session. |
| Uptime | Proposed always-on read-only tour and scheduled owner-controlled live sessions, with declared maintenance windows. Not accepted yet. |
| Domain and renewal | Pending. Use an existing subdomain if available; otherwise obtain a real renewal quote. |
| Operations and billing owner | Project owner proposed, acceptance pending. |
| Purchase/deployment authority | None granted by #52. Separate explicit owner authorization required. |
| Exact candidate acceptance | Pending review of the PR commit. |

If the ceiling is below the validated full-stack bill, or no host passes the resource/recovery gates, record that as a blocker for #53. Offer local reproduction plus a static architecture tour and recording. Static visibility does not meet REQ-15's public HTTPS tour plus controlled live session. The owner must explicitly revise the scope to accept a static-only deliverable. This assessment does not close that decision by assuming a budget.

## Options and recurring cost

The three options show the same synthetic story with different operating capabilities. The paid comparisons include all runtime processes from the [architecture](../architecture.md) and [deployment plan](../deployment.md). Managed here means a managed application platform and managed PostgreSQL, with self-operated Elasticsearch and Keycloak. It is not a fully managed search/identity offering.

| Item per month | One VM, 8 GiB | One VM, 16 GiB | Render multi-service | Static/recorded only |
| --- | ---: | ---: | ---: | ---: |
| Compute | $48 | $96 | $292 | $0 static site |
| Workspace | $0 | $0 | $0 Hobby | $0 Hobby |
| Persistent storage | Included 160 GiB SSD | Included 320 GiB SSD | $18 PostgreSQL + $5 search disk | No database |
| Provider backups | $9.60 weekly | $19.20 weekly | Paid PostgreSQL recovery included; search/application backups below | Local versioned assets |
| Off-host application backups or recording storage | $5 Spaces | $5 Spaces | $5 Spaces | $5 Spaces for recording |
| Domain renewal allowance | $1.67 | $1.67 | $1.67 | $1.67 |
| TLS, local monitoring, public IPv4 | $0 incremental | $0 incremental | TLS/metrics included | TLS included |
| Traffic in base example | $0 within allowance | $0 within allowance | $0 at <=5 GB outbound | $0 at <=5 GB site outbound and <=1 TiB recording outbound |
| Total before tax/overages | **$64.27** | **$121.87** | **$321.67** | **$6.67** |
| Tax | Unquoted; add actual checkout/invoice tax | Unquoted | Unquoted | Unquoted |

The $20/year domain allowance is an estimate, not a registrar quote. Domain choice is unknown; an existing subdomain or provider URL reduces it to zero. Registration and renewal can differ. Paid monitoring, registry subscriptions, CI overages, payment/foreign-exchange fees and operator time are not included in these subtotals. Reserve them separately if selected. Build immutable images in CI, not on the demonstration host. With an external free recording host and provider URL, static hosting could have zero incremental cost, subject to its terms and quotas.

Official price observations, checked 2026-10-04:

- [DigitalOcean Basic pricing](https://www.digitalocean.com/pricing/droplets): Regular 4 vCPU/8 GiB/160 GiB with 5,000 GiB transfer is $48/month; 8 vCPU/16 GiB/320 GiB with 6,000 GiB is $96/month. Weekly backups add 20%; daily backups would add 30%, increasing totals by $4.80/$9.60. These are shared CPU plans.
- [Spaces pricing](https://www.digitalocean.com/pricing/spaces-object-storage): $5/month includes 250 GiB storage and 1 TiB outbound. Excess storage is $0.02/GiB and outbound $0.01/GiB. Use private backups and separately public synthetic recording assets.
- [Render pricing](https://render.com/pricing): Standard services are $25/month for 1 CPU/2 GB RAM; Pro is $85/month for 2 CPU/4 GB. Basic-1gb PostgreSQL is $19/month for 0.5 CPU/1 GB. Disks are $0.25/GB/month; PostgreSQL storage is $0.30/GB. Hobby workspace is $0/month plus compute, with 5 GB outbound then $0.15/GB. Static site deployment and TLS are included. Current plans differ from historical pricing.

Managed compute calculation: six Standard services for API, worker, Keycloak and three adapters, $150; one Pro private Elasticsearch service, $85; three Basic-1gb PostgreSQL instances, $57. Total $292. Allocate 20 GB on each database and 20 GB search disk, conservatively budgeting all 60 GB database storage at $0.30/GB. Confirm any included storage credit at checkout. This buys 9.5 allocated CPUs and 19 GB RAM across isolated instances; unused memory cannot be shared between services. Smaller adapter plans are a later measured optimization.

Use three PostgreSQL instances for platform state, fulfillment and support. Platform state contains distinct databases/users for control plane, Keycloak and the durable search operation ledger. Render supports [multiple databases per instance](https://render.com/docs/postgresql-creating-connecting). Verify non-owner runtime roles, RLS and migration permissions; a provider's default privileged credential must not become an application credential. A [private Elasticsearch service with a persistent disk](https://render.com/docs/deploy-elasticsearch) is supported, but its pinned version must pass current bootstrap checks. Do not copy an old example image into deployment.

Traffic sensitivity: assume 1,000 tour visits/month at 5 MB delivered per visit, about 5 GB, and 100 recording views at 100 MB, about 10 GB from Spaces. These are estimates, not observed visitors. If Render site/API outbound reaches 100 GB, add 95 x $0.15 = $14.25/month on Hobby. Video streamed from Spaces uses its separate allowance. DigitalOcean [bandwidth billing](https://docs.digitalocean.com/platform/billing/bandwidth/) charges excess outbound at $0.01/GiB; short-lived Droplets accrue a prorated allowance. Alerts do not cap spending. Set operator alerts below the approved ceiling and restrict large downloads if needed.

Tax remains a quote blocker until the billing identity and invoice jurisdiction are known. Compute the approved total as subtotal + traffic/storage/build overages + actual taxes + currency/payment fees. For sensitivity only, a hypothetical 25% tax on the entire subtotal gives $80.34, $152.34, $402.09 and $8.34. This is arithmetic, not an assertion about the owner's tax treatment.

## Resource hypothesis

No backend, adapter images, Compose stack or measured capacity exists in this checkout at the baseline for #52. The SQL schemas and search mapping define fixtures, not process memory. All figures below are proposed resident-memory allowances, including JVM native memory where relevant. They are distinct from heap limits and from measured application capacity.

| Runtime | Estimated RAM GiB | CPU planning allowance | Persistent state |
| --- | ---: | --- | --- |
| Proxy serving built React assets | 0.10-0.20 | 0.1 CPU | Configuration, certificates |
| API | 0.60-1.00 | 0.5-1 CPU | Control-plane database |
| Worker, separate backend process | 0.40-0.75 | 0.25-0.5 CPU | Durable jobs/commands |
| Keycloak | 0.50-0.90 | 0.25-0.5 CPU | Identity database |
| Three adapters together | 1.05-2.10 | 0.75-1.5 CPU total | Source receipts and search ledger |
| PostgreSQL platform/source processes | 0.60-1.20 | 0.5-1 CPU total | Distinct databases, roles and WAL |
| Elasticsearch single node | 1.50-2.50 | 0.5-1 CPU | Search index data |
| OS, Docker, metrics, residual cache | 0.70-1.00 | 0.1-0.25 CPU | Rotated logs |
| Total | **5.45-9.65** | **2.95-5.85 CPU equivalent** | See disk budget |

CPU entries are workload assumptions, not guaranteed cores or concurrent limits. Startup, seeding, reset, garbage collection and backup can exceed these allowances. The upper memory estimate already exceeds 8 GiB. Treat 8 GiB as an experiment with capped services and staged startup; 16 GiB is the safer unmeasured starting envelope, not proven capacity. Do not use swap to conceal an unsafe working set.

Initial Elasticsearch heap hypothesis is 0.75-1 GiB inside a 1.5-2.5 GiB container allowance. Configure heap/container limits from the pinned version's guidance and leave room for filesystem cache. Its current [Docker production requirements](https://www.elastic.co/docs/deploy-manage/deploy/self-managed/install-elasticsearch-docker-prod) require host kernel settings, including `vm.max_map_count=1048576`; verify these on the actual platform. Inability to meet them blocks that managed topology until a tested alternative is priced.

Disk estimate for the small two-account profile: images/OS 20 GiB; all PostgreSQL data/WAL 15 GiB; search 10 GiB; rotated logs/audit exports 5 GiB; backup/reset scratch 20 GiB. Total 70 GiB, plus at least 30% free-space reserve, about 100 GiB provisioned. Included VM disks exceed that estimate. Managed disk allocations above need per-store measurement because they cannot borrow each other's free space. Generated load tiers, retention growth and additional recordings require a separate revised budget.

## Operating requirements

| Area | VM | Managed services | Static/recorded |
| --- | --- | --- | --- |
| Region | Proposed Frankfurt; confirm product availability | All services/databases Frankfurt, same private network | Global CDN; recording bucket region chosen by owner |
| Public routes | HTTPS `demo.<domain>` for tour/API, `auth.<domain>` for OIDC; HTTP only redirects/ACME | Static tour plus HTTPS API/identity service domains; validate cookies, CORS, CSRF and callback origins | HTTPS tour and synthetic recording; no identity service |
| Private routes | PostgreSQL, search, adapter/worker management and metrics stay on private container networks; SSH allowlisted | [Same-region private networking](https://render.com/docs/regions); deny external database access, search private service | No running data stores |
| Persistence | Durable named volumes for every store/ledger; credentials and certificates protected | Managed PostgreSQL plus paid search disk; no durable receipts on ephemeral local files | Versioned tour and preserved recording |
| Uptime | Always-on proposed; planned patch/reset windows | Always-on paid services; disk-backed redeploy downtime | Always-visible static tour subject to provider availability; live unavailable |
| Maintenance | Owner patches host/images, renews certificates, rotates secrets, rehearses recovery | Owner updates app/identity/search, validates provider maintenance and permissions | Owner refreshes content, links and recording |
| Monitoring | Private health/CPU/RAM/disk dashboards plus external HTTPS/login check | Provider metrics plus application/adapter/queue alerts and external check | Link/playback check and traffic/quota alerts |
| Teardown | Retain evidence, revoke credentials, remove DNS, destroy VM, backups, snapshots, volumes and buckets as applicable | Remove services, databases, disks, buckets, domains and integrations | Remove site/media/domain resources after preserving evidence |

Render [TLS certificates](https://render.com/docs/tls) are managed. [Persistent disks](https://render.com/docs/disks) attach to one service instance and prevent zero-downtime deployment. They are not a cross-service backup/ledger solution. The VM proxy must manage certificate renewal, external issuer URLs and trusted forwarding headers. Preserve separate source identities and tenant grants on either topology.

Before reset, pause dispatch, quiesce adapters and retire old commands/approvals. Restore only allowlisted synthetic source generations and consistent ledgers; preserve audit evidence outside reset stores. Unknown search effects require operation-key reconciliation, not broad retries. Back up PostgreSQL, identity and ledgers consistently and use supported [Elasticsearch snapshots](https://www.elastic.co/docs/deploy-manage/tools/snapshot-and-restore), not copies of live data directories. Weekly VM backups are extra host recovery protection, not proof of application consistency. Target daily application backups with seven daily restore points and an isolated restore drill. Proposed RPO 24 hours/RTO 4 hours remain unmeasured.

Budget owner time at roughly 2-4 hours/month for VM patching/review and 1-3 hours/month for managed maintenance, plus initial deployment and incidents. These are effort estimates. Monitor stale inventory, queue age, approvals, source heartbeat, partial/unknown outcomes, backup age and certificate expiry. Exercise the alerts before launch.

For low uptime cost, recreate and destroy a VM for scheduled sessions, preserving the tour/recording. A 16 GiB Droplet for 20 total provisioned hours would cost about $2.86 compute, plus retained storage, domain, backup and transfer charges. [Powering off a Droplet still incurs billing](https://docs.digitalocean.com/products/droplets/details/pricing/). Scheduled availability changes the public experience and requires owner acceptance; it is not an always-on live demo.

[Render free limits](https://render.com/docs/free) include idle web-service shutdown after 15 minutes, ephemeral files, no free persistent disks/private-service or worker instances, and a single free PostgreSQL database expiring after 30 days without backups. Free Key Value loses state on restart and is not in this architecture. These limits prevent an all-free durable full-stack demo. Static hosting is viable within bandwidth/build quotas, with the capability limitation recorded above.

Launch depends on the measured protocol in [validation.md](validation.md), owner decisions and #53's real public UAT. Follow-up incidents and cost drift go to GitHub issues, with the project owner responsible for pause, remediation or teardown.
