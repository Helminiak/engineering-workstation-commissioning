# Failures, blockers and unverified repairs

## Native Bionic context overflow — BLOCKED

Fresh operatorhello22:38:08local:122973tokens against113152context (excess9821); secondBioniclog22:41:18:122975against113152(excess9823). Old105472 failures are historical. Source: reports/BIONIC_CONTEXT_POST_REBOOT.md/json, evidence/bionic-fresh-context-rejection.json. Regular GUI result and full native assembly NOT_TESTED. Measured largest contributor: Notion47schemas,51547compacttokens; data-source query16284. Templateallcatalogs114825, withoutNotion54952. Synthetic measurements do not establish GUI success or exact native filter/module contribution. No context/plugin/security change made.

Reproduce telemetry only (does NOT submit hello): `python3 scripts/inspect-bionic-context.py` (expectedexit2 until native repair). After operator-authorizedresume, compare new GUIhello timestamps on sameactualmodel and preserve settings before a supported per-session optional-schema experiment. CurrentSDKload12544/oneslot/Q8KV differs from earlier113152/fourslots; no Codexreload, cause/actorunknown. Never claim olderrorusedcurrent12544.

## Interrupted startup-helper/handoff verification — NOT_TESTED

scripts/start-local-agent.sh source removed automaticQ6/32Kreload; ShellCheckpassed. The helper runtime command was aborted by operator before any saved transcript/proof. Both `state/local-agent-handoff-proof-post-reboot.json` and `scratch/local-agent-handoff-proof-post-reboot.json` are absent. No agentprocess/pendingtool remains. On authorizedresume: `scripts/start-local-agent.sh tests/local-agent-handoff-proof-task.txt --transcript state/handoff-proof-NEW-UNUSED-NAME.json --max-turns 8`, independentlyverifyproof and before/afterload. Do not call sourceedit a verifiedruntimefix.

## Missing pytest in default document runtime — scope limit

FreshQwen attempted pytest with workspacePython and encountered no pytest; switched to unittest and independentacceptancepassed. Directcheck `.venv/bin/python -m pytest --version` failed with No module namedpytest; `venvs/quant/bin/python -m pytest --version` passed9.1.1. Bridge tool descriptions now point to quant; no unnecessary install or environmentreplacement. `run_python(runtime="quant")` selects scientific/testingruntime.

## Catalog measurement repair attempts — resolved

First syntax attempt: IndentationError, fixed tupleparentheses. Installed MCP2 client rejected old HTTPheaders/cursorfields; adapted to httpx2 client, params, snakecase next_cursor, and by_alias schema serialization. NestedAttributeError nextCursor identified without rawexceptiondump. SandboxedDNS was unavailable; sandbox transport attempt interrupted; hostread-onlyprobes then passed9providers. Atlassian had no existing OAuth token and was NOT_TESTED; no login/refresh. Cachedfilesystem/Playwright entrypoints used directly, no npxdownload. Full nativeassembly remains unresolved despite successfulcatalog/tokenizermeasurement.

## Sandbox and privilege incidents — scope limits

Sandbox nvidia-smi and lms timedout/failed because hostdevices/processes/network were hidden. Host NVIDIA/API/health passed; no driverrepair. Git .git writes required hostexecution under managedprofile; authorizedstage/commit/pushsucceeded. sudoaptclipboard reached passwordprompt, canceled; now dpkgverifiesinstalled2.2.1-2build1, successfulinstallation/actorunobserved. No pendingprivilegedoperation or approvalprompt. No clipboardread.

## Credential-bearing tool output incidents

One MCPauth metadatafield and one unredactedbackendprocessargument probe emitted credential-bearingdata to tooloutput. Values are not preserved in these handoffs/summaries/Git. Probes corrected to whitelistedmetadata and pid/ppid/comm only. Older transientSDKhandledump incident also exists. Nocredentialrotation/change performed; any remediation requires explicitoperatoraction. Do not repeatprocessargumentdumps or copyrawrequests/logs into Git.

## Historical unresolved forensic anomaly — retained

One Python3.14 streaming KeyError remains unexplained; controls and isolatedPython3.12 passed. Commissionedforensics uses venvs/quantPython3.12. Existingrawfailed evidence and investigation live in commissioning/FAILURES.md and stageledger. Rootcauseunknown; do notclaimresolved or silentlydiscard.

## Integration/report freshness — BLOCKED / NOT_TESTED

Existing end_to_endstageBLOCKED. tests/end_to_end.py and scripts/build_reports.py were updated but fullintegration/reportregeneration NOT executed afterchanges. Oldcompletionreports mayrefer to previousmodelsettings. This handoff and handoff/progress.json are current; after nativefix rerunreviewed integration without overwritingevidence, then refreshreports. OptionalQ6benchmarks48K/64K, PRcreation, merge/deploy were notverified; scopeconstraintsremain.

Additional historical failures/repairs, exact sourceevidence and commands: commissioning/FAILURES.md, commissioning/progress.json, reports/FAILURE_REPORT.md. Preserve originals. No new commissioningstage began after urgentstop.
