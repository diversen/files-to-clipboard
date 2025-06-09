#!/usr/bin/env python3
import argparse
import subprocess

def files_to_clipboard(file_paths):
    content = []
    for path in file_paths:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                file_content = file.read()
                content.append(f"--- FILE START: {path} ---\n{file_content}\n--- FILE END: {path} ---\n")
        except Exception as e:
            print(f"Error reading {path}: {e}")
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
