from typing import Any, List, Dict

import nltk as nltk

from sage.logger import logger


class ParseError(Exception):
    """Base class for parse exceptions"""
    pass


class UnknownLeave(ParseError):
    """Raised when the leave is undefined"""

    def __init__(self, string):
        self.message = "Unknown `%s`" % string
        self.string = string


class NoImplemented(ParseError):
    """Raised when the operation is not implemented"""

    def __init__(self, string):
        self.message = "Not implemented `%s`" % string
        self.string = string


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
        return self.to_str(res_tree.value)

    def map_to_res(self, node) -> ResultNode:
        if type(node) is nltk.Tree:
            res = ResultNode(node=node)
            for ch in node:
                res.nodes.append(self.map_to_res(ch))
        else:
            res = ResultNode(node_value=node)
        return res

    def to_str(self, value):
        if value == round(value):
            return str(round(value))
        return str(value)

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


class EqParser(ResultParser):
    def __init__(self):
        super().__init__()
        logger.info("Init Eq Parser")
        self.leaves_map = init_leaves()
        self.operations_map = init_operations_eq()

    def to_str(self, value):
        return str(value)


def get_nodes(parent, deep):
    if type(parent) is nltk.Tree:
        if parent.label() == 'S':
            print("======== Sentence =========")
            print("Sentence:", " ".join(parent.leaves()))
    for node in parent:
        if type(node) is nltk.Tree:
            print("Label: %d - %s" % (deep, node.label()))
            print("Leaves:", node.leaves())
            get_nodes(node, deep + 1)
        else:
            print("Word:", node)


def init_leaves() -> dict:
    res = dict()
    res['vienas'] = 1
    add_to_dict(res, ['du', 'dviejų', 'dvi'], 2)
    res['trys'] = 3
    add_to_dict(res, ['keturi', 'ketvirtosios'], 4)
    add_to_dict(res, ['penki', 'penktosios'], 5)
    res['šeši'] = 6
    res['septyni'] = 7
    res['aštuoni'] = 8
    res['devyni'] = 9
    for k, v in {'dešimt': 10, 'dvidešimt': 20, 'trisdešimt': 30, 'keturiasdešimt': 40, 'penkiasdešimt': 50,
                 'šešiasdešimt': 60, 'septyniasdešimt': 70, 'aštuoniasdešimt': 80, 'devyniasdešimt': 90}.items():
        res[k] = v
    for k, v in {'vienuolika': 11, 'dvylika': 12, 'trylika': 13, 'keturiolika': 14, 'penkiolika': 15,
                 'šešiolika': 16, 'septyniolika': 17, 'aštuoniolika': 18, 'devyniolika': 19}.items():
        res[k] = v

    add_to_dict(res, ["plius", 'pridėti', 'atimti', 'minus', 'dalint', 'dalinti', 'dalinta', 'padalint', 'padalinti',
                      'padalinta', 'dauginti', 'dauginta', 'padauginti', 'padauginta', 'kart',
                      "iš", "kablelis", "skliaustai"], 0)
    add_to_dict(res, ["šimtas", "šimtai"], 100)
    add_to_dict(res, ["tūkstantis", "tūkstančiai", "tūkstančių"], 1000)
    add_to_dict(res, ["milijonas", "milijonai"], 1000000)
    return res


def add_to_dict(d: Dict, keys: List[str], val: Any):
    for s in keys:
        d[s] = val


