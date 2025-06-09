# files-to-clipboard

Simple Python script to copy multiple files to the clipboard. 

I am using it in order to generate a context for programming with the help of AI tools.

The script is only working on Linux and requires `xclip` to be installed.

You may create a pull request to add support for other operating systems.

# Installation

## Requirements linux

```bash
sudo apt update
sudo apt install xclip
```

Copy the script to a directory in your PATH, for example:

```bash
cp files_to_clipboard.py /usr/local/bin/files-to-clipboard
chmod +x /usr/local/bin/files-to-clipboard
```

# Usage

```bash
files-to-clipboard tests*
```

This will produce something like this in the clipboard:

```
--- FILE START: tests/file_1.txt ---
Content of file 1
--- FILE END: tests/file_1.txt ---

--- FILE START: tests/file_2.txt ---
Content of file 2
--- FILE END: tests/file_2.txt ---

--- FILE START: tests/file_3.txt ---
Content of file 3
--- FILE END: tests/file_3.txt ---
```

You may use multiple arguments:

```bash
files-to-clipboard tests/* README.md
```