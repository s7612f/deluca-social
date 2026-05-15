#!/usr/bin/env python3
"""
De Luca — social SVG generator
Outputs to: /Volumes/Disk 2/projects/De_Luca/outbox/generated/
- 10 rebrand templates (5 feed + 5 story) with food photos embedded
- 4 menu announcement designs (A La Carte + Dessert × post + story)
"""
import os, base64, re, subprocess, glob
from PIL import Image
import io

# ── Paths ─────────────────────────────────────────────────────────────────
BASE          = "/Volumes/Disk 2/projects/De_Luca"
FEED_TMPL     = f"{BASE}/project/git/Rebrand 2026/feed_templates"
STORY_TMPL    = f"{BASE}/project/git/Rebrand 2026/story_templates"
PHOTOS_DIR    = f"{BASE}/footage/photos/zv1_stills_2026-03-19"
OUTPUT_DIR    = f"{BASE}/outbox/generated"
MENUS_DIR     = "/Users/sebastianfisher/Downloads"
TMP           = "/tmp/dlc_menu"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

# ── Image helpers ─────────────────────────────────────────────────────────
def cover_crop_b64(path, target_w, target_h, quality=85):
    """Centre-crop + resize to exact dimensions, return JPEG base64."""
    img = Image.open(path).convert("RGB")
    w, h = img.size
    scale = max(target_w / w, target_h / h)
    nw, nh = int(w * scale) + 1, int(h * scale) + 1
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - target_w) // 2
    top  = (nh - target_h) // 2
    img  = img.crop((left, top, left + target_w, top + target_h))
    buf  = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()

def pdf_first_page_b64(pdf_path, target_w, target_h, dpi=200):
    """Render first page of PDF, centre-crop to target size, return base64."""
    prefix = os.path.join(TMP, os.path.basename(pdf_path).replace(" ", "_"))
    subprocess.run(
        ["pdftoppm", "-r", str(dpi), "-f", "1", "-l", "1", "-png", pdf_path, prefix],
        check=True, capture_output=True
    )
    candidates = sorted(glob.glob(prefix + "*.png"))
    if not candidates:
        raise FileNotFoundError(f"pdftoppm produced no output for {pdf_path}")
    return cover_crop_b64(candidates[0], target_w, target_h, quality=92)

# ── SVG mutation helpers ──────────────────────────────────────────────────
def add_to_defs(svg, extra):
    return svg.replace("</defs>", extra + "\n  </defs>", 1)

def inject_after_bg(svg, block):
    """Insert block after the <!-- Background --> rect."""
    return re.sub(
        r'(<!-- Background -->\s*<rect[^/]*/>\n)',
        r'\1' + block + '\n',
        svg, count=1
    )

def hide_olive(svg):
    return re.sub(
        r'(<!-- Olive sprig[^\n]*\n\s*<g transform="[^"]*")(\s)',
        r'\1 style="display:none"\2',
        svg, count=1
    )

# ── Pick 10 food photos spread evenly across the 161 stills ──────────────
all_stills = sorted([
    f for f in os.listdir(PHOTOS_DIR)
    if f.upper().endswith(".JPG") and not f.startswith("._")
])
n = len(all_stills)
picks = [all_stills[int(i * n / 10)] for i in range(10)]
photo_paths = [os.path.join(PHOTOS_DIR, p) for p in picks]

print(f"Using {n} stills — selected: {', '.join(picks)}\n")

# ── Template definitions ──────────────────────────────────────────────────
# (variant, kind, bg_hex, accent_hex)
TEMPLATES = [
    ("avorio",     "feed",  "#F4EDE3", "#18170F"),
    ("nero",       "feed",  "#18170F", "#F4EDE3"),
    ("nero_gold",  "feed",  "#18170F", "#F4EDE3"),
    ("salvia",     "feed",  "#3D5C35", "#F4EDE3"),
    ("terracotta", "feed",  "#C4622D", "#F4EDE3"),
    ("avorio",     "story", "#F4EDE3", "#18170F"),
    ("nero",       "story", "#18170F", "#F4EDE3"),
    ("nero_gold",  "story", "#18170F", "#F4EDE3"),
    ("salvia",     "story", "#3D5C35", "#F4EDE3"),
    ("terracotta", "story", "#C4622D", "#F4EDE3"),
]

