"""Bakes by Hoorain - Streamlit website (warm artisanal bakery design).
Run: streamlit run app.py  (from this folder)
Design: research-backed 2025/26 bakery trends — warm cream canvas, photo hero,
occasion categories, clear pricing, WhatsApp-first ordering.
"""
import base64
import io
import os
import urllib.parse

import streamlit as st

from images_b64 import IMAGES

WHATSAPP_NUMBER = "923127904882"
WA_BASE = f"https://wa.me/{WHATSAPP_NUMBER}"

TIKTOK_URL = "https://www.tiktok.com/@bakesbyhoorain0"
FACEBOOK_URL = "https://www.facebook.com/share/1FJYBezTW8/"
INSTAGRAM_URL = "https://www.instagram.com/bakesbyhoorain"

SHEET_ID = "1Tc8csdlZ655AU3dFLrj5TC1Fx4uG4rBZOecHV1fgB9w"

st.set_page_config(
    page_title="Bakes by Hoorain — Customized Cakes in Karachi",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def wa_link(message: str) -> str:
    return WA_BASE + "?text=" + urllib.parse.quote(message)


def img_bytes(name: str):
    b64 = IMAGES.get(name)
    if not b64:
        return None
    return io.BytesIO(base64.b64decode(b64))


def fetch_sheet_rows(sheet_name):
    import csv
    import urllib.request

    url = (
        "https://docs.google.com/spreadsheets/d/"
        + SHEET_ID
        + "/gviz/tq?tqx=out:csv&sheet="
        + urllib.parse.quote(sheet_name)
    )
    try:
        with urllib.request.urlopen(url, timeout=12) as r:
            text = r.read().decode("utf-8")
        return list(csv.reader(io.StringIO(text)))[1:]
    except Exception:
        return []


def drive_thumb(link):
    import re

    m = re.search(r"[-\w]{25,}", link or "")
    return "https://drive.google.com/thumbnail?id=" + m.group(0) + "&sz=w1000" if m else ""


# ---------------- Data ----------------
GALLERY = [
    ("blue-rosette.jpg", "Blue Rosette Cake"),
    ("anniversary-love.jpg", 'Anniversary "I Love You" Cake'),
    ("umrah-mubarak.jpg", "Umrah Mubarak Cake"),
    ("bear-theme.jpg", "Bear Theme Cake"),
    ("pink-birthday-topper.jpg", "Pink Birthday Cake with Topper"),
    ("daisy-birthday.jpg", "Daisy Birthday Cake"),
    ("best-wishes-roses.jpg", '"Best Wishes" Rose Wreath Cake'),
    ("blue-white-rosette.jpg", "Blue & White Rosette Cake"),
    ("lily-19th.jpg", "Lily Flower 19th Birthday Cake"),
    ("elegant-black-gold.jpg", "Elegant Black & Gold Birthday Cake"),
    ("calendar-september.jpg", "Calendar Theme Cake"),
    ("filled-donuts.jpg", "Calendar Cake"),
    ("glazed-donuts.jpg", "Chocolate-Filled Donuts"),
    ("ribbon-cake.jpg", "Chocolate-Glazed Donuts"),
    ("bye13-hello14.jpg", "Pink & Blue Ribbon Cake"),
    ("two-tier-pearl.jpg", "Two-Tier Pearl White Cake"),
    ("cupcakes-dessert.jpg", "Cupcakes & Chocolate Dessert Cups"),
    ("sprinkle-donuts.jpg", "Sprinkle Donuts"),
]

OCCASIONS = [
    ("pink-birthday-topper.jpg", "Birthday Cakes", "Make their day extra sweet"),
    ("anniversary-love.jpg", "Anniversary Cakes", "Celebrate your love story"),
    ("umrah-mubarak.jpg", "Umrah Mubarak", "Blessed treats for blessed journeys"),
    ("two-tier-pearl.jpg", "Weddings & 2-Tier", "Grand cakes for grand days"),
    ("sprinkle-donuts.jpg", "Donuts & Treats", "Fresh, glazed & irresistible"),
    ("elegant-black-gold.jpg", "Custom Themes", "Any design you dream up"),
]

BESTSELLERS = [
    ("elegant-black-gold.jpg", "Elegant Black & Gold", "2 lb — Rs 2,000"),
    ("bear-theme.jpg", "Bear Theme Cake", "2 lb — Rs 2,000"),
    ("lily-19th.jpg", "Lilly Flower Cake", "Rs 1,200"),
    ("two-tier-pearl.jpg", "2-Tier Pearl Cake", "3 lb — Rs 4,000"),
    ("calendar-september.jpg", "Calendar Theme Cake", "2 lb — Rs 2,000"),
    ("pink-birthday-topper.jpg", "Pink Birthday Cake", "2 lb — Rs 2,000"),
]

MENU_CAKES = [
    ("Elegant Design", "2 lb", 2000),
    ("Birthday Cake", "2 lb", 2000),
    ("Anniversary Theme", "2 lb", 2000),
    ("Chocolate Cake", "2 lb", 2000),
    ("Black Forest", "2 lb", 2000),
    ("Bear Theme", "2 lb", 2000),
    ("Umrah Theme", "2 lb", 2000),
    ("Pinterest Design", "2 lb", 2000),
    ("Husband Birthday Theme", "2 lb", 1800),
    ("Lilly Flower Cake (chocolate fudge)", "standard", 1200),
    ("Chocolate Fudge", "1 lb", 700),
    ("Tea Cake", "1 lb", 500),
    ("Fire Cake Unicorn Theme", "2 lb", 2500),
    ("2-Tier Cake", "3 lb", 4000),
    ("Pinterest Design", "2.5 lb", 3000),
]

MENU_DESSERTS = [
    ("Chocolate Dessert", "one glass", 300),
    ("Three Milk Cake", "per box", 200),
]

# --- Live menu from the admin Google Sheet (overrides the lists above) ---
_sheet_menu = fetch_sheet_rows("Menu")
if _sheet_menu:
    _cakes, _desserts = [], []
    for _r in _sheet_menu:
        if len(_r) < 3:
            continue
        _name, _size, _price = _r[0].strip(), _r[1].strip(), _r[2].strip()
        if not _name or not _price.replace(",", "").replace(".", "").isdigit():
            continue
        _cat = (_r[3].strip() if len(_r) > 3 else "") or "Cakes"
        _item = (_name, _size, int(_price.replace(",", "")))
        (_desserts if _cat.lower().startswith("dessert") else _cakes).append(_item)
    if _cakes or _desserts:
        MENU_CAKES, MENU_DESSERTS = _cakes, _desserts

# --- Extra gallery photos added via the admin Google Sheet ---
EXTRA_GALLERY = []
for _r in fetch_sheet_rows("Gallery"):
    if len(_r) < 2:
        continue
    _cap, _link = _r[0].strip(), _r[1].strip()
    if not _cap or not _link or _cap.lower().startswith("(example)") or _link.lower().startswith("paste "):
        continue
    _src = drive_thumb(_link)
    if _src:
        EXTRA_GALLERY.append((_src, _cap))

# Refresh bestseller price strings from the live sheet when names match
if _sheet_menu:
    _price_by_name = {}
    for _r in _sheet_menu:
        if len(_r) >= 3 and _r[0].strip() and _r[2].strip():
            _price_by_name[_r[0].strip().lower()] = _r[2].strip()
    _new_best = []
    for _fname, _name, _price_str in BESTSELLERS:
        for _k, _v in _price_by_name.items():
            if _k in _name.lower() or _name.lower() in _k:
                _price_str = "Rs " + _v
                break
        _new_best.append((_fname, _name, _price_str))
    BESTSELLERS = _new_best


# ---------------- Style ----------------
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,500&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    .stApp { background: #fdf8f3; }

    /* HERO */
    .hero { display:flex; flex-wrap:wrap; align-items:center; gap:1.6rem;
            background: linear-gradient(135deg, #fff5ee 0%, #fdeee4 55%, #fbd9c8 100%);
            border-radius: 26px; padding: 2rem 2.2rem; margin-bottom: .6rem;
            border: 1px solid #f3ddc9; box-shadow: 0 18px 50px rgba(190,120,80,.14); }
    .hero-text { flex: 1 1 300px; }
    .hero-kicker { color:#c26a4a; font-weight:600; letter-spacing:3px; font-size:.78rem;
            text-transform:uppercase; margin-bottom:.5rem; }
    .hero h1 { font-family:'Playfair Display',serif; font-size:2.7rem; line-height:1.12;
            color:#4a2c22; margin:.1rem 0 .7rem 0; }
    .hero h1 em { color:#e8557a; font-style:italic; }
    .hero p.sub { color:#8a6a58; font-size:1.02rem; font-weight:300; margin-bottom:1.2rem; }
    .hero-photo { flex: 1 1 260px; text-align:center; }
    .hero-photo img { width:100%; max-width:380px; border-radius:22px;
            box-shadow: 0 24px 60px rgba(190,90,60,.28); border:6px solid #fff; }

    /* BUTTONS */
    .wa-btn { display:inline-block; background:linear-gradient(135deg,#25D366,#1da851);
            color:#fff !important; padding:.8rem 1.9rem; border-radius:999px; font-weight:600;
            text-decoration:none; font-size:1.02rem; margin:.3rem .2rem;
            box-shadow:0 10px 26px rgba(37,211,102,.35); transition:transform .18s ease; }
    .wa-btn:hover { transform:translateY(-2px); color:#fff !important; }
    .ghost-btn { display:inline-block; background:#fff; color:#c26a4a !important;
            border:2px solid #eec9ae; padding:.72rem 1.7rem; border-radius:999px; font-weight:600;
            text-decoration:none; font-size:1rem; margin:.3rem .2rem; transition:all .18s ease;}
    .ghost-btn:hover { border-color:#e8557a; color:#e8557a !important; }

    /* TRUST BADGES */
    .badges { display:flex; flex-wrap:wrap; gap:.6rem; justify-content:center; margin:1.1rem 0 .4rem 0; }
    .badge { background:#fff; border:1px solid #f0d9c2; color:#8a5a3b; border-radius:999px;
            padding:.45rem 1.1rem; font-size:.86rem; font-weight:500;
            box-shadow:0 4px 14px rgba(190,120,80,.08); }
    .badge b { color:#e8557a; }

    /* SECTIONS */
    .sec { text-align:center; margin:2.2rem 0 .3rem 0; }
    .sec h2 { font-family:'Playfair Display',serif; font-size:1.9rem; color:#4a2c22; margin-bottom:.25rem; }
    .sec p { color:#a07a62; font-weight:300; font-size:.95rem; }
    .sec .rule { width:64px; height:3px; background:linear-gradient(90deg,#e8557a,#f5b942);
            border-radius:2px; margin:.6rem auto 0 auto; }

    /* CARDS */
    .card { background:#fff; border:1px solid #f3e2d2; border-radius:20px; padding:.85rem;
            text-align:center; height:100%; box-shadow:0 10px 30px rgba(190,120,80,.10);
            transition:transform .22s ease, box-shadow .22s ease; }
    .card:hover { transform:translateY(-5px); box-shadow:0 18px 44px rgba(190,120,80,.20); }
    .card img { border-radius:14px; }
    .card h4 { font-family:'Playfair Display',serif; color:#4a2c22; font-size:1.08rem; margin:.65rem 0 .15rem 0; }
    .card .desc { color:#a07a62; font-size:.85rem; font-weight:300; margin:0 0 .35rem 0; }
    .card .pr { color:#e8557a; font-weight:600; font-size:1.02rem; margin-bottom:.55rem; }
    .occ-card { cursor:pointer; }
    .occ-card h4 { font-size:1.12rem; }

    /* MENU */
    .menu-item { background:#fff; border:1px solid #f3e2d2; border-radius:16px;
            padding:.7rem 1rem; margin-bottom:.55rem; box-shadow:0 6px 18px rgba(190,120,80,.07); }
    .menu-item .nm { font-weight:500; color:#4a2c22; font-size:.98rem; }
    .menu-item .pr { color:#e8557a; font-weight:600; font-size:1.05rem; white-space:nowrap; }
    .menu-item .sz { color:#b08a6d; font-size:.82rem; }

    /* MISC */
    .note-bar { background:#fff7ef; border:1px dashed #e8b98a; border-radius:16px;
            padding:.9rem 1.2rem; text-align:center; color:#8a5a3b; margin-top:.9rem; }
    .howto { background:#fff; border:1px solid #f3e2d2; border-radius:20px; padding:1.3rem 1.5rem;
            color:#6b4a38; box-shadow:0 10px 30px rgba(190,120,80,.10); }
    .howto b { color:#4a2c22; }
    .howto .step { display:flex; gap:.8rem; align-items:flex-start; margin-bottom:.7rem; }
    .howto .n { background:linear-gradient(135deg,#e8557a,#f5b942); color:#fff; font-weight:600;
            width:30px; height:30px; border-radius:50%; display:flex; align-items:center;
            justify-content:center; flex-shrink:0; font-size:.9rem; }
    .social-btn { display:inline-block; background:#fff; color:#c26a4a !important;
            border:1.5px solid #eec9ae; padding:.55rem 1.3rem; border-radius:999px; font-weight:500;
            text-decoration:none; margin:.25rem; font-size:.92rem; transition:all .18s ease; }
    .social-btn:hover { border-color:#e8557a; color:#e8557a !important; transform:translateY(-2px); }
    .footer { text-align:center; color:#b08a6d; font-size:.85rem; padding:2.2rem 0 1.2rem 0; font-weight:300; }
    .stImage img { border-radius:14px; }
    </style>
    """,
    unsafe_allow_html=True,
)


def section(title, sub=""):
    st.markdown(
        f'<div class="sec"><h2>{title}</h2><p>{sub}</p><div class="rule"></div></div>',
        unsafe_allow_html=True,
    )


# ---------------- HERO ----------------
_hero_b64 = base64.b64encode(img_bytes("pink-birthday-topper.jpg").getvalue()).decode()
_logo_b64 = base64.b64encode(img_bytes("logo.jpg").getvalue()).decode()
st.markdown(
    '<div class="hero">'
    '<div class="hero-text">'
    f'<img src="data:image/jpeg;base64,{_logo_b64}" width="86" style="border-radius:50%;border:3px solid #fff;box-shadow:0 8px 22px rgba(190,120,80,.25);">'
    '<div class="hero-kicker">Homemade with love · Karachi</div>'
    "<h1>Customized cakes, made just for your <em>special moments</em></h1>"
    '<p class="sub">Birthdays, anniversaries, Umrah celebrations, Pinterest designs & fresh donuts — '
    "every order baked at home and finished by hand, exactly the way you pictured it.</p>"
    f'<a class="wa-btn" href="{wa_link("Assalam-o-Alaikum! I want to order a cake from Bakes by Hoorain.")}" target="_blank">💬 Order on WhatsApp</a>'
    '<a class="ghost-btn" href="#price-menu">See the menu</a>'
    "</div>"
    '<div class="hero-photo">'
    f'<img src="data:image/jpeg;base64,{_hero_b64}" alt="Signature pink birthday cake">'
    "</div>"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="badges">'
    '<span class="badge">📍 Karachi based home bakery</span>'
    '<span class="badge">Cakes from <b>Rs 500</b></span>'
    '<span class="badge">Treats from <b>Rs 200</b></span>'
    '<span class="badge"><b>100%</b> made to order</span>'
    "</div>",
    unsafe_allow_html=True,
)


# ---------------- SHOP BY OCCASION ----------------
section("Shop by Occasion", "Tell us the celebration — we'll bake the cake")
ocols = st.columns(3)
for i, (fname, name, desc) in enumerate(OCCASIONS):
    p = img_bytes(fname)
    with ocols[i % 3]:
        st.markdown('<div class="card occ-card">', unsafe_allow_html=True)
        if p:
            st.image(p, use_container_width=True)
        st.markdown(f"<h4>{name}</h4><p class='desc'>{desc}</p>", unsafe_allow_html=True)
        st.markdown(
            f'<a class="wa-btn" href="{wa_link(f"Assalam-o-Alaikum! I want a {name} cake from Bakes by Hoorain.")}" target="_blank">Order</a>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


# ---------------- BESTSELLERS ----------------
section("Bestsellers", "Most loved cakes by our customers")
bcols = st.columns(3)
for i, (fname, name, price) in enumerate(BESTSELLERS):
    p = img_bytes(fname)
    with bcols[i % 3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if p:
            st.image(p, use_container_width=True)
        st.markdown(f"<h4>{name}</h4><p class='pr'>{price}</p>", unsafe_allow_html=True)
        st.markdown(
            f'<a class="wa-btn" href="{wa_link(f"Assalam-o-Alaikum! I want to order: {name} ({price})")}" target="_blank">Order</a>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


# ---------------- SLIDER ----------------
section("Fresh From Our Oven", "A little glimpse of what we bake")
_slider_tags = []
for fname, cap in GALLERY:
    b64 = IMAGES.get(fname)
    if not b64:
        continue
    safe_cap = cap.replace('"', "").replace("<", "").replace(">", "")
    _slider_tags.append(
        '<img src="data:image/jpeg;base64,' + b64 + '" alt="' + safe_cap + '" loading="lazy">'
    )
_slider_doubled = "".join(_slider_tags) * 2
st.components.v1.html(
    "<style>"
    ".cslider{overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,#000 7%,#000 93%,transparent);"
    "mask-image:linear-gradient(90deg,transparent,#000 7%,#000 93%,transparent)}"
    ".ctrack{display:flex;gap:14px;width:max-content;animation:cslide 45s linear infinite;padding:6px 0}"
    ".ctrack img{height:160px;width:160px;object-fit:cover;border-radius:18px;border:4px solid #fff;"
    "box-shadow:0 10px 26px rgba(190,120,80,.22)}"
    "@keyframes cslide{to{transform:translateX(-50%)}}"
    "</style>"
    '<div class="cslider"><div class="ctrack">' + _slider_doubled + "</div></div>",
    height=190,
    scrolling=False,
)


# ---------------- MENU ----------------
section("Price Menu", "Live from our kitchen — always up to date")
st.markdown('<div id="price-menu"></div>', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;font-family:\'Playfair Display\',serif;font-size:1.3rem;color:#4a2c22;margin:1rem 0 .8rem 0;">Cakes</p>',
    unsafe_allow_html=True,
)
for name, size, price in MENU_CAKES:
    mc1, mc2 = st.columns([4, 2])
    with mc1:
        st.markdown(
            f'<div class="menu-item"><span class="nm">{name}</span><br><span class="sz">{size}</span></div>',
            unsafe_allow_html=True,
        )
    with mc2:
        st.markdown(
            f'<div class="menu-item" style="text-align:center;"><span class="pr">Rs {price:,}</span><br>'
            f'<a class="wa-btn" style="padding:.4rem 1.1rem;font-size:.88rem;margin:.3rem 0 0 0;" '
            f'href="{wa_link(f"Assalam-o-Alaikum! I want to order: {name} ({size} - Rs {price:,})")}" target="_blank">Order</a></div>',
            unsafe_allow_html=True,
        )

st.markdown(
    '<p style="text-align:center;font-family:\'Playfair Display\',serif;font-size:1.3rem;color:#4a2c22;margin:1.2rem 0 .8rem 0;">Desserts</p>',
    unsafe_allow_html=True,
)
for name, size, price in MENU_DESSERTS:
    mc1, mc2 = st.columns([4, 2])
    with mc1:
        st.markdown(
            f'<div class="menu-item"><span class="nm">{name}</span><br><span class="sz">{size}</span></div>',
            unsafe_allow_html=True,
        )
    with mc2:
        st.markdown(
            f'<div class="menu-item" style="text-align:center;"><span class="pr">Rs {price:,}</span><br>'
            f'<a class="wa-btn" style="padding:.4rem 1.1rem;font-size:.88rem;margin:.3rem 0 0 0;" '
            f'href="{wa_link(f"Assalam-o-Alaikum! I want to order: {name} ({size} - Rs {price:,})")}" target="_blank">Order</a></div>',
            unsafe_allow_html=True,
        )

st.markdown(
    '<div class="note-bar">🎨 Custom designs available on request — just message us on WhatsApp!</div>',
    unsafe_allow_html=True,
)


# ---------------- GALLERY ----------------
section("Gallery", "Every cake tells a story — tap any photo to view it bigger")
gcols = st.columns(3)
shown = 0
for fname, caption in GALLERY:
    p = img_bytes(fname)
    if not p:
        continue
    with gcols[shown % 3]:
        st.image(p, caption=caption, use_container_width=True)
    shown += 1
for src, caption in EXTRA_GALLERY:
    with gcols[shown % 3]:
        st.image(src, caption=caption, use_container_width=True)
    shown += 1


# ---------------- HOW TO ORDER ----------------
section("How to Order", "Three easy steps")
st.markdown(
    '<div class="howto">'
    '<div class="step"><div class="n">1</div><div><b>Pick</b> your cake from the menu or gallery above.</div></div>'
    '<div class="step"><div class="n">2</div><div><b>Tap Order</b> — WhatsApp opens with your order message ready.</div></div>'
    '<div class="step"><div class="n">3</div><div><b>Send</b> it to us on <b>0312 7904882</b> — we\'ll confirm your design & delivery. ✅</div></div>'
    "</div>",
    unsafe_allow_html=True,
)
st.markdown(
    f'<div style="text-align:center;margin-top:1rem;"><a class="wa-btn" href="{wa_link("Assalam-o-Alaikum! I want to place an order.")}" target="_blank">💬 Chat on WhatsApp: 0312 7904882</a></div>',
    unsafe_allow_html=True,
)


# ---------------- ABOUT ----------------
section("About", "Baked at home, with love")
st.markdown(
    '<div class="howto" style="text-align:center;">Bakes by Hoorain is a home-based bakery in Karachi, '
    "making customized cakes for birthdays, anniversaries, Umrah celebrations and every special moment. 🌸</div>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div style="text-align:center;margin-top:1rem;">'
    f'<a class="social-btn" href="{TIKTOK_URL}" target="_blank">🎵 TikTok</a>'
    f'<a class="social-btn" href="{INSTAGRAM_URL}" target="_blank">📸 Instagram</a>'
    f'<a class="social-btn" href="{FACEBOOK_URL}" target="_blank">📘 Facebook</a>'
    "</div>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="footer">Bakes by Hoorain · Karachi · WhatsApp 0312 7904882<br>Made with 💖 at home</div>',
    unsafe_allow_html=True,
)
