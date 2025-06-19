#!/usr/bin/env python3
import argparse
import subprocess
import os
import shutil # For checking if 'tree' command exists

def is_binary(file_path):
    """
    Checks if a file is likely a binary file by looking for null bytes.
    """
    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(1024)
            if b'\0' in chunk:
                return True
    except Exception as e:
        print(f"Error checking {file_path}: {e}")
        return True  # treat unreadable files as binary
    return False

def get_tree_output(path):
    """
    Generates a directory tree string using the 'tree' command.
    """
    if not shutil.which('tree'):
        print("Warning: 'tree' command not found. Skipping tree generation.")
        return ""
    try:
        # Use -a to show all files, -F to append indicators (e.g., / for directories)
        # -I ".*" to ignore dotfiles if preferred, but for a full tree, we might want them.
        # For this example, we'll keep it simple to show basic tree.
        # You might want to adjust tree arguments for your specific needs.
        result = subprocess.run(['tree', path], capture_output=True, text=True, check=True)
        return f"<directory path='{path}'>\n{result.stdout}\n</directory>\n"
    except subprocess.CalledProcessError as e:
        print(f"Error generating tree for {path}: {e}")
        print(f"Stderr: {e.stderr}")
        return ""
    except FileNotFoundError:
        print(f"Error: 'tree' command not found. Please install it to use --tree argument.")
        return ""

def get_sys_file_content(sys_file_path):
    """
    Reads the content of a specified system file.
    """
    if not os.path.isfile(sys_file_path):
        print(f"Warning: System file '{sys_file_path}' not found or is not a regular file. Skipping.")
        return ""
    if is_binary(sys_file_path):
        print(f"Warning: System file '{sys_file_path}' appears to be a binary file. Skipping.")
        return ""
    try:
        with open(sys_file_path, 'r', encoding='utf-8') as file:
            return f"<system>\n{file.read()}</system>\n"
    except Exception as e:
        print(f"Error reading system file {sys_file_path}: {e}")
        return ""

def files_to_clipboard(file_paths, include_tree=False, sys_file=None):
    content = []

    # Handle --sys argument first if present
    if sys_file:
        sys_content = get_sys_file_content(sys_file)
        if sys_content:
            content.append(sys_content)

    # Handle --tree argument if present and sys_file was not handled (or sys_content was empty)
    # The requirement is that if both are set, sys comes first.
    # So if sys_file was provided and successfully added content, we still add tree if requested.
    if include_tree:
        # For tree, we usually want the tree of the current directory, or a specified directory.
        # Given the original script takes file paths, we'll generate a tree for the parent directory
        # of the first file, or the current working directory if no files are provided.
        # Or, you could modify this to accept a specific directory for the tree.
        tree_root = "." # Default to current directory
        if file_paths:
            # Get the common parent directory of all files, or just the parent of the first file
            # for a simpler implementation.
            first_file_dir = os.path.dirname(os.path.abspath(file_paths[0]))
            if first_file_dir and os.path.isdir(first_file_dir):
                tree_root = first_file_dir
            elif os.path.exists(file_paths[0]) and os.path.isdir(file_paths[0]): # if the first "file" is a directory
                tree_root = os.path.abspath(file_paths[0])

        tree_output = get_tree_output(tree_root)
        if tree_output:
            content.append(tree_output)

    # Now add the content of the specified files
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
                content.append(f"<path='{path}'>\n{file_content}\n</path>\n")
        except Exception as e:
            print(f"Error reading {path}: {e}")

    if not content:
        print("No valid content to copy to clipboard.")
        return

    final_content = "\n".join(content)
    
    process = subprocess.run(['xclip', '-selection', 'clipboard'], input=final_content.encode('utf-8'))
    if process.returncode == 0:
        print("Content copied to clipboard.")
    else:
        print("Failed to copy to clipboard. Make sure 'xclip' is installed and running.")
        print(f"xclip error: {process.stderr.decode('utf-8')}")

def main():
    parser = argparse.ArgumentParser(description="Copy file paths and file contents to clipboard.")
    parser.add_argument('files', nargs='*', help='List of file paths. Can be omitted if --tree or --sys is used.')
    parser.add_argument('--tree', action='store_true', help='Include a directory tree at the beginning.')
    parser.add_argument('--sys', type=str, help='Specify a system file to read and insert at the beginning.')
    
    args = parser.parse_args()
    
    # Check if at least one file, --tree, or --sys is provided
    if not args.files and not args.tree and not args.sys:
        parser.error("At least one file, --tree, or --sys argument is required.")

    files_to_clipboard(args.files, args.tree, args.sys)

if __name__ == '__main__':
    main()