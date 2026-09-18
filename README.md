This repository provides code to do stuff with social media.

### Mastodon

`mstdn.py` is a script that reads the next event and posts it to the NSPS Mastodon account: https://mastodon.social/@nsps

### Bluesky

`bsky.py` is a script that reads the next event and posts it to the NSPS Bluesky account: https://bsky.app/profile/northshoreps.bsky.social

### Web

`web.py` is a script that detects changes on the website and posts it to Slack, so that others can post it on to the relevant social media accounts, such as Mastodon and Bluesky above.

All these scripts are triggered daily by the GitHub Actions contained in this repository.