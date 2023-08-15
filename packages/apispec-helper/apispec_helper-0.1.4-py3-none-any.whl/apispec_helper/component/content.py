from dataclasses import dataclass
from apispec_helper.basic_type.common_type import CommonType
from apispec_helper._internal_utils.dataclass_helper_base import DataclassHelperBase
from apispec_helper.component.header import Header
from typing import Union


class CommonMediaTypeName:
    APPLICATION_JSON = "application/json"
    APPLICATION_OCTET_STEAM = "application/octet-stream"
    APPLICATION_X_WWW_FORM_URLENCODED = "application/x-www-form-urlencoded"

    MULTIPART_FORM_DATA = "multipart/form-data"
    MULTIPART_MIXED = "multipart/mixed"

    TEXT_PAIN = "text/plain"


@dataclass
class Encoding(DataclassHelperBase):
    contentType: str

    # dict[str: str] for reference
    headers: dict[str, Header] | dict[str, str] = None
    # reference to ParameterStyle
    style: str = None
    explode: bool = None
    allowReserved: bool = None


@dataclass
class MediaType(DataclassHelperBase):
    schema: CommonType
    encoding: dict[str, Encoding] = None
    example: dict = None
    examples: dict = None


ContentType = Union[dict[str, MediaType]]
