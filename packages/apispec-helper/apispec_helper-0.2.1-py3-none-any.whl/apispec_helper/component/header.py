from apispec_helper.basic_type.common_type import CommonType
from apispec_helper.basic_type.external_documentation import ExternalDocumentation
from dataclasses import dataclass
from apispec_helper._internal_utils.dataclass_helper_base import DataclassHelperBase
from apispec_helper.basic_type.examples import ExamplesType


@dataclass
class Header(DataclassHelperBase):
    schema: CommonType = None
    content: dict[str, str] = None
    description: str = None
    externalDocs: ExternalDocumentation = None
    required: bool = None
    deprecated: bool = None
    allowEmptyValue: bool = None

    style: str = None
    explode: bool = None
    allowReserved: bool = None

    example: dict = None
    examples: ExamplesType = None
