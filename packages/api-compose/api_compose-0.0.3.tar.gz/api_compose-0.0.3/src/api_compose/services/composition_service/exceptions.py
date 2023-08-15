from typing import List, Type, Any, Dict
from pathlib import Path
import os


class TargetClassNotFoundError(Exception):
    def __init__(self, target_class_name: str, directories: List[Path]):
        self.target_class_name = target_class_name
        self.directories = directories

    def __str__(self):
        return f"Error: Target class '{self.target_class_name}' not found in below directories: {os.linesep} {os.linesep.join([str(directory) for directory in self.directories])}"


class ClassAlreadyRegisteredException(Exception):
    def __init__(
        self, annotation: str, registered_class: Type, to_be_registered_class: Type
    ):
        self.annotation = annotation
        self.registered_class = registered_class
        self.to_be_registered_class = to_be_registered_class

    def __str__(self):
        return f"Error: The annotation {self.annotation} is already registered with {self.registered_class}. The class {self.to_be_registered_class} cannot be registered!"


class ActionAlreadyExecutedException(Exception):
    def __init__(self, execution_id: str):
        self.execution_id = execution_id

    def __str__(self):
        return f"Error: Action with execution id {self.execution_id} is already executed. Cannot be executed twice."


class ActionsWithSameExecutionIdException(Exception):
    def __init__(self, execution_ids: List[str]):
        self.execution_ids = execution_ids

    def __str__(self):
        return f"Error: Actions with the same execution id found! {os.linesep} {os.linesep.join([execution_id for execution_id in self.execution_ids])}"

class NoActionsWithExecutionIdFoundException(Exception):
    def __init__(self, execution_id: str):
        self.execution_id = execution_id

    def __str__(self):
        return f"Error: No Action with Execution Id {self.execution_id} is found"

class NoMatchesFoundWithFilter(Exception):
    def __init__(self,
                 filter: Dict,
                 collection: List[Any],
                 ):
        self.filter = filter
        self.collection = collection

    def __str__(self):
        return f"No matches found with {self.filter=} in below collection {self.collection=}"
