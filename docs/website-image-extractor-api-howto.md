# Download every image from a web page with one API call (curl, Node, Python)

Grabbing all the images from a page usually means writing a scraper, resolving `srcset`, de-duplicating, and then downloading each file. [Website Image Extractor](https://apify.com/pennydata/website-image-extractor) does that behind one HTTP call: give it page URLs, get one row per unique image (and optionally the files themselves in a key-value store).

It reads `<img src>`, `srcset` (largest candidate), `<picture><source>`, `og:image`/`twitter:image`, and optionally CSS `background-image`. It uses plain HTTP, so there is no JavaScript rendering.

## curl

Get an API token from your Apify account settings, then:

```bash
curl -s -X POST \
  "https://api.apify.com/v2/acts/pennydata~website-image-extractor/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startUrls":[{"url":"https://en.wikipedia.org/wiki/Cat"}],"maxImages":3,"fetchMetadata":false}'
```

## Node.js

```js
const res = await fetch(
  `https://api.apify.com/v2/acts/pennydata~website-image-extractor/run-sync-get-dataset-items?token=${process.env.APIFY_TOKEN}`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      startUrls: [{ url: 'https://en.wikipedia.org/wiki/Cat' }],
      maxImages: 100,
      minWidth: 300,       // skip icons and tracking pixels
      sameDomainOnly: false,
    }),
  },
);
const rows = await res.json();
for (const r of rows.filter((r) => r.status === 'ok')) console.log(r.imageUrl);
```

## Python

```python
import os, requests

url = ("https://api.apify.com/v2/acts/pennydata~website-image-extractor/"
       "run-sync-get-dataset-items")
rows = requests.post(
    url,
    params={"token": os.environ["APIFY_TOKEN"]},
    json={"startUrls": [{"url": "https://en.wikipedia.org/wiki/Cat"}],
          "maxImages": 100, "minWidth": 300},
    timeout=300,
).json()

for r in rows:
    if r.get("status") == "ok":
        print(r["imageUrl"], r.get("alt"))
```

## Real output

This is the actual dataset from a run with `maxImages: 3` on the Wikipedia "Cat" page plus a deliberately bad URL (trimmed to the first rows):

```json
[
  {
    "status": "error",
    "pageUrl": "https://nonexistent.invalid/",
    "error": "Only public http(s) URLs are supported",
    "note": "Not charged."
  },
  {
    "status": "ok",
    "pageUrl": "https://en.wikipedia.org/wiki/Cat",
    "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/2/25/Siam_lilacpoint.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=thumbnail_unscaled",
    "alt": null, "width": null, "height": null,
    "contentType": null, "bytes": null,
    "source": "og:image"
  },
  {
    "status": "ok",
    "pageUrl": "https://en.wikipedia.org/wiki/Cat",
    "imageUrl": "https://en.wikipedia.org/static/images/footer/wikimedia-button.svg",
    "source": "picture-source"
  }
]
```

`contentType` and `bytes` are null here because that run had `fetchMetadata: false`. With it on (the default) the actor sends one HEAD request per image to fill them in. The `source` field tells you where each image came from, which is handy for dropping footer badges.

## Downloading the files, not just URLs

Set `"downloadToKvs": true` and every image (up to 10 MB each) is saved to the run's key-value store, with `kvsKey` and `kvsUrl` added to each row. For a plain list of file URLs, a CSV, or a dataset, use `"mode": "files"` instead, optionally with `"createZip": true` to get one `files.zip`.

## Useful knobs

- `maxPagesPerStart`: follow same-site links, up to 50 pages per start URL.
- `minWidth` / `minBytes`: filter out small images. Images with unknown size are kept.
- `includeCssBackgrounds`: also collect `url()` images from inline styles and `<style>` blocks.
- `maxImages`: a hard cap on how many image rows (and so how much) a run can produce.

## Honest limits

- No browser: images injected by JavaScript after page load, lazy-loaders that keep the real URL only in JS, and pages behind a login will be missed.
- External stylesheets are not read for CSS backgrounds.
- `width`/`height` are only what the page declares; they are not measured from the file.
- It respects robots.txt by default, and pages that are blocked or fail return no billable rows.
- You are responsible for having the right to download and reuse the images you collect.

Prices and options are on the [actor page](https://apify.com/pennydata/website-image-extractor); questions or missing features can go to the actor's Issues tab.


I built this and earn from its runs. Written with AI assistance (Claude).