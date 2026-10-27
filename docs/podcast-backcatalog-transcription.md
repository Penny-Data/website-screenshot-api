# Transcribe your whole podcast back catalog to text + SRT, done for you

You have a podcast feed with dozens of episodes and no transcripts. Send us the RSS URL and get every episode back as a text file and an SRT subtitle file, plus one combined CSV.

## Pick a size (fixed price, paid by card through Stripe)

| Tier | Covers | Price | Delivery |
|---|---|---|---|
| Starter | up to 20 episodes, up to 20 hours of audio in total | **29 USD**: https://buy.stripe.com/dRm3cn2SB4jedYz3IE7EQ07 | within 48 hours of payment |
| Standard | up to 60 episodes, up to 60 hours | **79 USD**: https://buy.stripe.com/14AfZ91Ox2b69Ij5QM7EQ08 | within 5 days |
| Full catalog | up to 150 episodes, up to 150 hours | **149 USD**: https://buy.stripe.com/9B66oz9gZ3facUvfrm7EQ09 | within 10 days |

Longer than your tier? Pay for the next tier up, or ask by email first: pennydata@proton.me.

## What you get

- Per episode: `.txt` (full text), `.srt` (timed subtitles).
- One `catalog.csv`: episode title, publish date, duration, word count, text.
- Sent as a download link to your checkout email.

## How it works

After paying, enter your podcast RSS feed URL in the checkout box. We run our open Apify actor [`pennydata/audio-transcriber`](https://apify.com/pennydata/audio-transcriber) (Whisper speech recognition) on the feed, newest episodes first, and send the files. English works best; other languages are possible but check the actor page first.

## Real example output

Source: *The Adventures of Pinocchio*, chapter 1, a LibriVox public-domain recording ([archive.org](https://archive.org/details/adventures_pinocchio_librivox)), 5 minutes, 832 words, transcribed by this actor:

```
1
00:00:20,000 --> 00:00:27,000
The Adventures of Pinocchio by C. Colody, translated by Carol Delac yesa.

2
00:00:27,000 --> 00:00:35,000
Chapter 1. How it happened that Master of Cherry, carpenter found a piece of wood that

3
00:00:35,000 --> 00:00:46,600
worked and laughed like a child. centuries ago they lived. A king, my little readers, will say immediately. No children, you are mistaken.
```

Note the misspelled names ("Colody", "Delac yesa"): this is raw machine output, not proofread. Audio: LibriVox recordings are public domain.

## How this compares

| Option | Price | Catch |
|---|---|---|
| Rev human transcript | 1.99 USD per minute (about 119 USD per hour of audio), [rev.com/pricing](https://www.rev.com/pricing) | ~99% accuracy, but a 20-hour show costs ~2,400 USD |
| Rev AI API (Whisper Large) | 0.005 USD per minute, [rev.ai/pricing](https://www.rev.ai/pricing) | Cheapest, but you write the code and handle the files yourself |
| Otter Pro | 16.99 USD per user per month, monthly plan, [otter.ai/pricing](https://otter.ai/pricing) | Monthly minute allowance, built for meetings; you upload files by hand |
| **This page** | 29 USD for 20 hours | Machine accuracy, no proofreading, done for you |

Our tier price covers the work of feeding your feed through, checking that every episode came back, and packaging the files. If you can write a script, the API route is cheaper.

## Honest limits

- Machine transcription, not proofread. Expect errors in names, jargon and music-heavy or noisy audio. No speaker labels.
- Feeds must be public. Private/paywalled feeds, and audio you do not have the right to transcribe, are out.
- Our actor currently runs a small, fast Whisper model, a bit slower than real time, which is why larger tiers take longer.
- **Refund:** full refund if the files are not delivered within the stated time, or if most of the text is unusable. Reply to the receipt email.

I run this service and earn from the actor's runs. Written with AI assistance (Claude); fulfilment is run by an AI agent for the PennyData account.