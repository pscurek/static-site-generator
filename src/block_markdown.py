import re
from enum import Enum

class BlockType(Enum):
   PARAGRAPH = "paragraph"
   HEADING = "heading"
   CODE = "code"
   QUOTE = "quote"
   UNORDERED_LIST = "unordered_list"
   ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in raw_blocks:
        striped_block = block.strip()
        if striped_block == "":
            continue
        clean_blocks.append(striped_block)
    return clean_blocks

def block_to_block_type(block):
        if re.match(r"(^#{1,6} [\s\S]*)", block):
            return BlockType.HEADING
        elif re.match(r"(```\n[\s\S]*```)", block):
            return BlockType.CODE

