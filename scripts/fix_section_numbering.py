import re
import os

# Directory containing the lecture .tex files
LATEX_DIR = r"d:\Academics\Projects\isuru sir\CO224-Web\Lectures\latex"

def remove_manual_numbering(content):
    """
    Remove manual numbering from LaTeX section commands.
    E.g., \subsection{1.3 Title} -> \subsection{Title}
          \subsubsection{1.3.2 Title} -> \subsubsection{Title}
    """
    # Pattern to match section commands with manual numbering
    # Matches: \section{1.2 Title}, \subsection{1.2.3 Title}, etc.
    pattern = r'(\\(?:section|subsection|subsubsection)\{)(\d+(?:\.\d+)*)\s+'
    
    # Replace with just the section command and title (remove the number)
    fixed_content = re.sub(pattern, r'\1', content)
    
    return fixed_content

def fix_lecture_file(filepath):
    """Fix a single lecture file."""
    print(f"Processing {os.path.basename(filepath)}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove manual numbering
    fixed_content = remove_manual_numbering(content)
    
    # Check if anything changed
    if content != fixed_content:
        # Write back the fixed content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"  ✓ Fixed numbering in {os.path.basename(filepath)}")
        return True
    else:
        print(f"  - No changes needed in {os.path.basename(filepath)}")
        return False

def main():
    """Fix all lecture files."""
    files_fixed = 0
    
    for i in range(1, 21):
        filepath = os.path.join(LATEX_DIR, f'lecture-{i:02d}.tex')
        if os.path.exists(filepath):
            if fix_lecture_file(filepath):
                files_fixed += 1
    
    print(f"\n✓ Complete! Fixed {files_fixed} lecture files.")

if __name__ == '__main__':
    main()
