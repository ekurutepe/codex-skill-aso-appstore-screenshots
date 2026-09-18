# Raster workflow

Read only when using the raster fallback. The constitution and approved storyboard in `SKILL.md` govern these rendering mechanics.

### Raster fallback generation — scaffold then imagegen enhance

Generation uses a two-stage approach for consistency:
1. **Stage 1 (Scaffold)**: compose.py creates a deterministic local image with the correct text, device frame, and screenshot. This guarantees consistent layout across all screenshots.
2. **Stage 2 (Enhance)**: The scaffold is edited with the built-in `image_gen` tool, following the `imagegen` skill, to add breakout elements, depth, and visual polish.

**The approved set direction governs the entire set; the first polished screenshot is a rendering reference.** All subsequent screenshots are enhanced using both their own scaffold (for layout) AND the first approved screenshot (for style). This ensures every screenshot in the set has the shared device frame rendering, typography, palette, artwork style, and overall visual quality, while preserving storyboard variations — so when viewed side-by-side in the App Store, they look like a cohesive professional set.

For each benefit + screenshot pair, generate **3 enhanced versions** so the user can pick the best one. In built-in `image_gen` mode, issue one tool call per version. Do not use CLI batch mode unless the user explicitly chooses the imagegen CLI fallback.

**Step 0: Save reusable style state**

Before generating any scaffolds, save the exact background specification, selected layout, any parameter overrides, and the social-proof evidence plus include/omit decision. Reuse an existing screenshot manifest when iterating instead of estimating values again.

**Step 1: Create the scaffold with compose.py**

The compose.py script lives in the skill directory. Run it to create the deterministic base screenshot.

Before running the command, resolve `SKILL_DIR` to the absolute path of the installed `aso-appstore-screenshots` skill directory, i.e. the directory that contains this `SKILL.md` and `compose.py`.

Batch independent scaffolds when practical. Example:

```bash
SKILL_DIR="[absolute path to this skill directory]" && \
mkdir -p screenshots/01-[benefit-slug] screenshots/02-[benefit-slug] screenshots/03-[benefit-slug] && \
python3 "$SKILL_DIR/compose.py" \
  --layout regular \
  --bg "[HEX CODE]" --verb "[VERB 1]" --desc "[DESC 1]" \
  --screenshot [path/to/screenshot-1.png] \
  --output screenshots/01-[benefit-slug]/scaffold.png && \
python3 "$SKILL_DIR/compose.py" \
  --layout regular \
  --bg "[HEX CODE]" --verb "[VERB 2]" --desc "[DESC 2]" \
  --screenshot [path/to/screenshot-2.png] \
  --output screenshots/02-[benefit-slug]/scaffold.png && \
python3 "$SKILL_DIR/compose.py" \
  --layout regular \
  --bg "[HEX CODE]" --verb "[VERB 3]" --desc "[DESC 3]" \
  --screenshot [path/to/screenshot-3.png] \
  --output screenshots/03-[benefit-slug]/scaffold.png
```

This outputs pixel-perfect 1284×2778 PNGs with:
- Bold white headline text (verb auto-sized to fit canvas width)
- iPhone device frame (from pre-rendered template)
- Simulator screenshot composited inside the frame
- The selected reproducible background specification
- A sibling `.aso.json` manifest containing the named layout, all resolved parameters, exact background, source paths, typography, device placement, and social-proof configuration

For a verified proof frame, use `--layout social-proof-vstack`, repeat `--proof` once or twice, and pass any approved parameter overrides. See `references/layouts-and-state.md` for the exact command and claim schema.

The scaffolds are internal intermediates — do NOT show them to the user or ask for confirmation. Proceed immediately to Step 2 (imagegen enhancement).

**Step 2: Enhance with imagegen (3 versions)**

Use the built-in `image_gen` tool from the `imagegen` skill. For each version:

- If the edit target is a local scaffold file, first inspect it with `view_image` so it is visible in the conversation context.
- For subsequent screenshots, also inspect the first approved screenshot with `view_image` so it is visible as the style template.
- Call `image_gen` with the appropriate prompt template below.
- The built-in tool saves generated images under `$CODEX_HOME/generated_images/...` by default. Move or copy each generated file into the project immediately after generation:
  - `./screenshots/01-[benefit-slug]/v1.png`
  - `./screenshots/01-[benefit-slug]/v2.png`
  - `./screenshots/01-[benefit-slug]/v3.png`
