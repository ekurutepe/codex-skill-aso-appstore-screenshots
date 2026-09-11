# ASO App Store Screenshots

A reusable Codex skill for planning, localizing, rendering, and iterating App Store screenshots for any iOS app.

## What It Does

1. **Benefit Discovery** — Analyzes your app's codebase to identify the 3-5 core benefits that drive downloads
2. **Screenshot Pairing** — Reviews your simulator screenshots, rates them, and pairs each with the best benefit
3. **Layouts** — Renders regular benefit frames or benefit-first social-proof frames with verified laurel claims
4. **Localization QA** — Preserves alignment and spacing while checking RTL, CJK, and long translations
5. **Editable generation** — Creates one Sketch template with base-localized iPhone and iPad designs, then exports localized PNGs through Sketch MCP
6. **Raster fallback** — Creates deterministic `compose.py` scaffolds with optional built-in `imagegen` enhancement when Sketch is unavailable

## Installation

### 1. Add the skill to Codex

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/ekurutepe/codex-skill-aso-appstore-screenshots \
  "${CODEX_HOME:-$HOME/.codex}/skills/aso-appstore-screenshots"
```

Restart Codex after installing the skill so it is loaded.

Alternatively, ask Codex to install the skill from GitHub with `$skill-installer`.

### 2. Install Python Dependencies

```bash
pip install Pillow
```

### 3. Optional brand font

The renderer automatically chooses a common bold system font. Pass `--font /path/to/font.ttf` to use a brand font or a locale-specific fallback. Only distribute fonts whose licenses permit redistribution.

### 4. Image Generation

The generation phase uses Codex's built-in `imagegen` skill and `image_gen` tool. No external image-generation MCP server is required.

## Usage

From within your app's project directory, run:

```text
Use $aso-appstore-screenshots to plan and generate screenshots for this app.
```

The skill will guide you through each phase interactively. Progress is saved to Codex memory, so you can resume across conversations.

## How It Works

### Sketch template pipeline

When Sketch MCP is available, the skill creates one editable `.sketch` template containing the approved base localization and separate iPhone and iPad panorama masters. Other locales render from temporary copies by replacing stable text and simulator-screenshot slots; Sketch exports the final App Store PNG slices directly.

The template remains the design source of truth. Localized pages do not accumulate in it unless a designer explicitly asks to retain one for hand-tuning.

### Raster fallback

When Sketch MCP is unavailable or flattened output is explicitly requested, the skill uses a two-stage approach:

1. **compose.py** creates a deterministic scaffold with exact text positioning, device frame, and your simulator screenshot composited inside
2. Codex's built-in **imagegen** workflow enhances the scaffold — adding a polished device frame, breakout elements, and visual polish

This keeps layout deterministic while letting AI handle optional creative enhancement. The renderer can also be used without image generation.

### Quick start

```bash
python3 compose.py \
  --layout regular \
  --bg-top "#5B21B6" --bg-bottom "#DB2777" \
  --verb "TRACK" --desc "YOUR DAILY PROGRESS" \
  --screenshot path/to/simulator.png \
  --output screenshots/01-track-progress.png
```

Add verified social proof only when its source is supportable:

```bash
python3 compose.py \
  --layout social-proof-vstack \
  --bg "#2563EB" \
  --verb "BUILD" --desc "BETTER HABITS" \
  --proof '{"kind":"ratings","top":"4.8","bottom":"RATING","source":"verified store data","verified_on":"2026-01-15"}' \
  --screenshot path/to/simulator.png \
  --output screenshots/01-build-better-habits.png
```

The bundled renderer outputs 1284×2778 RGB PNGs, an accepted iPhone 6.5-inch size. Verify [Apple's current screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications) before producing or uploading other display classes. Do not stretch the bundled iPhone frame into an iPad shape.

### Output

Screenshots are saved to a `screenshots/` directory in your project:

```
screenshots/
  01-benefit-slug/          ← working versions
    scaffold.png            ← deterministic compose.py output
    scaffold.aso.json       ← reusable layout, background, typography, and proof state
    v1.png, v2.png, v3.png  ← AI-enhanced versions
    v1-resized.png, ...     ← cropped to App Store dimensions
  final/                    ← approved screenshots, ready to upload
    01-benefit-slug.png
    01-benefit-slug.aso.json
    02-benefit-slug.png
  showcase.png              ← preview image with all screenshots
```

The `final/` folder contains approved screenshots and their manifests. Verify dimensions against the intended App Store slot before upload.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | The skill prompt — defines the multi-phase workflow |
| `compose.py` | Deterministic scaffold generator (Pillow-based) |
| `generate_frame.py` | Generates the device frame template |
| `showcase.py` | Generates the side-by-side showcase image |
| `assets/device_frame.png` | Pre-rendered iPhone device frame template |
| `assets/laurel.png` | Mirrored branch used for verified social proof |
| `references/layouts-and-state.md` | Layout and manifest contract |
| `references/localization-and-qa.md` | Storefront localization and visual QA checklist |
| `references/sketch-template-workflow.md` | Editable Sketch template, localization, panorama, and slice-export workflow |

## License

MIT
