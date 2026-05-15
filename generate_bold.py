#!/usr/bin/env python3
"""
De Luca — Bold social SVG generator
Output: outbox/generated_bold/

20 files:
  1–10  Site showcase templates (pt1–pt10) with real photos injected
 11–20  Original bold / editorial designs using actual menu content (no prices)
"""
import os, base64, subprocess, glob, io
from PIL import Image

BASE        = "/Volumes/Disk 2/projects/De_Luca"
PHOTOS_DIR  = f"{BASE}/footage/photos/zv1_stills_2026-03-19"
EDITED_DIR  = f"{BASE}/footage/photos/edited"
OUTPUT_DIR  = f"{BASE}/outbox/generated_bold"
TMP         = "/tmp/dlc_bold"
MENUS_DIR   = "/Users/sebastianfisher/Downloads"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

# ── Image helpers ─────────────────────────────────────────────────────────
def crop_b64(path, tw, th, quality=88):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    scale = max(tw / w, th / h)
    nw, nh = int(w * scale) + 1, int(h * scale) + 1
    img = img.resize((nw, nh), Image.LANCZOS)
    l, t = (nw - tw) // 2, (nh - th) // 2
    img = img.crop((l, t, l + tw, t + th))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()

def pdf_page_b64(pdf, tw, th, dpi=200):
    prefix = os.path.join(TMP, os.path.basename(pdf).replace(" ", "_"))
    subprocess.run(["pdftoppm", "-r", str(dpi), "-f", "1", "-l", "1",
                    "-png", pdf, prefix], check=True, capture_output=True)
    hits = sorted(glob.glob(prefix + "*.png"))
    if not hits:
        raise FileNotFoundError(pdf)
    return crop_b64(hits[0], tw, th, 92)

def img_el(b64, x, y, w, h, clip_id=None):
    clip = f' clip-path="url(#{clip_id})"' if clip_id else ""
    return (f'<image x="{x}" y="{y}" width="{w}" height="{h}"'
            f' href="data:image/jpeg;base64,{b64}"'
            f' preserveAspectRatio="xMidYMid slice"{clip}/>')

def clip_rect(cid, x, y, w, h):
    return f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>'

def write(name, content):
    path = os.path.join(OUTPUT_DIR, name)
    with open(path, "w") as f:
        f.write(content)
    print(f"  ✓  {name}")

# ── Photo pool ────────────────────────────────────────────────────────────
stills = sorted([f for f in os.listdir(PHOTOS_DIR)
                 if f.upper().endswith(".JPG") and not f.startswith("._")])
n = len(stills)
# Use a different spread from the first batch (which used 0,16,32,48,64,80,96,112,128,144)
idxs = [8, 24, 40, 56, 72, 88, 104, 120, 136, 155]
ph = [os.path.join(PHOTOS_DIR, stills[i]) for i in idxs]

TERRACE  = os.path.join(EDITED_DIR, "terrace_evening.jpg")
TERRACE2 = os.path.join(EDITED_DIR, "terrace_evening2.jpg")

print("Encoding photos for showcase templates…")
# Pre-encode at target sizes
p = {
    "food_960x600": crop_b64(ph[0], 960, 600),
    "terrace_920x560": crop_b64(TERRACE, 920, 560),
    "eve_920x580": crop_b64(ph[1], 920, 580),
    "terrace_540x1080": crop_b64(TERRACE2, 540, 1080),
    "food_1080x700": crop_b64(ph[2], 1080, 700),
    "kitchen_920x580": crop_b64(ph[3], 920, 580),
    "piano_920x580": crop_b64(ph[4], 920, 580),
    # Bold menu designs
    "burrata_1080x680": crop_b64(ph[5], 1080, 680),
    "tagliatelle_1080x1080": crop_b64(ph[6], 1080, 1080),
    "linguine_1080x620": crop_b64(ph[7], 1080, 620),
    "shortrib_1080x600": crop_b64(ph[8], 1080, 600),
    "tiramisu_1080x680": crop_b64(ph[9], 1080, 680),
    # Stories
    "burrata_story_1080x1180": crop_b64(ph[5], 1080, 1180),
    "food_story_1080x1180": crop_b64(ph[6], 1080, 1180),
}
print("  Done.\n")

# ══════════════════════════════════════════════════════════════════════════
# PART 1 — SITE SHOWCASE TEMPLATES (pt1–pt10) WITH PHOTOS
# ══════════════════════════════════════════════════════════════════════════
print("Building showcase templates…")

# ── pt1: Fatto a mano — crimson, bold italic, food photo top ──────────────
write("dlc_bold_fatto_a_mano.svg", f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="dots" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="20" cy="20" r="1.2" fill="#F4EDE3" opacity="0.08"/>
    </pattern>
    {clip_rect("pc", 60, 60, 960, 600)}
    <linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="60%" stop-color="#6E0B1C" stop-opacity="0"/>
      <stop offset="100%" stop-color="#6E0B1C" stop-opacity="0.85"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="#6E0B1C"/>
  <rect width="1080" height="1080" fill="url(#dots)"/>
  <rect x="24" y="24" width="1032" height="1032" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="0.6"/>
  {img_el(p['food_960x600'], 60, 60, 960, 600, "pc")}
  <rect x="60" y="60" width="960" height="600" fill="url(#fg)"/>
  <text x="80" y="830" font-family="Cormorant Garamond,Georgia,serif" font-size="130" fill="#fff" font-weight="700" font-style="italic" letter-spacing="-3">Fatto</text>
  <text x="80" y="960" font-family="Cormorant Garamond,Georgia,serif" font-size="130" fill="#fff" font-weight="700" font-style="italic" letter-spacing="-3">a mano.</text>
  <rect x="0" y="1010" width="1080" height="70" fill="rgba(0,0,0,0.3)"/>
  <text x="80" y="1053" font-family="DM Sans,Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.85)" font-weight="500" letter-spacing="4">DE LUCA</text>
  <text x="1000" y="1053" text-anchor="end" font-family="DM Sans,Arial,sans-serif" font-size="11" fill="rgba(255,255,255,0.45)" letter-spacing="2">CAMBRIDGE</text>
</svg>""")

# ── pt2: Al fresco — ivory, crimson border, terrace photo ─────────────────
write("dlc_bold_al_fresco.svg", f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {clip_rect("pc", 80, 80, 920, 560)}
    <linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="55%" stop-color="#FAF9F7" stop-opacity="0"/>
      <stop offset="100%" stop-color="#FAF9F7" stop-opacity="0.92"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="#FAF9F7"/>
  <rect x="40" y="40" width="1000" height="1000" fill="none" stroke="#6E0B1C" stroke-width="2"/>
  {img_el(p['terrace_920x560'], 80, 80, 920, 560, "pc")}
  <rect x="80" y="80" width="920" height="560" fill="url(#fg)"/>
  <text x="80" y="748" font-family="Cormorant Garamond,Georgia,serif" font-size="104" fill="#6E0B1C" font-weight="700" font-style="italic" letter-spacing="-2">Al fresco.</text>
  <line x1="80" y1="778" x2="500" y2="778" stroke="#6E0B1C" stroke-width="2.5"/>
  <text x="80" y="838" font-family="DM Sans,Arial,sans-serif" font-size="15" fill="#888" letter-spacing="5">THE TERRACE IS OPEN</text>
  <text x="80" y="980" font-family="Cormorant Garamond,Georgia,serif" font-size="22" fill="#6E0B1C" font-style="italic">De Luca · Cambridge</text>
</svg>""")

