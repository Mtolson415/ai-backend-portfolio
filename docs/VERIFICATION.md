# Verification evidence

Recorded November 11, 2026. The local environment used Docker Desktop's Linux engine; Proxmox was not accessed.

## Locally observed

- The test image built from the pinned Python base image.
- **27 tests passed** inside a non-root container with read-only root, no external network, dropped capabilities, no-new-privileges and bounded resources.
- The tests cover file traversal, symlink escapes, special-file denial, size limits, concurrent output creation, scoped writes, retrieval authorization, citations, authentication and metadata-only audit records.
- The catalog generator produced 181 entries in 16 categories with archive and license-review flags. The catalog validator checks evidence identifiers, short source excerpts, HTML data consistency and local documentation links. A minimal DOM harness checks filtering/reset/escaping behavior; visual browser QA has not been performed.

- **19 runtime checks passed** against the running two-service Compose example, including an unpublished internal backend, a loopback-only non-root gateway, actual configuration limits, API behavior and one denied outbound IPv4 connection. [Recorded result](evidence/runtime-smoke.json).
- **Zero known HIGH/CRITICAL findings** were reported for the final two local images by the pinned Trivy scanner at the recorded observation time. [Recorded result](evidence/image-scan.json). Initial image candidates were rejected after findings; the final Python image removes unnecessary pip, and the Nginx image installs a pinned patched library.

Independent GitHub Actions status is available from [the workflow](https://github.com/Mtolson415/ai-backend-portfolio/actions/workflows/verify.yml). Local evidence alone does not establish that an independent run passed.

## Reproducible environment

Python base: `python:3.13-alpine@sha256:1e1f6334529d1fb26a2ef619d7cffb30a7c7d7cc1cc7338ebee283a58d1aeaca`. Pip is removed because this standard-library service does not need a package installer at runtime.

Gateway base: `nginx:stable-alpine@sha256:583b7f2fce1cdb8da5ad5c39ebd3c33b98b87d493190e548bdee1fa8c619c311`. The image pins the patched `libxslt=1.1.43-r4` package. Upstream Nginx uses a [BSD-style license](https://nginx.org/LICENSE).

The GitHub checkout Action is pinned to a verified v6 commit. The application has no third-party Python runtime dependencies. Model weights and full upstream source snapshots are not included.

## What this does not establish

No browser, vector database, graph engine, model integration, MCP adapter, real knowledge ingestion, Supabase migration, cloud deployment or Proxmox compatibility has been tested. The research inventory is not a list of executed containers. One blocked outbound connection is not a complete network bypass assessment. Application tests do not prove protection against a kernel exploit or a malicious administrator.
