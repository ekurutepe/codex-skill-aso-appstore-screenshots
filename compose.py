#!/usr/bin/env python3
"""Deterministic App Store screenshot composer with reproducible layout manifests."""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CANVAS_W = 1284
CANVAS_H = 2778
FONT_PATH = "/Library/Fonts/SF-Pro-Display-Black.otf"
ASSET_DIR = Path(__file__).with_name("assets")
FRAME_PATH = ASSET_DIR / "device_frame.png"
LAUREL_PATH = ASSET_DIR / "laurel.png"

LAYOUTS = {
    "regular": {
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
        "desc_line_gap": 24,
    },
    "social-proof-vstack": {
        "text_top": 163,
        "device_y": 1115,
        "device_width": 1080,
        "verb_size_max": 335,
        "verb_size_min": 250,
        "desc_size": 104,
        "desc_size_min": 72,
        "max_verb_width": 1040,
        "max_text_width": 1080,
        "verb_desc_gap": 60,
        "desc_line_gap": 24,
        "proof_top": 625,
        "proof_badge_width": 520,
        "proof_gap": 80,
        "proof_text_width": 300,
        "proof_top_line_offset": 130,
        "proof_bottom_line_offset": 200,
        "laurel_height": 330,
        "laurel_outset": 18,
    },
}


def hex_to_rgb(value):
    value = value.lstrip("#")
    if len(value) != 6:
        raise ValueError(f"Expected a six-digit hex colour, got {value!r}")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def make_background(args):
    if args.background_reference:
        reference = Image.open(args.background_reference).convert("RGB")
        reference = reference.resize((CANVAS_W, CANVAS_H), Image.Resampling.LANCZOS)
        width = args.background_edge_width
        edges = Image.new("RGB", (width * 2, CANVAS_H))
        edges.paste(reference.crop((0, 0, width, CANVAS_H)), (0, 0))
        edges.paste(reference.crop((CANVAS_W - width, 0, CANVAS_W, CANVAS_H)), (width, 0))
        strip = edges.resize((1, CANVAS_H), Image.Resampling.BOX)
        return strip.resize((CANVAS_W, CANVAS_H)).convert("RGBA"), {
            "type": "reference-edge-gradient",
            "path": str(Path(args.background_reference).resolve()),
            "edge_width": width,
        }
    if args.background_image:
        image = Image.open(args.background_image).convert("RGBA")
        return image.resize((CANVAS_W, CANVAS_H), Image.Resampling.LANCZOS), {
            "type": "image",
            "path": str(Path(args.background_image).resolve()),
        }
    if args.bg_top or args.bg_bottom:
        top = hex_to_rgb(args.bg_top or args.bg or args.bg_bottom)
        bottom = hex_to_rgb(args.bg_bottom or args.bg or args.bg_top)
        strip = Image.new("RGBA", (1, CANVAS_H))
        pixels = strip.load()
        for y in range(CANVAS_H):
            amount = y / (CANVAS_H - 1)
            pixels[0, y] = tuple(round(a + (b - a) * amount) for a, b in zip(top, bottom)) + (255,)
        return strip.resize((CANVAS_W, CANVAS_H)), {
            "type": "vertical-gradient",
            "top": "#%02X%02X%02X" % top,
            "bottom": "#%02X%02X%02X" % bottom,
        }
    colour = args.bg or "#E31837"
    return Image.new("RGBA", (CANVAS_W, CANVAS_H), (*hex_to_rgb(colour), 255)), {
        "type": "solid",
        "colour": colour.upper(),
    }


def word_wrap(draw, text, font, max_width):
    lines, current = [], ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_font(font_path, text, max_width, size_max, size_min):
    draw = ImageDraw.Draw(Image.new("L", (1, 1)))
    for size in range(size_max, size_min - 1, -2):
        font = ImageFont.truetype(font_path, size)
        if draw.textbbox((0, 0), text, font=font)[2] <= max_width:
            return font
    return ImageFont.truetype(font_path, size_min)


