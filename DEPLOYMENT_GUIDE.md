# Deployment Guide

## Summary of Upgrades

This document describes the three major upgrades implemented for the Shrine Timeline static site.

### 1. ✅ Deployment Configuration (docs folder)

The build output has been configured to generate into the `docs` folder instead of the default `build` folder.

**What changed:**
- Modified `svelte.config.js` to set `pages: 'docs'` and `assets: 'docs'`
- Running `npm run build` now generates the site in the `docs` directory

**To deploy on GitHub Pages:**
1. Push your changes to the main branch
2. Go to GitHub repository Settings → Pages
3. Under "Build and deployment" → Source: select "Deploy from a branch"
4. Branch: select "main" and folder: select "/docs"
5. Save and wait for deployment (usually takes 1-2 minutes)

### 2. ✅ Search Engine Optimization (SEO)

Comprehensive SEO features have been added to improve search engine visibility and social media sharing.

**What was added:**

#### Meta Tags (in `src/app.html`)
- Description, keywords, author tags
- OpenGraph tags for Facebook/LinkedIn sharing
- Twitter Card metadata
- Robots meta tag for crawling
- Canonical URL

#### Page-Specific SEO
- Created `+page.js` files for `/people` and `/books` routes
- Dynamic meta tags with page-specific titles and descriptions
- Custom OpenGraph images for each page

#### Structured Data
- JSON-LD schema in `+layout.svelte`
- WebSite schema with SearchAction for search engines

#### SEO Files
- `static/robots.txt` - guides search engine crawlers
- `static/sitemap.xml` - lists all pages for indexing

**Important:** Update the placeholder URLs in these files:
- `src/app.html` - line 23 (canonical URL)
- `src/routes/+layout.svelte` - line 19 (structured data URL)
- `src/routes/people/+page.svelte` - line 16 (OG URL)
- `src/routes/books/+page.svelte` - line 16 (OG URL)
- `static/robots.txt` - line 5 (sitemap URL)
- `static/sitemap.xml` - all URLs (lines 4-23)

Replace `https://yourdomain.com` with your actual domain.

### 3. ✅ Click-and-Drag Panning

The timeline now supports intuitive panning via click-and-drag instead of just scrolling.

**Features:**
- Click and hold anywhere on the timeline to grab and drag
- Visual cursor feedback (grab/grabbing cursor states)
- Smart interaction detection - panning disabled when clicking on people, books, or popups
- Smooth panning with 1.5x multiplier for better UX
- Text selection prevention during drag
- Full keyboard accessibility support
  - Tab to navigate through timeline items
  - Enter or Space to view details

**Accessibility:**
- ARIA roles and labels for screen readers
- Keyboard navigation support
- Proper focus management

## Building and Deploying

### Build the site:
```bash
npm run build
```

This will generate the production site in the `docs` folder.

### Preview locally:
```bash
npm run preview
```

### File structure in docs/:
- `index.html`, `people.html`, `books.html`, `search.html` - main pages
- `_app/` - bundled JavaScript and CSS
- `images/` - all images (people and books)
- `robots.txt`, `sitemap.xml` - SEO files
- `favicon.png` - site icon
- `.nojekyll` - **CRITICAL**: Disables Jekyll processing on GitHub Pages (allows `_app` folder to be served)

## Important: .nojekyll File

The `.nojekyll` file in the `static/` folder is **critical** for GitHub Pages deployment. Without it:
- GitHub Pages uses Jekyll by default
- Jekyll ignores folders starting with underscore (like `_app/`)
- Your JavaScript and CSS won't load
- The site will be stuck on "Redirecting to people page..."

The build process automatically copies `.nojekyll` from `static/` to `docs/`. Never delete this file!

## Build Warnings

There is one minor accessibility warning about the timeline container div with mouse event listeners. This is a false positive - the element has `role="application"` which is the correct ARIA role for canvas-like widgets that need custom interaction handling. The warning does not affect functionality or prevent successful builds.

## Testing

After deployment, test:
1. ✅ Timeline panning (click and drag)
2. ✅ Clicking on people/books to view details
3. ✅ Navigation between pages
4. ✅ Search functionality
5. ✅ Keyboard navigation (Tab, Enter, Space keys)
6. ✅ Mobile responsiveness

## SEO Validation

After deployment, validate SEO with these tools:
- Google Search Console (submit sitemap)
- Facebook Sharing Debugger (test OpenGraph tags)
- Twitter Card Validator (test Twitter cards)
- Google Rich Results Test (validate structured data)

## Notes

- The base path is set to `/shrine` (configured in `svelte.config.js`)
- All asset paths use the `resolveBasePath` utility to work with the base path
- The site is fully static and requires no server-side rendering
- Initial scroll position is set to year 500 AD for optimal viewing

