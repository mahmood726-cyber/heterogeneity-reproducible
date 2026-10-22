# Local preparation runtime blockers

These are sandbox/runtime limitations, not measured failures of the app's numerical validation.

- Node, R/Rscript and PowerShell cannot start in this sandbox, as specified in TASK.md.
  Their verification commands are in RUN_PLAN.cmd for the human-side runner.
- Local Python imports numpy, but importing matplotlib fails with:
  ImportError: DLL load failed while importing _c_internal_utils:
  A dynamic link library (DLL) initialization routine failed.
  No numerical/reference results were generated here. The human run plan has an
  explicit numpy/matplotlib import preflight and requires the documented dependencies.

Preparation-only filesystem tests: 7 passed. App/source and protected-file hash
checks passed. These were preparation-time blockers; the final 2026-10-22
runner completed the numerical and browser validation successfully (RUN_EXIT 0).
See provenance/run_plan-2026-10-22-release.log and RECUT_NOTES.md. No dependency
reinstallation, tolerance changes or expected-value changes were attempted.
