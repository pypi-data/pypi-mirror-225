import time
from typing import Dict

from api_compose.core.jinja.core.engine import JinjaEngine
from api_compose.root.models.scenario import ScenarioModel
from api_compose.services.assertion_service.processors.assertion.base_assertion import \
    BaseAssertion
from api_compose.services.common.processors.base import BaseProcessor
from api_compose.services.common.registry.processor_registry import ProcessorRegistry, ProcessorType, PrceossorCategory
from api_compose.services.composition_service.jinja.context import ActionJinjaContext
from api_compose.services.composition_service.processors.executors.base_executor import BaseExecutor
from api_compose.services.composition_service.processors.schedulers.scheduler import ActionScheduler
from api_compose.services.composition_service.processors.schedulers.utils import convert_edges_from_str_to_model
from api_compose.services.persistence_service.processors.base_backend import BaseBackend


@ProcessorRegistry.set(
    processor_type=ProcessorType.Builtin,
    processor_category=PrceossorCategory.Backend,
    models=[
        ScenarioModel(
            id='example_scenario',
            description='example scenario',
            actions=[],
        )
    ]
)
class ScenarioProcessor(BaseProcessor):

    def __init__(self,
                 scenario_model: ScenarioModel,
                 backend: BaseBackend,
                 jinja_engine: JinjaEngine,
                 is_debug: bool,
                 ):
        super().__init__()
        self.scenario_model = scenario_model
        self.jinja_engine = jinja_engine
        self.is_debug = is_debug
        self.backend = backend

        self.executor: BaseExecutor = ProcessorRegistry.create_processor_by_name(
            class_name=scenario_model.config.executor.value,
            config=dict(scenario_model.config.executor_config),
        )


        self.action_scheduler: ActionScheduler = ActionScheduler(
            backend=backend,
            jinja_engine=jinja_engine,
            executor=self.executor,
            is_debug=self.is_debug,

            #Settings
            max_concurrent_node_execution_num=scenario_model.config.scheduler_config.max_concurrent_node_execution_num,
            rescan_all_nodes_in_seconds=scenario_model.config.scheduler_config.rescan_all_nodes_in_seconds,
            nodes=scenario_model.actions,
            edges=convert_edges_from_str_to_model(
                is_schedule_linear=scenario_model.config.scheduler_config.is_schedule_linear,
                custom_schedule_order=scenario_model.config.scheduler_config.custom_schedule_order,
                action_models=scenario_model.actions,
            )
        )

        self.scenario_model.digraph = self.action_scheduler.digraph


    def run(self):
        # Run Actions
        self.scenario_model.start_time = time.time()
        self.action_scheduler.run()
        self.scenario_model.end_time = time.time()

        # Get ActionJinjaContext
        jinja_context = ActionJinjaContext.build(backend=self.backend, action_model=self.scenario_model.actions[0])

        # Run Test Items
        for assertion_model in self.scenario_model.assertions:
            assertion: BaseAssertion = ProcessorRegistry.create_processor_by_name(
                class_name=assertion_model.class_name,
                config={**dict(assertion=assertion_model,
                               jinja_engine=self.jinja_engine,
                               jinja_context=jinja_context,
                               ),
                        **dict(assertion_model.config),
                        }
            )

            assertion.run()

        # Save results
        self.backend.add(self.scenario_model)
