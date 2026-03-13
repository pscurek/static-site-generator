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

    def test_to_html_None_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_empty_children_list(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_multiple_children_and_grandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild1")
        grandchild_node2 = LeafNode("p", "grandchild2")
        child_node1 = ParentNode("span", [grandchild_node1])
        child_node2 = ParentNode("span", [grandchild_node2])
        parent_node = ParentNode("div", [child_node1, child_node2])
        actual = parent_node.to_html()
        expected = "<div><span><b>grandchild1</b></span><span><p>grandchild2</p></span></div>"
        self.assertEqual(actual, expected)

    def test_to_html_with_children_and_props(self):
        child_node = LeafNode("span", "child", {"prop1": "property1", "prop2": "property2"})
        parent_node = ParentNode("div", [child_node], {"prop1": "property1"})
        actual = parent_node.to_html()
        expected = '<div prop1="property1"><span prop1="property1" prop2="property2">child</span></div>'
        self.assertEqual(actual, expected)

    def test_to_html_with_children_and_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"prop1": "property1"})
        actual = repr(parent_node)
        expected = "ParentNode(div, [LeafNode(span, child, None)], {'prop1': 'property1'})"
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
