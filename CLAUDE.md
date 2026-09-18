# CLAUDE.md

This file provides guidance to coding agents working with this repository. The filename is kept for compatibility with the upstream project.

## What This Is

A Codex skill (`aso-appstore-screenshots`) that guides users through creating high-converting App Store screenshots. It is invoked via the `/aso-appstore-screenshots` command from within a user's app project.

## Architecture

The core files are:

- **SKILL.md** — The skill prompt. Defines a multi-phase workflow: Benefit Discovery → Evidence-Visual Pairing → Storyboard and Set Direction → Generation → Full-Set Review. The four-principle constitution governs category clarity, first-frame action, attention hierarchy, and second-frame result. Uses the app project's `screenshots/aso-state.json` to persist state across conversations so users can resume mid-workflow. Sketch MCP is the primary editable generation path; compose.py remains the raster fallback.
- **references/sketch-template-workflow.md** — Defines the single-template Sketch workflow, separate iPhone and iPad panorama masters, temporary localization copies, stable replacement keys, slice export, and QA.
- **compose.py** — Deterministically renders the `regular` and `social-proof-vstack` layouts and writes a sibling `.aso.json` manifest with resolved parameters, background, source paths, and social-proof configuration.
- **references/layouts-and-state.md** — Defines the Sketch composition toolbelt, layout selection criteria, storyboard and contact-sheet review, raster defaults, background forms, social-proof decisions, evidence memory, and the per-screenshot manifest contract.
- **references/localization-and-qa.md** — Defines cross-storefront typography, alignment, spacing, and visual approval checks.
- **generate_frame.py** — Generates the device frame template PNG (`assets/device_frame.png`). Run once to create or update the template. The template is a tall device-frame RGBA PNG with a black iPhone body, transparent screen cutout, Dynamic Island, and side buttons.
- **showcase.py** — Generates a showcase image showing up to 3 final screenshots side-by-side with an optional GitHub link at the bottom. Used as the final step after all screenshots are approved.
- **assets/device_frame.png** — Pre-rendered iPhone device frame template used by compose.py. Using a template instead of drawing the frame at compose time ensures pixel-perfect consistency across all generated screenshots.
- **assets/laurel.png** — Approved single-branch laurel shape mirrored by compose.py around verified social-proof claims.

## Verification

Install `requirements.txt`, then run `python check.py`. CI runs the same command. Use `check.py --state` for saved app projects. See `evals/constitution.md` for decision-policy evaluations; mechanical checks cannot establish visual appeal.

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

- **Set direction before panel polish**: Save the storyboard and shared visual system; approve a rough full-set contact sheet, then review all final exports together at storefront size. The up-to-three-panel showcase is not a substitute.
- **Sketch layout variety**: Use native layers for photo heroes, device-first panels, enlarged results, breakouts, proof-led panels, and connected compositions. Panel backgrounds and geometry may vary within the approved identity. `compose.py` retains its two presets; `--breakout` saves metadata rather than rendering a crop.
- **Two-stage raster generation**: compose.py creates a deterministic scaffold first (text + frame + screenshot), then Codex imagegen enhances it. This avoids the inconsistencies of generating from scratch.
- **compose.py outputs an accepted iPhone screenshot size** (1284×2778 for the 6.5-inch slot). Verify Apple's current display requirements before rendering other device classes.
- **Device frame is a template image** (`assets/device_frame.png`) — not drawn at compose time. Regenerate with `python3 generate_frame.py` if the frame design needs updating.
- **Text auto-sizes and wraps** — supports whitespace-delimited languages and character wrapping for CJK copy.
- **Fonts are portable** — a common system bold font is selected automatically; brand and locale fonts can be supplied explicitly.
- **The raster workflow generates 3 versions** for each benefit so the user can pick the best one.
- **Raster finalization** — `finalize.py` creates exact-size opaque images and sibling manifests, retaining intended scaffold geometry as reference rather than claiming it describes generated pixels. See `references/raster-workflow.md`.
- **Project-local state** — benefits, captures, pairings, styling, storyboard, approvals, and exports live in `screenshots/aso-state.json`. Optional memory is a pointer, not the canonical record. Validate referenced artifacts before resuming.
- **Each raster image has a manifest** — preserve and update the sibling `.aso.json` instead of re-estimating layout or background values during iterations.
