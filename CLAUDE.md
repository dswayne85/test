# Best Case Agent

## Purpose
Build a Windows-only Python desktop automation agent for Best Case using pywinauto.

## Current milestone
Milestone 1 = inspection and single-creditor proof of life.
Do not attempt full batch automation until inspection artifacts exist.

## Rules
- Prefer pywinauto selectors over coordinates.
- Support both uia and win32 backends.
- Keep pywinauto calls inside adapter/screen classes.
- Save screenshots and reports for every inspection step.
- Use explicit waits and retry wrappers.
- Favor maintainability over shortcuts.
- Never bury selectors across multiple files.
- Add TODOs where Best Case-specific control names are still unknown.

## Repo priorities
1. Stable attach/connect.
2. Good logs and screenshots.
3. Control discovery.
4. Single-creditor entry.
5. Batch queue processing.

## Output discipline
All run artifacts go to output/.
All code should be type hinted where practical.
All business data models should be structured and validated.

## Coding conventions
- Python, src/ layout, package name `bestcase_agent`.
- Type hints everywhere practical.
- Use pathlib, not raw string paths.
- Use pydantic v2 models for structured/validated business data.
- Keep modules small and single-purpose; no monolithic scripts.
- All pywinauto/pywin32 imports are LAZY (inside functions/methods) so the
  package imports and the pure-logic tests run on any OS, including CI.
- Wrap every external interaction with clear, actionable error messages.
- Save artifacts with timestamps; never overwrite a prior run blindly.
- Prefer explicit waiters/retries (app/waiters.py) over blind time.sleep.

## Milestone plan
- Milestone 1 (CURRENT): inspection + single-creditor proof of life.
  1. Connect reliably to a running Best Case instance (both backends).
  2. Produce good logs, screenshots, and a control dump in output/reports/.
  3. Use the dump to fill in real selectors in app/selectors.py and screens/.
  4. Wire the single-creditor flow (flows/add_single_creditor.py).
- Milestone 2: batch queue processing driven by JSON jobs + checkpointing.
  Do NOT build the batch executor until the single-entry path works.

## Where things live
- Selectors: app/selectors.py + screens/*.py ONLY. Never bury them elsewhere.
- pywinauto calls: adapters/ and screens/ ONLY.
- Domain data: domain/models.py (model), validators.py, normalizers.py.
- Entry points: flows/ (logic) and scripts/ (thin CLI wrappers).
