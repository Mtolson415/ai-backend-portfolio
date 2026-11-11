# Self-hosted AI workspaces: research and engineering recommendations

Research date: **November 11, 2026**. Target: an AI workspace with its own knowledge, browser, filesystem and programs, running within an enforceable container perimeter on Proxmox-hosted Linux guests.

## Findings

The recommended architecture has three persistent services—interface/controller, permission-aware knowledge retrieval and tool gateway—plus disposable workers for browsing, document conversion and programs. Infrastructure administration stays outside the agent's capabilities. A full Supabase stack is optional until an application needs its auth, storage and API services.

This survey includes **181 projects across 16 categories**. It is intentionally broad, including alternatives and emerging projects. It cannot establish a literal inventory of every container project. The [catalog](CATALOG.md) links each candidate to official source material and records deployment family, role, recommendation, release reference, licensing and an access-boundary concern. [catalog.html](catalog.html) provides offline filtering. Recommendations are editorial judgments for this workload, not benchmark rankings or security certifications.

### What was checked

For 180 projects, authenticated read-only GitHub API calls inspected repository identity, archive state, latest non-prerelease release where available, license classification, root deployment/license paths and README references. Forgejo was checked through official Docker documentation and its licensing FAQ because its owning source is on Codeberg. README blob identifiers and fetch timestamps are recorded in [catalog-evidence.json](catalog-evidence.json). Full upstream snapshots remain local; published evidence uses short source excerpts and links.

The GitHub `releases/latest` field is a repository release reference, **not a recommended package version or verified image pin**. In monorepos it can name a CLI, JavaScript package or another subcomponent. Projects without a latest release may publish tags, rolling images or external releases. GitHub SPDX classifications can be incomplete or misleading for mixed licenses; original license files take precedence. Nothing in the inventory proves that an image is available for a specific CPU or that the system runs offline.

No catalog-wide builds, vulnerability scans or deployments were performed. The public companion's synthetic reference service is independently verified; its results must not be generalized to these products.

## Important changes from the earlier discussion

