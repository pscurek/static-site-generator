import unittest

from leafnode import LeafNode

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

if __name__ == "__main__":
    unittest.main()
