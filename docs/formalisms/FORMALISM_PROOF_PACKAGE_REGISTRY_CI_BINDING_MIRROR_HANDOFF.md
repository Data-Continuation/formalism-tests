# Formalism Proof-Package Registry CI-Binding Mirror Handoff

## Scope

This handoff governs issue #7 in `Data-Continuation/formalism-tests`.

Issue #7 exists only to bind the already-declared proof-package registry validation task into an existing repository-owned CI or workflow surface. It does not own canonical execution for any proof package.

## Existing declared task

```bash
python tools/run_declared_tasks.py tools/tasks/formalism_proof_package_registry_tasks.json --task-id check_formalism_proof_package_registry
```

Expected output:

```text
reports/formalism_proof_package_registry_verification.json
```

## Installed CI-binding surfaces

```text
status/formalism_proof_package_registry_ci_binding.pending.json
schemas/formalism_proof_package_registry_ci_binding.schema.json
tools/check_formalism_proof_package_registry_ci_binding.py
tools/tasks/formalism_proof_package_registry_ci_binding_tasks.json
docs/formalisms/FORMALISM_PROOF_PACKAGE_REGISTRY_CI_BINDING_MIRROR_HANDOFF.md
```

The pending record must retain the exact Schema and handoff references. The checker must fail closed when either reference is missing, substituted, or points to a missing file.

## Current bounded state

```text
status: PENDING_EXISTING_WORKFLOW_BINDING
workflow path: not identified
workflow run id: not observed
job id: not observed
commit SHA: not recorded
report SHA-256: not recorded
binding verified: false
canonical execution claimed: false
promotion eligible: false
authority posture: REGISTRY_CONSISTENCY_ONLY
```

No absence claim may be inferred from missing connector-visible workflow records. No new workflow may be created merely because an existing workflow was not discoverable through code search or guessed file paths.

## Required completion sequence

1. Inspect the repository-owned workflow inventory using an execution surface that can enumerate `.github/workflows/` reliably.
2. Select the existing workflow that already owns declared-task, proof, validation, or repository-integrity execution.
3. Add the existing registry command to that workflow without creating a competing registry-validation workflow.
4. Execute the workflow on a durable commit.
5. Confirm the registry report contains:

```text
status: PASS
package_count: 4
active_issue_count: 4
release_state: NOT_AUTHORIZED
errors: []
```

6. Record the exact workflow path, positive run id, positive job id, 40-character commit SHA, and report SHA-256 in the CI-binding record.
7. Change the record to `VERIFIED_EXISTING_WORKFLOW_BINDING` only after all evidence is present.
8. Run:

```bash
python tools/run_declared_tasks.py tools/tasks/formalism_proof_package_registry_ci_binding_tasks.json --task-id check_formalism_proof_package_registry_ci_binding
```

## Authority boundary

Registry validation is inventory-consistency evidence only.

It does not satisfy or close:

```text
issue #3 denial-reachability canonical execution
issue #4 FI continuity interoperability canonical execution
issue #5 Morrison Runtime commit-time scope canonical execution
issue #6 optimization-target commit-boundary canonical execution
```

It grants no execution, installation, production, release, publication, certification, financial, sovereign, or downstream mutation authority.

## Parallel-safe work

While workflow inventory remains unavailable, safe work is limited to:

```text
maintaining exact Schema, handoff, task, and output references
preserving fail-closed pending state
verifying the CI-binding checker and manifest remain synchronized
recording newly exposed repository-owned workflow evidence
preventing duplicate workflow creation
```

## Promotion prohibition

Documentation, issue comments, connector searches, empty status records, guessed workflow paths, and the existence of a declared task are not evidence of CI binding.
