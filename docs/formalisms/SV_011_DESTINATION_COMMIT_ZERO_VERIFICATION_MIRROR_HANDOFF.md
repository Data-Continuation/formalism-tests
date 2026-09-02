# SV-011 Destination Commit-Zero Verification Handoff

## Goal
Verify the real `SV-011/entity` checkout against the already validated deterministic Phase-0 tree.

## Rule
The destination must match the generated commit-zero tree exactly, byte-for-byte, excluding only `.git` metadata.

The verifier fails on:
- missing required files
- additional unexpected files
- byte drift in any required file

This prevents a README template, starter workflow, license, package scaffold, generated helper, or other unreviewed content from silently contaminating the from-scratch experiment.

## Boundary
A PASS proves destination-source equivalence to the validated Phase-0 tree only. It does not establish runtime activation, execution authority, autonomous status, or later-phase completion.
