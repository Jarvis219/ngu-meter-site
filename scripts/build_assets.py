#!/usr/bin/env python3
"""Builds the landing page images from the app repo (screenshots, badge art, font).

Run from this repo's root:  python3 scripts/build_assets.py
Expects the app repo next to this one (../ngu-meter) and the generated art in ~/Downloads/ngu_assets.
Writes assets/screens/*.webp, assets/badges/*.webp, assets/og-*.png, assets/apple-touch-icon.png, assets/favicon-32.png,
assets/sticker-*.png (cut from the sprite), and right-sized WebP copies of the icon, tier mascots and stickers
for the landing page (assets/web/).
"""
import math, os
from PIL import Image, ImageDraw, ImageFont

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
APP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "ngu-meter")
RAW = os.path.join(APP, "docs", "app-store", "screenshots", "raw")
FONT = os.path.join(APP, "docs", "app-store", "fonts", "Baloo2.ttf")
ART = os.path.expanduser("~/Downloads/ngu_assets")
INK, CREAM, LEMON, PINK, PURPLE = (34, 34, 34), (255, 247, 232), (255, 228, 92), (255, 143, 177), (167, 139, 250)

SCREENS = ["01-home", "02-hard-question", "03-answered", "04-result", "05-challenge", "07-unlocked", "08-achievements"]
BADGES = ["goldfish", "potato", "onebar", "icedtea", "hamster", "voidcat", "secret_3am", "secret_sane"]


def font(size, weight="ExtraBold"):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_name(weight)
    return f


def screens():
    out = os.path.join(SITE, "screens")
    os.makedirs(out, exist_ok=True)
    for lang in ("vi", "en"):
        for name in SCREENS + ["06-share-card"]:
            src = os.path.join(RAW, f"{lang}-{name}.png")
            im = Image.open(src).convert("RGB")
            width = 540 if name == "06-share-card" else 560
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
            im.save(os.path.join(out, f"{lang}-{name}.webp"), quality=82, method=6)


def badges():
    out = os.path.join(SITE, "badges")
    os.makedirs(out, exist_ok=True)
    for b in BADGES:
        im = Image.open(os.path.join(ART, f"badge_{b}.png")).convert("RGBA")
        im.thumbnail((180, 180), Image.LANCZOS)
        im.save(os.path.join(out, f"{b}.webp"), quality=85, method=6)


def icons():
    icon = Image.open(os.path.join(SITE, "icon.png")).convert("RGB")
    icon.resize((180, 180), Image.LANCZOS).save(os.path.join(SITE, "apple-touch-icon.png"), optimize=True)
    icon.resize((32, 32), Image.LANCZOS).save(os.path.join(SITE, "favicon-32.png"), optimize=True)


# Sticker sprite (4x3 grid, transparent background), read in rows.
STICKER_GRID = [["question", "exclaim", "sparkle", "bolt"],
                ["swirl", "drop", "star", "tape"],
                ["bubble", "arrow", "squiggle", "sock"]]


def stickers(max_side=360):
    """Cut each sticker out of the sprite along its own white outline (connected alpha blob), so no
    sticker is clipped or carries slivers of its neighbours. Writes assets/sticker-<name>.png."""
    import numpy as np
    from scipy import ndimage
    sheet = Image.open(os.path.join(ART, "stickers.png")).convert("RGBA")
    alpha = np.array(sheet)[:, :, 3] > 8
    labels, count = ndimage.label(alpha)
    sizes = ndimage.sum(alpha, labels, range(1, count + 1))
    rows, cols = len(STICKER_GRID), len(STICKER_GRID[0])
    cells = {}
    for label, size in enumerate(sizes, 1):
        if size < 2000:  # specks
            continue
        ys, xs = np.nonzero(labels == label)
        r, c = int(ys.mean() * rows / sheet.height), int(xs.mean() * cols / sheet.width)
        cells.setdefault((r, c), []).append(label)
    for (r, c), group in cells.items():
        mask = np.isin(labels, group)
        ys, xs = np.nonzero(mask)
        box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
        piece = np.array(sheet)
        piece[~mask] = 0  # drop anything that isn't this sticker
        im = Image.fromarray(piece).crop(box)
        pad = 4
        out = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
        out.paste(im, (pad, pad))
        out.thumbnail((max_side, max_side), Image.LANCZOS)
        out.save(os.path.join(SITE, f"sticker-{STICKER_GRID[r][c]}.png"), optimize=True)
    assert len(cells) == rows * cols, f"expected {rows * cols} stickers, found {len(cells)}"


