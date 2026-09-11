import os
import requests
from bs4 import BeautifulSoup

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_token = os.environ.get("SLACK_BOT_TOKEN", None)
client = WebClient(token=slack_token)
channel = "#it-strategy"

def send_to_slack(msg):
    if not slack_token:
        print("❌ SLACK_BOT_TOKEN environment variable not set, not sending to Slack but would have sent the following to {channel}")
        print(msg)
        return

    client.api_test()
    try:
        client.chat_postMessage(channel=channel, text=msg)
    except SlackApiError as e:
        print(f"❌ Error sending message to Slack: {e.response['error']}")

def check_website():
    old_image = ""
    with open(".old-image", "r") as f:
        old_image = f.read().strip()

    res = requests.get("https://nsps.ca", headers={"User-Agent": "mod_security sucks"})
    res.raise_for_status()
    soup = BeautifulSoup(res.content, 'html.parser')
    hero = soup.find("figure").find("img")
    src = hero["src"]
    who = soup.find("figure").find("figcaption").next_element.strip()
    what = soup.find("figure").find("figcaption").next_element.next_element.text.strip()
    social_media = True if "SOCYes" in src else False

    if src == old_image:
        print("👍 Image hasn't changed.")
        
    elif not social_media:
        print("👍 Image has changed, but social media is set to `No`, so don't post.")
        msg = f"📣 The image on the website changed to {src} by **{who}**, titled **{what}**. However is *NOT* approved to post on social media, so please don't do that."
        send_to_slack(msg)

    elif social_media:
        print("✅ Image has changed, and social media is set to `Yes`, so let's share it.")
        msg = f"📣 The image on the website changed to {src} by **{who}**, titled **{what}** and has approval 👍 to post on social media ."
        send_to_slack(msg)

    with open(".old-image", "w") as f:
        f.write(src)

if __name__=="__main__":
    check_website()