from dataclasses import dataclass
from apispec_helper._internal_utils.dataclass_helper_base import DataclassHelperBase


@dataclass
class ExternalDocumentation(DataclassHelperBase):
    url: str
    description: str = None
