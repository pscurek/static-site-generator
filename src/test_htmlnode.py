import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode 

class TestHTMLNode(unittest.TestCase):
    def test_one_prop(self):
        node = HTMLNode(props={"href": "https://example.com"})
        actual = node.props_to_html()
        expected = ' href="https://example.com"'
        self.assertEqual(actual, expected)

    def test_two_props(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        actual = node.props_to_html()
        expected = ' href="https://example.com" target="_blank"'
        self.assertEqual(actual, expected)

    def test_no_props(self):
        node = HTMLNode()
        actual = node.props_to_html()
        expected = ''
        self.assertEqual(actual, expected)

    def test_repr(self):
        node = HTMLNode("sample_tag", "sample_value", ["child1", "child2"], {"prop1": 1, "prop2": 2})
        actual = repr(node)
        expected = "HTMLNode(sample_tag, sample_value, ['child1', 'child2'], {'prop1': 1, 'prop2': 2})"
        self.assertEqual(actual, expected)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
       node = LeafNode("p", "Hello, world!") 
       actual = node.to_html()
       expected = '<p>Hello, world!</p>'
       self.assertEqual(actual, expected) 

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "some link text", {"href": "https://example.com"})
        actual = node.to_html()
        expected = '<a href="https://example.com">some link text</a>'
        self.assertEqual(actual, expected)

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode('a', 'link text', {'href': 'https://example.com', 'target': '_blank'})
        actual = node.to_html()
        expected = '<a href="https://example.com" target="_blank">link text</a>'
        self.assertEqual(actual, expected)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        actual = node.to_html()
        expected = "Hello, world!"
        self.assertEqual(actual, expected)

    def test_repr(self):
        node = LeafNode('a', 'link text', {'href': 'https://example.com', 'target': '_blank'})
        actual = repr(node)
        expected = "LeafNode(a, link text, {'href': 'https://example.com', 'target': '_blank'})"
        self.assertEqual(actual, expected)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        actual = parent_node.to_html()
        expected = "<div><span>child</span></div>"
        self.assertEqual(actual, expected)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        actual = parent_node.to_html()
        expected = "<div><span><b>grandchild</b></span></div>"
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
