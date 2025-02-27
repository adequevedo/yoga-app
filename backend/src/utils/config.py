import json
import os
from pathlib import Path


class ConfigHelper:
    def __init__(self, config_path: str, *args, **kwargs):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = Path(self.base_dir) / config_path
        self.config = self._open_config()

    def get_config(self, chain_name, section, *args, **kwargs):
        for chain in self.config["chains"]:
            if chain["name"] == chain_name:
                return chain["settings"][section]

    def _open_config(self):
        with self.config_path.open("r") as f:
            return json.load(f)
