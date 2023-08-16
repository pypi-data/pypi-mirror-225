import argparse
import logging
import os
import subprocess
import tomllib
from datetime import datetime

import randomname

logging.basicConfig(level=logging.ERROR)


def load_config_file():
    file_path = os.path.expanduser("~/.config/zeka.toml")
    if os.path.isfile(file_path):
        try:
            with open(file_path, "rb") as f:
                config = tomllib.load(f)
            return config
        except Exception as e:
            logging.error(f"Error loading config file: {e}")
            return None

    else:
        return None


def collect_user_input():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--title")
    parser.add_argument("-a", "--tags", default="[]")
    parser.add_argument("-l", "--lang", default="en-US")

    args = parser.parse_args()

    return args


def create_front_matter(args):
    metadata = {}
    time = datetime.now().isoformat()
    metadata["time"] = time

    if args.title:
        metadata["title"] = args.title
    else:
        metadata["title"] = randomname.get_name()

    if args.lang:
        metadata["lang"] = args.lang
    else:
        metadata["lang"] = "en-US"

    if args.tags:
        metadata["tags"] = args.tags
    else:
        metadata["tags"] = "[]"

    front_matter = ""

    for key, value in metadata.items():
        front_matter += f"{key}: {value}\n"

    front_matter = f"---\n{front_matter}---\n"

    return metadata["title"], front_matter


def create_zeka(filename: str, front_matter, path):
    path += filename
    with open(f"{path}.md", "w") as f:
        f.write(front_matter)


def open_zeka(filename):
    editor = os.environ.get("EDITOR")
    subprocess.run([editor, f"{filename}.md"])


def main():
    args = collect_user_input()
    filename, front_matter = create_front_matter(args)
    config = load_config_file()
    if config is None:
        save_path = "./"
    else:
        save_path = config["settings"]["save_path"]
        save_path = os.path.expanduser(save_path)
    create_zeka(filename=filename, front_matter=front_matter, path=save_path)
    file = save_path + filename
    open_zeka(file)


if __name__ == "__main__":
    main()
