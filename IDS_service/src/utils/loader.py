
import yaml

def load_yaml(path_file):
    with open(path_file) as f:
        configs = yaml.safe_load(f)
    return configs