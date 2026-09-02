#!/usr/bin/env python3
"""Builds index.html's body diagram from real anatomical path data
(vendor/bodyFront.ts, vendor/bodyBack.ts, vendor/SvgMaleWrapper.tsx — MIT
licensed, from react-native-body-highlighter by Hicham El Abbassi; see
vendor/LICENSE).

Reads index.template.html, fills in the front/back SVG markup and the
region-label table, and writes index.html.

Run this again after editing MUSCLE_MAP or PAGE_LABELS below (e.g. to relink
a muscle to a different regions/*.html page, or make one purely decorative).

Every interactive muscle shape is wrapped in a real <a href="regions/x.html">
(works with no JavaScript at all — JS only adds the hover tooltip) and gets
an invisible, generously-sized hit-area centered on its own bounding box, so
thin shapes (a neck, an Achilles sliver) are still comfortably tappable on a
phone even though the drawn muscle itself is narrow.
"""
import re
import os
import json

ROOT = os.path.dirname(os.path.abspath(__file__))

# Minimum tap target, in SVG viewBox units. Measured live: at a 320 CSS px
# phone viewport the diagram card's padding leaves the svg only ~256 CSS px
# wide against a 724-unit viewBox (~0.354 px/unit), so 44 CSS px needs
# ~124 units; rounded up for margin.
MIN_HIT_DIAMETER = 126

# slug (from the vendor data) -> destination page id in regions/, or None
# to render that body part as plain, non-interactive fill (no page for it).
MUSCLE_MAP = {
    "chest": "chest",
    "obliques": "obliques",
    "abs": "abs",
    "biceps": "biceps",
    "triceps": "triceps",
    "neck": "neck",
    "trapezius": "traps",
    "deltoids": "shoulders",
    "adductors": "adductors",
    "quadriceps": "quads",
    "knees": "knees",
    "tibialis": "calves",
    "calves": "calves",
    "forearm": "wrists",
    "hands": None,
    "ankles": "ankles",
    "feet": "ankles",
    "head": None,
    "hair": None,
    "upper-back": "upper-back",
    "lower-back": "lower-back",
    "gluteal": "glutes",
    "hamstring": "hamstrings",
}

# slug -> friendly name for that specific shape's tooltip / aria-label
DISPLAY_NAMES = {
    "chest": "Pectoralis Major (Chest)",
    "obliques": "Obliques",
    "abs": "Rectus Abdominis (Abs)",
    "biceps": "Biceps Brachii",
    "triceps": "Triceps Brachii",
    "neck": "Neck",
    "trapezius": "Trapezius",
    "deltoids": "Deltoids (Shoulders)",
    "adductors": "Adductors (Inner Thigh)",
    "quadriceps": "Quadriceps",
    "knees": "Knees",
    "tibialis": "Tibialis Anterior",
    "calves": "Calves",
    "forearm": "Forearm",
    "hands": "Hand",
    "ankles": "Ankle",
    "feet": "Foot",
    "head": "Head",
    "hair": "Hair",
    "upper-back": "Upper Back",
    "lower-back": "Lower Back",
    "gluteal": "Gluteus Maximus",
    "hamstring": "Hamstrings",
}

# destination page id -> label used in the fallback "browse the full list" panel
PAGE_LABELS = {
    "neck": "Neck",
    "shoulders": "Deltoids (Shoulders)",
    "traps": "Trapezius",
    "upper-back": "Upper Back",
    "lower-back": "Lower Back",
    "chest": "Pectoralis Major (Chest)",
    "abs": "Rectus Abdominis (Abs)",
    "obliques": "Obliques",
    "adductors": "Adductors (Inner Thigh)",
    "glutes": "Gluteus Maximus",
    "hamstrings": "Hamstrings",
    "quads": "Quadriceps",
    "knees": "Knees",
    "calves": "Calves & Shins",
    "ankles": "Ankles & Feet",
    "biceps": "Biceps Brachii",
    "triceps": "Triceps Brachii",
    "wrists": "Forearms",
}

BLOCK_RE = re.compile(
    r'slug:\s*"([\w-]+)".*?path:\s*\{(.*?)\n\s*\},\s*\n\s*\},',
    re.DOTALL,
)
ARRAY_RE = re.compile(r'(left|right|common)\s*:\s*\[(.*?)\]', re.DOTALL)
PATH_STR_RE = re.compile(r'"([^"]+)"')

# Real per-path bounding boxes, computed once via a browser's actual SVG
# engine (getBBox()) — see data/path-bboxes.json's header note below. SVG
# path data here mixes M/L/C/Q/S/T and relative *and* arc ('a') commands;
# a regex/naive-parser bbox is NOT reliable for this (arc flags in
# particular don't tokenize with a plain number regex), so this cache is
# the source of truth rather than a re-derived approximation.
with open(os.path.join(ROOT, "data", "path-bboxes.json")) as f:
    PATH_BBOXES = json.load(f)


def parse_body_file(path):
    with open(path) as f:
        text = f.read()
    parts = []
    for slug, path_block in BLOCK_RE.findall(text):
        sides = {}
        for side, arr_body in ARRAY_RE.findall(path_block):
            sides[side] = PATH_STR_RE.findall(arr_body)
        parts.append((slug, sides))
    return parts


