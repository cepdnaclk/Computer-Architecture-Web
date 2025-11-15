import os
import re
from pathlib import Path

def convert_markdown_to_html(md_content):
    """Convert markdown content to HTML"""
    html = md_content
    
    # Convert headers
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    
    # Convert bold and italic
    html = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    html = re.sub(r'_(.*?)_', r'<em>\1</em>', html)
    
    # Convert inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Convert images
    html = re.sub(r'<img src="img/', r'<img src="../Lectures/img/', html)
    html = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1" style="max-width: 100%;">', html)
    
    # Convert links
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
    
    # Convert unordered lists
    lines = html.split('\n')
    in_ul = False
    result_lines = []
    
    for line in lines:
        if re.match(r'^- ', line):
            if not in_ul:
                result_lines.append('<ul>')
                in_ul = True
            result_lines.append('<li>' + line[2:] + '</li>')
        else:
            if in_ul:
                result_lines.append('</ul>')
                in_ul = False
            result_lines.append(line)
    
    if in_ul:
        result_lines.append('</ul>')
    
    html = '\n'.join(result_lines)
    
    # Convert paragraphs (lines that aren't already HTML tags)
    lines = html.split('\n')
    result_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('<') and not line.endswith('>'):
            result_lines.append(f'<p>{line}</p>')
        else:
            result_lines.append(line)
    
    return '\n'.join(result_lines)

def get_lecture_title(filename):
    """Extract lecture title from filename"""
    match = re.match(r'Lecture (\d+) - (.+)\.md', filename)
    if match:
        num, title = match.groups()
        return f"Lecture {num}: {title}"
    return filename.replace('.md', '')

def create_lecture_html(lecture_num, title, content, prev_num=None, next_num=None):
    """Create HTML page for a lecture"""
    
    prev_link = f'<a href="lecture-{prev_num:02d}.html" class="nav-btn">← Previous Lecture</a>' if prev_num else '<span class="nav-btn disabled">← Previous Lecture</span>'
    next_link = f'<a href="lecture-{next_num:02d}.html" class="nav-btn">Next Lecture →</a>' if next_num else '<span class="nav-btn disabled">Next Lecture →</span>'
    
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - CO224 Computer Architecture</title>
    <link rel="stylesheet" href="../assets/css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <header class="lecture-header">
        <div class="container">
            <a href="../index.html" class="back-link">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="19" y1="12" x2="5" y2="12"></line>
                    <polyline points="12 19 5 12 12 5"></polyline>
                </svg>
                Back to All Lectures
            </a>
            <h1 class="lecture-title">{title}</h1>
            <p class="lecture-meta">CO224 - Computer Architecture</p>
        </div>
    </header>

    <main class="lecture-content-area container">
        <div class="content-body">
            {content}
            
            <div class="lecture-nav">
                {prev_link}
                {next_link}
            </div>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2025 CO224 Computer Architecture Lecture Series. All rights reserved.</p>
            <p>Department of Computer Engineering, University of Peradeniya</p>
        </div>
    </footer>
</body>
</html>
'''
    return html_template

def main():
    """Main function to convert all lecture markdown files to HTML"""
    lectures_dir = Path('Lectures')
    output_dir = Path('lectures')
    output_dir.mkdir(exist_ok=True)
    
    # Get all lecture files and sort them numerically by lecture number
    def get_lecture_number(filename):
        match = re.match(r'Lecture (\d+)', filename.name)
        return int(match.group(1)) if match else 0
    
    lecture_files = sorted([f for f in lectures_dir.glob('Lecture *.md')], key=get_lecture_number)
    
    print(f"Found {len(lecture_files)} lecture files")
    
    for i, lecture_file in enumerate(lecture_files):
        lecture_num = i + 1
        prev_num = i if i > 0 else None
        next_num = i + 2 if i < len(lecture_files) - 1 else None
        
        print(f"Processing: {lecture_file.name}")
        
        # Read markdown content
        with open(lecture_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Get title
        title = get_lecture_title(lecture_file.name)
        
        # Convert to HTML
        html_content = convert_markdown_to_html(md_content)
        
        # Create full HTML page
        full_html = create_lecture_html(lecture_num, title, html_content, prev_num, next_num)
        
        # Write to file
        output_file = output_dir / f'lecture-{lecture_num:02d}.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        print(f"Created: {output_file.name}")
    
    print(f"\nSuccessfully created {len(lecture_files)} lecture HTML pages!")

if __name__ == '__main__':
    main()
