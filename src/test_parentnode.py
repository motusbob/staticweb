import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildrens(self):
        grandchild_node1 = LeafNode("b", "grandchild bold")
        grandchild_node2 = LeafNode("i", "grandchild italic")
        child_node = ParentNode("span", [grandchild_node1, grandchild_node2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild bold</b><i>grandchild italic</i></span></div>",
        )

    def test_to_html_with_no_children(self):
        child_node = LeafNode("head", "some text")
        parent_node = ParentNode("html", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<html><head>some text</head></html>",
        )