- Never leave a project-bound generated screenshot only under `$CODEX_HOME/generated_images/...`.
- Copy the scaffold manifest beside each generated variant and add the style-template path plus variant identifier. The image and manifest always travel together.
- If the generated output already has exact target dimensions, keep it as-is. Otherwise crop/resize it in Step 3 before review.

#### First screenshot (no approved template yet)

Use only the scaffold as input:
- Inspect `screenshots/01-[benefit-slug]/scaffold.png` with `view_image` before calling `image_gen`.

**First screenshot prompt template:**

```
Use case: ads-marketing
Asset type: App Store screenshot
Input image: The visible scaffold image is the edit target.
Primary request: Transform the scaffold into a polished, professional App Store marketing screenshot that would make someone tap Download.

KEEP EXACTLY AS-IS:
- The headline text (wording, position, and approximate size)
- The app screenshot shown on the phone screen
- The background colour
- The portrait composition and approximate layout
- Any approved social-proof copy and laurel treatment described below

[SOCIAL PROOF — exact verified claim, localized wording, and laurel placement, or "None"]

ENHANCE AND POLISH:
- Refine the device frame into a sleek modern iPhone mockup with accurate proportions, reflections, and subtle shadows. Keep the same position and size as the scaffold.
- Refine the overall visual quality to look like a professional, high-budget App Store screenshot
- OPTIONALLY add a PRIMARY breakout element — but ONLY if there is an obvious, visually compelling UI panel on the app screen that directly relates to the benefit headline. If nothing on screen clearly reinforces the headline, skip the breakout entirely — a clean screenshot with no breakout is better than a forced one. When you DO add a breakout, it MUST be an entire UI panel or grouped section (e.g., a complete card with its title and content, a full list section, a complete dialog/sheet) — never individual small elements like a single button, icon, or colour dot. IMPORTANT: The panel must stay at the SAME vertical position and orientation as where it appears on screen — do NOT rotate or angle it. The panel must be SCALED UP significantly — rendered much larger than it appears on the phone screen — so that it extends dramatically beyond BOTH left and right edges of the device frame, clearly overlapping the phone bezel on both sides, expanding to nearly the full width of the screenshot canvas. Do NOT keep the panel at its original on-screen size with just padding added around it. The panel itself must be enlarged. It should appear to float in front of the device at this larger scale — add a soft drop shadow beneath it to create depth and sell the hovering effect. The panel must look like it came from the app — same colours, same style, same content. Do NOT invent new elements.
[PRIMARY BREAKOUT — if a relevant panel is obvious, describe the specific UI panel visible on screen and instruct it to extend beyond both edges of the device frame with a drop shadow, e.g., "The [panel name] card/row extends beyond both left and right edges of the device frame, overlapping the phone bezel on both sides, expanding to nearly the full screenshot width. It floats in front of the device with a soft drop shadow beneath it." If no panel clearly relates to the headline, write "No breakout — the app screen speaks for itself."]
- Optionally add 1-2 secondary elements that reinforce the benefit and message of the screenshot — the kind of enhancements a professional graphic designer would add for impact. These are NOT from the app UI; they are creative additions that help clearly communicate what the screenshot is trying to portray to the user browsing the App Store. They should carry the message and support ASO conversion, but never at the cost of the overall design aesthetic. They must not compete with the primary breakout for attention.
[SECONDARY ELEMENTS (optional) — describe 0-2 small supporting elements that tell the story, or "None needed"]
- Preserve the exact background specification recorded in the scaffold manifest. Do not add unrecorded glows, gradients, radial patterns, or light effects.
- Ensure the text is crisp, bold, and highly readable
- Avoid watermarks, unapproved extra text, invented UI content, App Store UI chrome, or changing the app screenshot content. Preserve any approved, verified social-proof claim and laurel treatment specified in the scaffold or prompt.

The final result should look like it was designed by a professional App Store screenshot agency — polished, high-converting, and visually striking. No watermarks, no unapproved extra text, no app store UI chrome. Approved social-proof copy and laurels are intentional exceptions.
```

#### Subsequent screenshots (after first is approved)

Use **two images** as input:
1. Inspect the **scaffold** for this benefit (`screenshots/0N-[benefit-slug]/scaffold.png`) with `view_image` — defines the layout
2. Inspect the **first approved screenshot** (`screenshots/final/01-[first-benefit-slug].png`) with `view_image` — defines the style template

**Subsequent screenshot prompt template:**

