#!/usr/bin/env python3
"""
add_person.py
Interactive script to add new people to the shrine timeline.

Usage: python add_person.py
"""

import json
import os
import pathlib
import re
import sys
import time
from urllib.parse import quote

import requests
from tqdm import tqdm

# Import the existing portrait fetching functions
# Reuse the existing infrastructure from patch.py
WIKI_API = "https://en.wikipedia.org/w/api.php"
WIKIDATA_API = "https://www.wikidata.org/wiki/Special:EntityData/{}.json"
COMMONS_FILE = "https://commons.wikimedia.org/wiki/Special:FilePath/{}"
HEADERS = {"User-Agent": "ShrineTimelineBot/0.2 (https://github.com/shrine)"}

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
            return page.get("pageprops", {}).get("wikibase_item")
    except Exception as e:
        print(f"Error fetching Wikipedia data: {e}")
    return None

def qid_to_image_filename(qid: str) -> str | None:
    """Return the Commons file name (e.g. 'Albert Einstein Head.jpg')."""
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

def download_commons_file(filename: str, local_path: pathlib.Path) -> bool:
    """Download a file from Wikimedia Commons."""
    if local_path.exists():
        print(f"Image already exists: {local_path}")
        return False
    
    try:
        # Ensure directory exists
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Download from Commons
        url = COMMONS_FILE.format(quote(filename))
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        
        # Save file
        with open(local_path, 'wb') as f:
            f.write(r.content)
        
        print(f"Downloaded: {local_path}")
        return True
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return False

def validate_year(year_str: str) -> int | None:
    """Validate and convert year string to integer, handling BC years."""
    if not year_str:
        return None
    
    year_str = year_str.strip()
    if not year_str:
        return None
    
    # Handle BC years
    if year_str.lower().endswith('bc') or year_str.lower().endswith('bce'):
        try:
            year = int(re.sub(r'[^\d]', '', year_str))
            return -year  # BC years are negative
        except ValueError:
            return None
    
    # Handle AD years
    try:
        return int(re.sub(r'[^\d]', '', year_str))
    except ValueError:
        return None

def create_person_id(name: str) -> str:
    """Create a URL-safe ID from a person's name."""
    # Take the last name, or if there's only one word, use it
    words = name.split()
    if len(words) == 1:
        base = words[0]
    else:
        base = words[-1]  # Last name
    
    # Convert to lowercase, remove non-alphanumeric characters
    person_id = re.sub(r'[^a-z0-9]', '', base.lower())
    return person_id

def get_person_info():
    """Interactive function to get person information."""
    print("\n=== Add New Person to Shrine Timeline ===\n")
    
    # Get basic info
    name = input("Full name: ").strip()
    if not name:
        print("Name is required!")
        return None
    
    # Get birth year
    birth_input = input("Birth year (e.g., 1879, 470BC): ").strip()
    birth_year = validate_year(birth_input) if birth_input else None
    
    # Get death year
    death_input = input("Death year (leave empty if still alive): ").strip()
    death_year = validate_year(death_input) if death_input else None
    
    # Get gender
    while True:
        gender_input = input("Gender (m/f/male/female): ").strip().lower()
        if gender_input in ['m', 'male', '1']:
            gender = 1
            break
        elif gender_input in ['f', 'female', '0']:
            gender = 0
            break
        else:
            print("Please enter 'm' for male or 'f' for female")
    
    # Generate ID and image path
    person_id = create_person_id(name)
    image_path = f"/images/people/{person_id}.jpg"
    
    # Get Wikipedia override if needed
    wikipedia_override = input(f"Wikipedia page title (leave empty to use '{name}'): ").strip()
    wiki_title = wikipedia_override if wikipedia_override else name
    
    person_data = {
        "id": person_id,
        "name": name,
        "born": birth_year,
        "died": death_year,
        "image": image_path,
        "gender": gender,
        "wiki_title": wiki_title  # Temporary field for image download
    }
    
    return person_data

def add_person_to_json(person_data: dict, json_path: str = "people.json"):
    """Add person to the people.json file."""
    try:
        with open(json_path, 'r') as f:
            people = json.load(f)
    except FileNotFoundError:
        people = []
    
    # Check if person already exists
    existing_ids = [p["id"] for p in people]
    if person_data["id"] in existing_ids:
        print(f"Person with ID '{person_data['id']}' already exists!")
        return False
    
    # Remove temporary wiki_title field before saving
    clean_data = {k: v for k, v in person_data.items() if k != "wiki_title"}
    
    # Add person
    people.append(clean_data)
    
    # Sort by birth year
    people.sort(key=lambda p: p.get("born", 0) or 0)
    
    # Save back to file
    with open(json_path, 'w') as f:
        json.dump(people, f, indent=2)
    
    print(f"Added {person_data['name']} to {json_path}")
    return True

def download_person_image(person_data: dict):
    """Download portrait image for the person."""
    wiki_title = person_data.get("wiki_title", person_data["name"])
    image_path = pathlib.Path("../../static" + person_data["image"])
    
    print(f"\nAttempting to download image for {person_data['name']}...")
    
    try:
        # Get Wikidata Q-ID
        qid = wikipedia_to_qid(wiki_title)
        if not qid:
            print(f"⚠️  Could not find Wikidata Q-ID for '{wiki_title}'")
            return False
        
        print(f"Found Wikidata ID: {qid}")
        
        # Get image filename
        filename = qid_to_image_filename(qid)
        if not filename:
            print(f"⚠️  No image found on Wikidata for {qid}")
            return False
        
        print(f"Found image: {filename}")
        
        # Download image
        success = download_commons_file(filename, image_path)
        if success:
            print(f"✅ Successfully downloaded image for {person_data['name']}")
        return success
        
    except Exception as e:
        print(f"❌ Error downloading image: {e}")
        return False

def main():
    """Main function."""
    # Change to the script directory
    os.chdir(pathlib.Path(__file__).parent)
    
    print("Shrine Timeline - Add New Person")
    print("=================================")
    
    # Get person information
    person_data = get_person_info()
    if not person_data:
        print("Failed to get person information.")
        return
    
    # Show summary
    print(f"\n--- Summary ---")
    print(f"Name: {person_data['name']}")
    print(f"Born: {person_data['born']}")
    print(f"Died: {person_data['died'] or 'Still alive'}")
    print(f"Gender: {'Male' if person_data['gender'] == 1 else 'Female'}")
    print(f"ID: {person_data['id']}")
    print(f"Image: {person_data['image']}")
    
    # Confirm
    confirm = input("\nAdd this person? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return
    
    # Add to JSON
    if add_person_to_json(person_data):
        print("✅ Person added to people.json")
        
        # Try to download image
        download_confirm = input("\nTry to download portrait image? (y/n): ").strip().lower()
        if download_confirm == 'y':
            download_person_image(person_data)
        
        print(f"\n🎉 Done! {person_data['name']} has been added to the timeline.")
    else:
        print("❌ Failed to add person.")

if __name__ == "__main__":
    # Check if required packages are available
    try:
        import requests
        import tqdm
    except ImportError:
        print("Error: Required packages not found.")
        print("Please install: pip install requests tqdm")
        sys.exit(1)
    
    main() 