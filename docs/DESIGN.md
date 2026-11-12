# Design System — Stretch Finder

<!-- Replaces the earlier Starbucks-inspired extraction. That direction
     (warm cream, green, consumer-retail) was tried and rejected as feeling
     empty and generic. This document describes what's actually implemented
     now — a sports-medicine / performance-lab system, not a retail one. -->

## 1. Visual Theme & Atmosphere

Reads as a clinical/athletic tool — the kind of thing a sports-medicine
clinic or a team's athletic-performance staff would actually put in front
of an athlete, not a consumer wellness brand. Single committed dark theme
(no light mode): a near-black graphite canvas, a fine dot-grid behind the
diagram (a "diagnostic monitor" field, not decoration), one confident blue
accent, and the muscle diagram rendered in a hot orange-red — reads as a
thermal/heat-map highlight ("where the load is"), not literal gore.

**Key characteristics:**
- One theme, always dark. No `prefers-color-scheme` branching — the use
  scene (a clinical/performance tool) doesn't call for a light variant.
- One accent color (blue, `#5c8ff5`) used consistently for links, active
  states, and stat numbers. The muscle diagram's orange-red is the
  illustrated subject's own color, not a second UI accent.
- Real, computed numbers as content (`18 muscle groups`, `36 curated
  videos`) — never fabricated stats or credibility claims.
- Front and back views render side by side on desktop (not a toggle) —
  a toggle is only reintroduced under the 900px breakpoint where there
  isn't room for both.
- Typography is IBM Plex Sans (body/display) + IBM Plex Mono (labels,
  stats, technical captions) — chosen because IBM Plex was designed for
  serious technical/enterprise software, which is the actual register
  here, not a warm consumer one.
- No cards-as-page-structure. Causes are plain rule-separated typography;
  only videos (which need a frame for the embed) are boxed.

## 2. Color Tokens

| Token | Value | Use |
|---|---|---|
| `--canvas` | `#0e1116` | Page background |
| `--surface` | `#171b22` | Video card background |
| `--surface-alt` | `#1d2229` | Video placeholder (pre-thumbnail) |
| `--ink` | `#f2f4f7` | Primary text |
| `--ink-soft` | `#93a0b0` | Secondary/body text, captions |
| `--border` | `rgba(242,244,247,0.12)` | Hairlines, dividers |
| `--accent` | `#5c8ff5` | Links, active tab, stat numbers, section labels |
| `--accent-dim` | `#2f6fed` | Non-text decorative use (selection bg) |
| `--focus` | `#5ec8ff` | Keyboard focus rings only — never reused elsewhere |
| `--muscle` | `#e2542f` | Diagram muscle fill (resting) |
| `--muscle-hover` | `#ff7a4d` | Diagram muscle fill (hover/press) |
| `--muscle-stroke` | `#7a2814` | Diagram muscle outline |
| `--skin` | `#3a4048` | Diagram inert parts (head/hands/feet) |

All text pairings verified ≥4.5:1 against their background before shipping
(see git history / prior critique for the actual computed ratios) — the
first version of this site shipped a contrast bug from skipping that step;
don't skip it again.

## 3. Typography

- **Family:** `IBM Plex Sans` (400/500/600/700), `IBM Plex Mono` (500/600)
  for labels, stat numbers, view captions ("FRONT"/"BACK"), and the
  wordmark. Loaded via Google Fonts `<link>` (this is a plain static site,
  not a bundled app — no `next/font` equivalent needed).
- **Display:** hero/region h1 at `clamp(2.1–3.1rem)`, weight 700,
  `letter-spacing: -0.02em`.
- **Body:** ~1.05rem, `--ink-soft`, measure capped around 42–62ch.
- **Labels:** small (0.72–0.95rem) IBM Plex Mono, uppercase,
  `letter-spacing: 0.06–0.12em`, colored `--accent` — used for section
  headers ("WHY THIS HAPPENS", "STRETCHES & PT VIDEOS") and the stat
  strip, never as a decorative "eyebrow" above every section (only where
  it's a genuine data/label role).

## 4. Layout

- **Home:** asymmetric split — copy column (`minmax(320px, 0.72fr)`) and
  diagram column (`1fr`), full `100dvh`-ish height, divided by a hairline
  border, not a card. Below 900px: single column, copy above, diagram
  below, front/back becomes a toggle.
- **Region pages:** `minmax(220px, 0.8fr) 1.5fr` two-column grid — causes
  (plain list) beside videos (boxed cards). Single column below 900px,
  causes first.
- Spacing is tighter than a consumer-retail site would use — this is a
  dense, information-forward tool, not an airy marketing page. Don't
  reintroduce large empty margins "for breathing room"; if something
  feels sparse, add real content (another real stat, a denser diagram
  treatment) rather than more whitespace.

## 5. Motion

- `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`, `--dur-fast: 140ms`,
  `--dur-base: 200ms` (both collapse to `1ms` under
  `prefers-reduced-motion`).
- Signature moment: `scale(0.94)` press feedback, applied identically to
  every pressable thing (muscle shapes, tab labels) — one authored
  moment, not scattered effects.

## 6. Do's and Don'ts

**Do:** keep the dot-grid subtle (it's a texture cue, not a pattern to
notice); keep the muscle diagram as the only illustrative color in the
system; keep stat numbers real and recomputed from `data/regions.json`
(see `build_diagram.py`'s `compute_stats()`) — never hardcode or invent
one; keep causes un-boxed.

**Don't:** add a light mode "for completeness" — the theme is a deliberate
choice, not an oversight; don't add a second accent color; don't put
everything back in matching rounded-white cards; don't fabricate
credibility copy ("trusted by athletic trainers", "as recommended by...")
— PRODUCT.md is explicit that no such relationship exists, and the honest
stat strip does that job instead.
