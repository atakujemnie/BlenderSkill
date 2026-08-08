from __future__ import annotations

"""Compact semantic validation helpers for baked Blender images."""

from typing import Mapping, Sequence

try:
    import numpy as np
except Exception:  # pragma: no cover - Blender normally ships NumPy
    np = None


def _array(image):
    if np is None:
        raise RuntimeError("NumPy is required by bake_validate candidate executor")
    data = np.array(image.pixels[:], dtype=np.float32)
    return data.reshape(int(image.size[1]), int(image.size[0]), 4)


def image_stats(image) -> dict:
    a = _array(image)[:, :, :3]
    mins = [float(a[:, :, i].min()) for i in range(3)]
    maxs = [float(a[:, :, i].max()) for i in range(3)]
    return {
        "name": image.name,
        "size": [int(image.size[0]), int(image.size[1])],
        "min": [round(v, 6) for v in mins],
        "max": [round(v, 6) for v in maxs],
        "mean": [round(float(a[:, :, i].mean()), 6) for i in range(3)],
        "spatial_range": [round(maxs[i] - mins[i], 6) for i in range(3)],
        "nonzero_fraction": round(float((a.max(axis=2) > 1e-6).mean()), 6),
        "near_one_fraction": round(float((a.min(axis=2) >= 0.999).mean()), 6),
    }


def _slice(a, rect):
    u0, v0, u1, v1 = map(float, rect)
    h, w = a.shape[:2]
    x0, x1 = max(0, int(u0 * w)), min(w, max(1, int(u1 * w)))
    y0, y1 = max(0, int(v0 * h)), min(h, max(1, int(v1 * h)))
    return a[y0:y1, x0:x1]


def rect_stats(image, rects: Mapping[str, Sequence[float]]) -> dict:
    a = _array(image)[:, :, :3]
    out = {}
    for key, rect in rects.items():
        r = _slice(a, rect)
        mins = [float(r[:, :, i].min()) for i in range(3)]
        maxs = [float(r[:, :, i].max()) for i in range(3)]
        out[str(key)] = {
            "min": [round(v, 6) for v in mins],
            "max": [round(v, 6) for v in maxs],
            "mean": [round(float(r[:, :, i].mean()), 6) for i in range(3)],
            "spatial_range": [round(maxs[i] - mins[i], 6) for i in range(3)],
            "nonzero_fraction": round(float((r.max(axis=2) > 1e-6).mean()), 6),
        }
    return out


def validate_non_degenerate(
    image,
    *,
    allow_all_zero: bool = False,
    allow_constant: bool = False,
    epsilon: float = 1e-5,
) -> dict:
    stats = image_stats(image)
    spatial_dynamic = max(stats["spatial_range"])
    reasons = []
    if not allow_all_zero and max(stats["max"]) <= epsilon:
        reasons.append("ALL_ZERO")
    if not allow_constant and spatial_dynamic <= epsilon:
        reasons.append("UNEXPECTED_SPATIALLY_CONSTANT")
    return {
        "status": "FAIL" if reasons else "PASS",
        "stats": stats,
        "reasons": reasons,
    }


def validate_emissive_regions(
    image,
    approved_rects: Mapping[str, Sequence[float]],
    *,
    threshold: float = 0.01,
    max_outside_fraction: float = 0.005,
) -> dict:
    a = _array(image)[:, :, :3]
    signal = a.max(axis=2) > float(threshold)
    allowed = np.zeros(signal.shape, dtype=bool)
    h, w = signal.shape

    per_region = {}
    for key, rect in approved_rects.items():
        u0, v0, u1, v1 = map(float, rect)
        x0, x1 = max(0, int(u0 * w)), min(w, max(1, int(u1 * w)))
        y0, y1 = max(0, int(v0 * h)), min(h, max(1, int(v1 * h)))
        allowed[y0:y1, x0:x1] = True
        region_signal = signal[y0:y1, x0:x1]
        per_region[str(key)] = {
            "signal_px": int(region_signal.sum()),
            "signal_fraction": round(float(region_signal.mean()), 6),
        }

    outside = signal & ~allowed
    outside_fraction = float(outside.sum()) / float(signal.size)
    reasons = []
    if not signal.any():
        reasons.append("NO_EMISSIVE_SIGNAL")
    if outside_fraction > max_outside_fraction:
        reasons.append("EMISSIVE_OUTSIDE_APPROVED_REGIONS")

    stats = image_stats(image)
    return {
        "status": "FAIL" if reasons else "PASS",
        "stats": stats,
        "regions": per_region,
        "outside_signal_px": int(outside.sum()),
        "outside_fraction": round(outside_fraction, 6),
        "reasons": reasons,
    }


def validate_scalar_region(
    image,
    rect,
    *,
    channel: int,
    mean_min: float | None = None,
    mean_max: float | None = None,
    label: str = "region",
) -> dict:
    a = _array(image)[:, :, :3]
    r = _slice(a, rect)[:, :, int(channel)]
    mean = float(r.mean())
    reasons = []
    if mean_min is not None and mean < mean_min:
        reasons.append("MEAN_BELOW_EXPECTED")
    if mean_max is not None and mean > mean_max:
        reasons.append("MEAN_ABOVE_EXPECTED")
    return {
        "label": label,
        "status": "FAIL" if reasons else "PASS",
        "mean": round(mean, 6),
        "min": round(float(r.min()), 6),
        "max": round(float(r.max()), 6),
        "reasons": reasons,
    }