def draw_centered_lines(draw, top, text, font, max_width, line_gap):
    lines = word_wrap(draw, text, font, max_width)
    y = top
    for index, line in enumerate(lines):
        box = draw.textbbox((0, 0), line, font=font)
        height = box[3] - box[1]
        draw.text((CANVAS_W // 2, y - box[1]), line, fill="white", font=font, anchor="mt")
        y += height
        if index < len(lines) - 1:
            y += line_gap
    return y


def exact_width_text(layer, font_path, center_x, center_y, text, target_width):
    font = fit_font(font_path, text, target_width, 110, 28)
    draw = ImageDraw.Draw(Image.new("L", (1, 1)))
    box = draw.textbbox((0, 0), text, font=font)
    line = Image.new("RGBA", (box[2] - box[0] + 8, box[3] - box[1] + 8))
    ImageDraw.Draw(line).text((4 - box[0], 4 - box[1]), text, font=font, fill="white")
    line = line.crop(line.getchannel("A").getbbox())
    line = line.resize((target_width, line.height), Image.Resampling.LANCZOS)
    layer.alpha_composite(line, (center_x - target_width // 2, center_y - line.height // 2))


def parse_proof(value):
    if value.lstrip().startswith("{"):
        claim = json.loads(value)
        if not claim.get("top") or not claim.get("bottom"):
            raise ValueError("Proof JSON requires top and bottom fields")
        return claim
    parts = value.split("|", 1)
    if len(parts) != 2:
        raise ValueError("Proof shorthand must be TOP|BOTTOM")
    return {"kind": "custom", "top": parts[0], "bottom": parts[1]}


def draw_social_proof(canvas, font_path, claims, layout, laurel_path):
    if len(claims) > 2:
        raise ValueError("Use at most two social-proof wreaths per screenshot")

    branch = Image.open(laurel_path).convert("RGBA")
    branch = branch.crop(branch.getchannel("A").getbbox())
    height = layout["laurel_height"]
    branch = branch.resize((round(branch.width * height / branch.height), height), Image.Resampling.LANCZOS)
    white = Image.new("RGBA", branch.size, "white")
    white.putalpha(branch.getchannel("A"))

    badge_width = layout["proof_badge_width"]
    gap = layout["proof_gap"]
    total_width = len(claims) * badge_width + (len(claims) - 1) * gap
    start_x = (CANVAS_W - total_width) // 2
    for index, claim in enumerate(claims):
        x = start_x + index * (badge_width + gap)
        outset = layout["laurel_outset"]
        canvas.alpha_composite(white, (x - outset, layout["proof_top"]))
        canvas.alpha_composite(
            white.transpose(Image.Transpose.FLIP_LEFT_RIGHT),
            (x + badge_width + outset - white.width, layout["proof_top"]),
        )
        center_x = x + badge_width // 2
        exact_width_text(
            canvas,
            font_path,
            center_x,
            layout["proof_top"] + layout["proof_top_line_offset"],
            claim["top"].upper(),
            layout["proof_text_width"],
        )
        exact_width_text(
            canvas,
            font_path,
            center_x,
            layout["proof_top"] + layout["proof_bottom_line_offset"],
            claim["bottom"].upper(),
            layout["proof_text_width"],
        )


def place_device(canvas, screenshot_path, device_y, device_width):
    frame = Image.open(FRAME_PATH).convert("RGBA")
    scale = device_width / frame.width
    frame = frame.resize((device_width, round(frame.height * scale)), Image.Resampling.LANCZOS)
    bezel = round(15 * scale)
    screen_width = device_width - 2 * bezel
    corner_radius = round(62 * scale)
    device_x = (CANVAS_W - device_width) // 2
    screen_x = device_x + bezel
    screen_y = device_y + bezel

    shot = Image.open(screenshot_path).convert("RGBA")
    shot_scale = screen_width / shot.width
    shot = shot.resize((screen_width, round(shot.height * shot_scale)), Image.Resampling.LANCZOS)
    screen_height = CANVAS_H - screen_y + 500

    mask = Image.new("L", canvas.size)
    ImageDraw.Draw(mask).rounded_rectangle(
        (screen_x, screen_y, screen_x + screen_width, screen_y + screen_height),
        radius=corner_radius,
        fill=255,
    )
    screen = Image.new("RGBA", canvas.size)
    ImageDraw.Draw(screen).rounded_rectangle(
        (screen_x, screen_y, screen_x + screen_width, screen_y + screen_height),
        radius=corner_radius,
        fill="black",
    )
    screen.paste(shot, (screen_x, screen_y))
    screen.putalpha(mask)
    canvas.alpha_composite(screen)
    canvas.alpha_composite(frame, (device_x, device_y))
    return {"x": device_x, "y": device_y, "width": device_width, "frame": str(FRAME_PATH.resolve())}


def resolved_layout(args):
    layout = dict(LAYOUTS[args.layout])
    for key in layout:
        value = getattr(args, key, None)
        if value is not None:
            layout[key] = value
    return layout


def compose(args):
    layout = resolved_layout(args)
    font_path = args.font or FONT_PATH
    canvas, background_spec = make_background(args)
    draw = ImageDraw.Draw(canvas)

    verb = args.verb.upper()
    desc = args.desc.upper()
    verb_font = fit_font(
        font_path,
        verb,
        layout["max_verb_width"],
        layout["verb_size_max"],
        layout["verb_size_min"],
    )
    desc_font = fit_font(
        font_path,
        desc,
        layout["max_text_width"],
        layout["desc_size"],
        layout["desc_size_min"],
    )
    text_bottom = draw_centered_lines(
        draw,
        layout["text_top"],
        verb,
        verb_font,
        layout["max_verb_width"],
        layout["desc_line_gap"],
    )
    draw_centered_lines(
        draw,
        text_bottom + layout["verb_desc_gap"],
        desc,
        desc_font,
        layout["max_text_width"],
        layout["desc_line_gap"],
    )

    claims = [parse_proof(value) for value in args.proof]
    proof_mode = args.social_proof
    if proof_mode == "auto":
        proof_mode = "laurels" if claims else "none"
    if proof_mode == "laurels":
        if not claims:
            raise ValueError("Laurel social proof requires at least one --proof claim")
        if "proof_top" not in layout:
            raise ValueError("Laurel social proof requires the social-proof-vstack layout")
        draw_social_proof(canvas, font_path, claims, layout, args.laurel_asset or LAUREL_PATH)

    device = place_device(canvas, args.screenshot, layout["device_y"], layout["device_width"])
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, "PNG")

    manifest = {
        "schema_version": 1,
        "output": str(output.resolve()),
        "canvas": {"width": CANVAS_W, "height": CANVAS_H},
        "layout": {"name": args.layout, "parameters": layout},
        "background": background_spec,
        "content": {
            "verb": verb,
            "descriptor": desc,
            "locale": args.locale,
            "screenshot": str(Path(args.screenshot).resolve()),
        },
        "typography": {"font": str(Path(font_path).resolve())},
        "device": device,
        "social_proof": {
            "mode": proof_mode,
            "laurel_asset": str(Path(args.laurel_asset or LAUREL_PATH).resolve()) if proof_mode == "laurels" else None,
            "claims": claims,
        },
    }
    manifest_path = Path(args.manifest) if args.manifest else output.with_suffix(".aso.json")
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"✓ {output} ({CANVAS_W}×{CANVAS_H})")
    print(f"✓ {manifest_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layout", choices=LAYOUTS, default="regular")
    parser.add_argument("--bg", help="Solid background hex colour")
    parser.add_argument("--bg-top", help="Vertical-gradient top hex colour")
    parser.add_argument("--bg-bottom", help="Vertical-gradient bottom hex colour")
    parser.add_argument("--background-image", help="Exact background image to resize to the canvas")
    parser.add_argument("--background-reference", help="Approved screenshot whose edge colours define the background")
    parser.add_argument("--background-edge-width", type=int, default=48)
    parser.add_argument("--font", help="Font path; defaults to SF Pro Display Black")
    parser.add_argument("--verb", required=True, help="Primary title/action verb")
    parser.add_argument("--desc", required=True, help="Benefit subtitle/descriptor")
    parser.add_argument("--locale", default="und", help="Storefront locale, e.g. en-US")
    parser.add_argument("--screenshot", required=True, help="Simulator screenshot path")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--manifest", help="Output manifest path; defaults beside the PNG")
    parser.add_argument("--social-proof", choices=("auto", "none", "laurels"), default="auto")
    parser.add_argument(
        "--proof",
        action="append",
        default=[],
        help='Repeat TOP|BOTTOM or JSON, e.g. {"kind":"downloads","top":"700K+","bottom":"DOWNLOADS"}',
    )
    parser.add_argument("--laurel-asset", help="Transparent single-branch laurel PNG")

    parameter_names = sorted({key for layout in LAYOUTS.values() for key in layout})
    for name in parameter_names:
        parser.add_argument(f"--{name.replace('_', '-')}", dest=name, type=int)
    compose(parser.parse_args())


if __name__ == "__main__":
    main()
