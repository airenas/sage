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


class NotImplementedOperation(ParseError):
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
        self.operations_map = init_operations(init_base_operations())

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
            node.value = v(node.nodes)
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
        self.operations_map = init_operations(init_base_operations_eq())

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
    add_to_dict(res, ['vienas', 'pirmuoju', 'vieno', 'pirmojo'], 1)
    add_to_dict(res, ['du', 'dviejų', 'dvi', 'kvadratu', 'antruoju', 'antrojo'], 2)
    add_to_dict(res, ['trys', 'trijų', 'trečiuoju', 'kubu', 'kubiniu', 'trečiojo'], 3)
    add_to_dict(res, ['keturi', 'keturių', 'ketvirtosios', 'ketvirtuoju', 'ketvirtojo'], 4)
    add_to_dict(res, ['penki', 'penkių', 'penktosios', 'penktuoju', 'penktojo'], 5)
    add_to_dict(res, ['šeši', 'šešių', 'šeštuoju', 'šeštojo'], 6)
    add_to_dict(res, ['septyni', 'septynių', 'septintuoju', 'septintojo'], 7)
    add_to_dict(res, ['aštuoni', 'aštuomnių', 'aštuntuoju', 'aštuntojo'], 8)
    add_to_dict(res, ['devyni', 'devynių', 'devintuoju', 'devintojo'], 9)
    add_to_dict(res, ['dešimt', 'dešimtuoju', 'dešimtojo'], 10)
    add_to_dict(res, ['vienuoliktuoju'], 11)
    add_to_dict(res, ['dvyliktuoju'], 12)
    add_to_dict(res, ['tryliktuoju'], 13)
    add_to_dict(res, ['keturioliktuoju'], 14)
    add_to_dict(res, ['penkioliktuoju'], 15)
    add_to_dict(res, ['šešioliktuoju'], 16)
    add_to_dict(res, ['septynioliktuoju'], 17)
    add_to_dict(res, ['aštuonioliktuoju'], 18)
    add_to_dict(res, ['devynioliktuoju'], 19)
    add_to_dict(res, ['dvidešimtuoju'], 20)
    add_to_dict(res, ['trisdešimtuoju'], 30)
    add_to_dict(res, ['keturiasdešimtuoju'], 40)
    add_to_dict(res, ['penkiasdešimtuoju'], 50)
    add_to_dict(res, ['šešiasdešimtuoju'], 60)
    add_to_dict(res, ['septyniasdešimtuoju'], 70)
    add_to_dict(res, ['aštuoniasdešimtuoju'], 80)
    add_to_dict(res, ['devyniasdešimtuoju'], 90)
    add_to_dict(res, ["šimtas", "šimtai", 'šimtuoju'], 100)
    add_to_dict(res, ["tūkstantis", "tūkstančiai", "tūkstančių", 'tūkstantuoju'], 1000)
    add_to_dict(res, ["milijonas", "milijonai", 'milijonu'], 1000000)

    for k, v in {'dvidešimt': 20, 'trisdešimt': 30, 'keturiasdešimt': 40, 'penkiasdešimt': 50,
                 'šešiasdešimt': 60, 'septyniasdešimt': 70, 'aštuoniasdešimt': 80, 'devyniasdešimt': 90}.items():
        res[k] = v
    for k, v in {'vienuolika': 11, 'dvylika': 12, 'trylika': 13, 'keturiolika': 14, 'penkiolika': 15,
                 'šešiolika': 16, 'septyniolika': 17, 'aštuoniolika': 18, 'devyniolika': 19}.items():
        res[k] = v

    add_to_dict(res, ["plius", 'pridėti', 'atimti', 'minus', 'dalint', 'dalinti', 'dalinta', 'padalint', 'padalinti',
                      'padalinta', 'dauginti', 'dauginta', 'padauginti', 'padauginta', 'kart',
                      "pakelta", 'pakelti', 'laipsniu',
                      "iš", "kablelis", "skliaustai", "skliausteliuose", "šaknis", "apskliausta", "sveikas", "visa",
                      "tai"], 0)
    return res


def add_to_dict(d: Dict, keys: List[str], val: Any):
    for s in keys:
        d[s] = val


def init_base_operations() -> dict:
    res = dict()
    res["Plius"] = op_plius
    res["Minus"] = op_minus
    res["Daugyba"] = op_daugint
    res["Dalyba"] = op_dalint
    res["Laipsnis"] = op_laipsnis
    res["Neig"] = op_neig
    res["Skliaustai"] = op_skliaustai
    return res


def init_base_operations_eq() -> dict:
    res = dict()
    res["Plius"] = op_plius_eq
    res["Minus"] = op_minus_eq
    res["Daugyba"] = op_daugint_eq
    res["Dalyba"] = op_dalint_eq
    res["Laipsnis"] = op_laipsnis_eq
    res["Neig"] = op_neig_eq
    res["Skliaustai"] = op_skliaustai_eq
    return res


