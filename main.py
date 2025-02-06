#Written by: Robb Simons - EleMantis Tech Solutions
#DoC: 2/06/2025
#DoLC:2/06/2025
import os
import shutil
from datetime import datetime
from PIL import Image
import piexif
from pathlib import Path

def get_photo_date(file_path):
    """Extract the date taken from image metadata or file modification date."""
    try:
        # Try to get EXIF data
        img = Image.open(file_path)
        if hasattr(img, '_getexif') and img._getexif() is not None:
            exif = img._getexif()
            if 36867 in exif:  # DateTimeOriginal tag
                date_str = exif[36867]
                return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
        
        # If no EXIF data, try alternative method with piexif
        try:
            exif_dict = piexif.load(img.info['exif'])
            if exif_dict['Exif'][36867]:  # DateTimeOriginal
                date_str = exif_dict['Exif'][36867].decode('utf-8')
                return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
        except:
            pass
        
        # If all else fails, use file modification time
        return datetime.fromtimestamp(os.path.getmtime(file_path))
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return datetime.fromtimestamp(os.path.getmtime(file_path))

def organize_files(source_dir, dest_dir):
    """
    Organize files from source directory into destination directory.
    
    Args:
        source_dir (str): Path to source directory
        dest_dir (str): Path to destination directory
    """
    # Create destination directories if they don't exist
    pictures_dir = os.path.join(dest_dir, "Pictures")
    other_media_dir = os.path.join(dest_dir, "Other media")
    
    for dir_path in [pictures_dir, other_media_dir]:
        os.makedirs(dir_path, exist_ok=True)
    
    # Common image file extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.raw', '.cr2', '.nef'}
    
    # Walk through all files in source directory
    for root, _, files in os.walk(source_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_ext = os.path.splitext(filename)[1].lower()
            
            try:
                if file_ext in image_extensions:
                    # Get photo date
                    photo_date = get_photo_date(file_path)
                    
                    # Create year/month subdirectories
                    year_dir = os.path.join(pictures_dir, str(photo_date.year))
                    month_dir = os.path.join(year_dir, f"{photo_date.month:02d}")
                    os.makedirs(month_dir, exist_ok=True)
                    
                    # Generate unique filename if necessary
                    dest_path = os.path.join(month_dir, filename)
                    counter = 1
                    while os.path.exists(dest_path):
                        name, ext = os.path.splitext(filename)
                        dest_path = os.path.join(month_dir, f"{name}_{counter}{ext}")
                        counter += 1
                    
                    # Copy file to destination
                    shutil.copy2(file_path, dest_path)
                    print(f"Copied {filename} to {dest_path}")
                
                else:
                    # Move non-image files to Other media
                    dest_path = os.path.join(other_media_dir, filename)
                    counter = 1
                    while os.path.exists(dest_path):
                        name, ext = os.path.splitext(filename)
                        dest_path = os.path.join(other_media_dir, f"{name}_{counter}{ext}")
                        counter += 1
                    
                    shutil.copy2(file_path, dest_path)
                    print(f"Copied {filename} to {dest_path}")
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    # Get source and destination directories from user
    source_dir = input("Enter the path to your external hard drive: ")
    dest_dir = input("Enter the destination path for organized files: ")
    
    # Validate directories
    if not os.path.exists(source_dir):
        print("Source directory does not exist!")
        exit(1)
    
    print("\nStarting file organization...")
    organize_files(source_dir, dest_dir)
    print("\nFile organization complete!")