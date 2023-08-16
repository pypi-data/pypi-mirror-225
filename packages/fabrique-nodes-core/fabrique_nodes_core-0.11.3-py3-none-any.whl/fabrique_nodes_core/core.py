from typing import List, Literal
from fabrique_nodes_core.ui_params import UIParams  # noqa: F401
from fabrique_nodes_core.port_types import port_type
from fabrique_nodes_core.configs_model import Port, NodeData


class Array(list):
    pass


class EmptyValue(float):
    def __new__(self):
        return float.__new__(self, float('nan'))


class NodeConfig(NodeData):
    """Node config data model

    :param id_: unique node id in actor
    :param ports_out: output ports list (generated from g_ports_out)
    :param ports_in: input ports list (generated from g_ports_in)
    :param description: node description
    :param schema_: node json schema
    :param config: configs form UI
    """
    id_: str
    ports_out: List[Port] = []
    ports_in: List[Port] = []
    description: str = ''
    schema_: str = ''


class BaseNode:
    """Base Node Class

    :param type_: your unique node type
    :param group_type_: leave this value undefined, will be filled automatically if this node belongs to a group
    :param category: one of ['StructOps', 'IO', 'Funcional', 'Stateful', 'Conditional', 'Misc']
                     used for grouping and styling nodes
    :param ui_params: UIParams your custom port groups parameters
    :param initial_config: initial node configuration
    """
    type_: str = ''
    group_type_: str = ''
    category: Literal['StructOps', 'IO', 'Funcional', 'Stateful', 'Conditional', 'Misc'] = 'Misc'
    ui_params: UIParams = UIParams()
    initial_config: NodeData = NodeData()

    def __init__(self, cfg: NodeConfig, user_id: str, **_kwargs):
        """Node init

        :param cfg: node configuration
        :type cfg: NodeConfig
        """
        cfg.ports_in = [p for ports in cfg.g_ports_in for p in ports]
        cfg.ports_out = [p for ports in cfg.g_ports_out for p in ports]
        self.cfg = cfg
        self.user_id = user_id

    def process(self, *args) -> list:
        """Default processing logic

        :param args: list of input values to process
        :return: list of output values
        :rtype: list
        """
        raise Exception('Process method must be implemented!')

    def is_valid_args(self, args) -> bool:
        return all([False if arg and isinstance(arg, EmptyValue) else True for arg in args])

    def process_universal(self, *array_args) -> list:
        nonnull_args = [a for a in array_args if a]
        if nonnull_args and isinstance(nonnull_args[0], Array):
            results_list = [self.process_universal(*args) for args in zip(*array_args) if self.is_valid_args(args)]
            return [Array(values_lst) for values_lst in zip(*results_list)]
        else:
            return self.process(*array_args)

    def process_many(self, microbatch) -> list:
        resulting_microbatch = []
        for args in zip(*microbatch):
            if self.is_valid_args(args):
                res = self.process_universal(*args)
                if res:
                    resulting_microbatch.append(res)
        return resulting_microbatch


class NodesGroup:
    """Node group wrapper

    :param type_: will be copied in group_type_ of BaseNode
    :param nodes_array: list of Node classes to group
    """
    type_: str = ''
    nodes_array: list[BaseNode] = []


root_port = Port(id_='root', name='', type_=port_type[None], special=False, code='')
