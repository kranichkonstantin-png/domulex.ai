#!/usr/bin/env python3
"""
Script to add disclaimer to all templates that don't have one yet.
"""

import re

DISCLAIMER = "⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.\n\n"

def add_disclaimers():
    file_path = "src/app/app/templates/page.tsx"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all template content blocks
    # Pattern: content: `[text that doesn't start with disclaimer]
    pattern = r"(content: `)(?!⚠️ HINWEIS:)"
    
    # Replace with disclaimer added
    new_content = re.sub(pattern, r'\1' + DISCLAIMER, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # Count how many were added
    original_count = content.count("content: `")
    new_count = new_content.count("⚠️ HINWEIS:")
    added = new_count - content.count("⚠️ HINWEIS:")
    
    print(f"✅ Disclaimer added to {added} templates")
    print(f"   Total templates: {original_count}")
    print(f"   Templates with disclaimer: {new_count}")

if __name__ == "__main__":
    add_disclaimers()
