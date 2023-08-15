from __future__ import annotations

from typing import List

import jinja2

from api_compose.services.composition_service.exceptions import NoMatchesFoundWithFilter
from api_compose.services.composition_service.models.calculated_field.calculated_field import CalculatedField


@jinja2.pass_context
def get_calculated_field(context: jinja2.runtime.Context, calculated_field_name: str):
    calculated_fields: List[CalculatedField] = dict(context).get('calculated_fields', [])
    for calculated_field in calculated_fields:
        if calculated_field.name == calculated_field_name:
            return calculated_field.value

    raise NoMatchesFoundWithFilter(filter={'calculated_field_name': calculated_field_name}, collection=calculated_fields)
