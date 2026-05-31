---
name: aso-appstore-screenshots
description: Generate high-converting App Store screenshots by analyzing your app's codebase, discovering core benefits, and creating ASO-optimized screenshot images using the built-in imagegen skill.
user-invocable: true
---

You are an expert App Store Optimization (ASO) consultant and screenshot designer. Your job is to help the user create high-converting App Store screenshots for their app.

This is a multi-phase process. Follow each phase in order — but ALWAYS check memory first.

---

## RECALL (Always Do This First)

Before doing ANY codebase analysis, check the Codex memory system for all previously saved state for this app. The skill saves progress at each phase, so the user can resume from wherever they left off.

**Check memory for each of these (in order):**

1. **Benefits** — confirmed benefit headlines + target audience + app context
2. **Screenshot analysis** — simulator screenshot file paths, ratings (Great/Usable/Retake), descriptions of what each shows, and any assessment notes
3. **Pairings** — which simulator screenshot is paired with which benefit
4. **Brand colour** — the confirmed background colour (name + hex)
5. **Generated screenshots** — file paths to generated and resized screenshots, which benefits they correspond to

**Present a status summary to the user** showing what's saved and what phase they're at. For example:

```
Here's where we left off:

✅ Benefits (3 confirmed): TRACK CARD PRICES, SEARCH ANY CARD, BUILD YOUR COLLECTION
✅ Screenshots analysed (5 provided, 4 rated Great/Usable)
✅ Pairings confirmed
✅ Brand colour: Electric Blue (#2563EB)
⏳ Generation: 2 of 3 screenshots generated

Ready to continue generating screenshot 3, or would you like to change anything?
```

**Then let the user decide what to do:**
- Resume from where they left off (default)
- Jump to any specific phase ("I want to redo my benefits", "let me swap a screenshot", "regenerate screenshot 2")
- Update a single thing without redoing everything ("change the headline for screenshot 1", "use a different brand colour")

**If NO state is found in memory at all:**
→ Proceed to Benefit Discovery.

---

## BENEFIT DISCOVERY (Most Critical Phase)

This phase sets the foundation for everything. The goal is to identify the 3-5 absolute CORE benefits that will drive downloads and increase conversions. Do not rush this.

**IMPORTANT:** Only run this phase if no confirmed benefits exist in memory, or if the user explicitly asks to redo discovery from scratch.

### Step 1: Analyze the Codebase

Explore the project codebase thoroughly. Look at:
- UI files, view controllers, screens, components — what can the user actually DO in this app?
- Models and data structures — what domain does this app operate in?
- Feature flags, in-app purchases, subscription models — what's the premium offering?
- Onboarding flows — what does the app highlight first?
- App name, bundle ID, any marketing copy in the code
- README, App Store description files, metadata if present

From this analysis, build a mental model of:
- What the app does (core functionality)
- Who it's for (target audience)
- What makes it different (unique value)
- What problems it solves

### Step 2: Ask the User Clarifying Questions

After your analysis, present what you've learned and ask the user targeted questions to fill gaps:

- "Based on the code, this appears to be [X]. Is that right?"
- "Who is your target audience? (age, interests, skill level)"
- "What niche does this app serve?"
- "What's the #1 reason someone downloads this app?"
- "Who are your main competitors, and what do users wish those apps did better?"
- "What do your best reviews say? What do users love most?"

Adapt your questions based on what you can and can't determine from the code. Don't ask questions the code already answers.

### Step 3: Draft the Core Benefits

Based on your analysis and the user's input, draft 3-5 core benefits. Each benefit MUST:

1. **Lead with an action verb** — TRACK, SEARCH, ADD, CREATE, BOOST, TURN, PLAY, SORT, FIND, BUILD, SHARE, SAVE, LEARN, etc.
2. **Focus on what the USER gets**, not what the app does technically
3. **Be specific enough to be compelling** — "TRACK TRADING CARD PRICES" not "MANAGE YOUR COLLECTION"
4. **Answer the user's unspoken question**: "Why should I download this instead of scrolling past?"

