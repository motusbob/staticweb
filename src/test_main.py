import unittest
from main import *

class TestBlockType(unittest.TestCase):
    def test_h1_header(self):
        markdown = "# TITLE"
        self.assertEqual(extract_title(markdown), "TITLE")

    def test_split_invalid_markdown(self):
        markdown = "TITLE"
        with self.assertRaises(Exception) as context:
            title = extract_title(markdown)
            self.assertTrue("No title found" in context.exception)
