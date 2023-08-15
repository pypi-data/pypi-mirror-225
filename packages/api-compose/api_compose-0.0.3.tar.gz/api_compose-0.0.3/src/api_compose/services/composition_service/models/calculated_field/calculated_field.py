from __future__ import annotations

import re
from enum import Enum
from typing import Callable, Any, List, Set

from pydantic import BaseModel as _BaseModel, Field

from api_compose.core.logging import get_logger
from api_compose.core.utils.linear_graph import get_linear_execution_order

logger = get_logger(__name__)


class BuiltinCalculatedFieldNameEnum(Enum):
    """
    Enum of Builtin Calculated Field Names used in the
    """
    URL = 'url'
    HTTP_METHOD = 'http_method'
    HTTP_HEADERS = 'http_headers'
    HTTP_PARAMS = 'http_params'
    HTTP_JSON_BODY = 'http_json_body'
    HTTP_XML_BODY = 'http_xml_body'


class CalculatedField(_BaseModel):
    func: Callable[[...], Any]
    name: str = Field(
        'Name of the Field',
    )

    required: bool = Field(
        description='Whether the field must be rendered. When True, it is always rendered. When False, it is rendered only if it is depended on by other fields.')
    depends_on: List[str] = Field(
        'A list of fields which the current field depends on. Used to build rendering order of the fields.'
    )

    # Value cannot be dynamic as it should depend on the value when function is called
    value: Any = None

    @property
    def qualname(self) -> str:
        return self.func.__qualname__

    @property
    def class_name(self):
        return self.qualname.split('.')[0]

    def __eq__(self, other):
        if isinstance(other, self.__class__) and other.name == self.name:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.name)


def get_ordered_calculated_fields(unordered_calculated_fields: List[CalculatedField],
                                  ) -> List[CalculatedField]:
    dependencies = {x.name: x.depends_on for x in unordered_calculated_fields}

    ordered_names = get_linear_execution_order(dependencies)
    logger.info(f"Calculated Fields Execution Order - {ordered_names}")
    ordered_calculated_fields = []

    for name in ordered_names:
        for calculated_field in unordered_calculated_fields:
            if calculated_field.name == name:
                ordered_calculated_fields.append(calculated_field)
                continue

    return ordered_calculated_fields


def get_filtered_calculated_fields_by_required(all_calculated_fields: List[CalculatedField]) -> List[
    CalculatedField]:
    # required =
    # i. calculated fields with required = True
    # ii. calculated fields with required = False, but which (i) depends on
    required: Set[str] = set()

    for calc_field in all_calculated_fields:
        if calc_field.required:
            required.add(calc_field.name)
            required.update(calc_field.depends_on)

    return [calc_field for calc_field in all_calculated_fields if calc_field.name in required]


def get_calculated_fields_in_string(
        string: str,
) -> List[str]:
    pattern = r"calculated_field\(\s*'(.*?)'\s*\)"
    matches = re.findall(pattern, string)
    return matches