```
Use case: ads-marketing
Asset type: App Store screenshot
Input images: First visible image is the scaffold edit target; second visible image is the style template reference.
Primary request: Create the next screenshot in an App Store screenshot set, matching the approved style while using the scaffold's exact content and layout.

You are creating the next screenshot in an App Store screenshot SET. It must look like it belongs to the same series as the style reference.

TWO REFERENCE IMAGES:
- FIRST image: The SCAFFOLD — use this as the definitive guide for layout: headline text wording/position, device frame placement, and the app screenshot on screen. This defines WHAT this screenshot shows.
- SECOND image: The STYLE TEMPLATE — this is an already-approved screenshot from the same set. Match its visual style EXACTLY: shared device styling, typography, palette, accents, and level of polish. Preserve the target panel's approved layout and background rather than copying the reference panel's composition. This defines HOW this screenshot should look. When references conflict, preserve the approved storyboard and target scaffold geometry.

REQUIREMENTS:
- CRITICAL: The device frame MUST match the style template EXACTLY — same photorealistic iPhone component, shadows, reflections, and edge treatment. Use the target scaffold's approved size and position. Do NOT reinvent or reimagine the device frame. Preserve the component appearance while following the target scaffold's geometry and screen contents.
- Match the style template's text rendering style (same font treatment, same crispness, same visual weight)
- Match the exact background specification in the target scaffold manifest. Do not invent additional effects.
- Use the scaffold's layout for positioning (text, device, screenshot placement); it takes precedence over reference-panel geometry
- Preserve the approved social-proof treatment from the scaffold or style template when specified.
[SOCIAL PROOF — exact verified claim, localized wording, and laurel placement, or "None"]
- OPTIONALLY add a PRIMARY breakout element — but ONLY if there is an obvious, visually compelling UI panel on the app screen that directly relates to the benefit headline. If nothing clearly reinforces the headline, skip the breakout entirely. When used, it MUST be an entire UI panel or grouped section (NOT individual small elements like a single button or icon). The panel must stay at the SAME vertical position and orientation as on screen — do NOT rotate or angle it. The panel must be SCALED UP significantly — rendered much larger than it appears on the phone screen — so that it extends dramatically beyond BOTH left and right edges of the device frame, clearly overlapping the phone bezel on both sides, expanding to nearly the full width of the screenshot canvas. Do NOT keep the panel at its original on-screen size. The panel itself must be enlarged. It should appear to float in front of the device at this larger scale — add a soft drop shadow beneath it to create depth. The panel MUST come from the app screenshot — same colours, same style, same content. Do NOT invent new elements.
[PRIMARY BREAKOUT — if a relevant panel is obvious, describe the specific UI panel visible on screen to pop out with a drop shadow, extending beyond both device frame edges. Otherwise write "No breakout — the app screen speaks for itself."]
- Optionally add 1-2 secondary elements that reinforce the benefit and message of the screenshot — the kind of enhancements a professional graphic designer would add for impact. These are NOT from the app UI; they are creative additions that help clearly communicate what the screenshot is trying to portray to the user browsing the App Store. They should carry the message and support ASO conversion, but never at the cost of the overall design aesthetic. They must not compete with the primary breakout for attention.
[SECONDARY ELEMENTS (optional) — 0-2 small supporting elements that tell the story, or "None needed"]
- The breakout elements should match the style and energy level of those in the style template
- Avoid watermarks, unapproved extra text, invented UI content, App Store UI chrome, or changing the app screenshot content. Preserve any approved, verified social-proof claim and laurel treatment specified in the scaffold or style template.

The result must look like it was designed alongside the style template as part of the same professional set. When placed side-by-side in the App Store, they should be visually cohesive — shared quality and design language, with the approved composition variations.

No watermarks, no unapproved extra text, no app store UI chrome. Approved social-proof copy and laurels are intentional exceptions.
```

**IMPORTANT — Consistency enforcement**: The scaffold guarantees consistent layout. The style template guides consistent visual treatment. If imagegen changes the text, layout, app UI content, or deviates from the style template, regenerate with a stricter prompt.

Before every iteration, read that screenshot's `.aso.json` first. Preserve the named layout, background, and resolved parameters unless the user explicitly requests a change; then update only those fields in the next manifest.

**Step 3: Finalize each variant and its manifest**

Run `finalize.py` on each imagegen output with the scaffold manifest. It handles both wider and narrower aspect ratios, creates an opaque exact-size PNG and sibling manifest, and records the crop and scale. It never overwrites existing artwork. Use a new version path for each iteration.

