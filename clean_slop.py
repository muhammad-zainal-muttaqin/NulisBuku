import os
import re
import glob

def clean_slop(text):
    # Dictionaries for simple replacements
    replacements = {
        r'\bkrusial\b': 'penting',
        r'\bkritis\b': 'penting',
        r'\blanskap\b': 'ekosistem',
        r'\bkesimpulannya\b': 'ringkasnya',
        r'\bsecara praktis\b': 'dalam praktiknya',
        r'\bbekerja baik\b': 'efektif',
        r'\baturan jempol\b': 'aturan praktis',
        r'\bkerangka mental\b': 'kerangka berpikir',
        r'\blangkah-per-langkah\b': 'langkah demi langkah',
        r'\bsejatinya\b': 'pada dasarnya',
        r'\brevolusioner\b': 'berdampak besar',
        r'\bluar biasa\b': 'signifikan',
        r'\bmengejutkan\b': 'tak terduga',
        # Throat clearers and emphasis crutches
        r'(^|\.\s+)Ingat,\s*': r'\1',
        r'(^|\.\s+)Perlu diingat bahwa\s*': r'\1',
        r'(^|\.\s+)Perlu diingat,\s*': r'\1',
        r'(^|\.\s+)Penting untuk diingat bahwa\s*': r'\1',
        r'(^|\.\s+)Satu hal yang sering disalahpahami:\s*': r'\1',
        r'(^|\.\s+)Perlu ditekankan bahwa\s*': r'\1',
        r'(^|\.\s+)Yang menarik di sini adalah\s*': r'\1',
        # Empty intensifiers
        r'\bbenenar-benar\s+': '',
        r'\bbenar-benar\s+': '',
        r'\bsungguhan\b': '',
        r'\bsebetulnya\b': '',
        # Em dash replacements
        r'—': ' - ',
    }
    
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
    # Clean up multiple spaces that might result from removals
    text = re.sub(r'  +', ' ', text)
    
    # Capitalize the first letter of sentences if the opener was removed and it's now lower case.
    # A bit complex via regex, so we'll just handle specific cases if needed, but since we removed them at the start of a sentence,
    # the next word should ideally be capitalized if it's the beginning.
    def capitalize_match(match):
        return match.group(1) + match.group(2).upper()
        
    text = re.sub(r'(^|\.\s+)([a-z])', capitalize_match, text)
    
    return text

def process_files():
    md_files = glob.glob('drafts/*.md')
    total_files = 0
    modified_files = 0
    
    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        cleaned_content = clean_slop(content)
        
        if content != cleaned_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            modified_files += 1
        total_files += 1
        
    print(f"Processed {total_files} files.")
    print(f"Modified {modified_files} files with slop fixes.")

if __name__ == "__main__":
    process_files()
