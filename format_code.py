import re
import glob
import os

def format_code_blocks(filepath):
    """Format code blocks in markdown files by adding proper language identifiers."""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = []
    
    # Pattern: Language identifier on own line followed by indented code (4+ spaces)
    # Match: \nlanguage\n then lines starting with 4+ spaces
    patterns = [
        (r'(?<=\n)assembly\n((?:[ \t]{4,}.*\n)+)', r'```assembly\n\1```\n', 'assembly blocks'),
        (r'(?<=\n)c\n((?:[ \t]{4,}.*\n)+)', r'```c\n\1```\n', 'c blocks'),
        (r'(?<=\n)bash\n((?:[ \t]{4,}.*\n)+)', r'```bash\n\1```\n', 'bash blocks'),
        (r'(?<=\n)python\n((?:[ \t]{4,}.*\n)+)', r'```python\n\1```\n', 'python blocks'),
        (r'(?<=\n)verilog\n((?:[ \t]{4,}.*\n)+)', r'```verilog\n\1```\n', 'verilog blocks'),
        (r'(?<=\n)Assembly \(\.s\)\n((?:[ \t]{4,}.*\n)+)', r'```assembly\n\1```\n', 'Assembly (.s) blocks'),
        (r'(?<=\n)Assembly\n((?:[ \t]{4,}.*\n)+)', r'```assembly\n\1```\n', 'Assembly blocks'),
    ]
    
    for pattern, replacement, desc in patterns:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            changes_made.append(f"Fixed {desc}")
            content = new_content
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes_made
    
    return False, []

def main():
    lecture_files = glob.glob('Lectures/markdown/*.md')
    
    total_updated = 0
    for filepath in sorted(lecture_files):
        filename = os.path.basename(filepath)
        updated, changes = format_code_blocks(filepath)
        
        if updated:
            print(f"✓ {filename}")
            for change in changes:
                print(f"  - {change}")
            total_updated += 1
        else:
            print(f"- {filename} (no changes)")
    
    print(f"\n{'='*60}")
    print(f"Updated {total_updated} out of {len(lecture_files)} files")

if __name__ == '__main__':
    main()