# ── pt3: Stasera — charcoal, crimson bars, evening atmosphere ─────────────
write("dlc_bold_stasera.svg", f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {clip_rect("pc", 80, 80, 920, 580)}
    <linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="50%" stop-color="#1A1A1A" stop-opacity="0"/>
      <stop offset="100%" stop-color="#1A1A1A" stop-opacity="0.82"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="#1A1A1A"/>
  <rect x="0" y="0" width="1080" height="5" fill="#6E0B1C"/>
  <rect x="0" y="1075" width="1080" height="5" fill="#6E0B1C"/>
  {img_el(p['eve_920x580'], 80, 80, 920, 580, "pc")}
  <rect x="80" y="80" width="920" height="580" fill="url(#fg)"/>
  <text x="80" y="790" font-family="Cormorant Garamond,Georgia,serif" font-size="110" fill="#FAF9F7" font-weight="700" font-style="italic" letter-spacing="-2">Stasera.</text>
  <line x1="80" y1="818" x2="440" y2="818" stroke="#6E0B1C" stroke-width="3"/>
  <text x="80" y="872" font-family="DM Sans,Arial,sans-serif" font-size="14" fill="#555" letter-spacing="4">OPEN FROM 18:00</text>
  <text x="80" y="938" font-family="DM Sans,Arial,sans-serif" font-size="12" fill="#6E0B1C" letter-spacing="2">BOOK YOUR TABLE ↗</text>
  <text x="1000" y="1050" text-anchor="end" font-family="DM Sans,Arial,sans-serif" font-size="12" fill="#333" letter-spacing="3">DE LUCA</text>
</svg>""")

# ── pt4: The terrace awaits — split crimson/photo ─────────────────────────
write("dlc_bold_terrace_split.svg", f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {clip_rect("pc", 540, 0, 540, 1080)}
    <linearGradient id="lg" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0%" stop-color="#6E0B1C" stop-opacity="0"/>
      <stop offset="65%" stop-color="#6E0B1C" stop-opacity="0"/>
      <stop offset="100%" stop-color="#6E0B1C" stop-opacity="0.9"/>
    </linearGradient>
  </defs>
  <rect width="540" height="1080" fill="#6E0B1C"/>
  {img_el(p['terrace_540x1080'], 540, 0, 540, 1080, "pc")}
  <rect x="540" y="0" width="540" height="1080" fill="url(#lg)"/>
  <text x="60" y="418" font-family="Cormorant Garamond,Georgia,serif" font-size="96" fill="#fff" font-weight="700" font-style="italic" letter-spacing="-2">The</text>
  <text x="60" y="528" font-family="Cormorant Garamond,Georgia,serif" font-size="96" fill="#fff" font-weight="700" font-style="italic" letter-spacing="-2">terrace</text>
  <text x="60" y="638" font-family="Cormorant Garamond,Georgia,serif" font-size="96" fill="#fff" font-weight="700" font-style="italic" letter-spacing="-2">awaits.</text>
  <line x1="60" y1="678" x2="340" y2="678" stroke="rgba(255,255,255,0.4)" stroke-width="1.5"/>
  <text x="60" y="718" font-family="DM Sans,Arial,sans-serif" font-size="12" fill="rgba(255,255,255,0.5)" letter-spacing="3">DE LUCA · CAMBRIDGE</text>
</svg>""")

