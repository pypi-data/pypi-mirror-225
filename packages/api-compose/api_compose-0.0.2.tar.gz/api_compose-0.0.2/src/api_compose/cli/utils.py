from typing import Optional, List, Dict

from api_compose import get_logger
from api_compose.cli.events import CliEvent
from api_compose.cli.validators import validate_context_kv_pair

logger = get_logger(__name__)


def parse_context(context: Optional[List[str]]) -> Dict[str, str]:
    dict_ = {}
    if context and type(context) == list:
        for val in context:
            key, val = validate_context_kv_pair(val)
            dict_[key] = val
        logger.info('Provided CLI context \n' f'{dict_=}', CliEvent())
    else:
        logger.warning('Ignoring provided context as it is not a list a strings \n' f'{context=}', CliEvent())

    return dict_
