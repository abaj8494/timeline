# Scripts Directory

This directory contains all Python scripts used for managing the Timeline project.

## Requirements

All scripts require Python 3.7+ and the following packages:
```bash
pip install requests tqdm pillow
```

## Scripts Overview

### 1. `add_person.py`
Interactive script to add new people to the timeline.

**Usage:**
```bash
cd /path/to/timeline
python scripts/add_person.py
```

See `README_add_person.md` for detailed instructions.

### 2. `fetch_portraits.py`
Download portrait images for all people in `people.json` from Wikimedia Commons.

**Usage:**
```bash
cd src/lib/data  # Must be run from this directory
python ../../scripts/fetch_portraits.py
```

### 3. `fetch_book_covers.py`
Download book cover images for all books in `books.json` from Open Library or Wikimedia Commons.

**Usage:**
```bash
cd src/lib/data  # Must be run from this directory
python ../../scripts/fetch_book_covers.py
```

### 4. `downsample_images.py`
Downsample images to reduce file size while maintaining quality.

**Usage:**
```bash
cd static/images  # Must be run from this directory
python ../../scripts/downsample_images.py
```

### 5. `get_img.py`
Helper script for fetching images (legacy).

## Notes

- Most scripts expect to be run from specific directories (see Usage above)
- Scripts use Wikipedia and Wikidata APIs to fetch images
- Images are downloaded to `static/images/people/` or `static/images/books/`
- All scripts include error handling and progress bars via `tqdm`

