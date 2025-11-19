"""
Advanced Markdown to LaTeX converter for lecture notes.
Handles complex markdown syntax while preserving exact content.
"""

import os
import re
from pathlib import Path

MARKDOWN_DIR = Path(r"d:\Academics\Projects\isuru sir\CO224-Web\Lectures\markdown")
LATEX_DIR = Path(r"d:\Academics\Projects\isuru sir\CO224-Web\Lectures\latex")

# Correct lecture order mapping
LECTURE_ORDER = [
    "Lecture 1 - Computer Abstractions.md",
    "Lecture 2 - Technology Trends.md",
    "Lecture 3 - Understanding Performance.md",
    "Lecture 4 - Introduction to ARM Assembly.md",
    "Lecture 5 - Number Representation and Data Processing.md",
    "Lecture 6 - Branching.md",
    "Lecture 7 - Function Call and Return.md",
    "Lecture 8 - Memory Access.md",
    "Lecture 9 - Microarchitecture and Datapath.md",
    "Lecture 10 - Processor Control.md",
    "Lecture 11 - Single-Cycle Execution.md",
    "Lecture 12 - Pipelined Processors.md",
    "Lecture 13 - Pipeline Operation and Timing.md",
    "Lecture 14 - Memory Hierarchy and Caching.md",
    "Lecture 15 - Direct Mapped Cache Control.md",
    "Lecture 16 - Associative Cache Control.md",
    "Lecture 17 - Multi-Level Caching.md",
    "Lecture 18 - Virtual Memory.md",
    "Lecture 19 - Multiprocessors.md",
    "Lecture 20 - Storage and Interfacing.md",
]


