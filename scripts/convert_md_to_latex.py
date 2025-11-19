"""
Convert Markdown lecture files to LaTeX format for inclusion in main document.
Preserves exact content without modification.
"""

import os
import re

# Define input and output directories
MARKDOWN_DIR = r"d:\Academics\Projects\isuru sir\CO224-Web\Lectures\markdown"
LATEX_DIR = r"d:\Academics\Projects\isuru sir\CO224-Web\Lectures\latex"

# Map lecture files to correct numbers
LECTURE_MAPPING = {
    "Lecture 1 - Computer Abstractions.md": 1,
    "Lecture 2 - Technology Trends.md": 2,
    "Lecture 3 - Understanding Performance.md": 3,
    "Lecture 4 - Introduction to ARM Assembly.md": 4,
    "Lecture 5 - Number Representation and Data Processing.md": 5,
    "Lecture 6 - Branching.md": 6,
    "Lecture 7 - Function Call and Return.md": 7,
    "Lecture 8 - Memory Access.md": 8,
    "Lecture 9 - Microarchitecture and Datapath.md": 9,
    "Lecture 10 - Processor Control.md": 10,
    "Lecture 11 - Single-Cycle Execution.md": 11,
    "Lecture 12 - Pipelined Processors.md": 12,
    "Lecture 13 - Pipeline Operation and Timing.md": 13,
    "Lecture 14 - Memory Hierarchy and Caching.md": 14,
    "Lecture 15 - Direct Mapped Cache Control.md": 15,
    "Lecture 16 - Associative Cache Control.md": 16,
    "Lecture 17 - Multi-Level Caching.md": 17,
    "Lecture 18 - Virtual Memory.md": 18,
    "Lecture 19 - Multiprocessors.md": 19,
    "Lecture 20 - Storage and Interfacing.md": 20,
}

def escape_latex(text):
    """Escape special LaTeX characters in text, but preserve intentional LaTeX."""
    # Don't escape if already in LaTeX command
    if text.startswith('\\'):
        return text
    
    # Mapping of characters to escape
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '#': r'\#',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }
    
    # Handle backslash and underscore specially
    text = text.replace('\\', r'\textbackslash{}')
    text = text.replace('_', r'\_')
    text = text.replace('$', r'\$')
    
    # Create a regular expression pattern for other characters
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    return text

