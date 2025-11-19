import re
import os

# Directory containing the lecture .tex files
LATEX_DIR = r"d:\Academics\Projects\isuru sir\CO224-Web\Lectures\latex"

def fix_itemize_formatting(content):
    """
    Fix itemize environment formatting issues:
    1. Ensure proper spacing around itemize environments
    2. Remove extra blank lines within itemize
    3. Ensure consistent item formatting
    """
    
    # Remove blank lines immediately after \begin{itemize}
    content = re.sub(r'(\\begin\{itemize\})\n\n+', r'\1\n', content)
    
    # Remove blank lines immediately before \end{itemize}
    content = re.sub(r'\n\n+(\\end\{itemize\})', r'\n\1', content)
    
    # Remove blank lines between \item entries (keep single newline)
    content = re.sub(r'(\\item [^\n]+)\n\n+(\\item )', r'\1\n\2', content)
    
    # Remove blank lines immediately after \begin{enumerate}
    content = re.sub(r'(\\begin\{enumerate\})\n\n+', r'\1\n', content)
    
    # Remove blank lines immediately before \end{enumerate}
    content = re.sub(r'\n\n+(\\end\{enumerate\})', r'\n\1', content)
    
    # Remove blank lines between enumerate items
    content = re.sub(r'(\\item [^\n]+)\n\n+(\\item )', r'\1\n\2', content)
    
    return content

def fix_lecture_file(filepath):
    """Fix a single lecture file."""
    print(f"Processing {os.path.basename(filepath)}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix itemize formatting
    content = fix_itemize_formatting(content)
    
    # Check if anything changed
    if content != original_content:
        # Write back the fixed content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed itemize formatting in {os.path.basename(filepath)}")
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
