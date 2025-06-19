# poor-mans-agent

Simple Python script to generate a LLM context.
I am using it in order to test programming with the help of AI tools.
Result is copied to the clipboard in a format that may be easy readable by 
AI tools like ChatGPT, Open-source AI, or others.

The script is only working on Linux and requires `xclip` to be installed.

You are welcome to create a pull request to add support for other operating systems.

# Installation

## Requirements linux

```bash
sudo apt update
sudo apt install xclip
```

Copy the script to a directory in your PATH, for example:

```bash
wget https://raw.githubusercontent.com/diversen/poor-mans-agent/refs/heads/main/poor_mans_agent.py -O pmg.py
sudo mv pmg.py /usr/local/bin/poor-mans-agent
sudo chmod +x /usr/local/bin/poor-mans-agent
```

# Usage

If in a PATH directory:

```bash
poor-mans-agent --tree --sys agents/test.md test_content.py
```

If cloned:

```bash
./poor_mans_agent.py --tree --sys agents/test.md test_content.py
```

Both script will produce the following output:

```xml
<system>
# Test instructions

This is a test.
</system>

<directory path='/home/dennis/poor-mans-agent'>
/home/dennis/poor-mans-agent
├── agents
│   ├── programmer.md
│   └── test.md
├── content.txt
├── files_to_clipboard.py
├── LICENSE
├── README.md
├── test_content.py
├── test_files_to_clipboard.py
└── tests
    ├── file_1.txt
    ├── file_2.txt
    └── file_3.txt

3 directories, 11 files

</directory>

<path='test_content.py'>
print("test_content.py loaded successfully.")
print("!!!")
</path>

```