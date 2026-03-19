import unittest

from textnode import (
        TextNode,
        TextType,
)

from inline_markdown import (
        split_nodes_delimiter,
        extract_markdown_images,
        extract_markdown_links,
        split_nodes_image,
        split_nodes_link,
)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_delim_code(self):
        nodes = [TextNode("this has `code block` text", TextType.TEXT)]
        actual = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
                TextNode("this has ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" text", TextType.TEXT)
            ]
        self.assertEqual(actual, expected)

    def test_no_matching_delimiter(self):
        nodes = [TextNode("this has `code block text", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    def test_no_delimiter(self):
        nodes = [TextNode("this has code block text", TextType.TEXT)]
        actual = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [TextNode("this has code block text", TextType.TEXT)]         
        self.assertEqual(actual, expected)

    def test_text_type_is_not_text(self):
        nodes = [TextNode("`this has code block text`", TextType.CODE)]
        actual = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(actual, nodes)

    def test_delim_italic(self):
        nodes = [TextNode("this has _italic_ text", TextType.TEXT)]
        actual = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        expected = [
                TextNode("this has ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT)
            ]
        self.assertEqual(actual, expected)

    def test_delim_bold(self):
        nodes = [TextNode("this has **bold** text", TextType.TEXT)]
        actual = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
                TextNode("this has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT)
            ]
        self.assertEqual(actual, expected)

    def test_delim_bold_multiple(self):
        nodes = [TextNode("this has **bold** text **here** and there", TextType.TEXT)]
        actual = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
                TextNode("this has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text ", TextType.TEXT),
                TextNode("here", TextType.BOLD),
                TextNode(" and there", TextType.TEXT),
            ]
        self.assertEqual(actual, expected)

    def test_delim_bold_and_italic(self):
        nodes = [TextNode("this has **bold** text and _italic_ text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        actual = new_nodes
        expected = [
                TextNode("this has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ]
        self.assertEqual(actual, expected)

class TestExtractMarkdownImagesAndLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        actual = matches
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(actual, expected)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        actual = matches
        expected = [("link", "https://example.com")]
        self.assertListEqual(actual, expected)

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image1](https://image1.png) here and an ![image2](https://image2.png) here"
        )
        actual = matches
        expected = [
                ("image1", "https://image1.png"),
                ("image2", "https://image2.png"),
        ]
        self.assertListEqual(actual, expected)

    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a [link1](https://example1.com) here and a [link2](https://example2.com) here"
        )
        actual = matches
        expected = [
                ("link1", "https://example1.com"),
                ("link2", "https://example2.com"),
        ]
        self.assertListEqual(actual, expected)

    def test_links_and_images_extract_links(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://image.png) here and a [link](https://example.com) here"
        )
        actual = matches
        expected = [("link", "https://example.com")]
        self.assertListEqual(actual, expected)

    def test_links_and_images_extract_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://image.png) here and a [link](https://example.com) here"
        )
        actual = matches
        expected = [("image", "https://image.png")]
        self.assertListEqual(actual, expected)

class TestSplitNodesOnImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_beginning_and_end(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_sequential_images(self):
        node = TextNode(
            "This is text with ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://second.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://second.example.com"
                ),
            ],
            new_nodes,
        )

    def test_split_links_at_beginning_and_end(self):
        node = TextNode(
            "[link](https://example.com) and another [second link](https://second.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://second.example.com"
                ),
            ],
            new_nodes,
        )

    def test_split_links_sequential_links(self):
        node = TextNode(
            "This is text with [link](https://example.com)[second link](https://second.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(
                    "second link", TextType.LINK, "https://second.example.com"
                ),
            ],
            new_nodes,
        )

    def test_split_links_then_images(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and an ![image](https://image.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "image", TextType.IMAGE, "https://image.png"
                ),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()
