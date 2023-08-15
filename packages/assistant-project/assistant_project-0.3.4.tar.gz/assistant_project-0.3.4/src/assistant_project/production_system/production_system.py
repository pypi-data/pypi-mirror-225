import json
from .resource_list import ResourceList, Resource
from .opg_list import OPG
# from .osg_list import OSG


class ProductionSystem:
    def __init__(self):
        self.ResourcesList = []
        self.oPG = OPG()
        # self.oSG = OSG()

    def add_resource(self):
        resource = Resource()
        self.ResourcesList.append(resource)
        return resource



    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
