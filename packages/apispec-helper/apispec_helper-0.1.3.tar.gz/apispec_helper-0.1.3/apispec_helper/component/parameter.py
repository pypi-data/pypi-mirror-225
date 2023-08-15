from dataclasses import dataclass
from apispec_helper._internal_utils.dataclass_helper_base import DataclassHelperBase
from apispec_helper.basic_type.common_type import CommonType
from apispec_helper.component.content import ContentType
from apispec_helper.basic_type.examples import ExamplesType
from typing import Union
from apispec_helper._internal_utils.mutual_exclusive_field_checker import MutualExclusiveFieldChecker
from apispec_helper._internal_utils.one_of_field_checker import OneOfFieldChecker
from apispec_helper._internal_utils.post_init_base import PostInitBase


class ParameterDataclassHelperBase(PostInitBase):
    def __post_init__(self):
        super().__post_init__()
        MutualExclusiveFieldChecker(self, ["schema", "content"]).execute()
        OneOfFieldChecker(self, ["schema", "content"]).execute()


class ParameterLocation:
    QUERY = "query"
    PATH = "path"
    COOKIE = "cookie"
    HEADER = "header"


@dataclass
class Parameter(DataclassHelperBase, ParameterDataclassHelperBase):
    # refer to ParameterLocation
    in_: str
    name: str

    schema: CommonType = None
    content: ContentType = None

    description: str = None
    required: bool = None
    deprecated: bool = None
    allowEmptyValue: bool = None

    # refer to ParameterStyle
    style: str = None
    explode: bool = None
    allowReserved: bool = None

    example: dict = None
    examples: ExamplesType = None


# str for reference
ParameterType = Union[Parameter, str]
