"""
config subcommand
"""
from pathlib import Path
from typing import Dict, Union, Any

import typer
import yaml

from api_compose.core.utils.settings import GlobalSettingsModel, GlobalSettings

app = typer.Typer(
    help="Configure your programme",
    no_args_is_help=True
)


def get_default_settings() -> Dict:
    def convert_path(path: Union[Path, Any]):
        if isinstance(path, Path):
            return str(path)
        else:
            return path

    dict_ = {}

    default_vals = {
        key: getattr(value, 'default') for key, value in
        GlobalSettingsModel.model_fields.items()
    }

    for key, val in default_vals.items():
        if type(val) == list:
            val = [convert_path(elem) for elem in val]
            dict_[key] = val

        if type(val) == dict:
            val = {ky: convert_path(vl) for ky, vl in val.items()}

        dict_[key] = convert_path(val)

    return dict_


@app.command(help="Initialise Configuration File")
def init() -> None:
    """
    generate a config file

    :return:
    """
    config_file = Path('config.yaml')
    if config_file.exists():
        typer.echo(f'Config File {config_file.absolute()} already exists! Aborted')
    else:
        with open(config_file, 'w') as f:
            yaml.dump(get_default_settings(), f)
        typer.echo(f'Config File {config_file.absolute()} is created')
@app.command(help="Show configurations")
def ls() -> None:
    """

    :return:
    """
    typer.secho("\n".join([f"{key}={value}" for key, value in GlobalSettings.get().__dict__.items()]))
