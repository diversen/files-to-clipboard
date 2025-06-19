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
wget https://raw.githubusercontent.com/diversen/files-to-clipboard/refs/heads/main/files_to_clipboard.py
sudo mv files_to_clipboard.py /usr/local/bin/files-to-clipboard
sudo chmod +x /usr/local/bin/files-to-clipboard
```

# Usage

```bash
./files_to_clipboard.py --tree files_to_clipboard.py tests/* --sys agents/programmer.md 

```
<system>
# Test instructions

This is a test.
</system>

<directory path='/home/dennis/files-to-clipboard'>
/home/dennis/files-to-clipboard
├── agents
│   ├── programmer.md
│   └── test.md
├── content.txt
├── files_to_clipboard.py
├── LICENSE
├── __pycache__
│   └── files_to_clipboard.cpython-312.pyc
├── README.md
├── test_content.py
├── test_files_to_clipboard.py
└── tests
    ├── file_1.txt
    ├── file_2.txt
    └── file_3.txt

4 directories, 12 files

</directory>

<path='test_content.py'>
print("Test test,content.py loaded successfully.")
</path>

```