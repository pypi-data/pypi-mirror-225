from copy import deepcopy
from typing import Callable, List, Iterator, Dict, Optional

from api_compose.core.logging import get_logger
from api_compose.services.composition_service.events.calculated_field import CalculatedFieldRenderingEvent, \
    CalculatedFieldData, CalculatedFieldRegistrationEvent
from api_compose.services.composition_service.models.calculated_field.calculated_field import CalculatedField, \
    get_ordered_calculated_fields, get_filtered_calculated_fields_by_required

logger = get_logger(__name__)


class CalculatedFieldRegistry:
    """
    - Use Decorator to Register Default Calculated Fields
    - When instantiated, made a deep copy of each calculated field
    - Within each instance of registry, render each field as per need only when render() is called.

    Lazy evaluation of Calculated Field.
    Only evaluate when `render()` is called
    """

    _registry: List[CalculatedField] = []

    @classmethod
    def set(cls, name: str, required: bool = False, depends_on: Optional[List[str]] = None):
        # Set Calculate Fields as templates
        if depends_on is None:
            depends_on = []

        logger.info("Registered Calculated Field %s" % (name), CalculatedFieldRegistrationEvent())

        def decorator(func: Callable):
            cls._registry.append(
                CalculatedField(
                    name=name,
                    required=required,
                    depends_on=depends_on,
                    func=func
                )
            )
            return func

        return decorator

    def set_attrs_by_name(self, name, depends_on: List[str], required: bool = False):
        for calc_field in self.calculated_fields:
            if calc_field.name == name:
                calc_field.depends_on = depends_on
                calc_field.required = required
                return

        raise KeyError(
            f'Calculated Field {name=} not found!. Available names are {[calc_field.name for calc_field in self.calculated_fields]}')

    def __init__(self):
        self.calculated_fields = [deepcopy(calc_field) for calc_field in self.__class__._registry]

    def get_value_by_name(self, name):
        for calc_field in self.calculated_fields:
            if calc_field.name == name:
                return calc_field.value

        raise KeyError(f'Calculated Field {name=} not found!')

    def render(self,
               adapter_instance,
               execution_id: str,
               **ctx: Dict,
               ) -> Iterator[CalculatedField]:
        calculated_fields = self.calculated_fields

        if calculated_fields is None:
            return
        else:
            new_ctx = deepcopy(ctx)
            # render each field one by one
            calculated_fields = get_filtered_calculated_fields_by_required(calculated_fields)
            calculated_fields = get_ordered_calculated_fields(calculated_fields)

            for calculated_field in calculated_fields:
                # Calculate field and pass back to the next func
                name = calculated_field.name
                value = calculated_field.func(
                    **dict(
                        self=adapter_instance,
                        **new_ctx
                    )
                )
                calculated_field.value = value

                if new_ctx.get(name):
                    raise KeyError(
                        f'Cannot add existing key {name=} to ctx for CalculatedField! Existing Keys = {[k for k in ctx.keys()]}')
                else:
                    new_ctx[name] = value

                logger.info(f"Action {execution_id=} - Rendered Calculated Calculated Field %s to %s" % (name, value),
                            CalculatedFieldRenderingEvent(
                                data=CalculatedFieldData(name=name, value=value, depends_on=calculated_field.depends_on,
                                                         required=calculated_field.required)))

                yield calculated_field
