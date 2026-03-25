import unittest
import inspect
from page_generator import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        md = "# Title"
        actual = extract_title(md)
        expected = "Title"
        self.assertEqual(actual, expected)

    def test_extra_whitespace(self):
        md = "#   This is a Title   "
        actual = extract_title(md)
        expected = "This is a Title"
        self.assertEqual(actual, expected)

    def test_title_not_first_line(self):
        md = inspect.cleandoc(
            """
            This is a markdown file called

            # This is a Title

            - item1
            - item2
            """
        )
        actual = extract_title(md)
        expected = "This is a Title"
        self.assertEqual(actual, expected)

    def test_no_title(self):
        md = inspect.cleandoc(
            """
            ## Title

            This is some markdown

            -item1
            -item2
            """
        )
        with self.assertRaises(Exception):
            title = extract_title(md)

if __name__ == "__main__":
    unittest.main()
