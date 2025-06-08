from textnode import TextNode, TextType
from leafnode import LeafNode
import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return Leafnode("a", text_node.text, None, {"href": f"{text_node.url}"})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": f"{text_node.url}", "alt": text_node.text})
        case _:
            raise Exception("invalid TextType")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    match delimiter:
        case "`":
            node_type = TextType.CODE
        case "**":
            node_type = TextType.BOLD
        case "_":
            node_type = TextType.ITALIC
        case _:
            raise Exception("invalid delimiter")
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
        else:
            if delimiter in node.text:
                split_node = node.text.split(delimiter)
                if len(split_node) != 3:
                    raise Exception("invalid markdown")
                new_nodes.append(TextNode(split_node[0], TextType.TEXT))
                new_nodes.append(TextNode(split_node[1], node_type))
                if len(split_node) > 2 and len(split_node[2]) > 0:
                    new_nodes.append(TextNode(split_node[2], TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    #r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    #matches = re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    #r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    #matches = re.findall(r"\[(.*?)\]\((.*?)\)",text)
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            image_info = extract_markdown_images(node.text)
            if image_info == None:
                new_nodes.append(node)
            else:
                work_text = node.text
                while len(image_info) > 0:
                    this_image = image_info.pop(0)
                    segments = work_text.split(f"![{this_image[0]}]({this_image[1]})", 1)
                    if len(segments[0]) > 0:
                        new_nodes.append(TextNode(segments[0], TextType.TEXT))
                    new_nodes.append(TextNode(this_image[0],TextType.IMAGE,this_image[1]))
                    if len(segments) >= 1:
                        work_text = segments[1]
                if work_text != "":
                    new_nodes.append(TextNode(work_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            link_info = extract_markdown_links(node.text)
            if link_info == None:
                new_nodes.append(node)
            else:
                work_text = node.text
                while len(link_info) > 0:
                    this_link = link_info.pop(0)
                    segments = work_text.split(f"[{this_link[0]}]({this_link[1]})", 1)
                    if len(segments[0]) > 0:
                        new_nodes.append(TextNode(segments[0], TextType.TEXT))
                    new_nodes.append(TextNode(this_link[0],TextType.LINK,this_link[1]))
                    if len(segments) >= 1:
                        work_text = segments[1]
                if work_text != "":
                    new_nodes.append(TextNode(work_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
#    print("\n\n", text)
    new_nodes = split_nodes_link(text)
#    print("\n\n", new_nodes)
    new_nodes = split_nodes_image(new_nodes)
#    print("\n\n", new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
#    print("\n\n", new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
#    print("\n\n", new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
#    print("\n\n", new_nodes)
    return new_nodes

