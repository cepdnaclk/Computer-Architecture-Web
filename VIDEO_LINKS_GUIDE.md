# Video Links Configuration

All lecture cards now have placeholders for video links. The video link buttons use the format:

```html
<a href="#video-XX" class="lecture-link-btn video-link" target="_blank"></a>
```

## How to Update Video Links

Edit `index.html` and replace the placeholder links with actual YouTube URLs:

### Current Placeholders (Replace these):

- Lecture 01: `#video-01` → Replace with actual YouTube URL
- Lecture 02: `#video-02` → Replace with actual YouTube URL
- Lecture 03: `#video-03` → Replace with actual YouTube URL
- Lecture 04: `#video-04` → Replace with actual YouTube URL
- Lecture 05: `#video-05` → Replace with actual YouTube URL
- Lecture 06: `#video-06` → Replace with actual YouTube URL
- Lecture 07: `#video-07` → Replace with actual YouTube URL
- Lecture 08: `#video-08` → Replace with actual YouTube URL
- Lecture 09: `#video-09` → Replace with actual YouTube URL
- Lecture 10: `#video-10` → Replace with actual YouTube URL
- Lecture 11: `#video-11` → Replace with actual YouTube URL
- Lecture 12: `#video-12` → Replace with actual YouTube URL
- Lecture 13: `#video-13` → Replace with actual YouTube URL
- Lecture 14: `#video-14` → Replace with actual YouTube URL
- Lecture 15: `#video-15` → Replace with actual YouTube URL
- Lecture 16: `#video-16` → Replace with actual YouTube URL
- Lecture 17: `#video-17` → Replace with actual YouTube URL
- Lecture 18: `#video-18` → Replace with actual YouTube URL
- Lecture 19: `#video-19` → Replace with actual YouTube URL
- Lecture 20: `#video-20` → Replace with actual YouTube URL

## Example

Find this in `index.html`:

```html
<a href="#video-01" class="lecture-link-btn video-link" target="_blank"></a>
```

Replace with actual YouTube URL:

```html
<a
  href="https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
  class="lecture-link-btn video-link"
  target="_blank"
></a>
```

## Bulk Update Script

You can also use this Python script to update all videos at once:

```python
video_urls = {
    '01': 'https://www.youtube.com/watch?v=...',
    '02': 'https://www.youtube.com/watch?v=...',
    # ... add all 20 URLs
}

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

for num, url in video_urls.items():
    content = content.replace(f'#video-{num}', url)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
```

## Changes Made

1. ✅ Changed all "CO224" references to "Lectures on Computer Architecture"
2. ✅ Updated page titles (index.html and all lecture pages)
3. ✅ Added video link buttons to all 20 lectures
4. ✅ Added "Read Notes" buttons alongside video links
5. ✅ Updated LaTeX document title
6. ✅ Regenerated all HTML lecture pages with new branding
