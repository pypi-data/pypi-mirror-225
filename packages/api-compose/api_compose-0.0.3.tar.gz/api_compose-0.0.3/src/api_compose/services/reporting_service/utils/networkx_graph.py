from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

from api_compose.core.logging import get_logger
from api_compose.services.composition_service.models.actions.actions import BaseActionModel

logger = get_logger(__name__)


def dump_actions_graph(digraph: nx.DiGraph, dump_file_path: Path):
    logger.info(f'Dumping Graph to path {dump_file_path=}')
    # Get mapping
    labels = {}
    for node, data in nx.get_node_attributes(digraph, 'data').items():
        data: BaseActionModel = data
        labels[node] = dict(data).get('execution_id')

    # Clear canvas
    plt.clf()
    nx.draw(digraph, pos=nx.spring_layout(digraph), labels=labels, with_labels=True)
    plt.draw()
    plt.savefig(dump_file_path)
