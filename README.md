# Stretch Finder

**Live site:** https://mattthomas7641.github.io/stretch-finder/

A small public website: click a muscle on a real anatomical front/back body
diagram, land on a page with a couple of curated stretch / physical-therapy
YouTube videos for that muscle. See `PRODUCT.md` for the product brief and
`DESIGN.md` for the visual design system (an athletic/sports-medicine look —
a bold black diagnostic "stage" for the diagram, one red-orange accent
shared with the muscle color, condensed display type).

Every clickable muscle is a real `<a href="regions/x.html">` and the "browse
the full list" fallback is a native `<details>` — the whole site (diagram,
front/back toggle, every destination page) works with JavaScript completely
disabled. JS only adds the hover/focus tooltip label.

## Structure

```
index.html               GENERATED — the diagram page. Don't hand-edit this.
index.template.html      the page shell (header/footer/script) for index.html
build_diagram.py         reads vendor/body*.ts + data/path-bboxes.json + index.template.html -> writes index.html
data/path-bboxes.json    real getBBox() measurements per muscle path (see below) — used to size tap targets
vendor/                  real anatomical muscle path data (MIT licensed, see below)
style.css                shared styles for every page
template.html            the HTML template used to build each region page
data/regions.json        content for every region (title, intro, causes, videos)
generate.py              reads regions.json + template.html -> writes regions/*.html
regions/*.html           generated pages (don't hand-edit — edit regions.json instead)
```

### Why `data/path-bboxes.json` exists

Every clickable muscle also gets an invisible, generously-sized tap target
(`build_diagram.py`'s `MIN_HIT_DIAMETER`) independent of the muscle's drawn
shape, so a thin sliver (a neck, an Achilles tendon) is still comfortably
tappable on a phone. Sizing that requires each path's real bounding box —
and this dataset's paths mix relative *and* absolute commands plus elliptical
arcs, which a regex or hand-rolled parser cannot reliably measure. The cache
was generated once by loading every path into a real browser and reading its
native `getBBox()`. If the vendor path data ever changes, regenerate it by
loading every unique `d` string into an SVG in a browser, calling
`getBBox()` on each, and re-running `build_diagram.py`.

## Editing the diagram (which muscle links to which page)

The body diagram itself is real anatomical path data, not hand-drawn shapes —
see **Credits** below. `build_diagram.py` has two tables you'll actually want
to touch:

- `MUSCLE_MAP` — maps each muscle's slug (e.g. `"quadriceps"`) to a
  `regions/<id>.html` page, or `None` to make it non-interactive (used for
  head/hair/hands — parts that aren't really "stretch" targets).
- `PAGE_LABELS` — the friendly name shown in the fallback link list under
  the diagram, per destination page.

After editing either table:

```bash
python3 build_diagram.py
```

To change the diagram's copy (header text, footer, script behavior), edit
`index.template.html` instead of `index.html`, then re-run the command above.

## Editing region page content

1. Edit `data/regions.json` — change a video ID, tweak the intro text, add a
   cause, etc.
2. Regenerate the pages:

   ```bash
   python3 generate.py
   ```

3. Refresh the browser.

## Adding a new region page

1. Add an entry to `data/regions.json` with a unique `id` plus `title`,
   `intro`, `causes`, and `videos` (YouTube video IDs — the part after
   `v=` in a YouTube URL).
2. Run `python3 generate.py`.
3. If a muscle on the diagram should link there, point it at the new id in
   `MUSCLE_MAP` inside `build_diagram.py`, then run `python3 build_diagram.py`.

Some pages built earlier (`hips`, `elbows`, `serratus-anterior`, `lats`)
aren't currently linked from the diagram because the underlying anatomical
data doesn't draw those as distinct shapes — the content is still there in
`regions/` if you want to wire one up later (e.g. map it onto a nearby
muscle's shape in `MUSCLE_MAP`).

## Running it locally

No build step or server required to just view it — open `index.html` in a
browser. For a local server (matches how relative links behave in
production):

```bash
python3 -m http.server 8000
```

then visit `http://localhost:8000`.

## Deploying

This is a plain static site, so any static host works, e.g. **GitHub
Pages**:

```bash
git init
git add .
git commit -m "Initial Stretch Finder site"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

Then enable GitHub Pages for the repo (Settings → Pages → deploy from
`main` branch, root folder).

## Credits

The body diagram's muscle shapes (`vendor/bodyFront.ts`, `vendor/bodyBack.ts`,
`vendor/SvgMaleWrapper.tsx`) are from
[react-native-body-highlighter](https://github.com/HichamELBSI/react-native-body-highlighter)
by Hicham El Abbassi, used under the MIT License — see `vendor/LICENSE`.
`build_diagram.py` converts that data into the plain SVG used on this site.

## Notes

- Videos are embedded via YouTube's standard `/embed/` iframe — no API key
  needed, but it does require an internet connection to actually load/play
  them.
- All video picks and copy are for general education, not medical advice
  (see the disclaimer on every page).