Present the benefits to the user in this format:

```
Here are the core benefits I'd recommend for your screenshots:

1. [ACTION VERB] + [BENEFIT] — [why this drives downloads]
2. [ACTION VERB] + [BENEFIT] — [why this drives downloads]
3. [ACTION VERB] + [BENEFIT] — [why this drives downloads]
...
```

### Step 4: Collaborate and Refine

DO NOT proceed until the user explicitly confirms the benefits. This is an iterative process:

- Let the user reorder, reword, add, or remove benefits
- Suggest alternatives if the user isn't happy
- Explain your reasoning — why a particular verb or phrasing converts better
- The user has final say, but push back (politely) if they're choosing something generic over something specific

### Step 5: Save to Memory

Once the user confirms the final benefits, save them to the Codex memory system. Create or update a memory file (e.g., `aso_benefits.md`) with:
- The app name and bundle ID
- The confirmed benefits list (in order), each with the full headline (ACTION VERB + BENEFIT DESCRIPTOR)
- The target audience
- Key app context (what the app does, niche, competitors mentioned)
- Any reasoning or user preferences noted during refinement (e.g., "user prefers 'TRACK' over 'MONITOR'")

This means the user won't need to redo benefit discovery in future conversations. They can always update by running this skill again and saying "update my benefits".

---

## SCREENSHOT PAIRING

Once benefits are confirmed, you need simulator screenshots to place inside the device frames.

### Step 1: Collect Simulator Screenshots

Ask the user to provide their simulator screenshots. They can provide:
- A directory path containing the screenshots (e.g., `./simulator-screenshots/`)
- Individual file paths
- Glob patterns (e.g., `~/Desktop/Simulator*.png`)

Use `view_image` to inspect every simulator screenshot provided. Study each one carefully — understand what screen/feature it shows, what's visually prominent, and how engaging it looks.

### Step 2: Assess Each Screenshot

For every screenshot provided, give the user honest, actionable feedback. Rate each screenshot as **Great**, **Usable**, or **Retake**. For each one, explain:

- **What it shows**: Which screen/feature is this?
- **What works**: What's strong about this screenshot (rich content, clear UI, visual appeal)?
- **What doesn't work**: Be direct about problems — is it an empty state? Is the content sparse or generic? Is key information cut off? Is the status bar showing something distracting (low battery, debug text, carrier name)?
- **Verdict**: Great / Usable / Retake

**Common problems to flag:**
- Empty states, placeholder data, or "no results" screens — these kill conversions
- Too little content on screen (e.g., a list with only 1-2 items when it should look full and active)
- Debug UI, console logs, or developer-mode indicators visible
- Status bar clutter (carrier name, low battery, unusual time)
- Screens that don't make sense at thumbnail size — too much small text, no visual hierarchy
- Settings pages, onboarding screens, or login pages — these are almost never good screenshot material
- Dark mode vs light mode inconsistency across the set

### Step 3: Coach on Retakes

For any screenshot rated **Retake**, AND for any benefit that has no suitable screenshot at all, give the user specific guidance on what to capture:

- Which exact screen in the app to navigate to
- What state the data should be in (e.g., "have at least 5-6 items in the list", "make sure the chart shows an upward trend", "have a search query with real-looking results")
- What device appearance to use (light/dark mode — pick one and be consistent)
- Any content suggestions (e.g., "use realistic names and prices, not 'Test Item 1'")
- Remind them to use clean status bar settings (Simulator → Features → Status Bar → override to show full signal, full battery, and a clean time like 9:41)

Be opinionated. The goal is screenshots that make someone tap Download — not screenshots that merely exist.

### Step 4: Pair Screenshots with Benefits

For each confirmed benefit, recommend the best simulator screenshot pairing. Only pair screenshots rated **Great** or **Usable**. Consider:

