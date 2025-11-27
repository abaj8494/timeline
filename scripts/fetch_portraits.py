#!/usr/bin/env python3
"""
fetch_portraits.py
Download portrait images for every person in people.json -→ ./images/people/…

How it works
------------
1. Wikipedia API  : get the Wikidata Q-id for the page about <name>
2. Wikidata API   : fetch property P18 (image filename) for that Q-id
3. Commons file   : resolve File:… to a real image URL via Special:FilePath
4. Save locally   : mkdir -p images/people && write binary data

If anything fails we log and continue.
"""

import json
import os
import pathlib
import sys
import time
from urllib.parse import quote_plus

import requests
from tqdm import tqdm

WIKI_API    = "https://en.wikipedia.org/w/api.php"
WIKIDATA_API = "https://www.wikidata.org/wiki/Special:EntityData/{}.json"
COMMONS_FILE = "https://commons.wikimedia.org/wiki/Special:FilePath/{}"

HEADERS = {"User-Agent": "TimelineBot/0.1 (https://github.com/timeline)"}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def wikipedia_to_qid(title: str) -> str | None:
    """Return the Wikidata Q-identifier for a Wikipedia page title."""
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "pageprops",
        "redirects": 1,
    }
    r = requests.get(WIKI_API, params=params, headers=HEADERS, timeout=15)
    r.raise_for_status()
    pages = r.json()["query"]["pages"].values()
    for page in pages:
        return page.get("pageprops", {}).get("wikibase_item")  # e.g. "Q937"
    return None


def qid_to_image_filename(qid: str) -> str | None:
    """Return the Commons file name (e.g. 'Albert Einstein Head.jpg')."""
    r = requests.get(WIKIDATA_API.format(qid), headers=HEADERS, timeout=15)
    r.raise_for_status()
    entity = r.json()["entities"][qid]
    claims = entity["claims"]
    if "P18" not in claims:
        return None
    # Use the first image in P18
    return claims["P18"][0]["mainsnak"]["datavalue"]["value"]

from urllib.parse import quote  # swap quote_plus → quote

def download_commons_file(filename: str, dest_path: pathlib.Path) -> bool:
    """
    Resolve image via Special:FilePath and stream to dest_path.
    Returns True if saved, False if already on disk.
    """
    if dest_path.exists():
        return False

    # 1. MediaWiki expects underscores, not spaces
    fname = filename.replace(" ", "_")

    # 2. URL-encode *except* underscores, parentheses, apostrophes, dots, dashes
    #    (keeps filenames readable and avoids double-encoding)
    safe = "_().'-"
    url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(fname, safe=safe)}"

    with requests.get(url, headers=HEADERS, stream=True, timeout=30) as r:
        r.raise_for_status()          # will now 302 → 200 instead of 404
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "wb") as fp:
            for chunk in r.iter_content(chunk_size=8192):
                fp.write(chunk)
    return True


# --------------------------------------------------------------------------- #
# Main script
# --------------------------------------------------------------------------- #
def main(json_path="people.json"):
    people = json.loads(pathlib.Path(json_path).read_text())
    saved, skipped, err = 0, 0, 0

    for person in tqdm(people, unit="person"):
        title = person["name"]
        out_path = pathlib.Path("." + person["image"])  # strip leading slash

        try:
            qid = wikipedia_to_qid(title)
            if not qid:
                tqdm.write(f"⚠️  {title}: no Wikidata Q-id");  err += 1;  continue

            filename = qid_to_image_filename(qid)
            if not filename:
                tqdm.write(f"⚠️  {title}: no P18 image");       err += 1;  continue

            if download_commons_file(filename, out_path):
                saved += 1
            else:
                skipped += 1  # already existed
            time.sleep(0.3)  # be polite to the APIs
        except Exception as e:
            tqdm.write(f"❌ {title}: {e}")
            err += 1

    print(f"\nDone: {saved} downloaded, {skipped} skipped, {err} errors.")



# --- BEGIN MANUAL PATCH -------------------------------------------------------
# Adds: Thales of Miletus, Carl Jung

from pathlib import Path

# 1) Map the JSON `name` → an *unambiguous* Wikipedia title or → a Wikidata Q-id.
OVERRIDE_LOOKUP = {
    # earlier fixes
    "Zeno":        "Zeno of Elea",            # page title ≈ Q132157
    "Seneca":      "Lucius Annaeus Seneca",   # ≈ Q2054
    "Newton":      "Isaac Newton",            # ≈ Q935
    "Charles Dodgson / Lewis Carroll": "Lewis Carroll",  # ≈ Q185764
    # NEW
    "Thales":      "Thales of Miletus",       # ≈ Q9334
    "Carl Jung":   "Carl Jung",               # ≈ Q135613
}

# 2) Local filenames that match your JSON `image` paths
LOCAL_PATH = {
    **{
        "Zeno":      Path("images/people/zeno.jpg"),
        "Seneca":    Path("images/people/seneca.jpg"),
        "Newton":    Path("images/people/newton.jpg"),
        "Charles Dodgson / Lewis Carroll": Path("images/people/carroll.jpg"),
    },
    # NEW
    "Thales":      Path("images/people/thales.jpg"),
    "Carl Jung":   Path("images/people/jung.jpg"),
}

for raw_name, override in OVERRIDE_LOOKUP.items():
    try:
        # override may be a page title *or* a ready Q-id
        if override.startswith("Q"):
            qid = override
        else:
            qid = wikipedia_to_qid(override)
        if not qid:
            print(f"⚠️  {raw_name}: could not resolve Q-id");  continue

        filename = qid_to_image_filename(qid)
        if not filename:
            print(f"⚠️  {raw_name}: no P18 image on Wikidata");  continue

        saved = download_commons_file(filename, LOCAL_PATH[raw_name])
        verb  = "Downloaded" if saved else "Exists"
        print(f"✅ {verb} {raw_name} → {LOCAL_PATH[raw_name]}")
    except Exception as e:
        print(f"❌ {raw_name}: {e}")
# --- END MANUAL PATCH ---------------------------------------------------------

if __name__ == "__main__":
    if not pathlib.Path("people.json").exists():
        sys.exit("people.json not found in current directory.")
    #main("people.json")

