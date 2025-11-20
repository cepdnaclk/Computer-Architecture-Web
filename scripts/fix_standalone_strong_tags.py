import re
import sys

def fix_standalone_strong_tags(filepath):
    """Fix standalone <strong> tags by wrapping them in <p> tags"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match standalone strong tags (not already in a paragraph)
    # Matches: \n<strong>...</strong>\n but not when preceded by <p> or <li>
    pattern = r'\n(<strong>.*?</strong>)\n'
    
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Check if line is a standalone strong tag
        if line.strip().startswith('<strong>') and line.strip().endswith('</strong>'):
            # Check previous line to see if we should wrap
            prev_line = lines[i-1].strip() if i > 0 else ''
            
            # Don't wrap if it's already in a paragraph or list item
            if not prev_line.endswith('>') or prev_line.endswith('</ul>') or prev_line.endswith('</ol>') or prev_line == '':
                # Wrap in paragraph tag
                fixed_lines.append(f'<p>{line.strip()}</p>')
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))
    
    print(f"Fixed standalone <strong> tags in {filepath}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fix_standalone_strong_tags(sys.argv[1])
    else:
        print("Usage: python fix_standalone_strong_tags.py <filepath>")