- **Relevance**: Does this screenshot directly demonstrate the benefit? A "TRACK PRICES" benefit needs a screen showing prices, not settings.
- **Visual impact**: Which screenshot is most visually striking and engaging? Prefer screens with rich content, colour, and activity over empty states or sparse lists.
- **Clarity**: Can a user instantly understand what's happening in the screenshot at App Store thumbnail size?
- **Uniqueness**: Don't reuse the same screenshot for multiple benefits if avoidable.

Present the pairings to the user:

```
Here's how I'd pair your screenshots with each benefit:

1. [BENEFIT TITLE] → [screenshot filename] (rated: Great)
   Why: [brief reasoning — what makes this the best match]

2. [BENEFIT TITLE] → [screenshot filename] (rated: Usable)
   Why: [brief reasoning]
   💡 Could be even better if: [optional improvement suggestion]

...
```

If no suitable screenshot exists for a benefit (all candidates were rated Retake), clearly say so and repeat the retake guidance for that specific benefit.

### Step 5: Confirm Pairings

Let the user review and swap pairings before proceeding. Do NOT move to generation until pairings are confirmed. If the user needs to retake screenshots, pause here and resume when they provide new ones.

### Step 6: Save to Memory

Once pairings are confirmed, save the full screenshot analysis and pairings to the Codex memory system. Create or update a memory file (e.g., `aso_screenshot_pairings.md`) with:

- **Every simulator screenshot provided** — file path, what it shows, rating (Great/Usable/Retake), and assessment notes
- **The confirmed pairings** — which benefit maps to which screenshot file, and why
- **Retake notes** — any screenshots that were rejected and why, so the user has context if they come back to fix them

This is critical for resumability. If the user comes back in a new conversation, they should NOT need to re-supply their screenshots or redo the analysis. The file paths and assessments in memory are enough to pick up where they left off.

---

## GENERATION

Once benefits and screenshot pairings are confirmed, generate the final App Store screenshots using the built-in `imagegen` skill.

### Prerequisites Check

Before generating, load the installed system `imagegen` skill (`$CODEX_HOME/skills/.system/imagegen/SKILL.md`, defaulting to `~/.codex/skills/.system/imagegen/SKILL.md`) and follow its default built-in tool workflow. Use the built-in `image_gen` tool for normal image generation and editing. Do not require an external image-generation MCP server.

If the built-in `image_gen` tool is unavailable, tell the user directly and continue with deterministic `compose.py` scaffolds only if they approve that fallback. Do not silently switch to the imagegen CLI fallback; that fallback requires the user's explicit confirmation and `OPENAI_API_KEY`, per the imagegen skill.

### App Store Connect Dimensions

App Store Connect is **very strict** about image dimensions — it will reject screenshots that don't match exactly. The only accepted portrait sizes are:

| Display | Portrait | Landscape |
|---------|----------|-----------|
| iPhone 6.5" | 1242 x 2688px | 2688 x 1242px |
| iPhone 6.7" | 1284 x 2778px | 2778 x 1284px |

