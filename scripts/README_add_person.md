# Adding New People to the Timeline

## Quick Start

1. **Run the script:**
   ```bash
   cd src/lib/data
   python add_person.py
   ```

2. **Follow the prompts:**
   - Enter the person's full name
   - Birth year (supports BC dates like "470BC")
   - Death year (leave empty if still alive)
   - Gender (m/f)
   - Wikipedia page title (optional override)

3. **The script will:**
   - Generate a unique ID from their name
   - Add them to `people.json`
   - Attempt to download their portrait from Wikipedia/Wikimedia Commons
   - Sort the timeline by birth year

## Example Usage

```
=== Add New Person to Timeline ===

Full name: Marie Curie
Birth year (e.g., 1879, 470BC): 1867
Death year (leave empty if still alive): 1934
Gender (m/f/male/female): f
Wikipedia page title (leave empty to use 'Marie Curie'): 

--- Summary ---
Name: Marie Curie
Born: 1867
Died: 1934
Gender: Female
ID: curie
Image: /images/people/curie.jpg

Add this person? (y/n): y
```

## Requirements

- Python 3.7+
- `requests` library: `pip install requests`
- `tqdm` library: `pip install tqdm`

## Notes

- The script automatically generates an ID from the last name
- Portrait images are downloaded from Wikimedia Commons when available
- Birth/death years support BC dates (use "470BC" format)
- People are automatically sorted by birth year in the JSON file
- Images are saved to `static/images/people/[id].jpg`

## Troubleshooting

- **No image found**: Some people might not have portraits on Wikimedia Commons
- **Duplicate ID**: The script will warn if someone with the same ID already exists
- **Wikipedia not found**: Try using the full Wikipedia page title (e.g., "Leonardo da Vinci" instead of "Da Vinci") 