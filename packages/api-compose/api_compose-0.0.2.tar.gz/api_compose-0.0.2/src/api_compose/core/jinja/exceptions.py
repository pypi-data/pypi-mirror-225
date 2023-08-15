from pathlib import Path
from typing import List


class FailedToFindTemplateByPathException(Exception):
    def __init__(self,
                 template_search_paths: List[Path],
                 required_template_path: str,
                 available_template_paths: List[str],
                 ):
        self.template_search_paths = template_search_paths
        self.required_template_path = required_template_path
        self.available_template_paths = available_template_paths

    def __str__(self):
        return (f'Search Paths: {self.template_search_paths} \n'
                f'Cannot find template {self.required_template_path}. \n'
                f'Available Templates {self.available_template_paths}. \n')


class FailedToRenderTemplateException(Exception):
    def __init__(self,
                 template: str,
                 exec: Exception,
                 custom_global_keys: List[str],
                 ):
        self.template = template
        self.exec = exec
        self.custom_global_keys = custom_global_keys

    def __str__(self):
        return f'Cannot render template {self.template=}. \n' \
               f'Exception Message: {str(self.exec)} \n' \
               f'Available Globals {self.custom_global_keys}. \n'
