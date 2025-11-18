import re
import os

def update_lecture_numbering(lecture_num, file_path):
    """Update section numbering for a single lecture file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Track what sections we've seen
    section_counter = 1
    
    def replace_section(match):
        nonlocal section_counter
        old_num = match.group(1)
        heading_text = match.group(2)
        
        # Skip "Introduction", "Key Takeaways", "Summary"
        if heading_text.strip() in ['Introduction', 'Key Takeaways', 'Summary']:
            if heading_text.strip() == 'Introduction':
                return f"## {lecture_num}.1 Introduction"
            else:
                return match.group(0)  # Don't change Key Takeaways or Summary
        
        # This is a numbered section
        result = f"## {lecture_num}.{section_counter + 1} {heading_text}"
        section_counter += 1
        return result
    
    # First, handle Introduction if it exists
    content = re.sub(r'^## Introduction$', f'## {lecture_num}.1 Introduction', content, flags=re.MULTILINE)
    
    # Replace main sections (## 1., ## 2., etc.)
    # Pattern: ## followed by number and dot, then space and text
    content = re.sub(r'^## (\d+)\. (.+)$', replace_section, content, flags=re.MULTILINE)
    
    # Now update all subsections (### 1.1, ### 1.2, etc.)
    # We need to track which main section we're in
    lines = content.split('\n')
    result_lines = []
    current_main_section = None
    current_subsection_map = {}
    
    for line in lines:
        # Check if this is a main section header
        main_section_match = re.match(r'^## ' + str(lecture_num) + r'\.(\d+) ', line)
        if main_section_match:
            current_main_section = main_section_match.group(1)
            current_subsection_map = {}
            result_lines.append(line)
            continue
        
        # Check if this is a subsection
        subsection_match = re.match(r'^### (\d+)\.(\d+) (.+)$', line)
        if subsection_match and current_main_section:
            old_main = subsection_match.group(1)
            old_sub = subsection_match.group(2)
            heading_text = subsection_match.group(3)
            
            # Create new numbering
            key = (old_main, old_sub)
            if key not in current_subsection_map:
                current_subsection_map[key] = len(current_subsection_map) + 1
            
            new_line = f"### {lecture_num}.{current_main_section}.{current_subsection_map[key]} {heading_text}"
            result_lines.append(new_line)
            continue
        
        result_lines.append(line)
    
    content = '\n'.join(result_lines)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated Lecture {lecture_num}")

# Update all lectures 2-20
lectures_dir = r"d:\Academics\Projects\isuru sir\CO224-Web\Lectures\markdown"

for i in range(2, 21):
    file_path = os.path.join(lectures_dir, f"Lecture {i} - *.md")
    # Find the actual file
    import glob
    files = glob.glob(file_path)
    if files:
        update_lecture_numbering(i, files[0])
    else:
        print(f"File not found for Lecture {i}")

print("All lectures updated!")
