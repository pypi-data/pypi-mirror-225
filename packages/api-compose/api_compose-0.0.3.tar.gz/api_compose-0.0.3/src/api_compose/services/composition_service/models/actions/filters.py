__all__ = [
    'get_action_output_body',
    'get_action_output_headers',
    'get_action_input_body',
    'get_action_output_status_code'
]

from typing import List

import jinja2

from api_compose.core.utils.transformers import parse_json_with_jsonpath
from api_compose.services.composition_service.exceptions import NoMatchesFoundWithFilter
from api_compose.services.composition_service.models.actions.actions import BaseActionModel


@jinja2.pass_context
def get_action_input_body(context: jinja2.runtime.Context, execution_id: str, json_path: str):
    """


    Parameters
    ----------
    execution_id: execution id of the target action
    json_path

    Returns
    -------

    """
    return _get_action_attr(execution_id, dict(context).get('action_models'), ['input', 'body'], json_path)


@jinja2.pass_context
def get_action_output_body(context: jinja2.runtime.Context, execution_id: str, json_path: str):
    """


    Parameters
    ----------
    execution_id: execution id of the target action
    json_path

    Returns
    -------

    """
    return _get_action_attr(execution_id, dict(context).get('action_models'), ['output', 'body'], json_path)


@jinja2.pass_context
def get_action_output_headers(context: jinja2.runtime.Context, execution_id: str, json_path: str):
    """
    Parameters
    ----------
    execution_id: id of the target action
    actions: a list of BaseActionComponentModels
    action_output_attr: Attribute of the OutputModel
    json_path

    Returns
    -------

    """
    return _get_action_attr(execution_id, dict(context).get('action_models'), ['output', 'headers'], json_path)


@jinja2.pass_context
def get_action_output_status_code(context: jinja2.runtime.Context, execution_id: str):
    """
    Parameters
    ----------
    execution_id: execution id of the target action

    Returns
    -------

    """
    return _get_action_attr(execution_id, dict(context).get('action_models'), ['output', 'status_code'])


def _get_action_attr(execution_id: str,
                     action_models: List[BaseActionModel],
                     action_attrs: List[str],
                     json_path: str = ""):
    """

    Parameters
    ----------
    execution_id: execution id of the target action
    action_models: a list of BaseActionComponentModels
    action_output_attr: Attribute of the OutputModel
    json_path

    Returns
    -------

    """
    for action in action_models:
        if action.execution_id == execution_id:
            _var = action
            for action_attr in action_attrs:
                _var = getattr(_var, action_attr)

            if json_path:
                return parse_json_with_jsonpath(_var, json_path)  # noqa - _var can be anything with getattr()
            else:
                return _var

    # Nothing found
    raise NoMatchesFoundWithFilter(filter={'execution_id': execution_id}, collection=action_models)

