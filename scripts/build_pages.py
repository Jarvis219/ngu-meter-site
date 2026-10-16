#!/usr/bin/env python3
"""Generates the landing pages: index.html (Vietnamese) and en/index.html (English).

Both languages share one layout, so edit COPY below and re-run:  python3 scripts/build_pages.py
"""
import hashlib, html, json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BASE = "https://jarvis219.github.io/ngu-meter-site/"
EMAIL = "jarvis.219.studio@gmail.com"
SCREEN_W, SCREEN_H = 560, 1217   # assets/screens/*.webp (iPhone 6.9" captures)
CARD_W, CARD_H = 540, 960         # share card

COPY = {
    "vi": {
        "path": "", "html_lang": "vi", "og_locale": "vi_VN",
        "title": "Đo Độ Ngu – Game đố vui xoắn não, câu đố mẹo vô tri cho iPhone",
        "description": "10 câu đố vui, câu lừa và câu xoắn não trong 1 phút. Nhận điểm vô tri, mở khoá huy hiệu, thách bạn bè bằng mã QR. Miễn phí, không quảng cáo, không cần mạng.",
        "brand": "Đo Độ Ngu", "wordmark": "ĐO ĐỘ NGU",
        "nav": [("cach-choi", "Cách chơi"), ("tinh-nang", "Tính năng"), ("hoi-dap", "Hỏi đáp")],
        "switch": ("English", "en/"),
        "eyebrow": "Game đố vui cho iPhone & iPad",
        "h1": "Não bạn đang <mark>đi nghỉ phép</mark>?",
        "lead": "10 câu đố mẹo, câu lừa và câu xoắn não. Khoảng 1 phút. Một kết quả rất đáng ngờ, kèm danh hiệu để khoe với cả nhóm.",
        "cta": "Sắp có trên App Store", "cta2": "Xem cách chơi",
        "chips": ["Miễn phí", "Không quảng cáo", "Không cần mạng", "Tiếng Việt & English"],
        "how_title": "Chơi thế nào?", "how_lead": "Ba bước, một phút, vô số tranh cãi trong nhóm chat.",
        "steps": [
            ("02-hard-question", "Trả lời 10 câu", "Khởi động nhẹ nhàng rồi tăng dần độ khó. 4 câu cuối là xoắn não thật sự 🔥🔥🔥."),
            ("04-result", "Nhận điểm vô tri", "Sai càng nhiều càng vô tri. Kèm một danh hiệu, từ “Tỉnh táo đáng ngờ” tới “Vô tri tối thượng”."),
            ("06-share-card", "Thách bạn bè", "Ảnh 9:16 đăng story có mã QR. Bạn bè quét là chơi đúng 10 câu của bạn, không cần mạng."),
        ],
        "features_title": "Có gì trong app?",
        "features": [
            ("sticker-swirl", "Hơn 1.000 câu", "Đố mẹo, câu lừa, logic, tình huống vô tri và kiến thức “ủa thật hả?”."),
            ("sticker-bolt", "Độ xoắn não", "Mỗi lượt 2 câu dễ, 4 câu vừa, 4 câu khó. Có biểu tượng 🔥 báo trước."),
            ("sticker-question", "Giải thích “Vì sao?”", "Câu khó nào cũng có lời giải ngắn, đọc xong là “à ra thế”."),
            ("sticker-star", "Đề hôm nay & chuỗi ngày", "Cả thế giới chung 10 câu mỗi ngày. Giữ chuỗi 🔥, có nhắc nhở nếu muốn."),
            ("sticker-sparkle", "26 huy hiệu", "Sưu tập danh hiệu, cột mốc và cả huy hiệu bí mật."),
            ("sticker-sock", "Widget màn hình chính", "Xem nhanh chuỗi ngày và đề hôm nay, chạm là vào chơi."),
            ("sticker-exclaim", "Thách đấu offline", "Mã 8 ký tự hoặc QR, dán cả tin nhắn vào là app tự tìm mã."),
            ("sticker-drop", "Riêng tư tuyệt đối", "Không tài khoản, không theo dõi. Mọi thứ nằm trên máy bạn."),
        ],
        "showcase_title": "Sai cũng được, miễn là vui",
        "showcase_lead": "Mascot não hồng phản ứng với từng câu trả lời. Câu khó có lời giải, chơi xong mở khoá huy hiệu mới.",
        "showcase": [("03-answered", "Câu khó có lời giải “Vì sao?”"), ("08-achievements", "Thành tích và huy hiệu")],
        "tiers_title": "Bạn sẽ là ai?",
        "tiers": [("Tỉnh táo đáng ngờ", "0–14"), ("Hơi lag", "15–34"), ("Chế độ tiết kiệm pin", "35–54"),
                  ("Wifi một vạch", "55–74"), ("Não đi nghỉ phép", "75–94"), ("Vô tri tối thượng", "95–100")],
        "badges_title": "Sưu tập huy hiệu",
        "badges": [("goldfish", "Chế độ cá vàng"), ("potato", "Khoai tây biết nói"), ("onebar", "Wifi một vạch"),
                   ("icedtea", "Não đi nghỉ phép"), ("hamster", "Chăm như hamster"), ("voidcat", "Gỡ xoắn đầu tiên"),
                   ("secret_3am", "Cú đêm vô tri"), ("secret_sane", "Thám tử đáng ngờ")],
        "faq_title": "Hỏi đáp",
        "faq": [
            ("Đo Độ Ngu có mất phí không?", "Miễn phí hoàn toàn. Không quảng cáo, không mua trong app."),
            ("Đây có phải bài kiểm tra IQ không?", "Không. Điểm vô tri chỉ để giải trí, không đo trí thông minh hay giá trị của ai cả. Trò đùa nhắm vào tình huống, không nhắm vào bạn."),
            ("Có cần mạng để chơi không?", "Không. Cả câu hỏi, đề hôm nay và thách đấu đều chạy offline. Mã thách đấu tự chứa đủ thông tin để dựng lại đúng đề."),
            ("Thách đấu bạn bè thế nào?", "Chơi xong, gửi ảnh kết quả hoặc mã 8 ký tự. Bạn bè quét QR hoặc bấm “Có mã thách đấu?” rồi dán vào là chơi đúng 10 câu của bạn."),
            ("App có thu thập dữ liệu không?", "Không. Không tài khoản, không theo dõi, không máy chủ. Lịch sử và thành tích chỉ nằm trên máy bạn."),
            ("Chơi được trên iPad không?", "Được. App hỗ trợ cả iPhone và iPad, xoay ngang dọc thoải mái trên iPad."),
        ],
        "final_title": "Sẵn sàng cho não đi nghỉ phép?",
        "final_lead": "Đo Độ Ngu sắp có mặt trên App Store. Trong lúc chờ, hãy đoán xem bạn được mấy điểm vô tri.",
        "footer_privacy": "Quyền riêng tư", "footer_support": "Hỗ trợ",
        "disclaimer": "Chỉ để giải trí, không phải bài kiểm tra IQ.",
        "skip": "Bỏ qua tới nội dung",
        "phone_alt": "Màn hình chính của Đo Độ Ngu trên iPhone",
    },
    "en": {
        "path": "en/", "html_lang": "en", "og_locale": "en_US",
        "title": "Ngu Meter – Brain Teasers, Riddles & Trick Questions Quiz for iPhone",
        "description": "10 riddles, trick questions and brain twisters in a minute. Get a chaos score, unlock badges and challenge friends with a QR code. Free, no ads, works offline.",
        "brand": "Ngu Meter", "wordmark": "NGU METER",
        "nav": [("how", "How it works"), ("features", "Features"), ("faq", "FAQ")],
        "switch": ("Tiếng Việt", "../"),
        "eyebrow": "A silly quiz for iPhone & iPad",
        "h1": "Is your brain <mark>on vacation</mark>?",
        "lead": "10 riddles, trick questions and brain twisters. About a minute. One very questionable result, plus a title to show off to the group chat.",
        "cta": "Coming soon to the App Store", "cta2": "See how it works",
        "chips": ["Free", "No ads", "Works offline", "English & Tiếng Việt"],
        "how_title": "How it works", "how_lead": "Three steps, one minute, endless group-chat arguments.",
        "steps": [
            ("02-hard-question", "Answer 10 questions", "A gentle warm-up that ramps up. The last four are proper brain twisters 🔥🔥🔥."),
            ("04-result", "Get your chaos score", "The more you miss, the more chaotic you are. Plus a title, from “Suspiciously Sane” to “Ultimate Chaos”."),
            ("06-share-card", "Dare your friends", "A story-ready card with a QR code. Friends scan it to play your exact 10 questions, offline."),
        ],
        "features_title": "What's inside",
        "features": [
            ("sticker-swirl", "1,000+ questions", "Riddles, trick questions, logic, everyday chaos and “wait, really?” trivia."),
            ("sticker-bolt", "Brain-twist meter", "Every round: 2 easy, 4 medium, 4 hard, with 🔥 flames as a warning."),
            ("sticker-question", "“Why?” explanations", "Every hard question explains itself in one line. Instant “ohh”."),
            ("sticker-star", "Daily quiz & streaks", "Everyone gets the same 10 questions each day. Keep your 🔥 streak, with optional reminders."),
            ("sticker-sparkle", "26 badges", "Collect titles, milestones and a few secret badges."),
            ("sticker-sock", "Home-screen widget", "Your streak and today's quiz at a glance. Tap to play."),
            ("sticker-exclaim", "Offline challenges", "An 8-character code or QR. Paste a whole message and the app finds the code."),
            ("sticker-drop", "Truly private", "No account, no tracking. Everything stays on your device."),
        ],
        "showcase_title": "Wrong answers, right vibes",
        "showcase_lead": "A pink brain mascot reacts to every answer. Hard questions explain themselves, and finished rounds unlock badges.",
        "showcase": [("03-answered", "Hard questions come with a “Why?”"), ("08-achievements", "Achievements and badges")],
        "tiers_title": "Who will you be?",
        "tiers": [("Suspiciously Sane", "0–14"), ("Slight Lag", "15–34"), ("Low Power Mode", "35–54"),
                  ("One-Bar Wifi", "55–74"), ("Brain on Vacation", "75–94"), ("Ultimate Chaos", "95–100")],
        "badges_title": "Collect badges",
        "badges": [("goldfish", "Goldfish Mode"), ("potato", "Talking Potato"), ("onebar", "One-Bar Wifi"),
                   ("icedtea", "Brain on Vacation"), ("hamster", "Hamster Wheel"), ("voidcat", "First Brain Twister"),
                   ("secret_3am", "3AM Owl"), ("secret_sane", "Suspicious Detective")],
        "faq_title": "FAQ",
        "faq": [
            ("Is Ngu Meter free?", "Completely free. No ads and no in-app purchases."),
            ("Is it an IQ test?", "No. The chaos score is just for fun and doesn't measure anyone's intelligence or worth. The jokes are about the situations, never about you."),
            ("Do I need the internet?", "No. Questions, the daily quiz and challenges all work offline. A challenge code carries everything needed to rebuild the exact round."),
            ("How do challenges work?", "After a round, share the result image or the 8-character code. Friends scan the QR or tap “Got a challenge code?” and paste it to play your exact 10 questions."),
            ("Does the app collect data?", "No. No account, no tracking, no server. History and achievements live only on your device."),
            ("Does it work on iPad?", "Yes. It supports iPhone and iPad, in any orientation on iPad."),
        ],
        "final_title": "Ready to send your brain on vacation?",
        "final_lead": "Ngu Meter is coming soon to the App Store. Meanwhile, guess your chaos score.",
        "footer_privacy": "Privacy", "footer_support": "Support",
        "disclaimer": "For entertainment only, not an IQ test.",
        "skip": "Skip to content",
        "phone_alt": "Ngu Meter home screen on iPhone",
    },
}


