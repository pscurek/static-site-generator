import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links

class TestExtractMarkdownImagesAndLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        actual = matches
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
