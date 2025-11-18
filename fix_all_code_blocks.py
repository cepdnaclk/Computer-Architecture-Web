import os
import glob

def fix_code_blocks_in_file(filepath):
    """Fix code blocks by wrapping language identifiers with proper markdown syntax."""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    changes = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this line is a language identifier (assembly, c, bash, python, verilog)
        lang_match = line.strip()
        
        if lang_match in ['assembly', 'c', 'bash', 'python', 'verilog', 'Assembly']:
            # Check if next line(s) start with spaces (indented code)
            if i + 1 < len(lines) and lines[i + 1].startswith(('    ', '\t')):
                # This is an unformatted code block
                # Convert language name to lowercase for consistency
                lang = lang_match.lower()
                
                # Add opening fence
                new_lines.append(f'```{lang}\n')
                i += 1
                
                # Collect all indented lines (the code)
                while i < len(lines) and lines[i].startswith(('    ', '\t')):
                    new_lines.append(lines[i])
                    i += 1
                
                # Add closing fence
                new_lines.append('```\n')
                changes += 1
                continue
        
        # Not a code block, just add the line as-is
        new_lines.append(line)
        i += 1
    
    if changes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True, changes
    
    return False, 0

def main():
    lecture_dir = 'Lectures/markdown'
    pattern = os.path.join(lecture_dir, '*.md')
    files = sorted(glob.glob(pattern))
    
    total_files = 0
    total_blocks = 0
    
    print("Processing lecture files...")
    print("=" * 70)
    
    for filepath in files:
        filename = os.path.basename(filepath)
        updated, num_changes = fix_code_blocks_in_file(filepath)
        
        if updated:
            print(f"✓ {filename:<50} {num_changes} blocks fixed")
            total_files += 1
            total_blocks += num_changes
        else:
            print(f"  {filename:<50} (no changes)")
    
    print("=" * 70)
    print(f"\nSummary:")
    print(f"  Files updated: {total_files}/{len(files)}")
    print(f"  Code blocks fixed: {total_blocks}")
    print(f"\n✓ All done!")

if __name__ == '__main__':
    main()
