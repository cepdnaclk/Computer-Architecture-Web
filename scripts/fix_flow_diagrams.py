import re
import os

# Directory containing the lecture .tex files
LATEX_DIR = r"d:\Academics\Projects\isuru sir\CO224-Web\Lectures\latex"

def fix_flow_diagrams(content):
    """
    Fix flow diagrams by:
    1. Converting Unicode ↓ to LaTeX $\downarrow$
    2. Detecting multi-line flow diagrams and wrapping them in center environment
    """
    
    # First, replace Unicode arrows with LaTeX commands
    content = content.replace('↓', r'$\downarrow$')
    content = content.replace('→', r'$\rightarrow$')
    content = content.replace('↔', r'$\leftrightarrow$')
    
    # Pattern to detect flow diagram sections (multiple lines with arrows)
    # This is a simple flow: line, arrow, line, arrow, etc.
    lines = content.split('\n')
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this looks like the start of a flow diagram
        # (line followed by arrow line, not in a list or verbatim)
        if (i + 2 < len(lines) and 
            not line.strip().startswith('\\item') and
            not line.strip().startswith('\\begin') and
            not line.strip().startswith('\\end') and
            r'$\downarrow$' in lines[i + 1] and
            len(line.strip()) > 0):
            
            # Collect the flow diagram lines
            flow_lines = []
            j = i
            consecutive_arrows = 0
            
            while j < len(lines):
                current = lines[j].strip()
                
                # Stop at section boundaries or lists
                if (current.startswith('\\subsection') or 
                    current.startswith('\\subsubsection') or
                    current.startswith('\\paragraph') or
                    current.startswith('\\begin{itemize}') or
                    current.startswith('\\begin{enumerate}')):
                    break
                
                # Count if this line has a downward arrow
                if r'$\downarrow$' in current:
                    consecutive_arrows += 1
                elif current and consecutive_arrows > 0:
                    consecutive_arrows = 0
                
                # If we have at least 2 arrow transitions, it's a flow diagram
                if consecutive_arrows >= 2 or (flow_lines and current):
                    flow_lines.append(lines[j])
                    j += 1
                    if not current:  # Empty line might signal end
                        j += 1
                        break
                elif flow_lines:
                    flow_lines.append(lines[j])
                    j += 1
                else:
                    break
            
            # If we collected a flow diagram (at least 3 lines with arrows)
            if len(flow_lines) >= 5 and flow_lines.count('$\\downarrow$') >= 2:
                # Check if not already in a center environment
                if i > 0 and '\\begin{center}' not in result_lines[-5:]:
                    result_lines.append('\\begin{center}')
                    for flow_line in flow_lines:
                        result_lines.append(flow_line)
                    result_lines.append('\\end{center}')
                    result_lines.append('')
                    i = j
                    continue
        
        result_lines.append(line)
        i += 1
    
    return '\n'.join(result_lines)

def fix_lecture_file(filepath):
    """Fix a single lecture file."""
    print(f"Processing {os.path.basename(filepath)}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix flow diagrams
    content = fix_flow_diagrams(content)
    
    # Check if anything changed
    if content != original_content:
        # Write back the fixed content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed flow diagrams in {os.path.basename(filepath)}")
        return True
    else:
        print(f"  - No changes needed in {os.path.basename(filepath)}")
        return False

def main():
    """Fix all lecture files."""
    files_fixed = 0
    
    for i in range(1, 21):
        filepath = os.path.join(LATEX_DIR, f'lecture-{i:02d}.tex')
        if os.path.exists(filepath):
            if fix_lecture_file(filepath):
                files_fixed += 1
    
    print(f"\n✓ Complete! Fixed {files_fixed} lecture files.")

if __name__ == '__main__':
    main()
