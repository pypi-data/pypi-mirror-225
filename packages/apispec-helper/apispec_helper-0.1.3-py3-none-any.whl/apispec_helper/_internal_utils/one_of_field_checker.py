from typing import List


class NoneOfOneOfFieldsProvidedError(Exception):
    def __init__(self, fields: List[str]):
        super().__init__(f"None of one of field provided: [{fields}]")


class OneOfFieldChecker:
    def __init__(self, instance, one_of_fields: List[str]):
        self.__instance = instance
        self.__one_of_fields = one_of_fields

    def execute(self):
        for field in self.__one_of_fields:
            if hasattr(self.__instance, field) is True:
                return

        raise NoneOfOneOfFieldsProvidedError(self.__one_of_fields)
