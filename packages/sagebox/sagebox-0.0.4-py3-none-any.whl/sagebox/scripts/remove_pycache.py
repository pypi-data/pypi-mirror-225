import os
import shutil
import argparse


def remove_pycache(directory):
    """
    Remove all __pycache__ directories in the specified directory.

    Args:
    - directory (str): The root directory to search and delete __pycache__ from.
    """
    for root, dirs, files in os.walk(directory,
                                     topdown=False):  # Use topdown=False to avoid modifying the list in place
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_path)
            print(f"Deleted {pycache_path}")

def main():
    parser = argparse.ArgumentParser(description="Remove all __pycache__ directories in the specified directory.")
    parser.add_argument("directory", help="The root directory to search and delete __pycache__ from.")
    args = parser.parse_args()

    remove_pycache(args.directory)

if __name__ == "__main__":
    main()
