"""
Automated Video Links Update Script

This script updates video links in TWO locations:
1. Main page (index.html) - Video button links
2. Lecture pages (Lectures/html/*.html) - Video thumbnails and links

Usage:
1. Add your YouTube URLs or video IDs to the VIDEO_IDS dictionary below
2. Run: python update_video_links_complete.py

Note: You can provide either full YouTube URLs or just the video IDs.
The script will automatically extract the video ID from full URLs.
"""

import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# =============================================================================
# HELPER FUNCTION
# =============================================================================
def extract_video_id(url_or_id):
    """
    Extract video ID from YouTube URL or return as-is if already an ID.
    
    Examples:
    - 'https://www.youtube.com/watch?v=PNaYa-LZkt4' -> 'PNaYa-LZkt4'
    - 'https://www.youtube.com/watch?v=PNaYa-LZkt4&list=...' -> 'PNaYa-LZkt4'
    - 'PNaYa-LZkt4' -> 'PNaYa-LZkt4'
    """
    if not url_or_id or 'YOUR_VIDEO_ID_HERE' in url_or_id:
        return url_or_id
    
    # If it looks like a URL, parse it
    if 'youtube.com' in url_or_id or 'youtu.be' in url_or_id:
        try:
            # Handle youtube.com/watch?v=ID format
            if 'watch?v=' in url_or_id:
                parsed = urlparse(url_or_id)
                query_params = parse_qs(parsed.query)
                return query_params.get('v', [url_or_id])[0]
            # Handle youtu.be/ID format
            elif 'youtu.be/' in url_or_id:
                return url_or_id.split('youtu.be/')[-1].split('?')[0]
        except:
            pass
    
    # Otherwise assume it's already a video ID
    return url_or_id

# =============================================================================
# CONFIGURE YOUR VIDEO IDS HERE
# =============================================================================
# You can provide either:
# - Full YouTube URL: 'https://www.youtube.com/watch?v=VIDEO_ID'
# - Just the video ID: 'VIDEO_ID'
# The script will handle both formats automatically.

VIDEO_IDS = {
    '01': 'https://www.youtube.com/watch?v=PNaYa-LZkt4',  # Lecture 1: Computer Abstractions
    '02': 'https://www.youtube.com/watch?v=Fy2u9oCNZ1E',  # Lecture 2: Technology Trends
    '03': 'https://www.youtube.com/watch?v=nhwsAOEidik',  # Lecture 3: Understanding Performance
    '04': 'https://www.youtube.com/watch?v=s1X7Rr7rzag',  # Lecture 4: Introduction to ARM Assembly
    '05': 'https://www.youtube.com/watch?v=rCS3oXcQPKo',  # Lecture 5: Number Representation and Data Processing
    '06': 'https://www.youtube.com/watch?v=aFCmb1CNnV8',  # Lecture 6: Branching
    '07': 'https://www.youtube.com/watch?v=T99xSt2ryKs',  # Lecture 7: Function Call and Return
    '08': 'https://www.youtube.com/watch?v=IxaTbKoCr1Y',  # Lecture 8: Memory Access
    '09': 'https://www.youtube.com/watch?v=v9az9n9UUD4',  # Lecture 9: Microarchitecture and Datapath
    '10': 'https://www.youtube.com/watch?v=ZURjn6FyzkI',  # Lecture 10: Processor Control
    '11': 'https://www.youtube.com/watch?v=TegJ2TBihPw',  # Lecture 11: Single-Cycle Execution
    '12': 'https://www.youtube.com/watch?v=l3GqbXXB2QA',  # Lecture 12: Pipelined Processors
    '13': 'https://www.youtube.com/watch?v=JSZYac-xI5g',  # Lecture 13: Pipeline Operation and Timing
    '14': 'https://www.youtube.com/watch?v=vCbnFagcXjo',  # Lecture 14: Memory Hierarchy and Caching
    '15': 'https://www.youtube.com/watch?v=BJY8nzyNMAY',  # Lecture 15: Direct Mapped Cache Control
    '16': 'https://www.youtube.com/watch?v=eez7NbgXk9g',  # Lecture 16: Associative Cache Control
    '17': 'https://www.youtube.com/watch?v=p6BmMrDKmTE',  # Lecture 17: Multi-Level Caching
    '18': 'https://www.youtube.com/watch?v=O3hgbPAQhvE',  # Lecture 18: Virtual Memory
    '19': 'https://www.youtube.com/watch?v=EcjOuKKF5eE',  # Lecture 19: Multiprocessors
    '20': 'https://www.youtube.com/watch?v=hte_h1SxhYY',  # Lecture 20: Storage and Interfacing
}

# =============================================================================
# SCRIPT EXECUTION
# =============================================================================

