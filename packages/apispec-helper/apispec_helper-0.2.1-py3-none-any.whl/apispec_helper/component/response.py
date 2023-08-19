from apispec_helper._internal_utils.dataclass_helper_base import DataclassHelperBase
from apispec_helper.component.content import ContentType
from apispec_helper.component.header import Header
from apispec_helper.component.link import Link
from dataclasses import dataclass


@dataclass
class Response(DataclassHelperBase):
    description: str
    headers: dict[str, Header] = None
    content: ContentType = None
    links: dict[str, Link] = None
