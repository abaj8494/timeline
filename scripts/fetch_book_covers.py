#!/usr/bin/env python3
"""
fetch_book_covers.py
Download book-cover images for every entry in books.json → ./images/books/…

Sources
-------
1. Open Library search  (fast, usually has modern covers)
2. Wikipedia → Wikidata → P18 fallback
3. Manual URL overrides for very old works

Author: Shrine Timeline project
"""

import json
import os
import pathlib
import time
from urllib.parse import quote, urlencode

import requests
from tqdm import tqdm

# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #
HEADERS = {"User-Agent": "TimelineBot/0.2 (https://github.com/timeline)"}

OPENLIB_SEARCH = "https://openlibrary.org/search.json"
OPENLIB_COVER  = "https://covers.openlibrary.org/b/id/{id}-L.jpg"   # L = ~600 px tall

WIKI_API      = "https://en.wikipedia.org/w/api.php"
WIKIDATA_API  = "https://www.wikidata.org/wiki/Special:EntityData/{}.json"
COMMONS_FILE  = "https://commons.wikimedia.org/wiki/Special:FilePath/{}"

# Manual last-resort images (URL → local filename)
URL_OVERRIDES = {
    "Plato's Dialogues": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Platon_Complete_Works_1903.jpg/512px-Platon_Complete_Works_1903.jpg",
    "Shakespeare's First Folio": "https://upload.wikimedia.org/wikipedia/commons/7/79/FirstFolioShakespeare.jpg",
}

# --------------------------------------------------------------------------- #
# Helper functions (re-use from your portrait script + a few new ones)
# --------------------------------------------------------------------------- #
def wikipedia_to_qid(title: str) -> str | None:
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
        return page.get("pageprops", {}).get("wikibase_item")
    return None


def qid_to_image_filename(qid: str) -> str | None:
    r = requests.get(WIKIDATA_API.format(qid), headers=HEADERS, timeout=15)
    r.raise_for_status()
    entity = r.json()["entities"][qid]
    claims = entity["claims"]
    if "P18" not in claims:
        return None
    return claims["P18"][0]["mainsnak"]["datavalue"]["value"]


def download_commons_file(filename: str, dest_path: pathlib.Path) -> bool:
    if dest_path.exists():
        return False
    fname = filename.replace(" ", "_")
    safe = "_().'-"
    url = COMMONS_FILE.format(quote(fname, safe=safe))
    return _stream_to_file(url, dest_path)


def openlibrary_cover(title: str, author: str) -> str | None:
    """Return full cover URL or None."""
    params = {"title": title, "author": author, "limit": 1}
    r = requests.get(OPENLIB_SEARCH, params=params, headers=HEADERS, timeout=15)
    r.raise_for_status()
    docs = r.json().get("docs")
    if not docs:
        return None
    cover_id = docs[0].get("cover_i")
    if cover_id:
        return OPENLIB_COVER.format(id=cover_id)
    return None


def _stream_to_file(url: str, dest_path: pathlib.Path) -> bool:
    with requests.get(url, headers=HEADERS, stream=True, timeout=30) as r:
        r.raise_for_status()
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "wb") as fp:
            for chunk in r.iter_content(chunk_size=8192):
                fp.write(chunk)
    return True

# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main(json_path="books.json"):
    books = json.loads(pathlib.Path(json_path).read_text())
    saved, skipped, err = 0, 0, 0

    for book in tqdm(books, unit="book"):
        title   = book["title"]
        author  = book["author"]
        outpath = pathlib.Path("." + book["image"])  # strip leading slash

        # 1) Manual override?
        if title in URL_OVERRIDES:
            try:
                if _stream_to_file(URL_OVERRIDES[title], outpath):
                    saved += 1
                else:
                    skipped += 1
                continue
            except Exception as e:
                tqdm.write(f"❌ {title}: {e}")
                err += 1
                continue

        # 2) Try Open Library
        try:
            cover_url = openlibrary_cover(title, author)
            if cover_url:
                if _stream_to_file(cover_url, outpath):
                    saved += 1
                else:
                    skipped += 1
                time.sleep(0.2)
                continue  # success
        except Exception as e:
            tqdm.write(f"⚠️  OpenLibrary failed for {title}: {e}")

        # 3) Fallback: Wikipedia → Wikidata → P18
        try:
            qid = wikipedia_to_qid(title)
            if not qid:
                tqdm.write(f"⚠️  {title}: no Wikidata Q-id");  err += 1;  continue

            filename = qid_to_image_filename(qid)
            if not filename:
                tqdm.write(f"⚠️  {title}: no P18 image");       err += 1;  continue

            if download_commons_file(filename, outpath):
                saved += 1
            else:
                skipped += 1
        except Exception as e:
            tqdm.write(f"❌ {title}: {e}")
            err += 1

        time.sleep(0.3)  # gentle on APIs

    print(f"\nDone: {saved} downloaded, {skipped} skipped, {err} errors.")


if __name__ == "__main__":
    if not pathlib.Path("books.json").exists():
        raise SystemExit("books.json not found in current directory.")
    main()

