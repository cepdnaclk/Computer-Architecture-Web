import re

# Read the index.html file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match lecture cards (lectures 02-20, since we already did 01)
pattern = r'(<div class="lecture-card">\s*<div class="lecture-number">(\d+)</div>\s*<div class="lecture-content">\s*<h4>\s*<a href="Lectures/html/lecture-(\d+)\.html"[^>]*>(.*?)</a>\s*</h4>\s*<p>(.*?)</p>\s*</div>\s*</div>)'

def replace_card(match):
    full_match = match.group(0)
    lecture_num = match.group(2)
    lecture_file_num = match.group(3)
    title = match.group(4)
    description = match.group(5)
    
    # Create new card with video links
    new_card = f'''<div class="lecture-card">
              <div class="lecture-number">{lecture_num}</div>
              <div class="lecture-content">
                <h4>
                  <a href="Lectures/html/lecture-{lecture_file_num}.html"
                    >{title}</a
                  >
                </h4>
                <p>{description}</p>
                <div class="lecture-links">
                  <a href="#video-{lecture_file_num}" class="lecture-link-btn video-link" target="_blank">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polygon points="5 3 19 12 5 21 5 3"></polygon>
                    </svg>
                    Watch Video
                  </a>
                  <a href="Lectures/html/lecture-{lecture_file_num}.html" class="lecture-link-btn notes-link">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                      <polyline points="14 2 14 8 20 8"></polyline>
                    </svg>
                    Read Notes
                  </a>
                </div>
              </div>
            </div>'''
    
    return new_card

# Replace all lecture cards (except the first one which we already did)
# We need to be more specific to avoid replacing lecture 01
for i in range(2, 21):
    lecture_num_str = f'{i:02d}'
    
    # More specific pattern for each lecture
    specific_pattern = rf'(<div class="lecture-card">\s*<div class="lecture-number">{i:02d}</div>.*?</div>\s*</div>)'
    
    matches = list(re.finditer(specific_pattern, content, re.DOTALL))
    
    if matches:
        match = matches[0]
        # Extract the inner content more carefully
        inner_match = re.search(
            rf'<div class="lecture-number">{i:02d}</div>\s*<div class="lecture-content">\s*<h4>\s*<a href="Lectures/html/lecture-{lecture_num_str}\.html"[^>]*>(.*?)</a>\s*</h4>\s*<p>(.*?)</p>',
            match.group(0),
            re.DOTALL
        )
        
        if inner_match:
            title = inner_match.group(1).strip()
            description = inner_match.group(2).strip()
            
            new_card = f'''<div class="lecture-card">
              <div class="lecture-number">{i:02d}</div>
              <div class="lecture-content">
                <h4>
                  <a href="Lectures/html/lecture-{lecture_num_str}.html"
                    >{title}</a
                  >
                </h4>
                <p>{description}</p>
                <div class="lecture-links">
                  <a href="#video-{lecture_num_str}" class="lecture-link-btn video-link" target="_blank">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polygon points="5 3 19 12 5 21 5 3"></polygon>
                    </svg>
                    Watch Video
                  </a>
                  <a href="Lectures/html/lecture-{lecture_num_str}.html" class="lecture-link-btn notes-link">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                      <polyline points="14 2 14 8 20 8"></polyline>
                    </svg>
                    Read Notes
                  </a>
                </div>
              </div>
            </div>'''
            
            content = content.replace(match.group(0), new_card)
            print(f"Updated lecture {i:02d}: {title}")

# Write the updated content
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nAll lecture cards updated with video links!")
