# Quick Deployment Guide for CO224 Website

## Prerequisites

- Git installed on your computer
- GitHub account with access to cepdnaclk/CO224-Web repository

## Step-by-Step Deployment

### 1. Add Your Materials (Important!)

Before deploying, add your PDF and supplementary materials:

```bash
# Place your files in the materials folder:
# - materials/CO224-Complete-Notes.pdf
# - materials/supplementary.zip
```

If you don't have these files ready yet, the website will still work but download links will return 404 errors.

### 2. Review Your Changes

```bash
# Check what files have been created/modified
git status
```

You should see:

- `index.html`
- `assets/css/style.css`
- `lectures/` folder with 20 HTML files
- `materials/` folder
- `_config.yml`
- `convert_lectures.py`
- `.gitignore`
- `README.md`

### 3. Commit and Push

```bash
# Stage all files
git add .

# Commit with a descriptive message
git commit -m "Add CO224 Computer Architecture lecture series website"

# Push to GitHub
git push origin main
```

### 4. Enable GitHub Pages

1. Go to: https://github.com/cepdnaclk/CO224-Web/settings/pages
2. Under "Source":
   - Select branch: **main**
   - Select folder: **/ (root)**
3. Click **Save**

### 5. Wait for Deployment

- GitHub Pages typically takes 1-3 minutes to build and deploy
- You'll see a green checkmark when it's ready
- Your site will be live at: **https://cepdnaclk.github.io/CO224-Web/**

### 6. Verify Your Site

1. Visit: https://cepdnaclk.github.io/CO224-Web/
2. Check that:
   - All lecture links work
   - Images display correctly
   - Navigation works between lectures
   - The site looks good on mobile and desktop

## Troubleshooting

### Images Not Displaying

- Check that the `Lectures/img/` folder is committed to the repository
- Verify image paths in the markdown files use `img/` prefix

### Download Links Not Working

- Make sure you added the files to the `materials/` folder
- Check that filenames match exactly:
  - `CO224-Complete-Notes.pdf`
  - `supplementary.zip`

### Site Not Updating

- Clear your browser cache (Ctrl+Shift+R or Cmd+Shift+R)
- Wait a few more minutes for GitHub Pages to rebuild
- Check the Actions tab for build status

### 404 Page Not Found

- Verify your repository name matches: `CO224-Web`
- Check that GitHub Pages is enabled and set to the correct branch

## Updating Content Later

To update lecture content:

1. Edit the markdown files in `Lectures/` folder
2. Run: `python convert_lectures.py`
3. Commit and push:
   ```bash
   git add .
   git commit -m "Update lecture content"
   git push origin main
   ```

## Custom Domain (Optional)

If you want to use a custom domain:

1. Add a `CNAME` file to the repository root with your domain
2. Configure DNS settings with your domain provider
3. Enable HTTPS in GitHub Pages settings

## Need Help?

- Check the main README.md for detailed documentation
- Review GitHub Pages documentation: https://docs.github.com/en/pages
- Contact the course coordinators

---

**Your website will be live at:** https://cepdnaclk.github.io/CO224-Web/
