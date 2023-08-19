from dataclasses import dataclass
from apispec_helper._internal_utils.dataclass_helper_base import DataclassHelperBase
from typing import List


@dataclass
class ServerVariables(DataclassHelperBase):
    enum_: List[str]
    default: str
    description: str = None


@dataclass
class Server(DataclassHelperBase):
    url: str
    description: str = None
    variables: dict[str, ServerVariables] = None
