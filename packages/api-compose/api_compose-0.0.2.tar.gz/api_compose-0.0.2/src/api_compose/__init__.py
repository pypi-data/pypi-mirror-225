__all__ = []

import sys
from pathlib import Path

from api_compose.core.utils.settings import GlobalSettings, GlobalSettingsModel
from api_compose.services.composition_service.events.calculated_field import CalculatedFieldRegistrationEvent

# read into global settings
GlobalSettings.set()

# Get logger after settings are set
import importlib
# Help with import from CLI
sys.path.append(str(Path.cwd()))
from api_compose.core.logging import get_logger

logger = get_logger(__name__)

# Display
logger.debug('Display Configurations: \n' + '\n'.join([f"{idx}: {key}={value}" for idx, (key, value) in enumerate(GlobalSettings.get().__dict__.items())]))

calculated_field_folder_path = GlobalSettings.get().CALCULATED_FIELDS_FOLDER_PATH
if calculated_field_folder_path.exists():
    # Extract the module name from the file path
    module_name = calculated_field_folder_path.stem
    # Import the module dynamically
    module = importlib.import_module(module_name)
else:
    logger.debug(f"Failed to Import Custom Calculated Fields. Folder {calculated_field_folder_path} does not exist", CalculatedFieldRegistrationEvent())

# Import for side effect (Controller Registration)
from api_compose.services.persistence_service.processors.base_backend import \
    BaseBackend  # noqa - register backend to Registry
from api_compose.services.persistence_service.processors.simple_backend import \
    SimpleBackend  # noqa - register backend to Registry

from api_compose.services.composition_service.processors.actions import Action  # noqa - register action to Registry
from api_compose.services.composition_service.processors.adapters.http_adapter.json_http_adapter import \
    JsonHttpAdapter  # noqa - register adapter to Registry
from api_compose.services.composition_service.processors.adapters.http_adapter.xml_http_adapter import \
    XmlHttpAdapter  # noqa - register adapter to Registry
from api_compose.services.composition_service.processors.adapters.websocket_adapter import \
    JsonRpcWebSocketAdapter  # noqa - register adapter to Registry
from api_compose.services.composition_service.processors.executors.local_executor import \
    LocalExecutor  # noqa - register executors to Registry

from api_compose.services.reporting_service.processors.html_report_renderer import \
    HtmlReportRenderer  # noqa - register report_renderers to Registry

from api_compose.services.assertion_service.processors.assertion.jinja_assertion import \
    JinjaAssertion  # noqa - register test executors to Registry
from api_compose.services.assertion_service.processors.assertion.python_assertion import \
    PythonAssertion  # noqa - register test executors to Registry