# ── pt5: Il nuovo menù — food photo top, crimson panel with bold type ──────
write("dlc_bold_il_nuovo_menu.svg", f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {clip_rect("pc", 0, 0, 1080, 700)}
    <linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="55%" stop-color="#6E0B1C" stop-opacity="0"/>
      <stop offset="100%" stop-color="#6E0B1C" stop-opacity="0.95"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="#6E0B1C"/>
  {img_el(p['food_1080x700'], 0, 0, 1080, 700, "pc")}
  <rect x="0" y="0" width="1080" height="700" fill="url(#fg)"/>
  <rect x="0" y="700" width="1080" height="380" fill="#6E0B1C"/>
  <text x="60" y="840" font-family="Cormorant Garamond,Georgia,serif" font-size="100" fill="#fff" font-weight="700" font-style="italic" letter-spacing="-2">Il nuovo</text>
  <text x="60" y="942" font-family="Cormorant Garamond,Georgia,serif" font-size="100" fill="#fff" font-weight="700" font-style="italic" letter-spacing="-2">menù.</text>
  <text x="60" y="998" font-family="DM Sans,Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.5)" letter-spacing="4">THE SEASON CHANGED. SO DID WE.</text>
  <text x="1020" y="1055" text-anchor="end" font-family="DM Sans,Arial,sans-serif" font-size="11" fill="rgba(255,255,255,0.35)" letter-spacing="2">DE LUCA</text>
</svg>""")

# ── pt6: Questa settimana — text-only menu board with real dishes ──────────
write("dlc_bold_questa_settimana.svg", """<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <rect width="1080" height="1080" fill="#FAF9F7"/>
  <rect x="0" y="0" width="1080" height="100" fill="#6E0B1C"/>
  <text x="60" y="62" font-family="DM Sans,Arial,sans-serif" font-size="13" fill="#fff" font-weight="500" letter-spacing="4">DE LUCA</text>
  <text x="1020" y="62" text-anchor="end" font-family="DM Sans,Arial,sans-serif" font-size="11" fill="rgba(255,255,255,0.6)" letter-spacing="3">A LA CARTE</text>
  <text x="60" y="250" font-family="Cormorant Garamond,Georgia,serif" font-size="76" fill="#1A1A1A" font-weight="700" font-style="italic">Burrata.</text>
  <text x="60" y="292" font-family="DM Sans,Arial,sans-serif" font-size="14" fill="#888" letter-spacing="0.5">Basil pesto, sun-dried tomato, roasted almonds</text>
  <line x1="60" y1="320" x2="1020" y2="320" stroke="#E5E2DD" stroke-width="1"/>
  <text x="60" y="454" font-family="Cormorant Garamond,Georgia,serif" font-size="76" fill="#1A1A1A" font-weight="700" font-style="italic">Linguine.</text>
  <text x="60" y="496" font-family="DM Sans,Arial,sans-serif" font-size="14" fill="#888" letter-spacing="0.5">Frutti di mare, white wine, chilli, garlic</text>
  <line x1="60" y1="524" x2="1020" y2="524" stroke="#E5E2DD" stroke-width="1"/>
  <text x="60" y="658" font-family="Cormorant Garamond,Georgia,serif" font-size="76" fill="#1A1A1A" font-weight="700" font-style="italic">Tiramisù.</text>
  <text x="60" y="700" font-family="DM Sans,Arial,sans-serif" font-size="14" fill="#888" letter-spacing="0.5">Made in-house. No shortcuts.</text>
  <rect x="0" y="900" width="1080" height="180" fill="#6E0B1C"/>
  <text x="60" y="1002" font-family="Cormorant Garamond,Georgia,serif" font-size="52" fill="#fff" font-weight="700" font-style="italic">On the menu now.</text>
</svg>""")

# ── pt7: Vent'anni — 20 years typographic, gold on dark ───────────────────
write("dlc_bold_ventanni.svg", """<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <rect width="1080" height="1080" fill="#1A1A1A"/>
  <rect x="0" y="0" width="1080" height="5" fill="#C9A96E"/>
  <rect x="0" y="1075" width="1080" height="5" fill="#C9A96E"/>
  <text x="-40" y="860" font-family="Cormorant Garamond,Georgia,serif" font-size="820" fill="#fff" font-weight="700" font-style="italic" opacity="0.03">20</text>
  <text x="80" y="60" font-family="DM Sans,Arial,sans-serif" font-size="11" fill="#C9A96E" letter-spacing="6">CAMBRIDGE · 2006–2026</text>
  <text x="80" y="450" font-family="Cormorant Garamond,Georgia,serif" font-size="230" fill="#FAF9F7" font-weight="700" font-style="italic" letter-spacing="-8">Vent'</text>
  <text x="80" y="668" font-family="Cormorant Garamond,Georgia,serif" font-size="230" fill="#C9A96E" font-weight="700" font-style="italic" letter-spacing="-8">anni.</text>
  <line x1="80" y1="720" x2="580" y2="720" stroke="#C9A96E" stroke-width="1.5"/>
  <text x="80" y="776" font-family="DM Sans,Arial,sans-serif" font-size="15" fill="#444" letter-spacing="5">TWENTY YEARS OF DE LUCA</text>
  <text x="80" y="940" font-family="DM Sans,Arial,sans-serif" font-size="13" fill="#C9A96E" letter-spacing="4">DE LUCA</text>
</svg>""")

# ── pt8: Grazie — crimson, massive white type, 20 years ───────────────────
write("dlc_bold_grazie.svg", """<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <rect width="1080" height="1080" fill="#6E0B1C"/>
  <text x="-40" y="860" font-family="Cormorant Garamond,Georgia,serif" font-size="820" fill="#000" font-weight="700" font-style="italic" opacity="0.06">20</text>
  <text x="80" y="56" font-family="DM Sans,Arial,sans-serif" font-size="11" fill="rgba(255,255,255,0.45)" letter-spacing="5">CAMBRIDGE · 2006–2026</text>
  <text x="80" y="430" font-family="Cormorant Garamond,Georgia,serif" font-size="250" fill="#fff" font-weight="700" font-style="italic" letter-spacing="-8">Gra-</text>
  <text x="80" y="678" font-family="Cormorant Garamond,Georgia,serif" font-size="250" fill="#fff" font-weight="700" font-style="italic" letter-spacing="-8">zie.</text>
  <line x1="80" y1="730" x2="460" y2="730" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
  <text x="80" y="790" font-family="DM Sans,Arial,sans-serif" font-size="15" fill="rgba(255,255,255,0.4)" letter-spacing="5">TWENTY YEARS · DE LUCA</text>
</svg>""")

# ── pt9: Le stesse mani — heritage craft, kitchen photo ───────────────────
write("dlc_bold_le_stesse_mani.svg", f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="dots" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="20" cy="20" r="1.2" fill="#6E0B1C" opacity="0.1"/>
    </pattern>
    {clip_rect("pc", 80, 80, 920, 580)}
    <linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="50%" stop-color="#FAF9F7" stop-opacity="0"/>
      <stop offset="100%" stop-color="#FAF9F7" stop-opacity="0.88"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="#FAF9F7"/>
  <rect width="1080" height="1080" fill="url(#dots)"/>
  {img_el(p['kitchen_920x580'], 80, 80, 920, 580, "pc")}
  <rect x="80" y="80" width="920" height="580" fill="url(#fg)"/>
  <text x="80" y="790" font-family="DM Sans,Arial,sans-serif" font-size="11" fill="#C9A96E" letter-spacing="6">VENT'ANNI DI MESTIERE</text>
  <text x="80" y="900" font-family="Cormorant Garamond,Georgia,serif" font-size="92" fill="#6E0B1C" font-weight="700" font-style="italic" letter-spacing="-2">Le stesse</text>
  <text x="80" y="992" font-family="Cormorant Garamond,Georgia,serif" font-size="92" fill="#1A1A1A" font-weight="700" font-style="italic" letter-spacing="-2">mani.</text>
  <line x1="80" y1="1020" x2="500" y2="1020" stroke="#C9A96E" stroke-width="1.5"/>
  <text x="80" y="1058" font-family="DM Sans,Arial,sans-serif" font-size="11" fill="#999" letter-spacing="3">DE LUCA · CAMBRIDGE</text>
</svg>""")

