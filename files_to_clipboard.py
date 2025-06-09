#!/usr/bin/env python3
import argparse
import subprocess
import os

def is_binary(file_path):
    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(1024)
            if b'\0' in chunk:
                return True
    except Exception as e:
        print(f"Error checking {file_path}: {e}")
        return True  # treat unreadable files as binary
    return False

def files_to_clipboard(file_paths):
    content = []
    for path in file_paths:
        if not os.path.isfile(path):
            print(f"Skipping {path}: not a regular file.")
            continue
        if is_binary(path):
            print(f"Skipping {path}: binary file detected.")
            continue
        try:
            with open(path, 'r', encoding='utf-8') as file:
                file_content = file.read()
                content.append(f"--- FILE START: {path} ---\n{file_content}\n--- FILE END: {path} ---\n")
        except Exception as e:
            print(f"Error reading {path}: {e}")
    if not content:
        print("No valid text files to copy.")
        return
    final_content = "\n".join(content)
    
    process = subprocess.run(['xclip', '-selection', 'clipboard'], input=final_content.encode('utf-8'))
    if process.returncode == 0:
        print("Content copied to clipboard.")
    else:
        print("Failed to copy to clipboard.")

def main():
    parser = argparse.ArgumentParser(description="Copy file paths and file contents to clipboard.")
    parser.add_argument('files', nargs='+', help='List of file paths')
    args = parser.parse_args()
    
    files_to_clipboard(args.files)

if __name__ == '__main__':
    main()
