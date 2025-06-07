import unittest
from convert import *

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq1(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_eq3(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node, node2)

    def test_eq4(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_eq5(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        node2 = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        self.assertEqual(node, node2)

    def test_diff(self):
        node = TextNode("this is a node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("this is a node", TextType.IMAGE, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_diff1(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_diff2(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        node2 = TextNode("This is an image", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_diff3(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a link", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text")
        self.assertEqual(html_node.to_html(), "<b>This is a bold text</b>")

    def test_italic(self):
        node = TextNode("this is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "this is italic")
        self.assertEqual(html_node.to_html(), "<i>this is italic</i>")

if __name__ == "__main__":
    unittest.main()
