# Adobe Express — Brand Kit Setup

Everything you need to set De Luca up as a brand kit in Adobe Express.

## 1. Brand colours (paste hex codes)

In Adobe Express: **Your stuff → Brand → Create brand kit → Colours**

| Name | Hex | Role |
|------|-----|------|
| Terracotta | `#C4622D` | PRIMARY |
| Terra Scuro | `#A04E1F` | ACCENT |
| Terra Chiaro | `#E08A50` | HIGHLIGHT |
| Nero | `#18170F` | BASE |
| Avorio | `#F4EDE3` | GROUND |
| Oro | `#C9A96E` | DETAIL |
| Fumo | `#6B5F55` | SECONDARY |

Set **Terracotta** as primary.

## 2. Fonts

Adobe Express has both built in — search and add to your brand kit:

- **Cormorant Garamond** — set as Heading. Use Bold or SemiBold.
- **DM Sans** — set as Body. Use Regular or Medium.

The TTF files in `fonts/` are for installing on your Mac if you also use Photoshop/Canva/etc.

## 3. Logos (upload PNGs — easier than SVGs in Adobe Express)

In Adobe Express: **Brand → Logos → Upload**

Recommended uploads from `logos/` (PNG versions):

- `dlc_wordmark_primary_transparent_nero.png` — main logo, dark, transparent bg
- `dlc_wordmark_primary_transparent_avorio.png` — main logo, light, for dark backgrounds
- `dlc_monogram_transparent_nero.png` — circular DL mark
- `dlc_wordmark_horizontal_transparent_nero.png` — wide format for headers

## 4. Decorative elements

Upload from `elements/png_nero/` (or `png_avorio/` for use on dark backgrounds):

- `dlc_olive_sprig.png` — botanical accent
- `dlc_corner_bracket.png` — corner detail
- `dlc_rule_diamond.png` — section divider
- `dlc_rule_double.png` — double line divider
- `dlc_arch.png` — architectural frame

## 5. Background templates

Upload from `feed_templates/` and `story_templates/`:

| Template PNG | Use |
|---|---|
| `dlc_feed_terracotta.png` | Hero feed posts |
| `dlc_feed_nero.png` | Premium evening feed |
| `dlc_feed_avorio.png` | Light editorial feed |
| `dlc_feed_salvia.png` | Seasonal/fresh feed |
| `dlc_story_terracotta.png` | Hero story |
| `dlc_story_nero.png` | Premium story |
| `dlc_story_avorio.png` | Light story |
| `dlc_story_nero_gold.png` | Premium-tier story (gold bars) |

Each template already has wordmark, brackets, border, dot texture baked in. Drop your photo or headline on top and post.

## 6. Brand photos

In `Brand → Brand photos`:

Upload curated food shots from the project's `footage/photos/raw/2026/food_pics/`:

- Desserts: `Cheescake_PannaCotta_*.JPG`, `New_York_Cheesecake_*.JPG`, `Vanilla_pannacotta_*.JPG`
- Mains: `Lasagna_*.JPG`, `Rigatoni_*.JPG`, `Salmon_*.JPG`, `ShortRib_*.JPG`
- Starters: `Burrata_*.JPG`, `Whole_GamberiniPrawns_*.JPG`

## Quick workflow

1. Open Adobe Express
2. Pick a template (or start blank, drop in a `feed_templates/` PNG)
3. Click brand kit icon → fonts and colours auto-populate
4. Add headline in Cormorant Garamond Bold, large
5. Drop a brand photo in the centre area
6. Logo is already on the template — don't double up
7. Export as PNG → post

## What NOT to do in Adobe Express

- Don't use the built-in "Italian restaurant" templates — they're the dated style we're replacing
- Don't use Adobe Express stock food photos — use the project's photography
- Don't apply default Adobe Express filters (they look 2018)
- Don't use script fonts even if Adobe Express suggests them
