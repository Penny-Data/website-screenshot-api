# Transcribe an audio or video URL to text and SRT with one API call (curl, Node, Python)

Speech-to-text without running Whisper yourself: send a link to an mp3, wav, m4a, ogg, flac, mp4 or webm file and get the text, timestamped segments and an SRT subtitle file back. [Audio Transcription](https://apify.com/pennydata/audio-transcriber) runs Whisper on Apify, so no OpenAI key is needed. Pricing is per audio minute (see the actor page for the current tiers); failed files are not charged.

## 1. Check the cost first (free dry run)

`estimateOnly` reads the duration of each file and returns the estimated cost without transcribing anything.

```bash
curl -s -X POST \
  "https://api.apify.com/v2/acts/pennydata~audio-transcriber/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"urls":["https://upload.wikimedia.org/wikipedia/commons/6/62/Weekly_Address-_Celebrating_Independence_Day.webm"],"estimateOnly":true}'
```

## 2. Transcribe (curl)

```bash
curl -s -X POST \
  "https://api.apify.com/v2/acts/pennydata~audio-transcriber/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"urls":["https://upload.wikimedia.org/wikipedia/commons/6/62/Weekly_Address-_Celebrating_Independence_Day.webm"],"outputFormats":["text","srt"],"maxMinutesPerFile":10}'
```

## Node.js

```js
const res = await fetch(
  `https://api.apify.com/v2/acts/pennydata~audio-transcriber/run-sync-get-dataset-items?token=${process.env.APIFY_TOKEN}`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      urls: ['https://upload.wikimedia.org/wikipedia/commons/6/62/Weekly_Address-_Celebrating_Independence_Day.webm'],
      outputFormats: ['text', 'srt'],
      maxCostUsd: 0.5, // spending guard: a file that would exceed it is skipped and the run stops
    }),
  },
);
const rows = await res.json();
for (const r of rows) console.log(r.text);
```

## Python

```python
import os, requests

r = requests.post(
    "https://api.apify.com/v2/acts/pennydata~audio-transcriber/run-sync-get-dataset-items",
    params={"token": os.environ["APIFY_TOKEN"]},
    json={
        "urls": ["https://upload.wikimedia.org/wikipedia/commons/6/62/Weekly_Address-_Celebrating_Independence_Day.webm"],
        "outputFormats": ["text", "srt"],
    },
    timeout=300,
)
for row in r.json():
    print(row["text"])
```

## What comes back

One dataset row per file with `text`, `segments` (`start` and `end` in seconds), `durationSeconds` and a link to the SRT file. First segments from a real run on the public 2 min 51 s video above:

| start | end | text |
|---|---|---|
| 0 | 13 | I hope you all had a safe and happy Fourth of July filled with parades and cookouts, fireworks, |
| 13 | 15.6 | and family reunions. |
| 15.6 | 19 | We celebrated the White House with a few members of the military and their families. |

## Useful options

- `translateToEnglish: true` outputs English text from other languages; `language` fixes the spoken language instead of auto-detect.
- `wordTimestamps: true` adds per-word start/end times; `outputFormats: ["vtt"]` gives WebVTT.
- `generateChapters: true` adds chapter lines you can paste into a YouTube or podcast description (extra per-file charge, see the actor page).
- `feedUrl` with `maxEpisodes` transcribes the newest episodes of a podcast RSS feed; `onlyNewSinceLastRun: true` makes it safe to schedule daily.
- Speaker labels are not supported: the transcript has no speaker names. Long runs use the small `tiny` model by default (`model: "base"` with `autoModel: false` is more accurate, same price).

I built this actor and earn from its runs. Written with AI assistance (Claude).