def convert_markdown_to_latex(md_content):
    """Convert markdown content to LaTeX, preserving exact content."""
    lines = md_content.split('\n')
    latex_lines = []
    in_code_block = False
    code_block_content = []
    in_list = False
    list_level = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Handle code blocks (triple backticks or indented code)
        if line.strip().startswith('```'):
            if in_code_block:
                # End code block
                latex_lines.append(r'\begin{verbatim}')
                latex_lines.extend(code_block_content)
                latex_lines.append(r'\end{verbatim}')
                latex_lines.append('')
                code_block_content = []
                in_code_block = False
            else:
                # Start code block
                in_code_block = True
            i += 1
            continue
        
        if in_code_block:
            code_block_content.append(line)
            i += 1
            continue
        
        # Handle headings
        if line.startswith('# '):
            # Main title (Lecture X:)
            title = line[2:].strip()
            # Remove asterisks for emphasis
            title = title.replace('*', '')
            latex_lines.append(r'\section{' + escape_latex(title) + '}')
            latex_lines.append('')
        elif line.startswith('## '):
            section_title = line[3:].strip()
            latex_lines.append(r'\subsection{' + escape_latex(section_title) + '}')
            latex_lines.append('')
        elif line.startswith('### '):
            subsection_title = line[4:].strip()
            latex_lines.append(r'\subsubsection{' + escape_latex(subsection_title) + '}')
            latex_lines.append('')
        elif line.startswith('#### '):
            para_title = line[5:].strip()
            latex_lines.append(r'\paragraph{' + escape_latex(para_title) + '}')
            latex_lines.append('')
        
        # Handle italic author line (e.g., *By Dr. Isuru Nawinne*)
        elif line.strip().startswith('*By ') and line.strip().endswith('*'):
            author = line.strip()[1:-1]  # Remove surrounding *
            latex_lines.append(r'\emph{' + escape_latex(author) + '}')
            latex_lines.append('')
        
        # Handle images
        elif line.strip().startswith('<img src='):
            # Extract image path
            match = re.search(r'<img src="([^"]+)"', line)
            if match:
                img_path = match.group(1)
                # Extract alt text if present
                alt_match = re.search(r'alt="([^"]+)"', line)
                caption = alt_match.group(1) if alt_match else ''
                
                latex_lines.append(r'\begin{figure}[h]')
                latex_lines.append(r'\centering')
                latex_lines.append(r'\includegraphics[width=0.7\textwidth]{' + img_path + '}')
                if caption:
                    latex_lines.append(r'\caption{' + escape_latex(caption) + '}')
                latex_lines.append(r'\end{figure}')
                latex_lines.append('')
        
        # Handle bold/italic text in regular lines
        elif line.strip() and not line.startswith('#'):
            # Process inline formatting
            processed_line = line
            
            # Handle **bold**
            processed_line = re.sub(r'\*\*([^\*]+)\*\*', r'\\textbf{\1}', processed_line)
            
            # Handle single * for italic (but not in middle of words)
            processed_line = re.sub(r'\*([^\*]+)\*', r'\\emph{\1}', processed_line)
            
            # Handle bullet points
            if processed_line.strip().startswith('- '):
                if not in_list:
                    latex_lines.append(r'\begin{itemize}')
                    in_list = True
                item_text = processed_line.strip()[2:]
                latex_lines.append(r'\item ' + item_text)
            else:
                if in_list:
                    latex_lines.append(r'\end{itemize}')
                    latex_lines.append('')
                    in_list = False
                
                # Regular text
                if processed_line.strip():
                    latex_lines.append(processed_line)
                else:
                    latex_lines.append('')
        else:
            # Empty line or already handled
            if in_list and not line.strip():
                latex_lines.append(r'\end{itemize}')
                latex_lines.append('')
                in_list = False
            elif not line.strip():
                latex_lines.append('')
        
        i += 1
    
    # Close any open lists
    if in_list:
        latex_lines.append(r'\end{itemize}')
    
    return '\n'.join(latex_lines)

def process_all_lectures():
    """Process all markdown lecture files."""
    # Ensure output directory exists
    os.makedirs(LATEX_DIR, exist_ok=True)
    
    # Get all markdown files and sort by lecture number
    md_files = [f for f in os.listdir(MARKDOWN_DIR) if f.endswith('.md')]
    
    # Sort files by lecture number using the mapping
    md_files_sorted = sorted(md_files, key=lambda x: LECTURE_MAPPING.get(x, 999))
    
    print(f"Found {len(md_files_sorted)} markdown files")
    
    for md_file in md_files_sorted:
        lecture_num = LECTURE_MAPPING.get(md_file, 0)
        if lecture_num == 0:
            print(f"⚠️  Skipping unknown file: {md_file}")
            continue
        
        print(f"Processing Lecture {lecture_num}: {md_file}")
        
        # Read markdown content
        md_path = os.path.join(MARKDOWN_DIR, md_file)
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert to LaTeX
        latex_content = convert_markdown_to_latex(md_content)
        
        # Create output filename
        latex_filename = f"lecture-{lecture_num:02d}.tex"
        latex_path = os.path.join(LATEX_DIR, latex_filename)
        
        # Write LaTeX file
        with open(latex_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"  → Created {latex_filename}")
    
    print(f"\n✅ Successfully created all 20 LaTeX files!")
    print(f"Output directory: {LATEX_DIR}")

if __name__ == '__main__':
    process_all_lectures()
