# pip install requests
# APIFY_TOKEN=... python python_example.py [https://example.com] [screenshot|pdf|both]
import os
import sys

import requests

token = os.environ.get("APIFY_TOKEN")
if not token:
    sys.exit("Error: APIFY_TOKEN is not set. Get a free token at https://console.apify.com/account/integrations")

url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
mode = sys.argv[2] if len(sys.argv) > 2 else "screenshot"

resp = requests.post(
    "https://api.apify.com/v2/acts/pennydata~shot-pdf/run-sync-get-dataset-items",
    params={"token": token},
    json={"urls": [{"url": url}], "mode": mode, "fullPage": True},
    timeout=300,
)
resp.raise_for_status()
for item in resp.json():
    print(item.get("pdfUrl") or item.get("screenshotUrl") or item.get("error"))
