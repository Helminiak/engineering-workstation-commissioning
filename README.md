# Engineering Workstation Commissioning

Controlled commissioning record, configuration guidance, and validation tooling for engineering and AI-development workstations.

## Repository purpose

This repository exists to make workstation configuration reproducible and auditable instead of relying on scattered screenshots, chat transcripts, BIOS notes, and one-off local changes.

It is intended for hardware commissioning, stability validation, performance baselining, and configuration-change tracking.

## Intended contents

- Hardware inventory templates
- BIOS/UEFI configuration records
- CPU power-limit and stability-test procedures
- DDR5 configuration and memory-validation procedures
- GPU configuration and validation
- storage/network validation
- operating-system provisioning scripts
- driver/version manifests
- benchmark procedures
- benchmark result templates
- thermal and power validation
- burn-in and acceptance criteria
- known-good configuration records
- rollback notes
- reproducibility checklists

## Relationship to other repositories

This repository documents the **workstation platform**.

Application-specific configuration should remain in the corresponding repository, for example:

- Local LLM runtime/model configuration → `LLM-Setup`
- Network diagnostic application → `NETWORK-DIAGNOSTIC-MONITOR`
- Bookmap market-data exporter → `bookmap-orderflow-exporter`
- Trading entry-model logic → private Orderflow repository

## Engineering principle

Every material configuration change should be attributable to:

```text
requirement or hypothesis
        ↓
configuration change
        ↓
stability/performance test
        ↓
measured result
        ↓
accept / reject / rollback
```

Do not treat a benchmark improvement as valid unless the resulting configuration also meets the required stability and thermal criteria.

## Public-repository hygiene

Do not commit:

- Windows product keys or software license keys
- passwords, tokens, private keys, or credentials
- serial numbers when disclosure is unnecessary
- network credentials
- personal documents
- proprietary binaries that cannot legally be redistributed

Use sanitized inventories and example configuration files where appropriate.

## Agent entrypoints and license

Before making changes, read [AGENTS.md](AGENTS.md), [the multi-LLM workflow](docs/MULTI_LLM_WORKFLOW.md) and the assigned issue. Use an owned task branch, record the full source commit and validate the actual repository state before handoff.

License: not yet selected by this governance bootstrap. Preserve existing copyright and any existing license or UNLICENSED declarations; public visibility is not an open-source license.
