__all__ = ['PythonAssertion']

from api_compose.services.assertion_service.processors.assertion.base_assertion import \
    BaseAssertion
from api_compose.services.assertion_service.models.assertion import PythonAssertionModel
from api_compose.services.assertion_service.models.configs import PythonAssertionConfigModel
from api_compose.services.common.registry.processor_registry import ProcessorType, ProcessorRegistry, \
    PrceossorCategory


@ProcessorRegistry.set(
    processor_type=ProcessorType.Builtin,
    processor_category=PrceossorCategory.Assertion,
    models=[
        PythonAssertionModel(
            id='example_python_assertion_controller',
            config=PythonAssertionConfigModel(
                funcname='',
            )
        ),

    ]
)
class PythonAssertion(BaseAssertion):

    def __init__(self,
                 funcname: str,
                 *args,
                 **kwargs
                 ):
        super().__init__(*args, **kwargs)
        self.funcname = funcname

    def execute(self) -> bool:
        return True
