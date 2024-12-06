import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Directory paths
source_dir = "/Users/brandoncarris/Downloads"
destination_dirs = {
    "/Users/brandoncarris/sorter-destinations/archives": [".zip", ".rar", ".7z"],
    "/Users/brandoncarris/sorter-destinations/audio": [".wav", ".mp3"],
    "/Users/brandoncarris/sorter-destinations/books": [".pdf", ".epub", ".mobi"],
    "/Users/brandoncarris/sorter-destinations/documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "/Users/brandoncarris/sorter-destinations/html": [".html"],
    "/Users/brandoncarris/sorter-destinations/images": [".jpg", ".png", ".jpeg", ".gif"],
    "/Users/brandoncarris/sorter-destinations/videos": [".mp4", ".avi", ".mkv"],
}
uncategorized_folder = "/Users/brandoncarris/sorter-destinations/uncategorized"

# Create directories if not already present
for folder in destination_dirs.keys():
    os.makedirs(folder, exist_ok=True)
os.makedirs(uncategorized_folder, exist_ok=True)

# Define event handler
class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:  # Ignore directories
            file_path = event.src_path
            filename = os.path.basename(file_path)
            file_ext = os.path.splitext(filename)[1].lower()

            categorized = False
            for folder, extensions in destination_dirs.items():
                if file_ext in extensions:
                    destination_path = os.path.join(folder, filename)
                    if not os.path.exists(destination_path):  # Avoid overwriting
                        shutil.move(file_path, destination_path)
                        print(f"Moved {filename} to {folder}")
                    categorized = True
                    break

            if not categorized:
                destination_path = os.path.join(uncategorized_folder, filename)
                if not os.path.exists(destination_path):  # Avoid overwriting
                    shutil.move(file_path, destination_path)
                    print(f"Moved {filename} to Uncategorized")

# Set up observer
event_handler = FileHandler()
observer = Observer()
observer.schedule(event_handler, path=source_dir, recursive=False)

# Start observer
observer.start()
print(f"Monitoring folder: {source_dir}")
try:
    while True:
        pass  # Keep script running
except KeyboardInterrupt:
    observer.stop()
observer.join()
