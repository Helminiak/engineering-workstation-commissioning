# Qwen3.8-27B — Tooling Matrix & Practical Configuration

_Generated 2026-10-07 from live inspection of this workstation.
Model: `qwen/qwen3.8-27b` (Q4_K_M 16 GB, Q6_K 21 GB, vision mmproj present).
Hardware: 32 cores, 61 GiB RAM, local NVMe. Bionic context cap: 33,280 tokens (≈ model's native 32K window)._

## 1. Tool matrix — what to load, when

### Always on (default state)

| Source | Tools | Why |
|---|---|---|
| Bionic built-ins | file read/write/edit, shell, Python sandbox, web search/extract, side editor, in-app browser | Covers ~90% of daily engineering work; zero config |
| **Local Workbench MCP** (the only enabled MCP) | `run_command`, `run_python` (real venv), `search_web`, `read_web`, **`read_document`** | `read_document` (PDF/DOCX/XLSX/PPTX/CSV) is the only MCP-exclusive capability; venv python for project packages |

### Enable per task, then disable again

| Task | Enable | Notes |
|---|---|---|
| JS-heavy sites, screenshots, form automation | **Playwright Browser** | Plain web tools are enough for static pages — don't enable Playwright for those |
| Coding against a library's current API | **Context7 Docs** | Injects live docs into context; token-hungry, so off by default |
| API-level GitHub work (create PR, comment, issues) | **GitHub** | git CLI already covers clone/commit/push — MCP only for API actions |
| Issue tracking / ticketing work | **Linear** | Only while the task is open |
| Doc writing in Notion | **Notion** | Only while the task is open |
| Error-triage work against Sentry | **Sentry** | Only while the task is open |
| Jira/Confluence work | **Atlassian** | Only while the task is open |
| Cloudflare-specific work | **Cloudflare Docs** | Only while the task is open |
| **Never enable** | **Workspace Files** | Fully redundant with built-ins + Local Workbench |

**Rule of thumb:** every active MCP adds tool schemas to *every* request. With a 33K cap that is real budget. Fewer active tools = more room for actual work. Enable → task → disable.

## 2. Qwen3.8-27B settings

### Quantization choice
| Situation | Use |
|---|---|
| Daily driver (quality) | **Q6_K** (21 GB) — 41 GiB available RAM leaves ~20 GB for KV cache; comfortable |
| Tight memory / speed priority | Q4_K_M (16 GB) |

### Thinking mode (Qwen3 hybrid thinking)
| Mode | When |
|---|---|
| **Thinking ON** | coding, planning, multi-step debugging, agentic tool loops, math/reasoning |
| **Thinking OFF** (`/no_think`) | quick lookups, summarization, chat, simple edits — saves tokens and latency |

### Sampling (Qwen-recommended)
| Setting | Thinking | Non-thinking |
|---|---|---|
| temperature | 0.6 | 0.7 |
| top_p | 0.95 | 0.8 |
| top_k | 20 | 20 |

### Context & output
| Setting | Value | Why |
|---|---|---|
| Context window | **keep 32K (the current 33,280 cap)** | Inside the model's trained window. Stretching to 128K locally on 27B costs huge KV-cache RAM and quality degrades; you already have the compaction + bounded-read workflow instead |
| Max output tokens | 8K–16K (thinking), 2K–4K (non-think) | Thinking needs headroom so reasoning + answer both fit |

### Bionic session toggles (current state = good)
| Toggle | Value | Keep |
|---|---|---|
| web search | on | yes — cheap, built-in |
| exploration subagent | on | yes — offloads file hunting from the main context |
| vision subagent | same model (mmproj installed) | yes |
| browser control | off | enable only when a Playwright task is active |

## 3. Agentic hygiene — the biggest real lever

The 2026-10-07 context-overflow failure (task 22929, 38,297 tokens rejected) was **not** a model or MCP-catalog problem. It was 62 tool results / 139,372 chars accumulated in one long resumed-session turn. Working rules that kept the fresh-session baseline healthy (15,447–31,748 tokens, all accepted):

1. **Bounded reads on state files.** Never read `handoff/progress.json` (25 KB) unbounded — read the section you need or use a jq/python extract. The single largest result in the failed turn was exactly this file.
2. **One turn, one goal.** Don't let a single agentic turn accumulate dozens of tool results. Checkpoint (commit + STATUS update) and start a fresh context when switching subtasks.
3. **Keep state files compact.** `STATUS.md` table + short `progress.json` pointers; details live in `evidence/` files that are read on demand, not kept in context.
4. **Prefer the exploration subagent** for "find X" work — it runs out-of-band and returns only the answer.
5. **Don't increase the context window** to fix prompt bloat; fix the bloat. (Operator directive 2026-10-07.)

## 4. Quick pre-flight checklist for a new agentic task

- [ ] Only Local Workbench MCP enabled? (add Playwright/Context7/GitHub only if the task needs them)
- [ ] Thinking ON for coding/debugging, OFF for chat/lookups?
- [ ] Q6_K loaded (or Q4_K_M under memory pressure)?
- [ ] State files to be read bounded (line range / jq / python slice)?
- [ ] Fresh session for a fresh subtask (don't resume a 30K+ context)?
