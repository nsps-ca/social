import os
import requests
from bs4 import BeautifulSoup

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_token = os.environ.get("SLACK_BOT_TOKEN", None)
client = WebClient(token=slack_token)
channel = "#chat"


def send_to_slack(image):
    if not slack_token:
        print(
            "❌ SLACK_BOT_TOKEN environment variable not set, not sending to Slack but would have sent the following to {channel}"
        )
        print(msg)
        return

    summary = f"📣 Image has changed on the website to *{image['what']}* by *{image['who']}*"
    social = "⛔️ This image is *NOT* approved for posting on social media, so please don't do that."
    if social:
        social = "✅ This image is approved to share on NSPS social media accounts."
    blocks = [
        {"type": "section", "text": {"type": "mrkdwn", "text": summary}},
        {"type": "section", "text": {"type": "mrkdwn", "text": social}},
        {"type": "divider"},
        {
            "type": "image",
            "image_url": image["src"],
            "title": {
                "type": "plain_text",
                "text": f"{image['what']} by {image['who']}"
            },
            "alt_text": f"{image['what']} by {image['who']}"
        },
    ]
    client.api_test()
    try:
        client.chat_postMessage(channel=channel, text=summary, blocks=blocks)
    except SlackApiError as e:
        print(f"❌ Error sending message to Slack: {e.response['error']}")


def check_website():
    old_image = ""
    with open(".old-image", "r") as f:
        old_image = f.read().strip()

    res = requests.get("https://nsps.ca", headers={"User-Agent": "mod_security sucks"})
    res.raise_for_status()
    soup = BeautifulSoup(res.content, "html.parser")

    figure = soup.find("figure")
    caption = figure.find("figcaption")
    src = figure.find("img")["src"]

    data = {
        "src": src,
        "who": caption.next_element.strip(),
        "what": caption.next_element.next_element.text.strip(),
        "social": True if "SOCYes" in src else False,
    }
    if src == old_image:
        print("👍 Image hasn't changed.")

    else:
        send_to_slack(data)

    with open(".old-image", "w") as f:
        f.write(src)


if __name__ == "__main__":
    check_website()
