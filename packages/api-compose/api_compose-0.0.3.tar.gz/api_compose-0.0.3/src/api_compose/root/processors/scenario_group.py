from api_compose.core.jinja.core.engine import JinjaEngine
from api_compose.root.models.scenario_group import ScenarioGroupModel
from api_compose.root.processors.scenario import ScenarioProcessor
from api_compose.services.common.processors.base import BaseProcessor
from api_compose.services.common.registry.processor_registry import ProcessorRegistry, ProcessorType, PrceossorCategory
from api_compose.services.persistence_service.processors.base_backend import BaseBackend


@ProcessorRegistry.set(
    processor_type=ProcessorType.Builtin,
    processor_category=PrceossorCategory.Backend,
    models=[
        ScenarioGroupModel(
            id='example_scenario_group',
            description='example scenario_group',
            scenarios=[],
        )
    ]
)
class ScenarioGroupProcessor(BaseProcessor):

    def __init__(self,
                 scenario_group_model: ScenarioGroupModel,
                 backend: BaseBackend,
                 jinja_engine: JinjaEngine,
                 is_debug: bool,
                 ):
        super().__init__()
        self.scenario_group_model = scenario_group_model
        self.jinja_engine = jinja_engine
        self.is_debug = is_debug
        self.backend = backend

    def run(self):
        for idx, scenario_model in enumerate(self.scenario_group_model.scenarios):
            scenario_controller = ScenarioProcessor(
                scenario_model=scenario_model,
                backend=self.backend,
                jinja_engine=self.jinja_engine,
                is_debug=self.is_debug
            )

            scenario_controller.run()

        self.backend.add(self.scenario_group_model)
