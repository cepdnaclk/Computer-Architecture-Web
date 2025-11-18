import re
from pathlib import Path
from collections import defaultdict

def check_duplicate_subsections(file_path):
    """Check for duplicate subsection numbering in a lecture file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    subsection_pattern = re.compile(r'^###\s+(\d+)\.(\d+)\.(\d+)')
    main_section_pattern = re.compile(r'^##\s+(\d+)\.(\d+)')
    
    duplicates = []
    seen_subsections = defaultdict(list)
    current_main_section = None
    
    for line_num, line in enumerate(lines, 1):
        # Track main sections
        main_match = main_section_pattern.match(line)
        if main_match:
            lecture_num, section_num = main_match.groups()
            current_main_section = f"{lecture_num}.{section_num}"
            continue
        
        # Check subsections
        subsection_match = subsection_pattern.match(line)
        if subsection_match:
            lecture_num, section_num, subsection_num = subsection_match.groups()
            full_number = f"{lecture_num}.{section_num}.{subsection_num}"
            title = line.strip()
            
            # Check if this subsection number was already used
            if full_number in seen_subsections:
                prev_line, prev_title = seen_subsections[full_number][0]
                duplicates.append({
                    'number': full_number,
                    'line': line_num,
                    'title': title,
                    'previous_line': prev_line,
                    'previous_title': prev_title
                })
            
            seen_subsections[full_number].append((line_num, title))
    
    return duplicates

def main():
    lectures_dir = Path(r'd:\Academics\Projects\isuru sir\CO224-Web\Lectures\markdown')
    
    all_issues = {}
    
    # Check each lecture file
    for i in range(1, 21):
        lecture_files = list(lectures_dir.glob(f'Lecture {i} - *.md'))
        
        if lecture_files:
            file_path = lecture_files[0]
            duplicates = check_duplicate_subsections(file_path)
            
            if duplicates:
                all_issues[file_path.name] = duplicates
    
    # Print results
    if all_issues:
        print("DUPLICATE SUBSECTION NUMBERING FOUND:\n")
        print("=" * 80)
        
        for filename, duplicates in sorted(all_issues.items()):
            print(f"\n{filename}:")
            print("-" * 80)
            for dup in duplicates:
                print(f"  Duplicate: {dup['number']}")
                print(f"    First occurrence (line {dup['previous_line']}): {dup['previous_title']}")
                print(f"    Second occurrence (line {dup['line']}): {dup['title']}")
                print()
        
        print("=" * 80)
        print(f"\nTotal files with issues: {len(all_issues)}")
        print(f"Total duplicate subsections found: {sum(len(dups) for dups in all_issues.values())}")
    else:
        print("✓ No duplicate subsection numbering found in any lecture!")

if __name__ == '__main__':
    main()
