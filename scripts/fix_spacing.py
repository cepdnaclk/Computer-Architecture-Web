import re
import os

# Directory containing the lecture .tex files
LATEX_DIR = r"d:\Academics\Projects\isuru sir\CO224-Web\Lectures\latex"

def fix_spacing(content):
    """
    Fix excessive blank lines in LaTeX files:
    1. Reduce 3+ consecutive blank lines to 2
    2. Ensure consistent spacing after section headers
    """
    
    # Replace 3 or more consecutive blank lines with exactly 2
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # Ensure consistent spacing: section command followed by max 1 blank line before content
    # This applies to \paragraph, \subsubsection, \subsection, \section
    content = re.sub(r'(\\(?:sub)*section\{[^}]+\})\n\n\n+', r'\1\n\n', content)
    content = re.sub(r'(\\paragraph\{[^}]+\})\n\n\n+', r'\1\n\n', content)
    
    return content

def fix_lecture_file(filepath):
    """Fix a single lecture file."""
    print(f"Processing {os.path.basename(filepath)}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix spacing
    content = fix_spacing(content)
    
    # Check if anything changed
    if content != original_content:
        # Write back the fixed content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed spacing in {os.path.basename(filepath)}")
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
