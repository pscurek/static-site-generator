from textnode import TextNode, TextType
from copystatic import copy_static_to_public
from page_generator import generate_pages_recursive

def main():
    # node = TextNode("This is some anchor text", TextType.LINK, "https://www.example.com")
    # print(node)

    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
