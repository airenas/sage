import nltk as nltk

from sage.logger import logger


class ParseError(Exception):
    """Base class for parse exceptions"""
    pass


class UnknownLeave(ParseError):
    """Raised when the leave is undefined"""
    pass


class UnknownOperation(ParseError):
    """Raised when the label is undefined"""
    pass


class ResultNode:
    def __init__(self, node: nltk.Tree = None, node_value: str = ""):
        self.nodes = []
        self.nltk_node = node
        self.name = ""
        if node is not None:
            self.name = node.label()
        self.node_value = node_value
        self.value = 0
        self.operation = None


class ResultParser:
    def __init__(self):
        logger.info("Init Result Parser")
        self.leaves_map = init_leaves()
        self.operations_map = init_operations()

    def parse(self, tree: nltk.Tree) -> str:
        res_tree = self.map_to_res(tree)
        self.calculate(res_tree)
        return str(res_tree.value)

    def map_to_res(self, node) -> ResultNode:
        if type(node) is nltk.Tree:
            res = ResultNode(node=node)
            for ch in node:
                res.nodes.append(self.map_to_res(ch))
        else:
            res = ResultNode(node_value=node)
        return res

    def calculate(self, node: ResultNode):
        for ch in node.nodes:
            self.calculate(ch)
        self.do_operation(node)

    def do_operation(self, node):
        if node.nltk_node is not None:
            v = self.operations_map.get(node.nltk_node.label())
            if v is None:
                raise UnknownOperation(node.nltk_node.label())
            v(node)
        else:
            v = self.leaves_map.get(node.node_value)
            if v is None:
                raise UnknownLeave(node.node_value)
            node.value = v


def getNodes(parent, deep):
    if type(parent) is nltk.Tree:
        if parent.label() == 'S':
            print("======== Sentence =========")
            print("Sentence:", " ".join(parent.leaves()))
    for node in parent:
        if type(node) is nltk.Tree:
            print("Label: %d - %s" % (deep, node.label()))
            print("Leaves:", node.leaves())
            getNodes(node, deep + 1)
        else:
            print("Word:", node)


def init_leaves() -> dict:
    res = dict()
    res['vienas'] = 1
    res['du'] = 2
    res['trys'] = 3
    res['keturi'] = 4
    res['penki'] = 5
    res['šeši'] = 6
    res['septyni'] = 7
    res['aštuoni'] = 8
    res['devyni'] = 9
    res['dešimt'] = 10
    res['dvidešimt'] = 20
    res['šimtai'] = 100
    for s in ["plius", "minus", "kart"]:
        res[s] = 0
    return res


def init_operations() -> dict:
    res = dict()
    for s in ["VIENETAS", "DESIMT", "DESIMTYS", "SIMTAS", "Israiska", "S"]:
        res[s] = take_first

    res["Vienet"] = process_vienetas
    res["Desimt"] = process_desimt
    res["Simt"] = process_simtai
    res["Tukst"] = process_vienetas
    res["Sveikas"] = process_vienetas
    res["Skaicius"] = process_vienetas
    res["Gilyn"] = process_vienetas
    res["Reiksme"] = process_vienetas
    res["Isrneig"] = process_vienetas
    res["Isrlps"] = process_vienetas
    res["Isrsak"] = process_vienetas
    res["Isrkart"] = process_op
    res["Israiskaplus"] = process_op
    res["Plius"] = process_plius
    res["Minus"] = process_minus
    res["Daugyba"] = process_kart
    for s in ["Skip", "PLIUS", "MINUS", "DAUGYBA"]:
        res[s] = process_skip
    return res


def process_vienetas(node: ResultNode):
    node.value = node.nodes[0].value


def process_desimt(node: ResultNode):
    res = 0
    for i in range(len(node.nodes)):
        res = res + node.nodes[i].value
    node.value = res


def process_simtai(node: ResultNode):
    if (len(node.nodes)) == 1:
        node.value = node.nodes[0].value
        return
    if (len(node.nodes)) == 3:
        node.value = node.nodes[0].value * node.nodes[1].value + node.nodes[2].value
        return
    if node.nodes[0].name == "SIMTAS":
        node.value = node.nodes[0].value + node.nodes[1].value
    else:
        node.value = node.nodes[0].value * node.nodes[1].value


def process_skip(node: ResultNode):
    pass


def take_first(node: ResultNode):
    node.value = node.nodes[0].value


def process_op(node: ResultNode):
    if len(node.nodes) == 3:
        node.nodes[1].operation(node)
        return
    node.value = node.nodes[0].value


def process_plius(node: ResultNode):
    def op(node_p: ResultNode):
        node_p.value = node_p.nodes[0].value + node_p.nodes[2].value

    node.operation = op


def process_kart(node: ResultNode):
    def op(node_p: ResultNode):
        node_p.value = node_p.nodes[0].value * node_p.nodes[2].value

    node.operation = op


def process_minus(node: ResultNode):
    def op(node_p: ResultNode):
        node_p.value = node_p.nodes[0].value - node_p.nodes[2].value

    node.operation = op
