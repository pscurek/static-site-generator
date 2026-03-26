from textnode import TextNode, TextType
from system_functions import copy_static_to_public
from page_generator import generate_page

def main():
    # node = TextNode("This is some anchor text", TextType.LINK, "https://www.example.com")
    # print(node)

    copy_static_to_public()
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
