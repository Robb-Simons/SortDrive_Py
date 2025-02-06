# SortDrive_Py

File to hard sort a complex file system

Core Function: Organizes files from a drive by:

Moving photos to dated folders (Year/Month)
Moving other files to "Other media" folder

How it works:

get_photo_date() extracts photo dates:

Tries EXIF data first (original photo date)
Falls back to file modification date if EXIF fails

organize_files() processes each file:

Creates Pictures/Year/Month folders for photos
Creates Other media folder for non-photos
Handles duplicate filenames by adding numbers
Preserves originals by copying
