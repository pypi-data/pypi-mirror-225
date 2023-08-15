from typing import List


class MultipleMutualExclusiveFieldsProvidedError(Exception):
    def __init__(self, fields: List[str]):
        super().__init__(f"Multiple mutual exclusive field provided: [{fields}]")


class MutualExclusiveFieldChecker:
    def __init__(self, instance, mutual_exclusive_fields: List[str]):
        self.__instance = instance
        self.__mutual_exclusive_fields = mutual_exclusive_fields

    def execute(self):
        mutual_exclusive_check = None

        for field in self.__mutual_exclusive_fields:
            field_provided = hasattr(self.__instance, field)
            if (mutual_exclusive_check is None) or (mutual_exclusive_check and field_provided is False):
                mutual_exclusive_check = field_provided
            else:
                raise MultipleMutualExclusiveFieldsProvidedError(self.__mutual_exclusive_fields) if mutual_exclusive_check is True else None