# ── Generate regular photo templates ──────────────────────────────────────
for idx, (variant, kind, bg, accent) in enumerate(TEMPLATES):
    photo = photo_paths[idx]
    tmpl_dir = FEED_TMPL if kind == "feed" else STORY_TMPL
    svg_file = f"{tmpl_dir}/dlc_{kind}_{variant}.svg"

    with open(svg_file) as f:
        svg = f.read()

    uid = f"{kind[0]}{idx}"  # unique prefix avoids ID collisions

    if kind == "feed":
        # Photo fills the content zone (full width, above wordmark separator at y=949)
        b64 = cover_crop_b64(photo, 1080, 949)

        defs_extra = f"""
    <clipPath id="pc{uid}">
      <rect x="0" y="0" width="1080" height="949"/>
    </clipPath>
    <linearGradient id="pf{uid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="{bg}" stop-opacity="0"/>
      <stop offset="62%"  stop-color="{bg}" stop-opacity="0"/>
      <stop offset="100%" stop-color="{bg}" stop-opacity="0.90"/>
    </linearGradient>"""

        injection = (
            f'  <!-- Photo -->\n'
            f'  <image x="0" y="0" width="1080" height="949"'
            f' href="data:image/jpeg;base64,{b64}"'
            f' clip-path="url(#pc{uid})" preserveAspectRatio="xMidYMid slice"/>\n'
            f'  <rect x="0" y="0" width="1080" height="949" fill="url(#pf{uid})"/>\n'
            f'  <rect x="0" y="0" width="1080" height="1080" fill="{bg}" opacity="0.10"/>'
        )

    else:  # story — photo fills middle zone y=200→1720
        b64 = cover_crop_b64(photo, 1080, 1520)

        defs_extra = f"""
    <clipPath id="pc{uid}">
      <rect x="0" y="200" width="1080" height="1520"/>
    </clipPath>
    <linearGradient id="ftop{uid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="{bg}" stop-opacity="0.72"/>
      <stop offset="14%"  stop-color="{bg}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="fbot{uid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="{bg}" stop-opacity="0"/>
      <stop offset="82%"  stop-color="{bg}" stop-opacity="0"/>
      <stop offset="100%" stop-color="{bg}" stop-opacity="0.88"/>
    </linearGradient>"""

        injection = (
            f'  <!-- Photo (story middle) -->\n'
            f'  <image x="0" y="200" width="1080" height="1520"'
            f' href="data:image/jpeg;base64,{b64}"'
            f' clip-path="url(#pc{uid})" preserveAspectRatio="xMidYMid slice"/>\n'
            f'  <rect x="0" y="200" width="1080" height="1520" fill="url(#ftop{uid})"/>\n'
            f'  <rect x="0" y="200" width="1080" height="1520" fill="url(#fbot{uid})"/>\n'
            f'  <rect x="0" y="0" width="1080" height="1920" fill="{bg}" opacity="0.08"/>'
        )
        svg = hide_olive(svg)

    svg = add_to_defs(svg, defs_extra)
    svg = inject_after_bg(svg, injection)

    out = os.path.join(OUTPUT_DIR, f"dlc_{kind}_{variant}_photo.svg")
    with open(out, "w") as f:
        f.write(svg)
    print(f"✓  {os.path.basename(out)}  ({picks[idx]})")

# ── Menu announcement SVGs ─────────────────────────────────────────────────
print("\nConverting menu PDFs…")

menus = {
    "alacarte": {
        "pdf":   os.path.join(MENUS_DIR, "DeLuca_ALaCarteMenu(May2026)3.pdf"),
        "title": "A LA CARTE",
        "sub":   "SPRING MENU — MAY 2026",
        "copy":  "From handmade pasta to wood-fired mains,\nevery dish made with love.",
        "bg":    "#18170F",
        "accent":"#F4EDE3",
        "gold":  "#C9A96E",
    },
    "dessert": {
        "pdf":   os.path.join(MENUS_DIR, "DeLuca_DessertMenu(March2026)2.pdf"),
        "title": "DOLCI",
        "sub":   "DESSERT MENU",
        "copy":  "A sweet finale,\nfatto a mano.",
        "bg":    "#F4EDE3",
        "accent":"#18170F",
        "gold":  "#C9A96E",
    },
}

