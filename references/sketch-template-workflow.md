# Sketch template workflow

Read this file when creating, editing, localizing, or exporting an ASO screenshot set through Sketch MCP.

## Source of truth

Use one `.sketch` template as the editable source of truth. It contains:

- The approved base localization
- Separate iPhone and iPad designs when the app supports both
- One continuous master composition per device family
- Exact adjacent export slices for every App Store screenshot
- Native text, device, mask, shadow, background, and social-proof layers

Sketch exports the final PNGs. Do not run Sketch exports through `compose.py`, imagegen, or a second renderer. External tools may perform read-only dimension, colour-mode, alpha, file-count, and seam checks.

Other localizations do not become permanent pages in the template. Render each from a temporary copy, export it, verify it, and discard the copy. Preserve a localized `.sketch` copy only when the user explicitly wants a designer to adjust that locale.

## MCP prerequisites

Use Sketch's MCP tools, not raw HTTP requests or direct edits to the `.sketch` package.

1. Confirm Sketch MCP exposes `get_guide`, `run_code`, `get_screenshot`, `get_document_info`, and `get_layer_tree_summary`.
2. Load `get_guide` topic `mcp`, then `use`; load `layout`, `styling`, `symbols`, or `assets` only when needed.
3. Follow the returned guide. Use only the public Sketch JavaScript API, keep each `run_code` action small, re-resolve targets on every call, log structured JSON, and screenshot-verify appearance changes.
4. If the tools are unavailable, tell the user and use the raster fallback only with their approval. Do not bypass a missing integration by calling the local MCP endpoint manually.

Before creating a template, inspect available libraries and design assets. Reuse a suitable device component, frame template, text style, or swatch when one exists.

## App Store targets

Verify Apple's current screenshot specification before creating or exporting slices. Select one accepted portrait or landscape size for each required display class and record it in project state. At the time this workflow was written, useful portrait targets included:

- iPhone 6.9-inch: 1320 x 2868
- iPad 13-inch: 2064 x 2752

These are defaults, not timeless constants. Use the currently accepted dimensions. A template for an iPad app must have a real iPad composition and localized iPad screenshots; never stretch the iPhone master or place an iPhone capture inside an iPad bezel.

## Template contract

Use these page names unless an existing approved template already has stable equivalents:

```text
00 - Components
Template - iPhone
Template - iPad
```

Each device page contains one master frame sized `screenshot_count * slice_width` by `slice_height`. Inside it:

```text
Master Panorama
  Background
  Background Artwork
  Devices
  Foreground Artwork
  Fades
  Copy
  Feature Badges
  Social Proof
Export Slices
  01
  02
  ...
```

Requirements:

- Use one background group across the full master, containing the approved panel treatments and any continuous imagery. Panel backgrounds may vary within the shared visual system; crossing imagery must remain continuous.
- Position device groups in master coordinates. A single device may cross one screenshot boundary; do not duplicate halves into adjacent panels.
- Place slices edge-to-edge at `x = index * slice_width`, with no gutters, overlap, or transparent pixels. Each slice is exactly the selected App Store size and exports as an opaque PNG at 1x.
- Keep essential copy inside one slice. Backgrounds and devices may cross boundaries, but every screenshot should remain understandable when viewed alone.
- Use native editable Sketch layers. Keep simulator screenshots as masked image layers or image overrides. Do not outline text or flatten the composition.
- Use separate reusable iPhone and iPad device components. Share text styles, swatches, and proof components where that does not constrain device-specific layout.

### Stable localization keys

Name every replaceable text layer with a unique semantic key:

```text
loc.01.title
loc.01.subtitle
loc.02.title
loc.02.subtitle
proof.01.top
proof.01.bottom
```

Name every replaceable simulator screenshot slot by device and panel:

```text
shot.iphone.01
shot.ipad.01
```

Names are discovery keys, not mutation targets. Before replacement, inspect the document, require every requested key to resolve exactly once, record the resolved layer or override IDs, and mutate by ID. Stop that locale on missing or duplicate keys; never use broad text search-and-replace.

## Creating or updating the base template

Reuse an existing approved template when present. Before changing it, inspect its pages and layer tree and screenshot both device masters.

When creating a new template through MCP:

