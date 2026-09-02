#!/usr/bin/env python3
"""Generates regions/<id>.html from data/regions.json + template.html.

Run this after editing data/regions.json (e.g. to add a region, swap a
video, or edit the copy) to regenerate every region page:

    python3 generate.py
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(ROOT, "data", "regions.json")) as f:
    data = json.load(f)

with open(os.path.join(ROOT, "template.html")) as f:
    template = f.read()

os.makedirs(os.path.join(ROOT, "regions"), exist_ok=True)

for region in data["regions"]:
    causes_html = "\n".join(f"      <li>{c}</li>" for c in region["causes"])

    video_cards = []
    for v in region["videos"]:
        video_cards.append(f"""      <div class="video-card">
        <div class="video-frame">
          <iframe src="https://www.youtube.com/embed/{v['id']}"
                  title="{v['title']}"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowfullscreen loading="lazy"></iframe>
        </div>
        <div class="video-meta">
          <div class="video-title">{v['title']}</div>
          <div class="video-channel">{v['channel']}</div>
        </div>
      </div>""")
    videos_html = "\n".join(video_cards)

    page = (
        template
        .replace("{{TITLE}}", region["title"])
        .replace("{{INTRO}}", region["intro"])
        .replace("{{CAUSES}}", causes_html)
        .replace("{{VIDEOS}}", videos_html)
    )

    out_path = os.path.join(ROOT, "regions", f"{region['id']}.html")
    with open(out_path, "w") as f:
        f.write(page)
    print(f"wrote {out_path}")

print(f"\nDone: {len(data['regions'])} region pages generated.")