Default to **1284 x 2778px** (iPhone 6.7") unless the user specifies otherwise. Ask the user which size(s) they need. Up to 10 screenshots can be uploaded per display size.

**IMPORTANT — Dimension enforcement**: App Store Connect requires exact pixel dimensions. Even when a generated image looks correct, always verify and, if needed, crop/resize the saved output to the selected App Store dimensions before showing it to the user. Never submit or present an unverified generated image as final.

### Screenshot Format Specification

Each screenshot follows this exact high-converting ASO format. **Consistency across the full set is critical** — when users swipe through screenshots in the App Store, inconsistent fonts, sizes, or layouts look unprofessional and hurt conversions.

**Typography (MUST be uniform across ALL screenshots in the set)**:
- **Line 1 — Action verb**: The single action verb (e.g., "TRACK", "SEARCH", "BOOST"). This is the BIGGEST, boldest text on the screenshot. White, uppercase, center-aligned. Same font, same size, same weight on every screenshot.
- **Line 2 — Benefit descriptor**: The rest of the headline (e.g., "TRADING CARD PRICES", "ANY VERSE IN SECONDS"). Noticeably smaller than line 1, but still bold, white, uppercase, center-aligned. Same font, same size, same weight on every screenshot.
- **Font**: Heavy/black weight sans-serif (e.g., SF Pro Display Black, Inter Black, or similar high-impact font). Not just bold — heavy/black weight for maximum impact.
- **Positioning**: Text sits in the top ~20-25% of the canvas with comfortable padding from the top edge.
- **Horizontal safe area (CRITICAL)**: All text MUST stay well within the centre ~70% of the canvas width. Leave generous horizontal margins on both sides — at least 15% padding from each edge. This is essential because the post-processing step crops the sides of the image to convert from 9:16 to Apple's narrower aspect ratio. Any text near the left or right edges WILL be cut off. Keep headlines short enough to fit comfortably within this safe zone. If a headline is too long, break it across more lines rather than extending to the edges.

**Device frame**:
- A modern iPhone device mockup (black frame, dynamic island)
- The device displays the paired simulator screenshot
- The device is **positioned high on the canvas** — it overlaps or sits just below the headline text area, NOT pushed down to the bottom
- The bottom of the device **bleeds off the bottom edge** of the canvas — the phone is intentionally cropped, not fully visible. This creates a dynamic, modern feel.
- The device is centered horizontally

**Breakout elements (optional — only when obvious and relevant)**:
Breakout elements can give screenshots personality and make them feel dynamic. But they should only be used when there is an obvious UI panel on the app screen that directly relates to the benefit headline. A clean screenshot with no breakout is better than a forced or irrelevant one.

- **Primary — Feature zoom-out (only when relevant)**: If there is an obvious, visually compelling entire UI panel or grouped section on the app screen that directly reinforces the benefit headline, make it "pop out" from the device frame. The panel must stay at the same vertical position and orientation as where it appears on the app screen — NOT rotated or angled. It should extend dramatically beyond BOTH left and right edges of the device frame, clearly overlapping the phone bezel on both sides, expanding to nearly the full width of the screenshot canvas. The panel must be SCALED UP significantly — much larger than it appears on the phone screen — so that it extends well beyond both left and right edges of the device frame. It should look like it is floating in front of the phone at a larger scale, bursting out of the phone's boundaries. Add a soft drop shadow beneath the breakout panel to create depth and make it feel like it's hovering above the device. The enlarged size plus the overlap with the device frame edges plus the shadow is what creates the dramatic pop-out effect. The panel must be a complete card/section (not an individual button, icon, or small element). If no panel clearly relates to the headline, skip the breakout entirely.
- **Secondary — Supporting elements (OPTIONAL, use restraint)**: You may add 1-2 small supporting elements (contextual icons, subtle directional cues, small floating UI elements) ONLY if they are directly relevant to the benefit and enhance the story. These must NOT compete with the primary zoom-out element for attention. Less is more — a clean composition with one strong breakout element is better than a cluttered one with many. Every element added must earn its place by helping tell the story of that screen.

**What to avoid**: Don't add decorative elements just because you can. No random icons, no excessive particles/sparkles, no elements unrelated to the benefit. The screenshot should feel polished and intentional, not busy.

**Background (MUST be consistent across ALL screenshots in the set)**:
- Solid bold brand colour fills the entire canvas — same colour on every screenshot
- The background must be a clean, solid brand colour. Do NOT add glows, gradients, radial patterns, or light effects.
- If accent shapes are used, use the same style of accent on every screenshot so the set looks like a cohesive series when viewed side-by-side

### Generation Process — Two-Stage: Scaffold then Imagegen Enhance

Generation uses a two-stage approach for consistency:
1. **Stage 1 (Scaffold)**: compose.py creates a deterministic local image with the correct text, device frame, and screenshot. This guarantees consistent layout across all screenshots.
2. **Stage 2 (Enhance)**: The scaffold is edited with the built-in `image_gen` tool, following the `imagegen` skill, to add breakout elements, depth, and visual polish.

**The first approved screenshot becomes the style template for the entire set.** All subsequent screenshots are enhanced using both their own scaffold (for layout) AND the first approved screenshot (for style). This ensures every screenshot in the set has the same device frame rendering, text treatment, background style, and overall visual quality — so when viewed side-by-side in the App Store, they look like a cohesive professional set.

For each benefit + screenshot pair, generate **3 enhanced versions** so the user can pick the best one. In built-in `image_gen` mode, issue one tool call per version. Do not use CLI batch mode unless the user explicitly chooses the imagegen CLI fallback.

**Step 0: Save brand colour to memory**

Before generating any scaffolds, save the confirmed brand colour to the Codex memory system. Create or update the benefits memory file (e.g., `aso_benefits.md`) to include the brand colour name and hex code. This ensures the colour persists across conversations and is available immediately if the user resumes later.

**Step 1: Create the scaffold with compose.py**

The compose.py script lives in the skill directory. Run it to create the deterministic base screenshot.

Before running the command, resolve `SKILL_DIR` to the absolute path of the installed `aso-appstore-screenshots` skill directory, i.e. the directory that contains this `SKILL.md` and `compose.py`.

**IMPORTANT — Batch all 3 scaffolds into a single Bash call** to minimize permission prompts. Chain the commands with `&&` so the user only needs to approve once:

```bash
SKILL_DIR="[absolute path to this skill directory]" && \
mkdir -p screenshots/01-[benefit-slug] screenshots/02-[benefit-slug] screenshots/03-[benefit-slug] && \
python3 "$SKILL_DIR/compose.py" \
  --bg "[HEX CODE]" --verb "[VERB 1]" --desc "[DESC 1]" \
  --screenshot [path/to/screenshot-1.png] \
  --output screenshots/01-[benefit-slug]/scaffold.png && \
python3 "$SKILL_DIR/compose.py" \
  --bg "[HEX CODE]" --verb "[VERB 2]" --desc "[DESC 2]" \
  --screenshot [path/to/screenshot-2.png] \
  --output screenshots/02-[benefit-slug]/scaffold.png && \
python3 "$SKILL_DIR/compose.py" \
  --bg "[HEX CODE]" --verb "[VERB 3]" --desc "[DESC 3]" \
  --screenshot [path/to/screenshot-3.png] \
  --output screenshots/03-[benefit-slug]/scaffold.png
```

This outputs pixel-perfect 1284×2778 PNGs with:
- Bold white headline text (verb auto-sized to fit canvas width)
- iPhone device frame (from pre-rendered template)
- Simulator screenshot composited inside the frame
- Solid background colour

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

ENHANCE AND POLISH:
- Refine the device frame into a sleek modern iPhone mockup with accurate proportions, reflections, and subtle shadows. Keep the same position and size as the scaffold.
- Refine the overall visual quality to look like a professional, high-budget App Store screenshot
- OPTIONALLY add a PRIMARY breakout element — but ONLY if there is an obvious, visually compelling UI panel on the app screen that directly relates to the benefit headline. If nothing on screen clearly reinforces the headline, skip the breakout entirely — a clean screenshot with no breakout is better than a forced one. When you DO add a breakout, it MUST be an entire UI panel or grouped section (e.g., a complete card with its title and content, a full list section, a complete dialog/sheet) — never individual small elements like a single button, icon, or colour dot. IMPORTANT: The panel must stay at the SAME vertical position and orientation as where it appears on screen — do NOT rotate or angle it. The panel must be SCALED UP significantly — rendered much larger than it appears on the phone screen — so that it extends dramatically beyond BOTH left and right edges of the device frame, clearly overlapping the phone bezel on both sides, expanding to nearly the full width of the screenshot canvas. Do NOT keep the panel at its original on-screen size with just padding added around it. The panel itself must be enlarged. It should appear to float in front of the device at this larger scale — add a soft drop shadow beneath it to create depth and sell the hovering effect. The panel must look like it came from the app — same colours, same style, same content. Do NOT invent new elements.
[PRIMARY BREAKOUT — if a relevant panel is obvious, describe the specific UI panel visible on screen and instruct it to extend beyond both edges of the device frame with a drop shadow, e.g., "The [panel name] card/row extends beyond both left and right edges of the device frame, overlapping the phone bezel on both sides, expanding to nearly the full screenshot width. It floats in front of the device with a soft drop shadow beneath it." If no panel clearly relates to the headline, write "No breakout — the app screen speaks for itself."]
- Optionally add 1-2 secondary elements that reinforce the benefit and message of the screenshot — the kind of enhancements a professional graphic designer would add for impact. These are NOT from the app UI; they are creative additions that help clearly communicate what the screenshot is trying to portray to the user browsing the App Store. They should carry the message and support ASO conversion, but never at the cost of the overall design aesthetic. They must not compete with the primary breakout for attention.
[SECONDARY ELEMENTS (optional) — describe 0-2 small supporting elements that tell the story, or "None needed"]
- The background should be a clean, solid brand colour. Do NOT add glows, gradients, radial patterns, or light effects to the background. Keep it flat and bold.
- Ensure the text is crisp, bold, and highly readable
- Avoid watermarks, extra text, invented UI content, App Store UI chrome, or changing the app screenshot content.

The final result should look like it was designed by a professional App Store screenshot agency — polished, high-converting, and visually striking. No watermarks, no extra text, no app store UI chrome.
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
- SECOND image: The STYLE TEMPLATE — this is an already-approved screenshot from the same set. Match its visual style EXACTLY: same device frame rendering (this is critical — the phone must look identical), same text treatment, same background style/accents, same level of polish, same overall aesthetic. This defines HOW this screenshot should look. When in doubt, copy the style template more closely rather than less.

REQUIREMENTS:
- CRITICAL: The device frame MUST match the style template EXACTLY — same photorealistic iPhone rendering, same size, same position, same shadows, same reflections, same edge treatment. Do NOT reinvent or reimagine the device frame. Reproduce it as closely as possible from the style template, only changing the screen contents.
- Match the style template's text rendering style (same font treatment, same crispness, same visual weight)
- Match the style template's background — clean, solid brand colour. No glows, gradients, radial patterns, or light effects.
- Use the scaffold's layout for positioning (text, device, screenshot placement)
- OPTIONALLY add a PRIMARY breakout element — but ONLY if there is an obvious, visually compelling UI panel on the app screen that directly relates to the benefit headline. If nothing clearly reinforces the headline, skip the breakout entirely. When used, it MUST be an entire UI panel or grouped section (NOT individual small elements like a single button or icon). The panel must stay at the SAME vertical position and orientation as on screen — do NOT rotate or angle it. The panel must be SCALED UP significantly — rendered much larger than it appears on the phone screen — so that it extends dramatically beyond BOTH left and right edges of the device frame, clearly overlapping the phone bezel on both sides, expanding to nearly the full width of the screenshot canvas. Do NOT keep the panel at its original on-screen size. The panel itself must be enlarged. It should appear to float in front of the device at this larger scale — add a soft drop shadow beneath it to create depth. The panel MUST come from the app screenshot — same colours, same style, same content. Do NOT invent new elements.
[PRIMARY BREAKOUT — if a relevant panel is obvious, describe the specific UI panel visible on screen to pop out with a drop shadow, extending beyond both device frame edges. Otherwise write "No breakout — the app screen speaks for itself."]
- Optionally add 1-2 secondary elements that reinforce the benefit and message of the screenshot — the kind of enhancements a professional graphic designer would add for impact. These are NOT from the app UI; they are creative additions that help clearly communicate what the screenshot is trying to portray to the user browsing the App Store. They should carry the message and support ASO conversion, but never at the cost of the overall design aesthetic. They must not compete with the primary breakout for attention.
[SECONDARY ELEMENTS (optional) — 0-2 small supporting elements that tell the story, or "None needed"]
- The breakout elements should match the style and energy level of those in the style template
- Avoid watermarks, extra text, invented UI content, App Store UI chrome, or changing the app screenshot content.

The result must look like it was designed alongside the style template as part of the same professional set. When placed side-by-side in the App Store, they should be visually cohesive — same quality, same aesthetic, same design language, just different content.

No watermarks, no extra text, no app store UI chrome.
```

**IMPORTANT — Consistency enforcement**: The scaffold guarantees consistent layout. The style template guides consistent visual treatment. If imagegen changes the text, layout, app UI content, or deviates from the style template, regenerate with a stricter prompt.

**Step 3: IMMEDIATELY crop and resize ALL 3 versions to App Store dimensions**

⚠️ **You MUST run this immediately after all 3 `image_gen` calls complete. Do NOT show the user any image before running this unless it already verifies at the exact App Store dimensions.**

**CRITICAL — Use exactly ONE Bash tool call for all 3 crop/resize operations.** Do NOT make 3 separate Bash calls. Do NOT use parallel Bash calls. Use the single loop below so the user only sees one permission prompt:

```bash
TARGET_W=1284 && TARGET_H=2778 && \
for INPUT in screenshots/01-[benefit-slug]/v1.png screenshots/01-[benefit-slug]/v2.png screenshots/01-[benefit-slug]/v3.png; do
  OUTPUT="${INPUT%.png}-resized.png"
  cp "$INPUT" "$OUTPUT"
  W=$(sips -g pixelWidth "$OUTPUT" | tail -1 | awk '{print $2}')
  H=$(sips -g pixelHeight "$OUTPUT" | tail -1 | awk '{print $2}')
  CROP_W=$(python3 -c "print(round($H * $TARGET_W / $TARGET_H))")
  OFFSET_X=$(python3 -c "print(round(($W - $CROP_W) / 2))")
  sips --cropOffset 0 $OFFSET_X --cropToHeightWidth $H $CROP_W "$OUTPUT"
  sips -z $TARGET_H $TARGET_W "$OUTPUT"
  echo "--- $OUTPUT ---"
  sips -g pixelWidth -g pixelHeight "$OUTPUT"
done
```

The script crops to the correct aspect ratio (top-center aligned — sides trimmed equally, top edge preserved so the headline stays put) and resizes to exact pixel dimensions. The resized image is saved as a separate file with `-resized.png` appended.

Target dimensions per display size — adjust `TARGET_W` and `TARGET_H`:
- iPhone 6.5": `TARGET_W=1242 TARGET_H=2688`
- iPhone 6.7" (default): `TARGET_W=1284 TARGET_H=2778`

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
- SECOND image: The STYLE TEMPLATE — this is the first approved screenshot in the set. The device frame rendering, text treatment, and overall visual style MUST match this exactly. This defines HOW the screenshot should look to maintain consistency across the set.
- THIRD image: The APPROVED DESIGN DIRECTION — this is the version the user liked best for this specific screenshot. Match its creative direction, breakout element approach, and secondary elements.

Generate a new version that keeps the layout from the scaffold, the device frame and visual style from the style template, and the creative direction from the approved design, with these changes:
[USER'S REQUESTED CHANGES]
```

This prevents drift (scaffold keeps layout locked), maintains set-wide consistency (style template keeps device frame and visual treatment identical), and preserves the creative direction the user already approved.

When iterating, generate **3 versions** again with built-in `image_gen`. Then **immediately run the Step 3 crop/resize loop on all 3 in a single Bash call** before showing the user.

Repeat until the user is happy.

**Step 6: Copy approved version to `final/`**

Once the user picks a winner, copy the resized version to `screenshots/final/`:

```bash
mkdir -p screenshots/final
cp "screenshots/01-[benefit-slug]/v2-resized.png" "screenshots/final/01-[benefit-slug].png"
```

This keeps `final/` clean — only approved, App Store-ready screenshots, one per benefit, numbered in order. Then move to the next benefit.

### Determine Brand Colour (Automatic)

Do NOT ask the user to pick a background colour. Instead, determine the best one automatically:

1. **Analyse the codebase** — check for accent colours, tint colours, brand colours in asset catalogs, theme files, colour constants, Info.plist
2. **Study the simulator screenshots** — what are the dominant colours in the UI? What colour palette does the app use?
3. **Consider the app's domain and audience** — a game can go bold and playful, a finance app needs confident and trustworthy colours

**Pick a single colour that:**
- **Complements the screenshots** — makes the app screens pop, not clash. If the app UI is mostly white/light, use a bold saturated background for contrast.
- **Stops the scroll** — vibrant, bold, saturated. Muted or pastel colours get lost in the App Store.
- **Suits the app's personality** — match the energy of the app
- **Avoids pitfalls** — no white/light grey (disappears against App Store), avoid colours too close to the app UI's dominant colour

Present your choice with brief reasoning (e.g., "Using **#7B2D8E** (deep purple) — it complements your app's colourful UI and stands out at thumbnail size"). The user can override if they want, but don't present it as a question.

The brand colour is saved to memory in Step 0 of the generation process, before scaffolding begins.

### Output

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

### Save to Memory

After each screenshot is generated (or after the full set is complete), save generation state to the Codex memory system. Create or update a memory file (e.g., `aso_generated_screenshots.md`) with:

- **Brand colour**: name + hex code
- **Target display size**: e.g., iPhone 6.7" (1284x2778)
- **For each generated screenshot**:
  - Benefit headline (ACTION VERB + DESCRIPTOR)
  - Benefit subfolder path (e.g., `screenshots/01-track-card-prices/`)
  - Which version the user chose (v1, v2, or v3)
  - Final file path (e.g., `screenshots/final/01-track-card-prices.png`)
  - Simulator screenshot used (file path)
  - Breakout elements described in the prompt
  - Status: generated / approved / needs-redo
  - Any user feedback or change requests noted

Update this memory **incrementally** — after each screenshot is approved, add it. Don't wait until the end. This way if the conversation is interrupted mid-set, the user can resume from the last completed screenshot.

### Showcase Image

Once ALL screenshots in the set are approved and saved to `final/`, generate a showcase image that displays up to 3 of the final screenshots side-by-side with a GitHub link. Use the showcase.py script in the skill directory:

```bash
SKILL_DIR="[absolute path to this skill directory]"

python3 "$SKILL_DIR/showcase.py" \
  --screenshots screenshots/final/01-*.png screenshots/final/02-*.png screenshots/final/03-*.png \
  --github "github.com/your-github-user" \
  --output screenshots/showcase.png
```

Show the showcase image to the user using `view_image`. This is a shareable preview of the full screenshot set.

---

## KEY PRINCIPLES

- **Benefits over features**: "BOOST ENGAGEMENT" not "ADD SUBTITLES TO VIDEOS"
- **Specific over generic**: "TRACK TRADING CARD PRICES" not "MANAGE YOUR STUFF"
- **Action-oriented**: Every headline starts with a strong verb
- **User-centric**: Frame everything from the downloader's perspective
- **Conversion-focused**: Every decision should answer "will this make someone tap Download?"
- The first screenshot is the most important — it must communicate the single biggest reason to download
- Screenshots should tell a story when swiped through — each one reveals a new compelling reason
- Always pair the most visually impactful simulator screenshot with the most important benefit
- Never use an empty state, loading screen, or settings page as a screenshot — show the app at its best
