# Verification status

## v2: full public API, 13 October 2026

- Operations: 152 actions in 22 tool groups, generated from every endpoint in `developer.systeme.io/llms.txt` by `scripts/build_operations.py`. Deprecated `PUT /api/mailing/newsletters/{id}` and `PUT /api/payment/coupons/{id}` are excluded; their `PATCH` versions are included.
- All v1 tool and action names are kept.
- Docker image: `mcp-systeme-extra:v2` built successfully.
- 20 automated tests passed (`python test_server.py`): valid previews for all 152 operations, write gate, read-only POST without confirm, high-impact write blocked, compact and detailed help, deep schema references and mocked HTTP behaviour.
- Gateway smoke test (`tests/gateway_smoke.py`): 22 tools, 152 operations and a write preview; no API requests sent.
- Live read-only checks (`tests/live_read_checks.py`, 30 GET actions plus a subscription list): 28 returned HTTP 200 across all groups; SMS services, numbers and Twilio account returned the documented 424 / 424 / 404 because Twilio is not connected. The user's own public API key was used via Docker secrets. No writes performed.
- Note: the official MCP key does not work here; this server needs a key from **Public API keys** (Systeme.io replies "Invalid API Key." otherwise).
- Direct Python route: a clean `git archive` copy installed into a new venv from `requirements-lock.txt` (Python 3.11.9); a stdio client listed 22 tools and a write preview passed.
- `AGENTS.md` added so an assistant given the repo link can install either route.
- Live writes: not performed.
- GitHub publication: not performed.

## v1: six companion groups, 6 October 2026


- Docker image: `mcp-systeme-extra:v1` built successfully.
- Docker custom catalog: `systeme-extra` registered and enabled.
- 15 automated tests passed, including valid previews for all 20 operations, mocked HTTP behavior and the documented missing-Twilio error responses.
- Gateway tool discovery: six tools found.
- End-to-end Gateway client: all six help calls and a course enrolment preview passed; no API requests sent.
- Source documentation and portrait repository infographic included.
- Live read-only Gateway checks: enrolments, communities, memberships and webhooks returned HTTP 200.
- SMS services and numbers returned HTTP 424; Twilio account returned HTTP 404. The official endpoint definitions explicitly describe all three responses as "The Twilio integration is not configured". Browser inspection confirmed the unconnected Twilio setup form. Requests match the documented GET methods, paths and empty parameter sets. Successful SMS responses remain untested until Twilio is connected.
- Subscription listing was skipped because no contact identifier was returned by the tested collections. Custom-field and other write operations remain validated locally only; no account data writes were performed.
- A temporary API key was created with user confirmation, used through Docker secrets, then deleted from Systeme.io. The empty key list was verified. Its Docker secret was also removed and absence verified. There is no retained working credential.
- GitHub publication: not performed.

Source location: `C:/Users/jovin/MCP/systeme-extra-mcp`.
The existing official connector remains unchanged.

## Documentation verification

- Expanded README: all 20 actions, use cases, required inputs, endpoint map, limitations and troubleshooting.
- Claude Desktop/Code, Codex, Antigravity and Cursor connection formats checked against their official documentation; in-app compatibility is not claimed as tested for every client.
- All 20 copyable operation inputs validated against the server's endpoint schemas; client JSON/TOML examples and README local links validated.
- Dedicated repository catalog accepted by Gateway: six tools, all help calls and enrolment preview passed without credentials or API requests.
- 15 automated tests passed again after the portable smoke-test change.
