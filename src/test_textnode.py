import unittest

from textnode import TextNode, TextType

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
        
if __name__ == "__main__":
    unittest.main()


