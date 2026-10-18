"""Bakes by Hoorain - Streamlit website.
Run: streamlit run app.py  (from this folder)
Deploy free: push this folder to GitHub, then deploy via share.streamlit.io
"""
import io
import os
import urllib.parse

import streamlit as st

from images_b64 import IMAGES

BASE = os.path.dirname(os.path.abspath(__file__))

WHATSAPP_NUMBER = "923127904882"
WA_BASE = f"https://wa.me/{WHATSAPP_NUMBER}"

TIKTOK_URL = "https://www.tiktok.com/@bakesbyhoorain0"
FACEBOOK_URL = "https://www.facebook.com/share/1FJYBezTW8/"
INSTAGRAM_URL = "https://www.instagram.com/bakesbyhoorain"

st.set_page_config(
    page_title="Bakes by Hoorain",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def wa_link(message: str) -> str:
    return WA_BASE + "?text=" + urllib.parse.quote(message)


def img_bytes(name: str):
    """Return a file-like object for an embedded image, or None."""
    b64 = IMAGES.get(name)
    if not b64:
        return None
    import base64

    return io.BytesIO(base64.b64decode(b64))


SHEET_ID = "1Tc8csdlZ655AU3dFLrj5TC1Fx4uG4rBZOecHV1fgB9w"


def fetch_sheet_rows(sheet_name):
    """Read a tab of the admin Google Sheet as rows (without header). Returns [] on failure."""
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
    """Turn a Google Drive share link into a direct thumbnail URL."""
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

BESTSELLERS = [
    ("elegant-black-gold.jpg", "Elegant Black & Gold", "2 lb — Rs 2,000"),
    ("bear-theme.jpg", "Bear Theme Cake", "2 lb — Rs 2,000"),
    ("lily-19th.jpg", "Lilly Flower Cake", "Rs 1,200"),
    ("two-tier-pearl.jpg", "2-Tier Pearl Cake", "3 lb — Rs 4,000"),
    ("calendar-september.jpg", "Calendar Theme Cake", "2 lb — Rs 2,000"),
    ("pink-birthday-topper.jpg", "Pink Birthday Cake", "2 lb — Rs 2,000"),
]

# Refresh bestseller price strings from the live sheet when names match
if "_sheet_menu" in dir() and _sheet_menu:
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

# ---------------- Style (premium dark bakery theme) ----------------
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,500&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    .hero { text-align: center; padding: 2.2rem 0 1rem 0;
            background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(232,160,180,.14), transparent);
            border-radius: 0 0 28px 28px; }
    .hero .logo-ring { display:inline-block; padding:6px; border-radius:50%;
            background: conic-gradient(from 180deg, #d4af37, #f6e2a8, #d4af37, #a87c1f, #d4af37);
            box-shadow: 0 10px 40px rgba(212,175,55,.35); margin-bottom: .9rem; }
    .hero .logo-ring img { border-radius:50%; display:block; }
    .hero h1 { font-family: 'Playfair Display', serif; font-weight:700;
            font-size: 2.9rem; margin: .2rem 0;
            background: linear-gradient(120deg, #f6e2a8, #e8a0b4 60%, #f6e2a8);
            -webkit-background-clip: text; background-clip: text; color: transparent; }
    .hero p.tag { color: #d9bfae; font-size: 1.02rem; font-weight:300; letter-spacing:.4px; margin-top:.4rem; }
    .hero p.tag b { color:#f6e2a8; font-weight:500; }
    .sec-head { font-family:'Playfair Display', serif; font-size:1.7rem; color:#f6e2a8;
            text-align:center; margin: 0 0 .2rem 0; }
    .sec-sub { text-align:center; color:#a98d7d; font-size:.92rem; margin-bottom:1.1rem; font-weight:300;}
    .orn { text-align:center; color:#d4af37; letter-spacing:12px; font-size:.8rem; margin:.4rem 0 1.2rem 0; }
    .price-tag { color: #f6e2a8; font-weight: 600; font-size: 1.08rem; }
    .card { background: linear-gradient(160deg, #2b1a12, #1f130d);
            border: 1px solid rgba(212,175,55,.28); border-radius: 18px;
            padding: 0.9rem; text-align: center; height: 100%;
            box-shadow: 0 12px 32px rgba(0,0,0,.45); transition: transform .25s ease; }
    .card:hover { transform: translateY(-4px); border-color: rgba(212,175,55,.6); }
    .card img { border-radius: 12px; }
    .card h4 { font-family:'Playfair Display',serif; color: #f6e2a8; margin: 0.6rem 0 0.15rem 0; font-size: 1.05rem; }
    .card p { color: #c9a98f; margin: 0 0 0.6rem 0; font-size: 0.9rem; }
    .wa-btn { display: inline-block; background: linear-gradient(135deg,#25D366,#1eb856);
              color: white !important; padding: 0.7rem 1.7rem; border-radius: 999px; font-weight: 600;
              text-decoration: none; margin: 0.35rem 0.15rem; font-size:1rem;
              box-shadow: 0 8px 24px rgba(37,211,102,.35); transition: transform .2s ease; }
    .wa-btn:hover { transform: scale(1.04); color: white !important; }
    .wa-btn.big { font-size:1.12rem; padding:.85rem 2.2rem; }
    .social-btn { display: inline-block; background: rgba(212,175,55,.12); color: #f6e2a8 !important;
              border:1px solid rgba(212,175,55,.45);
              padding: 0.55rem 1.25rem; border-radius: 999px; font-weight: 500;
              text-decoration: none; margin: 0.25rem; font-size: 0.92rem; transition: all .2s ease;}
    .social-btn:hover { background: rgba(212,175,55,.28); color:#fff !important; }
    .menu-row { background: rgba(255,255,255,.03); border:1px solid rgba(212,175,55,.14);
            border-radius:14px; padding:.55rem .9rem; margin-bottom:.5rem; }
    .howto { background: linear-gradient(160deg,#2b1a12,#1f130d); border:1px solid rgba(212,175,55,.28);
            border-radius:18px; padding:1.2rem 1.4rem; color:#e8d5c4; }
    .howto b { color:#f6e2a8; }
    .footer { text-align: center; color: #8a6f5f; font-size: 0.85rem; padding: 2rem 0 1rem 0; font-weight:300;}
    .stImage img { border-radius: 14px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Hero ----------------
logo = img_bytes("logo.jpg")
st.markdown('<div class="hero">', unsafe_allow_html=True)
if logo:
    import base64 as _b64

    _logo_b64 = _b64.b64encode(logo.getvalue()).decode()
    st.markdown(
        '<div class="logo-ring"><img src="data:image/jpeg;base64,' + _logo_b64 + '" width="150"></div>',
        unsafe_allow_html=True,
    )
st.markdown(
    "<h1>Bakes by Hoorain</h1>"
    '<p class="tag">Customized Cakes &mdash; <b>Homemade with Love</b><br>Made Just for Your Special Moments &middot; Karachi</p>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<a class="wa-btn big" href="{wa_link("Assalam-o-Alaikum! I want to order a cake from Bakes by Hoorain.")}" target="_blank">💬 Order on WhatsApp</a>',
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Cake slider ----------------
def _slider_html():
    import base64

    tags = []
    for fname, cap in GALLERY:
        b64 = IMAGES.get(fname)
        if not b64:
            continue
        safe_cap = cap.replace('"', "").replace("<", "").replace(">", "")
        tags.append(
            '<img src="data:image/jpeg;base64,' + b64 + '" alt="' + safe_cap + '" loading="lazy">'
        )
    doubled = "".join(tags) * 2
    return (
        "<style>"
        ".cslider{overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,#000 7%,#000 93%,transparent);"
        "mask-image:linear-gradient(90deg,transparent,#000 7%,#000 93%,transparent)}"
        ".ctrack{display:flex;gap:12px;width:max-content;animation:cslide 45s linear infinite;padding:4px 0}"
        ".ctrack img{height:150px;width:150px;object-fit:cover;border-radius:16px;border:1px solid rgba(212,175,55,.35);box-shadow:0 8px 22px rgba(0,0,0,.5)}"
        "@keyframes cslide{to{transform:translateX(-50%)}}"
        "</style>"
        '<div class="cslider"><div class="ctrack">' + doubled + "</div></div>"
    )


def _sec(title, sub=""):
    st.markdown(f'<div class="sec-head">{title}</div>', unsafe_allow_html=True)
    if sub:
        st.markdown(f'<div class="sec-sub">{sub}</div>', unsafe_allow_html=True)
    st.markdown('<div class="orn">✦ ✦ ✦</div>', unsafe_allow_html=True)


_sec("Our Cakes on Display", "Fresh from the oven — sliding showcase")
st.components.v1.html(_slider_html(), height=175, scrolling=False)

# ---------------- Bestsellers ----------------
_sec("Bestsellers", "Most loved cakes by our customers")
cols = st.columns(3)
for i, (fname, name, price) in enumerate(BESTSELLERS):
    p = img_bytes(fname)
    with cols[i % 3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if p:
            st.image(p, use_container_width=True)
        st.markdown(f"<h4>{name}</h4><p>{price}</p>", unsafe_allow_html=True)
        st.markdown(
            f'<a class="wa-btn" href="{wa_link(f"Assalam-o-Alaikum! I want to order: {name} ({price})")}" target="_blank">Order</a>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
st.divider()

# ---------------- Gallery ----------------
_sec("Gallery", "Tap any photo to view it bigger")
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
st.divider()

# ---------------- Menu ----------------
_sec("Price Menu", "Live from our kitchen — updated daily")
st.markdown('<div class="sec-head" style="font-size:1.25rem;">Cakes</div>', unsafe_allow_html=True)
for name, size, price in MENU_CAKES:
    c1, c2, c3 = st.columns([3, 2, 2])
    with c1:
        st.markdown(f'<div class="menu-row"><b style="color:#f7ece4;">{name}</b></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="menu-row"><span class="price-tag">Rs {price:,}</span> <span style="color:#a98d7d;font-size:.85rem;">· {size}</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(
            f'<a class="wa-btn" href="{wa_link(f"Assalam-o-Alaikum! I want to order: {name} ({size} - Rs {price:,})")}" target="_blank">Order</a>',
            unsafe_allow_html=True,
        )

st.markdown('<div class="sec-head" style="font-size:1.25rem;margin-top:.6rem;">Desserts</div>', unsafe_allow_html=True)
for name, size, price in MENU_DESSERTS:
    c1, c2, c3 = st.columns([3, 2, 2])
    with c1:
        st.markdown(f'<div class="menu-row"><b style="color:#f7ece4;">{name}</b></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="menu-row"><span class="price-tag">Rs {price:,}</span> <span style="color:#a98d7d;font-size:.85rem;">· {size}</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(
            f'<a class="wa-btn" href="{wa_link(f"Assalam-o-Alaikum! I want to order: {name} ({size} - Rs {price:,})")}" target="_blank">Order</a>',
            unsafe_allow_html=True,
        )

st.markdown(
    '<div class="howto" style="margin-top:.8rem;text-align:center;">🎨 Custom designs available on request — just message on WhatsApp!</div>',
    unsafe_allow_html=True,
)

# ---------------- How to order ----------------
_sec("How to Order", "Three easy steps")
st.markdown(
    '<div class="howto">'
    "1. <b>Pick</b> your cake from the menu or gallery above.<br>"
    "2. <b>Tap Order</b> — WhatsApp opens with your order message ready.<br>"
    "3. <b>Send</b> it to us on <b>0312 7904882</b> — we'll confirm your design & delivery. ✅"
    "</div>",
    unsafe_allow_html=True,
)
st.markdown(
    f'<div style="text-align:center;margin-top:.8rem;"><a class="wa-btn big" href="{wa_link("Assalam-o-Alaikum! I want to place an order.")}" target="_blank">💬 Chat on WhatsApp: 0312 7904882</a></div>',
    unsafe_allow_html=True,
)

# ---------------- About / Contact ----------------
_sec("About", "Our story")
st.markdown(
    '<div class="howto" style="text-align:center;">Bakes by Hoorain is a home-based bakery in Karachi, making customized cakes '
    "for birthdays, anniversaries, umrah celebrations and every special moment — "
    "homemade with love. 🌸</div>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div style="text-align:center;margin-top:.9rem;">'
    f'<a class="social-btn" href="{TIKTOK_URL}" target="_blank">🎵 TikTok</a>'
    f'<a class="social-btn" href="{INSTAGRAM_URL}" target="_blank">📸 Instagram</a>'
    f'<a class="social-btn" href="{FACEBOOK_URL}" target="_blank">📘 Facebook</a>'
    "</div>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="footer">Bakes by Hoorain · Karachi · WhatsApp 0312 7904882</div>',
    unsafe_allow_html=True,
)
