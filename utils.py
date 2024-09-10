import toml
import yaml

def load_config(filename: str) -> dict:
    return toml.load(filename)

def load_yaml(filename: str) -> dict:
    with open(filename, 'r') as f:
        data = yaml.safe_load(f)
    return data