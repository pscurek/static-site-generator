import re
from enum import Enum
from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import ParentNode, LeafNode 
from inline_markdown import text_to_textnodes

class BlockType(Enum):
   PARAGRAPH = "paragraph"
   HEADING = "heading"
   CODE = "code"
   QUOTE = "quote"
   UNORDERED_LIST = "unordered_list"
   ORDERED_LIST = "ordered_list"
   MATH = "math"

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
    if re.fullmatch(r"(```\n[\s\S]*```)", block):
        return BlockType.CODE
    if re.fullmatch(r"(\$\$\$[\s\S]*\$\$\$)", block):
        return BlockType.MATH

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

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block) 
        case BlockType.HEADING:
            return heading_to_html_node(block) 
        case BlockType.CODE:
            return code_to_html_node(block) 
        case BlockType.QUOTE:
            return quote_to_html_node(block) 
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block) 
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block) 
        case BlockType.MATH:
            return math_to_html_node(block)
        case _:
            raise TypeError(f'invalid BlockType: {block_type}')

def paragraph_to_html_node(block):
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))

def heading_to_html_node(block):
    for i in range(1, 7):
     if block[i] == " ":
         text = block[i + 1:]
         return ParentNode(f'h{i}', text_to_children(text)) 

def code_to_html_node(block):
    text = block[4:-4]
    text_node = TextNode(text, TextType.TEXT)
    code_node = ParentNode("code", [text_node_to_html_node(text_node)])
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    lines = block.split("\n")
    children = []
    current_text_list = []
    for line in lines:
        line_text = line[1:].strip()
        if line_text == "":
            current_text = " ".join(current_text_list).strip()
            if current_text:
                children.append(ParentNode("p", text_to_children(current_text)))
            current_text_list.clear()
            continue
        current_text_list.append(line_text)
    current_text = " ".join(current_text_list).strip()
    if current_text:
        children.append(ParentNode("p", text_to_children(current_text)))
    if children:
        return ParentNode("blockquote", children)
    return LeafNode("blockquote", "")

def unordered_list_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        line_text = line[2:]
        children.append(ParentNode("li", text_to_children(line_text)))
    return ParentNode("ul", children)

def ordered_list_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        line_text = line[3:]
        children.append(ParentNode("li", text_to_children(line_text)))
    return ParentNode("ol", children)

def math_to_html_node(block):
    # ToDo
    pass

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown.strip())
    block_nodes = []
    for block in blocks:
        block_nodes.append(block_to_html_node(block))
    return ParentNode("div", block_nodes)
