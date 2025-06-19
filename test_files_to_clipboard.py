import unittest
import tempfile
import os
import subprocess
import sys
import shutil
from files_to_clipboard import is_binary, get_tree_output, get_sys_file_content, files_to_clipboard

class TestFilesToClipboard(unittest.TestCase):

    def test_is_binary_with_text_file(self):
        with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
            tmp.write("This is a text file.\nNo binary here.")
            tmp_path = tmp.name
        self.assertFalse(is_binary(tmp_path))
        os.unlink(tmp_path)

    def test_is_binary_with_binary_file(self):
        with tempfile.NamedTemporaryFile('wb', delete=False) as tmp:
            tmp.write(b'\x00\x01\x02binarycontent')
            tmp_path = tmp.name
        self.assertTrue(is_binary(tmp_path))
        os.unlink(tmp_path)

    def test_get_tree_output_existing_dir(self):
        # Should return non-empty string if 'tree' is available
        if shutil.which('tree'):
            output = get_tree_output('.')
            self.assertIn("<directory path='.", output)
            self.assertIn("</directory>", output)
        else:
            output = get_tree_output('.')
            self.assertEqual(output, "")

    def test_get_tree_output_nonexistent_dir(self):
        # Should handle errors gracefully, return empty string
        output = get_tree_output('/nonexistent_directory_123456789')
        self.assertEqual(output, "")

    def test_get_sys_file_content_existing_text_file(self):
        with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
            content = "System file content"
            tmp.write(content)
            tmp_path = tmp.name
        result = get_sys_file_content(tmp_path)
        self.assertIn(content, result)
        self.assertTrue(result.startswith("<system>"))
        self.assertTrue(result.endswith("</system>\n"))
        os.unlink(tmp_path)

    def test_get_sys_file_content_binary_file(self):
        with tempfile.NamedTemporaryFile('wb', delete=False) as tmp:
            tmp.write(b'\x00\x01\x02binarycontent')
            tmp_path = tmp.name
        result = get_sys_file_content(tmp_path)
        self.assertEqual(result, "")
        os.unlink(tmp_path)

    def test_files_to_clipboard_skips_binary_and_nonfiles(self):
        with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
            tmp.write("text content")
            tmp_path = tmp.name

        # Non-existent file path
        non_file = "/nonexistent_1234"

        # Binary file
        with tempfile.NamedTemporaryFile('wb', delete=False) as tmp_bin:
            tmp_bin.write(b'\x00\x01binary')
            tmp_bin_path = tmp_bin.name

        # We mock subprocess.run to avoid actual clipboard interaction
        original_run = subprocess.run
        subprocess.run = lambda *args, **kwargs: type('proc', (), {'returncode': 0})()

        try:
            files_to_clipboard([tmp_path, non_file, tmp_bin_path], include_tree=False, sys_file=None)
        finally:
            subprocess.run = original_run
            os.unlink(tmp_path)
            os.unlink(tmp_bin_path)

    def test_files_to_clipboard_with_sys_file_and_tree(self):
        # Setup a text sys file
        with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
            tmp.write("sys file content")
            sys_file = tmp.name

        # Setup a text file
        with tempfile.NamedTemporaryFile('w', delete=False) as tmp2:
            tmp2.write("some file content")
            file_path = tmp2.name

        # Mock subprocess.run to avoid real clipboard copy and tree calls
        def mock_run(cmd, **kwargs):
            class Result:
                def __init__(self):
                    self.returncode = 0
                    self.stdout = "mock tree output\n"
                    self.stderr = b""
            if cmd[0] == 'tree':
                return Result()
            return Result()

        original_run = subprocess.run
        subprocess.run = mock_run

        # Mock shutil.which to pretend 'tree' exists
        import shutil
        original_which = shutil.which
        shutil.which = lambda cmd: '/usr/bin/tree' if cmd == 'tree' else None

        try:
            files_to_clipboard([file_path], include_tree=True, sys_file=sys_file)
        finally:
            subprocess.run = original_run
            shutil.which = original_which
            os.unlink(sys_file)
            os.unlink(file_path)

if __name__ == '__main__':
    unittest.main()
