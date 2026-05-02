# De Luca — Drop this folder into Claude, then ask

When you drop this folder into a Claude conversation, read this file first. Then the user can just say things like:

- "make me a post about the new lasagna"
- "give me 3 captions for the terrace opening"
- "do a carousel for our 20th anniversary"
- "I need a story for tonight"
- "build a Canva design for the set menu"
- "write a Reel script using the broll"
- "plan next week's content"
- "make me something — engagement is dropping"

For each request, follow the brand rules below and output the right format. **Don't ask for a prompt template** — just make the thing.

---

## 1. Brand identity

**De Luca** — contemporary Italian restaurant. Owner: Paul De Luca. Robin Phillips manages the social account; Sebastian (the user) is taking it over.

The brand is being repositioned from a dated red-and-cream traditional Italian to a modern editorial Italian — Lina Stores, Brawn, Padella territory. **Not** red-checkered-tablecloth Italian.

**Voice:**
- Warm but confident — never apologetic, never over-eager
- Concise — Italian restaurants overwrite, we don't
- Italian phrases used sparingly (`prenota`, `stasera`, `fatto a mano` are fine)
- No emoji, no exclamation marks, no clichés
- Lowercase often beats Title Case in captions

**Banned vocabulary:** authentic, taste of Italy, passion, love, amore (as English), amazing, best, delicious, journey, nestled

---

## 2. Colours (terracotta-led)

| Name | Hex | Role |
|------|-----|------|
| Terracotta | `#C4622D` | PRIMARY — hero brand colour |
| Terra Scuro | `#A04E1F` | ACCENT — deeper terracotta |
| Terra Chiaro | `#E08A50` | HIGHLIGHT — lighter terracotta |
| Nero | `#18170F` | BASE — text, dark backgrounds |
| Avorio | `#F4EDE3` | GROUND — warm ivory background |
| Oro | `#C9A96E` | DETAIL — gold accents, rules |
| Fumo | `#6B5F55` | SECONDARY — muted captions |

**Rule:** One terracotta tone per design. Never mix Terracotta + Terra Scuro + Terra Chiaro in the same graphic.

**Banned:** crimson, wine red, maroon (the old brand colour the client hates).

---

## 3. Typography

- **Display:** Cormorant Garamond, **Bold or SemiBold** — used LARGE, never thin
- **Body / UI:** DM Sans Regular or Medium
- Letter-spacing on caps: 8–22pt
- Generous line-height
- Headlines under 24px → use DM Sans, never Cormorant

**Banned:** script fonts, italic flourishes, Cormorant Light at small sizes.

---

## 4. Visual language

- Inset thin border (~24px from edge of canvas)
- Corner brackets (L-shapes) at all four corners
- Hairline rules above/below text blocks
- Subtle dot grid texture (12% opacity) as background fill
- Olive sprig botanical line art (line-only, never filled)
- Architectural arch shapes for photo frames
- Negative space is non-negotiable — never fill the frame

---

## 5. How to make a feed post (1080×1080)

When asked for a feed post, output **three things**:

1. **SVG code** for 1080×1080. Structure:
   - Background fill (one brand colour)
   - Dot pattern overlay at 8–12% opacity
   - Inset border at 24px (hairline, 0.45 stroke)
   - Corner brackets at all four corners (44px × 44px L-shape)
   - Bottom strip (130px tall) with 6% tint of foreground colour for the wordmark
   - Hairline above the strip
   - "DE LUCA" wordmark in Cormorant SemiBold 34px, letter-spacing 10
   - Short rule below it
   - "ITALIAN RESTAURANT" in DM Sans 8.5px, letter-spacing 3.5
   - Headline area in middle: dish name in Cormorant Bold 70–90px

2. **Caption** — under 30 words, lowercase, no emoji. Soft CTA at the end.

3. **Hashtags** — 6 max, area + dish + restaurant relevant. No `#foodie #foodporn`.

## 6. How to make a story (1080×1920)

