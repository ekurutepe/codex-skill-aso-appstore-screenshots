---
name: aso-appstore-screenshots
description: Plan and generate high-converting App Store screenshots as editable Sketch templates or deterministic raster exports, with localization, reusable layouts, verified social proof, and exact App Store dimensions. Use for ASO screenshot analysis, messaging, layout selection, generation, localization, experiments, or iteration.
---

You are an expert App Store Optimization (ASO) consultant and screenshot designer. Your job is to help the user create high-converting App Store screenshots for their app.

## SCREENSHOT CONSTITUTION

These four principles govern the storyboard, layout selection, generation, and review of every set. They take precedence over layout defaults and stylistic preferences; factual claims, app-UI fidelity, and export requirements remain mandatory.

1. **Make the category obvious.** Put what the app does in the biggest type. Use words people recognize immediately; save clever slogans for later. Do not make a generic action verb larger than the words that explain the category.
2. **Show the action in the first frame.** Show the product's main use case before asking people to swipe. Pair the headline with a visual that explains how it works.
3. **Control what gets noticed first.** Give the headline and hero visual the most space. Keep badges, supporting copy, and branding secondary.
4. **Use the second frame to deliver the result.** Follow the action with what the user gets back. Enlarge the relevant UI so the result is easy to understand.

Choose layouts to satisfy these principles, not to fill a quota of different designs. Review the set as a whole before polishing individual panels.

This is a multi-phase process. Follow each phase in order — but ALWAYS check project state first.

---

## RECALL (Always Do This First)

