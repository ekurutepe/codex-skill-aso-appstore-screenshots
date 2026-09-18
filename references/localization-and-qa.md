# Localization and final QA

Read this file before rendering multiple storefronts or approving final screenshots.

## Localization contract

- Start from approved source-language copy and localize the benefit, not its word order.
- In the Sketch workflow, keep only the approved base locale in the template. Render other locales from temporary copies by replacing unique `loc.*` text keys and `shot.*` image slots as defined in [`sketch-template-workflow.md`](sketch-template-workflow.md).
- Replacing marketing strings does not localize text inside simulator screenshots. Require localized iPhone and iPad captures whenever the visible app UI contains language.
- Keep the visible top of the primary title identical across locales for the same panel in each device family.
- Keep visible subtitle line spacing constant even when localized copy wraps to more lines.
- Use the approved brand font where it supports the script. Otherwise select a heavy locale-appropriate fallback and save its path, collection index, language, and direction in the manifest.
- Pass `--text-transform none` when uppercasing would be unnatural or harmful.
- Treat Arabic and other RTL storefronts as separate visual compositions. Confirm shaping, reading order, centered alignment, and spacing around Latin product names.
- Test Japanese, Korean, Simplified Chinese, and Traditional Chinese independently. Do not rely on whitespace-only wrapping or Latin font metrics.
- Localize social-proof descriptors naturally. Preserve verified numerals, brand names, and claim meaning.

## Layout invariants

- Keep each panel's approved `visible_text_top`, background, title hierarchy, and device placement consistent across locales. Different panels may use different approved layouts.
- Define line gaps as visible empty pixels between glyph bounds, not baseline distance.
- Keep laurel text centered in the widest usable area of the wreath with explicit horizontal clearance.
- Move the device down when localized copy needs more room. Never tighten text until lines nearly touch.
- Keep the Dynamic Island opaque black, centered, and part of the physical iPhone frame.
- When using a breakout, preserve the source panel's content and orientation. Save its crop, position, size, corner radius, and shadow in the manifest.

## Required final checks

Inspect every exported image at full size and as a small storefront thumbnail. Reject or fix any image with:

- Overlapping text, laurels, device hardware, or breakout elements
- Clipped glyphs or text outside the safe area
- Title anchoring or line spacing that differs from that panel's approved composition
- Incorrect RTL shaping or CJK wrapping
- Wreath text touching leaves or using inconsistent vertical gaps
- A missing, translucent, or content-filled Dynamic Island
- A background that differs from the saved specification
- A device or breakout shifted relative to its manifest
- Alpha transparency or dimensions that do not match the intended App Store slot
- Missing or duplicate Sketch localization keys
- An iPhone capture or device component in an iPad export, or the reverse
- Discontinuities when Sketch slices are reconstructed edge-to-edge

Run automated dimension and mode checks after visual review. Automation does not replace per-locale inspection.

## Full-set review

Inspect all exported panels together at storefront size against the constitution: obvious category, action demonstrated in frame one, headline/hero attention priority, and result delivered in frame two. Check balance, rhythm, shared visual identity, and the distinct value of subsequent panels. Compare each localized set with the approved storyboard; intentional panel variations are not QA failures. A three-panel showcase cannot replace this complete-set review.
