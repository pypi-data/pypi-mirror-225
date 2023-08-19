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
            # Field always exists(can be checked via __dir__), so we check value provided instead
            filed_with_value = getattr(self.__instance, field) is not None

            if filed_with_value is True:
                return

        raise NoneOfOneOfFieldsProvidedError(self.__one_of_fields)
