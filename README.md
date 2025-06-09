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
cp files-to-clipboard.py /usr/local/bin/files-to-clipboard
chmod +x /usr/local/bin/files-to-clipboard
```

# Usage

```bash
files-to-clipboard tests/file1.txt tests/file2.txt tests/file3.txt
```

OR

```bash
files-to-clipboard tests/* README.md
```