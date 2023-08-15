from dataclasses import dataclass
from apispec_helper._internal_utils.dataclass_helper_base import DataclassHelperBase
from apispec_helper.basic_type.server import Server


@dataclass
class Link(DataclassHelperBase):
    operationRef: str = None
    operationId: str = None

    parameters: dict[str, str] = None
    requestBody: str = None
    description: str = None
    server: Server = None
