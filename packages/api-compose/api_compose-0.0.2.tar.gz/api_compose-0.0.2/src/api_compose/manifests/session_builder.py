__all__ = ['build_session_from_model']

from pathlib import Path
from typing import List, Dict, Set

from api_compose import get_logger
from api_compose.manifests.deserialiser.deserialiser import get_all_template_paths, deserialise_manifest_to_dict, \
    deserialise_manifest_to_model
from api_compose.manifests.events import DeserialisationEvent
from api_compose.root import SessionModel
from api_compose.root.models.scenario import ScenarioModel
from api_compose.root.models.scenario_group import ScenarioGroupModel
from api_compose.services.common.models.base import BaseModel
from api_compose.services.composition_service.models.actions.actions import BaseActionModel

logger = get_logger(__name__)


def build_session_from_model(model: BaseModel,
                             **session_ctx: Dict,
                             ) -> SessionModel:
    """
    Build SessionModel from any given BaseModel
    Parameters
    ----------
    model
    session_ctx: Parameters to SessionModel

    Returns
    -------

    """
    id = session_ctx.get('id', 'default_id')
    description = session_ctx.get('description', 'default description')
    if isinstance(model, BaseActionModel):
        scenario_model = ScenarioModel(id=id, description=description, actions=[model])
        scenario_group_model = ScenarioGroupModel(id=id, description=description,
                                                  scenarios=[scenario_model])
        session_model = SessionModel(id=id, description=description,
                                     scenario_groups=[scenario_group_model])
    elif isinstance(model, ScenarioModel):
        scenario_group_model = ScenarioGroupModel(id=id, description=description, scenarios=[model])
        session_model = SessionModel(id=id, description=description,
                                     scenario_groups=[scenario_group_model])
    elif isinstance(model, ScenarioGroupModel):
        session_model = SessionModel(id=id, description=description, scenario_groups=[model])
    else:
        raise ValueError(f'Unhandled model type {type(model)}')

    return session_model


def build_session_from_tags(target_tags: Set[str],
                            manifests_folder_path: Path,
                            **session_ctx: Dict,
                            ) -> SessionModel:
    """
    Given all ScenarioGroups, filter for those with certain tags and put them in a session model

    Parameters
    ----------
    target_tags
    session_ctx

    Returns
    -------

    """
    id = session_ctx.get('id', 'default_id')
    description = session_ctx.get('description', 'default description')

    target_scenario_groups: List[ScenarioGroupModel] = []

    # Search for target scenario groups
    for template_path in get_all_template_paths(manifests_folder_path):
        dict_ = deserialise_manifest_to_dict(
            template_path,
            manifests_folder_path=manifests_folder_path,
            context=None)

        model_name = dict_.get('model_name')
        tags: Set = set(dict_.get('tags', [])) # Set set() as default

        if model_name and model_name == 'ScenarioGroupModel' and target_tags <= tags:
            scenario_group_model: ScenarioGroupModel = deserialise_manifest_to_model( # noqa - already known it must be ScenarioGroupModel
                template_path,
                manifests_folder_path=manifests_folder_path,
                context=None,
                json_dump=False,
            )
            target_scenario_groups.append(scenario_group_model)

    if len(target_scenario_groups) == 0:
        logger.warning(f'No Session Groups Found with {target_tags=}', DeserialisationEvent())

    return SessionModel(id=id, description=description, scenario_groups=target_scenario_groups)



