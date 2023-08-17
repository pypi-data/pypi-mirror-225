import os, sys

def init(root_dir = ".", excludes = []):
    _excludes = [
        "__pycache__",
        ".directory",
        ".Trashes",
        ".Python",
        ".pybuilder",
        ".ipynb_checkpoints",
        ".venv"
    ]
    _excludes += excludes
    for (dir_path, dir_names, file_names) in os.walk(root_dir):
        for ex in _excludes:
            if ex not in dir_path:
                sys.path.insert(0, dir_path)

if __name__ == "__main__":
    init()