1. Create and save the document at `screenshots/AppStore-Screenshots.sketch`.
2. Create the component page and separate iPhone and iPad template pages.
3. Create each device master and its continuous background.
4. Implement the approved storyboard with the layout toolbelt in `layouts-and-state.md`: reusable device components where needed, masked base-locale screenshots or result crops, background/foreground artwork, fades, editable copy, secondary badges, and verified social proof. Photo-led panels need not contain a device.
5. Add the exact export slices last and name them in App Store order.
6. Screenshot-verify the complete masters as storefront-size contact sheets against the constitution and set-review criteria, plus representative individual slices. Approve the rough set direction before polishing individual panels.
7. Save only after the base localization is approved.

Do not build the whole document in one opaque `run_code` call. Keep creation incremental according to the MCP guide so every structural or visual batch can be inspected.

## Localization input

Accept localization data as a user-provided mapping, localization file, or confirmed project state. Normalize it to semantic keys before touching Sketch. Example:

```json
{
  "base_locale": "en-US",
  "locales": {
    "de-DE": {
      "loc.01.title": "FANGE DAS LICHT EIN",
      "loc.01.subtitle": "Sonnenaufgang, Sonnenuntergang und goldene Stunde"
    }
  }
}
```

Preserve intentional line breaks. Do not translate product names, verified numerals, or social-proof claims beyond the user's approved localization.

Replacing marketing strings does not localize text inside raster screenshots. If a source screenshot contains visible language, require a localized iPhone or iPad capture for that slot and locale. If one is missing, stop that locale/device export and report the exact missing key.

## Render a locale

The base locale may export directly from the approved template. For every other locale:

1. Create a temporary directory and copy the template into it. Never mutate the original template to render a locale.
2. Open the temporary copy through the public Sketch API.
3. Resolve and validate every required text and image key, then record its ID.
4. Replace native `Text.text` values or symbol string overrides by ID. Replace localized screenshot image overrides by ID where required.
5. For symbol instances, call `resizeWithSmartLayout()` after changing text when the component uses Smart Layout.
6. Preserve each panel's approved visible title anchor and line gaps. Honor explicit localized line breaks first, then reduce font size only to the approved minimum. Move the device down when necessary. Never shrink text until it is technically contained but unreadable.
7. Treat RTL and CJK locales as separate visual QA cases. Do not mirror the panorama automatically; use the approved reading direction and inspect the actual result.
8. Use `get_screenshot` to inspect the complete iPhone and iPad masters and any panel whose copy or screenshot changed materially. Fix clipping, overflow, shaping, or collisions before export.
9. Export the named slices through Sketch as opaque 1x PNG files.
10. Close the working document. Remove the temporary copy only after every expected export passes QA.

## Export paths

Use stable locale and device directories:

```text
screenshots/
  AppStore-Screenshots.sketch
  final/
    en-US/
      iphone-6.9/
        01.png
        02.png
      ipad-13/
        01.png
        02.png
    de-DE/
      iphone-6.9/
      ipad-13/
```

Export filenames must preserve App Store order. Do not append automatic numeric suffixes that obscure the intended sequence.

## Required QA

For every locale and device family:

- Confirm the expected slice count and order.
- Confirm every PNG has the exact selected dimensions, is opaque, and has no alpha channel.
- Inspect full-size output and storefront-size thumbnails for clipping, shaping, readability, device alignment, and proof accuracy.
- Reconstruct the exported slices side-by-side without gaps and inspect every seam. A crossing background or device must align pixel-for-pixel.
- Confirm iPhone exports use iPhone captures and components; confirm iPad exports use iPad captures and components.
- Compare against the approved base template so localization changes do not alter unrelated artwork.

Do not claim completion when a locale or device family is missing required strings, screenshots, exports, or visual verification.

## Project state

Save incrementally:

- Renderer: `sketch-template`
- Template path, base locale, and last verified modification date
- Selected iPhone and iPad display classes, orientation, and slice dimensions
- Ordered semantic text and image keys
- Localization source and approved per-locale wording or overrides
- Localized simulator screenshot paths per device and slot
- Export directories and per-locale/device status
- Missing inputs, QA failures, and intentionally retained localized Sketch copies

The template is the design source of truth. `screenshots/aso-state.json` records workflow state; it must not attempt to duplicate every Sketch layer property.
