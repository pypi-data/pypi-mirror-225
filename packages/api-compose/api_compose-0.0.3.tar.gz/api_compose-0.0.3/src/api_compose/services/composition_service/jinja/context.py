from __future__ import annotations

from typing import List

from pydantic import Field, Extra

from api_compose import BaseBackend
from api_compose.core.jinja.core.context import BaseJinjaContext
from api_compose.services.common.models.base import BaseModel
from api_compose.services.composition_service.models.actions.actions import BaseActionModel
from api_compose.services.composition_service.models.calculated_field.calculated_field import CalculatedField


class ActionJinjaContext(BaseJinjaContext, extra='forbid'):
    """
    Jinja Context for Core rendering.

    Scope is per Action

    Used to render templated fields in actions. e.g. {{ output_body() }}
    """

    # Dynamic - Scenario Scoped
    action_models: List[BaseActionModel] = Field([], description='List of Action Models in their ending states')


    # Dynamic - Action Scoped
    calculated_fields: List[CalculatedField] = Field([], description='calculated fields in each instance of subclassed BaseAdapter')

    @classmethod
    def build(cls, backend: BaseBackend, action_model: BaseActionModel) -> ActionJinjaContext:
        c = ActionJinjaContext()

        # Get actions
        base_models: List[BaseModel] = backend.get_latest_siblings(action_model)
        c.action_models = [model for model in base_models if isinstance(model, BaseActionModel)]

        # Set empty calculated fields
        c.calculated_fields = []
        return c
