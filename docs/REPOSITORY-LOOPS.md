# Local and GitHub repository management loops

Status: required architecture, not implemented integration. Defined November 11, 2026. This extends the [master goal](MASTER-GOAL.md) to include GitHub Desktop on the user's computer, local Git, container workspaces and GitHub.com public/private repositories.

## Roles and authoritative state

GitHub Desktop provides the human-facing local repository view and review/handoff workflow. It is separate from the server containers. Agents perform scoped Git operations in assigned workspaces and use GitHub APIs or the official MCP server for authorized remote operations. Desktop UI automation is optional and must be researched separately; it is not a prerequisite for managing the same repositories through Git.

Git owns commit/branch/worktree state. GitHub owns remote repository identity, visibility, PRs, check results and releases. The project registry stores mappings and observations, not a competing history. Refresh authoritative state before consequential actions. Never interpret a successful local commit as a successful push, or a successful push as passing CI.

| Registry field | Purpose |
|---|---|
| Project/repository ID and owner | Select the correct project independent of display-name changes |
| Verified remote URL and visibility | Prevent wrong-remote pushes and unintended public disclosure |
| Local checkout/worktree and active branch | Map human and agent work to the correct filesystem location |
| Task/agent owner and workspace lease | Prevent competing edits or checkouts in the same directory |
| Base/head commit and last fetch | Detect stale plans, changed branches and concurrent remote work |
| Allowed operations and credential scope | Separate read, branch push, merge, release and administration |
| PR/check/deployment references | Correlate results with exact commits and environments |
| Public/private pairing and export policy | Define approved shared material without implying a mirror |

## Required loops

| Loop | Sequence | Completion evidence |
|---|---|---|
| Onboard | Create/add/clone repository → verify remote and visibility → register project → expose local repository in Desktop as appropriate | Matching local/remote identity and documented access scope |
| Local development | Fetch → choose base → allocate branch/worktree → implement → inspect diff → test → commit → push | Assigned workspace and expected remote branch/head |
| Human handoff | Agent checkpoints and releases workspace → user reviews in Desktop → user commits or returns task → agent refreshes state | Explicit handoff, refreshed head and no concurrent checkout ownership |
| PR delivery | Issue/work order → branch → PR → review → CI on exact revision → authorized merge → development deployment | PR, commit, check and development deployment references |
| Synchronize | Compare local/remote state → fetch → reconcile using project policy → test affected changes → push | Preserved unrelated work and verified remote head |
| Public promotion | Select allowlisted material → remove sensitive content → inspect patch/history/artifacts → publish through authorized public branch/PR → verify public result | Export manifest and reviewed public commit; no private-history mirror |
| Release | Select verified commit → generate release notes/artifacts → verify destination → publish when authorized | Tag, commit, artifact identities and release record |
| Recovery | Preserve dirty work → inspect divergence/reflog/backups → propose recovery → restore selected state → verify | Recoverable work and coherent local/remote state |
| Offline continuation | Record last known remote state → work locally within scope → queue remote actions → reconnect and reconcile before publication | Explicit pending operations; no fabricated remote/CI success |

Use separate worktrees or clones for parallel agent tasks and the user's Desktop checkout. Do not assume GitHub Desktop manages arbitrary server-side worktrees. Local review may use a dedicated clone of the pushed agent branch. Research the selected Desktop version's support before promising a specific UI handoff.

## Skills to specify

| Skill | Output contract |
|---|---|
| `/repo-onboard` | Verified registry entry, access policy and setup/recovery instructions |
| `/repo-sync` | Before/after revision references, reconciliation result and unresolved conflicts |
| `/branch-workspace` | Isolated branch/workspace, owner, base revision and cleanup rule |
| `/pr-review` | Findings tied to exact diff, check status and disposition |
| `/public-promote` | Allowlisted export manifest, privacy/license review and public destination |
| `/release` | Verified commit, release artifacts, change notes and rollback package |
| `/repo-recover` | Preserved work, recovery steps, verification and remaining uncertainty |

Skills describe workflows. Git credentials, repository rules and trusted hook enforcement determine authority.

## Hook and endpoint design requirements

| Proposed hook | Enforcement requirement |
|---|---|
| `workspace.before_acquire` | Confirm repository/project identity and exclusive checkout ownership |
| `git.before_commit` | Inspect intended diff, secret patterns, prohibited paths and required local checks |
| `git.before_push` | Revalidate remote, visibility, branch scope and publication authority |
| `github.pull_request.changed` | Verify webhook signature; deduplicate deliveries; invalidate stale review/check observations |
| `merge.before_execute` | Required reviews/checks apply to the actual proposed revision; respect repository rules |
| `public.before_promote` | Inspect exported content, history and artifacts; block private material outside allowlist |
| `deploy.before_execute` | Verify commit/artifact, assigned development environment and production approval where applicable |
| `repository.after_reconcile` | Record resulting head and rerun affected checks |

Proposed platform capabilities include `repository.inspect`, `workspace.acquire`, `git.diff`, `git.commit`, `git.push_branch`, `pull_request.open`, `checks.read`, `merge.request`, `release.prepare` and `public_export.prepare`. These are design names, not claims about upstream MCP tool names. Discover actual schemas and enabled toolsets from the selected server/version.

Use the [official GitHub MCP server](https://github.com/github/github-mcp-server) where its capabilities fit, plus a constrained local Git adapter. Credential scope must match assigned repositories and operations. Do not provide every agent broad account tokens. Server-side repository controls and trusted services must complement local hooks, which can otherwise be bypassed. Research feature availability for the account's public/private repositories before selecting required protection mechanisms.

Webhook events need signature validation, idempotent processing, bounded retry and reconciliation. Event arrival alone does not prove the current state. Merge/deploy actions need concurrency checks and must invalidate earlier approvals if relevant revisions change.

## Public and private separation

Pair repositories explicitly. Neither repo is an automatic two-way mirror of the other. Review content, commit history, CI logs, release artifacts, screenshots, configuration, datasets and generated files before publication. `.gitignore` does not remove previously committed material. Deleting a secret in a later commit does not make earlier history suitable for publication.

Preserve unrelated local changes and never use force push, destructive reset, history rewriting, repository deletion or visibility changes as routine synchronization fixes. Those actions require specifically applicable authorization. Development merge authority does not automatically authorize publishing previously private material or changing repository administration settings.

## Acceptance and research limits

Demonstrate public and private lifecycle flows, human/agent handoff, two-agent workspace separation, stale-head detection, failed CI preventing an unauthorized merge, duplicate webhook handling, offline reconciliation and private-to-public export with synthetic canary material excluded from files/history/artifacts. Production remains separately approved. Record exact Desktop, Git, MCP and GitHub feature assumptions.

Official starting references: [GitHub Desktop cloning and local/remote repositories](https://docs.github.com/en/desktop/adding-and-cloning-repositories/cloning-and-forking-repositories-from-github-desktop), [GitHub repository mirroring](https://docs.github.com/en/repositories/creating-and-managing-repositories/duplicating-a-repository), [official GitHub MCP server](https://github.com/github/github-mcp-server). Mirroring documentation describes a mechanism; it is not the recommended private-to-public publication workflow here.
