__all__ = ["Runner"]

from api_compose.root.processors.scenario import ScenarioProcessor
from api_compose.root.processors.scenario_group import ScenarioGroupProcessor

"""
Composition Root
"""
import datetime
import time

from api_compose.core.logging import get_logger
from api_compose.core.utils.settings import GlobalSettings
from api_compose.core.jinja.core.engine import JinjaEngine

from api_compose.services.reporting_service.processors.base_report_renderer import BaseReportRenderer
from api_compose.services.persistence_service.processors.base_backend import BaseBackend
from api_compose.root.models.session import SessionModel
from api_compose.root.models.scenario import ScenarioModel
from api_compose.root.models.scenario_group import ScenarioGroupModel
from api_compose.services.common.registry.processor_registry import ProcessorRegistry

logger = get_logger(name=__name__)


class Runner:

    def __init__(self,
                 session_model: SessionModel,
                 jinja_engine: JinjaEngine,
                 ):
        self.session_model = session_model
        self.session_model.set_parent_ids()

        self.is_debug = GlobalSettings.get().IS_DEBUG
        self.session_start_timestamp = datetime.datetime.utcnow()

        self.backend: BaseBackend = ProcessorRegistry.create_processor_by_name(
            class_name=session_model.config.backend.value,
            config=dict(session_model.config.backend_config),
        )
        self.jinja_engine: JinjaEngine = jinja_engine

    def _execute_scenario_group(self, scenario_group_model: ScenarioGroupModel):
        # Parallel Execution of Scenario Groups??
        print(scenario_group_model.fqn)

        scenario_group_processor = ScenarioGroupProcessor(
            scenario_group_model,
            backend=self.backend,
            jinja_engine=self.jinja_engine,
            is_debug=self.is_debug,
        )

        scenario_group_processor.run()

    def _execute_report_renderer(self):
        # Generate report(s)
        report_renderer: BaseReportRenderer = ProcessorRegistry.create_processor_by_name(
            class_name=self.session_model.config.report_renderer.value,
            config=dict(
                model=self.session_model,
                model_template_path='session.html.j2',
                output_folder=self.session_model.config.report_renderer_config.report_folder,
                timestamp=self.session_start_timestamp,
                registry=ProcessorRegistry(),
            )
        )
        report_renderer.run()

    def run(self):
        for idx, scenario_group_model in enumerate(self.session_model.scenario_groups):
            self._execute_scenario_group(scenario_group_model)
            if idx != len(self.session_model.scenario_groups) - 1:
                # don't sleep for last group at the end
                logger.debug(
                    f"Scenario Group Model {scenario_group_model.id} done..... going to sleep for {self.session_model.intersession_sleep_seconds}"
                )
                time.sleep(self.session_model.intersession_sleep_seconds)

        self._execute_report_renderer()
