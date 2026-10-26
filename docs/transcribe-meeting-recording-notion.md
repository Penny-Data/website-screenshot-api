# Transcribe a public meeting or Zoom recording URL and push the text to Notion (Apify webhook, Node.js)

Disclosure: I publish the Apify actor used here ([Audio Transcriber](https://apify.com/pennydata/audio-transcriber)) and earn a fee when it runs. This page was written with AI help (Claude).

Use case: a recording is available at a direct file URL (a public Zoom cloud share download link, a Drive/S3/Dropbox direct link, a council-meeting mp4). You want the transcript to land in a Notion page without opening anything by hand.

Limits: the actor needs the media file itself (mp3, wav, m4a, ogg, mp4, webm, mov). A Zoom share page or YouTube page is not a file; use its direct download link. Only transcribe recordings you have the right to process.

## 1. Start a run with a webhook

```js
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

await client.actor('pennydata/audio-transcriber').start(
  { urls: ['https://example.com/recordings/board-meeting.mp4'], language: 'auto', maxCostUsd: 2 },
  { webhooks: [{
      eventTypes: ['ACTOR.RUN.SUCCEEDED'],
      requestUrl: 'https://your-server.example.com/apify-done',
  }] },
);
```

`maxCostUsd` caps spend. Pricing is per audio minute with the first 2 minutes of each run free; the current rate is on the [actor page](https://apify.com/pennydata/audio-transcriber).

## 2. Receive the webhook and write to Notion

```js
import express from 'express';
import { ApifyClient } from 'apify-client';

const app = express();
app.use(express.json());
const apify = new ApifyClient({ token: process.env.APIFY_TOKEN });

app.post('/apify-done', async (req, res) => {
  res.sendStatus(200);
  const { defaultDatasetId } = req.body.resource;
  const { items } = await apify.dataset(defaultDatasetId).listItems();
  for (const row of items) {
    if (!row.text) continue;                      // failed/skipped rows carry no text
    await fetch('https://api.notion.com/v1/pages', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${process.env.NOTION_TOKEN}`,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        parent: { database_id: process.env.NOTION_DB },
        properties: { Name: { title: [{ text: { content: row.title ?? row.audioUrl ?? 'Transcript' } }] } },
        // Notion limits one text block to 2000 chars
        children: row.text.match(/[\s\S]{1,1900}/g).slice(0, 90).map(chunk => ({
          object: 'block', type: 'paragraph',
          paragraph: { rich_text: [{ type: 'text', text: { content: chunk } }] },
        })),
      }),
    });
  }
});
app.listen(3000);
```

For Google Sheets, replace the `fetch` with a `sheets.spreadsheets.values.append` call (one row per transcript; cells cap at 50,000 characters).

## What I did not test

- Neither script was run end to end. Field names (`text`, `title`, `audioUrl`) follow the actor's dataset rows; confirm them on the run's Output tab first.
- The webhook payload shape (`resource.defaultDatasetId`) is from Apify's webhook docs; the Notion call follows Notion's create-page API.
- Whisper is weaker with crosstalk, music and accents; timestamps can drift by a second or two; no speaker labels.
