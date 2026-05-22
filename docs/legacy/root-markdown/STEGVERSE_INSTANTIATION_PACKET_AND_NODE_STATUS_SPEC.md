# StegVerse Instantiation Packet and Node Status Specification

## Status

```text
schema_family: stegverse_instantiation_packet
spec_version: 0.1.0
status: pre-production draft
date: 2026-05-21
related_stage: Stage 27 through Stage 31
primary_work_entity: StegVerse-001 / Beta_Orionis
```

## Purpose

This specification defines the governed packet format, node-status model, FinCo eligibility boundary, discovery database outputs, canonical diff classifications, install-plan rules, iOS-safe path requirements, and revocation requirements for future StegVerse instantiation packets.

The purpose is to prevent the StegVerse core build from becoming an ordinary software installer.

A StegVerse instantiation packet is not merely a compressed set of files.

It is a governed transition candidate.

It must declare:

```text
what is being installed
where it is being installed
who authorized the packet
what scale profile applies
whether node participation is requested
whether FinCo participation is requested
what current state was discovered
what canonical state is expected
what diff was computed
what install plan is proposed
what policies govern the install
what receipts and reports are included
what must fail closed
```

## Core Rule

```text
An install plan is a candidate transition, not installation authority.
```

Discovery may observe, model, compare, classify, and propose.

Discovery may not install.

CGE and ingestion decide whether a proposed install plan may bind.

## Architectural Flow

```text
discovery
  -> discovered-state DB
  -> canonical-state comparison
  -> state diff
  -> install-plan candidate
  -> sandbox
  -> CGE
  -> ingestion
  -> receipts
  -> master-record export
```

The packet is the portable object that carries this proposed transition across environments.

## Scale Profiles

Every instantiation packet must declare a scale profile.

Initial allowed profiles:

```text
personal_core
repo_core
org_core
institution_core
enterprise_core
ecosystem_core
```

### personal_core

Default behavior:

```text
node_participation_opt_in: false
finco_participation_requested: false
public_mirror_enabled: false
master_record_export_enabled: false
external_status_reporting_enabled: false
memory_persistence_enabled: false
action_execution_requires_user_approval: true
```

Personal core builds prioritize user sovereignty, local-first behavior, explicit consent, revocation, and minimal external reporting.

### repo_core

Default behavior:

```text
node_participation_opt_in: false
finco_participation_requested: false
public_mirror_enabled: optional
master_record_export_enabled: optional
ingestion_enabled: true
sandbox_enabled: true
receipt_emission_enabled: true
```

Repo core builds are the first practical target for `core-lite`.

### org_core

Default behavior:

```text
node_participation_opt_in: optional
finco_participation_requested: false
cross_repo_discovery_enabled: true
org_policy_scope_required: true
master_record_export_enabled: optional
```

### institution_core

Default behavior:

```text
node_participation_opt_in: optional
finco_participation_requested: optional_restricted
role_authority_map_required: true
data_classification_required: true
public_private_report_split_required: true
revocation_authority_required: true
incident_response_required: true
```

### enterprise_core

Default behavior:

```text
node_participation_opt_in: optional
finco_participation_requested: optional_restricted
multi_unit_policy_required: true
audit_export_required: true
quorum_or_approval_policy_required: true
```

### ecosystem_core

Default behavior:

```text
node_participation_opt_in: true
node_status_required: true
master_record_export_enabled: true
reconstruction_required: true
revocation_required: true
```

## Core Unit Mode vs Node Mode

Core installation and node participation are separate states.

A target may install a core unit without becoming a StegVerse node.

Safe default:

```json
{
  "core_unit_installed": true,
  "node_participation_opt_in": false,
  "node_status": "NOT_A_NODE",
  "finco_participation_requested": false,
  "finco_participation_allowed": false
}
```

## Node Status Model

Allowed node statuses:

```text
NOT_A_NODE
NODE_PENDING
NODE_ACTIVE
NODE_LIMITED
NODE_SUSPENDED
NODE_REVOKED
NODE_RETIRED
```

### NOT_A_NODE

The target has a core unit but has not opted into StegVerse node participation.

### NODE_PENDING

The target requested node status, but activation is not complete.

### NODE_ACTIVE

The node is active and may participate within its declared policy scope.

### NODE_LIMITED

The node is active but constrained.

This may allow limited routing, limited reporting, or limited FinCo participation.

### NODE_SUSPENDED

The node is temporarily disabled.

No FinCo participation should be admitted.

### NODE_REVOKED

The node status has been revoked.

No network participation is allowed unless reaccredited.

### NODE_RETIRED

The node exited intentionally.

Historical receipts remain valid, but current participation is inactive.

## FinCo Boundary

Node status is necessary for FinCo participation, but not sufficient.

Rules:

```text
Core installation does not imply node participation.
Node participation does not imply FinCo eligibility.
FinCo eligibility requires explicit node status, valid receipts, compensation rules, and revocation rules.
```

Minimum FinCo requirements:

```text
node_participation_opt_in == true
node_status in [NODE_ACTIVE, NODE_LIMITED]
finco_participation_requested == true
consent_receipt_valid == true
access_receipt_valid == true
use_receipt_valid == true
compensation_rule_defined == true
revocation_rule_defined == true
chain_intact == true
```

Fail-closed cases:

```text
FinCo requested but node_status = NOT_A_NODE
FinCo requested but node_status = NODE_PENDING
FinCo requested but node_status = NODE_SUSPENDED
FinCo requested without consent receipt
FinCo requested without access receipt
FinCo requested without use receipt
FinCo requested without compensation rule
FinCo requested without revocation rule
FinCo requested with creates_entitlement = true but no authority
FinCo requested with broken chain
```

