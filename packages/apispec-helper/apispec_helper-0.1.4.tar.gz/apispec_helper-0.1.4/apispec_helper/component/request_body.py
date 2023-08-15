from apispec_helper._internal_utils.dataclass_helper_base import DataclassHelperBase
from apispec_helper.component.content import ContentType
from dataclasses import dataclass


@dataclass
class RequestBody(DataclassHelperBase):
    content: ContentType

    description: str = None
    required: bool = None

