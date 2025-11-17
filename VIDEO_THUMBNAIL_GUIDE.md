# YouTube Video Thumbnail Configuration Guide

All lecture pages now display YouTube video thumbnails at the beginning. The thumbnails use placeholder VIDEO_IDs that need to be replaced with actual YouTube video IDs.

## Current Setup

Each lecture page has a video thumbnail section that looks like this:

```html
<img src="https://img.youtube.com/vi/VIDEO_ID_01/maxresdefault.jpg" 
     alt="Lecture 1 Video Thumbnail"
     onerror="this.src='https://img.youtube.com/vi/VIDEO_ID_01/hqdefault.jpg'">
```

## How to Update Video IDs

### Option 1: Manual Update in Each HTML File

Edit each file in `Lectures/html/lecture-XX.html` and replace `VIDEO_ID_XX` with the actual YouTube video ID.

For example, if Lecture 1 video is at: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

Replace:
```html
VIDEO_ID_01
```

With:
```html
dQw4w9WgXcQ
```

### Option 2: Bulk Update Script

Create a Python script with your video IDs:

```python
import re
from pathlib import Path

# Dictionary mapping lecture numbers to YouTube video IDs
video_ids = {
    '01': 'YOUR_VIDEO_ID_HERE',  # Lecture 1: Computer Abstractions
    '02': 'YOUR_VIDEO_ID_HERE',  # Lecture 2: Technology Trends
    '03': 'YOUR_VIDEO_ID_HERE',  # Lecture 3: Understanding Performance
    '04': 'YOUR_VIDEO_ID_HERE',  # Lecture 4: Introduction to ARM Assembly
    '05': 'YOUR_VIDEO_ID_HERE',  # Lecture 5: Number Representation and Data Processing
    '06': 'YOUR_VIDEO_ID_HERE',  # Lecture 6: Branching
    '07': 'YOUR_VIDEO_ID_HERE',  # Lecture 7: Function Call and Return
    '08': 'YOUR_VIDEO_ID_HERE',  # Lecture 8: Memory Access
    '09': 'YOUR_VIDEO_ID_HERE',  # Lecture 9: Microarchitecture and Datapath
    '10': 'YOUR_VIDEO_ID_HERE',  # Lecture 10: Processor Control
    '11': 'YOUR_VIDEO_ID_HERE',  # Lecture 11: Single-Cycle Execution
    '12': 'YOUR_VIDEO_ID_HERE',  # Lecture 12: Pipelined Processors
    '13': 'YOUR_VIDEO_ID_HERE',  # Lecture 13: Pipeline Operation and Timing
    '14': 'YOUR_VIDEO_ID_HERE',  # Lecture 14: Memory Hierarchy and Caching
    '15': 'YOUR_VIDEO_ID_HERE',  # Lecture 15: Direct Mapped Cache Control
    '16': 'YOUR_VIDEO_ID_HERE',  # Lecture 16: Associative Cache Control
    '17': 'YOUR_VIDEO_ID_HERE',  # Lecture 17: Multi-Level Caching
    '18': 'YOUR_VIDEO_ID_HERE',  # Lecture 18: Virtual Memory
    '19': 'YOUR_VIDEO_ID_HERE',  # Lecture 19: Multiprocessors
    '20': 'YOUR_VIDEO_ID_HERE',  # Lecture 20: Storage and Interfacing
}

# Update all lecture files
html_dir = Path('Lectures/html')
for num, video_id in video_ids.items():
    file_path = html_dir / f'lecture-{num}.html'
    
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace placeholder with actual video ID
        content = content.replace(f'VIDEO_ID_{num}', video_id)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'✓ Updated lecture-{num}.html')
    else:
        print(f'✗ File not found: lecture-{num}.html')

print('\nAll video IDs updated successfully!')
```

### Option 3: Update via convert_lectures.py

You can also modify `convert_lectures.py` to include the video IDs directly. Add a dictionary at the top:

```python
VIDEO_IDS = {
    1: 'YOUR_VIDEO_ID_HERE',
    2: 'YOUR_VIDEO_ID_HERE',
    # ... etc
}
```

Then in the `create_lecture_html` function, replace:
```python
<img src="https://img.youtube.com/vi/VIDEO_ID_{lecture_num:02d}/maxresdefault.jpg"
```

With:
```python
<img src="https://img.youtube.com/vi/{VIDEO_IDS.get(lecture_num, f'VIDEO_ID_{lecture_num:02d}')}/maxresdefault.jpg"
```

Then run `python convert_lectures.py` to regenerate all pages.

## How to Get YouTube Video IDs

From a YouTube URL like: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

The video ID is: `dQw4w9WgXcQ` (the part after `v=`)

## Thumbnail Quality

The thumbnails use `maxresdefault.jpg` (1280x720) by default, with a fallback to `hqdefault.jpg` (480x360) if the high-quality version doesn't exist.

Available thumbnail sizes:
- `maxresdefault.jpg` - 1280x720 (best quality)
- `sddefault.jpg` - 640x480
- `hqdefault.jpg` - 480x360
- `mqdefault.jpg` - 320x180
- `default.jpg` - 120x90

## Features

✓ **Clickable thumbnails** - Click to open video in YouTube
✓ **Play button overlay** - YouTube-style play button
✓ **Hover effects** - Thumbnail lifts and scales on hover
✓ **Responsive design** - Works on all screen sizes
✓ **Fallback images** - Automatically falls back to lower quality if high-res not available
✓ **Visual notice** - Helpful text prompting users to click
