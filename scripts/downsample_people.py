#!/usr/bin/env python3
"""
Script to downsample people images from people-original folder to people folder.
Target: < 1MB per image while maintaining quality
"""

import os
from pathlib import Path
from PIL import Image
import sys

def get_file_size_mb(filepath):
    """Get file size in MB"""
    return os.path.getsize(filepath) / (1024 * 1024)

def downsample_image(input_path, output_path, target_size_mb=1.0, max_dimension=800):
    """
    Downsample an image to be under target_size_mb
    
    Args:
        input_path: Path to input image
        output_path: Path to save downsampled image
        target_size_mb: Target size in MB (default 1.0)
        max_dimension: Maximum width or height (default 800px)
    """
    try:
        # Open image
        img = Image.open(input_path)
        
        # Convert RGBA to RGB if necessary
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # Get original dimensions
        width, height = img.size
        original_size_mb = get_file_size_mb(input_path)
        
        print(f"Processing: {input_path.name}")
        print(f"  Original: {width}x{height}, {original_size_mb:.2f}MB")
        
        # Resize if larger than max_dimension
        if width > max_dimension or height > max_dimension:
            # Maintain aspect ratio
            if width > height:
                new_width = max_dimension
                new_height = int((max_dimension / width) * height)
            else:
                new_height = max_dimension
                new_width = int((max_dimension / height) * width)
            
            img = img.resize((new_width, new_height), Image.LANCZOS)
            print(f"  Resized to: {new_width}x{new_height}")
        
        # Start with quality 85 and adjust if needed
        quality = 85
        
        # Save with progressive quality reduction until under target size
        while quality > 20:
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            size_mb = get_file_size_mb(output_path)
            
            if size_mb <= target_size_mb:
                print(f"  Saved: {quality}% quality, {size_mb:.2f}MB")
                break
            
            quality -= 5
        
        final_size_mb = get_file_size_mb(output_path)
        reduction = ((original_size_mb - final_size_mb) / original_size_mb) * 100
        print(f"  ✓ Reduced by {reduction:.1f}%")
        
    except Exception as e:
        print(f"  ✗ Error processing {input_path.name}: {e}")

def main():
    # Set up paths
    script_dir = Path(__file__).parent.parent
    people_dir = script_dir / "static" / "images" / "people-original"
    downsampled_dir = script_dir / "static" / "images" / "people"
    
    # Create output directory if it doesn't exist
    downsampled_dir.mkdir(exist_ok=True)
    
    # Get all jpg files in people directory
    image_files = sorted(people_dir.glob("*.jpg"))
    
    if not image_files:
        print("No JPG files found in people directory")
        return
    
    print(f"Found {len(image_files)} images to process\n")
    
    # Process each image
    for img_path in image_files:
        output_path = downsampled_dir / img_path.name
        downsample_image(img_path, output_path, target_size_mb=1.0, max_dimension=800)
        print()
    
    # Summary
    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    total_original = sum(get_file_size_mb(f) for f in image_files)
    total_downsampled = sum(get_file_size_mb(downsampled_dir / f.name) for f in image_files)
    
    print(f"Total original size: {total_original:.2f}MB")
    print(f"Total downsampled size: {total_downsampled:.2f}MB")
    print(f"Total reduction: {((total_original - total_downsampled) / total_original) * 100:.1f}%")
    
    # Check for any files over 1MB
    large_files = []
    for img_path in image_files:
        output_path = downsampled_dir / img_path.name
        size = get_file_size_mb(output_path)
        if size > 1.0:
            large_files.append((img_path.name, size))
    
    if large_files:
        print(f"\nFiles still over 1MB ({len(large_files)}):")
        for name, size in large_files:
            print(f"  {name}: {size:.2f}MB")
    else:
        print("\n✓ All files are under 1MB!")

if __name__ == "__main__":
    main()