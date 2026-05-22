# Stage 31 Missing Runner Fix

## Assumptions

1. Stage 31 failed because GitHub Actions found the task manifest but could not find the runner file.
2. The failing command expected this file:

```text
tools/run_stage31_production_accreditation_revocation_tests.py
```

3. The task ID is correct:

```text
stage31_production_accreditation_revocation_tests
```

## Done

This fix is done when the repo contains both:

```text
tools/run_stage31_production_accreditation_revocation_tests.py
tools/tasks/stage31_production_accreditation_tasks.json
```

and this command succeeds:

```bash
python tools/run_declared_tasks.py tools/tasks/stage31_production_accreditation_tasks.json --task-id stage31_production_accreditation_revocation_tests
```

## What happened

The runner executed the declared task, but Python returned:

```text
can't open file ... tools/run_stage31_production_accreditation_revocation_tests.py
```

That means the manifest was present and the task ID resolved, but the script file was missing at the path declared by the task.

## Files included

This fix bundle includes the exact Stage 31 runner and manifest path expected by the declared-task runner.

It also includes the fixture and README/theorem-map update from the Stage 31 bundle so the runner has everything it needs.

## Task ID

```text
stage31_production_accreditation_revocation_tests
```

## Manifest path

```text
tools/tasks/stage31_production_accreditation_tasks.json
```
