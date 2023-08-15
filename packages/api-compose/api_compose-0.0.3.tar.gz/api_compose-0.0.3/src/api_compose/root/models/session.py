from typing import List

from pydantic import BaseModel as _BaseModel
from pydantic import Field

from api_compose.root.models.scenario_group import ScenarioGroupModel
from api_compose.services.common.models.base import BaseModel
from api_compose.services.persistence_service.models.config import BaseBackendConfigModel, SimpleBackendConfigModel
from api_compose.services.persistence_service.models.enum import BackendProcessorEnum
from api_compose.services.reporting_service.models.config import BaseReportRendererConfigModel, \
    HtmlReportRendererConfigModel
from api_compose.services.reporting_service.models.enum import ReportRendererProcessorEnum


class SessionModelConfig(_BaseModel):
    backend: BackendProcessorEnum = Field(
        BackendProcessorEnum.SimpleBackend,
        description='Backend Implementation to use',
    )
    backend_config: BaseBackendConfigModel = Field(
        SimpleBackendConfigModel(),
        description='Config required by Backend Implementation',
    )

    report_renderer: ReportRendererProcessorEnum = Field(
        ReportRendererProcessorEnum.HtmlReportRenderer,
        description='Report Renderer Implementation to use',
    )
    report_renderer_config: BaseReportRendererConfigModel = Field(
        HtmlReportRendererConfigModel(),
        description='Config required by Report Renderer Implementation',
    )


class SessionModel(BaseModel):
    scenario_groups: List[ScenarioGroupModel]

    config: SessionModelConfig = Field(
        SessionModelConfig(),
        description='Configuration for the Session',

    )

    # set to +ve integer if the actions between Scenario Groups need to wait
    intersession_sleep_seconds: int = 0
