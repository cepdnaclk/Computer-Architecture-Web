"""
Automated Video Links Update Script

This script updates video links in TWO locations:
1. Main page (index.html) - Video button links
2. Lecture pages (Lectures/html/*.html) - Video thumbnails and links

Usage:
1. Add your YouTube video IDs to the VIDEO_IDS dictionary below
2. Run: python update_video_links_complete.py
"""

import re
from pathlib import Path

# =============================================================================
# CONFIGURE YOUR VIDEO IDS HERE
# =============================================================================
# Get video IDs from YouTube URLs: https://www.youtube.com/watch?v=VIDEO_ID
# Just copy the part after "v="

VIDEO_IDS = {
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

# =============================================================================
# SCRIPT EXECUTION
# =============================================================================

def main():
    print("=" * 70)
    print("  YouTube Video Links Update Script")
    print("=" * 70)
    
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
        file_path = html_dir / f'lecture-{num}.html'
        
        if not file_path.exists():
            print(f'   ⚠️  File not found: lecture-{num}.html')
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            youtube_url = f'https://www.youtube.com/watch?v={video_id}'
            
            # Replace VIDEO_ID_XX in thumbnail image URLs
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
