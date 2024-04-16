import os
import shutil

def get_file_extension(file_path):
    """Return the file extension from a file path."""
    _, extension = os.path.splitext(file_path)
    return extension

def copy_file(source_path, destination_path):
    """Copy a file from source_path to destination_path."""
    shutil.copy2(source_path, destination_path)

def move_file(source_path, destination_path):
    """Move a file from source_path to destination_path."""
    shutil.move(source_path, destination_path)

def list_files_in_directory(directory_path, extension=None):
    """List all files in a directory. If extension is provided, only list files with that extension."""
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    if extension:
        files = [f for f in files if get_file_extension(f) == extension]
    return files