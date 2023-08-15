from apispec_helper._internal_utils.post_init_base import PostInitBase


class NullValueAttributeRemover:
    def __init__(self, instance):
        self.__instance = instance

    def execute(self):
        null_value_attr_list = self._search_null_value_attributes()
        self._remove_null_value_from_attribute(null_value_attr_list)
        self._remove_null_value_from_dataclass_fields(null_value_attr_list)

    def _search_null_value_attributes(self):
        attribute_list = self.__instance.__dict__
        null_value_attr_list = list()

        for attribute in attribute_list:
            if getattr(self.__instance, attribute) is None:
                null_value_attr_list.append(attribute)

        return null_value_attr_list

    def _remove_null_value_from_attribute(self, null_value_attr_list):
        for null_value_attr in null_value_attr_list:
            delattr(self.__instance, null_value_attr)

    def _remove_null_value_from_dataclass_fields(self, null_value_attr_list):
        dataclass_fields = getattr(self.__instance, "__dataclass_fields__")

        for null_value_attr in null_value_attr_list:
            if null_value_attr in dataclass_fields.keys():
                dataclass_fields.pop(null_value_attr)

        setattr(self.__instance, "__dataclass_fields__", dataclass_fields)


class KeywordAttributeRenamer:
    def __init__(self, instance):
        self.__instance = instance
        self.__keyword_list = ["in_", "type_", "format_"]

    def execute(self):
        for attribute_name in self.__keyword_list:
            new_attribute_name = attribute_name.rstrip("_")
            self.__rename_attribute(old_attribute_name=attribute_name, new_attribute_name=new_attribute_name)
            self.__rename_dataclass_field(old_attribute_name=attribute_name, new_attribute_name=new_attribute_name)

    def __rename_attribute(self, old_attribute_name: str, new_attribute_name: str):
        if hasattr(self.__instance, old_attribute_name):
            attribute_value = getattr(self.__instance, old_attribute_name)
            setattr(self.__instance, new_attribute_name, attribute_value)

    def __rename_dataclass_field(self, old_attribute_name: str, new_attribute_name: str):
        if old_attribute_name in getattr(self.__instance, "__dataclass_fields__").keys():
            dataclass_fields = getattr(self.__instance, "__dataclass_fields__")
            dataclass_fields[new_attribute_name] = dataclass_fields.pop(old_attribute_name)
            dataclass_fields[new_attribute_name].name = new_attribute_name
            setattr(self.__instance, "__dataclass_fields__", dataclass_fields)


class DataclassHelperBase(PostInitBase):
    def __post_init__(self):
        super().__post_init__()
        NullValueAttributeRemover(self).execute()
        KeywordAttributeRenamer(self).execute()