```bash
python3 "$SKILL_DIR/finalize.py" screenshots/01-benefit/v1.png screenshots/01-benefit/v1-resized.png --manifest screenshots/01-benefit/scaffold.aso.json
python3 "$SKILL_DIR/finalize.py" screenshots/01-benefit/v2.png screenshots/01-benefit/v2-resized.png --manifest screenshots/01-benefit/scaffold.aso.json
python3 "$SKILL_DIR/finalize.py" screenshots/01-benefit/v3.png screenshots/01-benefit/v3-resized.png --manifest screenshots/01-benefit/scaffold.aso.json
```

Scaffold geometry is stored under `reference_geometry`; it is not a measurement of generated artwork. Inspect every finalized image for UI fidelity, clipping, line breaks, and attention hierarchy. Record `visual_review: {"approved": true, "notes": "specific inspection findings"}` in its manifest only after review. Add actual measured `observed_geometry` and set `geometry_verified: true` only when measured; never relabel intended coordinates as observed. Do not show unverified raw outputs as final screenshots.

**Step 4: Review all 3 versions with the user**

Present all 3 **resized** versions (the `-resized.png` files) to the user using `view_image`. Never show an unverified raw generated output — always show exact-dimension post-processed versions.

Label them clearly as **Version 1**, **Version 2**, and **Version 3** and ask the user to pick their favourite or request changes.

**Step 5: Iterate if needed**

If the user wants changes, inspect **three images** with `view_image`, then call `image_gen`:
1. The **scaffold** (`scaffold.png`) — anchors the layout (text position, device placement, screenshot)
2. The **style template** (the first approved screenshot from `screenshots/final/01-*.png`) — defines the device frame rendering and overall visual style that must be consistent across the entire set
3. The **approved design** (the version the user liked best for this specific screenshot) — anchors the creative direction and breakout element approach

The prompt should reference all three:
```
Use case: ads-marketing
Asset type: App Store screenshot iteration
Input images: First visible image is the scaffold; second visible image is the set-wide style template; third visible image is the approved design direction.

Here are three reference images, each with a distinct purpose:

- FIRST image: The SCAFFOLD — use this as the definitive guide for layout: text position, device frame placement, and the app screenshot on screen. This defines WHERE everything goes.
- SECOND image: The STYLE TEMPLATE — this is the first approved screenshot in the set. Use its shared device styling, typography, palette, and quality while preserving the target panel's approved layout and background. This defines HOW the screenshot should look to maintain consistency across the set.
- THIRD image: The APPROVED DESIGN DIRECTION — this is the version the user liked best for this specific screenshot. Match its creative direction, breakout element approach, and secondary elements.

Generate a new version that keeps the layout from the scaffold, the device frame and visual style from the style template, and the creative direction from the approved design, with these changes:
[USER'S REQUESTED CHANGES]
```

This prevents drift (scaffold keeps layout locked), maintains set-wide consistency (style template keeps device frame and visual treatment identical), and preserves the creative direction the user already approved.

When iterating, generate **3 versions** again with built-in `image_gen`. Then finalize and inspect all variants as described in Step 3 before showing the user.

Repeat until the user is happy.

**Step 6: Copy approved version to `final/`**

Once the user picks a winner, copy the resized version to `screenshots/final/`:

```bash
python3 "$SKILL_DIR/finalize.py" screenshots/01-benefit/v2-resized.png screenshots/final/01-benefit.png
```

The final image and sibling manifest now both point to the final path. Save the approved export, size, and review evidence in project state, then run `check.py --state screenshots/aso-state.json`.

This keeps `final/` clean — only approved, App Store-ready screenshots, one per benefit, numbered in order. Then move to the next benefit.


### Raster fallback output

Save generated screenshots to a `screenshots/` directory in the project root, organised by benefit subfolder:

```
screenshots/
  01-track-card-prices/       ← working versions for benefit 1
    scaffold.png              ← deterministic compose.py output (text + frame + screenshot)
    v1.png                    ← imagegen enhanced version 1
    v1-resized.png            ← cropped/resized to App Store dimensions
    v2.png
    v2-resized.png
    v3.png
    v3-resized.png
  02-search-any-card/         ← working versions for benefit 2
    scaffold.png
    v1.png
    ...
  final/                      ← approved screenshots, ready to upload
    01-track-card-prices.png
    02-search-any-card.png
```

The `final/` folder is the only one the user needs to care about — it contains one approved, App Store-ready screenshot per benefit, numbered in order. The benefit subfolders contain all working versions and can be ignored or deleted after the set is complete.

Also tell the user exactly which App Store Connect display size slot each screenshot fits into.
