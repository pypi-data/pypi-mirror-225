from apispec_helper._internal_utils.post_init_base import PostInitBase
from dataclasses import fields, dataclass


keyword_fields = ["in_", "type_", "format_"]

@dataclass
class DataclassHelperBase(PostInitBase, dict):
    def __post_init__(self):
        super().__post_init__()

        argument_dict = self.__create_argument_dict()
        print(argument_dict)
        dict.__init__(self, **argument_dict)

    def __create_argument_dict(self):
        # dataclass.fields allow us to get self-defined fields. Pre-defined fields won't be included
        dataclass_fields = fields(self)
        argument_dict = dict()

        for single_field in dataclass_fields:
            field_value = getattr(self, single_field.name)
            # print(single_field.name)
            # print(field_value)
            if field_value is not None:
                argument_dict[self.__rename_keyword_fields(single_field.name)] = getattr(self, single_field.name)

        return argument_dict

    @staticmethod
    def __rename_keyword_fields(field_name):
        return field_name.rstrip("_") if field_name in keyword_fields else field_name