## Packet Structure

A future StegVerse instantiation packet should use this conceptual layout:

```text
stegverse-core-instantiation.tar.gz
  manifest/
    instantiation_manifest.json
    authority_boundary.json
    policy_scope.json
    node_status.json
    finco_participation.json
    path_mappings.json

  state/
    discovered_state.json
    canonical_state.json
    state_diff.json
    install_plan_candidate.json

  payload/
    core-lite/
    discovery/
    cge/
    sandbox/
    receipts/
    tvc-interface/
    master-record-export/
    site-mirror-export/

  receipts/
    build_receipt.json
    discovery_receipt.json
    canonical_diff_receipt.json
    install_plan_receipt.json
    node_status_receipt.json
    finco_eligibility_receipt.json

  reports/
    discovery_report.json
    capability_gap_report.md
    install_plan_report.json
    node_status_report.json
    finco_eligibility_report.json
    risk_report.json

  schemas/
    instantiation_manifest.schema.json
    discovered_state.schema.json
    state_diff.schema.json
    install_plan.schema.json
    receipt.schema.json

  iosnoperiod/
    ...

  iosnoperiod.md
```

## Instantiation Manifest

The main manifest should include:

```json
{
  "schema": "stegverse_instantiation_manifest.v0",
  "packet_id": "stegverse-core-instantiation-example",
  "packet_version": "0.1.0",
  "scale_profile": "repo_core",
  "target_unit": "core-lite",
  "target_repo": "Data-Continuation/core-lite",
  "source_canonical_version": "transition-table-v1-rc2",
  "discovered_state_ref": "state/discovered_state.json",
  "canonical_state_ref": "state/canonical_state.json",
  "state_diff_ref": "state/state_diff.json",
  "install_plan_ref": "state/install_plan_candidate.json",
  "node_participation": {
    "node_participation_opt_in": false,
    "node_status": "NOT_A_NODE"
  },
  "finco_participation": {
    "finco_participation_requested": false,
    "finco_participation_allowed": false
  },
  "authority_boundary_ref": "manifest/authority_boundary.json",
  "policy_scope_ref": "manifest/policy_scope.json",
  "path_mappings_ref": "manifest/path_mappings.json"
}
```

## Discovery DB Outputs

Start with JSON.

SQLite, StegDB, and master-record hydration can come later.

Minimum discovery outputs:

```text
state/discovered_state.json
state/canonical_state.json
state/state_diff.json
state/install_plan_candidate.json
reports/discovery_report.json
reports/capability_gap_report.md
receipts/discovery_receipt.json
```

## Discovered State

`discovered_state.json` should include:

```text
target identity
org identity
repo identity
branch
commit hash
file inventory
directory inventory
workflow inventory
schema inventory
task manifest inventory
receipt inventory
report inventory
module inventory
detected capabilities
node status if present
FinCo status if present
unknown files
protected files
hashes
```

## Canonical Diff Categories

Every difference must be classified.

Allowed initial classifications:

```text
present_and_valid
missing_required
present_but_stale
present_but_unknown
extra_but_allowed
extra_requires_review
local_extension
legacy_candidate
conflict
dangerous
quarantine_required
```

Unknown files should not automatically fail.

Suggested treatment:

```text
unknown outside protected paths -> extra_requires_review
unknown inside protected paths -> quarantine_required
unknown with secret-like filename -> quarantine_required
unknown workflow -> REQUIRE_REVIEW or FAIL_CLOSED
unknown receipt/report -> REQUIRE_REVIEW
```

## Install Plan Rules

An install plan must include:

```text
plan_id
target_unit
target_repo
scale_profile
diff_ref
actions
action classifications
required approvals
required receipts
sandbox_required
cge_required
install_allowed_by_plan: false
```

The final field is important.

```json
{
  "install_allowed_by_plan": false
}
```

The install plan does not authorize itself.

## iOS-Safe Path Requirements

Any canonical path with a leading dot must be mirrored under `iosnoperiod/`.

Examples:

```text
.github/workflows/core-lite-self-test.yml
.stegverse/policy.json
```

Mirror examples:

```text
iosnoperiod/github/workflows/core-lite-self-test-yml
iosnoperiod/stegverse/policy-json
```

The packet must include:

```text
iosnoperiod.md
manifest/path_mappings.json
```

The mappings should be explicit:

```json
{
  ".github/workflows/core-lite-self-test.yml": "iosnoperiod/github/workflows/core-lite-self-test-yml",
  ".stegverse/policy.json": "iosnoperiod/stegverse/policy-json"
}
```

## Revocation Requirements

Every node-capable packet must define revocation behavior.

Revocation triggers may include:

```text
authority drift
policy drift
receipt-chain break
sandbox escape
hidden dependency
unauthorized workflow mutation
FinCo chain break
node health failure
incident response event
human review override
```

Production status must remain revocable.

## Required README Phrase

Every discovery, packet, and install-plan README should include:

```text
An install plan is a candidate transition, not installation authority.
```

## Relationship to Stages

Revised tail roadmap:

```text
Stage 27 — Discovery-to-Canonical State DB
Stage 28 — Canonical Diff and Install Plan Candidate
Stage 29 — Optional Node Status and FinCo Eligibility
Stage 30 — Governed Instantiation Packet (*.tar.gz)
Stage 31 — Production Accreditation and Revocation Boundary
```
