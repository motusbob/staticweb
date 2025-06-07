import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_no_tag(self):
        node = HTMLNode(None, "This is just some text")
        print(node)

    def test_no_value(self):
        node = HTMLNode("<head>", None, HTMLNode("<body>", "body of the html"))
        print(node)
    
    def test_image(self):
        node = HTMLNode("<img>", None, None, {"src": "url/of/image.jpg", "alt": "Description of image"})
        print(node)