def dots_defs(uid, dot_fill, dot_opacity):
    return f"""
    <pattern id="dots{uid}" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="20" cy="20" r="1.4" fill="{dot_fill}" opacity="{dot_opacity}"/>
    </pattern>"""

def corner_brackets_feed(colour):
    return f"""
  <polyline points="76,32 32,32 32,76"      fill="none" stroke="{colour}" stroke-width="1.2" stroke-linecap="square"/>
  <polyline points="1004,32 1048,32 1048,76" fill="none" stroke="{colour}" stroke-width="1.2" stroke-linecap="square"/>
  <polyline points="76,1048 32,1048 32,1004" fill="none" stroke="{colour}" stroke-width="1.2" stroke-linecap="square"/>
  <polyline points="1004,1048 1048,1048 1048,1004" fill="none" stroke="{colour}" stroke-width="1.2" stroke-linecap="square"/>"""

def corner_brackets_story(colour):
    return f"""
  <polyline points="80,36 36,36 36,80"       fill="none" stroke="{colour}" stroke-width="1.3" stroke-linecap="square"/>
  <polyline points="1000,36 1044,36 1044,80"  fill="none" stroke="{colour}" stroke-width="1.3" stroke-linecap="square"/>
  <polyline points="80,1884 36,1884 36,1840"  fill="none" stroke="{colour}" stroke-width="1.3" stroke-linecap="square"/>
  <polyline points="1000,1884 1044,1884 1044,1840" fill="none" stroke="{colour}" stroke-width="1.3" stroke-linecap="square"/>"""

# ──────────────────────────────────────────────
# Menu POST  1080 × 1080 — split layout
# Left 50 %: brand text panel
# Right 50%: menu page image (full bleed, clipped)
# ──────────────────────────────────────────────
def make_menu_post(key, m):
    bg, acc, gold = m["bg"], m["accent"], m["gold"]
    title, sub, copy = m["title"], m["sub"], m["copy"]
    dot_fill = acc; dot_op = "0.07"

    img_b64 = pdf_first_page_b64(m["pdf"], 540, 950)

    copy_lines = copy.split("\n")
    copy_y1, copy_y2 = 620, 660
    copy_elems = "\n".join(
        f'  <text x="80" y="{copy_y1 + i*40}" font-family="Cormorant Garamond,Georgia,serif"'
        f' font-size="28" fill="{acc}" font-style="italic" opacity="0.78">{line}</text>'
        for i, line in enumerate(copy_lines)
    )

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="dots" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="20" cy="20" r="1.4" fill="{dot_fill}" opacity="{dot_op}"/>
    </pattern>
    <clipPath id="img-clip">
      <rect x="540" y="0" width="540" height="1080"/>
    </clipPath>
    <linearGradient id="img-fade" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0%"   stop-color="{bg}" stop-opacity="0"/>
      <stop offset="65%"  stop-color="{bg}" stop-opacity="0"/>
      <stop offset="100%" stop-color="{bg}" stop-opacity="0.95"/>
    </linearGradient>
    <linearGradient id="bottom-fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="{bg}" stop-opacity="0"/>
      <stop offset="80%"  stop-color="{bg}" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="{bg}" stop-opacity="0.88"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="1080" height="1080" fill="{bg}"/>
  <rect width="1080" height="1080" fill="url(#dots)"/>

  <!-- Menu page image — right half -->
  <image x="540" y="0" width="540" height="1080"
         href="data:image/jpeg;base64,{img_b64}"
         clip-path="url(#img-clip)" preserveAspectRatio="xMidYMid slice"/>
  <!-- Left-edge fade so image bleeds softly into text panel -->
  <rect x="540" y="0" width="540" height="1080" fill="url(#img-fade)"/>
  <!-- Bottom fade for wordmark legibility -->
  <rect x="540" y="0" width="540" height="1080" fill="url(#bottom-fade)"/>

  <!-- Dividing hairline -->
  <line x1="540" y1="60" x2="540" y2="1020" stroke="{acc}" stroke-width="0.5" opacity="0.4"/>

  <!-- Inset border -->
  <rect x="24" y="24" width="1032" height="1032" fill="none" stroke="{acc}" stroke-width="0.45"/>
  {corner_brackets_feed(acc)}

  <!-- Gold accent bars -->
  <rect x="0"    y="0"    width="1080" height="5" fill="{gold}"/>
  <rect x="0"    y="1075" width="1080" height="5" fill="{gold}"/>

  <!-- Left panel — text -->
  <!-- MENU label -->
  <text x="80" y="180"
        font-family="DM Sans,Arial,sans-serif" font-size="9"
        fill="{gold}" font-weight="500" letter-spacing="4">{sub}</text>
  <line x1="80" y1="196" x2="300" y2="196" stroke="{gold}" stroke-width="0.8" opacity="0.6"/>

  <!-- Main title -->
  <text x="80" y="340"
        font-family="Cormorant Garamond,Georgia,serif" font-size="86"
        fill="{acc}" font-weight="600" letter-spacing="6">{title}</text>
  <line x1="80" y1="370" x2="460" y2="370" stroke="{acc}" stroke-width="0.5" opacity="0.3"/>

  <!-- Copy -->
  {copy_elems}

  <!-- Bottom wordmark panel -->
  <line  x1="60"  y1="949" x2="520"  y2="949" stroke="{acc}" stroke-width="0.5"/>
  <rect  x="0"    y="950"  width="540" height="130" fill="{acc}" opacity="0.06"/>
  <text  x="270"  y="1002" text-anchor="middle"
         font-family="Cormorant Garamond,Georgia,serif" font-size="34"
         fill="{acc}" font-weight="600" letter-spacing="10">DE LUCA</text>
  <line  x1="120" y1="1012" x2="420" y2="1012" stroke="{acc}" stroke-width="0.5"/>
  <text  x="270"  y="1032" text-anchor="middle"
         font-family="DM Sans,Arial,sans-serif" font-size="8.5"
         fill="{acc}" font-weight="400" letter-spacing="3.5">ITALIAN RESTAURANT</text>

