# Static Images Directory

This directory contains all static images for the OrderKanto project.

## Directory Structure

- `menu/` - Menu item images (food photos, etc.)
- `products/` - Product images 
- `banners/` - Banner and promotional images
- `icons/` - Icon files (SVG, PNG)
- `logos/` - Logo files

## Usage

Images in this directory can be referenced in templates using:

```html
<img src="{% static 'images/menu/kwek-kwek.jpg' %}" alt="Kwek-Kwek">
```

## File Naming Convention

- Use lowercase letters and hyphens
- Include descriptive names
- Use appropriate file extensions (.jpg, .png, .svg)
- Keep file sizes optimized for web

## Supported Formats

- JPEG (.jpg, .jpeg) - For photographs
- PNG (.png) - For images with transparency
- SVG (.svg) - For scalable graphics and icons
- WebP (.webp) - For modern web optimization 