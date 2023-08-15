from typing import Any, Dict, List, Union

import jsonpath_ng

from api_compose.core.utils.exceptions import NoMatchesFoundForJsonPathException


def overlay_dict(overlayed_dict: Dict[str, Any], overlaying_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Overlay the `overlaying_dict` on top of the `overlayed_dict`, and include fields missing from the `overlayed_dict`
    """
    new_dict = overlayed_dict.copy()
    for key, value in overlaying_dict.items():
        if key in overlayed_dict:
            # If the key is present in both dictionaries and its value is a dictionary,
            # recursively call overlay_dict() on the value
            if isinstance(value, dict) and isinstance(new_dict[key], dict):
                new_dict[key] = overlay_dict(new_dict[key], value)
            else:
                new_dict[key] = value
        else:
            new_dict[key] = value

    return new_dict


def parse_json_with_jsonpath(deserialised_json: Union[Dict, List, None], json_path: str):
    if deserialised_json is None:
        raise NoMatchesFoundForJsonPathException(deserialised_json=deserialised_json, json_path=json_path)
    else:
        matches = [
            match.value for match in jsonpath_ng.parse(json_path).find(deserialised_json)
        ]
        if len(matches) == 0:
            raise NoMatchesFoundForJsonPathException(deserialised_json=deserialised_json, json_path=json_path)
        else:
            return matches[0]
