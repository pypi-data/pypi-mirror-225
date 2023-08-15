from api_compose.core.jinja.core.engine import JinjaEngine, JinjaTemplateSyntax
from api_compose.core.logging import get_logger
from api_compose.root.events import SessionEvent
from api_compose.root.models.session import SessionModel
from api_compose.root.models.session import SessionModel
from api_compose.root.runner import Runner
from api_compose.services.composition_service.models.actions.filters import get_action_input_body, \
    get_action_output_body, get_action_output_headers, get_action_output_status_code
from api_compose.services.composition_service.models.calculated_field.filters import get_calculated_field

logger = get_logger(__name__)


def run_session_model(session_model: SessionModel) -> SessionModel:
    logger.info(f'Running Session {session_model.id=}', SessionEvent())
    jinja_engine: JinjaEngine = build_runtime_jinja_engine()
    runner = Runner(session_model, jinja_engine)
    runner.run()
    return runner.session_model


def build_runtime_jinja_engine(
) -> JinjaEngine:
    return JinjaEngine(
        globals={
            # For Model Jinja Field -> Model Rendered FIeld
            'calculated_field': get_calculated_field,
            'input_body': get_action_input_body,
            'output_body': get_action_output_body,
            'output_headers': get_action_output_headers,
            'output_status_code': get_action_output_status_code,
        },
        jinja_template_syntax=JinjaTemplateSyntax.CURLY_BRACES,
    )
