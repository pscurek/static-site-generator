from enum import Enum
from htmlnode import LeafNode
from htmlnode import ParentNode

class MathType(Enum):
    IDENTIFIER = "identifier"
    NUMBER = "number"
    OPERATOR = "operator"

class MathNode:
    def __init__(self, text, math_type):
        self.text = text
        self.math_type = math_type

    def __eq__(self, other):
        is_equal = (
                self.text == other.text and
                self.math_type == other.math_type and
            )
        return is_equal

    def __repr__(self):
        return f"MathNode({self.text}, {self.math_type.value})"

def math_node_to_html_node(math_node):
    match math_node.math_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case TextType.MATH:
            return LeafNode("math", text_node.text, {"display": "inline"})
        case _:
            raise TypeError("invalid TextType")
