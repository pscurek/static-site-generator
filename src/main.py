from textnode import TextNode, TextType
from system_functions import copy_static_to_public

def main():
    # node = TextNode("This is some anchor text", TextType.LINK, "https://www.example.com")
    # print(node)

    copy_static_to_public()

if __name__ == "__main__":
    main()