def init_operations() -> dict:
    res = dict()
    add_to_dict(res, ["VIENETAS", "DESIMT", "DESIMTYS", "SIMTAS", "TUKSTANTIS",
                      "MILIJONAS", "Israiska", "S", "VIENETASSHAK", 'KABLELIS',
                      "VIENETASSKAIT", "VIENETASVARD", "VIENUOLIKOS"],
                take_first)
    add_to_dict(res, ["Vienet", "VienetShak", "VienetSkait", "VienetVard", "SveikojiDal", "Trupmenine", "SingleParen"],
                take_first)
    add_to_dict(res, ["Desimt", "DesimtShak", "DesimtSkait", "DesimtVard"], process_desimt)
    add_to_dict(res, ["Simt", "SimtShak", "SimtSkait", "SimtVard"], process_simtai)
    add_to_dict(res, ["Tukst", "TukstShak", "TukstSkait", "TukstVard"], process_tukst)
    add_to_dict(res, ["Sveikas", "SveikasShak", "SveikasSkait", "SveikasVard"], process_sveikas)
    res["Skaicius"] = process_skaicius
    res["Gilyn"] = process_vienetas
    res["Reiksme"] = process_vienetas
    res["Isrneig"] = process_vienetas_neig
    res["Isrlps"] = process_vienetas
    res["Isrsak"] = process_vienetas
    res["Isrkart"] = process_op
    res["Israiskaplus"] = process_op
    res["Plius"] = process_plius
    res["Minus"] = process_minus
    res["Daugyba"] = process_kart
    res["Dalyba"] = process_dalint
    res["Realus"] = process_realus
    for s in ["Skip", "PLIUS", "MINUS", "DAUGYBA", "DALYBA"]:
        res[s] = process_skip
    res["SklKair"] = process_skip
    res["KairysSkl"] = process_skl_kair
    res["More"] = process_more

    return res


def init_operations_eq() -> dict:
    res = dict()
    add_to_dict(res, ["VIENETAS", "DESIMT", "DESIMTYS", "SIMTAS", "TUKSTANTIS",
                      "MILIJONAS", "Israiska", "S", "VIENETASSHAK", 'KABLELIS',
                      "VIENETASSKAIT", "VIENETASVARD", "VIENUOLIKOS"],
                take_first)
    add_to_dict(res, ["Vienet", "VienetShak", "VienetSkait", "VienetVard", "SveikojiDal", "Trupmenine", "SingleParen"],
                take_first)
    add_to_dict(res, ["Desimt", "DesimtShak", "DesimtSkait", "DesimtVard"], process_desimt)
    add_to_dict(res, ["Simt", "SimtShak", "SimtSkait", "SimtVard"], process_simtai)
    add_to_dict(res, ["Tukst", "TukstShak", "TukstSkait", "TukstVard"], process_tukst)
    add_to_dict(res, ["Sveikas", "SveikasShak", "SveikasSkait", "SveikasVard"], process_sveikas)
    res["Skaicius"] = process_skaicius_eq
    res["Gilyn"] = process_vienetas
    res["Reiksme"] = process_vienetas
    res["Isrneig"] = process_vienetas_neig_eq
    res["Isrlps"] = process_vienetas
    res["Isrsak"] = process_vienetas
    res["Isrkart"] = process_op
    res["Israiskaplus"] = process_op
    res["Plius"] = process_plius_eq
    res["Minus"] = process_minus_eq
    res["Daugyba"] = process_kart_eq
    res["Dalyba"] = process_dalint_eq
    res["Realus"] = process_realus
    for s in ["Skip", "PLIUS", "MINUS", "DAUGYBA", "DALYBA"]:
        res[s] = process_skip
    res["SklKair"] = process_skip
    res["KairysSkl"] = process_skl_kair_eq
    res["More"] = process_more_eq
    return res


def process_vienetas(node: ResultNode):
    node.value = node.nodes[0].value


def process_vienetas_neig(node: ResultNode):
    if (len(node.nodes)) == 2:
        node.value = 0 - node.nodes[1].value
    else:
        process_vienetas(node)


def process_vienetas_neig_eq(node: ResultNode):
    if (len(node.nodes)) == 2:
        node.value = "- %s" % node.nodes[1].value
    else:
        process_vienetas(node)


def process_desimt(node: ResultNode):
    res = 0
    for i in range(len(node.nodes)):
        res = res + node.nodes[i].value
    node.value = res


def process_realus(node: ResultNode):
    num = "%d.%d" % (node.nodes[0].value, node.nodes[2].value)
    res = float(num)
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


def process_skaicius(node: ResultNode):
    if (len(node.nodes)) == 1:
        node.value = node.nodes[0].value
        return
    node.value = node.nodes[0].value / node.nodes[1].value


