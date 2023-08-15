from typing import Dict, Type, Callable, Optional

# from api_compose.core.controllers.test_suite.base_test_suite import BaseTestSuite


#FIXME
# class TestItemRegistry:
#     registry: Dict[str, Type[BaseTestSuite]] = {}
#
#     @classmethod
#     def _validate_class(cls, test_suite_class: Type[BaseTestSuite]):
#         assert issubclass(test_suite_class, BaseTestSuite), f'Your Class {test_suite_class.__qualname__} must subclass BaseTestSuite!!!'
#
#     @classmethod
#     def _validate_no_same_key(cls, id: str):
#         assert id not in cls.registry.keys(), f'key {id} already registered!'
#
#     @classmethod
#     def set(cls, id: str) -> Callable:
#         def decorator(test_suite_class: Type[BaseTestSuite]):
#             cls._validate_class(test_suite_class)
#             cls._validate_no_same_key(id)
#             cls.registry[id] = test_suite_class
#             return test_suite_class
#         return decorator
#
#     @classmethod
#     def get(cls, id: str) -> Optional[Type[BaseTestSuite]]:
#         return cls.registry.get(id)
