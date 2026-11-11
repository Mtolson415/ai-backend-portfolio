# AI container and tool catalog

Research snapshot: **November 11, 2026**. **181 projects / 16 categories.**

This is a broad bounded inventory, including libraries, extensions and host runtimes that can support containerized AI work. It is not 181 ready-made containers or a tested stack. Read [the analysis](ANALYSIS.md) and [the source evidence](catalog-evidence.json).

## Reading the catalog

- **Start:** suitable for an early limited pilot, subject to validation.
- **Evaluate:** strong fit worth comparing against a baseline.
- **Alternative:** an overlapping choice; do not install all alternatives.
- **Experimental:** higher uncertainty; keep out of the initial persistent platform.
- **Later:** defer until scale or complexity warrants it.
- **Reference:** source or building block, not a recommended standalone deployment.
- **Avoid-new:** archived upstream; retain as research/migration context.

**Deployment families are editorial classifications:** Container/Stack indicate a service-style deployment to investigate, not proof of a production image. Build/Library/Extension require packaging/integration. Platform/Runtime/Host need infrastructure work. Plugin needs a separate host application/backend.

**Release references** come from the repository latest-release endpoint (or stated official documentation). They can name subpackages and are not tested service/image pins. A missing reference is not proof of inactivity. GitHub license classification is not a complete legal assessment. Follow the license source for custom/mixed cases.