# Cache-busting: the stylesheet URL changes whenever its content does.
CSS_VERSION = hashlib.sha1(open(os.path.join(ROOT, "assets", "style.css"), "rb").read()).hexdigest()[:8]


def esc(s):
    return html.escape(s, quote=True)


def page(lang):
    c = COPY[lang]
    up = "../" if c["path"] else ""          # path back to the site root for assets
    url = BASE + c["path"]
    other = "en" if lang == "vi" else "vi"
    shot = lambda name: f'{up}assets/screens/{lang}-{name}.webp'

    app_ld = {
        "@context": "https://schema.org", "@type": "MobileApplication",
        "name": c["brand"], "alternateName": "Đo Độ Ngu" if lang == "en" else "Ngu Meter",
        "operatingSystem": "iOS 17 or later", "applicationCategory": "GameApplication",
        "applicationSubCategory": "Trivia", "inLanguage": ["vi", "en"],
        "description": c["description"], "url": url, "image": BASE + f"assets/og-{lang}.png",
        "screenshot": [BASE + f"assets/screens/{lang}-{n}.webp" for n in ("01-home", "02-hard-question", "04-result")],
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "author": {"@type": "Person", "name": "Jarvis Tran"},
        "isAccessibleForFree": True,
    }
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faq"]]}

    nav = "".join(f'<a href="#{i}">{esc(t)}</a>' for i, t in c["nav"])
    chips = "".join(f"<li>{esc(t)}</li>" for t in c["chips"])
    steps = "".join(f"""
        <li class="step">
          <span class="step-num" aria-hidden="true">{n}</span>
          <div class="phone{' phone-card' if name == '06-share-card' else ''}">
            <img src="{shot(name)}" width="{CARD_W if name == '06-share-card' else SCREEN_W}" height="{CARD_H if name == '06-share-card' else SCREEN_H}" loading="lazy" decoding="async" alt="{esc(t)}">
          </div>
          <h3>{esc(t)}</h3>
          <p>{esc(d)}</p>
        </li>""" for n, (name, t, d) in enumerate(c["steps"], 1))
    features = "".join(f"""
        <li class="feature">
          <img src="{up}assets/{icon}.png" width="56" height="56" alt="" loading="lazy">
          <h3>{esc(t)}</h3>
          <p>{esc(d)}</p>
        </li>""" for icon, t, d in c["features"])
    showcase = "".join(f"""
        <figure>
          <div class="phone"><img src="{shot(name)}" width="{SCREEN_W}" height="{SCREEN_H}" loading="lazy" decoding="async" alt="{esc(cap)}"></div>
          <figcaption>{esc(cap)}</figcaption>
        </figure>""" for name, cap in c["showcase"])
    tiers = "".join(f"""
        <figure><img src="{up}assets/tier-{i}.png" width="120" height="120" loading="lazy" alt=""><figcaption>{esc(t)}<br><span class="score">{r}</span></figcaption></figure>"""
                    for i, (t, r) in enumerate(c["tiers"]))
    badges = "".join(f"""
        <li><img src="{up}assets/badges/{b}.webp" width="96" height="96" loading="lazy" alt=""><span>{esc(t)}</span></li>""" for b, t in c["badges"])
    faq = "".join(f"""
        <details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>""" for q, a in c["faq"])

    css = f"{up}assets/style.css?v={CSS_VERSION}"
    return f"""<!doctype html>
<html lang="{c['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(c['title'])}</title>
<meta name="description" content="{esc(c['description'])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="vi" href="{BASE}">
<link rel="alternate" hreflang="en" href="{BASE}en/">
<link rel="alternate" hreflang="x-default" href="{BASE}">
<meta name="theme-color" content="#FFE45C">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(c['brand'])}">
<meta property="og:locale" content="{c['og_locale']}">
<meta property="og:locale:alternate" content="{COPY[other]['og_locale']}">
<meta property="og:title" content="{esc(c['title'])}">
<meta property="og:description" content="{esc(c['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}assets/og-{lang}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(c['brand'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(c['title'])}">
<meta name="twitter:description" content="{esc(c['description'])}">
<meta name="twitter:image" content="{BASE}assets/og-{lang}.png">
<link rel="icon" type="image/png" sizes="32x32" href="{up}assets/favicon-32.png">
<link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="{shot('01-home')}" type="image/webp">
<link rel="stylesheet" href="{css}">
<script type="application/ld+json">{json.dumps(app_ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
</head>
<body class="landing">
<a class="skip" href="#main">{esc(c['skip'])}</a>
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="{BASE}{c['path']}"><img src="{up}assets/icon.png" width="36" height="36" alt=""><span>{esc(c['brand'])}</span></a>
    <nav aria-label="{esc(c['brand'])}">{nav}</nav>
    <a class="lang-switch" href="{c['switch'][1]}" hreflang="{other}" lang="{other}">{esc(c['switch'][0])}</a>
  </div>
</header>

<main id="main">
  <section class="hero">
    <img class="doodle d1" src="{up}assets/sticker-question.png" alt="">
    <img class="doodle d2" src="{up}assets/sticker-sparkle.png" alt="">
    <img class="doodle d3" src="{up}assets/sticker-bolt.png" alt="">
    <img class="doodle d4" src="{up}assets/sticker-sock.png" alt="">
    <div class="hero-copy">
      <p class="eyebrow"><span class="wordmark-sm">{esc(c['wordmark'])}</span> {esc(c['eyebrow'])}</p>
      <h1>{c['h1']}</h1>
      <p class="lead">{esc(c['lead'])}</p>
      <div class="cta-row">
        <span class="button app-store" role="link" aria-disabled="true"><img src="{up}assets/sticker-star.png" width="24" height="24" alt="">{esc(c['cta'])}</span>
        <a class="button secondary" href="#{c['nav'][0][0]}">{esc(c['cta2'])}</a>
      </div>
      <ul class="chips">{chips}</ul>
    </div>
    <div class="hero-art">
      <div class="phone phone-hero"><img src="{shot('01-home')}" width="{SCREEN_W}" height="{SCREEN_H}" fetchpriority="high" alt="{esc(c['phone_alt'])}"></div>
      <img class="hero-mascot" src="{up}assets/tier-4.png" width="190" height="190" alt="">
    </div>
  </section>

  <section id="{c['nav'][0][0]}" class="block">
    <h2 class="label">{esc(c['how_title'])}</h2>
    <p class="block-lead">{esc(c['how_lead'])}</p>
    <ol class="steps">{steps}
    </ol>
  </section>

  <section id="{c['nav'][1][0]}" class="block">
    <h2 class="label pink">{esc(c['features_title'])}</h2>
    <ul class="features">{features}
    </ul>
  </section>

  <section class="block showcase">
    <div>
      <h2 class="label purple">{esc(c['showcase_title'])}</h2>
      <p class="block-lead">{esc(c['showcase_lead'])}</p>
    </div>
    <div class="showcase-phones">{showcase}
    </div>
  </section>

  <section class="block">
    <h2 class="label">{esc(c['tiers_title'])}</h2>
    <div class="tiers">{tiers}
    </div>
  </section>

  <section class="block">
    <h2 class="label pink">{esc(c['badges_title'])}</h2>
    <ul class="badge-strip">{badges}
    </ul>
  </section>

  <section id="{c['nav'][2][0]}" class="block">
    <h2 class="label purple">{esc(c['faq_title'])}</h2>
    <div class="faq">{faq}
    </div>
  </section>

  <section class="block final">
    <img src="{up}assets/tier-5.png" width="160" height="160" alt="" loading="lazy">
    <h2>{esc(c['final_title'])}</h2>
    <p>{esc(c['final_lead'])}</p>
    <span class="button app-store" role="link" aria-disabled="true"><img src="{up}assets/sticker-star.png" width="24" height="24" alt="">{esc(c['cta'])}</span>
  </section>
</main>

<footer>
  <span class="disclaimer">{esc(c['disclaimer'])}</span><br>
  <a href="{up}privacy/#{lang}">{esc(c['footer_privacy'])}</a> · <a href="{up}support/#{lang}">{esc(c['footer_support'])}</a> ·
  <a href="mailto:{EMAIL}">{EMAIL}</a><br>© 2026 Jarvis Tran
</footer>
</body>
</html>
"""


if __name__ == "__main__":
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page("vi"))
    os.makedirs(os.path.join(ROOT, "en"), exist_ok=True)
    open(os.path.join(ROOT, "en", "index.html"), "w", encoding="utf-8").write(page("en"))
    # Privacy, support and 404 are hand-written: just refresh their stylesheet version.
    for other in ["privacy/index.html", "support/index.html", "404.html"]:
        path = os.path.join(ROOT, other)
        text = re.sub(r'(assets/style\.css)(\?v=[0-9a-f]+)?"', rf'\1?v={CSS_VERSION}"', open(path).read())
        open(path, "w").write(text)
    pages = ["", "en/", "privacy/", "support/"]
    sitemap = "".join(f"  <url><loc>{BASE}{p}</loc><lastmod>2026-10-16</lastmod></url>\n" for p in pages)
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap}</urlset>\n')
    print("pages built")
