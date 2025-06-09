import unittest

from blocknode import BlockType
from blocknode import block_to_block_type

class TestBlockType(unittest.TestCase):
    def test_header1(self):
        markdown = "# this is a header"
        self.assertEqual(BlockType.HEADING, block_to_block_type(markdown))
    def test_header2(self):
        markdown = "## this is a header"
        self.assertEqual(BlockType.HEADING, block_to_block_type(markdown))
    def test_header3(self):
        markdown = "### this is a header"
        self.assertEqual(BlockType.HEADING, block_to_block_type(markdown))
    def test_header4(self):
        markdown = "#### this is a header"
        self.assertEqual(BlockType.HEADING, block_to_block_type(markdown))
    def test_header5(self):
        markdown = "##### this is a header"
        self.assertEqual(BlockType.HEADING, block_to_block_type(markdown))
    def test_header6(self):
        markdown = "###### this is a header"
        self.assertEqual(BlockType.HEADING, block_to_block_type(markdown))
    def test_code(self):
        markdown = "```this is a line of code```"
        self.assertEqual(BlockType.CODE, block_to_block_type(markdown))
    def test_code_multiline(self):
        markdown = """```this is a line of code
and this is another line of code
followed by more lines of code```"""
        self.assertEqual(BlockType.CODE, block_to_block_type(markdown))

    def test_quote(self):
        markdown = "> some quote"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(markdown))
    
    def test_quote_multiline(self):
        markdown = """> this is a line of quote
> and this is another line of quote"""
        self.assertEqual(BlockType.QUOTE, block_to_block_type(markdown))

    def test_unordered_list_multiline(self):
        markdown = """- this is a line of list
- and this is another line of list
- and more list"""
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(markdown))

    def test_ul(self):
        markdown = "- some quote"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(markdown))

    def test_ol(self):
        markdown = "* some quote"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(markdown))

    def test_ordered_list_multiline(self):
        markdown = """* this is a line of list
* and this is another line of list"""
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(markdown))

    def test_paragraph(self):
        markdown = "This is just a paragraph"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(markdown))
