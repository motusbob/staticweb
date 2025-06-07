import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href":'"https://www.google.com"'})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_bold(self):
        node = LeafNode("b", "some BOLD text")
        self.assertEqual(node.to_html(), "<b>some BOLD text</b>")

    def test_leaf_to_html_it(self):
        node = LeafNode("i", "some _italic_ text")
        self.assertEqual(node.to_html(), "<i>some _italic_ text</i>")
