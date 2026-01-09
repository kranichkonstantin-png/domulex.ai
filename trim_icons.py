#!/usr/bin/env python3
"""Trim icons to remove white border"""
from PIL import Image

# Load original icon
img = Image.open('public/icon-512.png')
print(f'Original size: {img.size}')

if img.mode != 'RGBA':
    img = img.convert('RGBA')

bbox = img.getbbox()
print(f'Content bbox: {bbox}')

if bbox:
    left, top, right, bottom = bbox
    content_width = right - left
    content_height = bottom - top
    print(f'Content: {content_width}x{content_height}')
    
    cropped = img.crop(bbox)
    
    # Fill 512px with 3px margin only
    margin = 3
    target_size = 512 - 2 * margin
    scale = target_size / max(content_width, content_height)
    new_w = int(content_width * scale)
    new_h = int(content_height * scale)
    
    resized = cropped.resize((new_w, new_h), Image.LANCZOS)
    
    new_img = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    x = (512 - new_w) // 2
    y = (512 - new_h) // 2
    new_img.paste(resized, (x, y), resized)
    
    new_img.save('public/icon-512.png')
    print('✅ icon-512.png saved')
    
    new_img.resize((192, 192), Image.LANCZOS).save('public/icon-192.png')
    print('✅ icon-192.png saved')
    
    new_img.resize((32, 32), Image.LANCZOS).save('public/favicon.ico', format='ICO')
    print('✅ favicon.ico saved')
    
    print('\n🎉 Icons with minimal margin created!')
else:
    print('Could not detect content bounds')
