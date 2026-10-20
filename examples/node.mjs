// npm install apify-client
// APIFY_TOKEN=... node node.mjs [https://example.com] [screenshot|pdf|both]
const token = process.env.APIFY_TOKEN;
if (!token) {
  console.error('Error: APIFY_TOKEN is not set. Get a free token at https://console.apify.com/account/integrations');
  process.exit(1);
}

const { ApifyClient } = await import('apify-client');

const url = process.argv[2] || 'https://example.com';
const mode = process.argv[3] || 'screenshot';

const client = new ApifyClient({ token });
const run = await client.actor('pennydata/shot-pdf').call({ urls: [{ url }], mode, fullPage: true });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const item of items) {
  console.log(item.error ? `FAILED ${item.input}: ${item.error}` : item);
}