def init_operations(base_op) -> dict:
    res = dict()
    add_to_dict(res, ["VIENETAS", "DESIMT", "DESIMTYS", "SIMTAS", "TUKSTANTIS",
                      "MILIJONAS", "Israiska", "S", "VIENETASSHAK", 'KABLELIS',
                      "VIENETASSKAIT", "VIENETASVARD", "VIENUOLIKOS",
                      "VIENETASLPS", "VienetLps", "SIMTASLPS", "DESIMTYSLPS", "VIENUOLIKOSLPS", "MILIJONASLPS",
                      "TUKSTANTISLPS"],
                take_first)
    add_to_dict(res, ["Vienet", "Vienet2", "VienetShak", "VienetSkait", "VienetVard", "SveikojiDal", "Trupmenine",
                      "SingleParen"],
                take_first)
    add_to_dict(res, ["Desimt", "Desimt2", "DesimtShak", "DesimtSkait", "DesimtVard", "DesimtLps"], process_desimt)
    add_to_dict(res, ["Simt", "Simt2", "SimtShak", "SimtSkait", "SimtVard", "SimtLps"], process_simtai)
    add_to_dict(res, ["Tukst", "Tukst2", "TukstShak", "TukstSkait", "TukstVard", "TukstLps"], process_tukst)
    add_to_dict(res, ["Sveikas", "Sveikas2", "SveikasShak", "SveikasSkait", "SveikasVard", "SveikasLps"],
                process_sveikas)
    add_to_dict(res, ["Skaicius", "Skaicius2"], with_base(base_op, process_skaicius))
    add_to_dict(res, ["Gilyn", "Gilyn2"], process_vienetas)
    add_to_dict(res, ["Reiksme", "Reiksme2"], process_vienetas)
    add_to_dict(res, ["Isrneig", "Isrneig2"], with_base(base_op, process_vienetas_neig))
    res["Isrlps"] = process_vienetas
    res["Isrsak"] = process_vienetas
    res["Isrkart"] = with_base(base_op, process_op)
    res["Israiskaplus"] = with_base(base_op, process_op)
    res["Plius"] = process_skip
    res["Minus"] = process_skip
    res["Daugyba"] = process_skip
    res["Lps"] = with_base(base_op, process_laipsnis)
    res["Laipsnis"] = process_laipsnis_next
    res["Dalyba"] = process_skip
    res["Realus"] = process_realus
    for s in ["Skip", "PLIUS", "MINUS", "DAUGYBA", "DALYBA", "LAIPSNISPAGRINDAS"]:
        res[s] = process_skip
    res["SklKair"] = process_skip
    res["KairysSkl"] = with_base(base_op, process_skl_kair)
    res["SklDes"] = process_skip
    res["DesinysSkl"] = with_base(base_op, process_skl_des)
    res["IsraiskaSkl"] = with_base(base_op, process_skl)

    res["More"] = with_base(base_op, process_more)

    return res


def with_base(base, op):
    def res(n) -> Any:
        return op(base, n)

    return res


def get_op(base, name):
    res = base.get(name)
    if res is None:
        raise UnknownOperation(name)
    return res


def process_vienetas(nodes: List[ResultNode]) -> Any:
    return nodes[0].value


def process_vienetas_neig(base_op, nodes: List[ResultNode]) -> Any:
    if (len(nodes)) == 2:
        return get_op(base_op, "Neig")(nodes)
    return process_vienetas(nodes)


def process_laipsnis(base_op, nodes: List[ResultNode]) -> Any:
    return get_op(base_op, "Laipsnis")(nodes)


def process_laipsnis_next(nodes: List[ResultNode]) -> Any:
    if len(nodes) == 2:
        if nodes[1].node_value == "laipsniu":
            return nodes[0].value
        elif nodes[0].node_value == "minus":
            return -nodes[1].value
        else:
            return nodes[1].value
    else:
        return nodes[0].value


def process_desimt(nodes: List[ResultNode]) -> Any:
    res = 0
    for i in range(len(nodes)):
        res = res + nodes[i].value
    return res


def process_realus(nodes: List[ResultNode]) -> Any:
    num = "%d.%d" % (nodes[0].value, nodes[2].value)
    res = float(num)
    return res


def process_simtai(nodes: List[ResultNode]) -> Any:
    if (len(nodes)) == 1:
        return nodes[0].value
    if (len(nodes)) == 3:
        return nodes[0].value * nodes[1].value + nodes[2].value
    if nodes[0].name == "SIMTAS":
        return nodes[0].value + nodes[1].value
    else:
        return nodes[0].value * nodes[1].value


