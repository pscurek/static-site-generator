import os
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.strip().split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Invalid Markdown: missing title")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    node = markdown_to_html_node(md)
    html_content = node.to_html()
    html_title = extract_title(md)
    full_html = template.replace("{{ Title }}", html_title).replace("{{ Content }}", html_content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(full_html)