| Category | Entries |
|---|---:|
| [Agent workspaces](#agent-workspaces) | 15 |
| [Orchestration](#orchestration) | 8 |
| [Tool gateways](#tool-gateways) | 11 |
| [Browsing and research](#browsing-and-research) | 13 |
| [Knowledge and RAG](#knowledge-and-rag) | 9 |
| [Document ingestion](#document-ingestion) | 10 |
| [Databases and search](#databases-and-search) | 16 |
| [Model services](#model-services) | 12 |
| [Programs and desktops](#programs-and-desktops) | 12 |
| [Knowledge sources](#knowledge-sources) | 14 |
| [Storage and exchange](#storage-and-exchange) | 6 |
| [Automation](#automation) | 7 |
| [Evaluation and telemetry](#evaluation-and-telemetry) | 11 |
| [Identity and perimeter](#identity-and-perimeter) | 13 |
| [Isolation and supply chain](#isolation-and-supply-chain) | 13 |
| [Management and backup](#management-and-backup) | 11 |

## Agent workspaces

Choose one primary interface and one execution model. An integrated agent computer is powerful but shares browser, file and shell state. Archived entries are retained only for reference.

| Project / official source | Purpose | Family / recommendation | Repository release reference | License classification | Boundary / adoption concern |
|---|---|---|---|---|---|
| [OpenHands](https://github.com/OpenHands/OpenHands) | Coding agent with managed execution workspaces | Stack / **Evaluate** | [v1.38.0](https://github.com/OpenHands/OpenHands/releases/tag/v1.38.0) | MIT | Controller is privileged infrastructure; isolate its worker host |
| [Agent Infra AIO Sandbox](https://github.com/agent-infra/sandbox) | Browser, shell, files and notebook environment exposed through APIs | Container / **Evaluate** | [v1.11.0](https://github.com/agent-infra/sandbox/releases/tag/v1.11.0) | Apache-2.0 | All-in-one shared state enlarges compromise scope; disposable workers |
| [OpenSandbox](https://github.com/opensandbox-group/OpenSandbox) | Lifecycle and execution APIs for agent sandboxes | Platform / **Evaluate** | [release-1.2.0](https://github.com/opensandbox-group/OpenSandbox/releases/tag/release-1.2.0) | Apache-2.0 | Runtime controller needs infrastructure permissions; keep outside agent reach |
| [NVIDIA OpenShell](https://github.com/NVIDIA/OpenShell) | Agent runtime with filesystem and outbound network policy | Runtime / **Evaluate** | [v0.1.8](https://github.com/NVIDIA/OpenShell/releases/tag/v0.1.8) | Apache-2.0 | Linux kernel and effective-policy requirements must be verified |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Persistent tool-using agent with skills and memory | Build / **Evaluate** | [v0.23.1](https://github.com/NousResearch/hermes-agent/releases/tag/v0.23.1) | MIT | Audit tools, messaging connectors and memory writes before enabling |
| [OpenClaw](https://github.com/openclaw/openclaw) | Personal agent with tools and communication integrations | Stack / **Evaluate** | [v2026.11.3](https://github.com/openclaw/openclaw/releases/tag/v2026.11.3) | MIT | Broad account and execution access requires separate identities |
| [Sandbar](https://github.com/jdrolls/sandbar) | Visible agent desktop with human takeover and API control | Container / **Experimental** | No latest-release reference; inspect tags/docs | MIT | Emerging project; validate viewer authentication and session separation |
| [LibreChat](https://github.com/LibreChat-AI/LibreChat) | Multi-provider chat and agent interface | Stack / **Alternative** | No latest-release reference; inspect tags/docs | MIT | Resource permissions must match downstream retrieval permissions |
| [Open WebUI](https://github.com/open-webui/open-webui) | Private chat interface with knowledge and external tools | Container / **Start** | [v0.13.3](https://github.com/open-webui/open-webui/releases/tag/v0.13.3) | [NOASSERTION; Custom Open WebUI license; inspect exact release terms](https://github.com/open-webui/open-webui/blob/main/LICENSE) | Avoid unreviewed in-process extensions and broad terminal access |
| [LobeChat](https://github.com/lobehub/lobehub) | Assistant interface and knowledge integrations | Stack / **Alternative** | [v2.3.2](https://github.com/lobehub/lobehub/releases/tag/v2.3.2) | [NOASSERTION; inspect exact license](https://github.com/lobehub/lobehub/blob/canary/LICENSE) | Check deployed edition, authentication and external-service dependencies |
| [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) | Integrated document chat and agent workspace | Container / **Alternative** | [v1.19.0](https://github.com/Mintplex-Labs/anything-llm/releases/tag/v1.19.0) | MIT | Workspace separation needs end-to-end permission tests |
| [Dify](https://github.com/langgenius/dify) | Visual AI applications, workflows and retrieval | Stack / **Alternative** | [1.19.0](https://github.com/langgenius/dify/releases/tag/1.19.0) | [NOASSERTION; Modified Apache terms; additional conditions](https://github.com/langgenius/dify/blob/main/LICENSE) | Plugin execution and provider credentials need separate controls |
| [Flowise](https://github.com/FlowiseAI/Flowise) | Visual agent and retrieval workflow builder | Container / **Avoid-new** | [flowise@3.1.4](https://github.com/FlowiseAI/Flowise/releases/tag/flowise%403.1.4) | [NOASSERTION; inspect exact license](https://github.com/FlowiseAI/Flowise/blob/main/LICENSE.md) | Upstream repository is archived; not selected for a new foundation |
| [Langflow](https://github.com/langflow-ai/langflow) | Visual orchestration of AI components | Container / **Alternative** | [v1.13.2](https://github.com/langflow-ai/langflow/releases/tag/v1.13.2) | MIT | Treat workflow creation as privileged code configuration |
| [DeerFlow](https://github.com/bytedance/deer-flow) | Research and agent execution workflows | Stack / **Experimental** | [v2.2.0](https://github.com/bytedance/deer-flow/releases/tag/v2.2.0) | MIT | Inspect version-specific sandbox and tool permissions |

Source detail, README blob identifiers, observation times and root deployment/license paths are in the structured evidence. No runtime validation is implied.

## Orchestration

These are application frameworks, not standalone isolation boundaries. Package only the selected framework and write explicit tool authorization.

| Project / official source | Purpose | Family / recommendation | Repository release reference | License classification | Boundary / adoption concern |
|---|---|---|---|---|---|
| [LangGraph](https://github.com/langchain-ai/langgraph) | Stateful agent workflows, checkpoints and human review | Library / **Evaluate** | [sdk==0.4.14](https://github.com/langchain-ai/langgraph/releases/tag/sdk%3D%3D0.4.14) | MIT | Framework is not a security boundary; package your own service |
| [Haystack](https://github.com/deepset-ai/haystack) | Explicit indexing, retrieval and agent pipelines | Library / **Evaluate** | [v3.5.0](https://github.com/deepset-ai/haystack/releases/tag/v3.5.0) | Apache-2.0 | Connector identities and filtering belong in application design |
| [LlamaIndex](https://github.com/run-llama/llama_index) | Document indexing and retrieval integrations | Library / **Alternative** | [v0.14.25](https://github.com/run-llama/llama_index/releases/tag/v0.14.25) | MIT | Audit each integration for cloud calls and permission handling |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | Typed agent inputs, outputs and tool interfaces | Library / **Evaluate** | [v2.67.0](https://github.com/pydantic/pydantic-ai/releases/tag/v2.67.0) | MIT | Validation is not authorization or execution isolation |
| [Semantic Kernel](https://github.com/microsoft/semantic-kernel) | Application-oriented agent and tool orchestration | Library / **Alternative** | [dotnet-1.82.0](https://github.com/microsoft/semantic-kernel/releases/tag/dotnet-1.82.0) | MIT | Run approved plugins with least-privilege service identities |
| [AutoGen](https://github.com/microsoft/autogen) | Agent coordination and tool-based applications | Library / **Alternative** | [python-v0.7.5](https://github.com/microsoft/autogen/releases/tag/python-v0.7.5) | CC-BY-4.0 | Check current maintenance direction before starting new work |
| [CrewAI](https://github.com/crewAIInc/crewAI) | Role-oriented multi-agent workflows | Library / **Alternative** | [1.15.39](https://github.com/crewAIInc/crewAI/releases/tag/1.15.39) | MIT | Shared memory and tool permissions need explicit isolation |
| [Deep Agents](https://github.com/langchain-ai/deepagents) | Planning, filesystem and delegated agent workflows | Library / **Evaluate** | [deepagents==0.7.35](https://github.com/langchain-ai/deepagents/releases/tag/deepagents%3D%3D0.7.35) | MIT | Virtual filesystem abstraction is not OS isolation |

Source detail, README blob identifiers, observation times and root deployment/license paths are in the structured evidence. No runtime validation is implied.

## Tool gateways

Gateways, MCP servers and server-building libraries have different responsibilities. Dynamic discovery must not grant permission. Keep infrastructure control outside the model.

| Project / official source | Purpose | Family / recommendation | Repository release reference | License classification | Boundary / adoption concern |
|---|---|---|---|---|---|
| [agentgateway](https://github.com/agentgateway/agentgateway) | Gateway for agent, model and MCP traffic | Container / **Evaluate** | [v1.7.0](https://github.com/agentgateway/agentgateway/releases/tag/v1.7.0) | Apache-2.0 | Verify enforcement per route and caller; no automatic trust in tools |
| [Docker MCP Gateway](https://github.com/docker/mcp-gateway) | Containerized MCP tool routing and discovery | Platform / **Evaluate** | No latest-release reference; inspect tags/docs | MIT | Controller access to Docker belongs on dedicated worker infrastructure |
| [ContextForge MCP Gateway](https://github.com/IBM/mcp-context-forge) | Federated MCP gateway and management | Container / **Alternative** | [v1.1.1](https://github.com/IBM/mcp-context-forge/releases/tag/v1.1.1) | Apache-2.0 | Validate identity propagation, SSRF controls and administrative routes |
| [FastMCP](https://github.com/PrefectHQ/fastmcp) | Build narrow Python MCP tools for local services | Library / **Start** | [v4.1.8](https://github.com/PrefectHQ/fastmcp/releases/tag/v4.1.8) | Apache-2.0 | Implement path checks, caller authorization and request limits |
| [MCP reference servers](https://github.com/modelcontextprotocol/servers) | Reference filesystem and other tool implementations | Build / **Reference** | [v2.4.0](https://github.com/modelcontextprotocol/servers/releases/tag/v2.4.0) | [NOASSERTION; inspect exact license](https://github.com/modelcontextprotocol/servers/blob/main/LICENSE) | Reference examples are not an audited production tool catalog |
| [ToolHive](https://github.com/stacklok/toolhive) | Manage and run MCP servers in controlled environments | Platform / **Evaluate** | [v0.64.0](https://github.com/stacklok/toolhive/releases/tag/v0.64.0) | Apache-2.0 | Inspect runtime permissions and selected deployment backend |
| [GitHub MCP Server](https://github.com/github/github-mcp-server) | Official repository, issue and code tools | Container / **Evaluate** | [v2.1.0](https://github.com/github/github-mcp-server/releases/tag/v2.1.0) | MIT | Start with read-only toolsets and scoped repository access |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | Browser tools exposed through MCP | Container / **Evaluate** | [v0.0.85](https://github.com/microsoft/playwright-mcp/releases/tag/v0.0.85) | Apache-2.0 | Use isolated browser profile; tool server is not a hardened browser boundary |
| [Context7](https://github.com/upstash/context7) | Retrieve current library documentation on demand | Build / **Evaluate** | [@upstash/context7-mcp@4.6.0](https://github.com/upstash/context7/releases/tag/%40upstash/context7-mcp%404.6.0) | MIT | Local MCP process can still depend on external hosted documentation |
| [Qdrant MCP Server](https://github.com/qdrant/mcp-server-qdrant) | Store and retrieve selected semantic knowledge | Build / **Alternative** | [v0.8.1](https://github.com/qdrant/mcp-server-qdrant/releases/tag/v0.8.1) | Apache-2.0 | Scope collections and forbid cross-project recall |
| [Terraform MCP Server](https://github.com/hashicorp/terraform-mcp-server) | Provider documentation and infrastructure tools | Container / **Reference** | [v1.4.1](https://github.com/hashicorp/terraform-mcp-server/releases/tag/v1.4.1) | MPL-2.0 | Separate documentation lookup from credentialed infrastructure actions |

Source detail, README blob identifiers, observation times and root deployment/license paths are in the structured evidence. No runtime validation is implied.

## Browsing and research

Separate search discovery, page extraction, persistent research capture and interactive account actions. Browser sessions and downloads are untrusted or credential-bearing.

| Project / official source | Purpose | Family / recommendation | Repository release reference | License classification | Boundary / adoption concern |
|---|---|---|---|---|---|
| [Playwright](https://github.com/microsoft/playwright) | Deterministic browser automation and screenshots | Build / **Start** | [v1.65.0](https://github.com/microsoft/playwright/releases/tag/v1.65.0) | Apache-2.0 | Official test image alone is not hardened for arbitrary hostile sites |
| [Browserless](https://github.com/browserless/browserless) | Remote browser automation service | Container / **Evaluate** | [v2.62.0](https://github.com/browserless/browserless/releases/tag/v2.62.0) | [NOASSERTION; SSPL or commercial terms](https://github.com/browserless/browserless/blob/main/LICENSE) | Browser debugging endpoints are powerful; authenticate and isolate |
| [Browser Use](https://github.com/browser-use/browser-use) | LLM-driven browser task execution | Build / **Evaluate** | [1.0.2](https://github.com/browser-use/browser-use/releases/tag/1.0.2) | MIT | Separate browser accounts, downloads and outbound access |
| [Skyvern](https://github.com/Skyvern-AI/skyvern) | Vision-assisted browser workflows | Stack / **Evaluate** | [v1.0.57](https://github.com/Skyvern-AI/skyvern/releases/tag/v1.0.57) | AGPL-3.0 | Authenticated automation can change external accounts |
| [Stagehand](https://github.com/browserbase/stagehand) | Browser automation combining code and AI | Library / **Alternative** | [stagehand-server-v3/v3.7.7](https://github.com/browserbase/stagehand/releases/tag/stagehand-server-v3/v3.7.7) | MIT | Distinguish local browser support from hosted Browserbase services |
| [Crawl4AI](https://github.com/unclecode/crawl4ai) | Web extraction and crawling for retrieval | Container / **Evaluate** | [v0.9.5](https://github.com/unclecode/crawl4ai/releases/tag/v0.9.5) | Apache-2.0 | Restrict destinations, redirects, file sizes and crawl budgets |
| [Firecrawl](https://github.com/firecrawl/firecrawl) | Website crawling and structured extraction API | Stack / **Alternative** | [v2.11.0](https://github.com/firecrawl/firecrawl/releases/tag/v2.11.0) | AGPL-3.0 | Self-hosted feature parity differs; bound crawling and outbound traffic |
| [SearXNG](https://github.com/searxng/searxng) | Self-hosted metasearch endpoint | Container / **Start** | No latest-release reference; inspect tags/docs | AGPL-3.0 | Queries still reach configured upstream search engines |
| [Karakeep](https://github.com/karakeep-app/karakeep) | Saved links and research collection | Stack / **Evaluate** | [v0.34.1](https://github.com/karakeep-app/karakeep/releases/tag/v0.34.1) | AGPL-3.0 | Saved pages and AI enrichment can contain sensitive data |
| [ArchiveBox](https://github.com/ArchiveBox/ArchiveBox) | Preserve captured web research | Container / **Evaluate** | [v0.9.77](https://github.com/ArchiveBox/ArchiveBox/releases/tag/v0.9.77) | MIT | Downloaded content is untrusted and retention needs limits |
| [Wallabag](https://github.com/wallabag/wallabag) | Read-later article collection | Container / **Alternative** | [2.6.15](https://github.com/wallabag/wallabag/releases/tag/2.6.15) | MIT | Protect authenticated feeds and exported content |
| [Perplexica](https://github.com/ItzCrazyKns/Vane) | Self-hosted search and research assistant | Stack / **Evaluate** | [v1.12.2](https://github.com/ItzCrazyKns/Vane/releases/tag/v1.12.2) | MIT | Verify source citations, model calls and search-provider traffic |
| [GPT Researcher](https://github.com/assafelovic/gpt-researcher) | Multi-source research and report generation | Stack / **Evaluate** | [v3.8.0](https://github.com/assafelovic/gpt-researcher/releases/tag/v3.8.0) | Apache-2.0 | Treat retrieved instructions as untrusted and bound research budgets |

Source detail, README blob identifiers, observation times and root deployment/license paths are in the structured evidence. No runtime validation is implied.

## Knowledge and RAG

Evaluate an integrated product against a simpler custom pipeline. Test source ACL propagation, deletion, citations and temporal facts before ingesting private material.

| Project / official source | Purpose | Family / recommendation | Repository release reference | License classification | Boundary / adoption concern |
|---|---|---|---|---|---|
| [RAGFlow](https://github.com/infiniflow/ragflow) | Integrated document retrieval and agent platform | Stack / **Evaluate** | [v1.0.0](https://github.com/infiniflow/ragflow/releases/tag/v1.0.0) | Apache-2.0 | Check actual dependency footprint and access isolation |
| [Onyx](https://github.com/onyx-dot-app/onyx) | Connected enterprise-style knowledge search | Stack / **Evaluate** | [v5.1.1](https://github.com/onyx-dot-app/onyx/releases/tag/v5.1.1) | [NOASSERTION; MIT core plus separately licensed enterprise directories](https://github.com/onyx-dot-app/onyx/blob/main/LICENSE) | Connector ACL synchronization must be proven for each source |
| [Kotaemon](https://github.com/Cinnamon/kotaemon) | Document question answering interface | Container / **Alternative** | [v0.12.0](https://github.com/Cinnamon/kotaemon/releases/tag/v0.12.0) | Apache-2.0 | Test citations and multi-user separation |
| [LightRAG](https://github.com/HKUDS/LightRAG) | Graph-assisted document retrieval | Container / **Evaluate** | [v1.5.7](https://github.com/HKUDS/LightRAG/releases/tag/v1.5.7) | MIT | Configure authentication and protect compatibility endpoints |
| [Microsoft GraphRAG](https://github.com/microsoft/graphrag) | Entity and community based graph retrieval | Library / **Experimental** | [v3.3.0](https://github.com/microsoft/graphrag/releases/tag/v3.3.0) | MIT | Indexing cost and inferred relationships need evaluation |
| [Graphiti](https://github.com/getzep/graphiti) | Temporal knowledge graph for changing facts | Library / **Evaluate** | [v0.31.2](https://github.com/getzep/graphiti/releases/tag/v0.31.2) | Apache-2.0 | Entity provenance, deletion and date-sensitive access need design |
| [Mem0](https://github.com/mem0ai/mem0) | Persistent agent memory extraction and retrieval | Library / **Evaluate** | [ts-v3.3.1](https://github.com/mem0ai/mem0/releases/tag/ts-v3.3.1) | Apache-2.0 | Require consent, provenance and correction/deletion workflows |
| [Letta](https://github.com/letta-ai/letta) | Stateful agents with persistent memory | Container / **Alternative** | [0.16.8](https://github.com/letta-ai/letta/releases/tag/0.16.8) | Apache-2.0 | Agent memory should not silently become authoritative evidence |
| [Khoj](https://github.com/khoj-ai/khoj) | Personal knowledge assistant and search | Stack / **Alternative** | [2.0.0-beta.28](https://github.com/khoj-ai/khoj/releases/tag/2.0.0-beta.28) | AGPL-3.0 | Check local-model paths and optional hosted dependencies |

Source detail, README blob identifiers, observation times and root deployment/license paths are in the structured evidence. No runtime validation is implied.

## Document ingestion

Documents are untrusted parser input. Bound file sizes, decompression, time and memory. Preserve page/section provenance and original files.

| Project / official source | Purpose | Family / recommendation | Repository release reference | License classification | Boundary / adoption concern |
|---|---|---|---|---|---|
| [Docling Serve](https://github.com/docling-project/docling-serve) | API for structured document conversion | Container / **Start** | [v1.38.2](https://github.com/docling-project/docling-serve/releases/tag/v1.38.2) | MIT | Restrict input paths, parser resources and model downloads |
| [Docling](https://github.com/docling-project/docling) | Document layout and conversion pipeline | Library / **Reference** | [v2.150.0](https://github.com/docling-project/docling/releases/tag/v2.150.0) | MIT | Use through isolated workers; models have separate licenses |
| [MarkItDown](https://github.com/microsoft/markitdown) | Convert office and other formats into Markdown | Build / **Evaluate** | [v0.1.9](https://github.com/microsoft/markitdown/releases/tag/v0.1.9) | MIT | Optional plugins may contact external providers |
| [Unstructured](https://github.com/Unstructured-IO/unstructured) | Parse and partition heterogeneous documents | Library / **Alternative** | [0.27.37](https://github.com/Unstructured-IO/unstructured/releases/tag/0.27.37) | Apache-2.0 | Distinguish library, API container and hosted service capabilities |
| [Apache Tika](https://github.com/apache/tika) | Broad file-format text and metadata extraction | Container / **Evaluate** | No latest-release reference; inspect tags/docs | Apache-2.0 | Untrusted parsers need time, memory and upload limits |
| [Gotenberg](https://github.com/gotenberg/gotenberg) | HTML and office document conversion to PDF | Container / **Evaluate** | [v9.4.0](https://github.com/gotenberg/gotenberg/releases/tag/v9.4.0) | MIT | Control browser fetches and arbitrary URL conversion |
| [OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF) | Add OCR text layers to scanned PDFs | Build / **Evaluate** | [v17.14.1](https://github.com/ocrmypdf/OCRmyPDF/releases/tag/v17.14.1) | MPL-2.0 | Untrusted PDFs belong in disposable conversion jobs |
| [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | OCR and document understanding | Build / **Evaluate** | [v3.7.0](https://github.com/PaddlePaddle/PaddleOCR/releases/tag/v3.7.0) | Apache-2.0 | Verify model licenses and CPU/GPU image compatibility |
| [MinerU](https://github.com/opendatalab/MinerU) | Document extraction and layout reconstruction | Build / **Experimental** | [mineru-4.2.0-released](https://github.com/opendatalab/MinerU/releases/tag/mineru-4.2.0-released) | [NOASSERTION; inspect exact license](https://github.com/opendatalab/MinerU/blob/master/LICENSE.md) | Model resources and licensing require separate review |
| [Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx) | Searchable archive for scanned and digital documents | Stack / **Start** | [v3.4.2](https://github.com/paperless-ngx/paperless-ngx/releases/tag/v3.4.2) | GPL-3.0 | Originals, OCR text and previews share sensitivity |

Source detail, README blob identifiers, observation times and root deployment/license paths are in the structured evidence. No runtime validation is implied.

## Databases and search

Start with one primary retrieval store. A graph database, vector index and full-text index serve different query needs. Extensions require compatible database images.

| Project / official source | Purpose | Family / recommendation | Repository release reference | License classification | Boundary / adoption concern |
|---|---|---|---|---|---|
| [Supabase](https://github.com/supabase/supabase) | Postgres, auth, storage and application APIs | Stack / **Evaluate** | [v1.26.08](https://github.com/supabase/supabase/releases/tag/v1.26.08) | Apache-2.0 | Use official compose bundle; RLS and backups remain operator duties |
| [pgvector](https://github.com/pgvector/pgvector) | Vector similarity search inside PostgreSQL | Extension / **Start** | No latest-release reference; inspect tags/docs | [NOASSERTION; PostgreSQL-style license; inspect source license](https://github.com/pgvector/pgvector/blob/master/LICENSE) | Pin extension with database version; test filtered recall |
| [Qdrant](https://github.com/qdrant/qdrant) | Dedicated vector search and metadata filtering | Container / **Evaluate** | [v1.20.0](https://github.com/qdrant/qdrant/releases/tag/v1.20.0) | Apache-2.0 | Configure authentication; network isolation alone is insufficient |
| [Weaviate](https://github.com/weaviate/weaviate) | Object and vector search platform | Container / **Alternative** | [v1.40.5](https://github.com/weaviate/weaviate/releases/tag/v1.40.5) | [NOASSERTION; BSD core plus separately licensed wl directory](https://github.com/weaviate/weaviate/blob/main/LICENSE) | Explicit auth, module and model-provider configuration |
| [Milvus](https://github.com/milvus-io/milvus) | Vector retrieval for larger workloads | Stack / **Later** | [v3.0.6](https://github.com/milvus-io/milvus/releases/tag/v3.0.6) | Apache-2.0 | Additional services increase recovery and operations burden |
| [Chroma](https://github.com/chroma-core/chroma) | Vector storage for experiments and applications | Container / **Alternative** | [1.5.9](https://github.com/chroma-core/chroma/releases/tag/1.5.9) | Apache-2.0 | Validate deployed security model before multi-user use |
| [OpenSearch](https://github.com/opensearch-project/OpenSearch) | Text, vector and structured search | Stack / **Alternative** | [3.9.0](https://github.com/opensearch-project/OpenSearch/releases/tag/3.9.0) | Apache-2.0 | Heap sizing, plugins and security configuration require attention |
| [Meilisearch](https://github.com/meilisearch/meilisearch) | Fast application search | Container / **Alternative** | [v1.56.2](https://github.com/meilisearch/meilisearch/releases/tag/v1.56.2) | [NOASSERTION; inspect exact license](https://github.com/meilisearch/meilisearch/blob/main/LICENSE) | Distinguish community and commercial features |
| [Typesense](https://github.com/typesense/typesense) | Application search with filtering | Container / **Alternative** | [v30.2](https://github.com/typesense/typesense/releases/tag/v30.2) | GPL-3.0 | Scope search and administrative API keys separately |
| [Vespa](https://github.com/vespa-engine/vespa) | Advanced retrieval and ranking applications | Stack / **Later** | [v8.781.11](https://github.com/vespa-engine/vespa/releases/tag/v8.781.11) | Apache-2.0 | Powerful but operationally complex for a small personal corpus |
| [Neo4j](https://github.com/neo4j/neo4j) | Property graph storage and traversal | Container / **Evaluate** | [3.2.0-alpha08](https://github.com/neo4j/neo4j/releases/tag/3.2.0-alpha08) | GPL-3.0 | Community and Enterprise features and licenses differ |
| [Apache AGE](https://github.com/apache/age) | Graph querying inside PostgreSQL | Extension / **Experimental** | [PG18/v1.8.0-rc0](https://github.com/apache/age/releases/tag/PG18/v1.8.0-rc0) | Apache-2.0 | Verify supported Postgres versions and image build compatibility |
| [FalkorDB](https://github.com/FalkorDB/FalkorDB) | Graph database for relationship retrieval | Container / **Alternative** | [v6.0.4](https://github.com/FalkorDB/FalkorDB/releases/tag/v6.0.4) | [NOASSERTION; inspect exact license](https://github.com/FalkorDB/FalkorDB/blob/main/LICENSE) | Check licensing and backend support of chosen RAG framework |
| [DuckDB](https://github.com/duckdb/duckdb) | Local analytical SQL over datasets | Library / **Start** | [v2.0.0](https://github.com/duckdb/duckdb/releases/tag/v2.0.0) | MIT | Run on authorized files with memory limits |
| [LanceDB](https://github.com/lancedb/lancedb) | Embedded vector and multimodal retrieval | Library / **Alternative** | [v0.41.0](https://github.com/lancedb/lancedb/releases/tag/v0.41.0) | Apache-2.0 | Separate open-source embedded engine from managed features |
| [sqlite-vec](https://github.com/asg017/sqlite-vec) | Vector search embedded in SQLite | Extension / **Experimental** | [v0.1.9](https://github.com/asg017/sqlite-vec/releases/tag/v0.1.9) | Apache-2.0 | Useful single-user option; verify extension and database access boundaries |

Source detail, README blob identifiers, observation times and root deployment/license paths are in the structured evidence. No runtime validation is implied.

## Model services

Model runtime, model weights and GPU drivers have independent compatibility and licensing. No model ranking or tokens-per-second benchmark was performed.

| Project / official source | Purpose | Family / recommendation | Repository release reference | License classification | Boundary / adoption concern |
|---|---|---|---|---|---|
| [Ollama](https://github.com/ollama/ollama) | Simple local model serving | Container / **Start** | [v0.40.16](https://github.com/ollama/ollama/releases/tag/v0.40.16) | MIT | Protect API and record model identifiers and licenses |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | Portable quantized inference and compatible API | Build / **Start** | [v0.9.0](https://github.com/ggml-org/llama.cpp/releases/tag/v0.9.0) | MIT | CPU/GPU builds differ; bound context and parallel requests |
| [vLLM](https://github.com/vllm-project/vllm) | Higher-throughput model inference | Container / **Evaluate** | [v0.33.0rc3](https://github.com/vllm-project/vllm/releases/tag/v0.33.0rc3) | Apache-2.0 | Verify accelerator, driver, model and image compatibility |
| [SGLang](https://github.com/sgl-project/sglang) | Optimized language and multimodal model serving | Container / **Evaluate** | [v0.5.23](https://github.com/sgl-project/sglang/releases/tag/v0.5.23) | Apache-2.0 | Hardware requirements and rapidly changing APIs need testing |
| [LocalAI](https://github.com/mudler/LocalAI) | Local multi-backend inference APIs | Container / **Alternative** | [v4.12.1](https://github.com/mudler/LocalAI/releases/tag/v4.12.1) | MIT | Enable only needed backends and protect exposed API |
| [Xinference](https://github.com/xorbitsai/inference) | Manage multiple inference model types | Container / **Alternative** | [v4.2.0](https://github.com/xorbitsai/inference/releases/tag/v4.2.0) | Apache-2.0 | Model deployment privileges and resource quotas need control |
| [Text Embeddings Inference](https://github.com/huggingface/text-embeddings-inference) | Dedicated embedding and reranking service | Container / **Evaluate** | [v1.9.4](https://github.com/huggingface/text-embeddings-inference/releases/tag/v1.9.4) | Apache-2.0 | Pin embedding model revision and resulting vector dimensions |
| [LiteLLM](https://github.com/BerriAI/litellm) | Model routing, credentials and usage gateway | Container / **Evaluate** | [v1.109.0](https://github.com/BerriAI/litellm/releases/tag/v1.109.0) | [NOASSERTION; MIT core plus separately licensed enterprise directory](https://github.com/BerriAI/litellm/blob/main/LICENSE) | Cloud fallback must not silently export private data |
| [ComfyUI](https://github.com/Comfy-Org/ComfyUI) | Image and multimodal generation workflows | Build / **Evaluate** | [v0.45.0](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.45.0) | GPL-3.0 | Custom nodes execute code; separate image worker from knowledge services |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Speech transcription engine | Library / **Evaluate** | [v1.2.1](https://github.com/SYSTRAN/faster-whisper/releases/tag/v1.2.1) | MIT | Wrap as a bounded worker; transcripts inherit audio sensitivity |
| [whisper.cpp](https://github.com/ggml-org/whisper.cpp) | Portable local speech transcription | Build / **Alternative** | [v1.9.5](https://github.com/ggml-org/whisper.cpp/releases/tag/v1.9.5) | MIT | Test accuracy, timestamp handling and hardware build |
| [Kokoro FastAPI](https://github.com/remsky/Kokoro-FastAPI) | Local text-to-speech API | Container / **Experimental** | [v0.10.0](https://github.com/remsky/Kokoro-FastAPI/releases/tag/v0.10.0) | Apache-2.0 | Voice/model licenses and input retention need review |

Source detail, README blob identifiers, observation times and root deployment/license paths are in the structured evidence. No runtime validation is implied.

## Programs and desktops

Editors, notebooks and desktops are code execution. Mount a project workspace, not an entire home directory. Export reviewed outputs from disposable jobs.

| Project / official source | Purpose | Family / recommendation | Repository release reference | License classification | Boundary / adoption concern |
|---|---|---|---|---|---|
| [Jupyter Docker Stacks](https://github.com/jupyter/docker-stacks) | Notebook and data analysis environments | Container / **Start** | No latest-release reference; inspect tags/docs | BSD-3-Clause | Token authentication; no unrelated host mounts |
| [code-server](https://github.com/coder/code-server) | Browser-accessible development editor | Container / **Evaluate** | [v4.145.2](https://github.com/coder/code-server/releases/tag/v4.145.2) | MIT | Terminal access is code execution; restrict project and network |
| [OpenVSCode Server](https://github.com/gitpod-io/openvscode-server) | Web-based development workspace | Container / **Alternative** | [openvscode-server-v1.109.5](https://github.com/gitpod-io/openvscode-server/releases/tag/openvscode-server-v1.109.5) | MIT | Protect editor endpoint and extension installation |
| [Coder](https://github.com/coder/coder) | Provision managed developer workspaces | Platform / **Later** | [v2.38.7](https://github.com/coder/coder/releases/tag/v2.38.7) | AGPL-3.0 | Provisioner has broad infrastructure access |
| [LinuxServer Webtop](https://github.com/linuxserver/docker-webtop) | Linux desktop applications in a browser | Container / **Evaluate** | [0c46c80a-ls325](https://github.com/linuxserver/docker-webtop/releases/tag/0c46c80a-ls325) | GPL-3.0 | Desktop shares session secrets; isolate viewers and clipboard |
| [Apache Guacamole](https://github.com/apache/guacamole-client) | Browser access to remote desktop sessions | Stack / **Alternative** | No latest-release reference; inspect tags/docs | Apache-2.0 | Remote desktop gateway is an administrator-sensitive service |
| [Stirling PDF](https://github.com/Stirling-Tools/Stirling-PDF) | Interactive PDF manipulation tools | Container / **Evaluate** | [v3.3.0](https://github.com/Stirling-Tools/Stirling-PDF/releases/tag/v3.3.0) | [NOASSERTION; inspect exact license](https://github.com/Stirling-Tools/Stirling-PDF/blob/main/LICENSE) | Private documents and conversion endpoints need access control |
| [Pandoc](https://github.com/jgm/pandoc) | Convert documents and produce reports | Build / **Start** | [3.13](https://github.com/jgm/pandoc/releases/tag/3.13) | GPL-2.0 | External filters execute code; use approved templates and filters |
| [Marimo](https://github.com/marimo-team/marimo) | Reactive notebooks and data applications | Build / **Evaluate** | [0.25.2](https://github.com/marimo-team/marimo/releases/tag/0.25.2) | Apache-2.0 | Separate public app view from execution/edit privileges |
| [D2](https://github.com/d2lang/d2) | Generate architecture diagrams from text | Build / **Evaluate** | [v0.9.0](https://github.com/d2lang/d2/releases/tag/v0.9.0) | MPL-2.0 | Use job outputs; restrict external imports |
| [FFmpeg](https://github.com/FFmpeg/FFmpeg) | Audio and video processing jobs | Build / **Evaluate** | No latest-release reference; inspect tags/docs | [NOASSERTION; Build-dependent LGPL/GPL and optional codec constraints](https://github.com/FFmpeg/FFmpeg/blob/master/LICENSE.md) | Codecs have distinct build/license constraints and parsers handle untrusted media |
| [LibreOffice core](https://github.com/LibreOffice/core) | Headless office conversion or dedicated desktop application | Build / **Reference** | No latest-release reference; inspect tags/docs | GPL-3.0; Mixed source licensing; GitHub classifier is not a complete distribution license | Large untrusted-document attack surface; use isolated jobs |

Source detail, README blob identifiers, observation times and root deployment/license paths are in the structured evidence. No runtime validation is implied.

## Knowledge sources

These own source documents or synchronization. Retrieval should preserve their permissions and provenance. A plugin is not itself a server container.

| Project / official source | Purpose | Family / recommendation | Repository release reference | License classification | Boundary / adoption concern |
|---|---|---|---|---|---|
| [Obsidian LiveSync](https://github.com/vrtmrz/obsidian-livesync) | Community sync integration for an Obsidian vault | Plugin / **Alternative** | [1.0.49](https://github.com/vrtmrz/obsidian-livesync/releases/tag/1.0.49) | MIT | Plugin is not a standalone container; backend and sync conflicts need testing |
| [CouchDB](https://github.com/apache/couchdb) | Document database and potential sync backend | Container / **Alternative** | No latest-release reference; inspect tags/docs | Apache-2.0 | Do not expose permissive database access for sync convenience |
| [Syncthing](https://github.com/syncthing/syncthing) | Replicate selected source folders | Container / **Evaluate** | [v2.1.7](https://github.com/syncthing/syncthing/releases/tag/v2.1.7) | MPL-2.0 | Synchronization is not backup; validate deletion/conflict behavior |
| [Nextcloud Server](https://github.com/nextcloud/server) | Self-hosted files and collaboration | Stack / **Alternative** | [v33.0.10](https://github.com/nextcloud/server/releases/tag/v33.0.10) | AGPL-3.0 | Connectors must preserve source sharing permissions |
| [BookStack](https://github.com/BookStackApp/BookStack) | Structured documentation and runbooks | Stack / **Evaluate** | [v26.09.3](https://github.com/BookStackApp/BookStack/releases/tag/v26.09.3) | MIT | Validate API access against document permissions |
| [Wiki.js](https://github.com/requarks/wiki) | Private wiki and documentation | Stack / **Alternative** | [3.3.1](https://github.com/requarks/wiki/releases/tag/3.3.1) | AGPL-3.0 | Check deployment channel and export/recovery support |
| [SilverBullet](https://github.com/silverbulletmd/silverbullet) | Markdown-oriented personal knowledge workspace | Container / **Evaluate** | [2.12.1](https://github.com/silverbulletmd/silverbullet/releases/tag/2.12.1) | MIT | Plugins and scripts may extend permissions |
| [TriliumNext](https://github.com/TriliumNext/Trilium) | Hierarchical personal knowledge collection | Container / **Alternative** | [v0.107.0](https://github.com/TriliumNext/Trilium/releases/tag/v0.107.0) | AGPL-3.0 | Verify export formats and server access model |
| [Forgejo](https://forgejo.org/docs/latest/admin/installation/docker/) | Private Git repositories, issues and project documentation | Stack / **Evaluate** | [v17.0.1 (documentation channel)](https://forgejo.org/docs/latest/admin/installation/docker/) | [GPL-3.0-or-later](https://forgejo.org/faq/) | Repository hooks and runners need execution isolation |
| [Gitea](https://github.com/go-gitea/gitea) | Private source hosting and project history | Container / **Alternative** | [v28.3.0](https://github.com/go-gitea/gitea/releases/tag/v28.3.0) | MIT | Protect SSH keys, hooks and actions runners |
| [FreshRSS](https://github.com/FreshRSS/FreshRSS) | RSS intake and research feeds | Container / **Evaluate** | [1.30.4](https://github.com/FreshRSS/FreshRSS/releases/tag/1.30.4) | AGPL-3.0 | Limit feed fetch destinations and sensitive subscription URLs |
| [RSSHub](https://github.com/DIYgod/RSSHub) | Generate feeds from supported sites | Container / **Alternative** | [v2026.11.11-8627.1f862f8](https://github.com/DIYgod/RSSHub/releases/tag/v2026.11.11-8627.1f862f8) | AGPL-3.0 | Upstream scraping and authenticated routes need review |
| [Calibre-Web](https://github.com/janeczku/calibre-web) | Searchable ebook/reference library interface | Container / **Alternative** | [0.6.27](https://github.com/janeczku/calibre-web/releases/tag/0.6.27) | GPL-3.0 | Use lawfully held content and protect library write access |
| [Linkwarden](https://github.com/linkwarden/linkwarden) | Preserve and organize bookmarked web content | Stack / **Alternative** | [v2.17.0](https://github.com/linkwarden/linkwarden/releases/tag/v2.17.0) | AGPL-3.0 | Browser captures and shared collections need permission control |

Source detail, README blob identifiers, observation times and root deployment/license paths are in the structured evidence. No runtime validation is implied.

## Storage and exchange

Object stores, caches and message brokers have different persistence semantics. Validate S3 compatibility and backups with actual clients.

| Project / official source | Purpose | Family / recommendation | Repository release reference | License classification | Boundary / adoption concern |
|---|---|---|---|---|---|
| [Garage](https://github.com/deuxfleurs-org/garage) | Self-hosted S3-compatible object storage | Container / **Evaluate** | No latest-release reference; inspect tags/docs | AGPL-3.0 | Validate API compatibility, credentials and restore procedure |
| [SeaweedFS](https://github.com/seaweedfs/seaweedfs) | File and object storage services | Stack / **Alternative** | [4.53](https://github.com/seaweedfs/seaweedfs/releases/tag/4.53) | Apache-2.0 | Distribution adds complexity; test consistency requirements |
| [MinIO](https://github.com/minio/minio) | S3-compatible object storage candidate | Container / **Avoid-new** | [RELEASE.2025-10-15T17-29-55Z](https://github.com/minio/minio/releases/tag/RELEASE.2025-10-15T17-29-55Z) | AGPL-3.0 | Upstream repository is archived; evaluate maintained alternatives |
| [Valkey](https://github.com/valkey-io/valkey) | Cache, coordination and job primitives | Container / **Evaluate** | [9.1.3](https://github.com/valkey-io/valkey/releases/tag/9.1.3) | BSD-3-Clause | Internal access only; persistence and eviction must match usage |
| [RabbitMQ](https://github.com/rabbitmq/rabbitmq-server) | Reliable worker message queues | Container / **Alternative** | [v4.4.0](https://github.com/rabbitmq/rabbitmq-server/releases/tag/v4.4.0) | [NOASSERTION; inspect exact license](https://github.com/rabbitmq/rabbitmq-server/blob/main/LICENSE) | Use per-service users, dead-letter queues and bounded retries |
| [NATS](https://github.com/nats-io/nats-server) | Service messaging and event streams | Container / **Alternative** | [v2.15.3](https://github.com/nats-io/nats-server/releases/tag/v2.15.3) | Apache-2.0 | Restrict subjects and administrative monitoring endpoints |

Source detail, README blob identifiers, observation times and root deployment/license paths are in the structured evidence. No runtime validation is implied.

## Automation

Workflow authors can often execute code or use stored credentials. Prefer durable, idempotent jobs with retry budgets and explicit ownership.

| Project / official source | Purpose | Family / recommendation | Repository release reference | License classification | Boundary / adoption concern |
|---|---|---|---|---|---|
| [Temporal](https://github.com/temporalio/temporal) | Durable long-running jobs and retries | Stack / **Evaluate** | [v1.32.2](https://github.com/temporalio/temporal/releases/tag/v1.32.2) | MIT | Activities must be idempotent; cluster adds operational cost |
| [n8n](https://github.com/n8n-io/n8n) | Visual workflows and connectors | Container / **Evaluate** | [n8n@2.47.4](https://github.com/n8n-io/n8n/releases/tag/n8n%402.47.4) | [NOASSERTION; Fair-code/custom terms; inspect exact distribution](https://github.com/n8n-io/n8n/blob/master/LICENSE.md) | Fair-code terms; editors can run powerful workflows |
| [Windmill](https://github.com/windmill-labs/windmill) | Scripts, jobs and internal tools | Stack / **Alternative** | [v1.868.0](https://github.com/windmill-labs/windmill/releases/tag/v1.868.0) | [NOASSERTION; inspect exact license](https://github.com/windmill-labs/windmill/blob/main/LICENSE) | Worker secrets and execution permissions require separation |
| [Kestra](https://github.com/kestra-io/kestra) | Declarative scheduled and event workflows | Stack / **Alternative** | [v2.0.9](https://github.com/kestra-io/kestra/releases/tag/v2.0.9) | Apache-2.0 | Workers and plugin execution need separate permissions |
| [Prefect](https://github.com/PrefectHQ/prefect) | Python data workflow orchestration | Stack / **Alternative** | [3.9.2](https://github.com/PrefectHQ/prefect/releases/tag/3.9.2) | Apache-2.0 | Restrict worker pools and API access |
| [Node-RED](https://github.com/node-red/node-red) | Visual event-driven integrations | Container / **Alternative** | [5.0.9](https://github.com/node-red/node-red/releases/tag/5.0.9) | Apache-2.0 | Editor and installed nodes are privileged |
| [Apache Airflow](https://github.com/apache/airflow) | Scheduled data engineering pipelines | Stack / **Later** | [3.4.0](https://github.com/apache/airflow/releases/tag/3.4.0) | Apache-2.0 | Substantial footprint; DAG authors effectively execute code |

Source detail, README blob identifiers, observation times and root deployment/license paths are in the structured evidence. No runtime validation is implied.

## Evaluation and telemetry

Trace payloads can contain private source text. Use metadata first and test citation, retrieval and permission behavior separately.

| Project / official source | Purpose | Family / recommendation | Repository release reference | License classification | Boundary / adoption concern |
|---|---|---|---|---|---|
| [Langfuse](https://github.com/langfuse/langfuse) | Model traces, prompt management and evaluation | Stack / **Evaluate** | [v4.78.0](https://github.com/langfuse/langfuse/releases/tag/v4.78.0) | [NOASSERTION; MIT core plus separately licensed enterprise directories](https://github.com/langfuse/langfuse/blob/main/LICENSE) | Traces may contain full private documents and credentials |
| [Arize Phoenix](https://github.com/Arize-ai/phoenix) | AI tracing, evaluation and retrieval debugging | Container / **Evaluate** | [@arizeai/phoenix-cli@1.22.0](https://github.com/Arize-ai/phoenix/releases/tag/%40arizeai/phoenix-cli%401.22.0) | [NOASSERTION; Elastic License 2.0](https://github.com/Arize-ai/phoenix/blob/main/LICENSE) | Review license and tracing/export defaults |
| [MLflow](https://github.com/mlflow/mlflow) | Track experiments, models and evaluation | Container / **Alternative** | [v3.18.0](https://github.com/mlflow/mlflow/releases/tag/v3.18.0) | Apache-2.0 | Protect artifact store and execution/deployment features |
| [Promptfoo](https://github.com/promptfoo/promptfoo) | Prompt, tool and adversarial regression evaluation | Build / **Evaluate** | [0.125.1](https://github.com/promptfoo/promptfoo/releases/tag/0.125.1) | MIT | Synthetic test data first; scanner jobs need bounded network access |
| [Ragas](https://github.com/vibrantlabsai/ragas) | Retrieval and answer evaluation | Library / **Alternative** | [v0.4.3](https://github.com/vibrantlabsai/ragas/releases/tag/v0.4.3) | Apache-2.0 | Judge models can leak evaluation data to providers |
| [DeepEval](https://github.com/confident-ai/deepeval) | LLM application evaluation tests | Library / **Alternative** | [python-v4.2.4](https://github.com/confident-ai/deepeval/releases/tag/python-v4.2.4) | Apache-2.0 | Separate local tooling from optional hosted reporting |
| [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector-contrib) | Receive, filter and route service telemetry | Container / **Evaluate** | [v0.165.1](https://github.com/open-telemetry/opentelemetry-collector-contrib/releases/tag/v0.165.1) | Apache-2.0 | Redact content before export; restrict collector receivers |
| [Prometheus](https://github.com/prometheus/prometheus) | Service metrics and alert inputs | Container / **Evaluate** | [v3.16.0](https://github.com/prometheus/prometheus/releases/tag/v3.16.0) | Apache-2.0 | Metrics endpoints can expose system details |
| [Grafana](https://github.com/grafana/grafana) | Operational dashboards | Container / **Evaluate** | [v13.3.1](https://github.com/grafana/grafana/releases/tag/v13.3.1) | AGPL-3.0 | Datasource credentials and dashboard sharing need restrictions |
| [Loki](https://github.com/grafana/loki) | Centralized service logs | Container / **Alternative** | [v3.7.9](https://github.com/grafana/loki/releases/tag/v3.7.9) | AGPL-3.0 | Log access can reveal private content; define retention |
| [Uptime Kuma](https://github.com/louislam/uptime-kuma) | Simple endpoint health monitoring | Container / **Start** | [2.5.9](https://github.com/louislam/uptime-kuma/releases/tag/2.5.9) | MIT | Monitoring credentials and dashboard need protection |

Source detail, README blob identifiers, observation times and root deployment/license paths are in the structured evidence. No runtime validation is implied.

## Identity and perimeter

VPN, login, authorization and outbound policy are distinct controls. A proxy only enforces egress when alternate routes are blocked.

| Project / official source | Purpose | Family / recommendation | Repository release reference | License classification | Boundary / adoption concern |
|---|---|---|---|---|---|
| [Caddy](https://github.com/caddyserver/caddy) | HTTPS ingress and explicit routing | Container / **Start** | [v2.11.9](https://github.com/caddyserver/caddy/releases/tag/v2.11.9) | Apache-2.0 | Protect admin API and handle certificate trust deliberately |
| [Traefik](https://github.com/traefik/traefik) | Dynamic service routing | Container / **Alternative** | [v3.7.18](https://github.com/traefik/traefik/releases/tag/v3.7.18) | MIT | Discovery providers may require privileged runtime access |
| [Authentik](https://github.com/goauthentik/authentik) | Central identity, SSO and MFA | Stack / **Evaluate** | [version/2026.8.5](https://github.com/goauthentik/authentik/releases/tag/version/2026.8.5) | [NOASSERTION; Mixed core, enterprise and documentation licensing](https://github.com/goauthentik/authentik/blob/main/LICENSE) | Identity service compromise affects all connected applications |
| [Authelia](https://github.com/authelia/authelia) | Authentication gateway and identity services | Container / **Alternative** | [v4.39.28](https://github.com/authelia/authelia/releases/tag/v4.39.28) | Apache-2.0 | Proxy headers and bypass routes need testing |
| [Keycloak](https://github.com/keycloak/keycloak) | Full identity and federation platform | Container / **Alternative** | [26.8.2](https://github.com/keycloak/keycloak/releases/tag/26.8.2) | Apache-2.0 | More configuration and lifecycle work than simple personal login |
| [Tailscale](https://github.com/tailscale/tailscale) | Private network access | Container / **Start** | [v1.104.6](https://github.com/tailscale/tailscale/releases/tag/v1.104.6) | BSD-3-Clause | Hosted coordination by default; access policies remain necessary |
| [Headscale](https://github.com/juanfont/headscale) | Self-hosted Tailscale-compatible coordination | Container / **Alternative** | [v0.29.7](https://github.com/juanfont/headscale/releases/tag/v0.29.7) | BSD-3-Clause | Client compatibility and control-plane availability need verification |
| [WireGuard tools](https://github.com/WireGuard/wireguard-tools) | Self-managed encrypted network tunnels | Host / **Alternative** | No latest-release reference; inspect tags/docs | GPL-2.0 | Kernel/network setup belongs to trusted administrators |
| [Open Policy Agent](https://github.com/open-policy-agent/opa) | External policy decisions for tool and API requests | Container / **Evaluate** | [v1.22.3](https://github.com/open-policy-agent/opa/releases/tag/v1.22.3) | Apache-2.0 | Policies need a trusted enforcement point to have effect |
| [OpenFGA](https://github.com/openfga/openfga) | Relationship-based application authorization | Container / **Evaluate** | [v1.22.1](https://github.com/openfga/openfga/releases/tag/v1.22.1) | Apache-2.0 | Model document/project permissions and test changes |
| [SpiceDB](https://github.com/authzed/spicedb) | Relationship permissions service | Container / **Alternative** | [v1.57.1](https://github.com/authzed/spicedb/releases/tag/v1.57.1) | Apache-2.0 | Application must enforce decisions and handle consistency |
| [Squid](https://github.com/squid-cache/squid) | Controlled outbound HTTP proxy | Container / **Evaluate** | [SQUID_7_8](https://github.com/squid-cache/squid/releases/tag/SQUID_7_8) | GPL-2.0 | Also block direct egress, DNS rebinding and private destinations |
| [Gitleaks](https://github.com/gitleaks/gitleaks) | Detect secrets in repositories and outputs | Build / **Start** | [v8.30.1](https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1) | MIT | Detection complements credential isolation; not complete prevention |

Source detail, README blob identifiers, observation times and root deployment/license paths are in the structured evidence. No runtime validation is implied.

## Isolation and supply chain

Several entries are host runtimes or build tools, not Compose applications. Kernel/device/nested-virtualization support must be demonstrated on the target.

| Project / official source | Purpose | Family / recommendation | Repository release reference | License classification | Boundary / adoption concern |
|---|---|---|---|---|---|
| [gVisor](https://github.com/google/gvisor) | Additional syscall isolation for containers | Runtime / **Evaluate** | [release-20261102.0](https://github.com/google/gvisor/releases/tag/release-20261102.0) | Apache-2.0 | Host runtime component; test browser and workload compatibility |
| [Kata Containers](https://github.com/kata-containers/kata-containers) | VM-backed isolation for container workloads | Runtime / **Later** | [4.3.1](https://github.com/kata-containers/kata-containers/releases/tag/4.3.1) | Apache-2.0 | Inside Proxmox VMs nested virtualization and device support need validation |
| [Firecracker](https://github.com/firecracker-microvm/firecracker) | MicroVM building block for stronger job boundaries | Runtime / **Later** | [v1.18.0](https://github.com/firecracker-microvm/firecracker/releases/tag/v1.18.0) | Apache-2.0 | Needs KVM and a management layer; not a drop-in Compose service |
| [Podman](https://github.com/podman-container-tools/podman) | Rootless-capable OCI container management | Host / **Alternative** | [v6.2.0](https://github.com/podman-container-tools/podman/releases/tag/v6.2.0) | Apache-2.0 | Rootless reduces some risks but is not a separate-kernel boundary |
| [Trivy](https://github.com/aquasecurity/trivy) | Image, dependency, secret and configuration inspection | Build / **Start** | [v0.76.2](https://github.com/aquasecurity/trivy/releases/tag/v0.76.2) | Apache-2.0 | Scan exact pinned artifacts and record accepted exceptions |
| [Syft](https://github.com/anchore/syft) | Generate software bills of materials | Build / **Evaluate** | [v1.57.1](https://github.com/anchore/syft/releases/tag/v1.57.1) | Apache-2.0 | SBOM is inventory, not proof of security |
| [Grype](https://github.com/anchore/grype) | Vulnerability inspection of artifacts and SBOMs | Build / **Alternative** | [v0.121.3](https://github.com/anchore/grype/releases/tag/v0.121.3) | Apache-2.0 | Findings depend on database freshness and package identification |
| [Cosign](https://github.com/sigstore/cosign) | Verify and sign artifact provenance | Build / **Evaluate** | [v3.1.4](https://github.com/sigstore/cosign/releases/tag/v3.1.4) | Apache-2.0 | Verify expected issuer and identity, not just any signature |
| [SOPS](https://github.com/getsops/sops) | Encrypt configuration secrets for version control | Build / **Start** | [v3.13.3](https://github.com/getsops/sops/releases/tag/v3.13.3) | MPL-2.0 | Keep decryption keys separate from repository and agent workspace |
| [OpenBao](https://github.com/openbao/openbao) | Secret storage and credentials service | Container / **Evaluate** | [v2.7.2](https://github.com/openbao/openbao/releases/tag/v2.7.2) | MPL-2.0 | Unseal, backup and disaster-recovery procedures are essential |
| [ClamAV](https://github.com/Cisco-Talos/clamav) | Inspect staged downloads and attachments | Container / **Evaluate** | [clamav-1.5.4](https://github.com/Cisco-Talos/clamav/releases/tag/clamav-1.5.4) | GPL-2.0 | Malware scanning cannot prove a file safe |
| [Falco](https://github.com/falcosecurity/falco) | Runtime behavioral detection for Linux workloads | Host / **Later** | [0.45.2](https://github.com/falcosecurity/falco/releases/tag/0.45.2) | Apache-2.0 | Requires privileged host visibility; detection does not enforce policy |
| [Docker Sandboxes](https://github.com/docker/sbx-releases) | MicroVM environments for coding agents | Runtime / **Evaluate** | [v0.53.0](https://github.com/docker/sbx-releases/releases/tag/v0.53.0) | [NOASSERTION; Proprietary product terms; release repository is not an OSS license](https://github.com/docker/sbx-releases/blob/main/LICENSE) | Validate current supported Linux platform, licensing and nested virtualization |

Source detail, README blob identifiers, observation times and root deployment/license paths are in the structured evidence. No runtime validation is implied.

## Management and backup

Container managers have administrator power. Application-consistent backups and off-host restore evidence complement VM snapshots.

| Project / official source | Purpose | Family / recommendation | Repository release reference | License classification | Boundary / adoption concern |
|---|---|---|---|---|---|
| [Dockge](https://github.com/louislam/dockge) | Manage Docker Compose stacks through a UI | Container / **Start** | [1.5.0](https://github.com/louislam/dockge/releases/tag/1.5.0) | MIT | Docker access grants host control; administrator-only service |
| [Portainer](https://github.com/portainer/portainer) | Manage container environments | Container / **Alternative** | [2.45.3](https://github.com/portainer/portainer/releases/tag/2.45.3) | Zlib | Edition differences and endpoint credentials need review |
| [Komodo](https://github.com/moghtech/komodo) | Manage builds, deployment and multiple servers | Stack / **Evaluate** | [v2.3.4](https://github.com/moghtech/komodo/releases/tag/v2.3.4) | GPL-3.0 | Server agents hold powerful deployment permissions |
| [Homepage](https://github.com/gethomepage/homepage) | Private service directory and status portal | Container / **Evaluate** | [v2.7.0](https://github.com/gethomepage/homepage/releases/tag/v2.7.0) | GPL-3.0 | Use static links first; avoid mounting Docker socket directly |
| [Dozzle](https://github.com/amir20/dozzle) | Container log viewing | Container / **Alternative** | [v11.4.2](https://github.com/amir20/dozzle/releases/tag/v11.4.2) | MIT | Logs and runtime socket access are sensitive |
| [restic](https://github.com/restic/restic) | Encrypted file and backup artifact protection | Build / **Start** | [v0.19.1](https://github.com/restic/restic/releases/tag/v0.19.1) | BSD-2-Clause | Use database-native consistent backups and off-host copies |
| [pgBackRest](https://github.com/pgbackrest/pgbackrest) | PostgreSQL backups and point-in-time recovery | Build / **Evaluate** | [release/2.60.0](https://github.com/pgbackrest/pgbackrest/releases/tag/release/2.60.0) | [NOASSERTION; inspect exact license](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE) | Integrate WAL, storage, retention and restore tests explicitly |
| [Kopia](https://github.com/kopia/kopia) | Encrypted snapshot backups | Container / **Alternative** | [v0.23.1](https://github.com/kopia/kopia/releases/tag/v0.23.1) | Apache-2.0 | Verify restore keys, retention and repository access |
| [Renovate](https://github.com/renovatebot/renovate) | Propose reviewed dependency and image updates | Container / **Evaluate** | [44.231.0](https://github.com/renovatebot/renovate/releases/tag/44.231.0) | AGPL-3.0 | Use narrow repository token; never auto-upgrade stateful services blindly |
| [Harbor](https://github.com/goharbor/harbor) | Private image registry and artifact management | Stack / **Later** | [v2.16.0](https://github.com/goharbor/harbor/releases/tag/v2.16.0) | Apache-2.0 | Large supporting stack; protect signing and registry credentials |
| [Dagu](https://github.com/dagucloud/dagu) | Lightweight workflow and job scheduling | Container / **Alternative** | [v2.26.0](https://github.com/dagucloud/dagu/releases/tag/v2.26.0) | GPL-3.0 | Command runners need scoped files, credentials and outbound access |

Source detail, README blob identifiers, observation times and root deployment/license paths are in the structured evidence. No runtime validation is implied.

## Additional infrastructure outside the container catalog

- [Proxmox VE documentation](https://pve.proxmox.com/pve-docs/): hypervisor, VM lifecycle, networking and storage.
- [Proxmox Backup Server documentation](https://pbs.proxmox.com/docs/): evaluate dedicated backup infrastructure and off-host recovery.
- [Docker Engine security](https://docs.docker.com/engine/security/): runtime and administrator boundaries.
- [MCP security guidance](https://modelcontextprotocol.io/specification/latest/basic/security_best_practices): protocol and identity risks.

No claim is made that all tools interoperate. Choose one component per responsibility, validate CPU/GPU support and permissions, and record actual deployment evidence.
