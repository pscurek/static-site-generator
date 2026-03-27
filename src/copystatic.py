import os
import shutil
from datetime import datetime

def copy_files(source_path, dest_path):
    root = os.getcwd()
    if not root.endswith("static-site-generator"):
        raise Exception("not a valid path")
    log_path = os.path.join(root, f"logs/{datetime.now().strftime("%Y.%m.%d-%I.%M.%S")}-static_to_public.log")

    try:
        with open(log_path, "w") as f:
            f.write(f"copying contents of {source_path} to {dest_path} ...\n")
    except Exception as e:
        print(e)
        return

    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
        add_to_log(log_path, f"directory {dest_path} removed recursively")

    os.mkdir(dest_path)
    add_to_log(log_path, f"directory {dest_path} created")
    recursive_copy(source_path, dest_path, log_path)

def recursive_copy(source, destination, log_path):
    contents = os.listdir(source)
    for item in contents:
        item_source_path = os.path.join(source, item)
        item_destination_path = os.path.join(destination, item)
        if os.path.isfile(item_source_path):
            shutil.copy(item_source_path, item_destination_path)
            add_to_log(log_path, f"file {item_source_path} copied to {item_destination_path}")
        else:
            os.mkdir(item_destination_path)
            add_to_log(log_path, f"directory {item_destination_path} created to mimic {item_source_path}")
            recursive_copy(item_source_path, item_destination_path, log_path)

def add_to_log(path, message):
    with open(path, "a") as f:
        f.write(f"\n{message}")
