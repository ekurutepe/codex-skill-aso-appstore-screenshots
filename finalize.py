#!/usr/bin/env python3
"""Finalize raster output and its manifest without claiming scaffold geometry is measured."""

import argparse
import json
from pathlib import Path

from PIL import Image

from compose import CANVAS_W, CANVAS_H


def finalize(source, output, manifest=None, size=(CANVAS_W, CANVAS_H)):
    source, output = Path(source).resolve(), Path(output).resolve()
    manifest = Path(manifest) if manifest else source.with_suffix(".aso.json")
    data = json.loads(manifest.read_text())
    if source == output or output.exists() or output.with_suffix(".aso.json").exists():
        raise ValueError("Choose a new output path; finalization never overwrites artwork")
    if min(size) <= 0:
        raise ValueError("Output dimensions must be positive")
    with Image.open(source) as image:
        if image.convert("RGBA").getchannel("A").getextrema() != (255, 255):
            raise ValueError("Source must be opaque; resolve transparency first")
        width, height = image.size
        target_w, target_h = size
        if width / height >= target_w / target_h:
            crop_w, crop_h = round(height * target_w / target_h), height
        else:
            crop_w, crop_h = width, round(width * target_h / target_w)
        left = (width - crop_w) // 2
        crop = (left, 0, left + crop_w, crop_h)
        result = image.crop(crop).resize(size, Image.Resampling.LANCZOS).convert("RGB")

    # A scaffold describes intended placement, not measured imagegen output.
    reference = data.pop("reference_geometry", None)
    if reference is None:
        reference = {"canvas": data["canvas"], "layout": data["layout"],
                     "device": data.pop("device", None),
                     "breakout": data.pop("primary_breakout", None),
                     "proof": data.get("social_proof", {}).pop("parameters", None)}
    data["reference_geometry"] = reference
    data["layout"] = {"name": reference["layout"]["name"]}
    data.pop("observed_geometry", None)
    data["geometry_verified"] = False
    if image.size != size or crop != (0, 0, width, height):
        data.pop("visual_review", None)
    data["output"] = str(output)
    data["canvas"] = {"width": target_w, "height": target_h}
    data["processing"] = {"source": str(source), "source_size": [width, height],
                          "crop_box": list(crop),
                          "scale": [target_w / crop_w, target_h / crop_h]}
    output.parent.mkdir(parents=True, exist_ok=True)
    result.save(output, "PNG")
    output.with_suffix(".aso.json").write_text(json.dumps(data, indent=2) + "\n")
    with Image.open(output) as exported:
        if exported.size != size or exported.mode != "RGB":
            raise ValueError("Output verification failed")
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("--manifest", help="Use the scaffold manifest for a new imagegen variant")
    parser.add_argument("--width", type=int, default=CANVAS_W)
    parser.add_argument("--height", type=int, default=CANVAS_H)
    args = parser.parse_args()
    finalize(args.source, args.output, args.manifest, (args.width, args.height))
    print(f"Verified image and manifest: {args.output}; visual geometry review still required")
