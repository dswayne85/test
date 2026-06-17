# Best Case Agent

A Windows-only Python desktop automation agent for **Best Case** bankruptcy
software, built on [pywinauto](https://pywinauto.readthedocs.io/). It automates
creditor data entry on the same Windows machine where Best Case is installed,
with logging, screenshots, retries, and (later) checkpointed batch processing.

> **Milestone 1 (current): robust window inspection + a single-creditor proof of
> life.** Full batch automation comes only after real selectors are captured.

## Requirements

- Windows 10/11 (pywinauto/pywin32 are Windows-only).
- Python 3.10+ (3.11 recommended).
- Best Case installed and runnable on the same machine.

The package is intentionally importable on non-Windows machines (the Windows-only
dependencies are gated, and pywinauto imports are lazy) so the pure-logic tests
can run in CI. Actual GUI automation only works on Windows.

## Setup (Windows PowerShell)

```powershell
# 1) From the project root, create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Upgrade pip and install the project (editable) with dev tools
python -m pip install --upgrade pip
pip install -e ".[dev]"

# 3) Create your local config from the template and edit as needed
Copy-Item .env.example .env
notepad .env
```

`pywinauto` and `pywin32` install automatically from the standard pip index on
Windows. If `comtypes` warns on first import, re-run the command once.

## First run — what to run on the Best Case machine

**Open Best Case first**, then run the inspection. Try the `uia` backend first;
if the control tree looks empty or opaque, try `win32`.

```powershell
# Connect + list top-level windows (quick sanity check)
python scripts/connect_bestcase.py --backend uia

# Full inspection: window list + control dump + screenshot + summary report
python scripts/inspect_bestcase.py --backend uia
#   ...or, if uia is unhelpful:
python scripts/inspect_bestcase.py --backend win32

# Dump a SPECIFIC window's controls (repeat as you open each dialog)
python scripts/dump_controls.py --title-re ".*Creditor.*" --backend uia
```

Artifacts are written under `output/`:

- `output/logs/`         — timestamped run logs
- `output/screenshots/`  — PNG captures
- `output/reports/`      — control dumps (`*.txt`) and inspection summaries (`*.md`)

### Run the tests

```powershell
pytest
```

## Project layout

```
src/bestcase_agent/
  config.py          # env-driven configuration (paths, backend, timeouts, titles)
  logging_setup.py   # file + console logging
  runner.py          # CLI dispatcher (inspect / add-creditor)
  app/               # waiters, keyboard, screenshots, selectors, connect (lazy pywinauto)
  adapters/          # ALL pywinauto interaction lives here
  screens/           # one class per window/dialog (selectors owned here + app/selectors.py)
  flows/             # inspect_bestcase (real), add_single_creditor (stub w/ TODOs)
  domain/            # pydantic Creditor model + validators + normalizers (pure)
  state/             # session + checkpoints (for resumable batch later)
scripts/             # thin CLI wrappers: connect / inspect / dump_controls
tests/               # smoke (imports, config) + logic (normalizers, validators)
output/              # run artifacts (git-ignored)
```

## How to continue after the first inspection

1. Open the relevant control dump(s) in `output/reports/`.
2. Replace the `TODO_*` placeholders and `title_re` patterns in
   `src/bestcase_agent/app/selectors.py` (and the title regexes in `.env`) with
   the real `auto_id` / `control_type` / `title` values from the dump.
3. Implement the navigation stubs in `screens/main_window.py` and
   `screens/case_window.py` (open case → open creditor section → add creditor).
4. Run the single-creditor flow:
   ```powershell
   python -m bestcase_agent.runner add-creditor tests/fixtures/creditors_small.json --index 0
   ```
5. Once one creditor reliably lands, build the batch executor on top of
   `state/checkpoints.py`.

## Configuration

All settings come from environment variables (optionally a `.env` file). See
`.env.example` for the full list: executable path, backend, process name, window
title regexes, timeouts/retries, output dir, and log level.
