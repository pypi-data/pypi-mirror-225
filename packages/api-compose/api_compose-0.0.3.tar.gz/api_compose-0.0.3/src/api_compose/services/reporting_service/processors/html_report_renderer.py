from pathlib import Path

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from api_compose.core.logging import get_logger
from api_compose.root import SessionModel
from api_compose.services.common.registry.processor_registry import ProcessorRegistry, ProcessorType, \
    PrceossorCategory
from api_compose.services.composition_service.models.actions.states import ActionState
from api_compose.services.reporting_service.processors.base_report_renderer import BaseReportRenderer
from api_compose.services.reporting_service.utils.networkx_graph import dump_actions_graph

HTML_FILE_TEMPLATE_FOLDER = Path(__file__).parent.joinpath("html_templates")

logger = get_logger(__name__)


@ProcessorRegistry.set(
    processor_type=ProcessorType.Builtin,
    processor_category=PrceossorCategory.Executor,
    models=[
        # No model required
    ]
)
class HtmlReportRenderer(BaseReportRenderer):
    """
    Implementation for rendering reports in HTML
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self):
        env = Environment(loader=FileSystemLoader(HTML_FILE_TEMPLATE_FOLDER))
        env.globals["set"] = set
        env.globals["vars"] = vars
        env.globals["enumerate"] = enumerate

        try:
            template = env.get_template(self.model_template_path)
        except TemplateNotFound as e:
            logger.error(f'Available templates: {env.list_templates(extensions="j2")}')
            raise ValueError(
                f'Template Not Found: {self.model_template_path}. Available Templates: {env.list_templates("j2")}')
        else:
            self.report = template.render(
                model=self.model,
                model_template_path=self.model_template_path,
                registered_entries=self.registry.registry,
                action_state=ActionState,
            )

    def write(self):
        # Dump Graph
        if type(self.model) == SessionModel:
            digraphs_mapping = {scenario.digraph_file_name: scenario.digraph for scenario_group in self.model.scenario_groups for scenario in scenario_group.scenarios}
            for digraph_file_name, digraph in digraphs_mapping.items():
                file_path = self.output_folder_path.joinpath(digraph_file_name)
                dump_actions_graph(digraph, file_path)

        # Write HTML
        self.path_to_output = self.output_folder_path.joinpath(
            f"{self.model.__class__.__name__}_report.html"
        )
        with open(self.path_to_output, "w") as f:
            logger.info(f'Dumping HTML report - {self.path_to_output=}')
            f.write(self.report)
