import requests
import icalendar
import datetime
import os
import sys
import argparse
from bsky_bridge import BskySession, post_text

from mstdn import send_mastodon
from bsky import send_bsky

calendar_url = "https://nsps.ca/?post_type=tribe_events&ical=1&eventDisplay=list"
tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).date()

def get_calendar():
    headers = {"User-Agent": "mod_security sucks"}
    r = requests.get(calendar_url, headers=headers)
    return icalendar.Calendar.from_ical(r.text)


def get_events_from_calendar(day):
    events = []
    target = day or tomorrow
    cal = get_calendar()
    for element in cal.walk():
        if isinstance(element, icalendar.cal.event.Event):
            if element.DTSTART.date() == target:
                events.append(element)
    
    return events

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--day')
    args = parser.parse_args()
    day = datetime.date.strptime(args.day, "%Y-%m-%d") if args.day else tomorrow
    print(f"ℹ️ Looking for events for the day {day}")
    
    events = get_events_from_calendar(day)
    for event in events:
        text = f"""Join us tomorrow, {event.DTSTART.strftime('%b %d')}, for our next event 👉 {event.summary}

More information at https://nsps.ca
"""
        send_bsky(text, event)
        send_mastodon(text, event)