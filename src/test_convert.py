import unittest
from convert import *

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
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

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual([TextNode("This is text with a ", TextType.TEXT),TextNode("code block", TextType.CODE),TextNode(" word", TextType.TEXT)], new_nodes)

    def test_split_bold(self):
        node = [TextNode("This is **bold1** text", TextType.TEXT), TextNode("This is **bold2** text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is ", TextType.TEXT),TextNode("bold1", TextType.BOLD),TextNode(" text", TextType.TEXT),TextNode("This is ", TextType.TEXT),TextNode("bold2", TextType.BOLD),TextNode(" text", TextType.TEXT)])

    def test_split_italic(self):
        node = TextNode("This is _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is ", TextType.TEXT),TextNode("italic", TextType.ITALIC)])

    def test_split_no_delimiter(self):
        node = TextNode("This is just text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual([node], new_nodes)

    def test_split_invalid_markdown(self):
        node = TextNode("This is **bold text", TextType.TEXT)
        #new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
            self.assertTrue("invalid markdown" in context.exception)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images("this is 2 images ![image1](host1) and ![image2](host2)")
        self.assertListEqual([("image1","host1"),("image2","host2")], matches)

    def test_extract_markdown_multiple_link(self):
        matches = extract_markdown_links("REF: [link1](url1) [link2](url2) [link3](url3)")
        self.assertListEqual([("link1","url1"),("link2","url2"),("link3","url3")], matches)

    def test_extract_image_from_site(self):
        matches = extract_markdown_images("blabla ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual(matches, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_link_from_site(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual(matches, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])


    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_first(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) and some text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),TextNode(" and some text", TextType.TEXT)], new_nodes)

    def test_split_images_after(self):
        node = TextNode("Some text then ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("Some text then ", TextType.TEXT), TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")], new_nodes)

    def test_split_images_from_link(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another [somelink](https://i.imgur.com/)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another [somelink](https://i.imgur.com/)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
        "This is text with a [link](https://i.imgur.com) and another [link](https://i.imgur.com)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link", TextType.LINK, "https://i.imgur.com"
                ),
            ],
            new_nodes,
        )

    def test_split_links_first(self):
        node = TextNode("[link](https://i.imgur.com) and some text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("link", TextType.LINK, "https://i.imgur.com"),TextNode(" and some text", TextType.TEXT)], new_nodes)

    def test_split_links_after(self):
        node = TextNode("Some text then a [link](https://i.imgur.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("Some text then a ", TextType.TEXT), TextNode("link", TextType.LINK, "https://i.imgur.com")], new_nodes)

    def test_split_links_from_image(self):
        node = TextNode(
        "This is text with a [link](https://i.imgur.com) and ![someimage](https://i.imgur.com/abc.jpg)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com"),
                TextNode(" and ![someimage](https://i.imgur.com/abc.jpg)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_full_split(self):
        node = TextNode('This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)', TextType.TEXT)
        new_nodes = text_to_textnodes([node])
        self.assertListEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])


if __name__ == "__main__":
    unittest.main()