def process_skaicius_eq(node: ResultNode):
    if (len(node.nodes)) == 1:
        node.value = node.nodes[0].value
        return
    node.value = "\\frac{%s}{%s}" % (node.nodes[0].value, node.nodes[1].value)


def process_skl_kair(node: ResultNode):
    if (len(node.nodes)) == 1:
        node.value = node.nodes[0].value
        return
    node.value = node.nodes[1].value


def process_skl_kair_eq(node: ResultNode):
    v = node.nodes[0].value
    if (len(node.nodes)) > 1:
        v = node.nodes[1].value
    node.value = "\\left( %s \\right)" % v


def process_more(node: ResultNode):
    if (len(node.nodes)) == 3:
        if node.nodes[1].name == "Plius":
            op_plius(node)
            return
        if node.nodes[1].name == "Minus":
            op_minus(node)
            return
    raise NotImplemented(node.name)


def process_more_eq(node: ResultNode):
    if (len(node.nodes)) == 3:
        if node.nodes[1].name == "Plius":
            op_plius_eq(node)
            return
        if node.nodes[1].name == "Minus":
            op_minus_eq(node)
            return
    raise NotImplemented(node.name)


def process_tukst(node: ResultNode):
    if (len(node.nodes)) == 1:
        node.value = node.nodes[0].value
        return
    if (len(node.nodes)) == 3:
        node.value = node.nodes[0].value * node.nodes[1].value + node.nodes[2].value
        return
    if node.nodes[0].name == "TUKSTANTIS":
        node.value = node.nodes[0].value + node.nodes[1].value
    else:
        node.value = node.nodes[0].value * node.nodes[1].value


def process_sveikas(node: ResultNode):
    if (len(node.nodes)) == 1:
        node.value = node.nodes[0].value
        return
    if (len(node.nodes)) == 3:
        node.value = node.nodes[0].value * node.nodes[1].value + node.nodes[2].value
        return
    if node.nodes[0].name == "MILIJONAS":
        node.value = node.nodes[0].value + node.nodes[1].value
    else:
        node.value = node.nodes[0].value * node.nodes[1].value


def process_skip(node: ResultNode):
    pass


def take_first(node: ResultNode):
    node.value = node.nodes[0].value


def process_op(node: ResultNode):
    if len(node.nodes) >= 3:
        node.nodes[1].operation(node)
        return
    node.value = node.nodes[0].value


def op_plius(node: ResultNode):
    node.value = node.nodes[0].value + node.nodes[2].value


def process_plius(node: ResultNode):
    node.operation = op_plius


def op_plius_eq(node: ResultNode):
    node.value = "%s + %s" % (node.nodes[0].value, node.nodes[2].value)


def process_plius_eq(node: ResultNode):
    node.operation = op_plius_eq


def process_kart(node: ResultNode):
    def op(node_p: ResultNode):
        node_p.value = node_p.nodes[0].value * node_p.nodes[2].value

    node.operation = op


def process_kart_eq(node: ResultNode):
    def op(node_p: ResultNode):
        node_p.value = "%s \\cdot %s" % (node_p.nodes[0].value, node_p.nodes[2].value)

    node.operation = op


def process_dalint(node: ResultNode):
    def op(node_p: ResultNode):
        node_p.value = node_p.nodes[0].value / node_p.nodes[2].value

    node.operation = op


def process_dalint_eq(node: ResultNode):
    def op(node_p: ResultNode):
        node_p.value = "\\frac{%s}{%s}" % (node_p.nodes[0].value, node_p.nodes[2].value)

    node.operation = op


def op_minus(node: ResultNode):
    node.value = node.nodes[0].value - node.nodes[2].value


def process_minus(node: ResultNode):
    node.operation = op_minus


def op_minus_eq(node: ResultNode):
    node.value = "%s - %s" % (node.nodes[0].value, node.nodes[2].value)


def process_minus_eq(node: ResultNode):
    node.operation = op_minus_eq
