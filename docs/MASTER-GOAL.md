# Master goal

Defined November 11, 2026 from the user's stated requirements and decisions. This is the intended outcome and research brief, not a claim of delivered capability. It supersedes the earlier narrow interpretation of the platform as a retrieval service with isolated tools.

## Goal statement

Design and build a professional, self-hosted, local-first agent engineering platform on Proxmox that can manage AI agents and coordinate the complete delivery of substantial full-stack software, AI and cloud projects. The platform must connect durable agent management, reusable skills, lifecycle hooks, scoped MCP servers, project knowledge and code intelligence, isolated execution environments, model routing, governance, evaluation and CI/CD into an auditable operating system for engineering work.

Agents should be able to implement, test, merge and deploy within explicitly assigned development environments. Production changes require human approval. Local agents and a self-hosted interface are the starting point; cloud models are optional escalations constrained by explicit spending and data-access rules.

This platform must provide the practical engineering foundation for building UltiStack and progressively realizing the software and governance capabilities envisioned for Sovereign DIOS. Those projects are major intended workloads, not prerequisites that delay a usable engineering platform. Architectural support does not establish AGI, consciousness, infallible governance or completion of the long-term vision.

## Immediate priority

Define the complete operating architecture before expanding the prototype. The architecture must explain how professional engineering work moves through the system, which component owns each decision and state transition, how failures and interruptions are handled, and which controls are enforced outside the model.

The existing 181-project catalog and synthetic reference API are inputs. They are not a substitute for the platform architecture, agent lifecycle or end-to-end delivery workflow.

## Required capabilities

| Domain | Required behavior |
|---|---|
| Command center | Self-hosted interface for projects, work orders, agents, progress, tool activity, approvals, costs, outputs and intervention |
| Agent management | Versioned agent definitions; roles; task assignment; scoped delegation; concurrency limits; spawn/pause/resume/cancel/retire; health, budgets and failure escalation |
| Durable work | Persistent work orders, dependencies, checkpoints, ownership, leases, cancellation propagation, bounded retries, idempotent side effects and restart recovery |
| Skills | Versioned, discoverable and tested workflows with declared inputs, outputs, required capabilities, completion checks and rollback guidance |
| Hooks | Defined lifecycle events and handlers with schemas, ordering, blocking versus advisory behavior, timeouts, failure policy, audit records and bypass protection |
| MCP and tools | Maintained upstream servers where suitable; scoped identities; tool discovery; per-project authorization; credential isolation; revocation; request correlation; custom adapters where necessary |
| Project workspaces | Isolated repository checkouts/worktrees, files, browser sessions, programs, dependencies, datasets, secrets, databases and development deployments |
| Knowledge and memory | Obsidian/document retrieval, source citations, project decisions, code structure and dependency context, task state, temporal facts, provenance, permission propagation, correction and deletion |
| Model routing | Local inference first; task/model matching; context budgets; fallback policy; cloud escalation within explicit provider, spend and data limits |
| Engineering delivery | Requirements, architecture, frontend/backend/APIs/data/auth, implementation, code review, unit/integration/browser tests, security checks, artifacts, infrastructure as code, development deployment and production handoff |
| Repository management | Local Git and GitHub Desktop plus GitHub.com public/private repositories; create/add/clone, repository registration, branch/worktree ownership, synchronization, issues, PRs, CI, merge, releases, recovery and controlled public promotion |
| Governance | Human ownership, permission boundaries, production approval, secret handling, scoped external effects, emergency stop, credential revocation and recovery |
| Evaluation and improvement | Task and agent results, retrieval/citation quality, costs, failures, regression suites and proposed skill/prompt/tool changes tested before controlled promotion |
| Operations | Proxmox placement, container management, observability, resource allocation, image/version management, application-consistent backups, restore and portable rebuild |
| Public evidence | Reproducible synthetic demonstrations, architecture decisions, source references, CI evidence and clear separation of researched, implemented, tested and deployed claims |

## Concrete workflow requirements

Initial skill designs must cover research, architecture, implementation, debugging, code review, security review, cloud review, QA, cost review, release, handoff, learning and postmortems. They are workflow contracts, not permission grants.

Initial hooks must cover task admission, agent assignment, context assembly, model routing, tool calls, workspace changes, test completion, merge, development deployment, production promotion, memory writes, failures, budget exhaustion and task completion. Enforcement hooks run in trusted services that the executing agent cannot rewrite or bypass.

MCP designs must cover scoped filesystem operations, Git/repository hosting, browser/search, current technical documentation, authorized SQL/data queries, vector/graph retrieval, code intelligence, CI/artifacts and approved cloud-development operations. Administrator functions such as Proxmox and Docker management stay on a separate control path; ordinary agents request bounded jobs instead of receiving general infrastructure credentials.

A specialist agent, an MCP tool, a hook and a container are different abstractions. They need not each become a separate service. Deployment boundaries should follow security, lifecycle, resource and recovery needs. Each selected component must have an identified owner and an explicit contract.

### Local and GitHub.com repository loops

GitHub Desktop is the local human review and repository-management interface. Agents use scoped Git operations and GitHub APIs/MCP tools in isolated workspaces. Both must participate in the same recorded project lifecycle without concurrent ownership of the same checkout. Desktop is not assumed to run in the Linux server containers.

