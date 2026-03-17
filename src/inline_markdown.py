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

def split_nodes_image(old_nodes):
    pass
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
       
        extracted_images = extract_markdown_images(node.text)
        if extracted_images == []:
            new_node.append(node)
            continue
      
        split_nodes = []
        for alt_text, image_link in extracted_images:
            sections = node.text.split(f'![{alt_text}]({image_link})', 1)
            text_nodes = [
                    TextNode(sections[0], TextType.TEXT),
                    TextNode(alt_text, TextType.IMAGE, image_link)
                    TextNode(sections[1], TextType.TEXT),
            ]

def split_nodes_link(old_nodes):
    pass
