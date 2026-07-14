# Denial Reachability Continuation Report

- Status: `PASS`
- Cases: `5`
- Passed: `5`
- Failed: `0`
- Report SHA-256: `8c2c460e3d7ae790a4f5fc347e44f9e91615db8b1913ee98c893e3071a5fb284`

## Results

### REACHABLE_DENY

- Decision: `DENY`
- Failure class: `None`
- Execution prevented: `true`
- Denial controlled execution: `true`

### UNREACHABLE_DENY

- Decision: `FAIL_CLOSED`
- Failure class: `INHERITED_AUTHORIZATION`
- Execution prevented: `true`
- Denial controlled execution: `false`

### COSMETIC_GATING

- Decision: `FAIL_CLOSED`
- Failure class: `COSMETIC_GATING`
- Execution prevented: `true`
- Denial controlled execution: `false`

### LATE_REFUSAL

- Decision: `FAIL_CLOSED`
- Failure class: `LATE_REFUSAL`
- Execution prevented: `false`
- Denial controlled execution: `false`

### SPLIT_BOUNDARY_INSUFFICIENCY

- Decision: `FAIL_CLOSED`
- Failure class: `SPLIT_BOUNDARY_INSUFFICIENCY`
- Execution prevented: `true`
- Denial controlled execution: `false`

## Boundary conclusion

Authorization is valid at the consequence-binding boundary only when denial remains both reachable and enforceable until the decision controls execution.
