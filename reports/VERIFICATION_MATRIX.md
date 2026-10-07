# Verification matrix

| Phase | Status | Scope / remaining work |
|---|---|---|
| execution | PASS | Recorded verifier evidence in progress.json |
| local_agent | PASS_WITH_LIMITATIONS | Actual API/MCP execution verified independently; native Bionic UI and approval behavior remain MANUAL_REQUIRED. Joe-account shell is not an OS sandbox. |
| resume_engine | PASS | Recorded verifier evidence in progress.json |
| development | PASS | Recorded verifier evidence in progress.json |
| github | MANUAL_REQUIRED | CLI authentication as Helminiak and account API read PASS; dedicated repository unavailable and no Git remote configured. Repository creation/push awaiting separate authorization; write access NOT_TESTED. |
| gpu_llm | PASS_WITH_LIMITATIONS | 16K/32K measured; 48K/64K not tested. Short inference performance only. CLI/SDK allocation registry differs from native REST. Bionic native UI unverified. |
| scientific | PASS | Recorded verifier evidence in progress.json |
| forensics | PASS_WITH_LIMITATIONS | 200K synthetic streaming record verification. Descriptive statistics only. One unexplained Python 3.14 failure retained; controls pass and commissioned forensic interpreter is isolated Python 3.12. |
| mbo | PASS_WITH_LIMITATIONS | Synthetic Java/Python foundation, not a CME decoder. Queue/persistence are reference rules; regimes describe volume imbalance, not trading strategies. Measured 200-order depth, not exchange-scale load. |
| security | PASS_WITH_LIMITATIONS | Heuristic secret scan and scoped type checks; GPU wheel advisory coverage incomplete. No private code uploaded. |
| rag | PASS_WITH_LIMITATIONS | Local synthetic authorized directories; PDF text supported/tested, OCR not included. No personal or external data indexed. |
| end_to_end | BLOCKED | Local integration and CLI authentication pass; GitHub remote writes await authorization, native Bionic UI remains MANUAL_REQUIRED. |

PASS applies only to recorded verifiers. MANUAL_REQUIRED and BLOCKED are unfinished. Raw per-command evidence remains local under evidence/.
