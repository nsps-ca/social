import requests
from bs4 import BeautifulSoup

old_image = ""
with open(".old-image", "r") as f:
    old_image = f.read().strip()

res = requests.get("https://nsps.ca", headers={"User-Agent": "mod_security sucks"})
res.raise_for_status()
soup = BeautifulSoup(res.content, 'html.parser')
hero = soup.find_all("img")[1]
src = hero["src"]
social_media = True if "SOCYes" in src else False

if src == old_image:
    print("Image hasn't changed.")
    
elif not social_media:
    print("Image has changed, but social media is set to `No`, so don't post.")

elif social_media:
    print("Image has changed, and social media is set to `Yes`, so let's share it.")

with open(".old-image", "w") as f:
    f.write(src)
