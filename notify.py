import json
import os
import requests
import feedparser

RSS_URL = "https://wikiwiki.jp/2chpc-mine/::cmd/mixirss"
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

STATE_FILE = "state.json"

headers = {
    "User-Agent": "GitHub-Hookshot"
}

feed = feedparser.parse(requests.get(RSS_URL, headers=headers).text)

if not feed.entries:
    raise Exception("RSS取得失敗")

latest = feed.entries[0]

latest_id = latest.get("id", latest.link)

if not os.path.exists(STATE_FILE):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"latest": latest_id}, f)
    print("Initialized state.")
    exit(0)

with open(STATE_FILE, "r", encoding="utf-8") as f:
    state = json.load(f)

if state.get("latest") != latest_id:

    embed = {
        "title": "📝 Wiki更新",
        "url": latest.link,
        "description": latest.title,
        "fields": [
            {
                "name": "更新日時",
                "value": latest.get("dc_date", "不明"),
                "inline": False
            }
        ]
    }

    requests.post(
        WEBHOOK_URL,
        json={
            "embeds": [embed]
        }
    )

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"latest": latest_id}, f)