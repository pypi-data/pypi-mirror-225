import yaml


def import_yaml_cfg(yaml_file):
    with open(yaml_file, "r") as stream:
        try:
            config = yaml.safe_load(stream, Loader=yaml.FullLoader)
        except:
            config = yaml.safe_load(stream)

    return config


