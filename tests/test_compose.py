import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


class ComposeTests(unittest.TestCase):
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
