# Verification matrix

| Phase | Status | Scope / remaining work |
|---|---|---|
| execution | PASS | Recorded verifier evidence in progress.json |
| local_agent | PASS_WITH_LIMITATIONS | Historical API/MCP and native engineering acceptance verified. Current Bionic chat usability is separately BLOCKED by request/context mismatch. Joe-account shell is not an OS sandbox. |
| resume_engine | PASS | Recorded verifier evidence in progress.json |
| development | PASS | Recorded verifier evidence in progress.json |
| github | PASS_WITH_LIMITATIONS | Authorized private repository/task branch push and remote commit verified. PR creation, merge and deployment not tested or authorized. |
| gpu_llm | PASS_WITH_LIMITATIONS | Historical Q6_K16K/32K benchmark scope retained. Current operator-loaded Q4_K_M105472/four-slot configuration differs; Bionic request around123K exceeds it. 48K/64K Q6 tests not performed. |
| scientific | PASS | Recorded verifier evidence in progress.json |
| forensics | PASS_WITH_LIMITATIONS | 200K synthetic streaming record verification. Descriptive statistics only. One unexplained Python 3.14 failure retained; controls pass and commissioned forensic interpreter is isolated Python 3.12. |
| mbo | PASS_WITH_LIMITATIONS | Synthetic Java/Python foundation, not a CME decoder. Queue/persistence are reference rules; regimes describe volume imbalance, not trading strategies. Measured 200-order depth, not exchange-scale load. |
| security | PASS_WITH_LIMITATIONS | Heuristic secret scan and scoped type checks; GPU wheel advisory coverage incomplete. No private code uploaded. |
| rag | PASS_WITH_LIMITATIONS | Local synthetic authorized directories; PDF text supported/tested, OCR not included. No personal or external data indexed. |
| end_to_end | BLOCKED | Historical native engineering acceptance PASS verified; current Bionic chat usability separately BLOCKED by context overflow. Other previously tested subsystems and GitHub synchronization remain verified. |
| bionic_native | PASS | Recorded verifier evidence in progress.json |
| bionic_usability | BLOCKED | Current Bionic chat BLOCKED by122973-token request versus105472 context. Base prompt474 and stored message text167 tokens; dynamic overhead remains unattributed. Historical native acceptance PASS preserved; fresh GUI comparison pending. |

PASS applies only to recorded verifiers. MANUAL_REQUIRED and BLOCKED are unfinished. Raw per-command evidence remains local under evidence/.
