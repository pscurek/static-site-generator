import os
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.strip().split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Invalid Markdown: missing title")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    node = markdown_to_html_node(md)
    html_content = node.to_html()
    html_title = extract_title(md)
    full_html = template.replace("{{ Title }}", html_title).replace("{{ Content }}", html_content)
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(full_html)

def generate_pages_recursive(content_dir_path, template_path, dest_dir_path, basepath):
    content_files = os.listdir(content_dir_path)
    for file in content_files:
        from_path = os.path.join(content_dir_path, file)
        root, extension = os.path.splitext(file)
        if os.path.isfile(from_path) and extension == ".md":
            dest_file_name = f"{root}.html"
            dest_path = os.path.join(dest_dir_path, dest_file_name)
            generate_page(from_path, template_path, dest_path, basepath)
        if os.path.isdir(from_path):
            dest_path = os.path.join(dest_dir_path, file)
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
