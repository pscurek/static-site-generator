import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError("invalid Markdown: formatted section not closed")
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(split_text[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(split_text[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)

def extract_markdown_math(text):
    return re.findall(r"\$([\S].*?[\S])\$", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
       
        extracted_images = extract_markdown_images(node.text)
        if extracted_images == []:
            new_nodes.append(node)
            continue
      
        split_nodes = []
        text_to_split = node.text
        for alt_text, image_link in extracted_images:
            sections = text_to_split.split(f'![{alt_text}]({image_link})', 1)
            
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_link))
            text_to_split = sections[1]
        if sections[1]:
            new_nodes.append(TextNode(sections[1], TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
       
        extracted_links = extract_markdown_links(node.text)
        if extracted_links == []:
            new_nodes.append(node)
            continue
      
        split_nodes = []
        text_to_split = node.text
        for anchor_text, link in extracted_links:
            sections = text_to_split.split(f'[{anchor_text}]({link})', 1)
            
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, link))
            text_to_split = sections[1]
        if sections[1]:
            new_nodes.append(TextNode(sections[1], TextType.TEXT))
    return new_nodes

def split_nodes_math(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
       
        extracted_math = extract_markdown_math(node.text)
        if extracted_math == []:
            new_nodes.append(node)
            continue
      
        split_nodes = []
        text_to_split = node.text
        for math_text in extracted_math:
            sections = text_to_split.split(f'${math_text}$', 1)
            
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(math_text, TextType.MATH))
            text_to_split = sections[1]
        if sections[1]:
            new_nodes.append(TextNode(sections[1], TextType.TEXT))
    return new_nodes

def text_to_textnodes(text): 
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_math(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes
