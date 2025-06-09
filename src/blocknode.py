from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    #matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    #print(block[0:3], block[-3:])
    #print(re.findall(r"^\> .*$", block, re.MULTILINE))
    #print(len(block.split("\n")))
    if len(re.findall(r"^#{1,6} ", block)) == 1:
        return BlockType.HEADING
    #elif block[0:3] == "```" and block[-3:] == "```":
    elif len(re.findall(r"^```(\n|.)*?```$", block, re.MULTILINE)) == 1:
        return BlockType.CODE
    elif len(re.findall(r"^> .*$", block, re.MULTILINE)) == len(block.split("\n")):
        return BlockType.QUOTE
    elif len(re.findall(r"^- .*$", block, re.MULTILINE)) == len(block.split("\n")):
        return BlockType.UNORDERED_LIST
    elif len(re.findall(r"^\* .*$", block, re.MULTILINE)) == len(block.split("\n")):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
                                                

