from typing import Dict, List

import json

class ManifestMissingModelNameException(Exception):
    def __init__(self,
                 manifest_file_path: str,
                 manifest_content: Dict,
                 available_model_names: List[str],
                 ):
        self.manifest_file_path = manifest_file_path
        self.manifest_content = manifest_content
        self.available_model_names = available_model_names

    def __str__(self):
        return (f"Missing Key ***model_name*** in manifest {self.manifest_file_path=} with content \n"
                f"{json.dumps(self.manifest_content, indent=4)} \n"
                f"Please add a key-value pair with key **model_name**. {self.available_model_names=}")
