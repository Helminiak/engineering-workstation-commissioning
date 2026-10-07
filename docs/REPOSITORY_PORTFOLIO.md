# Repository Portfolio

This document records the intended GitHub repository boundaries for the current engineering projects. It exists to prevent future ambiguity about where new files belong.

## Repository inventory

| Repository | Desired visibility | Role |
|---|---|---|
| `NETWORK-DIAGNOSTIC-MONITOR` | Public | Windows network diagnostics, release engineering, and the portability boundary toward Asuswrt-Merlin. |
| `LimaCharlieAero` | Public | Public website source, build/validation tooling, SEO/accessibility controls, and release artifacts. |
| `bookmap-orderflow-exporter` | Public | Bookmap historical/live market-data decoding, normalization, raw-event export, and deterministic validation. |
| `LLM-Setup` | Public | Reproducible local-LLM runtime configuration, installation, interoperability, and model-performance testing. |
| `engineering-workstation-commissioning` | Public | Workstation commissioning, BIOS/hardware configuration, stability validation, and acceptance records. |
| `orderflow-entry-engine` | **Private** | Proprietary Orderflow research, feature engineering, model evaluation, and hard-right-edge entry-quality system. |
| `asus-merlin-network-tools` | Public | Router-native network diagnostics and operational tooling if/when the Merlin implementation deserves an independent lifecycle. |
| `lca-maintenance-tools` | Public | Generic, reusable Rotax/LSA maintenance calculators, inspection templates, validation helpers, and public-safe tooling. |
| `pc-performance-lab` | Public | Reproducible CPU/GPU/RAM performance experiments, overclocking/undervolting records, benchmarks, and stability methodology. |
| `goldencheetah-tools` | Public | GoldenCheetah automation, analysis scripts, exported configuration helpers, and reusable endurance-data tooling. |

## Source-control rule

A Git commit identifies the controlled working state.

ZIP files are release, transfer, or archival artifacts only. They are not authoritative working copies once their source is under Git.

## Repository boundary rule

Code, configuration, schemas, tests, documentation, and small sanitized fixtures belong in Git.

Large generated datasets, credentials, customer records, private evidence, licensed binaries, model weights, and other sensitive or non-reproducible material generally do not.

## Private Orderflow boundary

The public `bookmap-orderflow-exporter` repository should stop at deterministic market-event capture and normalization.

The private `orderflow-entry-engine` repository will own proprietary downstream logic such as research features, entry-event labeling, model evaluation, scoring, and other strategy-specific implementation.

Bulk BMF/NDJSON/CSV/Parquet data should remain outside normal Git even when used by the private repository. Store dataset manifests, hashes, schemas, and generation code in Git instead.

## Future-agent handoff rule

When asking ChatGPT, Codex, or another agent to continue a repository task, identify at minimum:

```text
repository
branch
commit SHA
issue / PR if applicable
current objective
acceptance criteria
```

This should replace ambiguous references such as "the latest ZIP" or "the version from the other chat."
