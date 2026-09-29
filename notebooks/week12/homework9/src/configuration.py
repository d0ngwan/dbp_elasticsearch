import os
import yaml

class Configuration:
    def __init__(self):
        self.config = None
        self.load_config()

    def load_config(self):
        config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config')
        config_file = os.path.join(config_dir, 'config.yml')
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)

    def get_config(self, key):
        return self.config[key] if key in self.config else None
