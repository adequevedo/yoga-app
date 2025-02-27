from pathlib import Path
import os
import json


class MetadataHelper:
    def __init__(self, file_path: str):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = Path(self.base_dir) / file_path

    def get_metadata(self):
        with self.file_path.open("r") as f:
            metadata = json.load(f)
        return metadata
