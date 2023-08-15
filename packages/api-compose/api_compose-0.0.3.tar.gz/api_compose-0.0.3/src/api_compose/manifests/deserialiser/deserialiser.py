__all__ = ['deserialise_manifest_to_model']

from pathlib import Path
from typing import Dict, Optional, Union, List

import yaml

from api_compose import GlobalSettings
from api_compose.core.jinja.core.context import BaseJinjaContext
from api_compose.core.jinja.core.engine import JinjaEngine, JinjaTemplateSyntax
from api_compose.core.logging import get_logger
from api_compose.manifests.deserialiser.exceptions import ManifestMissingModelNameException
from api_compose.manifests.events import DeserialisationEvent
from api_compose.services.common.models.base import BaseModel
from api_compose.services.common.registry.processor_registry import ProcessorRegistry

logger = get_logger(__name__)


def deserialise_manifest_to_model(
        manifest_file_path: str,
        manifests_folder_path: Path,
        context: Dict = None,
        json_dump=False,
) \
        -> Optional[Union[BaseModel, str]]:
    """
    Given relative path to a manifest file, deserialise it to a model based on the field `model_name` in the file.

    Parameters
    ----------
    manifest_file_path: Path to Manifest relative to MANIFESTS_FOLDER_PATH
    context: user-defined additional contexts
    json_dump: If True, dump model as json string. Else, return Model itself

    Returns
    -------

    """
    dict_ = deserialise_manifest_to_dict(
        manifest_file_path=manifest_file_path,
        manifests_folder_path=manifests_folder_path,
        context=context,
    )
    model = deserialise_dict_to_model(dict_)

    if model:
        if json_dump:
            return model.model_dump_json()
        else:
            return model
    else:
        raise ManifestMissingModelNameException(
            manifest_file_path=manifest_file_path,
            manifest_content=dict_,
            available_model_names=[
                name for name in
                ProcessorRegistry.get_model_names()]
        )


def deserialise_manifest_to_dict(
        manifest_file_path: str,
        manifests_folder_path: Path,
        context: Dict = None,
) -> Dict:
    if context is None:
        context = {}

    context = {**context, **GlobalSettings.get().env_vars}

    logger.debug(f'Deserialising {manifest_file_path=} relative to {manifests_folder_path=}. \n'
                 f'{context=}', DeserialisationEvent())
    relative_template_path = manifest_file_path

    id = Path(manifest_file_path).parts[-1].split('.')[0]

    # Read + Render
    str_, is_success, exec = (build_compile_time_jinja_engine(manifests_folder_path)
    .set_template_by_file_path(
        template_file_path=str(relative_template_path),
        can_strip=True
    ).render_to_str(
        jinja_context=BaseJinjaContext(**context)))

    if not is_success:
        raise exec

    dict_ = yaml.safe_load(str_)
    if dict_.get('id'):
        logger.warning(f'Id field is already set in the file. Will be overridden by the file name {id=}',
                       DeserialisationEvent())

    dict_['id'] = id
    return dict_


def deserialise_dict_to_model(
        dict_: Dict,
) -> Optional[BaseModel]:
    model_name = dict_.get('model_name')
    if model_name:
        return ProcessorRegistry.create_model_by_name(model_name, dict_)
    else:
        return None


def get_all_template_paths(manifest_folder_path: Path) -> List[str]:
    jinja_engine = build_compile_time_jinja_engine(manifests_folder_path=manifest_folder_path)
    return jinja_engine.get_available_templates()


def build_compile_time_jinja_engine(
        manifests_folder_path: Path,
) -> JinjaEngine:
    return JinjaEngine(
        globals={
            'ref': lambda path, **context: deserialise_manifest_to_model(
                path,
                manifests_folder_path=manifests_folder_path,
                context=context,
                json_dump=True
            ),
        },
        jinja_template_syntax=JinjaTemplateSyntax.SQUARE_BRACKETS,
        templates_search_paths=[
            manifests_folder_path,
        ],
    )
