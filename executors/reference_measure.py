"""Compact reference measurement executor for Blender AI agents.

Purpose
-------
Measure registered concept-art / technical-sheet ROIs inside Blender while
keeping raw pixel profiles out of the language-model context.

The caller is expected to provide validated ROIs from the Reference Registry.
This executor intentionally does not try to solve full concept-sheet
segmentation. It focuses on deterministic local measurement and aggregation.

Coordinates are top-down image coordinates: [x0, y0, x1, y1].

Typical Blender use::

    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "reference_measure",
        r".../BlenderSkill/executors/reference_measure.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    result = mod.measure_reference({
        "source_image": r".../concept_art.png",
        "views": {
            "FRONT": {"roi": [735, 165, 860, 640], "threshold": 0.72},
            "SIDE":  {"roi": [930, 165, 1030, 640], "threshold": 0.72},
        },
        "known_dimensions": {"height_mm": 1050},
    })

The result is JSON-serializable and contains aggregate summaries only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

import bpy
import numpy as np


EXECUTOR_ID = "REFERENCE_MEASURE"
EXECUTOR_VERSION = "0.1.0"


@dataclass(frozen=True)
class Run:
    x0: int
    x1: int

    @property
    def width(self) -> int:
        return self.x1 - self.x0 + 1

    @property
    def center(self) -> float:
        return (self.x0 + self.x1) * 0.5


def _load_rgba_top_down(path: str) -> np.ndarray:
    image = bpy.data.images.load(path, check_existing=True)
    width, height = int(image.size[0]), int(image.size[1])
    channels = int(image.channels)
    pixels = np.asarray(image.pixels[:], dtype=np.float32)
    pixels = pixels.reshape(height, width, channels)[::-1]

    if channels < 3:
        raise ValueError(f"Expected RGB/RGBA image, got {channels} channel(s)")
    return pixels[:, :, : min(channels, 4)]


def _validate_roi(roi: Iterable[int], width: int, height: int) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = [int(v) for v in roi]
    if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height):
        raise ValueError(
            f"REF_ROI_INVALID: roi={[x0, y0, x1, y1]} image={[width, height]}"
        )
    return x0, y0, x1, y1


def _row_runs(mask_row: np.ndarray) -> list[Run]:
    idx = np.flatnonzero(mask_row)
    if idx.size == 0:
        return []

    breaks = np.where(np.diff(idx) > 1)[0]
    starts = np.r_[0, breaks + 1]
    ends = np.r_[breaks, idx.size - 1]
    return [Run(int(idx[s]), int(idx[e])) for s, e in zip(starts, ends)]


def _select_object_run(
    runs: list[Run],
    *,
    center_x: float,
    previous_center: float | None,
    min_width_px: int,
) -> Run | None:
    candidates = [run for run in runs if run.width >= min_width_px]
    if not candidates:
        return None

    # Prefer a run containing the expected object center. This rejects many
    # dimension lines / leaders that sit beside an axis-centered product view.
    containing = [run for run in candidates if run.x0 <= center_x <= run.x1]
    if containing:
        return max(containing, key=lambda r: r.width)

    target = previous_center if previous_center is not None else center_x
    return min(candidates, key=lambda r: abs(r.center - target))


def _apply_exclusions(mask: np.ndarray, exclusions: Iterable[Iterable[int]]) -> None:
    """Zero local exclusion rectangles expressed relative to the ROI."""
    h, w = mask.shape
    for rect in exclusions:
        x0, y0, x1, y1 = [int(v) for v in rect]
        x0, x1 = max(0, x0), min(w, x1)
        y0, y1 = max(0, y0), min(h, y1)
        if x0 < x1 and y0 < y1:
            mask[y0:y1, x0:x1] = False


def _compress_profile(
    rows: list[tuple[int, int, float]],
    *,
    tolerance_px: float,
    min_rows: int,
) -> list[dict[str, Any]]:
    """Compress per-row widths into stable width segments.

    Input stays local; only segments are returned to the caller.
    """
    if not rows:
        return []

    segments: list[list[tuple[int, int, float]]] = []
    current: list[tuple[int, int, float]] = [rows[0]]

    for item in rows[1:]:
        y, width, center = item
        prev_y = current[-1][0]
        median_width = float(np.median([r[1] for r in current]))
        if y == prev_y + 1 and abs(width - median_width) <= tolerance_px:
            current.append(item)
        else:
            segments.append(current)
            current = [item]
    segments.append(current)

    out: list[dict[str, Any]] = []
    for seg in segments:
        if len(seg) < min_rows:
            continue
        widths = np.asarray([r[1] for r in seg], dtype=np.float32)
        centers = np.asarray([r[2] for r in seg], dtype=np.float32)
        out.append(
            {
                "y_px": [int(seg[0][0]), int(seg[-1][0])],
                "rows": int(len(seg)),
                "width_px_median": round(float(np.median(widths)), 3),
                "width_px_mean": round(float(widths.mean()), 3),
                "width_px_std": round(float(widths.std()), 3),
                "center_px_mean": round(float(centers.mean()), 3),
            }
        )
    return out


def measure_view(
    rgba_top_down: np.ndarray,
    *,
    roi: Iterable[int],
    threshold: float = 0.72,
    min_width_px: int = 3,
    segment_tolerance_px: float = 2.0,
    min_segment_rows: int = 4,
    exclusions: Iterable[Iterable[int]] = (),
) -> dict[str, Any]:
    """Measure one registered view and return compact silhouette statistics."""
    height, width = rgba_top_down.shape[:2]
    x0, y0, x1, y1 = _validate_roi(roi, width, height)

    rgb = rgba_top_down[y0:y1, x0:x1, :3]
    luminance = rgb.mean(axis=2)
    mask = luminance < float(threshold)
    _apply_exclusions(mask, exclusions)

    local_center = (mask.shape[1] - 1) * 0.5
    previous_center: float | None = None
    profile: list[tuple[int, int, float]] = []

    for local_y in range(mask.shape[0]):
        run = _select_object_run(
            _row_runs(mask[local_y]),
            center_x=local_center,
            previous_center=previous_center,
            min_width_px=min_width_px,
        )
        if run is None:
            continue
        previous_center = run.center
        profile.append((local_y + y0, run.width, run.center + x0))

    if not profile:
        return {
            "status": "FAIL",
            "error": "REF_LOW_CONTRAST",
            "roi": [x0, y0, x1, y1],
            "threshold": float(threshold),
        }

    widths = np.asarray([r[1] for r in profile], dtype=np.float32)
    centers = np.asarray([r[2] for r in profile], dtype=np.float32)
    ys = np.asarray([r[0] for r in profile], dtype=np.int32)

    segments = _compress_profile(
        profile,
        tolerance_px=float(segment_tolerance_px),
        min_rows=int(min_segment_rows),
    )

    return {
        "status": "PASS",
        "roi": [x0, y0, x1, y1],
        "threshold": float(threshold),
        "occupied_y_px": [int(ys.min()), int(ys.max())],
        "sampled_rows": int(widths.size),
        "width_px": {
            "median": round(float(np.median(widths)), 3),
            "mean": round(float(widths.mean()), 3),
            "std": round(float(widths.std()), 3),
            "p10": round(float(np.percentile(widths, 10)), 3),
            "p90": round(float(np.percentile(widths, 90)), 3),
        },
        "axis_center_px": {
            "mean": round(float(centers.mean()), 3),
            "std": round(float(centers.std()), 3),
        },
        "segments": segments,
    }


def compare_view_widths(a: Mapping[str, Any], b: Mapping[str, Any]) -> dict[str, Any]:
    if a.get("status") != "PASS" or b.get("status") != "PASS":
        return {"status": "UNVERIFIED", "reason": "VIEW_MEASUREMENT_FAILED"}

    wa = float(a["width_px"]["median"])
    wb = float(b["width_px"]["median"])
    denom = max((wa + wb) * 0.5, 1e-9)
    difference_pct = abs(wa - wb) / denom * 100.0
    return {
        "status": "MEASURED",
        "median_width_difference_pct": round(difference_pct, 3),
    }


def measure_reference(spec: Mapping[str, Any]) -> dict[str, Any]:
    """Run compact measurements for registered views.

    Expected spec::

        {
          "source_image": "...",
          "views": {
             "FRONT": {"roi": [...], "threshold": 0.72},
             "SIDE":  {"roi": [...], "threshold": 0.72}
          },
          "known_dimensions": {...}
        }
    """
    source = str(spec["source_image"])
    rgba = _load_rgba_top_down(source)

    results: dict[str, Any] = {}
    for view_id, cfg_raw in dict(spec.get("views", {})).items():
        cfg = dict(cfg_raw)
        results[str(view_id)] = measure_view(
            rgba,
            roi=cfg["roi"],
            threshold=float(cfg.get("threshold", 0.72)),
            min_width_px=int(cfg.get("min_width_px", 3)),
            segment_tolerance_px=float(cfg.get("segment_tolerance_px", 2.0)),
            min_segment_rows=int(cfg.get("min_segment_rows", 4)),
            exclusions=cfg.get("exclusions", ()),
        )

    cross_view: dict[str, Any] = {}
    if "FRONT" in results and "SIDE" in results:
        cross_view["front_side"] = compare_view_widths(
            results["FRONT"], results["SIDE"]
        )

    statuses = [v.get("status") for v in results.values()]
    overall = "PASS" if results and all(s == "PASS" for s in statuses) else "PARTIAL"

    return {
        "executor": EXECUTOR_ID,
        "version": EXECUTOR_VERSION,
        "status": overall,
        "source_image": source,
        "image_size_px": [int(rgba.shape[1]), int(rgba.shape[0])],
        "known_dimensions": dict(spec.get("known_dimensions", {})),
        "views": results,
        "cross_view": cross_view,
    }


__all__ = [
    "EXECUTOR_ID",
    "EXECUTOR_VERSION",
    "measure_view",
    "compare_view_widths",
    "measure_reference",
]