def web_images():
    """The landing page shows these PNGs small; serve WebP at twice their largest on-screen size."""
    out = os.path.join(SITE, "web")
    os.makedirs(out, exist_ok=True)
    sizes = {"icon": 72}
    sizes.update({f"tier-{i}": 380 for i in range(6)})
    sizes.update({f"sticker-{n}": 112 for n in ("bolt", "drop", "exclaim", "question", "sock", "sparkle", "star", "swirl")})
    for name, px in sizes.items():
        im = Image.open(os.path.join(SITE, f"{name}.png")).convert("RGBA")
        im.thumbnail((px, px), Image.LANCZOS)
        im.save(os.path.join(out, f"{name}.webp"), quality=86, method=6)


def og_image(lang, title, subtitle):
    """1200x630 social preview: wordmark + tagline on the left, the app on the right."""
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), LEMON)
    d = ImageDraw.Draw(img)
    cx, cy = 900, 330  # sunburst behind the phone
    for i in range(0, 28, 2):
        a0, a1 = 2 * math.pi * i / 28, 2 * math.pi * (i + 1) / 28
        d.polygon([(cx, cy), (cx + 1600 * math.cos(a0), cy + 1600 * math.sin(a0)), (cx + 1600 * math.cos(a1), cy + 1600 * math.sin(a1))], fill=(255, 238, 150))

    # Wordmark pill.
    word = "ĐO ĐỘ NGU" if lang == "vi" else "NGU METER"
    wf = font(78)
    tw = d.textlength(word, font=wf)
    pill = Image.new("RGBA", (int(tw) + 80, 120), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pill)
    pd.rounded_rectangle([0, 10, pill.width - 1, 119], radius=55, fill=INK)
    pd.rounded_rectangle([0, 0, pill.width - 1, 108], radius=55, fill=PINK, outline=INK, width=6)
    pd.text((pill.width / 2, 56), word, font=wf, fill=INK, anchor="mm")
    pill = pill.rotate(3, resample=Image.BICUBIC, expand=True)
    img.paste(pill, (54, 70), pill)

    tf, sf = font(64), font(34, "SemiBold")
    y = 240
    for line in title.split("\n"):
        d.text((70, y), line, font=tf, fill=INK)
        y += 74
    y += 10
    for line in subtitle.split("\n"):
        d.text((72, y), line, font=sf, fill=(70, 70, 70))
        y += 44

    # Phone with the home screen, sticker style.
    shot = Image.open(os.path.join(RAW, f"{lang}-01-home.png")).convert("RGB")
    pw = 290
    shot = shot.resize((pw, round(shot.height * pw / shot.width)), Image.LANCZOS)
    phone = Image.new("RGBA", (pw + 28, shot.height + 28), (0, 0, 0, 0))
    ph = ImageDraw.Draw(phone)
    ph.rounded_rectangle([14, 14, phone.width - 1, phone.height - 1], radius=48, fill=INK)
    ph.rounded_rectangle([0, 0, pw + 13, shot.height + 13], radius=48, fill=INK)
    mask = Image.new("L", shot.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, shot.width - 1, shot.height - 1], radius=40, fill=255)
    phone.paste(shot, (7, 7), mask)
    phone = phone.rotate(-6, resample=Image.BICUBIC, expand=True)
    img.paste(phone, (760, 40), phone)

    mascot = Image.open(os.path.join(ART, "tier_4.png")).convert("RGBA")
    mascot.thumbnail((230, 230), Image.LANCZOS)
    img.paste(mascot, (610, 380), mascot)
    img.save(os.path.join(SITE, f"og-{lang}.png"), optimize=True)


if __name__ == "__main__":
    screens()
    badges()
    icons()
    stickers()
    web_images()
    og_image("vi", "Não bạn đang\nđi nghỉ phép?", "10 câu đố vui xoắn não.\nMột kết quả đáng ngờ.")
    og_image("en", "Is your brain\non vacation?", "10 brain-twisting questions.\nOne questionable result.")
    print("assets built")
