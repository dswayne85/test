"""Milestone 1 single-creditor entry flow (STUB).

The control logic and structure are real; the Best Case-specific navigation
steps are guarded with TODO/NotImplementedError until the inspection dump tells
us the actual selectors. Wire main_window/case_window navigation first, then the
creditor dialog (which is already mapped to placeholder selectors).
"""

from __future__ import annotations

from pathlib import Path

from ..adapters.bestcase_adapter import BestCaseAdapter
from ..app.screenshots import capture
from ..app.waiters import retry
from ..config import AppConfig
from ..domain.models import Creditor
from ..logging_setup import get_logger, setup_logging
from ..screens.case_window import CaseWindow
from ..screens.creditor_dialog import CreditorDialog
from ..screens.main_window import MainWindow
from ..screens.popup_dialog import PopupDialog
from ..state.session import Session

log = get_logger(__name__)


def add_single_creditor(
    config: AppConfig,
    case_name: str,
    creditor: Creditor,
) -> None:
    """Enter ONE creditor into ONE case. Proof-of-life path for Milestone 1.

    Raises NotImplementedError on the navigation steps that still need real
    selectors from the inspection run. The creditor-dialog fill/save step uses
    placeholder selectors from app/selectors.py.
    """
    session = Session.create(config)
    setup_logging(config.logs_dir, level=config.log_level, run_id=session.run_id)
    log.info("Single-creditor entry: case=%r creditor=%r", case_name, creditor.name)

    adapter = BestCaseAdapter(config)

    @retry(
        attempts=config.retry_attempts,
        delay=config.retry_delay,
        description="connect_to_bestcase",
    )
    def _connect() -> None:
        adapter.connect_or_start()

    _connect()

    try:
        # --- Navigation: TODO wire after inspection -----------------------
        main = MainWindow(adapter.main_window(), config)
        main.open_case(case_name)  # TODO: implement (raises until wired)
        main.open_creditor_section()  # TODO: implement (raises until wired)

        case = CaseWindow(adapter.case_window(), config)
        case.add_new_creditor()  # TODO: implement (raises until wired)

        # --- Dialog: already mapped to placeholder selectors --------------
        dialog = CreditorDialog(adapter.creditor_dialog(), config)
        dialog.fill(creditor)
        dialog.save()

        # Handle any confirmation popup that may appear after saving.
        PopupDialog(adapter.main_window(), config).accept()

        log.info("Creditor %r entered successfully.", creditor.name)
    except Exception as exc:  # noqa: BLE001
        log.exception("Single-creditor entry failed: %r", exc)
        capture(config.screenshots_dir, label="single_creditor_failure")
        raise


def add_single_creditor_from_json(config: AppConfig, job_path: Path, index: int = 0) -> None:
    """Convenience entry: load a job JSON and enter the creditor at ``index``."""
    from ..domain.models import CreditorJob  # local import keeps module load light

    job = CreditorJob.from_json_file(job_path)
    if not job.creditors:
        raise ValueError(f"No creditors in job file: {job_path}")
    add_single_creditor(config, job.case_name, job.creditors[index])
