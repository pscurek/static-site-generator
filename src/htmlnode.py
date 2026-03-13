from textnode import TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})' 

    def to_html(self):
        raise NotImplementedError("to_html method has not been implemented")

    def props_to_html(self):
        props = self.props

        if props is None:
            return ""
        
        html = ""
        for key in props:
            html += f' {key}="{props[key]}"'
        return html

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'
   
    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

    def to_html(self):
        if self.tag is None:
            raise ValueError("value error: required property <tag> not present")
        if self.children is None or self.children == []:
            raise ValueError("value error: ParentNode object must have at least one child. No children provided.")
        child_html_list = []
        for child in self.children:
            child_html_list.append(child.to_html())
        child_html = "".join(child_html_list)
        return f'<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>'

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
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise TypeError("invalid TextType")
