import requests
import icalendar
import datetime
import os
import sys
import argparse
from bsky_bridge import BskySession, post_text

bsky_token = os.environ.get("BSKY_TOKEN", None)
calendar_url = "https://nsps.ca/?post_type=tribe_events&ical=1&eventDisplay=list"
tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).date()

def get_calendar():
    headers = {"User-Agent": "mod_security sucks"}
    r = requests.get(calendar_url, headers=headers)
    return icalendar.Calendar.from_ical(r.text)

def get_events_from_calendar(day):
    target = day or tomorrow
    cal = get_calendar()
    for element in cal.walk():
        if isinstance(element, icalendar.cal.event.Event):
            if element.DTSTART.date() == target:
                send_bsky(element)

def send_bsky(event):
    text = f"""Join us tomorrow, {event.DTSTART.strftime('%b %d')}, for our next event 👉 {event.summary}

More information at https://nsps.ca
"""
    if bsky_token:
        session = BskySession("northshoreps.bsky.social", bsky_token)
        post_text(session, text)
        print(f"✅ Bluesky post sent for: {event.DTSTART.strftime('%b %d')}.")
    else:
        print(text)
        print(f"❌ No Bluesky token, not sent")

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--day')
    args = parser.parse_args()
    day = datetime.date.strptime(args.day, "%Y-%m-%d") if args.day else datetime.date.today()
    print(f"ℹ️ Looking for events for the day {day}")
    
    get_events_from_calendar(day)
