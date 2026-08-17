# Localization and final QA

Read this file before rendering multiple storefronts or approving final screenshots.

## Localization contract

- Start from approved source-language copy and localize the benefit, not its word order.
- Keep the visible top of the primary title identical across locales for each device set.
- Keep visible subtitle line spacing constant even when localized copy wraps to more lines.
- Use the approved brand font where it supports the script. Otherwise select a heavy locale-appropriate fallback and save its path, collection index, language, and direction in the manifest.
- Pass `--text-transform none` when uppercasing would be unnatural or harmful.
- Treat Arabic and other RTL storefronts as separate visual compositions. Confirm shaping, reading order, centered alignment, and spacing around Latin product names.
- Test Japanese, Korean, Simplified Chinese, and Traditional Chinese independently. Do not rely on whitespace-only wrapping or Latin font metrics.
- Localize social-proof descriptors naturally. Preserve verified numerals, brand names, and claim meaning.

## Layout invariants

- Keep `visible_text_top`, background, title hierarchy, and device centering consistent across locales.
- Define line gaps as visible empty pixels between glyph bounds, not baseline distance.
- Keep laurel text centered in the widest usable area of the wreath with explicit horizontal clearance.
- Move the device down when localized copy needs more room. Never tighten text until lines nearly touch.
- Keep the Dynamic Island opaque black, centered, and part of the physical iPhone frame.
- When using a breakout, preserve the source panel's content and orientation. Save its crop, position, size, corner radius, and shadow in the manifest.

## Required final checks

Inspect every exported image at full size and as a small storefront thumbnail. Reject or fix any image with:

- Overlapping text, laurels, device hardware, or breakout elements
- Clipped glyphs or text outside the safe area
- Inconsistent title-top alignment or line spacing
- Incorrect RTL shaping or CJK wrapping
- Wreath text touching leaves or using inconsistent vertical gaps
- A missing, translucent, or content-filled Dynamic Island
- A background that differs from the saved specification
- A device or breakout shifted relative to its manifest
- Alpha transparency or dimensions that do not match the intended App Store slot

Run automated dimension and mode checks after visual review. Automation does not replace per-locale inspection.
