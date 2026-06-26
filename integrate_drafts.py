import os
import re

def get_chapter_title(qmd_path):
    if not os.path.exists(qmd_path):
        return None
    with open(qmd_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        if first_line.startswith('# '):
            return first_line
    return None

def process_headings(content):
    # Check if the top heading of the file is level 1 (#)
    lines = content.split('\n')
    has_level_1 = False
    for line in lines:
        if line.strip().startswith('# '):
            has_level_1 = True
            break
    
    if has_level_1:
        # Shift all headings down by 1 level
        # To avoid shifting ## into ### and then shift it again to ####, we process them in reverse or with regex replacement
        # Let's replace headings with placeholders or use regex with a callback
        def shift_heading(match):
            heading_hashes = match.group(1)
            # Add one more hash
            return f"#{heading_hashes} "
        
        # Regex matches lines starting with one or more '#' followed by space
        processed_lines = []
        for line in lines:
            if line.startswith('#'):
                # Count hashes
                m = re.match(r'^(#+)\s+(.*)$', line)
                if m:
                    hashes = m.group(1)
                    title = m.group(2)
                    # Shift down by 1
                    new_hashes = '#' + hashes
                    processed_lines.append(f"{new_hashes} {title}")
                else:
                    processed_lines.append(line)
            else:
                processed_lines.append(line)
        return '\n'.join(processed_lines)
    else:
        return content

def integrate_all_chapters():
    drafts_dir = 'drafts'
    chapters_dir = 'website/chapters'
    
    for ch_num in range(1, 18):
        ch_prefix = f"ch{ch_num:02d}"
        qmd_path = os.path.join(chapters_dir, f"{ch_prefix}.qmd")
        
        chapter_title = get_chapter_title(qmd_path)
        if not chapter_title:
            # Fallback title if we can't find it in existing qmd
            chapter_title = f"# Chapter {ch_num:02d}"
            print(f"Warning: Could not read chapter title for {ch_prefix}. Using fallback.")
            
        print(f"Integrating drafts for {ch_prefix} ({chapter_title})...")
        
        # Find all draft files for this chapter
        draft_files = []
        for file in os.listdir(drafts_dir):
            if file.startswith(ch_prefix) and file.endswith('.md'):
                draft_files.append(file)
        
        # Sort draft files by name (e.g. ch01_s01.md, ch01_s02.md, etc.)
        draft_files.sort()
        
        chapter_content = [chapter_title, ""]
        
        for df in draft_files:
            df_path = os.path.join(drafts_dir, df)
            with open(df_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Process heading levels
            processed_content = process_headings(content)
            chapter_content.append(processed_content)
            chapter_content.append("") # blank line between subsections
            chapter_content.append("") # extra blank line for padding
            
        # Join and write to the qmd file
        final_qmd_content = '\n'.join(chapter_content).strip() + '\n'
        
        with open(qmd_path, 'w', encoding='utf-8') as f:
            f.write(final_qmd_content)
            
        print(f"  Saved integrated chapter to {qmd_path}")

if __name__ == '__main__':
    integrate_all_chapters()
