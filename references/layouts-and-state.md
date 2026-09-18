# Layouts and reproducible screenshot state

Read this file before selecting a screenshot layout, rendering a scaffold, or resuming an existing screenshot set.

## Layout selection

Choose the layout that best satisfies the constitution and the panel's communication role. Repetition is allowed; variety must improve comprehension or visual rhythm.

## Set planning and review

Before generation, save the ordered storyboard and shared visual system. For each panel record its role (category/action, result, additional benefit, or proof), headline, evidence visual, layout, reason, exact background, and artwork layers. Preserve a conversion-positive treatment as a testable component where it does not conflict with the constitution; disclose conflicts rather than silently replacing a winner.

Review a rough full-set contact sheet at storefront size before polishing, and the complete exported set before final approval:

- Frame one makes the category and main action understandable; frame two shows what that action returns.
- Each panel has a clear headline and evidence visual; badges and branding attract less attention.
- Relevant UI is legible without reading every tiny label. Essential meaning survives when a panel is viewed alone.
- Typography, palette, margins, device styling, and artwork form one identity. Vary density and background deliberately; avoid adjacent panels competing at maximum intensity.
- Every later panel adds a distinct reason to download. Do not add decoration solely to avoid repetition.

## Composition toolbelt (Sketch)

These are supported design instructions implemented with native Sketch text, image, mask, shape, symbol, and shadow layers, not additional `compose.py` CLI presets. Use the Sketch workflow for these layouts; do not claim raster support or silently substitute a preset when Sketch is unavailable.

| Layout | Choose when | Composition |
|---|---|---|
| `photo-hero` | Context or a person using the product explains the main action faster than UI alone | Large contextual photo or cutout plus recognizable category headline; device optional; proof secondary. Avoid generic mood photography. |
| `device-first` | The screen is the strongest evidence, with copy clearer below or beside it | Prominent device placed high; headline below or alongside; add a foreground fade only where needed for copy contrast. |
| `ui-result` | The returned result is too small in a full device | Enlarge an actual result card, crop, or grouped section as the hero; device optional or supporting. Keep original content intact. |
| `device-breakout` | One UI section deserves emphasis while retaining screen context | Device plus an enlarged source UI panel and soft shadow. Keep its orientation and relation to the source clear. |
| `proof-led` | Verified credibility adds value after the opening action/result pair | Clear verified claim with laurels or rating treatment; app imagery optional and supporting. |
| `connected` | Adjacent panels clarify a relationship or progression | One master composition with artwork or devices crossing slice boundaries; each panel remains understandable alone. |

Layer tools may be combined with these layouts:

- **Foreground artwork:** use supplied or appropriately sourced imagery; isolate people/objects using a prepared transparent cutout or native mask. Record asset paths and front/behind-device ordering. Do not pretend Sketch itself performs automatic background removal.
- **Foreground fades:** use native transparent-to-colour gradient shapes above artwork/device and below copy. Preserve the UI that proves the benefit.
- **Headline emphasis:** native text colour ranges may emphasize category or benefit words using the shared palette; maintain a clear hierarchy.
- **Feature badges:** reuse a small editable text/icon component when it clarifies the feature. Keep it secondary; avoid unverified endorsement cues.
- **Panel backgrounds:** allow approved palette variants, contextual map imagery, or photography within the shared visual system. Record every treatment.

Name artwork and badge slots semantically when they vary by locale, just as text and app screenshot slots do. Use localized assets where required.

## Raster presets

`compose.py` implements only the following two presets. Their geometry is a renderer starting point, not a requirement for all Sketch compositions. It always renders a device and white, centered text. `--breakout` stores metadata only; imagegen supplies the current raster breakout treatment. Use `--text-transform none` for sentence-case copy. If the presets cannot communicate the opening category/action/result clearly, disclose the limitation and select a capable workflow rather than violating the constitution.

### `regular`

Use for the default benefit frame:

1. Primary title/action verb
2. Benefit subtitle
3. Device screenshot, high on the canvas and bleeding below the bottom edge

Default parameters for 1284×2778:

```json
{
  "text_top": 200,
  "device_y": 720,
  "device_width": 1030,
  "verb_size_max": 256,
  "verb_size_min": 150,
  "desc_size": 124,
  "desc_size_min": 72,
  "max_verb_width": 1181,
  "max_text_width": 1181,
  "verb_desc_gap": 44,
  "desc_line_gap": 40
}
```

### `social-proof-vstack`

Use when verified social proof should support the main benefit without replacing it:

1. Primary title/action verb
2. Benefit subtitle
3. One or two laurel wreaths
4. Device screenshot, lowered so its most relevant upper content remains visible

The title and subtitle remain dominant. The laurels must have generous horizontal clearance around their text.

Default parameters for 1284×2778:

```json
{
  "text_top": 163,
  "device_y": 1115,
  "device_width": 1080,
  "verb_size_max": 335,
  "verb_size_min": 250,
  "desc_size": 104,
  "desc_size_min": 72,
  "max_verb_width": 1040,
  "max_text_width": 1080,
  "verb_desc_gap": 44,
  "desc_line_gap": 40,
  "proof_top": 625,
  "proof_badge_width": 520,
  "proof_gap": 80,
  "proof_text_width": 300,
  "proof_center_y": 815,
  "proof_line_gap": 18,
  "laurel_height": 330,
  "laurel_outset": 18
}
```

Treat these as starting values. When the user approves an adjustment, save the resolved values in that screenshot's manifest and reuse those values for later iterations of the same frame.

`desc_line_gap` and `proof_line_gap` mean visible pixel clearance between rendered glyph bounds, not baseline distance. Keep these values stable for the same approved panel across locales. Keep that panel's `text_top` fixed across locales; move the device down when localized text needs more vertical room.

