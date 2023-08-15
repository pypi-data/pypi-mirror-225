from typing import List, Set

from pydantic import Field

from api_compose.services.common.models.base import BaseModel
from api_compose.root.models.scenario import ScenarioModel


class ScenarioGroupModel(BaseModel):
    scenarios: List[ScenarioModel]
    tags: Set[str] = Field(
        set(),
        description='Tags which identify the Scenario Group'
    )


    @property
    def is_success(self) -> bool:
        return all([scenario.is_success for scenario in self.scenarios])

    @property
    def elapsed_time(self) -> float:
        return sum(scenario.elapsed_time for scenario in self.scenarios)

