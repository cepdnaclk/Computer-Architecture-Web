#!/usr/bin/env python3
"""
Standardize KaTeX and Prism.js libraries across all lecture HTML files.
Uses consistent CDN (cdnjs.cloudflare.com) and all required components.
"""

import re
import os
from pathlib import Path

# Standard library block to insert
STANDARD_LIBRARIES = """    <!-- KaTeX for math rendering -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body);"></script>

    <!-- Prism.js for code syntax highlighting -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-c.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-asm6502.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
"""

def standardize_lecture(file_path):
    """Remove existing library includes and add standardized ones."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the </head> tag
    head_end_match = re.search(r'</head>', content)
    if not head_end_match:
        print(f"  ⚠️  Warning: No </head> tag found in {file_path}")
        return False
    
    # Remove all existing KaTeX and Prism references
    # Remove KaTeX lines
    content = re.sub(r'    <!-- KaTeX.*?-->\n', '', content)
    content = re.sub(r'    <link rel="stylesheet" href="https://cdn\.jsdelivr\.net/npm/katex@.*?>\n', '', content)
    content = re.sub(r'    <script.*?katex.*?></script>\n', '', content)
    
    # Remove Prism lines
    content = re.sub(r'    <!-- Prism.*?-->\n', '', content)
    content = re.sub(r'    <link.*?prism.*?>\n', '', content, flags=re.IGNORECASE)
    content = re.sub(r'    <script.*?prism.*?></script>\n', '', content, flags=re.IGNORECASE)
    
    # Insert standard libraries before </head>
    content = content.replace('</head>', f'{STANDARD_LIBRARIES}</head>')
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    lectures_dir = Path('Lectures/html')
    
    if not lectures_dir.exists():
        print(f"❌ Directory not found: {lectures_dir}")
        return
    
    lecture_files = sorted(lectures_dir.glob('lecture-*.html'))
    
    print(f"🔧 Standardizing libraries in {len(lecture_files)} lecture files...\n")
    
    for lecture_file in lecture_files:
        print(f"Processing {lecture_file.name}...", end=" ")
        if standardize_lecture(lecture_file):
            print("✅")
        else:
            print("❌")
    
    print(f"\n✨ Standardization complete!")

if __name__ == '__main__':
    main()
