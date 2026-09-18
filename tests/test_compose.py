import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from compose import draw_centered_lines, resolve_font_path, word_wrap
from finalize import finalize
from check import validate_state


ROOT = Path(__file__).resolve().parents[1]


class ComposeTests(unittest.TestCase):
    def test_visible_top_and_line_gap_from_pixels(self):
        font = ImageFont.truetype(resolve_font_path(), 100)
        image = Image.new("L", (1284, 700))
        draw = ImageDraw.Draw(image)
        bottom = draw_centered_lines(draw, 200, "TRACK\nFISH", font, 1181, 40)
        rows = [y for y in range(image.height) if image.crop((0, y, image.width, y + 1)).getbbox()]
        self.assertEqual(rows[0], 200)
        self.assertEqual(rows[-1] + 1, bottom)
        gaps = [b - a - 1 for a, b in zip(rows, rows[1:]) if b - a > 1]
        self.assertEqual(gaps, [40])
        self.assertEqual(word_wrap(draw, "FIND\nFISH", font, 1181), ["FIND", "FISH"])

    def test_finalization_preserves_reference_and_updates_output(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            reference = {"canvas": {"width": 1284, "height": 2778},
                         "layout": {"name": "regular", "parameters": {"text_top": 200}},
                         "device": {"x": 127, "y": 720}, "output": "old.png"}
            scaffold = work / "scaffold.aso.json"
            scaffold.write_text(json.dumps(reference))
            for size in ((900, 1600), (400, 1200), (1284, 2778)):
                source = work / f"source-{size[0]}.png"
                output = work / f"final-{size[0]}.png"
                Image.new("RGB", size, "red").save(source)
                manifest = finalize(source, output, scaffold)
                with Image.open(output) as image:
                    self.assertEqual(image.size, (1284, 2778))
                    self.assertEqual(image.mode, "RGB")
                self.assertEqual(json.loads(output.with_suffix(".aso.json").read_text()), manifest)
                self.assertEqual(manifest["output"], str(output.resolve()))
                self.assertEqual(manifest["reference_geometry"]["canvas"], reference["canvas"])
                self.assertFalse(manifest["geometry_verified"])
                self.assertNotIn("device", manifest)
                crop = manifest["processing"]["crop_box"]
                self.assertGreaterEqual(crop[0], 0)
                self.assertLessEqual(crop[2], size[0])
                self.assertLessEqual(crop[3], size[1])
                with self.assertRaises(ValueError):
                    finalize(source, output, scaffold)
                manifest["visual_review"] = {"approved": True, "notes": "UI and copy inspected"}
                output.with_suffix(".aso.json").write_text(json.dumps(manifest))
                promoted = work / f"approved-{size[0]}.png"
                final_manifest = finalize(output, promoted)
                self.assertEqual(final_manifest["output"], str(promoted.resolve()))
                self.assertEqual(final_manifest["visual_review"], manifest["visual_review"])
                self.assertEqual(final_manifest["reference_geometry"], manifest["reference_geometry"])
            transparent = work / "transparent.png"
            Image.new("RGBA", (100, 200), (0, 0, 0, 0)).save(transparent)
            with self.assertRaisesRegex(ValueError, "opaque"):
                finalize(transparent, work / "invalid.png", scaffold)
            self.assertFalse((work / "invalid.png").exists())


    def test_state_rejects_wrong_sequence_and_missing_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "aso-state.json"
            panel = {"role": "category-action", "headline": "Fish ID", "visual": "scan fish",
                     "layout": "photo-hero", "reason": "demonstrates action"}
            state = {"schema_version": 1, "renderer": "sketch-template", "visual_system": {"font": "Arial"},
                     "panels": [panel, dict(panel, role="result")], "files": []}
            path.write_text(json.dumps(state))
            validate_state(path)
            state["panels"][0]["role"] = "proof"
            path.write_text(json.dumps(state))
            with self.assertRaisesRegex(ValueError, "category-action"):
                validate_state(path)
            state["panels"][0]["role"] = "category-action"
            state["files"] = ["missing.png"]
            path.write_text(json.dumps(state))
            with self.assertRaisesRegex(ValueError, "Missing saved artifact"):
                validate_state(path)
            state["files"] = []
            state["status"] = "approved"
            path.write_text(json.dumps(state))
            with self.assertRaisesRegex(ValueError, "review"):
                validate_state(path)
            sheet = path.parent / "contact-sheet.png"
            Image.new("RGB", (16, 16), "red").save(sheet)
            review = {"approved": True, "notes": "All panels reviewed", "contact_sheet": sheet.name}
            state["reviews"] = {"direction": review, "final": review}
            state["renderer"] = "raster-fallback"
            state["exports"] = []
            for index in (1, 2):
                image = path.parent / "final" / f"{index:02}.png"
                image.parent.mkdir(exist_ok=True)
                Image.new("RGB", (8, 16), "red").save(image)
                image.with_suffix(".aso.json").write_text(json.dumps({
                    "canvas": {"width": 8, "height": 16}, "output": str(image.resolve()),
                    "visual_review": {"approved": True, "notes": "Copy and UI checked"}}))
                state["exports"].append({"path": str(image.relative_to(path.parent)), "size": [8, 16]})
            path.write_text(json.dumps(state))
            validate_state(path)
            state["exports"].pop()
            path.write_text(json.dumps(state))
            with self.assertRaisesRegex(ValueError, "one image per panel"):
                validate_state(path)


    def test_regular_and_social_proof_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            source = work / "source.png"
            Image.new("RGB", (1170, 2532), "#102030").save(source)

            regular = work / "regular.png"
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "compose.py"),
                    "--layout",
                    "regular",
                    "--bg",
                    "#5B21B6",
                    "--verb",
                    "見つける",
                    "--desc",
                    "必要な情報をすばやく",
                    "--locale",
                    "ja",
                    "--text-transform",
                    "none",
                    "--screenshot",
                    str(source),
                    "--output",
                    str(regular),
                ],
                check=True,
            )

            proof = work / "proof.png"
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "compose.py"),
                    "--layout",
                    "social-proof-vstack",
                    "--bg-top",
                    "#2563EB",
                    "--bg-bottom",
                    "#7C3AED",
                    "--verb",
                    "BUILD",
                    "--desc",
                    "BETTER HABITS",
                    "--proof",
                    '{"kind":"ratings","top":"4.8","bottom":"RATING","source":"test fixture"}',
                    "--screenshot",
                    str(source),
                    "--output",
                    str(proof),
                ],
                check=True,
            )

            for output in (regular, proof):
                with Image.open(output) as image:
                    self.assertEqual(image.size, (1284, 2778))
                    self.assertEqual(image.mode, "RGB")
                manifest = json.loads(output.with_suffix(".aso.json").read_text())
                self.assertEqual(manifest["canvas"], {"width": 1284, "height": 2778})
                self.assertEqual(manifest["layout"]["parameters"]["visible_text_top"], manifest["layout"]["parameters"]["text_top"])

            proof_manifest = json.loads(proof.with_suffix(".aso.json").read_text())
            self.assertEqual(proof_manifest["social_proof"]["parameters"]["proof_line_gap"], 18)


if __name__ == "__main__":
    unittest.main()
