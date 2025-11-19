"""
Professional Markdown to LaTeX converter - Properly handles all formatting
"""

import re
from pathlib import Path

MARKDOWN_DIR = Path(r"d:\Academics\Projects\isuru sir\CO224-Web\Lectures\markdown")
LATEX_DIR = Path(r"d:\Academics\Projects\isuru sir\CO224-Web\Lectures\latex")

LECTURE_FILES = [
    ("Lecture 1 - Computer Abstractions.md", 1),
    ("Lecture 2 - Technology Trends.md", 2),
    ("Lecture 3 - Understanding Performance.md", 3),
]


def process_markdown_file(md_path):
    """Convert markdown file to LaTeX with proper structure."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    latex_output = []
    
    i = 0
    in_code_block = False
    in_list = False
    list_type = None  # 'itemize' or 'enumerate'
    
    while i < len(lines):
        line = lines[i]
        
        # Handle code blocks
        if line.strip().startswith('```'):
            if not in_code_block:
                latex_output.append(r'\begin{verbatim}')
                in_code_block = True
            else:
                latex_output.append(r'\end{verbatim}')
                latex_output.append('')
                in_code_block = False
            i += 1
            continue
        
        if in_code_block:
            latex_output.append(line)
            i += 1
            continue
        
        # Close list if we're not continuing it
        if in_list and not (line.strip().startswith('- ') or re.match(r'^\d+\.\s', line.strip())):
            if not line.strip() or line.startswith('#') or line.startswith('**'):
                if list_type == 'itemize':
                    latex_output.append(r'\end{itemize}')
                else:
                    latex_output.append(r'\end{enumerate}')
                latex_output.append('')
                in_list = False
                list_type = None
        
        # Handle headings
        if line.startswith('# ') and not line.startswith('## '):
            title = line[2:].strip().replace('*', '')
            latex_output.append(f'\\section{{{title}}}')
            latex_output.append('')
            i += 1
            continue
        elif line.startswith('## '):
            title = line[3:].strip()
            latex_output.append(f'\\subsection{{{title}}}')
            latex_output.append('')
            i += 1
            continue
        elif line.startswith('### '):
            title = line[4:].strip()
            latex_output.append(f'\\subsubsection{{{title}}}')
            latex_output.append('')
            i += 1
            continue
        elif line.startswith('#### '):
            title = line[5:].strip()
            latex_output.append(f'\\paragraph{{{title}}}')
            latex_output.append('')
            i += 1
            continue
        
        # Handle author line
        if re.match(r'^\*By .+\*$', line.strip()):
            author = line.strip()[1:-1]
            latex_output.append(f'\\emph{{{author}}}')
            latex_output.append('')
            i += 1
            continue
        
        # Handle images
        if '<img src=' in line:
            img_match = re.search(r'<img src="([^"]+)"[^>]*alt="([^"]+)"', line)
            if img_match:
                img_path = img_match.group(1)
                caption = img_match.group(2)
                latex_output.append(r'\begin{figure}[h]')
                latex_output.append(r'\centering')
                latex_output.append(f'\\includegraphics[width=0.7\\textwidth]{{{img_path}}}')
                latex_output.append(f'\\caption{{{caption}}}')
                latex_output.append(r'\end{figure}')
                latex_output.append('')
            i += 1
            continue
        
        # Handle bullet lists
        if line.strip().startswith('- '):
            if not in_list or list_type != 'itemize':
                if in_list:
                    latex_output.append(r'\end{enumerate}')
                    latex_output.append('')
                latex_output.append(r'\begin{itemize}')
                in_list = True
                list_type = 'itemize'
            
            item_text = line.strip()[2:]
            # Process inline formatting
            item_text = process_inline(item_text)
            latex_output.append(f'\\item {item_text}')
            i += 1
            continue
        
        # Handle numbered lists
        if re.match(r'^\d+\.\s', line.strip()):
            if not in_list or list_type != 'enumerate':
                if in_list:
                    latex_output.append(r'\end{itemize}')
                    latex_output.append('')
                latex_output.append(r'\begin{enumerate}')
                in_list = True
                list_type = 'enumerate'
            
            item_text = re.sub(r'^\d+\.\s+', '', line.strip())
            item_text = process_inline(item_text)
            latex_output.append(f'\\item {item_text}')
            i += 1
            continue
        
        # Handle empty lines
        if not line.strip():
            if in_list:
                # Check if next line continues the list
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if not (next_line.startswith('- ') or re.match(r'^\d+\.', next_line)):
                        if list_type == 'itemize':
                            latex_output.append(r'\end{itemize}')
                        else:
                            latex_output.append(r'\end{enumerate}')
                        in_list = False
                        list_type = None
            latex_output.append('')
            i += 1
            continue
        
        # Regular text paragraph
        processed_line = process_inline(line)
        latex_output.append(processed_line)
        i += 1
    
    # Close any unclosed environments
    if in_code_block:
        latex_output.append(r'\end{verbatim}')
    if in_list:
        if list_type == 'itemize':
            latex_output.append(r'\end{itemize}')
        else:
            latex_output.append(r'\end{enumerate}')
    
    return '\n'.join(latex_output)


def process_inline(text):
    """Process inline markdown formatting."""
    # Handle bold
    text = re.sub(r'\*\*([^\*]+)\*\*', r'\\textbf{\1}', text)
    
    # Handle italic (but not already processed bold)
    text = re.sub(r'(?<!\*)\*(?!\*)([^\*]+)\*(?!\*)', r'\\emph{\1}', text)
    
    # Handle inline code
    text = re.sub(r'`([^`]+)`', r'\\texttt{\1}', text)
    
    # Handle arrows
    text = text.replace('→', r'$\rightarrow$')
    text = text.replace('←', r'$\leftarrow$')
    text = text.replace('↔', r'$\leftrightarrow$')
    
    # Handle math symbols
    text = text.replace('×', r'$\times$')
    text = text.replace('÷', r'$\div$')
    text = text.replace('≤', r'$\leq$')
    text = text.replace('≥', r'$\geq$')
    text = text.replace('≠', r'$\neq$')
    
    # Escape special LaTeX characters (except in math mode)
    # Be careful not to escape already escaped characters
    text = text.replace('&', r'\&')
    text = text.replace('%', r'\%')
    text = text.replace('#', r'\#')
    text = re.sub(r'(?<!\\)_', r'\_', text)  # Only escape unescaped underscores
    
    return text


def main():
    """Convert lectures 1-3 to LaTeX."""
    LATEX_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Converting Lectures 1-3 to LaTeX...\n")
    
    for filename, num in LECTURE_FILES:
        print(f"Processing Lecture {num}: {filename}")
        
        md_path = MARKDOWN_DIR / filename
        if not md_path.exists():
            print(f"  ⚠️  File not found!")
            continue
        
        latex_content = process_markdown_file(md_path)
        
        latex_file = LATEX_DIR / f"lecture-{num:02d}.tex"
        with open(latex_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"  ✅ Created lecture-{num:02d}.tex\n")
    
    print("✅ Complete! Lectures 1-3 have been regenerated with proper formatting.")


if __name__ == '__main__':
    main()
