import unittest

from htmlnode import HTMLNode 

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

if __name__ == "__main__":
    unittest.main()
