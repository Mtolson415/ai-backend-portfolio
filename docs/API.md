# Reference tool contract

Every `POST /v1/` request requires `Authorization: Bearer <token>` and `Content-Type: application/json`. Credentials map server-side to fixed synthetic identities. Caller-supplied identity headers do not change authorization. Responses include a request ID. Unknown routes return 404; missing/invalid credentials return 401; denied operations return 403.

| Endpoint | Body | Result |
|---|---|---|
| `GET /health` | None | Status only; does not require credentials |
| `POST /v1/knowledge/search` | `{"project":"alpha","query":"recovery"}` | Authorized lexical matches with source citations |
| `POST /v1/files/read` | `{"project":"alpha","path":"notes.txt"}` | UTF-8 contents of a scoped regular file |
| `POST /v1/files/write-output` | `{"project":"alpha","path":"outputs/report.txt","text":"Synthetic report"}` | Create a new output; never overwrite an existing destination |

Alpha's identity may search/read its own project and create new outputs. Beta's identity may search/read only its own project. There is no cross-project administrator token in this example.

Files are limited to 64 KiB and requests to 8 KiB. Unknown questions return an empty match list. Output size is additionally constrained by the HTTP request limit when accessed through the API. Metadata audit records include principal, operation, status, elapsed time and request ID; they exclude credentials, queries, paths and content.

The small API can be wrapped by an MCP server or an agent framework later. Such an adapter is not implemented here. The current service neither invokes a model nor interprets instructions inside retrieved text.
