# Website Screenshot API & URL to PDF API

A simple **website screenshot API** and **URL to PDF API** built on headless Chromium. Send a list of URLs (or raw HTML), get back full-page screenshots (PNG/JPEG) and/or PDFs. Bulk, pay per result, failed pages are never billed.

It runs as the [`pennydata/shot-pdf`](https://apify.com/pennydata/shot-pdf) Actor on the Apify platform, so you call it over plain HTTP, with the Node or Python Apify client, or from the Apify Console with no code.

- Full-page website screenshot, or viewport only
- URL to PDF (A4, Letter, landscape, print backgrounds)
- HTML to PDF from inline HTML strings
- Height limit, clip region, hide sticky headers/cookie bars, lazy-load scrolling
- Bulk: many URLs per call, concurrent
- Failed URLs return an error row and cost nothing

**Actor page:** https://apify.com/pennydata/shot-pdf

## Pricing

Pay per successful result (Apify pay-per-event, Free plan prices; paid Apify plans get lower per-event prices):

| Output | Price |
| --- | --- |
| Screenshot captured | $0.001 each ($1 per 1,000) |
| PDF rendered | $0.004 each ($4 per 1,000) |
| Mode `both` | screenshot + PDF |

There is also a tiny per-run start fee ($0.00005 per GB of memory). Failed captures are not charged. Check the [actor page](https://apify.com/pennydata/shot-pdf) for current prices. An Apify account is free to create and includes monthly free platform credit.

## Quick start

Get an API token at https://console.apify.com/account/integrations and export it:

```bash
export APIFY_TOKEN=your_token_here
```

### curl: website screenshot API

```bash
curl -X POST "https://api.apify.com/v2/acts/pennydata~shot-pdf/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"urls":[{"url":"https://example.com"}],"mode":"screenshot","fullPage":true}'
```

### curl: URL to PDF API

```bash
curl -X POST "https://api.apify.com/v2/acts/pennydata~shot-pdf/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"urls":[{"url":"https://en.wikipedia.org/wiki/Web_scraping"}],"mode":"pdf","pdfFormat":"A4"}'
```

Each response item looks like:

```json
{
  "input": "https://example.com",
  "finalUrl": "https://example.com/",
  "httpStatus": 200,
  "title": "Example Domain",
  "screenshotUrl": "https://api.apify.com/v2/key-value-stores/.../records/...",
  "pdfUrl": null,
  "error": null
}
```

`screenshotUrl` / `pdfUrl` point to files stored in the run's key-value store. Download them with your token.

### Node.js (apify-client)

```bash
npm install apify-client
APIFY_TOKEN=... node examples/node.mjs https://example.com screenshot
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('pennydata/shot-pdf').call({
  urls: [{ url: 'https://example.com' }],
  mode: 'pdf',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### Python

```bash
pip install requests
APIFY_TOKEN=... python examples/python_example.py https://example.com pdf
```

```python
import os, requests

resp = requests.post(
    "https://api.apify.com/v2/acts/pennydata~shot-pdf/run-sync-get-dataset-items",
    params={"token": os.environ["APIFY_TOKEN"]},
    json={"urls": [{"url": "https://example.com"}], "mode": "screenshot"},
    timeout=300,
)
print(resp.json())
```

Without `APIFY_TOKEN` the example scripts exit immediately with a clear error and make no request.

## Input reference

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `urls` | array | | Public http(s) pages: `[{"url": "..."}]` |
| `htmlDocuments` | string[] | | Inline HTML to render (HTML to PDF / screenshot) |
| `mode` | `screenshot` \| `pdf` \| `both` | `screenshot` | What to produce |
| `format` | `png` \| `jpeg` | `png` | Screenshot format |
| `fullPage` | boolean | `true` | Capture the whole scrollable page |
| `maxHeight` | integer | `0` | Crop full-page screenshots to this many px (0 = no limit) |
| `clip` | object | | Region `{"x":0,"y":0,"width":1280,"height":720}` |
| `hideFixedElements` | boolean | `true` | Make sticky headers, cookie bars, chat widgets static |
| `scrollTimeoutSecs` | integer | `10` | Scroll to trigger lazy-loaded images |
| `viewportWidth` / `viewportHeight` | integer | `1280` / `800` | Browser viewport |
| `waitUntil` | `load` \| `domcontentloaded` \| `networkidle` | `load` | Page event to wait for |
| `delayMs`, `waitForSelector` | | | Extra waiting before capture |
| `pdfFormat`, `pdfLandscape`, `pdfPrintBackground` | | | PDF paper options |
| `maxConcurrency`, `maxRetries` | integer | | Throughput and retry control |

Ready-to-use input files: [`examples/input-screenshot.json`](examples/input-screenshot.json), [`examples/input-pdf.json`](examples/input-pdf.json), [`examples/input-html-to-pdf.json`](examples/input-html-to-pdf.json). The full schema is on the [actor page](https://apify.com/pennydata/shot-pdf/input-schema).

## Use cases

Link previews and thumbnails, visual regression snapshots, archiving pages as PDF, invoices and reports from HTML, SEO and uptime evidence, bulk website screenshots for lead lists.

## Notes

- Only capture pages you are allowed to capture; respect the target site's terms.
- Prices and limits are set on the Apify actor page and may change; that page is the source of truth.

## AI-built disclosure

This repository and the underlying Actor were built and are maintained by an AI-assisted workflow (Claude), operated by the owner of the `jjlarsensa` GitHub account and the `pennydata` Apify account. Examples were checked for the no-token error path; run them yourself before depending on them.

## License

MIT, see [LICENSE](LICENSE). The README, examples and landing page are MIT; the Actor itself is a hosted service on Apify.

[Catalog of all pennydata actors](catalog.md)
