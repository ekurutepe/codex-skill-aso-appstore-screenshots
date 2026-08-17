# Layouts and reproducible screenshot state

Read this file before selecting a screenshot layout, rendering a scaffold, or resuming an existing screenshot set.

## Layout selection

Use one of these named layouts. Do not invent a third layout until the user approves it and it is added here.

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

`desc_line_gap` and `proof_line_gap` mean visible pixel clearance between rendered glyph bounds, not baseline distance. Keep these values constant within a device set. Keep `text_top` fixed across locales; move the device down when localized text needs more vertical room.

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

Prefer at most two wreaths on one screenshot. Keep them supporting the benefit message. Never convert an unverified number into a rounded-up milestone.

## Per-screenshot manifest

Every scaffold and approved final screenshot must have a sibling `<stem>.aso.json`. `compose.py` writes this automatically. Copy and update the manifest alongside imagegen variants and final files.

The manifest is the source of truth for future iterations and must contain:

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