1. **Flowise and MinIO are archived upstream.** They remain in the catalog as migration/reference candidates, marked against new adoption. Do not treat earlier generic recommendations as current picks. [Flowise](https://github.com/FlowiseAI/Flowise), [MinIO](https://github.com/minio/minio).
2. **OpenShell, OpenSandbox and Agent Infra AIO solve different problems.** Policy enforcement, environment lifecycle and an integrated agent computer are separate responsibilities. Do not layer all three without an integration case.
3. **A local process is not necessarily a local data path.** Search, embeddings, parsing, tracing, authentication and model fallbacks may use hosted endpoints. Inspect every route.
4. **Container packaging is not isolation strength.** Frameworks, extensions, host runtimes and service stacks appear alongside ready-to-run containers and are labeled separately.
5. **A public AI portfolio needs reproducible evidence.** Research, diagrams and a large Compose file establish design intent. A small tested tool service establishes a narrower but demonstrable engineering capability.

## Architecture shortlist

| Responsibility | Preferred evaluation | Alternatives | Reason and condition |
|---|---|---|---|
| Chat interface | Open WebUI | LibreChat, AnythingLLM | Existing tool and knowledge interfaces; inspect custom license and privacy defaults |
| Agent controller | Small typed orchestration service using Pydantic AI or LangGraph | Haystack, Deep Agents, DeerFlow, Hermes | Select one framework based on workflow and local model tool-call reliability |
| Tool gateway | Narrow custom API first; evaluate agentgateway or ToolHive | Docker MCP Gateway, ContextForge | Need identity, tool allowlists, limits and auditable enforcement; avoid duplicate gateways |
| Agent computer | Agent Infra AIO in disposable execution guest | OpenHands for coding; separate browser/files/program services | Closest to browser + files + shell concept; shared state requires a conscious boundary |
| Environment lifecycle | OpenSandbox | Dedicated fixed job launcher | Useful as number of disposable environments grows |
| Runtime policy | OpenShell evaluation | VM isolation plus OS/network controls; gVisor | Demonstrate actual denied behavior and host support |
| Knowledge core | PostgreSQL + pgvector | Qdrant; LanceDB for embedded cases | Combine ownership metadata, full-text and vector retrieval; avoid duplicated stores initially |
| Integrated knowledge platform | RAGFlow or Onyx evaluation | Dify, Khoj, Kotaemon | Choose only if the packaged UI/connectors outweigh dependency and ACL complexity |
| Document processing | Docling Serve | Tika, MarkItDown, Unstructured | Typed job boundary around untrusted parsers |
| Document archive | Paperless-ngx | Source files + retrieval API | Durable originals and operational document search |
| Web research | SearXNG + bounded crawler | Perplexica, GPT Researcher | Search discovery, extraction and evidence retention are distinct stages |
| Browser automation | Playwright service | Browser Use, Skyvern, Stagehand | Prefer deterministic steps where reliable; AI-assisted browser use adds flexibility and uncertainty |
| Graph | Explicit Obsidian links, then Neo4j/LightRAG | Graphiti, AGE, FalkorDB | Add graph extraction only for questions that improve measurably |
| Local model | Ollama or llama.cpp | vLLM, SGLang, LocalAI | Validate actual hardware and model support rather than popularity |
| Observability | Metadata audit + health checks | Langfuse/Phoenix and OpenTelemetry | Capture private payloads only when necessary and authorized |
| Management | Compose + one of Dockge/Portainer/Komodo | Trusted CLI workflow | Administrator-facing; no arbitrary agent access |

The primary sources for these choices are linked in the per-project catalog. The shortlist is a plan for comparative pilots, not a claim that the components have been integrated.

## The most relevant emerging approaches

### Agent computer: browser, files and programs in one environment

[Agent Infra AIO Sandbox](https://github.com/agent-infra/sandbox) exposes a shared environment for browser, shell, file and code operations. [OpenHands](https://github.com/OpenHands/OpenHands) focuses on coding-agent workflows. [Sandbar](https://github.com/jdrolls/sandbar) adds a visible desktop and human takeover as an emerging option. Compare API surface, session separation, authentication, lifecycle, storage and auditability.

An all-in-one environment is convenient when a browser download must become a program input immediately. The tradeoff is that shell code and browser sessions share more state. Use a separate profile per identity and a disposable execution guest. Never mount a personal browser profile, SSH agent, entire home directory or database-admin credentials into the environment.

### Sandbox lifecycle and runtime enforcement

[OpenSandbox](https://github.com/opensandbox-group/OpenSandbox) provides environment and execution management. [OpenShell](https://github.com/NVIDIA/OpenShell) applies filesystem, process and network policy; its [policy documentation](https://docs.nvidia.com/openshell/dev/how-it-works/policies/overview) describes static and dynamic controls. Ensure a missing kernel feature causes the desired fail-closed behavior. Inspect the **effective** policy, including provider-added network permissions.

[Docker Sandboxes](https://docs.docker.com/ai/sandboxes/) uses microVM isolation. Its [current installation guidance](https://docs.docker.com/ai/sandboxes/install/) includes Ubuntu/KVM prerequisites and nested virtualization for use inside another VM. It is not a universal Docker Engine feature and its release repository does not establish an open-source license for the whole product. [Kata](https://katacontainers.io/), [Firecracker](https://github.com/firecracker-microvm/firecracker) and [gVisor](https://gvisor.dev/docs/) also require deployment-specific compatibility checks.

### Progressive tool discovery

Large tool lists increase selection errors and consume context. A gateway should expose a small discovery capability, then only the tools needed for the task. Useful candidates include [agentgateway](https://github.com/agentgateway/agentgateway), [ToolHive](https://github.com/stacklok/toolhive), [Docker MCP Gateway](https://github.com/docker/mcp-gateway) and [ContextForge](https://github.com/IBM/mcp-context-forge). Do not confuse dynamic discovery with permission approval: a tool's description is untrusted metadata, and discovering a tool must not authorize it.

The [MCP security guidance](https://modelcontextprotocol.io/specification/latest/basic/security_best_practices) addresses token handling, confused deputies, SSRF and other protocol-specific risks. Use caller-bound credentials, audience validation and narrow downstream scopes. Tool schemas and read-only annotations are helpful interface metadata; application and OS enforcement are still necessary.

### Temporal memory and knowledge graphs

[Graphiti](https://github.com/getzep/graphiti), [Mem0](https://github.com/mem0ai/mem0) and [Letta](https://github.com/letta-ai/letta) explore persistent agent knowledge. Keep observations, inferences, user preferences and authoritative records distinct. Store source, valid time, ingestion time, owner, confidence and deletion lineage. A generated summary must not silently override a more recent source or become an uncited fact.

Begin with explicit links and a query set. Extracted graphs can be costly to construct, can merge unrelated entities and can preserve deleted information in summaries or edges. Test correction, deletion, revocation and date-sensitive answers before expansion.

## Knowledge sources and retrieval design

### Sources to reference on demand

| Source family | Examples | Retrieval treatment |
|---|---|---|
| Notes | Selected Obsidian folders | Markdown-aware sections, tags, aliases, backlinks and source locations |
| Project engineering | READMEs, architecture decisions, test reports | Preserve commit/date and verified-versus-proposed status |
| Documents | PDFs, manuals, correspondence, office files | OCR/parse in workers; retain page and original-object citation |
| Web evidence | Saved articles, documentation, research | Store URL, fetch date, content hash and exact capture |
| Structured records | Inventory, project status, datasets | Restricted SQL/views; preserve schema and ownership |
| Code | Selected repositories | Repository/commit/path/line references; separate secrets and build outputs |
| Audio/media | Transcripts, subtitles, technical recordings | Timestamped retrieval; review OCR/transcription errors |
| Operational telemetry | Approved metrics and incident summaries | Short retention and scoped queries; raw logs can be highly sensitive |

[Obsidian stores Markdown files](https://obsidian.md/help/data-storage). Preserve them as the source of truth and index a read-only controlled copy. Sync is a distribution mechanism; backup is a recovery mechanism. A community sync plugin and its database backend are separate components.

### Ingestion contract

Each imported item needs a document ID, owner/project, source URI, content hash, version, timestamp and sensitivity. Chunks inherit permissions. Record parser and embedding versions, dimensions, normalization and chunking policy. Handle renames, updates, duplicates and deletion as first-class events. Use bounded retries and a dead-letter queue rather than silently dropping failures.

The query path authenticates the caller, determines authorized collections, performs filtered retrieval, combines lexical and semantic results as needed, reranks authorized candidates and returns citations. Apply authorization to raw passages, graph edges, generated summaries, caches and exports. Do not retrieve everything into the model and ask it to hide forbidden content afterward. Shared vector filters and SQL grants require adversarial cross-project testing.

Use a new index for changed embedding models and keep an explicit switch/rollback mechanism. Approximate nearest-neighbor indexes can return different recall under restrictive filtering; measure against exact retrieval on representative examples. Start with full-text + pgvector and add Qdrant or another engine only when requirements or measured results warrant it.

## Supabase's place in the platform

Use the [official self-hosted Docker bundle](https://supabase.com/docs/guides/self-hosting/docker) when application auth, storage and APIs are required. PostgreSQL/pgvector alone can be sufficient for the first retrieval service. The research checked the [current changelog](https://supabase.com/changelog.md); it contains a CLI v3 behavior change, so earlier command examples require verification before use.

A migration needs a staging restore, extension compatibility, row and object checks, authentication flows, RLS, function redeployment and configuration review. Database restore does not alone move stored objects, provider settings or all external integrations. Preserve a write-freeze/cutover/rollback plan. [Official restore guide](https://supabase.com/docs/guides/self-hosting/restore-from-platform).

## Best practices for this workload

| Practice | Concrete application | How to verify |
|---|---|---|
| Keep the control plane outside the agent | No Docker socket or Proxmox token in model-facing workers | Attempt prohibited management operations |
| Deny unwanted egress | Worker network permits only approved destinations through enforced routes | IPv4/IPv6, direct connection, DNS and redirect tests |
| Minimize data exposure | Retrieval returns authorized excerpts instead of whole vault mounts | Inspect mounts, credentials and actual request payloads |
| Treat content as untrusted | Retrieved text cannot alter tool policy | Malicious-document and tool-metadata regression examples |
| Make filesystem scope real | Canonical path, symlink and race-resistant file operations | Traversal/symlink/cross-project tests |
| Use disposable execution | New job directory/session and bounded resources | Timeout, memory, cleanup and output-promotion checks |
| Separate identities | Different browser accounts and service credentials per role | Revocation and cross-session access tests |
| Pin verified artifacts | Release plus image digest, model revision and dependency lock | Rebuild from a recorded manifest |
| Review updates | Scan images, generate SBOM, stage updates, restore before migrations | Evidence from build, vulnerability review and recovery |
| Preserve provenance | Answers identify original source and version | Citation and stale-document evaluation |
| Record limited telemetry | Correlation IDs and policy decisions; redact secrets | Inspect actual log output, retention and reader permissions |
| Test recovery | Restore files, DB, keys and objects independently of failed server | Timed clean-environment recovery drill |

[Docker security](https://docs.docker.com/engine/security/) and [firewall documentation](https://docs.docker.com/engine/network/packet-filtering-firewalls/) explain why merely creating containers and enabling a host firewall does not establish these properties. [Open WebUI hardening](https://docs.openwebui.com/getting-started/advanced-topics/hardening/) covers application-specific sharing, extension, access and outbound behavior. [Qdrant security](https://qdrant.tech/documentation/security/) requires explicit self-hosted configuration.

## Licensing and product boundaries

The catalog retains raw GitHub SPDX values and flags unclassified/mixed cases. Custom terms were inspected for prominent candidates: Open WebUI has its own license; Dify modifies Apache terms; Browserless offers SSPL/commercial terms; Onyx, Langfuse, LiteLLM and Authentik separate core and other licensed areas; Phoenix uses Elastic License 2.0; Weaviate distinguishes BSD and separately licensed directories. See each linked license file in the evidence. This is source identification, not legal interpretation.

Model weights, OCR models, voices, browser binaries, codecs, plugins and commercial features have separate terms. Do not copy a permissive repository label onto an entire assembled image. Before a public hosted offering, verify the exact edition/features and rights independently. The public portfolio can demonstrate synthetic integrations without redistributing third-party source snapshots or model weights.

## Practical rollout and resources

Begin with one UI, one retrieval database, one ingestion worker, one execution boundary and one management route. Choose between an integrated knowledge platform and a custom retrieval pipeline initially; avoid maintaining both without a use case. Use separate Compose projects for independent update and recovery lifecycles.

For planning, a persistent-services guest with 8–16 GB RAM and an execution guest with 8–16 GB can support an initial limited pilot, depending on selected services. These are unmeasured allocations and exclude large local models, graph extraction and heavyweight multi-service platforms. Supabase alone documents 8 GB+ recommended RAM. Inventory actual host capacity and reserve hypervisor resources before allocating guests. GPU/accelerator compatibility, model size, context and concurrency determine inference needs; no hardware purchase is justified by this report alone.

For each selected component, record a component manifest: upstream, license, exact version/digest, CPU architecture, ports, mounts, credentials, outbound destinations, data retention, backup method, owner, allowed tools, denied operations and evidence. Use [the roadmap](../../ROADMAP.md) for acceptance gates and [the Proxmox design](../../PROXMOX-ARCHITECTURE.md) for placement.

## Troubleshooting and recovery limits

Stale search usually indicates missed events, parser failures, an index-version mismatch or an authorization filter. Inspect ingestion records before changing model prompts. A browser that cannot reach a site may be correctly denied by policy; inspect denied-request logs before widening access. A tool that works only with root or host networking needs a permissions/design review. An empty vector result may be an ownership/filter/index issue rather than a model problem.

Recover originals, database and credentials before rebuilding disposable indexes. Test object/database consistency. A Git repository restores code and design, not the data platform. Keep application backups and VM backups, with off-host copies and independent keys. No recovery guarantee or performance result is claimed until measured in a real deployment.