# ── pt10: Piano Bar — dark, atmospheric photo, two-colour type ────────────
write("dlc_bold_piano_bar.svg", f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {clip_rect("pc", 80, 80, 920, 580)}
    <linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="50%" stop-color="#1A1A1A" stop-opacity="0"/>
      <stop offset="100%" stop-color="#1A1A1A" stop-opacity="0.85"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="#1A1A1A"/>
  {img_el(p['piano_920x580'], 80, 80, 920, 580, "pc")}
  <rect x="80" y="80" width="920" height="580" fill="url(#fg)"/>
  <text x="80" y="788" font-family="Cormorant Garamond,Georgia,serif" font-size="120" fill="#FAF9F7" font-weight="700" font-style="italic" letter-spacing="-3">Piano</text>
  <text x="80" y="900" font-family="Cormorant Garamond,Georgia,serif" font-size="120" fill="#6E0B1C" font-weight="700" font-style="italic" letter-spacing="-3">Bar.</text>
  <text x="80" y="960" font-family="DM Sans,Arial,sans-serif" font-size="14" fill="#444" letter-spacing="4">EVERY FRIDAY &amp; SATURDAY</text>
  <text x="80" y="1004" font-family="DM Sans,Arial,sans-serif" font-size="12" fill="#6E0B1C" letter-spacing="2">FROM 20:00 ↗</text>
  <text x="1000" y="1055" text-anchor="end" font-family="DM Sans,Arial,sans-serif" font-size="12" fill="#333" letter-spacing="3">DE LUCA</text>
</svg>""")

print("  Showcase templates done.\n")

# ══════════════════════════════════════════════════════════════════════════
# PART 2 — ORIGINAL BOLD MENU DESIGNS (no prices)
# ══════════════════════════════════════════════════════════════════════════
print("Building original bold designs…")

# Shared brand elements (inlined from git elements SVGs)
ARCH = """<g transform="translate({x},{y}) scale({s})" opacity="{op}" color="{c}">
  <path d="M20 280 L20 120 Q20 20 100 20 Q180 20 180 120 L180 280" fill="none" stroke="{c}" stroke-width="1.2" stroke-linecap="square"/>
  <path d="M32 280 L32 122 Q32 34 100 34 Q168 34 168 122 L168 280" fill="none" stroke="{c}" stroke-width="0.4"/>
</g>"""

def arch(x, y, scale, colour, opacity=1.0):
    return ARCH.format(x=x, y=y, s=scale, op=opacity, c=colour)

def diamond_rule(x, y, width, colour, opacity=1.0):
    cx = x + width / 2
    scale = width / 600
    return f"""<g transform="translate({x},{y}) scale({scale},1)" opacity="{opacity}">
  <line x1="0" y1="12" x2="276" y2="12" stroke="{colour}" stroke-width="0.7"/>
  <polygon points="300,6 309,12 300,18 291,12" fill="{colour}"/>
  <line x1="324" y1="12" x2="600" y2="12" stroke="{colour}" stroke-width="0.7"/>
</g>"""

def monogram(cx, cy, size, colour, opacity=1.0):
    r = size * 0.44
    r2 = size * 0.39
    fs = size * 0.26
    return f"""<g opacity="{opacity}">
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{colour}" stroke-width="1"/>
  <circle cx="{cx}" cy="{cy}" r="{r2}" fill="none" stroke="{colour}" stroke-width="0.4"/>
  <text x="{cx}" y="{cy + fs*0.35:.0f}" text-anchor="middle"
        font-family="Cormorant Garamond,Georgia,serif" font-size="{fs:.0f}"
        fill="{colour}" font-style="italic" letter-spacing="4">DL</text>
</g>"""

def wordmark_h(cx, y, colour, size=34, sub_size=8):
    hw = size * 5
    return f"""<text x="{cx}" y="{y}" text-anchor="middle"
      font-family="Cormorant Garamond,Georgia,serif" font-size="{size}" fill="{colour}"
      font-weight="600" letter-spacing="10">DE LUCA</text>
    <line x1="{cx-hw:.0f}" y1="{y+10}" x2="{cx+hw:.0f}" y2="{y+10}" stroke="{colour}" stroke-width="0.5"/>
    <text x="{cx}" y="{y+28}" text-anchor="middle"
      font-family="DM Sans,Arial,sans-serif" font-size="{sub_size}" fill="{colour}"
      font-weight="400" letter-spacing="3.5">ITALIAN RESTAURANT</text>"""

# ── 11: Burrata hero — ivory, arch frame, photo, bold type ───────────────
write("dlc_bold_burrata_post.svg", f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {clip_rect("pc", 0, 0, 1080, 680)}
    <linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="45%" stop-color="#F4EDE3" stop-opacity="0"/>
      <stop offset="100%" stop-color="#F4EDE3" stop-opacity="0.96"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="#F4EDE3"/>
  {img_el(p['burrata_1080x680'], 0, 0, 1080, 680, "pc")}
  <rect x="0" y="0" width="1080" height="680" fill="url(#fg)"/>
  <!-- Arch decoration (right, decorative) -->
  {arch(780, 30, 1.5, "#18170F", 0.07)}
  <!-- Content zone -->
  <text x="80" y="730" font-family="DM Sans,Arial,sans-serif" font-size="10" fill="#C9A96E" letter-spacing="5">ANTIPASTI</text>
  {diamond_rule(80, 748, 440, "#18170F", 0.2)}
  <text x="80" y="840" font-family="Cormorant Garamond,Georgia,serif" font-size="140" fill="#18170F" font-weight="700" font-style="italic" letter-spacing="-4">Burrata.</text>
  <text x="82" y="886" font-family="DM Sans,Arial,sans-serif" font-size="14" fill="#666" letter-spacing="0.5">Basil pesto · sun-dried tomato · roasted almonds</text>
  {diamond_rule(80, 910, 920, "#18170F", 0.15)}
  {wordmark_h(540, 970, "#18170F", 28, 7.5)}
</svg>""")

