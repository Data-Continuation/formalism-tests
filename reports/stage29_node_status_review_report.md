# Stage 29 Node Status and FinCo Eligibility Review

## Core Rule

```text
Core installation does not imply node participation.
Node participation does not imply FinCo eligibility.
FinCo eligibility requires explicit node status, valid receipts, compensation rules, and revocation rules.
```

## Default State

```json
{
  "core_unit_installed": true,
  "node_participation_opt_in": false,
  "node_status": "NOT_A_NODE",
  "finco_participation_requested": false,
  "finco_participation_allowed": false
}
```

## Findings

- Node status is explicit opt-in.
- FinCo eligibility is separate from node status.
- Suspended and revoked nodes fail closed.
- Pending nodes require review.
- FinCo requires consent, access, use, compensation, revocation, and intact-chain evidence.
- Entitlement creation requires explicit entitlement authority.
