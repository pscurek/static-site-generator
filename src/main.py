import sys
from textnode import TextNode, TextType
from copystatic import copy_files
from page_generator import generate_pages_recursive

def main():
    # node = TextNode("This is some anchor text", TextType.LINK, "https://www.example.com")
    # print(node)

    if len(sys.argv) >= 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    dir_path_static = "./static"
    dir_path_public = "./docs"
    dir_path_content = "./content"
    template_path = "./template.html"

    copy_files(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)

if __name__ == "__main__":
    main()
