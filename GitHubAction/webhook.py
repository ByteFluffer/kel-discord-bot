import requests
import json
import os

commit_name = os.getenv("commit_name")
webhook_url = "https://discord.com/api/webhooks/1105459494756044851/C6MCQdhtOMGgtZDEWQThGFulQt8VANmCdDNpUBLCHOpbGVAasHx06nF_-ZIopTUGFxX0"

data = {
    "name": "Kelvin",
    "content": str(commit_name)
    }

req = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
print(req)