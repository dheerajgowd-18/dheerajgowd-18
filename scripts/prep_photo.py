#!/usr/bin/env python3
"""Prepare a photo for ASCII rendering.

Crops tightly to subject, suppresses background noise,
applies CLAHE equalization, and normalizes contrast for clean ASCII conversion.

Example:
    python scripts/prep_photo.py source-photo.jpeg
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "source-prepped.png"
MAX_SIDE = 1400
BINS = 256


def clahe(gray: np.ndarray, tiles: tuple[int, int] = (8, 8), clip: float = 2.0) -> np.ndarray:
    h, w = gray.shape
    ty, tx = tiles
    pad_y, pad_x = (-h) % ty, (-w) % tx
    g = np.pad(gray, ((0, pad_y), (0, pad_x)), mode="edge")
    gh, gw = g.shape
    th, tw = gh // ty, gw // tx
    limit = max(1.0, clip * th * tw / BINS)
    maps = np.zeros((ty, tx, BINS), dtype=np.float32)

    for i in range(ty):
        for j in range(tx):
            tile = g[i * th : (i + 1) * th, j * tw : (j + 1) * tw]
            hist = np.bincount(tile.ravel(), minlength=BINS).astype(np.float32)
            excess = np.maximum(hist - limit, 0).sum()
            hist = np.minimum(hist, limit) + excess / BINS
            cdf = np.cumsum(hist)
            span = max(float(cdf[-1] - cdf[0]), 1e-6)
            maps[i, j] = (cdf - cdf[0]) / span * (BINS - 1)

    fy = (np.arange(gh) + 0.5) / th - 0.5
    fx = (np.arange(gw) + 0.5) / tw - 0.5
    y0 = np.clip(np.floor(fy).astype(int), 0, ty - 1)
    x0 = np.clip(np.floor(fx).astype(int), 0, tx - 1)
    y1, x1 = np.clip(y0 + 1, 0, ty - 1), np.clip(x0 + 1, 0, tx - 1)
    wy = np.clip(fy - np.floor(fy), 0, 1)[:, None].astype(np.float32)
    wx = np.clip(fx - np.floor(fx), 0, 1)[None, :].astype(np.float32)

    def take(mi: np.ndarray, mj: np.ndarray) -> np.ndarray:
        return maps[mi[:, None], mj[None, :], g]

    out = (
        (1 - wy) * (1 - wx) * take(y0, x0)
        + (1 - wy) * wx * take(y0, x1)
        + wy * (1 - wx) * take(y1, x0)
        + wy * wx * take(y1, x1)
    )
    return np.clip(out, 0, 255).astype(np.uint8)[:h, :w]


def crop_to_aspect(img: Image.Image, aspect: float, bias: float) -> Image.Image:
    w, h = img.size
    if h / w > aspect:
        new_h = int(round(w * aspect))
        top = int(round((h - new_h) * bias))
        return img.crop((0, top, w, top + new_h))
    new_w = int(round(h / aspect))
    left = (w - new_w) // 2
    return img.crop((left, 0, left + new_w, h))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("photo", type=Path, nargs="?", default=ROOT / "source-photo.jpeg")
    parser.add_argument("--aspect", type=float, default=1.02)
    parser.add_argument("--bias", type=float, default=0.10)
    parser.add_argument("--clip", type=float, default=2.0)
    parser.add_argument("--gamma", type=float, default=1.2)
    parser.add_argument("--bg-thresh", type=float, default=24.0)
    args = parser.parse_args()

    photo_path = args.photo
    if not photo_path.exists():
        fallback = ROOT / "source-photo.jpg"
        if fallback.exists():
            photo_path = fallback
        else:
            raise SystemExit(f"photo not found: {args.photo}")

    image = ImageOps.exif_transpose(Image.open(photo_path).convert("RGB"))
    image = crop_to_aspect(image, args.aspect, args.bias)
    if max(image.size) > MAX_SIDE:
        image.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)

    raw_gray = np.asarray(image.convert("L"), dtype=np.uint8)

    bg_mask = raw_gray <= args.bg_thresh
    enhanced = clahe(raw_gray, (8, 8), args.clip)

    subject_pixels = enhanced[~bg_mask]
    if len(subject_pixels) > 0:
        low, high = np.percentile(subject_pixels, [3.0, 96.0])
        if high - low < 1:
            low, high = 0.0, 255.0
        stretched = np.clip((enhanced.astype(np.float32) - low) / (high - low), 0, 1)
        stretched = (stretched ** (1.0 / args.gamma)) * 255.0
    else:
        stretched = enhanced.astype(np.float32)

    final = np.where(bg_mask, 0, stretched).astype(np.uint8)

    Image.fromarray(final).save(OUT)
    print(f"wrote {OUT.relative_to(ROOT)} ({final.shape[1]}x{final.shape[0]})")


if __name__ == "__main__":
    main()
