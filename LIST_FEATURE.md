# List View Feature

## Overview
A new List View has been added to the Shrine project, inspired by the math-map project. This provides an alternative way to browse historical figures.

## Features Implemented

### 1. List View (`/list`)
- **Route**: `/list`
- **Description**: Shows all people sorted by birth date in a clean, browsable list format
- **Features**:
  - Displays people with their images, names, birth/death dates, and lifespan
  - Clickable cards that show detailed information in a popup
  - Direct link to view selected person in the timeline
  - Sorted chronologically by birth date

### 2. Gender Filtering
- Simple filter with three options:
  - **All**: Show all people
  - **Male**: Show only male historical figures (gender = 1)
  - **Female**: Show only female historical figures (gender = 0)
- Filter is displayed as buttons in the header
- Count of filtered people is shown in the title

### 3. Keyboard Shortcuts
Global keyboard shortcuts are now available throughout the application:

| Key | Action | Note |
|-----|--------|------|
| `S` | Navigate to Search page | Works from any page |
| `B` | Navigate to Books timeline | Only when NOT on books page |
| `L` | Navigate to List view | Works from any page |
| `P` | Navigate to People timeline | Only when NOT on people page |

**Important**: Keyboard shortcuts are disabled when typing in input fields or text areas.

### 4. Navigation Updates
All pages now include a List View button (📋) in the navigation controls:
- **People Timeline**: Books, List, Search buttons
- **Books Timeline**: People, List, Search buttons
- **Search Page**: People, Books, List buttons
- **List View**: Timeline, Books, Search buttons

## Design Choices

### Simplified Filtering
Unlike the math-map project which has advanced filtering by difficulty, category, and type, the Shrine list view uses simple gender-based filtering, which is appropriate for the people dataset.

### Consistent Navigation
All pages now follow a consistent navigation pattern with circular icon buttons in the top-left corner.

### Keyboard Shortcuts Logic
- The `B` and `P` shortcuts only work when NOT on their respective pages to avoid confusion
- The `S` and `L` shortcuts work from any page as they're always useful navigation options
- Shortcuts are case-insensitive

## Technical Implementation

### Files Created/Modified

**New Files**:
- `/src/routes/list/+page.svelte` - Main list view component
- `/src/routes/list/+page.js` - Page metadata loader

**Modified Files**:
- `/src/routes/+layout.svelte` - Added keyboard shortcut handler
- `/src/routes/people/+page.svelte` - Added List button
- `/src/routes/books/+page.svelte` - Added List button
- `/src/routes/search/+page.svelte` - Added List button, updated navigation layout

### Data Structure
The list view uses the existing `people.json` data structure:
```json
{
  "id": "string",
  "name": "string",
  "born": number,
  "died": number,
  "image": "string",
  "gender": number  // 0 = female, 1 = male
}
```

## Usage

1. **Accessing List View**:
   - Click the 📋 button from any page
   - Press `L` key from anywhere
   - Navigate to `/list` directly

2. **Filtering**:
   - Click on "All", "Male", or "Female" buttons in the header
   - The list updates instantly with filtered results
   - Count in the title updates to show number of filtered people

3. **Viewing Details**:
   - Click on any person card
   - A popup appears with their image, full dates, and lifespan
   - Click "View in Timeline" to see them in the timeline view
   - Click the X button or outside to close the popup

4. **Keyboard Navigation**:
   - Use `P` to jump to People timeline
   - Use `B` to jump to Books timeline
   - Use `S` to jump to Search
   - Use `L` to return to List view

## Future Enhancements (Optional)
- Add sorting options (by name, by death date, by lifespan)
- Add search within the list
- Add multiple filter options (by century, by location, etc.)
- Virtualization for better performance with large datasets
- Export/share filtered lists

