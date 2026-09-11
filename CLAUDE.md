# CLAUDE.md

This file provides guidance to coding agents working with this repository. The filename is kept for compatibility with the upstream project.

## What This Is

A Codex skill (`aso-appstore-screenshots`) that guides users through creating high-converting App Store screenshots. It is invoked via the `/aso-appstore-screenshots` command from within a user's app project.

## Architecture

The core files are:

- **SKILL.md** — The skill prompt. Defines a multi-phase workflow: Benefit Discovery → Screenshot Pairing → Generation. Uses Codex memory to persist state across conversations so users can resume mid-workflow. Sketch MCP is the primary editable generation path; compose.py remains the raster fallback.
- **references/sketch-template-workflow.md** — Defines the single-template Sketch workflow, separate iPhone and iPad panorama masters, temporary localization copies, stable replacement keys, slice export, and QA.
- **compose.py** — Deterministically renders the `regular` and `social-proof-vstack` layouts and writes a sibling `.aso.json` manifest with resolved parameters, background, source paths, and social-proof configuration.
- **references/layouts-and-state.md** — Defines layout defaults, background forms, social-proof decisions, evidence memory, and the per-screenshot manifest contract.
- **references/localization-and-qa.md** — Defines cross-storefront typography, alignment, spacing, and visual approval checks.
- **generate_frame.py** — Generates the device frame template PNG (`assets/device_frame.png`). Run once to create or update the template. The template is a tall device-frame RGBA PNG with a black iPhone body, transparent screen cutout, Dynamic Island, and side buttons.
- **showcase.py** — Generates a showcase image showing up to 3 final screenshots side-by-side with an optional GitHub link at the bottom. Used as the final step after all screenshots are approved.
- **assets/device_frame.png** — Pre-rendered iPhone device frame template used by compose.py. Using a template instead of drawing the frame at compose time ensures pixel-perfect consistency across all generated screenshots.
- **assets/laurel.png** — Approved single-branch laurel shape mirrored by compose.py around verified social-proof claims.

## Running compose.py

```bash
# Requires: pip install Pillow
# Optional: pass --font /path/to/brand-or-locale-font.ttf

python3 compose.py \
  --layout regular \
  --bg "#E31837" \
  --verb "TRACK" \
  --desc "TRADING CARD PRICES" \
  --screenshot path/to/simulator.png \
  --output output.png
```

## Key Design Decisions

- **Two-stage generation**: compose.py creates a deterministic scaffold first (text + frame + screenshot), then Codex imagegen enhances it. This avoids the inconsistencies of generating from scratch.
- **compose.py outputs an accepted iPhone screenshot size** (1284×2778 for the 6.5-inch slot). Verify Apple's current display requirements before rendering other device classes.
- **Device frame is a template image** (`assets/device_frame.png`) — not drawn at compose time. Regenerate with `python3 generate_frame.py` if the frame design needs updating.
- **Text auto-sizes and wraps** — supports whitespace-delimited languages and character wrapping for CJK copy.
- **Fonts are portable** — a common system bold font is selected automatically; brand and locale fonts can be supplied explicitly.
- **SKILL.md generates 3 versions** for each benefit so the user can pick the best one.
- **The crop/resize step in SKILL.md is mandatory** after every `image_gen` call unless the output already verifies at exact App Store Connect dimensions.
- **Memory is central to the workflow** — benefits, screenshot assessments, pairings, brand colour, and generation state are all persisted so users can resume across conversations.
- **Each image has a manifest** — preserve and update the sibling `.aso.json` instead of re-estimating layout or background values during iterations.
