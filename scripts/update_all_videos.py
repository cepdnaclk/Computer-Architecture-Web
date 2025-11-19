import re

# Video link HTML template
video_links_template = '''                <div class="lecture-links">
                  <a href="#video-{num}" class="lecture-link-btn video-link" target="_blank">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polygon points="5 3 19 12 5 21 5 3"></polygon>
                    </svg>
                    Watch Video
                  </a>
                  <a href="Lectures/html/lecture-{num}.html" class="lecture-link-btn notes-link">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                      <polyline points="14 2 14 8 20 8"></polyline>
                    </svg>
                    Read Notes
                  </a>
                </div>'''

# Read the file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Lectures that need updating (those without video links already)
lectures_to_update = [3, 4, 5, 7, 9, 11, 12, 13, 14, 15, 16, 17, 20]

for num in lectures_to_update:
    num_str = f'{num:02d}'
    
    # Pattern to find lecture cards without video links
    pattern = rf'(<div class="lecture-number">{num_str}</div>\s*<div class="lecture-content">.*?</p>\s*)(</div>\s*</div>)'
    
    match = re.search(pattern, content, re.DOTALL)
    if match:
        # Check if video links already exist
        if 'lecture-links' not in match.group(0):
            # Insert video links before the closing divs
            video_html = video_links_template.format(num=num_str)
            replacement = match.group(1) + video_html + '\n              ' + match.group(2)
            content = content.replace(match.group(0), replacement)
            print(f"Added video links to lecture {num_str}")
        else:
            print(f"Lecture {num_str} already has video links")
    else:
        print(f"Could not find lecture {num_str}")

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✓ All lectures updated with video links!")