# ── 12: Tagliatelle — full bleed photo, huge white italic over dark grad ──
write("dlc_bold_tagliatelle_post.svg", f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {clip_rect("pc", 0, 0, 1080, 1080)}
    <linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="30%" stop-color="#1A1A1A" stop-opacity="0"/>
      <stop offset="75%" stop-color="#1A1A1A" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#1A1A1A" stop-opacity="1"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="#1A1A1A"/>
  {img_el(p['tagliatelle_1080x1080'], 0, 0, 1080, 1080, "pc")}
  <rect x="0" y="0" width="1080" height="1080" fill="url(#fg)"/>
  <rect x="0" y="0" width="1080" height="5" fill="#6E0B1C"/>
  <!-- Type -->
  <text x="60" y="764" font-family="DM Sans,Arial,sans-serif" font-size="10" fill="#C9A96E" letter-spacing="5">PASTA FATTA A MANO</text>
  <text x="60" y="880" font-family="Cormorant Garamond,Georgia,serif" font-size="156" fill="#FAF9F7" font-weight="700" font-style="italic" letter-spacing="-5">Taglia-</text>
  <text x="60" y="1000" font-family="Cormorant Garamond,Georgia,serif" font-size="156" fill="#FAF9F7" font-weight="700" font-style="italic" letter-spacing="-5">telle.</text>
  <text x="62" y="1042" font-family="DM Sans,Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.45)" letter-spacing="1">Slow cooked beef shin ragu · handmade pasta</text>
  <text x="1020" y="1066" text-anchor="end" font-family="DM Sans,Arial,sans-serif" font-size="11" fill="rgba(255,255,255,0.25)" letter-spacing="3">DE LUCA</text>
</svg>""")

# ── 13: Linguine Frutti di Mare — staggered bold type, photo + dark ───────
write("dlc_bold_linguine_post.svg", f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {clip_rect("pc", 0, 0, 1080, 620)}
    <linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="55%" stop-color="#6E0B1C" stop-opacity="0"/>
      <stop offset="100%" stop-color="#6E0B1C" stop-opacity="0.93"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="#6E0B1C"/>
  {img_el(p['linguine_1080x620'], 0, 0, 1080, 620, "pc")}
  <rect x="0" y="0" width="1080" height="620" fill="url(#fg)"/>
  <!-- Large gold monogram watermark -->
  {monogram(920, 820, 180, "#FAF9F7", 0.06)}
  <!-- Staggered type block -->
  <text x="60" y="682" font-family="DM Sans,Arial,sans-serif" font-size="10" fill="rgba(255,255,255,0.5)" letter-spacing="5">IL NOSTRO MARE</text>
  <text x="60" y="788" font-family="Cormorant Garamond,Georgia,serif" font-size="112" fill="#FAF9F7" font-weight="700" font-style="italic" letter-spacing="-3">Linguine</text>
  <text x="120" y="892" font-family="Cormorant Garamond,Georgia,serif" font-size="112" fill="#FAF9F7" font-weight="700" font-style="italic" letter-spacing="-3">frutti di</text>
  <text x="60" y="996" font-family="Cormorant Garamond,Georgia,serif" font-size="112" fill="#FAF9F7" font-weight="700" font-style="italic" letter-spacing="-3">mare.</text>
  <text x="62" y="1040" font-family="DM Sans,Arial,sans-serif" font-size="12" fill="rgba(255,255,255,0.4)" letter-spacing="1">Seafood · white wine · chilli · garlic</text>
</svg>""")

# ── 14: Pasta & Risotto menu board — no photo, editorial text-only ─────────
write("dlc_bold_pasta_menu_board.svg", """<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="dots" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="20" cy="20" r="1.2" fill="#6E0B1C" opacity="0.07"/>
    </pattern>
  </defs>
  <rect width="1080" height="1080" fill="#FAF9F7"/>
  <rect width="1080" height="1080" fill="url(#dots)"/>
  <!-- Left crimson column -->
  <rect x="0" y="0" width="10" height="1080" fill="#6E0B1C"/>
  <!-- Section heading -->
  <text x="80" y="90" font-family="DM Sans,Arial,sans-serif" font-size="10" fill="#6E0B1C" letter-spacing="5" font-weight="500">PASTA &amp; RISOTTO</text>
  <line x1="80" y1="108" x2="1000" y2="108" stroke="#6E0B1C" stroke-width="1.5"/>
  <!-- Dishes — names only, no prices -->
  <text x="80" y="210" font-family="Cormorant Garamond,Georgia,serif" font-size="80" fill="#1A1A1A" font-weight="700" font-style="italic">Tagliatelle.</text>
  <text x="80" y="252" font-family="DM Sans,Arial,sans-serif" font-size="13" fill="#888">Slow cooked beef shin ragu · handmade pasta</text>
  <line x1="80" y1="276" x2="1000" y2="276" stroke="#E5E2DD" stroke-width="0.8"/>
  <text x="80" y="368" font-family="Cormorant Garamond,Georgia,serif" font-size="80" fill="#1A1A1A" font-weight="700" font-style="italic">Linguine.</text>
  <text x="80" y="410" font-family="DM Sans,Arial,sans-serif" font-size="13" fill="#888">Frutti di mare · white wine · chilli · garlic</text>
  <line x1="80" y1="434" x2="1000" y2="434" stroke="#E5E2DD" stroke-width="0.8"/>
  <text x="80" y="526" font-family="Cormorant Garamond,Georgia,serif" font-size="80" fill="#1A1A1A" font-weight="700" font-style="italic">Risotto.</text>
  <text x="80" y="568" font-family="DM Sans,Arial,sans-serif" font-size="13" fill="#888">Mixed wild mushroom · parmesan shavings</text>
  <line x1="80" y1="592" x2="1000" y2="592" stroke="#E5E2DD" stroke-width="0.8"/>
  <text x="80" y="684" font-family="Cormorant Garamond,Georgia,serif" font-size="80" fill="#6E0B1C" font-weight="700" font-style="italic">Rigatoni.</text>
  <text x="80" y="726" font-family="DM Sans,Arial,sans-serif" font-size="13" fill="#888">Gorgonzola, speck, house sauce</text>
  <!-- Footer -->
  <line x1="80" y1="900" x2="1000" y2="900" stroke="#6E0B1C" stroke-width="0.8"/>
  <text x="80" y="950" font-family="Cormorant Garamond,Georgia,serif" font-size="28" fill="#6E0B1C" font-style="italic">Pasta fatta a mano · De Luca</text>
  <text x="80" y="986" font-family="DM Sans,Arial,sans-serif" font-size="10" fill="#AAA" letter-spacing="2">CAMBRIDGE · delucacucina.co.uk</text>
</svg>""")

