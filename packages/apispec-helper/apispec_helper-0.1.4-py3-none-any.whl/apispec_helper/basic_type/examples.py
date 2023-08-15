from dataclasses import dataclass
from apispec_helper._internal_utils.dataclass_helper_base import DataclassHelperBase
from apispec_helper._internal_utils.post_init_base import PostInitBase
from apispec_helper._internal_utils.mutual_exclusive_field_checker import MutualExclusiveFieldChecker
from apispec_helper._internal_utils.one_of_field_checker import OneOfFieldChecker


class ExampleDataclassHelperBase(PostInitBase):
    def __post_init__(self):
        super().__post_init__()
        MutualExclusiveFieldChecker(self, ["value", "externalValue"]).execute()
        OneOfFieldChecker(self, ["value", "externalValue"]).execute()


@dataclass
class Example(DataclassHelperBase, ExampleDataclassHelperBase):
    summary: str = None
    description: str = None

    value: int | str | dict = None
    externalValue: str = None


ExamplesType = dict[str: Example]
