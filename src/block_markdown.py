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
        if re.fullmatch(r"(#{1,6} .*)", block):
            return BlockType.HEADING
        elif re.fullmatch(r"(```\n[\s\S]*```)", block):
            return BlockType.CODE

        lines = block.split("\n")
        line_number = 1
        is_quote_block = True
        is_unordered_list = True
        is_ordered_list = True
        for line in lines:
            if is_quote_block and not line.startswith(">"):
                is_quote_block = False
            if is_unordered_list and not line.startswith("- "):
                is_unordered_list = False
            if is_ordered_list and not line.startswith(f"{line_number}. "):
                is_ordered_list = False
            
            if not (is_quote_block or is_unordered_list or is_ordered_list):
                break

            line_number += 1

        if is_quote_block:
            return BlockType.QUOTE
        elif is_unordered_list:
            return BlockType.UNORDERED_LIST
        elif is_ordered_list:
            return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH
