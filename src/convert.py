from textnode import TextNode, TextType
from leafnode import LeafNode
from blocknode import BlockType, block_to_block_type
from htmlnode import HTMLNode
from parentnode import ParentNode
import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text.replace("\n"," "))
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": f"{text_node.url}"})
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
            if image_info is None:
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
            if link_info is None:
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
    new_nodes = split_nodes_link(text)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split("\n\n")]
    return blocks



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    node_list = []
#    print(blocks)
    for block in blocks:
        block_type = block_to_block_type(block)
        #print(block_type)
        match block_type:
            case BlockType.PARAGRAPH:
                node = [TextNode(block, TextType.TEXT)]
                new_node = text_to_textnodes(node)
                extra_html = []
                for node in new_node:
                    extra_html.append(text_node_to_html_node(node))
                if len(extra_html) != 0:
                    parn_node = ParentNode("p", extra_html) # p node over test
                    node_list.append(parn_node)
            case BlockType.HEADING:
                node = [TextNode(block, TextType.TEXT)]
                for n in node:
                    hash_count = n.text.count('#')
                    n.text = n.text.lstrip("#").lstrip()
                    new_node = LeafNode(f"h{hash_count}", n.text) # header node with #count
                    node_list.append(new_node)
            case BlockType.CODE:
                code_text = block.strip("```\n")
                code_text = code_text.split("\n")
                code_text = "\n".join(code_text)+"\n"
                html_node = LeafNode("code", code_text) # code node
                pre_node = ParentNode("pre", [html_node]) # pre node over code node
                node_list.append(pre_node)
            case BlockType.QUOTE:
                node = [TextNode(block, TextType.TEXT)]
                for n in node:
                    n.text = n.text.lstrip(">").lstrip()
                    this_tag = "blockquote"
                    new_node = LeafNode(this_tag, n.text)
                    node_list.append(new_node)
            case BlockType.UNORDERED_LIST:
                node_text = block[2:].split("\n")
                list_node = []
                for node in node_text:
                    text = node.lstrip("- ")
                    new_node = LeafNode("li", text)  # header node with #count
                    list_node.append(new_node)
                node_list.append(ParentNode("ul", list_node)) # with li child

            case BlockType.ORDERED_LIST:  # TODO TODO
                node_text = block.split("\n")
                list_node = []
                for node in node_text:
                    index_space = [pos for pos, char in enumerate(node) if char == " "]
                    first_space = index_space.pop(0)
                    text = node[first_space+1:]
                    new_node = LeafNode("li", text)  # header node with #count
                    list_node.append(new_node)
                node_list.append(ParentNode("ol", list_node)) # with li child
            case _:
                raise Exception("Unknown Markdown")

    return ParentNode("div", node_list) # overall parent node
