import unittest
import inspect
from block_markdown import (
        BlockType,
        markdown_to_blocks,
        block_to_block_type,
        markdown_to_html_node,
)

class TestMarkdownToBocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md =  inspect.cleandoc(
            """
            This is **bolded** paragraph
            
            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line
            
            - This is a list
            - with items
            """
        )
        actual = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(actual, expected)

    def test_markdown_to_blocks_extra_whitespace(self):
        md =  inspect.cleandoc(
            """
                This is **bolded** paragraph
           

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line    
            
              - This is a list
            - with items
            """
        )
        actual = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(actual, expected)

    def test_markdown_to_blocks_single_block(self):
        md = "This is a paragraph with\ntwo lines."
        actual = markdown_to_blocks(md)
        expected = [
            "This is a paragraph with\ntwo lines.",
        ]
        self.assertEqual(actual, expected)

    def test_markdown_to_blocks_just_whitespace(self):
        md = "   \n     \n\n    "
        actual = markdown_to_blocks(md)
        expected = []
        self.assertEqual(actual, expected)

    def test_markdown_to_blocks_empty_markdown(self):
        md = ""
        actual = markdown_to_blocks(md)
        expected = []
        self.assertEqual(actual, expected)

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        block = "# this is a heading"
        actual = block_to_block_type(block)
        expected = BlockType.HEADING
        self.assertEqual(actual, expected)

    def test_block_to_block_type_multiline_code(self):
        block = inspect.cleandoc(
                """
                ```
                x = [1, 2, 3, 4, 5]
                for i in x:
                    print(i)
                ```
                """
        )
        actual = block_to_block_type(block)
        expected = BlockType.CODE
        self.assertEqual(actual, expected)

    def test_block_to_block_type_quote_block(self):
        block = inspect.cleandoc(
                """
                >quote line 1
                > quote line 2
                > quote line 3
                >quote line 4
                """
        )
        actual = block_to_block_type(block)
        expected = BlockType.QUOTE
        self.assertEqual(actual, expected)

    def test_block_to_block_type_unordered_list(self):
        block = inspect.cleandoc(
                """
                - item 1
                - item 2
                - item 3
                - item 4
                - item 5
                """
        )
        actual = block_to_block_type(block)
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(actual, expected)

    def test_block_to_block_type_ordered_list(self):
        block = inspect.cleandoc(
                """
                1. item 1
                2. item 2
                3. item 3
                4. item 4
                5. item 5
                """
        )
        actual = block_to_block_type(block)
        expected = BlockType.ORDERED_LIST
        self.assertEqual(actual, expected)
        
    def test_block_to_block_type_paragraph(self):
        block = inspect.cleandoc(
                """
                # item
                1. item
                > item
                - item
                Regular Paragraph
                """
        )
        actual = block_to_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(actual, expected)
    
    def test_block_to_block_type_math(self):
        block = inspect.cleandoc(
                """
                $$$
                a(b + c) = ab + ac
                $$$
                """
        )
        actual = block_to_block_type(block)
        expected = BlockType.MATH
        self.assertEqual(actual, expected)

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = inspect.cleandoc(
            """
            This is **bolded** paragraph
            text in a p
            tag here
            
            This is another paragraph with _italic_ text and `code` here
            """
        )

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = inspect.cleandoc(
            """
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """
        )

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_headings(self):
        md = inspect.cleandoc(
            """
            # Heading 1

            ## Heading 2

            ### Heading 3

            #### Heading 4

            ##### Heading 5

            ###### Heading 6
            """
        )

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
        )

    def test_blockquote(self):
        md = inspect.cleandoc(
            """
            >
            > This is a block quote
            > with multiple
            >lines
            >
            >and markdown
            > formatting
            > 
            """
        )

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>This is a block quote with multiple lines</p><p>and markdown formatting</p></blockquote></div>",
        )

    def test_empty_blockquote(self):
        md = inspect.cleandoc(
            """
            >
            >
            >
            """
        )

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote></blockquote></div>",
        )

    def test_unordered_list(self):
        md = inspect.cleandoc(
            """
            - item 1
            - item 2
            - item 3
            """
        )

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item 1</li><li>item 2</li><li>item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = inspect.cleandoc(
            """
            1. item 1
            2. item 2
            3. item 3
            """
        )

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>item 1</li><li>item 2</li><li>item 3</li></ol></div>",
        )

    def test_multiple_blocks(self):
        md = inspect.cleandoc(
            """
            This is a paragraph
            with **multiple** lines

            ### Here is an _ordered_ list

            1. write `code`
            2. test
            3. repeat
            """
        )

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph with <b>multiple</b> lines</p><h3>Here is an <i>ordered</i> list</h3><ol><li>write <code>code</code></li><li>test</li><li>repeat</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()
