#!/usr/bin/env python3
"""Run repository checks, or validate a screenshot project's saved state."""

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

from PIL import Image
import yaml

ROOT = Path(__file__).resolve().parent


def validate_state(path):
    path = Path(path).resolve()
    data = json.loads(path.read_text())
    if data.get("status", "draft") not in ("discovery", "draft", "approved"):
        raise ValueError("State status must be discovery, draft, or approved")
    if data.get("schema_version") != 1:
        raise ValueError("State requires schema_version 1")
    for value in data.get("files", []):
        if not (path.parent / value).is_file():
            raise ValueError(f"Missing saved artifact: {value}; retake or relocate it before resuming")
    if data.get("status") == "discovery":
        if data.get("exports"):
            raise ValueError("Discovery state cannot contain approved exports")
        return data
    if data.get("renderer") not in ("sketch-template", "raster-fallback"):
        raise ValueError("State requires an explicit renderer")
    if not data.get("visual_system"):
        raise ValueError("Save the shared visual system before rendering")
    panels = data.get("panels", [])
    if len(panels) < 2 or panels[0].get("role") != "category-action" or panels[1].get("role") != "result":
        raise ValueError("Storyboard must open with category-action, then result")
    allowed = {"category-action", "result", "benefit", "proof"}
    for panel in panels:
        if panel.get("role") not in allowed or not all(panel.get(k) for k in ("headline", "visual", "layout", "reason")):
            raise ValueError("Each panel needs role, headline, visual, layout, and reason")
    if data.get("status") == "approved":
        for key in ("direction", "final"):
            review = data.get("reviews", {}).get(key, {})
            if review.get("approved") is not True or not review.get("notes"):
                raise ValueError(f"Approved state needs {key} review notes and approval")
            sheet = review.get("contact_sheet")
            if not sheet or not (path.parent / sheet).is_file():
                raise ValueError(f"Missing {key} full-set contact sheet")
        if not data.get("exports"):
            raise ValueError("Approved state requires exports")
        groups = {}
        for export in data["exports"]:
            target = Path(export["path"])
            group = groups.setdefault(target.parent, set())
            if target.name in group:
                raise ValueError(f"Duplicate export: {target}")
            group.add(target.name)
        if any(len(group) != len(panels) for group in groups.values()):
            raise ValueError("Every exported locale/device directory needs one image per panel")
    for export in data.get("exports", []):
        image_path = path.parent / export["path"]
        with Image.open(image_path) as image:
            if image.size != tuple(export["size"]) or image.mode != "RGB":
                raise ValueError(f"Wrong dimensions or mode: {image_path}")
        if data["renderer"] == "raster-fallback":
            manifest = json.loads(image_path.with_suffix(".aso.json").read_text())
            expected = {"width": export["size"][0], "height": export["size"][1]}
            if manifest["canvas"] != expected or Path(manifest["output"]).resolve() != image_path.resolve():
                raise ValueError(f"Stale manifest: {image_path}")
            if data.get("status") == "approved" and (manifest.get("visual_review", {}).get("approved") is not True
                    or not manifest.get("visual_review", {}).get("notes")):
                raise ValueError(f"Final raster export needs visual review notes: {image_path}")
    return data


def check_repository():
    skill = (ROOT / "SKILL.md").read_text()
    metadata = yaml.safe_load(skill.split("---", 2)[1])
    if metadata.get("name") != "aso-appstore-screenshots" or not metadata.get("description"):
        raise ValueError("Invalid skill frontmatter")
    interface = yaml.safe_load((ROOT / "agents/openai.yaml").read_text())
    if not all(interface.get("interface", {}).get(key) for key in ("display_name", "short_description", "default_prompt")):
        raise ValueError("Missing skill interface metadata")
    for document in ROOT.rglob("*.md"):
        body = document.read_text()
        if body.count("```") % 2:
            raise ValueError(f"Unclosed code fence: {document}")
        # Exclude code examples so illustrative paths are not treated as dependencies.
        prose = re.sub(r"```.*?```", "", body, flags=re.S)
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", prose):
            if "://" not in target and not target.startswith("#"):
                target = target.split("#", 1)[0]
                if not (document.parent / target).exists():
                    raise ValueError(f"Broken reference in {document}: {target}")
    for asset in ("device_frame.png", "laurel.png"):
        with Image.open(ROOT / "assets" / asset) as image:
            image.verify()
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path)
    args = parser.parse_args()
    try:
        if args.state:
            validate_state(args.state)
        else:
            check_repository()
    except (ValueError, KeyError, OSError, yaml.YAMLError) as error:
        parser.exit(1, f"Check failed: {error}\n")
    print("Checks passed (visual review is separate).")
