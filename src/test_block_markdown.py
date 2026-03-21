import unittest
import inspect
from block_markdown import (
        BlockType,
        markdown_to_blocks,
        block_to_block_type,
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

if __name__ == "__main__":
    unittest.main()
