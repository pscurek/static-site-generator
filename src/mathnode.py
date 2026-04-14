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
        case MathType.IDENTIFIER:
            return LeafNode("mi", math_node.text)
        case MathType.NUMBER:
            return LeafNode("mn", math_node.text)
        case MathType.OPERATOR:
            return LeafNode("mo", math_node.text)
        case _:
            raise TypeError("invalid TextType")