Support public and private repositories independently and as explicitly paired projects. Track repository identity, local checkout/worktree, remote, visibility, branch, owning task/agent, allowed operations and current synchronization/CI state. Include local-only/offline work, creation or cloning, fetch/pull/reconciliation, commits, pushes, issues, pull requests, review, authorized merge, development deployment, release and recovery.

Add `/repo-onboard`, `/repo-sync`, `/branch-workspace`, `/pr-review`, `/repo-recover` and `/public-promote` skills. Hooks must check remote identity and visibility before push, workspace ownership before edits, source freshness before merge, exact-commit CI before merge/deployment and content/history/artifact suitability before public promotion. Private-to-public promotion uses reviewed allowlisted exports or patches, never automatic whole-history mirroring. Visibility changes and publication require authorization applicable to the specific action.

See [repository management loops](REPOSITORY-LOOPS.md) for the required contracts, handoffs and acceptance scenarios. These are architecture requirements, not claims of installed GitHub Desktop integration.

## Research method

Begin with a dedicated deep-research phase focused on actively maintained implementations and demonstrably successful engineering loops. Inspect official code, configuration, skills, hooks, tool schemas, deployment examples, tests, CI, issues, release history and licenses. Distinguish independent operational evidence from vendor claims, demos and popularity.

Prefer established workflows and components already demonstrated together. Record exact versions and sources, compatibility constraints, local-model support, hardware requirements, maintenance burden, paid/cloud dependencies, permissions, recovery behavior and reasons for rejecting alternatives. A current source check is necessary before final selection.

There is no mandatory standalone integration-experiment phase. Research informs architecture selection directly. Where compatibility is undocumented, record the uncertainty rather than inventing proof. Verify the chosen assembly during implementation; upstream success does not prove the local deployment works.

## Architecture deliverables

1. Requirements and decision register, including explicit autonomy and budget boundaries.
2. Deep-research report with workflow comparisons, evidence quality, recommendation and alternatives.
3. Logical service and agent architecture with responsibilities and owned state.
4. End-to-end task, delegation, tool-call, hook, review, delivery and recovery sequence diagrams.
5. Agent, skill, hook, capability and MCP endpoint catalogs with versioned contracts.
6. Knowledge, code-intelligence, memory, event and artifact data models with permission and retention rules.
7. Proxmox/container/network/storage/identity placement, including administration and execution boundaries.
8. Model, context, concurrency and cloud-cost policies with resource estimates based on current inventory.
9. Threat model, failure modes, emergency stop, backup/restore and upgrade strategy.
10. Prioritized implementation roadmap, acceptance criteria and public engineering evidence plan.

## Demonstration of success

The implemented platform must demonstrate the following on an explicitly scoped project rather than only through component health checks:

- Accept a substantial engineering brief and preserve its requirements, plan, ownership and acceptance criteria.
- Coordinate appropriate specialist roles with bounded delegation and isolated workspaces; prevent conflicting edits and cross-project access.
- Retrieve relevant code and project knowledge, select versioned skills and use authorized MCP tools with traceable identities.
- Build and test a full-stack application with documented frontend, backend/API, data/auth and an AI or cloud integration appropriate to the project.
- Review, merge and deploy the project to its assigned isolated development environment without requiring approval for every routine step.
- Stop at the production boundary and produce a concrete release/rollback package for human approval.
- Resume interrupted work without silently duplicating external side effects; support cancellation and revoke effective tool authority.
- Enforce model/data/spend limits and demonstrate denied actions as well as successful ones.
- Preserve useful project memory, citations, artifacts, costs, decisions and results with correction/deletion behavior.
- Restore required state and publish a reproducible synthetic evidence package with honest limitations.
- Demonstrate the local GitHub Desktop/Git/GitHub.com lifecycle for public and private repositories, including concurrent-user/agent handoff, synchronization conflict recovery, exact-commit PR/CI checks and a reviewed private-to-public promotion that excludes private history and operational artifacts.

Architecture readiness is a separate milestone: every deliverable above must identify ownership, interfaces, failure behavior, decisions and unresolved dependencies. It must be sufficiently concrete to implement without redesigning the core agent-management and delivery loop.

## Scope and boundaries

This is an architecture-first engineering platform, not a mandate to install every catalog candidate or create a microservice for every idea. Private operational data stays private; public demonstrations use synthetic data. Autonomy applies to designated repositories and development environments, not all existing projects, shared infrastructure or production.

Later sensing, continuous capture, robotics, simulated societies and speculative cognitive research require separate requirements and authorization. The foundation should be extensible to those workloads without claiming they already exist. Improvement loops may propose changes; they may not silently expand permissions or rewrite governing controls.

## Decisions already made and items still to resolve

Confirmed: self-hosted interface and local agents first; autonomous implement/test/merge/development deployment within assigned scope; human production approval; local-first models with budgeted cloud escalation; Proxmox target; deep research using successful upstream patterns; no separate experimental phase as a prerequisite; private planning and public engineering evidence.

Still to resolve through inventory/research: current Proxmox capacity, model/hardware suitability, initial agent framework, interface and gateway, first full-stack demonstration project, numeric resource/spend limits, provider/data permissions, recovery objectives and exact component versions. These are recorded decisions to make, not reasons to shrink the master goal.
