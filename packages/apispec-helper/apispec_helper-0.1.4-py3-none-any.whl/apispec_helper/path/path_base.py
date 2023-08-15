from dataclasses import asdict
from apispec_helper.path.path_item import PathItem


class PathBase:
    def __init__(self, path: str, path_item_definition: PathItem):
        self.__path_item_definition = path_item_definition
        self.__path = path

    @property
    def operations(self):
        return asdict(self.__path_item_definition)['operations']

    @property
    def summary(self):
        return asdict(self.__path_item_definition)['summary']

    @property
    def description(self):
        return asdict(self.__path_item_definition)['description']

    @property
    def servers(self):
        return asdict(self.__path_item_definition)['servers']

    @property
    def parameters(self):
        return asdict(self.__path_item_definition)['parameters']

    @property
    def path(self):
        return self.__path

    @property
    def apispec_parameter(self) -> dict:
        parameter_list = ["path", "operations", "summary", "description", "servers", "parameters"]
        parameter_dict = dict()

        for parameter in parameter_list:
            try:
                value = getattr(self, parameter)
                parameter_dict[parameter] = value
            except KeyError:
                pass

        return parameter_dict
