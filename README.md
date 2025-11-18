# Lectures on Computer Architecture

A comprehensive lecture series by Dr. Isuru Nawinne - a professional, static GitHub Pages website for the "Lectures on Computer Architecture" course. This website provides easy access to lecture notes, downloadable materials, and organized content for students following the lecture series.

Hands-on practical series to complement the lecture series, providing practical experience with processor microarchitecture and memory systems using Verilog. Students build their own processors and implement memory hierarchy with caching.

## 🌟 Features

- **Professional Design**: Clean, modern interface with responsive design
- **20 Lecture Pages**: Individual HTML pages for each lecture with converted markdown content
- **Easy Navigation**: Organized by categories (Foundations, Programming Concepts, Processor Design, Memory Systems, Advanced Topics)
- **Download Materials**: Direct links to complete PDF notes and supplementary materials
- **Mobile Responsive**: Works seamlessly on desktop, tablet, and mobile devices
- **Previous/Next Navigation**: Easy navigation between lectures

## 📁 Project Structure


CO224-Web/
├── index.html              # Main landing page
├── assets/
│   └── css/
│       └── style.css       # Professional stylesheet
├── lectures/               # Generated HTML pages for each lecture
│   ├── lecture-01.html
│   ├── lecture-02.html
│   └── ... (20 lectures total)
├── Lectures/               # Original markdown files
│   ├── Lecture 1 - Computer Abstractions.md
│   ├── Lecture 2 - Technology Trends.md
│   └── ... (20 lectures)
│   └── img/                # Images used in lectures
├── materials/              # Downloadable materials
│   ├── Lectures-Complete-Notes.pdf (add your PDF here)
│   └── supplementary.zip (add your materials here)
├── convert_lectures.py     # Python script to convert MD to HTML
└── _config.yml             # GitHub Pages configuration


## 🚀 Deployment to GitHub Pages

### Step 1: Prepare Your Materials

1. **Add your PDF**: Place your complete lecture notes PDF in the `materials/` folder and name it `CO224-Complete-Notes.pdf`
2. **Add supplementary materials**: Create a zip file with supplementary materials and place it as `materials/supplementary.zip`

### Step 2: Push to GitHub

bash
git add .
git commit -m "Add CO224 lecture series website"
git push origin main


### Step 3: Enable GitHub Pages

1. Go to your GitHub repository: `https://github.com/cepdnaclk/CO224-Web`
2. Click on **Settings** (top menu)
3. Scroll down to **Pages** (left sidebar)
4. Under **Source**, select:
   - Branch: `main`
   - Folder: `/ (root)`
5. Click **Save**
6. Wait a few minutes for deployment

Your website will be live at: `https://cepdnaclk.github.io/CO224-Web/`

## 🔄 Updating Lecture Content

If you need to update the markdown files and regenerate the HTML pages:

### Method 1: Using Python Script (Recommended)

bash
# Ensure you have Python installed
python convert_lectures.py


This will regenerate all lecture HTML pages from the markdown files in the `Lectures/` folder.

### Method 2: Manual Updates

You can manually edit the HTML files in the `lectures/` folder if you need to make small changes.

## 🎨 Customization

### Changing Colors

Edit `assets/css/style.css` and modify the CSS variables at the top:

css
:root {
  --primary-color: #2563eb; /* Main blue color */
  --primary-dark: #1e40af; /* Darker blue */
  --accent-color: #0ea5e9; /* Accent color */
  /* ... other colors */
}


### Updating Header/Footer

Edit `index.html` to change the header or footer content.

### Modifying Lecture Categories

In `index.html`, find the sections with class `lecture-category` and update the categories and lecture assignments as needed.

## 📝 Adding New Lectures

1. Add your new lecture markdown file to the `Lectures/` folder following the naming convention: `Lecture XX - Title.md`
2. Run the conversion script: `python convert_lectures.py`
3. Update `index.html` to add a link to the new lecture
4. Commit and push changes

## 🛠️ Technologies Used

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with flexbox and grid
- **Python**: Markdown to HTML conversion script
- **GitHub Pages**: Free static site hosting

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📄 License

This educational material is provided for academic purposes. Please contact the course instructors for usage permissions.

## 👥 Contributors

Department of Computer Engineering, University of Peradeniya

## 📧 Contact

For questions or issues, please contact the course coordinators.

---

**Note**: Make sure to add your actual PDF and supplementary materials to the `materials/` folder before deploying to ensure download links work correctly.
