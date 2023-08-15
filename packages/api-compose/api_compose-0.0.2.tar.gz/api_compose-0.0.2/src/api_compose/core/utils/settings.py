"""
Programme's Global Settings.

Cannot use logger. That would cause Cyclical Dependency OR double or triple logging of the same message
"""

__all__ = ['GlobalSettings', 'GlobalSettingsModel']

import logging
import os
from pathlib import Path
from typing import List, Optional, Dict, Type, Union, Set

import yaml
from dotenv import dotenv_values
from pydantic import field_validator, BaseModel

from api_compose.core.events.base import EventType
from api_compose.core.events.read_config import ReadConfigEvent


def parse_string_to_path(value: Union[str]) -> Path:
    if type(value) == str:
        return Path(value)
    else:
        raise TypeError(f'value={value} is not a string nor a list')


def parse_string_to_list_of_strings(value: Union[str, List[str]]) -> List[str]:
    if type(value) == str:
        return [path_str for path_str in value.split(',')]
    elif type(value) == list:
        return value
    else:
        raise TypeError(f'value={value} is neither a string nor a list')


def parse_string_to_list_of_paths(value: Union[str, List[str]]) -> List[Path]:
    if type(value) == str:
        return [Path(path_str) for path_str in value.split(',')]
    elif type(value) == list:
        return [Path(stuff) for stuff in value]
    else:
        raise TypeError(f'value={value} is neither a string nor a list')


class GlobalSettingsModel(BaseModel):
    LOGGER_LEVEL: int = logging.ERROR
    LOG_FILE_PATH: Optional[Path] = Path.cwd().joinpath('log.jsonl')
    LOG_EVENT_FILTERS: List[EventType] = []

    ENV_VAR_FILE_PATH: Optional[Path] = None
    IS_DEBUG: bool = False

    MANIFESTS_FOLDER_PATH: Path = Path.cwd().joinpath('manifests')
    CALCULATED_FIELDS_FOLDER_PATH: Path = Path.cwd().joinpath('calculated_fields')
    TAGS: Set[str] = set()

    @field_validator("LOGGER_LEVEL", mode="before")
    @classmethod
    def parse_logger_level(cls, value: Optional[str]):
        if value:
            return int(value)
        else:
            # Use default
            return logging.ERROR

    @field_validator("IS_DEBUG", mode="before")
    @classmethod
    def parse_is_debug(cls, value: Optional[str]):
        if value and type(value) == str and value.strip().upper() in ('TRUE', 'T', 'Y', 'YES'):
            return True
        else:
            # Use default
            return False

    @field_validator("LOG_FILE_PATH", mode="before")
    @classmethod
    def parse_log_file_path(cls, value: Optional[str]):
        if value:
            return Path.cwd().joinpath(value) if type(value) == str and len(value) > 0 else Path.cwd().joinpath('log.jsonl')
        else:
            # empty string LOG_FILE_PATH means no logs
            return None

    @field_validator("TAGS", mode="before")
    @classmethod
    def parse_tags(cls, value: List[str]):
        if type(value) == list:
            return set(value)
        else:
            print(f'ERROR - Cannot create tags {value=}')
            return set()

    @field_validator("MANIFESTS_FOLDER_PATH", mode="before")
    @classmethod
    def parse_manifests_folder_path(cls, value: Optional[str]):
        return Path.cwd().joinpath(value) if type(value) == str and len(value) > 0 else Path.cwd().joinpath('manifests')

    @field_validator("CALCULATED_FIELDS_FOLDER_PATH", mode="before")
    @classmethod
    def parse_calculated_fields_folder_path(cls, value: Optional[str]):
        return Path.cwd().joinpath(value) if type(value) == str and len(value) > 0 else Path.cwd().joinpath('manifests')

    @property
    def env_vars(self) -> Dict:
        """
        Read value
        Returns
        -------
        """
        if self.ENV_VAR_FILE_PATH is None:
            return {}
        else:
            kvs: Dict = dotenv_values(self.ENV_VAR_FILE_PATH, verbose=True)
            return kvs


def read_config_from_file(config_file_path: Path) -> Dict:
    dict_ = {}
    if config_file_path.exists():
        with open(config_file_path, 'r') as f:
            dict_: Optional[Dict] = yaml.load(f, Loader=yaml.FullLoader)

    # File might be empty
    return dict_ or {}


def read_config_from_env(model_clazz: Type[BaseModel]) -> Dict:
    """
    Read config env based on field from pydantic root

    Parameters
    ----------
    model_clazz

    Returns
    -------

    """
    return dict(os.environ)


class GlobalSettings():
    _GLOBAL_SETTINGS: Optional[GlobalSettingsModel] = None

    @classmethod
    def set(cls, config_file_path: Optional[Path] = Path('config.yaml')):
        config_from_file = read_config_from_file(config_file_path=config_file_path)
        config_from_env = dict(os.environ)

        config = {}

        for key in GlobalSettingsModel.model_fields.keys():
            val_from_file = config_from_file.get(key)
            val_from_env = config_from_env.get(key)

            if val_from_env:
                config[key] = val_from_env
            elif val_from_file:
                config[key] = val_from_file
            else:
                pass


        cls._GLOBAL_SETTINGS = GlobalSettingsModel(**config)

    @classmethod
    def get(cls) -> GlobalSettingsModel:
        if cls._GLOBAL_SETTINGS is None:
            raise ValueError('Global Settings Model not yet created!')
        return cls._GLOBAL_SETTINGS
