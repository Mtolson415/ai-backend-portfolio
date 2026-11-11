# AI Backend Engineering

[![Verify synthetic reference tools](https://github.com/Mtolson415/ai-backend-portfolio/actions/workflows/verify.yml/badge.svg)](https://github.com/Mtolson415/ai-backend-portfolio/actions/workflows/verify.yml)

A self-hosted AI workspace design and working reference tools: permission-aware knowledge retrieval, scoped files and container boundaries, with a proposed Proxmox deployment architecture.

**Current evidence:** 181 researched projects across 16 categories; a synthetic reference API; 27 passing containerized tests; 19 passing local runtime checks; zero known HIGH/CRITICAL findings in the final local image scans. Browser automation, local model integration, vector search and Proxmox deployment remain planned. See [verification evidence](docs/VERIFICATION.md) for the exact scope.

## What a reviewer can inspect

| Engineering area | Artifact |
|---|---|
| Research and component selection | [Findings](docs/research/2026-11-11/ANALYSIS.md), [181-project catalog](docs/research/2026-11-11/CATALOG.md), [source evidence](docs/research/2026-11-11/catalog-evidence.json) |
| Architecture and trust boundaries | [Proxmox design](docs/PROXMOX-ARCHITECTURE.md), [threat model](docs/SECURITY.md) |
| Agent-facing tool design | [API contract](docs/API.md), [reference implementation](src/ai_backend/core.py) |
| Meaningful verification | [Permission and API tests](tests/test_tools.py), [CI workflow](.github/workflows/verify.yml) |
| Operational discipline | Pinned base image, non-root runtime, read-only root, narrow volumes, resource limits and [runtime checks](tools/smoke_runtime.py) |
| Honest scope | [Roadmap](docs/ROADMAP.md) separates implemented behavior from proposed integrations |

The retrieval example is an intentionally small **lexical baseline with citations**, not an LLM or vector database. It demonstrates authorization before retrieval and a reproducible tool contract without personal data or model downloads.

## Run the synthetic demo

Requirements: Docker with Linux containers, Docker Compose v2, Python 3.11+ on the client for helper scripts. Docker runs inside a Linux VM when hosted under Proxmox. The Python server itself uses the standard library and Linux descriptor-relative filesystem operations.

```text
python tools/make_demo_env.py
docker compose -p ai-backend-portfolio-demo config --quiet
docker compose -p ai-backend-portfolio-demo up --build --wait --wait-timeout 90
python tools/smoke_runtime.py
docker compose -p ai-backend-portfolio-demo down
```

Expected result: health, authentication, cited retrieval, cross-project denial, traversal denial, scoped output creation and runtime configuration checks pass. The service binds to localhost port 8080. Two generated tokens live in an ignored `.env`; the helper does not print them. No real knowledge source or host directory is mounted.

The tool service has only an internal Compose network; a separate Nginx gateway publishes localhost port 8080. The runtime check attempts one direct outbound IPv4 connection from the tool service and expects failure; it does not establish comprehensive network isolation against every bypass. Named volumes preserve synthetic outputs when the service is stopped.

## Run the tests

```text
docker build --target test -t ai-backend-tests .
docker run --rm --read-only --network none --cap-drop ALL --security-opt no-new-privileges --pids-limit 64 --memory 256m --tmpfs /tmp:rw,noexec,nosuid,size=64m,uid=10001,gid=10001 ai-backend-tests
python tools/verify_catalog.py
```

Expected result: 27 tests pass, including symlink/traversal denials, concurrent output creation, cross-project retrieval filtering, authentication and content-free audit records. CI repeats these and checks the running Compose service on Ubuntu.

## Read and use the research

Open the [Markdown catalog](docs/research/2026-11-11/CATALOG.md), or download [catalog.html](docs/research/2026-11-11/catalog.html) and open it locally for filtering. GitHub displays HTML source rather than hosting the interactive page. The catalog has no external scripts or analytics.

Entries distinguish service containers, multi-service stacks, libraries, extensions, plugins and host runtimes. Release references are dated upstream observations, not tested installation pins. Archived projects are retained as reference and marked against new adoption. Licenses and paid feature boundaries need exact-release review.

## Troubleshooting, recovery and limits

See [the demo guide](docs/DEMO.md) for authentication, ports, volumes and cleanup. Regenerate the catalog with `python tools/build_catalog.py` after an authorized source refresh. Do not resolve access failures by disabling authentication or mounting the Docker socket.

Source notes are baked-in synthetic fixtures. Recover them from Git; persist outputs through the named volumes or export them before removing volumes. The proposed real knowledge platform requires independent database, file and off-host backups.

This reference is a small, synchronous service for local demonstration, not a production multi-tenant service or arbitrary-code sandbox. It has no browser, shell-execution endpoint, Proxmox credentials or Docker administration endpoint. No real Supabase migration or home-lab deployment is claimed.

Original reference code is MIT licensed. Third-party projects in the catalog retain their own licenses; model weights and complete upstream source snapshots are not redistributed.
