import os
import shutil
import time

# Directory paths
source_dir = "/Users/brandoncarris/Downloads"
destination_dirs = { # updated to organize based on file extension rather than overarching folders 

    # documents 
    "/Users/brandoncarris/sorter-destinations/documents/pdf": [".pdf"],
    "/Users/brandoncarris/sorter-destinations/documents/epub": [".epub"],
    "/Users/brandoncarris/sorter-destinations/documents/docx": [".docx"],
    "/Users/brandoncarris/sorter-destinations/documents/txt": [".txt"],
    "/Users/brandoncarris/sorter-destinations/documents/xlsx": [".xlsx"],
    # misc
    "/Users/brandoncarris/sorter-destinations/misc/webp": [".webp"],
    "/Users/brandoncarris/sorter-destinations/misc/html": [".html"],
    # image
    "/Users/brandoncarris/sorter-destinations/image/jpg": [".jpg"],
    "/Users/brandoncarris/sorter-destinations/image/png": [".png"],
    "/Users/brandoncarris/sorter-destinations/image/jpeg": [".jpeg"],
    "/Users/brandoncarris/sorter-destinations/image/gif": [".gif"],
    # audio
    "/Users/brandoncarris/sorter-destinations/audio/wav": [".wav"],
    "/Users/brandoncarris/sorter-destinations/audio/mp3": [".mp3"],
    # video
    "/Users/brandoncarris/sorter-destinations/video/mp4": [".mp4"],
    "/Users/brandoncarris/sorter-destinations/video/avi": [".avi"],
    "/Users/brandoncarris/sorter-destinations/video/mkv": [".mkv"],
    # compressed
    "/Users/brandoncarris/sorter-destinations/compressed/zip": [".zip"],
    "/Users/brandoncarris/sorter-destinations/compressed/rar": [".rar"],
    "/Users/brandoncarris/sorter-destinations/compressed/7z": [".7z"],
}
uncategorized_folder = "/Users/brandoncarris/sorter-destinations/uncategorized"

# Create directories if not already present
for folder in destination_dirs.keys():
    os.makedirs(folder, exist_ok=True)
os.makedirs(uncategorized_folder, exist_ok=True)

# Define event handler
def organize_files():
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        file_ext = os.path.splitext(filename)[1].lower()
        categorized = False

        # Move file to correct category
        for folder, extensions in destination_dirs.items():
            if file_ext in extensions:
                destination_path = os.path.join(folder, filename)
                if not os.path.exists(destination_path):  # Avoid overwriting
                    shutil.move(file_path, destination_path)
                    print(f"Moved {filename} to {folder}")
                categorized = True
                break

        # If no matching category, move to Uncategorized
        if not categorized:
            destination_path = os.path.join(uncategorized_folder, filename)
            if not os.path.exists(destination_path):  # Avoid overwriting
                shutil.move(file_path, destination_path)
                print(f"Moved {filename} to Uncategorized")



# Run periodically
INTERVAL = 60  # Check every 60 seconds

print(f"Monitoring {source_dir} every {INTERVAL} seconds...")

try:
    while True:
        organize_files()
        time.sleep(INTERVAL)  # Sleep before next scan
except KeyboardInterrupt:
    print("Script stopped by user.")
