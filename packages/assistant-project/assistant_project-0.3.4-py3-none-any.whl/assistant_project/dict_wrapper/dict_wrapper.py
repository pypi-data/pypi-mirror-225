import json
from .utils import import_yaml_cfg
# from utils import import_yaml_cfg


class DictReader:
    def __init__(self, data_cfg):
        # Read from yaml if not already as dict
        self.config = data_cfg if type(data_cfg) is dict else import_yaml_cfg(data_cfg)

    def get_cfg_from_name(self, file_name):
        return self.config["FILES"][file_name]

    def iterate_for_list(self, obj, search_key, prekey=""):
        if type(obj) is dict:
            for key, value in obj.items():
                if type(value) is dict:
                    result = self.iterate_for_list(value, search_key, prekey=(prekey + '.' + key))
                    if result is not None:
                        return result
                elif type(value) is list:
                    if (prekey+'.' + key).__contains__(search_key):
                        return value
        return None

    def iterate_for_value(self, obj, pattern, prekey=""):
        # Currently only for single values, not for entire list of chars. Might be updated at a later stage
        values = {}
        if type(obj) is dict:
            for key, value in obj.items():
                if type(value) in [dict, list]:
                    result = self.iterate_for_value(value, pattern, prekey=(prekey + '.' + key))
                    values.update(result)
                else:
                    contained = [x for x in pattern.values() if (prekey+'.' + key).__contains__(x)]
                    for match in set(contained):
                        # new_dict_key = list(pattern.keys())[list(pattern.values()).index(match)]
                        dict_keys = [k for k in pattern.keys() if pattern[k] == match]
                        for k in dict_keys:
                            values[k] = value
        if type(obj) is list and len(obj) > 0:
            result = self.iterate_for_value(obj[0], pattern, prekey=prekey)
            values.update(result)
        return values

    def get_items(self, file_dict, identifier):
        cfg = self.config[identifier]
        obj = self.iterate_for_list(file_dict, cfg['LIST'])
        db_items = []
        for element in obj:
            item = self.iterate_for_value(element, cfg['ATTRIBUTES'])
            if not db_items.__contains__(item):
                db_items.append(item)
        return db_items


if __name__ == "__main__":
    def import_json():
        with open('config/ProcessGraph1_4.json') as json_file:
            data = json.load(json_file)
        return data

    wrapper = DictReader(data_cfg="config/task.yaml")
    file = import_json()
    db_item = wrapper.get_items(file, 'NODE')
    print(db_item)

