from typing import Union, Dict, List, Set


class NoMatchesFoundForJsonPathException(Exception):
    def __init__(self,
                 deserialised_json: Union[Dict, List, None],
                 json_path: str
                 ):
        self.deserialised_json = deserialised_json
        self.json_path = json_path

    def __str__(self):
        return f'No matches found for {self.json_path=} in {self.deserialised_json=}'

class CircularDependencyException(Exception):
    def __init__(self,
                 visiting_nodes: Set[str],
                 offending_node: str,
                 ):
        self.visiting_nodes = visiting_nodes
        self.offending_node = offending_node

    def __str__(self):
        return f"Circular Dependency Detected in {self.offending_node=} - {self.visiting_nodes=}"

class NonExistentNodeException(Exception):
    def __init__(self,
                 nodes,
                 non_existent_node,
                 ):
        self.nodes = nodes
        self.non_existent_node = non_existent_node

    def __str__(self):
        return f'{self.non_existent_node=} does not exist! Available nodes are {self.nodes=}'