## Backgrounds

Record one of these background forms in every manifest:

- `solid`: exact hex colour.
- `vertical-gradient`: exact top and bottom hex colours.
- `image`: absolute path to the exact reusable background image.
- `reference-edge-gradient`: approved screenshot path plus sampled edge width. Use this when the approved background must be recovered without including its foreground content.

Never estimate a background from memory when an approved screenshot or saved manifest exists. Reuse the saved background specification.

## Social-proof decision

Eligible proof includes:

- Download or install milestones
- Rating average and/or rating count
- App Store or Apple editorial features
- Verifiable awards or press recognition

Only render a claim when its exact wording and evidence are supportable. For each candidate, remember:

```json
{
  "kind": "downloads | ratings | app-store-feature | award | press | custom",
  "top": "4.8",
  "bottom": "RATING",
  "source": "analytics report or public source",
  "verified_on": "YYYY-MM-DD",
  "localizations": {"en-US": {"top": "4.8", "bottom": "RATING"}},
  "decision": "include | omit",
  "decision_reason": "user preference, experiment evidence, or ASO rationale"
}
```

If the stored evidence and prior user decision make inclusion clear, follow them. Otherwise ask one concise question before generation that resolves all missing facts: whether to include laurels and the exact verified claims/wording to use. Save the answer, including an explicit decision to omit social proof. Do not ask again unless the evidence, wording, locale, or user preference changes.

Prefer at most two wreaths on one screenshot. Keep them supporting the benefit message in action/result frames; a dedicated proof-led panel belongs after those frames. Never convert an unverified number into a rounded-up milestone.

## Per-screenshot manifest

Every raster scaffold and approved raster final screenshot must have a sibling `<stem>.aso.json`. `compose.py` writes this automatically. Copy and update the manifest alongside imagegen variants and final files.

The manifest is the source of truth for future raster iterations. Scaffold manifests describe intended geometry; finalization retains that under `reference_geometry` and records real output dimensions plus processing transforms. Generated output geometry remains unverified until measured. Manifests must contain:

- Canvas dimensions
- Named layout and all resolved layout parameters
- Exact background specification
- Title, subtitle, locale, and font path
- Resolved text lines, visible title top, line gaps, and text bottom
- Device frame path, position, width, Dynamic Island geometry when applicable, and simulator screenshot path
- Social-proof mode, laurel asset, exact claims, evidence, localization, and include/omit decision
- Proof line gap and the measured text bounds inside each badge
- Breakout source crop, output position, size, corner radius, and shadow when used
- Font path and text transformation; add shaping metadata when a locale-specific renderer uses it
- Style-template path and imagegen variant when applicable

Before changing an existing screenshot, read its manifest first. Preserve every stored value except the fields the user explicitly asks to change. If an old screenshot has no manifest, measure or inspect it once, create the manifest, and then stop guessing.

## Renderer examples

Regular:

```bash
python3 compose.py --layout regular --bg "#E31837" \
  --verb "PLAN" --desc "BEFORE THE LIGHT IS GONE" \
  --screenshot source.png --output 02-plan.png
```

Social-proof vertical stack:

```bash
python3 compose.py --layout social-proof-vstack --bg-top "#D92700" --bg-bottom "#F36A13" \
  --verb "TRACK" --desc "YOUR DAILY PROGRESS" \
  --proof '{"kind":"ratings","top":"4.8","bottom":"RATING","source":"verified store data","verified_on":"2026-01-15"}' \
  --proof '{"kind":"award","top":"BEST OF","bottom":"2025","source":"verified award page","verified_on":"2026-01-15"}' \
  --screenshot source.png --output 01-track.png
```

## Project state

Store canonical progress in the app project's `screenshots/aso-state.json`, not this skill repository. Optional memory only points to that file. Paths in `files`, contact sheets, and exports are relative to the state file's directory; include all captures, artwork, fonts, template, manifests, and other artifacts needed to resume in `files` (absolute external paths are accepted but less portable).

Minimum storyboard state:

```json
{
  "schema_version": 1,
  "status": "draft",
  "renderer": "sketch-template",
  "app": {"name": "Example", "bundle_id": "com.example.app"},
  "visual_system": {"font": "approved brand font", "palette": ["#123456"], "device_treatment": "shared frame"},
  "panels": [
    {"role": "category-action", "headline": "Fish ID", "visual": "capture a fish", "layout": "photo-hero", "reason": "demonstrates identification action"},
    {"role": "result", "headline": "Know your catch", "visual": "actual species result", "layout": "ui-result", "reason": "enlarges the returned identification"}
  ],
  "files": [],
  "exports": [],
  "reviews": {}
}
```

Also save confirmed `benefits`, `screenshot_analysis`, `pairings`, `social_proof`, localized inputs/wording, template path and revision, and per-panel status/background overrides as they become available. Discovery may use `status: discovery` before a complete storyboard exists; do not render until a draft storyboard passes validation. An empty draft file list is only appropriate before collecting assets.

Update state incrementally using a temporary sibling file and atomic replacement. Record explicit user approvals with evidence rather than inferring approval from elapsed time. Validate before resuming and before marking complete:

```bash
python3 "$SKILL_DIR/check.py" --state screenshots/aso-state.json
```

Put every locale/device set in its own directory, with one export per panel. Each export is `{"path": "final/en-US/iphone-6.9/01.png", "size": [1320, 2868]}`. `status: approved` requires exports and both `reviews.direction` and `reviews.final`, each containing `approved: true`, `contact_sheet` (all panels, in order), and specific `notes`. Raster manifests also require approved visual-review notes. Mechanical validation verifies sequence metadata and artifact integrity; actual category clarity, truthful proof, visual appeal, and completeness of a contact sheet require visual review. Do not claim that a passing state check proves these.
