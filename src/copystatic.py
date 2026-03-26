import os
import shutil
from datetime import datetime

def copy_static_to_public():
    root = os.getcwd()
    if not root.endswith("static-site-generator"):
        raise Exception("not a valid path")
    static_path = os.path.join(root, "static")
    public_path = os.path.join(root, "public")
    log_path = os.path.join(root, f"logs/{datetime.now().strftime("%Y.%m.%d-%I.%M.%S")}-static_to_public.log")

    try:
        with open(log_path, "w") as f:
            f.write(f"copying contents of {static_path} to {public_path} ...\n")
    except Exception as e:
        print(e)
        return

    if os.path.exists(public_path):
        shutil.rmtree(public_path)
        add_to_log(log_path, f"directory {public_path} removed recursively")

    os.mkdir(public_path)
    add_to_log(log_path, f"directory {public_path} created")
    recursive_copy(static_path, public_path, log_path)

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
