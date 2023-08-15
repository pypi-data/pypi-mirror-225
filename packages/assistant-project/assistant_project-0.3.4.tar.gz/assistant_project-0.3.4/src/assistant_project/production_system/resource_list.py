class ResourceList:
    def add_resource(self):
        resource = Resource()
        self.ResourcesList.append(resource)
        return resource

    def get_resource_by_id(self, cpdid):
        for resource in self.ResourcesList:
            if resource.CPDID == cpdid:
                return resource
        return None


class Resource:
    def __init__(self):
        self.Name = ""
        self.CPDID = ""
        self.Reconfiguration = False
        self.oActorialResource = ActorialResource()
        # self.oSensorialResource = self.SensorialResource()


class ActorialResource:
    def __init__(self):
        self.ActuatorName = ""
        self.ActuatorID = ""
        self.ActuatorType = ""


class SensorialResource:
    def __init__(self):
        pass
