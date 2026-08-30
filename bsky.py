import os
from bsky_bridge import BskySession, post_text

bsky_token = os.environ.get("BSKY_TOKEN", None)

def send_bsky(text, event):
    if bsky_token:
        session = BskySession("northshoreps.bsky.social", bsky_token)
        post_text(session, text)
        print(f"✅ Bluesky post sent for: {event.DTSTART.strftime('%b %d')}.")
    else:
        print(text)
        print(f"❌ No Bluesky token, not sent")

