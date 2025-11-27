#!/usr/bin/env python3
"""
fetch_artworks.py
Download artwork images for every entry in artworks.json → ./images/artworks/…

How it works
------------
1. Wikipedia API  : get the Wikidata Q-id for the artwork page
2. Wikidata API   : fetch property P18 (image filename) for that Q-id
3. Commons file   : resolve File:… to a real image URL via Special:FilePath
4. Save locally   : mkdir -p images/artworks && write binary data

If anything fails we log and continue.
"""

import json
import os
import pathlib
import sys
import time
from urllib.parse import quote

import requests
from tqdm import tqdm

WIKI_API    = "https://en.wikipedia.org/w/api.php"
WIKIDATA_API = "https://www.wikidata.org/wiki/Special:EntityData/{}.json"
COMMONS_FILE = "https://commons.wikimedia.org/wiki/Special:FilePath/{}"

HEADERS = {"User-Agent": "TimelineBot/0.1 (https://github.com/timeline)"}

# Manual overrides for artworks that need specific Wikipedia page titles or direct Wikidata IDs
# Can also use direct URLs for problematic images
ARTWORK_OVERRIDES = {
    "Sistine Chapel Ceiling": "Sistine Chapel ceiling",
    "Basket of Fruit": "Basket of Fruit (Caravaggio)",
    "The Great Wave off Kanagawa": "The Great Wave off Kanagawa",
    "The Disquieting Muses": "The Disquieting Muses",
    "Nighthawks": "Nighthawks (Hopper)",
    "Liberty Leading the People": "Liberty Leading the People",
    "David with the Head of Goliath": "David with the Head of Goliath (Caravaggio)",
    "Self-Portrait with Thorn Necklace and Hummingbird": "Self-Portrait with Thorn Necklace and Hummingbird",
    "Ophelia": "Ophelia (painting)",
    "Irises": "Irises (painting)",
    "Girl with a Pearl Earring": "Girl with a Pearl Earring",
    "Wheat Field with Cypresses": "Wheat Field with Cypresses",
    "The Water Lily Pond": "Water Lilies (Monet)",
    "Vitruvian Man": "Vitruvian Man",
}

# Direct image URLs for artworks that can't be found via Wikidata or need specific versions
DIRECT_IMAGE_URLS = {
    "David with the Head of Goliath": "https://www.wikiart.org/en/caravaggio/david-with-the-head-of-goliath-1610/@@images/image/large",
    "Self-Portrait with Thorn Necklace and Hummingbird": "https://www.wikiart.org/en/frida-kahlo/self-portrait-with-thorn-necklace-and-hummingbird-1940/@@images/image/large",
    "The Disquieting Muses": "https://media.tate.org.uk/art/images/work/T/T00/T00900_10.jpg",
    "Irises": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Irises-Vincent_van_Gogh.jpg/800px-Irises-Vincent_van_Gogh.jpg",
}

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
    try:
        r = requests.get(WIKI_API, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
        pages = r.json()["query"]["pages"].values()
        for page in pages:
            return page.get("pageprops", {}).get("wikibase_item")  # e.g. "Q937"
    except Exception as e:
        print(f"Error fetching Wikipedia data: {e}")
    return None


def qid_to_image_filename(qid: str) -> str | None:
    """Return the Commons file name (e.g. 'Mona Lisa.jpg')."""
    try:
        r = requests.get(WIKIDATA_API.format(qid), headers=HEADERS, timeout=15)
        r.raise_for_status()
        entity = r.json()["entities"][qid]
        claims = entity["claims"]
        if "P18" not in claims:
            return None
        # Use the first image in P18
        return claims["P18"][0]["mainsnak"]["datavalue"]["value"]
    except Exception as e:
        print(f"Error fetching Wikidata: {e}")
    return None


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

    try:
        with requests.get(url, headers=HEADERS, stream=True, timeout=30) as r:
            r.raise_for_status()          # will now 302 → 200 instead of 404
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dest_path, "wb") as fp:
                for chunk in r.iter_content(chunk_size=8192):
                    fp.write(chunk)
        return True
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return False


# --------------------------------------------------------------------------- #
# Main script
# --------------------------------------------------------------------------- #
def download_direct_url(url: str, dest_path: pathlib.Path) -> bool:
    """Download image from a direct URL."""
    if dest_path.exists():
        return False
    
    try:
        with requests.get(url, headers=HEADERS, stream=True, timeout=30) as r:
            r.raise_for_status()
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dest_path, "wb") as fp:
                for chunk in r.iter_content(chunk_size=8192):
                    fp.write(chunk)
        return True
    except Exception as e:
        print(f"Error downloading from URL: {e}")
        return False


def main(json_path="artworks.json"):
    artworks = json.loads(pathlib.Path(json_path).read_text())
    saved, skipped, err = 0, 0, 0

    for artwork in tqdm(artworks, unit="artwork"):
        title = artwork["title"]
        out_path = pathlib.Path("." + artwork["image"])  # strip leading slash

        # Check if we have a direct URL first
        if title in DIRECT_IMAGE_URLS:
            try:
                if download_direct_url(DIRECT_IMAGE_URLS[title], out_path):
                    saved += 1
                    tqdm.write(f"✅ Downloaded (direct): {title}")
                else:
                    skipped += 1
                time.sleep(0.3)
                continue
            except Exception as e:
                tqdm.write(f"❌ {title} (direct): {e}")
                err += 1
                continue

        # Use override if available, otherwise use the title as-is
        wiki_title = ARTWORK_OVERRIDES.get(title, title)

        try:
            qid = wikipedia_to_qid(wiki_title)
            if not qid:
                tqdm.write(f"⚠️  {title}: no Wikidata Q-id");  err += 1;  continue

            filename = qid_to_image_filename(qid)
            if not filename:
                tqdm.write(f"⚠️  {title}: no P18 image");       err += 1;  continue

            if download_commons_file(filename, out_path):
                saved += 1
                tqdm.write(f"✅ Downloaded: {title}")
            else:
                skipped += 1  # already existed
            time.sleep(0.3)  # be polite to the APIs
        except Exception as e:
            tqdm.write(f"❌ {title}: {e}")
            err += 1

    print(f"\nDone: {saved} downloaded, {skipped} skipped, {err} errors.")


if __name__ == "__main__":
    # Change to src/lib/data directory where artworks.json should be
    script_dir = pathlib.Path(__file__).parent
    data_dir = script_dir.parent / "src" / "lib" / "data"
    
    if not data_dir.exists():
        sys.exit(f"Data directory not found: {data_dir}")
    
    os.chdir(data_dir)
    
    if not pathlib.Path("artworks.json").exists():
        sys.exit("artworks.json not found in src/lib/data directory.")
    
    main("artworks.json")