</svg>"""
    return svg

# ──────────────────────────────────────────────
# Menu STORY  1080 × 1920
# Header zone: wordmark
# Image: full width, y=180→1360 (1180px tall)
# Bottom zone: menu title + CTA
# ──────────────────────────────────────────────
def make_menu_story(key, m):
    bg, acc, gold = m["bg"], m["accent"], m["gold"]
    title, sub = m["title"], m["sub"]
    dot_fill = acc; dot_op = "0.07"

    img_b64 = pdf_first_page_b64(m["pdf"], 1080, 1180)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1920" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="dots" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="20" cy="20" r="1.4" fill="{dot_fill}" opacity="{dot_op}"/>
    </pattern>
    <clipPath id="img-clip">
      <rect x="0" y="180" width="1080" height="1180"/>
    </clipPath>
    <linearGradient id="img-fade-top" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="{bg}" stop-opacity="0.80"/>
      <stop offset="16%"  stop-color="{bg}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="img-fade-bot" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="{bg}" stop-opacity="0"/>
      <stop offset="72%"  stop-color="{bg}" stop-opacity="0"/>
      <stop offset="100%" stop-color="{bg}" stop-opacity="0.96"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="1080" height="1920" fill="{bg}"/>
  <rect width="1080" height="1920" fill="url(#dots)"/>

  <!-- Menu page image — full width, middle zone -->
  <image x="0" y="180" width="1080" height="1180"
         href="data:image/jpeg;base64,{img_b64}"
         clip-path="url(#img-clip)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="180" width="1080" height="1180" fill="url(#img-fade-top)"/>
  <rect x="0" y="180" width="1080" height="1180" fill="url(#img-fade-bot)"/>

  <!-- Inset border -->
  <rect x="26" y="26" width="1028" height="1868" fill="none" stroke="{acc}" stroke-width="0.45"/>
  {corner_brackets_story(acc)}

  <!-- Gold accent bars -->
  <rect x="0"    y="0"    width="1080" height="5" fill="{gold}"/>
  <rect x="0"    y="1915" width="1080" height="5" fill="{gold}"/>

  <!-- Top header zone -->
  <rect x="0" y="0" width="1080" height="180" fill="{bg}" opacity="0.05"/>
  <line x1="60" y1="178" x2="1020" y2="178" stroke="{acc}" stroke-width="0.5"/>
  <text x="540" y="80" text-anchor="middle"
        font-family="Cormorant Garamond,Georgia,serif" font-size="40"
        fill="{acc}" font-weight="600" letter-spacing="12">DE LUCA</text>
  <line x1="340" y1="93" x2="740" y2="93" stroke="{acc}" stroke-width="0.5"/>
  <text x="540" y="116" text-anchor="middle"
        font-family="DM Sans,Arial,sans-serif" font-size="9"
        fill="{acc}" font-weight="400" letter-spacing="3.5">ITALIAN RESTAURANT</text>

  <!-- Bottom menu info zone -->
  <line x1="60"  y1="1360" x2="1020" y2="1360" stroke="{acc}" stroke-width="0.5" opacity="0.5"/>

  <!-- Gold label -->
  <text x="540" y="1460" text-anchor="middle"
        font-family="DM Sans,Arial,sans-serif" font-size="9"
        fill="{gold}" font-weight="500" letter-spacing="4.5">{sub}</text>
  <line x1="340" y1="1475" x2="740" y2="1475" stroke="{gold}" stroke-width="0.7" opacity="0.5"/>

  <!-- Menu title -->
  <text x="540" y="1600" text-anchor="middle"
        font-family="Cormorant Garamond,Georgia,serif" font-size="110"
        fill="{acc}" font-weight="600" letter-spacing="8">{title}</text>

  <!-- CTA -->
  <line x1="340" y1="1700" x2="740" y2="1700" stroke="{acc}" stroke-width="0.5" opacity="0.35"/>
  <text x="540" y="1776" text-anchor="middle"
        font-family="DM Sans,Arial,sans-serif" font-size="11"
        fill="{acc}" font-weight="500" letter-spacing="3">PRENOTA UN TAVOLO</text>
  <text x="540" y="1806" text-anchor="middle"
        font-family="DM Sans,Arial,sans-serif" font-size="9"
        fill="{acc}" opacity="0.6" letter-spacing="2">BOOK YOUR TABLE</text>

  <!-- Olive sprig (bottom zone decoration) -->
  <g transform="translate(492,1638) scale(0.5)" opacity="0.22">
    <path d="M60 88 C58 70,52 54,42 38 C36 28,30 18,32 8" fill="none" stroke="{acc}" stroke-width="2" stroke-linecap="round"/>
    <path d="M54 62 C62 56,74 54,80 46" fill="none" stroke="{acc}" stroke-width="1.4" stroke-linecap="round"/>
    <ellipse cx="82" cy="43" rx="8" ry="5" transform="rotate(-35 82 43)" fill="none" stroke="{acc}" stroke-width="1.4"/>
    <path d="M48 55 C40 50,30 50,24 43" fill="none" stroke="{acc}" stroke-width="1.4" stroke-linecap="round"/>
    <ellipse cx="22" cy="40" rx="8" ry="5" transform="rotate(35 22 40)" fill="none" stroke="{acc}" stroke-width="1.4"/>
  </g>

</svg>"""
    return svg


for key, m in menus.items():
    print(f"  PDF → {key}…")

    post_svg  = make_menu_post(key, m)
    story_svg = make_menu_story(key, m)

    post_out  = os.path.join(OUTPUT_DIR, f"dlc_menu_{key}_post.svg")
    story_out = os.path.join(OUTPUT_DIR, f"dlc_menu_{key}_story.svg")

    with open(post_out,  "w") as f: f.write(post_svg)
    with open(story_out, "w") as f: f.write(story_svg)
    print(f"  ✓  dlc_menu_{key}_post.svg")
    print(f"  ✓  dlc_menu_{key}_story.svg")

print(f"\nDone — {len(os.listdir(OUTPUT_DIR))} files in {OUTPUT_DIR}")