class MarkdownToLatexConverter:
    def __init__(self):
        self.in_code_block = False
        self.in_list = False
        self.in_table = False
        self.list_stack = []
        
    def escape_text(self, text):
        """Escape special LaTeX characters."""
        # Special characters that need escaping
        text = text.replace('\\', r'\textbackslash{}')
        text = text.replace('&', r'\&')
        text = text.replace('%', r'\%')
        text = text.replace('$', r'\$')
        text = text.replace('#', r'\#')
        text = text.replace('_', r'\_')
        text = text.replace('{', r'\{')
        text = text.replace('}', r'\}')
        text = text.replace('~', r'\textasciitilde{}')
        text = text.replace('^', r'\textasciicircum{}')
        return text
    
    def process_inline_formatting(self, text):
        """Process inline markdown formatting (bold, italic, code)."""
        # Don't process if we're in a code block
        if self.in_code_block:
            return text
        
        # Handle inline code first (to avoid processing markdown inside code)
        text = re.sub(r'`([^`]+)`', r'\\texttt{\1}', text)
        
        # Handle bold (**text**)
        text = re.sub(r'\*\*([^\*]+)\*\*', lambda m: r'\textbf{' + self.escape_text(m.group(1)) + '}', text)
        
        # Handle italic (*text* but not ** and not in middle of word)
        text = re.sub(r'(?<!\*)\*(?!\*)([^\*]+)\*(?!\*)', lambda m: r'\emph{' + self.escape_text(m.group(1)) + '}', text)
        
        # Handle arrows
        text = text.replace('→', r'$\rightarrow$')
        text = text.replace('←', r'$\leftarrow$')
        text = text.replace('↔', r'$\leftrightarrow$')
        
        # Handle special symbols
        text = text.replace('×', r'$\times$')
        text = text.replace('÷', r'$\div$')
        text = text.replace('≤', r'$\leq$')
        text = text.replace('≥', r'$\geq$')
        text = text.replace('≠', r'$\neq$')
        
        return text
    
    def convert_line(self, line):
        """Convert a single line of markdown to LaTeX."""
        result = []
        
        # Handle code block delimiters
        if line.strip().startswith('```'):
            if not self.in_code_block:
                self.in_code_block = True
                # Check if language is specified
                lang = line.strip()[3:].strip()
                if lang:
                    result.append(f'\\begin{{lstlisting}}[language={lang}]')
                else:
                    result.append(r'\begin{verbatim}')
            else:
                if '\\begin{lstlisting}' in str(result):
                    result.append(r'\end{lstlisting}')
                else:
                    result.append(r'\end{verbatim}')
                self.in_code_block = False
            return result
        
        # If in code block, return line as-is
        if self.in_code_block:
            return [line]
        
        # Handle headings
        if line.startswith('# '):
            title = line[2:].strip().replace('*', '')
            return [f'\\section{{{self.escape_text(title)}}}', '']
        elif line.startswith('## '):
            title = line[3:].strip()
            return [f'\\subsection{{{self.escape_text(title)}}}', '']
        elif line.startswith('### '):
            title = line[4:].strip()
            return [f'\\subsubsection{{{self.escape_text(title)}}}', '']
        elif line.startswith('#### '):
            title = line[5:].strip()
            return [f'\\paragraph{{{self.escape_text(title)}}}', '']
        
        # Handle author line (e.g., *By Dr. Isuru Nawinne*)
        if re.match(r'^\*By [^\*]+\*$', line.strip()):
            author = line.strip()[1:-1]
            return [f'\\emph{{{self.escape_text(author)}}}', '']
        
        # Handle images
        img_match = re.search(r'<img src="([^"]+)"[^>]*alt="([^"]+)"[^>]*>', line)
        if img_match:
            img_path = img_match.group(1)
            caption = img_match.group(2)
            return [
                r'\begin{figure}[h]',
                r'\centering',
                f'\\includegraphics[width=0.7\\textwidth]{{{img_path}}}',
                f'\\caption{{{self.escape_text(caption)}}}',
                r'\end{figure}',
                ''
            ]
        
        # Handle lists
        if line.strip().startswith('- '):
            if not self.in_list:
                result.append(r'\begin{itemize}')
                self.in_list = True
            item_text = line.strip()[2:]
            processed_text = self.process_inline_formatting(item_text)
            result.append(f'\\item {processed_text}')
            return result
        elif line.strip().startswith(('1. ', '2. ', '3. ', '4. ', '5. ', '6. ', '7. ', '8. ', '9. ')):
            # Numbered list
            if not self.in_list or 'enumerate' not in str(self.list_stack):
                if self.in_list:
                    result.append(r'\end{itemize}')
                result.append(r'\begin{enumerate}')
                self.in_list = True
                self.list_stack.append('enumerate')
            item_text = re.sub(r'^\d+\.\s+', '', line.strip())
            processed_text = self.process_inline_formatting(item_text)
            result.append(f'\\item {processed_text}')
            return result
        else:
            # Not a list item, close list if open
            if self.in_list:
                if self.list_stack and self.list_stack[-1] == 'enumerate':
                    result.append(r'\end{enumerate}')
                    self.list_stack.pop()
                else:
                    result.append(r'\end{itemize}')
                result.append('')
                self.in_list = False
        
        # Handle horizontal rules
        if line.strip() in ['---', '***', '___']:
            return [r'\hrule', '']
        
        # Handle blank lines
        if not line.strip():
            return ['']
        
        # Handle regular text paragraphs
        processed_line = self.process_inline_formatting(line)
        result.append(processed_line)
        
        return result
    
    def convert(self, markdown_text):
        """Convert entire markdown document to LaTeX."""
        lines = markdown_text.split('\n')
        latex_lines = []
        
        for line in lines:
            converted = self.convert_line(line)
            latex_lines.extend(converted)
        
        # Close any open environments
        if self.in_list:
            if self.list_stack and self.list_stack[-1] == 'enumerate':
                latex_lines.append(r'\end{enumerate}')
            else:
                latex_lines.append(r'\end{itemize}')
        if self.in_code_block:
            latex_lines.append(r'\end{verbatim}')
        
        return '\n'.join(latex_lines)


def main():
    """Convert all markdown lectures to LaTeX."""
    # Ensure output directory exists
    LATEX_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Converting {len(LECTURE_ORDER)} lectures to LaTeX...")
    print(f"Input: {MARKDOWN_DIR}")
    print(f"Output: {LATEX_DIR}\n")
    
    for idx, filename in enumerate(LECTURE_ORDER, 1):
        print(f"[{idx:2d}/20] Processing: {filename}")
        
        # Read markdown file
        md_file = MARKDOWN_DIR / filename
        if not md_file.exists():
            print(f"  ⚠️  File not found: {filename}")
            continue
        
        with open(md_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert to LaTeX
        converter = MarkdownToLatexConverter()
        latex_content = converter.convert(markdown_content)
        
        # Write LaTeX file
        latex_file = LATEX_DIR / f"lecture-{idx:02d}.tex"
        with open(latex_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"         → Created: lecture-{idx:02d}.tex")
    
    print(f"\n✅ Successfully created all 20 LaTeX files in {LATEX_DIR}")


if __name__ == '__main__':
    main()