def parse_outline(path, side):
    with open(path) as f:
        text = f.read()
    label = f"male-body-outline-{side}"
    m = re.search(r'd="([^"]+)"\s*\n\s*accessible=\{true\}\s*\n\s*accessibilityLabel="' + label + '"', text)
    return m.group(1) if m else None


def bbox_of(d):
    """(cx, cy, half-width, half-height) of a path, from the precomputed
    getBBox() cache (see PATH_BBOXES above)."""
    b = PATH_BBOXES[d]
    cx = b["x"] + b["w"] / 2
    cy = b["y"] + b["h"] / 2
    return cx, cy, b["w"] / 2, b["h"] / 2


def render_svg_body(parts, outline_d, view_label):
    lines = []
    if outline_d:
        lines.append(f'      <path class="body-outline" d="{outline_d}" aria-hidden="true"></path>')
    for slug, sides in parts:
        region = MUSCLE_MAP.get(slug)
        label = DISPLAY_NAMES.get(slug, slug)
        interactive = region is not None
        all_paths = []
        for side in ("left", "right", "common"):
            all_paths.extend(sides.get(side, []))
        if not all_paths:
            continue

        if not interactive:
            for d in all_paths:
                lines.append(f'      <path class="muscle-inert" d="{d}" aria-hidden="true"></path>')
            continue

        lines.append(f'      <a href="regions/{region}.html" class="muscle-link" aria-label="{label}">')
        for d in all_paths:
            cx, cy, hw, hh = bbox_of(d)
            # Clamp each axis independently rather than forcing a uniform
            # circle from the larger axis — an already-wide-enough thigh
            # shouldn't get its hit-area ballooned sideways into its
            # neighbor just because it's also tall.
            rx = max(hw, MIN_HIT_DIAMETER / 2)
            ry = max(hh, MIN_HIT_DIAMETER / 2)
            lines.append(f'        <path class="muscle-fill" d="{d}"></path>')
            lines.append(
                f'        <ellipse class="hit-area" cx="{cx:.1f}" cy="{cy:.1f}" '
                f'rx="{rx:.1f}" ry="{ry:.1f}"></ellipse>'
            )
        lines.append('      </a>')

    body = "\n".join(lines)
    view_box = "0 0 724 1448" if view_label == "front" else "724 0 724 1448"
    return (
        f'    <svg id="view-{view_label}" viewBox="{view_box}" '
        f'xmlns="http://www.w3.org/2000/svg" aria-label="{view_label.title()} view muscle diagram">\n'
        f"{body}\n"
        f"    </svg>"
    )


def render_fallback_grid():
    return "\n".join(
        f'          <li><a href="regions/{page_id}.html">{label}</a></li>'
        for page_id, label in PAGE_LABELS.items()
    )


def compute_stats():
    """Real counts from data/regions.json, scoped to pages actually linked
    from the diagram (PAGE_LABELS) — never a fabricated or stale number."""
    with open(os.path.join(ROOT, "data", "regions.json")) as f:
        regions = json.load(f)["regions"]
    linked = set(PAGE_LABELS.keys())
    video_ids = set()
    for r in regions:
        if r["id"] in linked:
            for v in r["videos"]:
                video_ids.add(v["id"])
    return len(linked), len(video_ids)


def main():
    front = parse_body_file(os.path.join(ROOT, "vendor", "bodyFront.ts"))
    back = parse_body_file(os.path.join(ROOT, "vendor", "bodyBack.ts"))
    outline_front = parse_outline(os.path.join(ROOT, "vendor", "SvgMaleWrapper.tsx"), "front")
    outline_back = parse_outline(os.path.join(ROOT, "vendor", "SvgMaleWrapper.tsx"), "back")

    front_svg = render_svg_body(front, outline_front, "front")
    back_svg = render_svg_body(back, outline_back, "back")
    fallback_grid = render_fallback_grid()
    muscle_count, video_count = compute_stats()

    with open(os.path.join(ROOT, "index.template.html")) as f:
        template = f.read()

    page = (
        template
        .replace("{{FRONT_SVG}}", front_svg)
        .replace("{{BACK_SVG}}", back_svg)
        .replace("{{FALLBACK_GRID}}", fallback_grid)
        .replace("{{MUSCLE_COUNT}}", str(muscle_count))
        .replace("{{VIDEO_COUNT}}", str(video_count))
    )

    with open(os.path.join(ROOT, "index.html"), "w") as f:
        f.write(page)

    print(f"front: {len(front)} body parts parsed (outline {'found' if outline_front else 'MISSING'})")
    print(f"back:  {len(back)} body parts parsed (outline {'found' if outline_back else 'MISSING'})")
    print("wrote index.html")

    mapped_slugs = {slug for slug, _ in front} | {slug for slug, _ in back}
    unknown = mapped_slugs - set(MUSCLE_MAP.keys())
    if unknown:
        print(f"WARNING: slugs with no entry in MUSCLE_MAP (rendered inert): {sorted(unknown)}")


if __name__ == "__main__":
    main()