# ── 15: Short Rib hero — dark, photo top, bold copy ───────────────────────
write("dlc_bold_short_rib_post.svg", f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {clip_rect("pc", 0, 0, 1080, 600)}
    <linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="50%" stop-color="#1A1A1A" stop-opacity="0"/>
      <stop offset="100%" stop-color="#1A1A1A" stop-opacity="0.97"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="#1A1A1A"/>
  <rect x="0" y="0" width="1080" height="5" fill="#C9A96E"/>
  <rect x="0" y="1075" width="1080" height="5" fill="#C9A96E"/>
  {img_el(p['shortrib_1080x600'], 0, 0, 1080, 600, "pc")}
  <rect x="0" y="0" width="1080" height="600" fill="url(#fg)"/>
  <!-- Gold label -->
  <text x="60" y="644" font-family="DM Sans,Arial,sans-serif" font-size="10" fill="#C9A96E" letter-spacing="5">CARNE — SLOW COOKED</text>
  <line x1="60" y1="662" x2="600" y2="662" stroke="#C9A96E" stroke-width="0.8" opacity="0.5"/>
  <!-- Main title — stacked bold -->
  <text x="60" y="768" font-family="Cormorant Garamond,Georgia,serif" font-size="120" fill="#FAF9F7" font-weight="700" font-style="italic" letter-spacing="-3">Slow cooked</text>
  <text x="60" y="880" font-family="Cormorant Garamond,Georgia,serif" font-size="120" fill="#C9A96E" font-weight="700" font-style="italic" letter-spacing="-3">short rib.</text>
  <!-- Description -->
  <text x="62" y="936" font-family="DM Sans,Arial,sans-serif" font-size="13" fill="rgba(255,255,255,0.45)" letter-spacing="0.5">Braised in red wine · herby polenta · tender stem broccoli</text>
  <!-- Monogram bottom right -->
  {monogram(980, 1010, 80, "#FAF9F7", 0.12)}
</svg>""")

# ── 16: A La Carte announcement — bold typographic, dark, gold accents ────
write("dlc_bold_alacarte_announce.svg", f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="dots" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="20" cy="20" r="1.2" fill="#F4EDE3" opacity="0.06"/>
    </pattern>
  </defs>
  <rect width="1080" height="1080" fill="#18170F"/>
  <rect width="1080" height="1080" fill="url(#dots)"/>
  <rect x="0" y="0" width="1080" height="5" fill="#C9A96E"/>
  <rect x="0" y="1075" width="1080" height="5" fill="#C9A96E"/>
  <!-- Top label -->
  <text x="540" y="96" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="10" fill="#C9A96E" letter-spacing="6">MAY 2026</text>
  {diamond_rule(140, 112, 800, "#C9A96E", 0.5)}
  <!-- Main headline -->
  <text x="540" y="310" text-anchor="middle" font-family="Cormorant Garamond,Georgia,serif" font-size="200" fill="#F4EDE3" font-weight="700" font-style="italic" letter-spacing="-6">A La</text>
  <text x="540" y="512" text-anchor="middle" font-family="Cormorant Garamond,Georgia,serif" font-size="200" fill="#F4EDE3" font-weight="700" font-style="italic" letter-spacing="-6">Carte.</text>
  {diamond_rule(140, 548, 800, "#C9A96E", 0.5)}
  <!-- Section names -->
  <text x="540" y="624" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="13" fill="#F4EDE3" opacity="0.55" letter-spacing="4">STARTERS · PASTA · RISOTTO · MEAT &amp; FISH</text>
  <!-- Arch pair decorative -->
  {arch(120, 580, 1.1, "#C9A96E", 0.09)}
  {arch(760, 580, 1.1, "#C9A96E", 0.09)}
  <!-- Middle section — 3 hero dishes -->
  <text x="540" y="730" text-anchor="middle" font-family="Cormorant Garamond,Georgia,serif" font-size="42" fill="#F4EDE3" font-style="italic" opacity="0.9">Burrata · Tagliatelle · Tiramisù</text>
  <text x="540" y="770" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="11" fill="#C9A96E" opacity="0.65" letter-spacing="2">AND MUCH MORE — HANDMADE DAILY</text>
  <!-- Wordmark -->
  {diamond_rule(140, 870, 800, "#F4EDE3", 0.15)}
  {wordmark_h(540, 940, "#F4EDE3", 38, 9)}
</svg>""")

# ── 17: Dolci showcase — cream, elegant dessert list, no photo ────────────
write("dlc_bold_dolci_board.svg", f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="dots" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="20" cy="20" r="1.2" fill="#18170F" opacity="0.06"/>
    </pattern>
  </defs>
  <rect width="1080" height="1080" fill="#F4EDE3"/>
  <rect width="1080" height="1080" fill="url(#dots)"/>
  <!-- Right arch decoration -->
  {arch(820, 80, 1.8, "#18170F", 0.06)}
  <!-- Top wordmark -->
  <text x="540" y="72" text-anchor="middle" font-family="Cormorant Garamond,Georgia,serif" font-size="16" fill="#18170F" letter-spacing="8" font-weight="600">DE LUCA</text>
  <line x1="300" y1="82" x2="780" y2="82" stroke="#18170F" stroke-width="0.5"/>
  <!-- DOLCI heading -->
  <text x="80" y="202" font-family="Cormorant Garamond,Georgia,serif" font-size="168" fill="#18170F" font-weight="700" font-style="italic" letter-spacing="-5">Dolci.</text>
  {diamond_rule(80, 226, 920, "#18170F", 0.2)}
  <!-- Dessert list — name + description only, no prices -->
  <text x="80" y="310" font-family="Cormorant Garamond,Georgia,serif" font-size="54" fill="#18170F" font-weight="600" font-style="italic">Tiramisù.</text>
  <text x="82" y="342" font-family="DM Sans,Arial,sans-serif" font-size="12.5" fill="#666">Chocolate, coffee liqueur &amp; fresh espresso — made in-house</text>
  <line x1="80" y1="368" x2="1000" y2="368" stroke="#18170F" stroke-width="0.4" opacity="0.2"/>
  <text x="80" y="452" font-family="Cormorant Garamond,Georgia,serif" font-size="54" fill="#18170F" font-weight="600" font-style="italic">Panna Cotta.</text>
  <text x="82" y="484" font-family="DM Sans,Arial,sans-serif" font-size="12.5" fill="#666">Vanilla · cinnamon shortbread · blackberry coulis</text>
  <line x1="80" y1="510" x2="1000" y2="510" stroke="#18170F" stroke-width="0.4" opacity="0.2"/>
  <text x="80" y="594" font-family="Cormorant Garamond,Georgia,serif" font-size="54" fill="#18170F" font-weight="600" font-style="italic">New York Cheesecake.</text>
  <text x="82" y="626" font-family="DM Sans,Arial,sans-serif" font-size="12.5" fill="#666">Citrus &amp; vanilla · blueberry compote</text>
  <line x1="80" y1="652" x2="1000" y2="652" stroke="#18170F" stroke-width="0.4" opacity="0.2"/>
  <text x="80" y="736" font-family="Cormorant Garamond,Georgia,serif" font-size="54" fill="#18170F" font-weight="600" font-style="italic">Affogato al Caffè.</text>
  <text x="82" y="768" font-family="DM Sans,Arial,sans-serif" font-size="12.5" fill="#666">Amaretto · espresso · Cantucci biscuit</text>
  <line x1="80" y1="794" x2="1000" y2="794" stroke="#18170F" stroke-width="0.4" opacity="0.2"/>
  <text x="80" y="878" font-family="Cormorant Garamond,Georgia,serif" font-size="54" fill="#C4622D" font-weight="600" font-style="italic">Sgroppino.</text>
  <text x="82" y="910" font-family="DM Sans,Arial,sans-serif" font-size="12.5" fill="#666">Lemon sorbet · vodka &amp; prosecco in a champagne flute</text>
  <!-- Footer rule + subtext -->
  {diamond_rule(80, 968, 920, "#18170F", 0.25)}
  <text x="540" y="1018" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="9.5" fill="#18170F" opacity="0.4" letter-spacing="3">HOMEMADE DESSERTS · ITALIAN RESTAURANT</text>
</svg>""")

# ── 18: Tiramisù hero — cream, photo, huge display type ───────────────────
write("dlc_bold_tiramisu_post.svg", f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {clip_rect("pc", 0, 0, 1080, 680)}
    <linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="48%" stop-color="#F4EDE3" stop-opacity="0"/>
      <stop offset="100%" stop-color="#F4EDE3" stop-opacity="0.97"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="#F4EDE3"/>
  {img_el(p['tiramisu_1080x680'], 0, 0, 1080, 680, "pc")}
  <rect x="0" y="0" width="1080" height="680" fill="url(#fg)"/>
  <!-- Arch pair flanking title -->
  {arch(60, 550, 1.2, "#18170F", 0.08)}
  {arch(868, 550, 1.2, "#18170F", 0.08)}
  <!-- Content -->
  <text x="540" y="726" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="10" fill="#C9A96E" letter-spacing="6">DOLCI FATTI IN CASA</text>
  <text x="540" y="856" text-anchor="middle" font-family="Cormorant Garamond,Georgia,serif" font-size="148" fill="#18170F" font-weight="700" font-style="italic" letter-spacing="-5">Tiramisù.</text>
  <text x="540" y="900" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="14" fill="#666" letter-spacing="0.5">Chocolate · coffee liqueur · fresh espresso</text>
  {diamond_rule(140, 928, 800, "#18170F", 0.18)}
  <text x="540" y="980" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="11" fill="#18170F" opacity="0.4" letter-spacing="2">MADE IN-HOUSE · EVERY DAY</text>
  {monogram(540, 1040, 56, "#18170F", 0.2)}
</svg>""")

