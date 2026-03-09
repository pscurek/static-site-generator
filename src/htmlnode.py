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
