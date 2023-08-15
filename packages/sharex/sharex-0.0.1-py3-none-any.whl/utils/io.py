from typing import Any, Text

import yaml


def read_yaml_file(file_path: Text) -> Any:
    """Reads a YAML file and returns a dictionary object"""

    try:
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
            return data
    except Exception as e:
        print(f"Error reading YAML file: {e}")
        return None