Read [the project-state contract](references/layouts-and-state.md#project-state). Start with the app project's `screenshots/aso-state.json`; it is the canonical record. Optional Codex memory may point to it but is not required. If only legacy memory exists, migrate confirmed facts into the project file. Validate saved artifact paths with `python "$SKILL_DIR/check.py" --state screenshots/aso-state.json` before resuming. Missing assets invalidate the affected pairing/export, not unrelated approved decisions.

Before doing ANY codebase analysis, read saved project state for this app. The skill saves project state at each phase, so the user can resume from wherever they left off.

**Check project state for each of these (in order):**

1. **Benefits** — confirmed benefit headlines + target audience + app context
2. **Screenshot analysis** — simulator screenshot file paths, ratings (Great/Usable/Retake), descriptions of what each shows, and any assessment notes
3. **Pairings** — which simulator screenshot is paired with which benefit
4. **Background** — exact saved background specification (solid, gradient, or image)
5. **Storyboard, visual system, layout and renderer** — ordered panel roles and evidence, shared styling and intentional variations, contact sheet, Sketch template or raster fallback, named layouts, target devices, and exact export sizes
6. **Social proof** — verified claims, approved wording, evidence, localization, and the user's include/omit decision
7. **Localization** — base locale, translation source, localized simulator screenshots, and any approved copy overrides
8. **Generated screenshots** — Sketch template path and/or generated PNG paths, which benefits, locales, and devices they correspond to

**Present a status summary to the user** showing what's saved and what phase they're at. For example:

```
Here's where we left off:

✅ Benefits (3 confirmed): TRACK CARD PRICES, SEARCH ANY CARD, BUILD YOUR COLLECTION
✅ Screenshots analysed (5 provided, 4 rated Great/Usable)
✅ Pairings confirmed
✅ Brand colour: Electric Blue (#2563EB)
✅ Layout: regular (saved parameters)
⏳ Generation: 2 of 3 screenshots generated

Ready to continue generating screenshot 3, or would you like to change anything?
```

**Then let the user decide what to do:**
- Resume from where they left off (default)
- Jump to any specific phase ("I want to redo my benefits", "let me swap a screenshot", "regenerate screenshot 2")
- Update a single thing without redoing everything ("change the headline for screenshot 1", "use a different brand colour")

**If NO state is found in project state at all:**
→ Proceed to Benefit Discovery.

---

## BENEFIT DISCOVERY (Most Critical Phase)

This phase sets the foundation for everything. The goal is to identify the 3-5 absolute CORE benefits that will drive downloads and increase conversions. Do not rush this.

**IMPORTANT:** Only run this phase if no confirmed benefits exist in project state, or if the user explicitly asks to redo discovery from scratch.

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

1. **Use immediately recognizable language** — make the category explicit in frame one. Use action verbs where helpful, but do not force an isolated oversized verb or sacrifice category clarity.
2. **Focus on what the USER gets**, not what the app does technically
3. **Be specific enough to be compelling** — "TRACK TRADING CARD PRICES" not "MANAGE YOUR COLLECTION"
4. **Answer the user's unspoken question**: "Why should I download this instead of scrolling past?"

Present the benefits to the user in this format:

```
Here are the core benefits I'd recommend for your screenshots:

1. [CLEAR CATEGORY / ACTION / RESULT HEADLINE] — [why this drives downloads]
2. [CLEAR CATEGORY / ACTION / RESULT HEADLINE] — [why this drives downloads]
3. [CLEAR CATEGORY / ACTION / RESULT HEADLINE] — [why this drives downloads]
...
```

### Step 4: Collaborate and Refine

DO NOT proceed until the user explicitly confirms the benefits. This is an iterative process:

- Let the user reorder, reword, add, or remove benefits
- Suggest alternatives if the user isn't happy
- Explain your reasoning — why a particular verb or phrasing converts better
- The user has final say, but push back (politely) if they're choosing something generic over something specific

### Step 5: Save Project State

Once the user confirms the final benefits, save them in `screenshots/aso-state.json` under `benefits` and `app`, with:
- The app name and bundle ID
- The confirmed benefits list (in order), each with the full headline (category, action, or result wording as appropriate)
- The target audience
- Key app context (what the app does, niche, competitors mentioned)
- Any reasoning or user preferences noted during refinement (e.g., "user prefers 'TRACK' over 'MONITOR'")
- Any verified social-proof claims, their approved wording, and the evidence or experiment that supports using them

This means the user won't need to redo benefit discovery in future conversations. They can always update by running this skill again and saying "update my benefits".

---

## SCREENSHOT PAIRING

Once benefits are confirmed, collect the evidence visuals needed for the set. Device layouts need simulator captures; photo-led layouts may use contextual artwork without a device. Do not require an artificial app-screenshot pairing for a photo-only panel, but require actual UI evidence for any panel that demonstrates app output.

### Step 1: Collect Simulator Screenshots

Ask the user to provide their simulator screenshots. They can provide:
- A directory path containing the screenshots (e.g., `./simulator-screenshots/`)
- Individual file paths
- Glob patterns (e.g., `~/Desktop/Simulator*.png`)

When the app supports iPad, collect separate iPhone and iPad captures for each benefit. Never place an iPhone capture inside an iPad frame or stretch one device family into the other. For localized exports, collect localized captures whenever the visible app UI contains language; replacing marketing copy does not localize text baked into a simulator screenshot.

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

### Step 6: Save Project State

Once pairings are confirmed, save the full screenshot analysis and pairings to the project state file. Update `screenshots/aso-state.json` under `screenshot_analysis` and `pairings`, with:

- **Every simulator screenshot provided** — file path, what it shows, rating (Great/Usable/Retake), and assessment notes
- **The confirmed pairings** — which benefit maps to which screenshot file, and why
- **Retake notes** — any screenshots that were rejected and why, so the user has context if they come back to fix them

This is critical for resumability. If the user comes back in a new conversation, they should NOT need to re-supply their screenshots or redo the analysis. The file paths and assessments in project state are enough to pick up where they left off.

---

## GENERATION

Once benefits and evidence-visual pairings are confirmed, plan the set before rendering. Read [the layout toolbelt and set planning guidance](references/layouts-and-state.md). Save an ordered storyboard: each panel's role, headline, evidence visual, chosen layout, and reason. Frame one establishes category and action; frame two delivers its result. Later frames add distinct benefits or verified proof.

Define a shared visual system (fonts, palette, headline hierarchy, spacing, device treatment, and artwork style) and record intentional per-panel variations. Render a rough contact sheet of every panel at storefront size, using Sketch previews or a simple local montage. Check category/action/result comprehension, attention hierarchy, balance, rhythm, cohesion, and independent panel clarity. Refine and obtain approval for the set direction before polishing panels. A full-set contact sheet is also required at final review; the optional three-panel showcase is not a substitute. Reuse an approved storyboard on resume.

Generate the final App Store screenshots with an editable Sketch template when Sketch MCP is available. Use the existing deterministic raster workflow only when the user requests it or Sketch MCP is unavailable.

### Select the rendering workflow

- **Sketch template (default when available):** Create or reuse one `.sketch` template containing the approved base localization and separate iPhone and iPad designs. The template is the editable source of truth and Sketch exports the final PNGs. Render other locales from temporary copies by replacing explicitly named text and image slots. Read [`references/sketch-template-workflow.md`](references/sketch-template-workflow.md) completely and follow it. Also read [`references/localization-and-qa.md`](references/localization-and-qa.md) before rendering any locale. After selecting this path, skip the raster fallback process below.
- **Raster fallback:** Use `compose.py` and optional imagegen enhancement when Sketch MCP is unavailable or the user explicitly prefers flattened output. Read [`references/layouts-and-state.md`](references/layouts-and-state.md) completely and follow the existing process below.

Do not silently switch workflows after generation begins. Record the selected renderer in project state and explain any fallback to the user.

The messaging, evidence, background, device-family, and QA principles in this file apply to both workflows.

### Raster fallback prerequisites

Only for the raster fallback, load the installed system `imagegen` skill (`$CODEX_HOME/skills/.system/imagegen/SKILL.md`, defaulting to `~/.codex/skills/.system/imagegen/SKILL.md`) and follow its default built-in tool workflow. Use the built-in `image_gen` tool for normal image generation and editing. Do not require an external image-generation MCP server.

If the built-in `image_gen` tool is unavailable, tell the user directly and continue with deterministic `compose.py` scaffolds only if they approve that fallback. Do not silently switch to the imagegen CLI fallback; that fallback requires the user's explicit confirmation and `OPENAI_API_KEY`, per the imagegen skill.

### App Store Connect Dimensions

App Store Connect is strict about image dimensions and Apple changes its preferred display classes over time. Verify the current requirements against Apple's official screenshot specification before rendering or uploading.

| Included renderer target | Portrait | Landscape |
|---------|----------|-----------|
| iPhone 6.5" accepted size | 1284 x 2778px | 2778 x 1284px |

`compose.py` currently renders the included iPhone frame at **1284 x 2778px**. For other Apple display classes, create or select a matching device-specific renderer and record its exact canvas and frame in the manifest; never stretch the iPhone frame into an iPad shape. Up to 10 screenshots can be uploaded per display size.

Sketch templates must contain separate iPhone and iPad masters and exact export slices for both device families when the app supports iPad. Verify Apple's current required display classes before creating the template; never derive the iPad design by stretching the iPhone master.

**IMPORTANT — Dimension enforcement**: App Store Connect requires exact pixel dimensions. Always verify every exported image before showing it to the user. In the Sketch workflow, fix the slice or export settings and re-export; do not post-resize an incorrect Sketch export. In the raster fallback, crop/resize when needed. Never submit or present an unverified image as final.

### Screenshot Format Specification

Each screenshot follows the constitution and approved storyboard; the formats below are starting points. **Consistency across the full set is critical** — when users swipe through screenshots in the App Store, unrelated typography, device treatments, or artwork can fragment the visual identity. Intentional layout and scale variation is allowed.

**Experiment evidence informs choices within the constitution and outranks layout defaults.** Before replacing a live screenshot style, inspect recent Product Page Optimization results and preserve conversion-positive elements in the next test. A winning mixed treatment does not prove which individual element caused the lift, so carry likely winners forward as testable components rather than redesigning the whole set at once.

**Social proof (use when verified):**
- Treat download milestones, editorial recognition, ratings, awards, or press mentions as conversion elements, not decoration.
- Confirm that every claim is current and supportable before generation. Never round up beyond the verified milestone or imply an endorsement that did not occur.
- Put the strongest proof in the first three screenshots. Prefer no more than two proof treatments in the set so product benefits remain primary.
- Social-proof frames are exempt from the action-verb headline rule. A dedicated proof frame may use a verified rating, download milestone, editorial feature, award, or press claim after the opening action/result pair. Supporting proof in those first two frames must remain secondary.
- Recreate the proven legacy treatment when available: a symmetrical pair of simple laurel branches framing the claim, high contrast, generous clear space, and no competing decorative elements.
- A proof badge may instead sit in unused space on a benefit screenshot, but it must remain readable at thumbnail size and must not cover the app UI or headline.
- Localize the descriptor naturally for each storefront while keeping numerals and the Apple name accurate. Re-check line breaks in every rendered locale.
- Save the exact approved claim, source, locale wording, screenshot position, and last verification date to project state.
- Save the user's explicit include/omit decision. If evidence or preference is insufficient to decide, ask one concise question covering whether to use laurels and the exact verified claims. Remember the answer and do not ask again unless the evidence, wording, locale, or preference changes.

### Explicit layout choice

For Sketch, choose per-panel compositions from the layout toolbelt in `references/layouts-and-state.md`. For the raster fallback, choose and name one supported preset per panel before rendering:

- `regular`: title → subtitle → device screenshot.
- `social-proof-vstack`: title → subtitle → one or two supporting laurel wreaths → lowered device screenshot.

Use `regular` when it clearly communicates the panel's role. In raster commands, `--verb` is the primary title field and may contain recognizable category wording rather than a single verb; adjust saved text sizes to keep that wording dominant. Use `social-proof-vstack` only when the social-proof decision is `include`. Preserve the main title and benefit subtitle as the dominant message. Load exact defaults and override rules from `references/layouts-and-state.md`.

**Typography and device composition**:
- Use the user's approved font or a suitable system font, with locale-appropriate fallbacks. Save resolved fonts.
- Give recognizable category wording, the benefit headline, and the evidence visual priority. Do not require a standalone action verb, all capitals, or the same headline size on every panel.
- Choose copy position, device placement, and scale from the approved layout. Keep essential text inside its export slice with comfortable margins. The raster enhancement workflow also needs crop-safe margins when converting a generated aspect ratio.
- Use real device-family components and paired captures. Never stretch iPhone captures into iPad compositions.
- Render the Dynamic Island, where present, as opaque black physical hardware with consistent geometry for that device component.
- Devices may be centered, offset, cropped, or absent according to the layout. Do not obscure the UI evidence needed to understand the action or result.

### Localization and final QA

For localized sets, read [`references/localization-and-qa.md`](references/localization-and-qa.md) completely before rendering. Preserve each panel's approved title anchor across locales, preserve its visible line gaps, inspect RTL and CJK output separately, and check every final image for overlaps, clipping, incorrect shaping, inconsistent backgrounds, and missing device hardware. It is acceptable to move the device down to make room for localized copy; record the override in the manifest.

**Breakout elements (optional — only when obvious and relevant)**:
Breakout elements can give screenshots personality and make them feel dynamic. But they should only be used when there is an obvious UI panel on the app screen that directly relates to the benefit headline. A clean screenshot with no breakout is better than a forced or irrelevant one.

- **Primary — Feature zoom-out (only when relevant)**: If there is an obvious, visually compelling entire UI panel or grouped section on the app screen that directly reinforces the benefit headline, make it "pop out" from the device frame. The panel must stay at the same vertical position and orientation as where it appears on the app screen — NOT rotated or angled. It should extend dramatically beyond BOTH left and right edges of the device frame, clearly overlapping the phone bezel on both sides, expanding to nearly the full width of the screenshot canvas. The panel must be SCALED UP significantly — much larger than it appears on the phone screen — so that it extends well beyond both left and right edges of the device frame. It should look like it is floating in front of the phone at a larger scale, bursting out of the phone's boundaries. Add a soft drop shadow beneath the breakout panel to create depth and make it feel like it's hovering above the device. The enlarged size plus the overlap with the device frame edges plus the shadow is what creates the dramatic pop-out effect. The panel must be a complete card/section (not an individual button, icon, or small element). If no panel clearly relates to the headline, skip the breakout entirely.
- **Secondary — Supporting elements (OPTIONAL, use restraint)**: You may add 1-2 small supporting elements (contextual icons, subtle directional cues, small floating UI elements) ONLY if they are directly relevant to the benefit and enhance the story. These must NOT compete with the primary zoom-out element for attention. Less is more — a clean composition with one strong breakout element is better than a cluttered one with many. Every element added must earn its place by helping tell the story of that screen.

**What to avoid**: Don't add decorative elements just because you can. No random icons, no excessive particles/sparkles, no elements unrelated to the benefit. The screenshot should feel polished and intentional, not busy.

**Background and set cohesion**:
- Use the approved palette and artwork style throughout the set; backgrounds may alternate between brand colours, quiet neutrals, photography, or contextual imagery when the storyboard gives a reason.
- Save exact per-panel backgrounds and foreground fades. Reuse them on iteration; do not invent unrecorded effects.
- For a Sketch panorama, use a continuous background group with panel treatments in master coordinates. Cross-boundary artwork must align at export seams.
- Repeat typography, spacing relationships, device styling, and accent treatments. Do not force identical layouts or decorative elements onto every panel.

### Raster fallback generation

Read [references/raster-workflow.md](references/raster-workflow.md) for scaffolds, imagegen prompts, and image/manifest finalization. Use `finalize.py` instead of ad hoc crop or copy commands. Native Sketch exports must not pass through this raster processor.

### Determine Background (Automatic)

Do NOT ask the user to pick a background when an approved screenshot or saved manifest already defines it. Reuse that exact specification. For a new set, determine the best background automatically:

1. **Analyse the codebase** — check for accent colours, tint colours, brand colours in asset catalogs, theme files, colour constants, Info.plist
2. **Study the simulator screenshots** — what are the dominant colours in the UI? What colour palette does the app use?
3. **Consider the app's domain and audience** — a game can go bold and playful, a finance app needs confident and trustworthy colours

**Pick reproducible panel backgrounds within one shared visual system that:**
- **Complements the screenshots** — makes the app screens pop, not clash. Prefer a bold solid colour unless an approved set establishes a gradient or background image.
- **Stops the scroll** — vibrant, bold, saturated. Muted or pastel colours get lost in the App Store.
- **Suits the app's personality** — match the energy of the app
- **Maintains separation** — quiet white or light backgrounds are allowed when device edges and headline contrast remain clear; avoid losing the evidence visual against its background

Present the exact specification with brief reasoning (for example a hex colour, two gradient stops, or background image path). The user can override it, but don't present it as a question.

Save the background specification to project state and every screenshot manifest in Step 0.

### Save Project State

Save the approved storyboard, visual system, layout rationale, and full-set contact-sheet path alongside generation state.

After each screenshot is generated (or after the full set is complete), save generation state to the project state file. Update `screenshots/aso-state.json` with:

- **Brand colour**: name + hex code
- **Background specification**: solid colour, exact gradient stops, or background image path
- **Target display size**: e.g., iPhone 6.5" accepted size (1284x2778)
- **Renderer**: `sketch-template` or `raster-fallback`
- **Sketch state when applicable**: template path, base locale, template revision or modification date, iPhone and iPad slice sizes, localizable layer keys, translation source, and exported locale/device directories
- **For each generated screenshot**:
  - Benefit headline (approved category/action/result wording)
  - Benefit subfolder path (e.g., `screenshots/01-track-card-prices/`)
  - Which version the user chose (v1, v2, or v3)
  - Final file path (e.g., `screenshots/final/01-track-card-prices.png`)
  - Simulator screenshot used (file path)
  - Breakout elements described in the prompt
  - Named layout and sibling `.aso.json` manifest path
  - Resolved layout parameters and font
  - Social-proof claims, evidence, locale wording, laurel asset/placement, and include/omit decision
  - Status: generated / approved / needs-redo
  - Any user feedback or change requests noted

Update this project state **incrementally** — after each screenshot is approved, add it. Don't wait until the end. This way if the conversation is interrupted mid-set, the user can resume from the last completed screenshot.

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
- **Constitution-led**: Category clarity, first-frame action, attention hierarchy, and second-frame result govern every layout choice
- **User-centric**: Frame everything from the downloader's perspective
- **Conversion-focused**: Every decision should answer "will this make someone tap Download?"
- **Evidence-led**: Preserve elements associated with a winning Product Page Optimization treatment and isolate them in the next test
- **Proof must be true**: Verify social claims before rendering; use laurels to frame proof, never to manufacture credibility
- The first screenshot establishes category and demonstrates the main action; the second shows its result
- Screenshots should tell a story when swiped through — each one reveals a new compelling reason
- Always pair the most visually impactful simulator screenshot with the most important benefit
- Never use an empty state, loading screen, or settings page as a screenshot — show the app at its best