def main():
    print("=" * 70)
    print("  YouTube Video Links Update Script")
    print("=" * 70)
    
    # Extract video IDs from URLs if needed
    processed_ids = {}
    for num, url_or_id in VIDEO_IDS.items():
        video_id = extract_video_id(url_or_id)
        processed_ids[num] = video_id
        if url_or_id != video_id and 'YOUR_VIDEO_ID_HERE' not in video_id:
            print(f"   Extracted ID for lecture {num}: {video_id}")
    
    VIDEO_IDS.update(processed_ids)
    
    # Check if any placeholder values remain
    placeholder_count = sum(1 for v in VIDEO_IDS.values() if 'YOUR_VIDEO_ID_HERE' in v)
    if placeholder_count > 0:
        print(f"\n⚠️  WARNING: {placeholder_count} video IDs still have placeholder values!")
        response = input("\nDo you want to continue anyway? (yes/no): ")
        if response.lower() != 'yes':
            print("\n❌ Update cancelled. Please add your video IDs first.")
            return
    
    print("\n📝 Updating video links in 2 locations...\n")
    
    # ==========================================================================
    # 1. Update index.html - Video button links
    # ==========================================================================
    print("1️⃣  Updating index.html (main page video buttons)...")
    
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            index_content = f.read()
        
        updated_count = 0
        for num, video_id in VIDEO_IDS.items():
            if 'YOUR_VIDEO_ID_HERE' in video_id:
                continue
                
            youtube_url = f'https://www.youtube.com/watch?v={video_id}'
            
            # Replace #video-XX with actual YouTube URL
            old_href = f'href="#video-{num}"'
            new_href = f'href="{youtube_url}"'
            
            if old_href in index_content:
                index_content = index_content.replace(old_href, new_href)
                updated_count += 1
                print(f'   ✓ Lecture {num}: Updated video button link')
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f'\n   ✅ Updated {updated_count} video button links in index.html\n')
        
    except Exception as e:
        print(f'\n   ❌ Error updating index.html: {e}\n')
        return
    
    # ==========================================================================
    # 2. Update lecture HTML pages - Thumbnails and links
    # ==========================================================================
    print("2️⃣  Updating lecture pages (video thumbnails and links)...")
    
    html_dir = Path('Lectures/html')
    if not html_dir.exists():
        print(f'\n   ❌ Directory not found: {html_dir}\n')
        return
    
    updated_files = 0
    for num, video_id in VIDEO_IDS.items():
        if 'YOUR_VIDEO_ID_HERE' in video_id:
            continue
            
        file_path = html_dir / f'lecture-{num}.html'
        
        if not file_path.exists():
            print(f'   ⚠️  File not found: lecture-{num}.html')
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            youtube_url = f'https://www.youtube.com/watch?v={video_id}'
            
            # Replace VIDEO_ID_XX in thumbnail image URLs (older pattern)
            content = content.replace(f'VIDEO_ID_{num}', video_id)
            
            # Replace YOUR_VIDEO_ID_HERE in thumbnail URLs (newer pattern)
            # This handles files that haven't been updated yet
            if 'YOUR_VIDEO_ID_HERE' in content:
                content = content.replace('YOUR_VIDEO_ID_HERE', video_id)
            
            # Replace #video-lecture-XX in thumbnail links
            content = content.replace(
                f'href="#video-lecture-{num}"', 
                f'href="{youtube_url}"'
            )
            
            # Also replace href="https://www.youtube.com/watch?v=YOUR_VIDEO_ID_HERE"
            content = content.replace(
                f'href="https://www.youtube.com/watch?v=YOUR_VIDEO_ID_HERE"',
                f'href="{youtube_url}"'
            )
            content = content.replace(f'VIDEO_ID_{num}', video_id)
            
            # Replace #video-lecture-XX in thumbnail links
            content = content.replace(
                f'href="#video-lecture-{num}"', 
                f'href="{youtube_url}"'
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            updated_files += 1
            print(f'   ✓ Lecture {num}: Updated thumbnail and link')
            
        except Exception as e:
            print(f'   ❌ Error updating lecture-{num}.html: {e}')
    
    print(f'\n   ✅ Updated {updated_files} lecture page files\n')
    
    # ==========================================================================
    # Summary
    # ==========================================================================
    print("=" * 70)
    print("  UPDATE COMPLETE!")
    print("=" * 70)
    print(f"\n✅ Updated video links for {len(VIDEO_IDS)} lectures")
    print("\n📋 What was updated:")
    print("   • index.html: Video button links on lecture cards")
    print("   • Lectures/html/*.html: Video thumbnails and clickable links")
    print("\n🚀 Next steps:")
    print("   1. Test the website locally to verify links work")
    print("   2. Commit changes: git add .")
    print("   3. Commit: git commit -m 'Update video links with actual YouTube URLs'")
    print("   4. Push: git push origin main")
    print("\n" + "=" * 70 + "\n")

if __name__ == '__main__':
    main()
