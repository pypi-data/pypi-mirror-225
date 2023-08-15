class OPG:
    def __init__(self):
        self.Name = ""
        self.ListOfNodes = []
        self.ListPGEdges = []

    def add_node(self):
        node = Node()
        self.ListOfNodes.append(node)
        return node


class Node:
    def __init__(self):
        self.NodeNr = 0
        self.NodeID = ""
        self.ListCPDCCombinations = []

    def add_cpdc_combination(self):
        combination = CPDCCombination()
        self.ListCPDCCombinations.append(combination)
        return combination


class CPDCCombination:
    def __init__(self):
        self.ListActorialResources = []
        self.Name = ""
        self.CPDCID = ""

    def add_actorial_resource(self, resource):
        self.ListActorialResources.append(resource)
