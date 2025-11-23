import os
import re
import glob

def scan_for_errors(lectures_dir):
    print(f"Scanning HTML files in {lectures_dir}...\n")
    
    files = sorted(glob.glob(os.path.join(lectures_dir, "lecture-*.html")))
    
    suspicious_patterns = [
        (r'(\w+)\s+\1', "Repeated word"), # Word followed by itself
        (r'(\w+)(rd|vements|dresses|peration|KB)\s+\1', "Potential stutter typo"), # Specific patterns seen before
        (r'[A-Z][a-z]+[A-Z][a-z]+', "CamelCase inside word?"), # e.g. SizerdSize
    ]

    # Specific typos seen: "Sizerd Size", "Addressesdresses", "Improvementsvements", "PagesKB Pages", "Operationperation", "Must Do Must Do"
    
    for file_path in files:
        filename = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check headings specifically
        headings = re.findall(r'<(h[1-6])>(.*?)</\1>', content, re.IGNORECASE)
        
        for tag, text in headings:
            # Check for repeated words at end of string which seems to be the pattern
            # e.g. "Address Space by CPU Word Sizerd Size" -> "Size" and "rd Size"
            
            # Check for "WordWord" pattern at end
            # Ignore 'ss' ending (Process, Access)
            match = re.search(r'(\w{3,})\1$', text)
            if match:
                 print(f"[{filename}] {tag}: Suspicious ending repetition in '{text}'")

            # Check for "Word Word" repetition
            words = text.split()
            if len(words) > 1:
                if words[-1] == words[-2]:
                     print(f"[{filename}] {tag}: Repeated last word in '{text}'")
                
                # Check for "WordSuffix Word" where Suffix is part of Word
                # e.g. "Improvementsvements" is not quite "Word Word"
                # But "Sizerd Size" -> "Size" is in "Sizerd"
                
                last_word = words[-1]
                second_last = words[-2]
                
                if len(last_word) > 3 and last_word in second_last and last_word != second_last:
                     # Check if second_last ends with last_word
                     if second_last.endswith(last_word):
                         # Check if the prefix is suspicious (like 'rd' or 'vements')
                         prefix = second_last[:-len(last_word)]
                         if len(prefix) < 4 or prefix in ["Sizerd", "Addresses", "Improvements", "Operation"]:
                             print(f"[{filename}] {tag}: Last word contained in previous in '{text}'")

            # Check for specific known bad suffixes in the text
            if "vements" in text and "Improvements" not in text: # Improvementsvements
                 if re.search(r'Improvements?vements', text):
                     print(f"[{filename}] {tag}: Found 'Improvementsvements' type error in '{text}'")

            # Check for double numbering e.g. "19.18.1 1. Title"
            if re.search(r'\d+(\.\d+)*\s+\d+\.', text):
                 print(f"[{filename}] {tag}: Potential double numbering in '{text}'")
            
            if "dresses" in text and "Addresses" not in text:
                 if re.search(r'Addresses?dresses', text):
                     print(f"[{filename}] {tag}: Found 'Addressesdresses' type error in '{text}'")

            if "peration" in text and "Operation" not in text:
                 if re.search(r'Operation?peration', text):
                     print(f"[{filename}] {tag}: Found 'Operationperation' type error in '{text}'")

if __name__ == "__main__":
    scan_for_errors(r"d:\Academics\Projects\isuru sir\CO224-Web\Lectures\html")
