#!/usr/bin/env python3
"""Builds the landing page images from the app repo (screenshots, badge art, font).

Run from this repo's root:  python3 scripts/build_assets.py
Expects the app repo next to this one (../ngu-meter) and the generated art in ~/Downloads/ngu_assets.
Writes assets/screens/*.webp, assets/badges/*.webp, assets/og-*.png, assets/apple-touch-icon.png, assets/favicon-32.png
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
    og_image("vi", "Não bạn đang\nđi nghỉ phép?", "10 câu đố vui xoắn não.\nMột kết quả đáng ngờ.")
    og_image("en", "Is your brain\non vacation?", "10 brain-twisting questions.\nOne questionable result.")
    print("assets built")
