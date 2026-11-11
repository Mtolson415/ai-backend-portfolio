# Run, inspect and recover the synthetic demo

## Why this example

The example isolates three functions that a larger AI system needs: cited retrieval, project-scoped file reads and controlled output creation. It uses standard-library Python to keep the dependency surface small and the enforcement logic inspectable. Real retrieval engines, model runtimes and browsers remain separate planned components.

## Setup and expected behavior

Run the commands in the root README. `make_demo_env.py` intentionally refuses to overwrite an existing `.env`. Generate fresh credentials only after removing or securely backing up the old local demo file. Do not commit it. Environment variables are used for local-demo convenience; a real deployment should use protected file-mounted credentials or a secrets service and rotation.

The gateway listens only on host loopback port 8080 and forwards to the unpublished tool service. Both run as UID/GID 10001 with read-only roots, all capabilities dropped, no-new-privileges and bounded resources. The tool service has 64-PID and 256 MiB limits. It receives only two Docker-managed output volumes and a temporary directory, with no host bind mounts. Source fixtures remain read-only through the image/root filesystem.

A local verification found that directly publishing the internal-only service did not expose the expected host endpoint on the tested runtime. The explicit gateway provides the ingress path while leaving the backend on its internal network. This is a local HTTP demo; real remote access needs properly configured HTTPS and identity controls.

The test target contains tests; the runtime target does not. Both use the same pinned Python image digest. Test-only credentials are plainly labeled synthetic constants and never belong in a real deployment.

## Troubleshooting

| Symptom | Check |
|---|---|
| Environment helper reports file exists | Keep the existing local demo credentials or deliberately rotate them; do not print the file in shared logs |
| Port 8080 already used | Stop the conflicting service or update the loopback port and helper together |
| Startup rejects credentials | Two distinct ASCII tokens of at least 32 characters are required |
| File operation returns 403 | Confirm token project/capability and path; traversal and symlinks are intentionally denied |
| Output returns 409 | Choose a new filename; the API intentionally does not overwrite outputs |
| Container reports read-only filesystem | Only the assigned output volumes and `/tmp` are writable |
| Retrieval returns no matches | This is a lexical baseline; use a term present in the synthetic fixture |
| Compose helper cannot reach the service | Check container health, host port binding and the runtime's network implementation |
| Native Windows tests fail on filesystem flags | Run the Linux container tests; native Windows is not the server target |

Do not print unrestricted `docker inspect` or rendered Compose configuration in public logs: environment values include demo credentials. The runtime helper prints only selected nonsensitive assertions.

## Stop and recover

`docker compose -p ai-backend-portfolio-demo down` stops the demo while retaining named output volumes. Rebuilding from Git restores the original synthetic sources. Export any desired generated outputs before using `down --volumes`, which removes this demo's output volumes. Keep cleanup scoped to the named Compose project; do not prune unrelated containers or volumes.

## Limits

No arbitrary program execution, browser, model, vector database, MCP adapter or production reverse proxy is included. The internal Docker network and one outbound probe are limited evidence, not a comprehensive firewall certification. The HTTP server is a small local demonstration and lacks production rate limiting, TLS, credential rotation, distributed authorization and durable audit storage.
