# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML/CSS/JS today: `regions/*.html` are generated from `data/regions.json` via `generate.py`, and the body diagram in `index.html` is generated from real anatomical SVG path data (`vendor/`, MIT licensed) via `build_diagram.py`. Open to introducing a lightweight build tool or framework during the redesign if it genuinely earns its place (e.g. for shared components/tokens across the diagram and 20+ region pages), provided the shipped result is still a static site deployable for free with no accounts, sign-in, or backend (e.g. GitHub Pages).

## Users

Public — anyone who finds the site, arriving cold with no context on who built it or why. Design must be self-explanatory within seconds, not assume a returning or briefed visitor.

## Product Purpose

Let someone with a sore or tight muscle get to a couple of trustworthy stretch/physical-therapy videos as fast as possible, by clicking directly on a body diagram instead of typing a search query. Success is reaching the right muscle's videos in one or two clicks.

## Positioning

The mechanism a search engine or YouTube search doesn't offer: point at where it hurts (recognition) instead of naming it (recall). The interactive anatomical diagram *is* the product, not a feature bolted onto a list.

## Operating Context

Visitor is often looking this up in the moment — mid-workout cooldown, desk-posture stiffness, an old injury acting up — frequently on a phone, sometimes one-handed or physically moving/stretching rather than sitting at a keyboard. Must work well touch-first, not just as a scaled-down desktop layout.

## Capabilities and Constraints

- Interactive front/back anatomical body diagram (real muscle-shaped SVG paths, not illustrative shapes); clicking/tapping a muscle navigates to that muscle's dedicated stretch page.
- Each region page: a short "why this happens" intro, common causes, and 2 curated real YouTube videos (embedded), pulled from `data/regions.json`.
- The diagram-to-page mapping lives in `build_diagram.py`'s `MUSCLE_MAP` — not every anatomical shape currently has (or needs) a page.
- No accounts, no backend, no database.
- Code-only visual craft for this redesign pass — no newly generated illustrations, icons, or custom fonts.
- Non-negotiable through any redesign: a detailed, clickable anatomical diagram remains the primary way to reach the stretch content. Layout/structure/navigation model around it is open to change.
- Not medical advice. A disclaimer to that effect must remain visible on every page.

## Brand Commitments

Named **Painpoint**. No logo beyond the wordmark; visual identity established during the redesign (see DESIGN.md).

## Evidence on Hand

Real, verified YouTube videos already selected per muscle (2 each, from named PT/fitness channels), in `data/regions.json`. No user research, analytics, or testimonials exist — none should be fabricated or implied.

## Product Principles

1. One click from "it hurts here" to a relevant video — the diagram is the product.
2. Designed for a cold, public visitor — no assumed context, no explanation required to start using it.
3. Curated over comprehensive — a couple of trustworthy videos beats an exhaustive list.
4. Static and free to run forever — no accounts, no backend, $0 to host.
5. Not medical advice, always — the disclaimer is a permanent fixture, not a formality to shrink away.

## Accessibility & Inclusion

No formal standard specified by the user. Flagged as a real audit target given the primary navigation is a visual diagram: every muscle's page must also be reachable without a mouse (keyboard) and without sight (screen reader), not just via clicking a shape.