def process_skaicius(base_op, nodes: List[ResultNode]) -> Any:
    if (len(nodes)) == 1:
        return nodes[0].value
    return get_op(base_op, "Dalyba")(nodes[0].value, nodes[1].value)


def process_skl_kair(base_op, nodes: List[ResultNode]) -> Any:
    if (len(nodes)) == 1:
        return get_op(base_op, "Skliaustai")(nodes[0].value)
    return get_op(base_op, "Skliaustai")(nodes[1].value)


def process_skl_des(base_op, nodes: List[ResultNode]) -> Any:
    if (len(nodes)) == 4:
        return get_op(base_op, "Skliaustai")(exec_simple_op(base_op, nodes[0:3]))
    if (len(nodes)) == 3:
        return nodes[0].value ** nodes[1].value
    if (len(nodes)) == 2:
        return get_op(base_op, "Skliaustai")(nodes[0].value)
    raise NotImplementedOperation("process_skl_des")


def process_skl(base_op, nodes: List[ResultNode]) -> Any:
    if nodes[0].name == "S":
        return get_op(base_op, "Skliaustai")(nodes[0].value)
    elif len(nodes) == 2:
        return get_op(base_op, "Skliaustai")(nodes[0].value)
    if (len(nodes)) == 4:
        return get_op(base_op, "Skliaustai")(exec_simple_op(base_op, nodes[0:3]))
    if (len(nodes)) == 3:
        return exec_simple_op(base_op, nodes[0:3])
    raise NotImplementedOperation("process_skl")


def exec_simple_op(base_op, nodes: List[ResultNode]) -> Any:
    if nodes[1].name == "Dalyba":
        return get_op(base_op, nodes[1].name)(nodes[0].value, nodes[2].value)
    return get_op(base_op, nodes[1].name)(nodes)


def process_more(base_op, nodes: List[ResultNode]) -> Any:
    if (len(nodes)) == 3:
        return exec_simple_op(base_op, nodes)
    raise NotImplementedOperation("process_more")


def process_tukst(nodes: List[ResultNode]) -> Any:
    if (len(nodes)) == 1:
        return nodes[0].value
    if (len(nodes)) == 3:
        return nodes[0].value * nodes[1].value + nodes[2].value
    if nodes[0].name == "TUKSTANTIS":
        return nodes[0].value + nodes[1].value
    else:
        return nodes[0].value * nodes[1].value


def process_sveikas(nodes: List[ResultNode]) -> Any:
    if (len(nodes)) == 1:
        return nodes[0].value
    if (len(nodes)) == 3:
        return nodes[0].value * nodes[1].value + nodes[2].value
    if nodes[0].name == "MILIJONAS":
        return nodes[0].value + nodes[1].value
    else:
        return nodes[0].value * nodes[1].value


def process_skip(nodes: List[ResultNode]) -> Any:
    return ""


def take_first(nodes: List[ResultNode]) -> Any:
    return nodes[0].value


def process_op(base_op, nodes: List[ResultNode]) -> Any:
    if len(nodes) >= 3:
        return exec_simple_op(base_op, nodes)
    return nodes[0].value


def op_plius(nodes: List[ResultNode]) -> Any:
    return nodes[0].value + nodes[2].value


def op_plius_eq(nodes: List[ResultNode]) -> Any:
    return "%s + %s" % (nodes[0].value, nodes[2].value)


def op_dalint(v1, v2) -> Any:
    return v1 / v2


def op_daugint(nodes: List[ResultNode]) -> Any:
    return nodes[0].value * nodes[2].value


def op_daugint_eq(nodes: List[ResultNode]) -> Any:
    return "%s \\cdot %s" % (nodes[0].value, nodes[2].value)


def op_dalint_eq(v1, v2) -> Any:
    return "\\frac{%s}{%s}" % (v1, v2)


def op_minus(nodes: List[ResultNode]) -> Any:
    return nodes[0].value - nodes[2].value


def op_minus_eq(nodes: List[ResultNode]) -> Any:
    return "%s - %s" % (nodes[0].value, nodes[2].value)


def op_laipsnis(nodes: List[ResultNode]) -> Any:
    return nodes[0].value ** nodes[1].value


def op_laipsnis_eq(nodes: List[ResultNode]) -> Any:
    return "%s^{%s}" % (nodes[0].value, nodes[1].value)


def op_neig(nodes: List[ResultNode]) -> Any:
    return 0 - nodes[1].value


def op_neig_eq(nodes: List[ResultNode]) -> Any:
    return "-%s" % (nodes[1].value)


def op_skliaustai(v) -> Any:
    return v


def op_skliaustai_eq(v) -> Any:
    return "\\left( %s \\right)" % v
