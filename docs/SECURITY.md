# Threat model and enforcement limits

## Assets and adversaries

Protect project documents, generated outputs, credentials and the host. Assume a caller can send arbitrary JSON, choose paths and try another project's identifiers. Assume indexed text may contain malicious instructions. A future browser may encounter hostile sites; future generated code may be hostile. Those future workloads require a separate isolation design and are not executed by this demo.

## Implemented controls

| Threat | Enforcement | Evidence |
|---|---|---|
| Caller claims another identity | Tokens map to fixed server-side principals; identity headers ignored | HTTP spoofing test |
| Cross-project retrieval | Authorize project before scoring/filtering documents | Canary text and explicit-denial tests |
| Path traversal | Validate path components, open directories relative to trusted descriptors | Traversal and absolute-path tests |
| Symlink escape | Linux `O_NOFOLLOW` for each path component | Parent, leaf and output-parent symlink tests |
| Unexpected special file | Require regular file and use nonblocking open | FIFO denial test |
| Output overwrite/race | Create temporary file, atomically link only to absent destination | Concurrent-writer and existing-symlink tests |
| Large inputs | Request and file limits; container memory/PID controls | Oversize tests and runtime inspection |
| Credential/content leakage through normal logs | Metadata-only structured audit records | Audit exclusion test |
| Host access | No host mounts or runtime administration endpoints | Runtime mount inspection |

Path controls do not protect against a trusted administrator replacing the configured root or deliberately introducing hard links to sensitive content. The example assumes the root is provisioned by the administrator and the only writer capability is controlled output creation. It does not let an agent invoke a shell inside the service.

## Proposed controls, not yet demonstrated

Browser profiles, URL filtering, redirect and DNS-rebinding defense, IPv6 egress coverage, per-job microVMs, arbitrary-program isolation, Proxmox firewall enforcement, authenticated MCP transport, local model policy and application ACL synchronization are design/roadmap items.

Container administrators can inspect runtime environment credentials. Rootless execution is a separate optional evaluation; `USER 10001` alone is not rootless Docker. Containers share the guest kernel. An internal network does not stop traffic routed through an explicitly attached additional network or another allowed service.

## Reporting and updates

Report issues through the repository's GitHub issue channel using synthetic reproductions and no credentials or personal data. Pinning an image gives reproducibility; it does not make an old image safe indefinitely. Stage updates and rerun application, runtime and restore checks. Catalog licenses and release status must be refreshed independently of application tests.
