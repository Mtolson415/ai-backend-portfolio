# Implementation roadmap and acceptance gates

This is a proposed sequence, not evidence of completed deployment.

| Stage | Deliverable | Expected result | Evidence required |
|---|---|---|---|
| 0 | Source and architecture research | Reproducible candidate inventory | Dated metadata, official links, license caveats |
| 1 | Synthetic tool-service example | Scoped files, cited retrieval and policy decisions | Reproducible tests with denied operations and authenticated API checks |
| 2 | Proxmox inventory and guest plan | Workload placement fits available resources | Current host version, CPU/RAM/storage/network inventory and rollback plan |
| 3 | Persistent knowledge pilot | Read-only source indexing and cited answers | Rename/update/delete tests; permission-aware retrieval; backup restore |
| 4 | Isolated browser pilot | Research and downloads stay inside job boundary | Authentication, private-address denial, redirects, output and timeout tests |
| 5 | Program execution pilot | Synthetic analysis runs within assigned resources | Non-root, mount, process, memory, network and cleanup checks |
| 6 | Gateway and capability discovery | Only allowed tools available per task | Caller identity, downstream authorization and audit correlation |
| 7 | Supabase staging migration if needed | App works against restored isolated instance | Rows, objects, auth flows, RLS, functions, external settings and rollback |
| 8 | Optional graph and memory | Better results on defined relationship questions | Baseline comparison, provenance, dated facts, deletion and correction |
| 9 | Public portfolio demonstration | Reviewer can reproduce supported claims | CI logs, release manifest, synthetic examples and explicit limits |

## Knowledge acceptance

Prepare 30–50 synthetic questions spanning exact IDs, paraphrases, cross-document questions, restricted documents, stale versions and unknown answers. Measure retrieval success, citation correctness, unauthorized disclosure, freshness and latency separately. Model-judged scores alone are insufficient. Reindex after an embedding-model change; preserve a versioned manifest and an old index until rollback is no longer needed.

## Perimeter acceptance

Test both allowed and denied behavior. Include traversal and symlink escapes, cross-project files, direct database access, management subnet access, IPv4/IPv6 bypasses, private/link-local destinations, redirect chains, oversized content, zip bombs, process/time limits, shell output limits, forged identity, tool metadata changes and malicious instructions in retrieved content. Record the enforcement layer for each assertion.

## Portfolio acceptance

The public repository must distinguish unit-tested application policy from demonstrated OS isolation. A simulated denied network decision does not prove an actual network packet was blocked. A successful container test does not prove Proxmox compatibility or safe browsing of hostile sites. Publish only evidence that exists; retain these limits even when CI is green.
