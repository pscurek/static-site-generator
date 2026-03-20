def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in raw_blocks:
        striped_block = block.strip()
        if striped_block == "":
            continue
        clean_blocks.append(striped_block)
    return clean_blocks
