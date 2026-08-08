from __future__ import annotations

"""Pure-Python subprocess test oracle.

Runs the target process directly and reports its own return code, avoiding shell
pipelines that can accidentally expose the formatter/`tail` exit status.
"""

import subprocess
from pathlib import Path
from typing import Iterable, Mapping, Sequence


def _tail(text: str, lines: int) -> str:
    parts = text.splitlines()
    return "\n".join(parts[-max(0, int(lines)):])


def run_process(
    argv: Sequence[str],
    *,
    cwd: str | None = None,
    env: Mapping[str, str] | None = None,
    timeout_s: float | None = None,
    output_tail_lines: int = 30,
) -> dict:
    if not argv:
        raise ValueError("argv must not be empty")

    completed = subprocess.run(
        [str(x) for x in argv],
        cwd=str(Path(cwd).resolve()) if cwd else None,
        env=dict(env) if env is not None else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout_s,
        shell=False,
        check=False,
    )

    return {
        "status": "PASS" if completed.returncode == 0 else "FAIL",
        "returncode": int(completed.returncode),
        "argv": [str(x) for x in argv],
        "stdout_tail": _tail(completed.stdout or "", output_tail_lines),
        "stderr_tail": _tail(completed.stderr or "", output_tail_lines),
    }


def classify_failure(report: Mapping, *, expected_failure_markers: Iterable[str] = ()) -> dict:
    code = int(report.get("returncode", -999999))
    combined = f"{report.get('stdout_tail', '')}\n{report.get('stderr_tail', '')}"
    markers = [str(x) for x in expected_failure_markers]
    seen = [m for m in markers if m in combined]

    if code == 0:
        kind = "PASS"
    elif markers and seen:
        kind = "EXPECTED_ASSERTION_FAIL"
    else:
        kind = "UNCLASSIFIED_NONZERO"

    return {
        "process_status": kind,
        "returncode": code,
        "expected_markers": markers,
        "seen_markers": seen,
        "status": "PASS" if kind in {"PASS", "EXPECTED_ASSERTION_FAIL"} else "UNVERIFIED",
    }


def validate_bite_pair(
    failing_report: Mapping,
    restored_report: Mapping,
    *,
    expected_failure_marker: str,
) -> dict:
    fail_class = classify_failure(
        failing_report,
        expected_failure_markers=[expected_failure_marker],
    )
    restored_ok = int(restored_report.get("returncode", -1)) == 0
    valid_bite = (
        fail_class["process_status"] == "EXPECTED_ASSERTION_FAIL"
        and restored_ok
    )
    return {
        "status": "PASS" if valid_bite else "FAIL",
        "failing_returncode": int(failing_report.get("returncode", -1)),
        "expected_failure_message_seen": bool(fail_class["seen_markers"]),
        "restored_returncode": int(restored_report.get("returncode", -1)),
        "restored_green": restored_ok,
    }
