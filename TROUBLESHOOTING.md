# Troubleshooting Guide

## Issue: Site stuck on "Redirecting to people page..."

### The Problem
When visiting `https://abaj8494.github.io/timeline/`, the page displays "Redirecting to people page..." but never actually redirects.

### Root Cause
GitHub Pages uses **Jekyll** by default, which:
1. Processes all files through the Jekyll static site generator
2. **Ignores any folders starting with underscore** (like `_app/`)
3. This means the `_app/` folder containing all JavaScript and CSS was not being served
4. Without JavaScript, the client-side navigation couldn't work

### The Solution
Created a `.nojekyll` file in the `static/` folder, which:
- Tells GitHub Pages to **disable Jekyll processing**
- Allows the `_app/` folder to be served normally
- Enables all JavaScript and CSS to load properly

### Files Modified
1. ✅ `static/.nojekyll` - Created (empty file)
2. ✅ `svelte.config.js` - Fixed prerender error handler to allow base path in image URLs
3. ✅ Rebuilt the site with `npm run build`

### What You Need to Do
1. **Commit and push** the newly built `docs/` folder with `.nojekyll` file:
   ```bash
   git add docs/ static/.nojekyll
   git commit -m "Fix GitHub Pages deployment - add .nojekyll file"
   git push origin main
   ```

2. **Wait 1-2 minutes** for GitHub Pages to rebuild

3. **Test** your site at https://abaj8494.github.io/timeline/

### Expected Result
✅ Site loads immediately at https://abaj8494.github.io/timeline/people  
✅ You can click and drag to pan the timeline  
✅ Clicking on people/books shows their details  
✅ All navigation works properly

## Other Common Issues

### Issue: 404 errors on navigation
**Symptom:** Clicking links or refreshing the page shows a 404 error

**Solution:** Make sure you're deploying from the `docs/` folder in GitHub Pages settings, not using GitHub Actions.

### Issue: Assets not loading (broken images, no CSS)
**Symptom:** Page loads but looks broken, images don't show

**Causes:**
1. Missing `.nojekyll` file (see above)
2. Incorrect base path configuration
3. Files not committed to git

**Solution:** 
1. Verify `.nojekyll` exists in `docs/` folder
2. Check that `base: '/timeline'` in `svelte.config.js` matches your repo name
3. Ensure all files in `docs/` are committed and pushed

### Issue: Changes not appearing after push
**Symptom:** You pushed changes but the site still shows old content

**Solution:**
1. Check GitHub Actions tab - deployment might have failed
2. Clear your browser cache (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows)
3. Check that you committed the `docs/` folder, not just source files
4. GitHub Pages can take 1-2 minutes to update

### Issue: Site works locally but not on GitHub Pages
**Symptom:** `npm run preview` works fine but deployed site is broken

**Likely causes:**
1. Missing `.nojekyll` file
2. Base path mismatch
3. Absolute URLs instead of relative URLs

**Solution:**
1. Add `.nojekyll` to `static/` folder
2. Rebuild with `npm run build`
3. Verify `base: '/timeline'` matches your repository name

## Verification Checklist

After pushing your changes, verify:
- [ ] `.nojekyll` file exists in both `static/` and `docs/` folders
- [ ] `docs/` folder is committed and pushed to main branch
- [ ] GitHub Pages settings point to "Deploy from a branch" → main → `/docs`
- [ ] Site loads at https://abaj8494.github.io/timeline/
- [ ] Timeline is interactive (can click and drag)
- [ ] Clicking on people/books shows popups
- [ ] Navigation between pages works
- [ ] Browser console shows no 404 errors for `_app/` files

## Getting Help

If you're still experiencing issues:
1. Check browser console (F12) for error messages
2. Verify the `_app/` folder files are loading (check Network tab)
3. Confirm the base path in the HTML matches your URL structure
4. Try clearing browser cache and hard refresh (Cmd+Shift+R or Ctrl+Shift+R)

