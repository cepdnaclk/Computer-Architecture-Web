# 🚀 Quick Start Guide - CO224 Website

## What You Have

A complete, professional GitHub Pages website for your CO224 Computer Architecture lecture series with:

- ✅ 20 lecture pages with converted markdown content
- ✅ Professional, responsive design
- ✅ Easy navigation and organization
- ✅ Download sections for materials
- ✅ Mobile-friendly layout

## Preview Locally (Before Deployment)

### Option 1: Using Python Server (Recommended)

```bash
python preview_server.py
```

This will:

- Start a local web server
- Automatically open your browser to http://localhost:8000
- Let you preview the entire website

### Option 2: Direct File Opening

Simply double-click `index.html` to open it in your browser.

## Deploy to GitHub Pages

### Quick Deployment (3 Steps)

**Step 1: Add your materials** (optional)

```bash
# Place your files in the materials/ folder:
# - CO224-Complete-Notes.pdf
# - supplementary.zip
```

**Step 2: Commit and push**

```bash
git add .
git commit -m "Add CO224 lecture series website"
git push origin main
```

**Step 3: Enable GitHub Pages**

1. Go to: https://github.com/cepdnaclk/CO224-Web/settings/pages
2. Select branch: **main**, folder: **/ (root)**
3. Click **Save**

**Done!** Your site will be live at: https://cepdnaclk.github.io/CO224-Web/

## Common Tasks

### Update Lecture Content

```bash
# 1. Edit markdown files in Lectures/ folder
# 2. Regenerate HTML
python convert_lectures.py

# 3. Deploy
git add .
git commit -m "Update lecture content"
git push origin main
```

### Change Website Colors

Edit `assets/css/style.css` and modify the CSS variables:

```css
:root {
  --primary-color: #2563eb; /* Change this */
  --primary-dark: #1e40af; /* And this */
}
```

### Add YouTube Video Links

Edit `index.html` and add YouTube links in the lecture descriptions or create a new section.

## File Structure

```
CO224-Web/
├── index.html                 # Main page - START HERE
├── assets/css/style.css       # All styling
├── lectures/                  # 20 lecture HTML pages
├── Lectures/                  # Original markdown files
│   └── img/                   # Images
├── materials/                 # PDF and zip files
├── preview_server.py          # Local preview tool
└── convert_lectures.py        # MD to HTML converter
```

## Troubleshooting

### Problem: Images not showing

**Solution:** Make sure `Lectures/img/` folder is committed to git

### Problem: Download links return 404

**Solution:** Add your PDF and zip files to `materials/` folder

### Problem: Site not updating on GitHub Pages

**Solution:** Wait 2-3 minutes, then clear browser cache (Ctrl+Shift+R)

### Problem: Lecture links broken

**Solution:** Check that all 20 HTML files are in `lectures/` folder

## Need Help?

📖 **Full Documentation:** See `README.md`  
🚀 **Deployment Guide:** See `DEPLOYMENT.md`  
📊 **Project Summary:** See `PROJECT-SUMMARY.md`

## Quick Commands Reference

```bash
# Preview locally
python preview_server.py

# Regenerate lecture pages
python convert_lectures.py

# Check git status
git status

# Deploy to GitHub
git add .
git commit -m "Update website"
git push origin main
```

## Your Website URL

After deployment: **https://cepdnaclk.github.io/CO224-Web/**

---

**🎉 You're all set!** The website is ready to deploy whenever you are.
