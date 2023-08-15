__all__ = ['JinjaAssertion']

from typing import Optional

from api_compose.core.jinja.core.context import BaseJinjaContext
from api_compose.core.jinja.core.engine import JinjaEngine
from api_compose.core.logging import get_logger
from api_compose.services.assertion_service.processors.assertion.base_assertion import \
    BaseAssertion
from api_compose.services.assertion_service.models.assertion import JinjaAssertionModel
from api_compose.services.assertion_service.models.configs import JinjaAssertionConfigModel
from api_compose.services.common.registry.processor_registry import ProcessorType, ProcessorRegistry, \
    PrceossorCategory

logger = get_logger(__name__)


@ProcessorRegistry.set(
    processor_type=ProcessorType.Builtin,
    processor_category=PrceossorCategory.Assertion,
    models=[
        JinjaAssertionModel(
            id='example_jinja_assertion_controller',
            config=JinjaAssertionConfigModel(
                template="{{ True is True }}",
                template_file_path='',
            ),
        ),
    ]
)
class JinjaAssertion(BaseAssertion):

    def __init__(self,
                 template: Optional[str],
                 template_file_path: Optional[str],
                 jinja_context: BaseJinjaContext,
                 jinja_engine: JinjaEngine,
                 *args,
                 **kwargs
                 ):
        super().__init__(*args, **kwargs)
        self.template = template
        self.template_file_path = template_file_path
        self.jinja_context = jinja_context
        self.jinja_engine = jinja_engine

        self._validate_template()

    def _validate_template(self):
        if type(self.template) == str and len(self.template) > 0:
            pass
        else:
            logger.debug('Template string not set. Looking for template...')
            # Search for template
            self.template = self.jinja_engine.set_template_by_file_path(self.template_file_path).current_source

    def execute(self) -> bool:
        rendered_str, is_success, exec = self.jinja_engine.set_template_by_string(self.template).render_to_str(
            self.jinja_context)

        if is_success and rendered_str.strip().lower() == 'true':
            return True
        else:
            logger.info(f'{self.template=} {is_success=} {rendered_str=} {exec=}')
            return False
