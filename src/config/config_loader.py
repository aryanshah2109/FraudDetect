import yaml

from src.path_constants import CONFIG_PATH


def load_config():
    """
        Function to load config.yaml file and then returns the loaded object
    """

    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)