import os
import shutil
import sys

# Extension mapping dictionary matching project specifications
EXTENSION_MAPPING = {
    # Documents
    '.pdf': 'Documents',
    '.docx': 'Documents',
    '.txt': 'Documents',
    '.xlsx': 'Documents',
    '.pptx': 'Documents',
    '.csv': 'Documents',
    
    # Images
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.gif': 'Images',
    '.webp': 'Images',
    
    # Videos & Audio
    '.mp4': 'Videos',
    '.mkv': 'Videos',
    '.mov': 'Videos',
    '.mp3': 'Audio',
    
    # Archives
    '.zip': 'Archives',
    '.tar': 'Archives',
    '.gz': 'Archives',
    '.rar': 'Archives',
    '.7z': 'Archives',
    
    # Code & Scripts
    '.py': 'Code',
    '.js': 'Code',
    '.html': 'Code',
    '.css': 'Code',
    '.json': 'Code'
}

def organize_directory(target_directory):
    """Scans the target directory, organizes files into category folders, and handles errors."""
    if not os.path.exists(target_directory):
        print(f"[!] Error: The directory '{target_directory}' does not exist.")
        return

    print(f"\n==================================================")
    print(f"      AUTOMATED FILE ORGANIZER & CLEANUP")
    print(f"==================================================")
    print(f"Target Directory: {os.path.abspath(target_directory)}\n")

    moved_count = 0
    error_count = 0

    # Use os.scandir() for efficient directory iteration
    try:
        with os.scandir(target_directory) as entries:
            for entry in entries:
                # Skip subdirectories and hidden files
                if entry.is_dir() or entry.name.startswith('.'):
                    continue

                file_path = entry.path
                file_ext = os.path.splitext(entry.name)[1].lower()

                # Determine category subfolder (defaults to 'Others' if unmapped)
                category = EXTENSION_MAPPING.get(file_ext, 'Others')
                dest_folder = os.path.join(target_directory, category)

                # Dynamically create the destination subfolder if missing
                os.makedirs(dest_folder, exist_ok=True)
                dest_path = os.path.join(dest_folder, entry.name)

                # Handle naming collisions safely by appending an incremental counter
                if os.path.exists(dest_path):
                    base, ext = os.path.splitext(entry.name)
                    counter = 1
                    while True:
                        new_name = f"{base}_{counter}{ext}"
                        dest_path = os.path.join(dest_folder, new_name)
                        if not os.path.exists(dest_path):
                            break
                        counter += 1

                # Implement try-except blocks to catch FileExistsError or PermissionError
                try:
                    shutil.move(file_path, dest_path)
                    print(f"[+] Relocated: {entry.name} -> /{category}/")
                    moved_count += 1
                except PermissionError:
                    print(f"[!] Permission Denied: Could not move '{entry.name}'. File may be open or locked.")
                    error_count += 1
                except FileExistsError:
                    print(f"[!] Conflict Error: Destination file already exists for '{entry.name}'.")
                    error_count += 1
                except Exception as e:
                    print(f"[!] Unexpected error moving '{entry.name}': {e}")
                    error_count += 1

    except OSError as e:
        print(f"[!] Critical OS error while scanning directory: {e}")
        return

    # Print a formatted execution summary showing total files relocated
    print("\n" + "=" * 50)
    print(f"               ORGANIZATION SUMMARY")
    print("=" * 50)
    print(f"Total Files Successfully Relocated: {moved_count}")
    print(f"Total Files Skipped / Errors:       {error_count}")
    print("=" * 50 + "\n")

def main():
    # Allow passing target directory via command-line argument or interactive prompt
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = input("Enter path of the directory to organize (Press Enter for current directory): ").strip()
        if not target_dir:
            target_dir = "."

    organize_directory(target_dir)

if __name__ == "__main__":
    main()