# ── 19: A La Carte story — 1080×1920, editorial typographic ───────────────
write("dlc_bold_alacarte_story.svg", f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1920" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="dots" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="20" cy="20" r="1.2" fill="#F4EDE3" opacity="0.06"/>
    </pattern>
  </defs>
  <rect width="1080" height="1920" fill="#18170F"/>
  <rect width="1080" height="1920" fill="url(#dots)"/>
  <rect x="0" y="0" width="1080" height="5" fill="#C9A96E"/>
  <rect x="0" y="1915" width="1080" height="5" fill="#C9A96E"/>
  <!-- Corner brackets -->
  <polyline points="80,36 36,36 36,80" fill="none" stroke="#F4EDE3" stroke-width="1.3" stroke-linecap="square"/>
  <polyline points="1000,36 1044,36 1044,80" fill="none" stroke="#F4EDE3" stroke-width="1.3" stroke-linecap="square"/>
  <polyline points="80,1884 36,1884 36,1840" fill="none" stroke="#F4EDE3" stroke-width="1.3" stroke-linecap="square"/>
  <polyline points="1000,1884 1044,1884 1044,1840" fill="none" stroke="#F4EDE3" stroke-width="1.3" stroke-linecap="square"/>
  <!-- Wordmark -->
  <text x="540" y="96" text-anchor="middle" font-family="Cormorant Garamond,Georgia,serif" font-size="36" fill="#F4EDE3" font-weight="600" letter-spacing="12">DE LUCA</text>
  <line x1="300" y1="110" x2="780" y2="110" stroke="#F4EDE3" stroke-width="0.5"/>
  <text x="540" y="134" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="9" fill="#F4EDE3" letter-spacing="3.5">ITALIAN RESTAURANT</text>
  {diamond_rule(80, 158, 920, "#C9A96E", 0.6)}
  <!-- Season label -->
  <text x="80" y="250" font-family="DM Sans,Arial,sans-serif" font-size="11" fill="#C9A96E" letter-spacing="5">SPRING — MAY 2026</text>
  <!-- Headline -->
  <text x="80" y="430" font-family="Cormorant Garamond,Georgia,serif" font-size="220" fill="#F4EDE3" font-weight="700" font-style="italic" letter-spacing="-7">A La</text>
  <text x="80" y="650" font-family="Cormorant Garamond,Georgia,serif" font-size="220" fill="#C9A96E" font-weight="700" font-style="italic" letter-spacing="-7">Carte.</text>
  {diamond_rule(80, 690, 920, "#F4EDE3", 0.2)}
  <!-- Arch decorations -->
  {arch(780, 440, 2.2, "#C9A96E", 0.07)}
  <!-- Sections -->
  <text x="80" y="790" font-family="DM Sans,Arial,sans-serif" font-size="10" fill="#F4EDE3" opacity="0.4" letter-spacing="4">STARTERS</text>
  <text x="80" y="870" font-family="Cormorant Garamond,Georgia,serif" font-size="64" fill="#F4EDE3" font-weight="600" font-style="italic">Burrata.</text>
  <text x="82" y="900" font-family="DM Sans,Arial,sans-serif" font-size="13" fill="#F4EDE3" opacity="0.5">Basil pesto · sun-dried tomato · roasted almonds</text>
  <line x1="80" y1="926" x2="1000" y2="926" stroke="#F4EDE3" stroke-width="0.4" opacity="0.15"/>
  <text x="80" y="978" font-family="DM Sans,Arial,sans-serif" font-size="10" fill="#F4EDE3" opacity="0.4" letter-spacing="4">PASTA</text>
  <text x="80" y="1058" font-family="Cormorant Garamond,Georgia,serif" font-size="64" fill="#F4EDE3" font-weight="600" font-style="italic">Tagliatelle.</text>
  <text x="82" y="1088" font-family="DM Sans,Arial,sans-serif" font-size="13" fill="#F4EDE3" opacity="0.5">Slow cooked beef shin ragu · handmade</text>
  <line x1="80" y1="1114" x2="1000" y2="1114" stroke="#F4EDE3" stroke-width="0.4" opacity="0.15"/>
  <text x="80" y="1166" font-family="DM Sans,Arial,sans-serif" font-size="10" fill="#F4EDE3" opacity="0.4" letter-spacing="4">CARNE &amp; PESCE</text>
  <text x="80" y="1246" font-family="Cormorant Garamond,Georgia,serif" font-size="64" fill="#F4EDE3" font-weight="600" font-style="italic">Ribollita &amp; Branzino.</text>
  <text x="82" y="1276" font-family="DM Sans,Arial,sans-serif" font-size="13" fill="#F4EDE3" opacity="0.5">Sea bass · salsa verde · grilled lemon</text>
  <line x1="80" y1="1302" x2="1000" y2="1302" stroke="#F4EDE3" stroke-width="0.4" opacity="0.15"/>
  <text x="80" y="1354" font-family="DM Sans,Arial,sans-serif" font-size="10" fill="#F4EDE3" opacity="0.4" letter-spacing="4">DOLCI</text>
  <text x="80" y="1434" font-family="Cormorant Garamond,Georgia,serif" font-size="64" fill="#C9A96E" font-weight="600" font-style="italic">Tiramisù.</text>
  <text x="82" y="1464" font-family="DM Sans,Arial,sans-serif" font-size="13" fill="#F4EDE3" opacity="0.5">Made in-house · no shortcuts</text>
  <!-- CTA band -->
  {diamond_rule(80, 1640, 920, "#C9A96E", 0.5)}
  <text x="540" y="1734" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="11" fill="#F4EDE3" font-weight="500" letter-spacing="3">PRENOTA UN TAVOLO</text>
  <text x="540" y="1764" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="9" fill="#F4EDE3" opacity="0.5" letter-spacing="2">BOOK YOUR TABLE — delucacucina.co.uk</text>
  {diamond_rule(80, 1800, 920, "#C9A96E", 0.5)}
</svg>""")

# ── 20: Dolci story — photo + dessert section, editorial ──────────────────
write("dlc_bold_dolci_story.svg", f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1080" height="1920" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {clip_rect("pc", 0, 0, 1080, 1180)}
    <linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#F4EDE3" stop-opacity="0.8"/>
      <stop offset="12%"  stop-color="#F4EDE3" stop-opacity="0"/>
      <stop offset="70%"  stop-color="#F4EDE3" stop-opacity="0"/>
      <stop offset="100%" stop-color="#F4EDE3" stop-opacity="0.98"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1920" fill="#F4EDE3"/>
  {img_el(p['food_story_1080x1180'], 0, 0, 1080, 1180, "pc")}
  <rect x="0" y="0" width="1080" height="1180" fill="url(#fg)"/>
  <!-- Top wordmark -->
  <text x="540" y="88" text-anchor="middle" font-family="Cormorant Garamond,Georgia,serif" font-size="36" fill="#18170F" font-weight="600" letter-spacing="12">DE LUCA</text>
  <line x1="300" y1="100" x2="780" y2="100" stroke="#18170F" stroke-width="0.5"/>
  <text x="540" y="124" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="9" fill="#18170F" letter-spacing="3.5">ITALIAN RESTAURANT</text>
  <!-- DOLCI headline at bottom of photo -->
  <text x="80" y="1130" font-family="Cormorant Garamond,Georgia,serif" font-size="200" fill="#18170F" font-weight="700" font-style="italic" letter-spacing="-6">Dolci.</text>
  <!-- Bottom section -->
  {diamond_rule(80, 1200, 920, "#18170F", 0.25)}
  <text x="80" y="1284" font-family="Cormorant Garamond,Georgia,serif" font-size="52" fill="#18170F" font-weight="600" font-style="italic">Tiramisù.</text>
  <text x="82" y="1312" font-family="DM Sans,Arial,sans-serif" font-size="12.5" fill="#555">Made in-house · coffee liqueur · fresh espresso</text>
  <line x1="80" y1="1336" x2="1000" y2="1336" stroke="#18170F" stroke-width="0.4" opacity="0.18"/>
  <text x="80" y="1420" font-family="Cormorant Garamond,Georgia,serif" font-size="52" fill="#18170F" font-weight="600" font-style="italic">Panna Cotta.</text>
  <text x="82" y="1448" font-family="DM Sans,Arial,sans-serif" font-size="12.5" fill="#555">Vanilla · cinnamon shortbread · blackberry coulis</text>
  <line x1="80" y1="1472" x2="1000" y2="1472" stroke="#18170F" stroke-width="0.4" opacity="0.18"/>
  <text x="80" y="1556" font-family="Cormorant Garamond,Georgia,serif" font-size="52" fill="#C4622D" font-weight="600" font-style="italic">Affogato al Caffè.</text>
  <text x="82" y="1584" font-family="DM Sans,Arial,sans-serif" font-size="12.5" fill="#555">Amaretto · espresso · Cantucci biscuit</text>
  <!-- CTA -->
  {diamond_rule(80, 1680, 920, "#18170F", 0.2)}
  <text x="540" y="1766" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="11" fill="#18170F" font-weight="500" letter-spacing="3">PRENOTA UN TAVOLO</text>
  <text x="540" y="1796" text-anchor="middle" font-family="DM Sans,Arial,sans-serif" font-size="9" fill="#18170F" opacity="0.5" letter-spacing="2">BOOK YOUR TABLE — delucacucina.co.uk</text>
  {diamond_rule(80, 1832, 920, "#18170F", 0.2)}
  <!-- Corner brackets -->
  <polyline points="80,36 36,36 36,80" fill="none" stroke="#18170F" stroke-width="1.3" stroke-linecap="square" opacity="0.5"/>
  <polyline points="1000,36 1044,36 1044,80" fill="none" stroke="#18170F" stroke-width="1.3" stroke-linecap="square" opacity="0.5"/>
  <polyline points="80,1884 36,1884 36,1840" fill="none" stroke="#18170F" stroke-width="1.3" stroke-linecap="square" opacity="0.5"/>
  <polyline points="1000,1884 1044,1884 1044,1840" fill="none" stroke="#18170F" stroke-width="1.3" stroke-linecap="square" opacity="0.5"/>
</svg>""")

print(f"\n  Done — {len(os.listdir(OUTPUT_DIR))} files in {OUTPUT_DIR}")
