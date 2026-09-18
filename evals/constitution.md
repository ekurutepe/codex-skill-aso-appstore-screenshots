# Constitution evaluation

Run after changing the constitution, layout-selection guidance, or generation
workflow. These are behavioral cases, not regex tests or claims about conversion.
Use a fresh agent session for each case, loading this repository's skill.
Do not show the expectations below to the generating agent. Provide only the
case prompt; review its decisions separately. Do not purchase imagery or call
paid generation tools for this planning evaluation.

Save each response and review in a temporary evaluation directory outside the
repository. Record the skill commit, agent/model, supplied tools, proposed
storyboard, and specific findings. Do not record a pass without running the case.

## Cases

### 1. Category before slogan

Prompt: Plan a three-panel screenshot set for an app that photographs a plant
and identifies its species, then gives care instructions. Available assets:
a person photographing a plant, a capture-screen screenshot, a detailed species
result, and a care checklist. Brand palette is forest green and cream. The
suggested opening headline is “Discover the extraordinary.” Provide a storyboard,
layout reasons, and a shared visual system. Planning only; do not generate assets.

Review: Frame one explicitly communicates plant identification and shows the
capture action. Frame two delivers the species result. The agent should challenge
or replace the vague slogan. It may choose photography or actual capture UI;
neither choice is inherently required. Care adds distinct later value.

### 2. Small result, strong proof

Prompt: Plan four screenshots for a receipt-scanning expense app. Available
captures show taking a receipt photo, extracted merchant/date/total in a small
card, categorized spending, and export. A supplied dated report verifies 100,000
downloads; the team wants that claim to occupy the whole first panel. Use navy,
white, and lime. Provide a storyboard and explain your layout choices. Planning
only; do not generate assets.

Review: Category and scanning action remain in frame one, enlarged extraction
result appears in frame two, and proof is secondary there or gets a later panel.
The agent should explain the conflict with the team's requested ordering.
Do not inflate the supplied claim or imply an award. Breakout/crop is justified
by result legibility rather than decoration.

### 3. Renderer limitations and missing localization

Prompt: Plan a localized set for a fish-identification app, in English and German.
Only English captures exist. Sketch tools are unavailable; compose.py and imagegen
are available. The requested compositions are a phone-free photo opener, a bottom
headline over the second phone, and a connected panorama. State what can proceed
and what needs a different workflow or missing input. Planning only.

Review: The agent does not invent raster presets or claim these layouts are
implemented by compose.py. It exposes the renderer tradeoff and requests a
capable workflow or an explicit simpler direction. It does not claim German
marketing copy localizes English text baked into captures. Category/action/result
planning can proceed while affected rendering/localization stays unresolved.

## Review rubric

For each case, record pass/fail and concrete evidence for:

1. Recognizable category receives primary headline emphasis.
2. Frame one demonstrates the main action.
3. Headline/hero take priority; proof, badges, and branding remain secondary.
4. Frame two clearly presents the returned result at an appropriate scale.
5. Layout reasons follow communication needs; the set shares an intentional
   visual system without forced variation.
6. Tool capabilities, missing inputs, and claim evidence are represented honestly.

All six must pass before accepting a changed decision policy. A storyboard pass
does not prove rendering quality: inspect generated full-set contact sheets at
storefront size using the same first five criteria. Record visual failures and
feed them back into a focused regression case or executable check where possible.
