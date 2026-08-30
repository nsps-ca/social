import os
from mastodon import Mastodon

mastodon_token = os.environ.get("MASTODON_TOKEN", None)

def send_mastodon(text, event):
    if mastodon_token:
        session = Mastodon(access_token="fbYYFSwAp05_LsH7NSAG-BvfVNJppbJiNhn85GxS4Is", api_base_url="https://mastodon.social")
        session.toot(text)
        print(f"✅ Mastodon post sent for: {event.DTSTART.strftime('%b %d')}.")
    else:
        print(text)
        print(f"❌ No mastodon token, not sent")

