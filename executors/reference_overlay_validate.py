from __future__ import annotations

"""Registered reference-vs-render visual fidelity validator.

Designed for reconstruction QA before runtime/LOD work. It deliberately does not
perform free alignment: caller must supply globally registered reference/candidate
images for the same view. The validator returns compact metrics only.
"""

from typing import Any, Mapping

import numpy as np

EXECUTOR_ID = "REFERENCE_OVERLAY_VALIDATE"
EXECUTOR_VERSION = "0.1.0"


def _load_rgba(path: str) -> np.ndarray:
    try:
        from PIL import Image
        return np.asarray(Image.open(path).convert("RGBA"), dtype=np.float32) / 255.0
    except Exception:
        import bpy
        img = bpy.data.images.load(str(path), check_existing=False)
        w, h, ch = int(img.size[0]), int(img.size[1]), int(img.channels)
        px = np.asarray(img.pixels[:], dtype=np.float32).reshape(h, w, ch)[::-1]
        if ch == 3:
            px = np.concatenate([px, np.ones((h, w, 1), dtype=np.float32)], axis=2)
        bpy.data.images.remove(img)
        return px[:, :, :4]


def _mask(arr: np.ndarray, cfg: Mapping[str, Any]) -> np.ndarray:
    mode = str(cfg.get("mode", "LUMINANCE_DARK")).upper()
    rgb, alpha = arr[:, :, :3], arr[:, :, 3]
    lum = rgb.mean(axis=2)
    if mode == "ALPHA":
        return alpha >= float(cfg.get("alpha_threshold", 0.5))
    if mode == "LUMINANCE_DARK":
        return lum <= float(cfg.get("luminance_threshold", 0.80))
    if mode == "LUMINANCE_OR_CHROMA":
        dark = lum <= float(cfg.get("luminance_threshold", 0.80))
        spread = rgb.max(axis=2) - rgb.min(axis=2)
        chroma = spread >= float(cfg.get("chroma_threshold", 0.08))
        blue = rgb[:, :, 2] - 0.5 * (rgb[:, :, 0] + rgb[:, :, 1])
        blue_dom = blue >= float(cfg.get("blue_dominance_threshold", 0.05))
        return dark | chroma | blue_dom
    raise ValueError(f"Unsupported mask mode: {mode}")


def _boundary(mask: np.ndarray) -> np.ndarray:
    p = np.pad(mask, 1, constant_values=False)
    inner = p[1:-1, 1:-1]
    eroded = inner & p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
    return inner & ~eroded


def _sample_points(boundary: np.ndarray, max_points: int = 5000) -> np.ndarray:
    pts = np.argwhere(boundary)
    if len(pts) <= max_points:
        return pts.astype(np.float32)
    idx = np.linspace(0, len(pts) - 1, max_points, dtype=np.int32)
    return pts[idx].astype(np.float32)


def _nearest_distances(a: np.ndarray, b: np.ndarray, chunk: int = 512) -> np.ndarray:
    if len(a) == 0 or len(b) == 0:
        return np.asarray([np.inf], dtype=np.float32)
    out = []
    for i in range(0, len(a), chunk):
        aa = a[i:i + chunk]
        d2 = ((aa[:, None, :] - b[None, :, :]) ** 2).sum(axis=2)
        out.append(np.sqrt(d2.min(axis=1)))
    return np.concatenate(out)


def _metrics(ref: np.ndarray, cand: np.ndarray) -> dict[str, Any]:
    inter = int(np.logical_and(ref, cand).sum())
    union = int(np.logical_or(ref, cand).sum())
    iou = 1.0 if union == 0 else inter / union
    rb, cb = _sample_points(_boundary(ref)), _sample_points(_boundary(cand))
    d = np.concatenate([_nearest_distances(rb, cb), _nearest_distances(cb, rb)])
    finite = d[np.isfinite(d)]
    if finite.size == 0:
        mean_d = max_d = float("inf")
    else:
        mean_d, max_d = float(finite.mean()), float(finite.max())
    return {
        "iou": round(float(iou), 5),
        "mean_contour_deviation_px": round(mean_d, 3),
        "max_contour_deviation_px": round(max_d, 3),
        "reference_pixels": int(ref.sum()),
        "candidate_pixels": int(cand.sum()),
    }


def _passes(m: Mapping[str, Any], thresholds: Mapping[str, Any]) -> bool:
    return (
        float(m["iou"]) >= float(thresholds.get("min_iou", 0.0))
        and float(m["mean_contour_deviation_px"]) <= float(thresholds.get("max_mean_contour_px", float("inf")))
        and float(m["max_contour_deviation_px"]) <= float(thresholds.get("max_contour_px", float("inf")))
    )


def validate(spec: Mapping[str, Any]) -> dict[str, Any]:
    ref = _load_rgba(str(spec["reference_image"]))
    cand = _load_rgba(str(spec["candidate_image"]))
    if ref.shape[:2] != cand.shape[:2]:
        return {"status": "FAIL", "error": "REGISTRATION_SIZE_MISMATCH", "reference_hw": list(ref.shape[:2]), "candidate_hw": list(cand.shape[:2])}

    ref_mask = _mask(ref, dict(spec.get("reference_mask", {})))
    cand_mask = _mask(cand, dict(spec.get("candidate_mask", {"mode": "ALPHA"})))
    thresholds = dict(spec.get("thresholds", {}))
    global_metrics = _metrics(ref_mask, cand_mask)
    regions = {}
    failed_regions = []

    h, w = ref_mask.shape
    for region_id, raw in dict(spec.get("regions", {})).items():
        cfg = dict(raw)
        x0, y0, x1, y1 = [int(v) for v in cfg["roi"]]
        if not (0 <= x0 < x1 <= w and 0 <= y0 < y1 <= h):
            return {"status": "FAIL", "error": "ROI_INVALID", "region": region_id, "roi": [x0, y0, x1, y1]}
        m = _metrics(ref_mask[y0:y1, x0:x1], cand_mask[y0:y1, x0:x1])
        t = {**thresholds, **dict(cfg.get("thresholds", {}))}
        m["status"] = "PASS" if _passes(m, t) else "FAIL"
        regions[region_id] = m
        if m["status"] == "FAIL" and str(cfg.get("criticality", "MUST")).upper() == "MUST":
            failed_regions.append(region_id)

    global_pass = _passes(global_metrics, thresholds)
    status = "PASS" if global_pass and not failed_regions else "FAIL"
    return {
        "status": status,
        "registration_policy": "GLOBAL_PRE_REGISTERED_NO_LOCAL_WARP",
        "global": {**global_metrics, "status": "PASS" if global_pass else "FAIL"},
        "regions": regions,
        "failed_must_regions": failed_regions,
    }