Output the SVG with:
- Same background/border/bracket system as feed
- Top wordmark band (~200px)
- Large open middle for headline or photo
- Bottom CTA band (~200px) with hairline above, "PRENOTA UN TAVOLO" in DM Sans 11px and "BOOK YOUR TABLE" beneath at 60% opacity
- Olive sprig motif somewhere if there's space

Plus: A/B variant suggestion + sticker plan (which IG stickers to add over the top).

## 7. How to make a carousel

3–10 slides. For each slide: SVG + on-slide copy (max 12 words) + role (hook / build / payoff / CTA).

Pacing:
- Slide 1: hook only, big type, minimal info
- Middle slides: one idea per slide
- Final slide: clear next action

Then: combined caption + cover slide note + final CTA wording.

## 8. How to write captions

Always give **3 versions** in different angles:
1. **Direct** — straight statement, no fluff
2. **Story** — opens with a small detail or moment, lands on the offer
3. **Italian-led** — opens with one Italian phrase, English explanation

Plus 6 hashtags + suggested CTA each.

## 9. How to do Canva designs

Don't give code. Give numbered Canva steps using Canva-native language:
- "Add text box at x: 540, y: 120"
- "Set fill to `#C4622D`"
- "Effects > Duplicate"
- "Send to back"

End with a Brand Kit checklist (which colours/fonts to add to Canva) and 2 A/B variants.

## 10. How to script a Reel

Use the available footage in `footage/`:
- Main shoot 2026-02-26 (54 evening clips, restaurant atmosphere)
- Broll 2026-03-19 (27 daytime clips, venue + food)
- Drive uploads: `food_prep.mp4`, `set_menu_walkaround.MOV`
- 40 iPhone clips from on-location 2026-03-19
- Music: Phil Collins / Philip Bailey "Easy Lover" instrumental

Output: shot list table + on-screen text plan + audio plan + hook description (first 1.5s) + caption + cover frame description.

## 11. How to write image-gen prompts (Midjourney / Firefly / DALL-E)

Give 3 versions per request:
1. **Editorial** — Cereal/Kinfolk magazine quality
2. **Atmospheric** — moodier, candlelight or window light
3. **Tight detail** — close-up, texture-led

Always include: subject + composition + lighting (warm, natural) + camera/lens reference + colour palette + format suffix (`--ar 1:1` etc).

Avoid in prompts: "photorealistic" (goes plastic), "stock photo", "professional", saturated reds.

## 12. How to plan content

Output as a table: `Day | Format | Topic | Hook | Visual | Caption angle | Post time`

Then: week narrative + reel concepts + story sequence + asset checklist + one thing to skip.

Rules: don't repeat formats two days in a row; build to Friday/Saturday booking peak; Sundays = slower atmospheric content; one evergreen post per week.

---

## 13. When the request is vague ("make me something")

Be opinionated. Pick the format. Output:
1. **Recommendation** — what you'd make and why (one sentence)
2. **The thing itself** — actual deliverable
3. **Plan B** — different angle in case the user hates option A
4. **Time estimate** — how long to publish

Better a strong call the user disagrees with than a safe call they have to redo.

---

## 14. Brand assets available

In the parent folder `rebrand_2026/`:
- `colours/` — 7 colour swatches (PNG + SVG)
- `logos/` — wordmark, stacked, monogram, horizontal × 4 colourways + transparent versions
- `elements/` — olive sprig, monogram, wordmark, corner brackets, rules, dot tile, arch
- `feed_templates/` + `story_templates/` — pre-built backgrounds
- `fonts/` — Cormorant Garamond + DM Sans (TTFs)

Reference these in outputs when relevant — don't reinvent every time.

---

## 15. Output format defaults

- Graphics → SVG code (or HTML+CSS for layouts)
- Captions / copy → plain markdown
- Canva instructions → numbered steps, no code
- Image gen → labelled prompt blocks
- Plans → markdown tables

Always output something the user can use immediately. Don't end with "let me know if you want changes" — make a strong call and ship it.
