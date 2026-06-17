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
