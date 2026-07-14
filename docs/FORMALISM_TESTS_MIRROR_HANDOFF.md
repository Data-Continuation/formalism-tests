# Formalism-Tests Mirror Handoff

This file is the source of truth for continuing `Data-Continuation/formalism-tests` work across sessions.

## Current version

```text
0.4.0-gcat-bcat-sketch-lineage-recorded
```

## Current status

```text
MIRROR_HANDOFF_PRESENT
STEGCLAW_EVALUATION_HANDOFF_DECLARED
STEGCLAW_EVALUATION_VALIDATOR_PRESENT
STEGCLAW_EVALUATION_WORKFLOW_COVERED
GCAT_BCAT_SKETCH_LINEAGE_RECORDED
GCAT_BCAT_SKETCH_ORIGIN_UNRESOLVED
LOCAL_ONLY
```

## Source-of-truth documents

```text
docs/FORMALISM_TESTS_MIRROR_HANDOFF.md
docs/STEGCLAW_EVALUATION_HANDOFF.md
docs/evidence/GCAT_BCAT_ADMISSIBILITY_SKETCH_LINEAGE.md
evidence/gcat_bcat_admissibility_sketch_lineage.json
```

## Current managed files

```text
formalism_tests/stegclaw_evaluation_handoff.json
tools/validate_stegclaw_evaluation_handoff.py
docs/STEGCLAW_EVALUATION_HANDOFF.md
github/workflows/stegclaw-evaluation-handoff.yml
docs/evidence/GCAT_BCAT_ADMISSIBILITY_SKETCH_LINEAGE.md
evidence/gcat_bcat_admissibility_sketch_lineage.json
```

Path note: `github/workflows/stegclaw-evaluation-handoff.yml` is displayed without the leading dot. The actual path is `.github/workflows/stegclaw-evaluation-handoff.yml`.

## GCAT/BCAT sketch lineage state

The earliest currently confirmed recoverable evidence is an Apple Photos export from ChatGPT on **2026-03-05 at 10:39 PM**, followed by a second export at **11:18 PM**. These timestamps are recovery/export boundaries only. The physical drawing date, original capture date, first ChatGPT upload, and first discussion remain unresolved.

The human-readable lineage document and machine-readable receipt preserve five recovery identifiers, dimensions, byte lengths, and SHA-256 fingerprints. The image binaries are not yet installed in the repository.

## Remaining lineage work

```text
1. Search historical ChatGPT data for the earliest image or discussion.
2. Preserve the exact conversation timestamp and surrounding text.
3. Recover original image metadata when available.
4. Install original or earliest recovered image binaries under docs/evidence/assets/.
5. Update hashes and chronology without replacing UNKNOWN values with estimates.
```

## Next build candidates

```text
A. Inspect a visible stegclaw-evaluation-handoff artifact and confirm it contains reports/stegclaw_evaluation_handoff.json.
B. Resolve the GCAT/BCAT sketch's first-upload and first-discussion chronology from recoverable historical evidence.
```

## Archival boundary

The lineage facts discovered by the 2026-07-13 session are now durable in this repository. The origin-search task remains open but can continue from these records without requiring the conversation, provided any subsequently recovered image is hashed and attached before claims are updated.
