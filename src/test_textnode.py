import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = TextNode("This is a code node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        self.assertEqual(repr(node), "TextNode(This is an italic text node, italic, None)")

    def test_comparison(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertTrue(node1 == node2)

    def test_url(self):
        node1 = TextNode("This is a link text node", TextType.LINK, "http://example.com")
        node2 = TextNode("This is a link text node", TextType.LINK)
        self.assertNotEqual(node1, node2)
        self.assertFalse(node1.url == node2.url)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("anchor text", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "anchor text")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://example.com", "alt": "alt text"})

    def test_code(self):
        node = TextNode("some code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "some code")
        self.assertEqual(html_node.props, None)

    def test_no_text_type(self):
        node = TextNode("text", None)
        with self.assertRaises(TypeError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()
