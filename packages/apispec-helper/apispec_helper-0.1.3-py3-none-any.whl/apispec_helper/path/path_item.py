from dataclasses import dataclass
from apispec_helper._internal_utils.dataclass_helper_base import DataclassHelperBase
from typing import List, Mapping
from apispec_helper.basic_type.external_documentation import ExternalDocumentation
from apispec_helper.component.parameter import ParameterType
from apispec_helper.component.request_body import RequestBody
from apispec_helper.component.response import Response
from apispec_helper.basic_type.server import Server

from apispec_helper._internal_utils.one_of_field_checker import OneOfFieldChecker
from apispec_helper._internal_utils.post_init_base import PostInitBase


class OperationsDataclassHelperBase(PostInitBase):
    def __post_init__(self):
        super().__post_init__()
        OneOfFieldChecker(self, ["get", "put", "post", "delete", "options", "head", "patch", "trace"]).execute()


@dataclass
class Operation(DataclassHelperBase):
    # can be "default" or HTTP status code
    responses: dict[str, Response]

    tags: List[str] = None
    summary: str = None
    description: str = None
    externalDocs: ExternalDocumentation = None
    operationId: str = None
    parameters: List[ParameterType] = None
    requestBody: RequestBody = None
    # callback is a special case as callback can be nested, which will be circular dependency. Therefore, set type of
    # callback as dict and let user construct callback object dict for convenience
    # str is for reference
    callbacks: dict | str = None
    deprecated: bool = None
    security: List = None
    servers: List[Server] = None


@dataclass
class Operations(DataclassHelperBase, OperationsDataclassHelperBase):
    get: Operation = None
    put: Operation = None
    post: Operation = None
    delete: Operation = None
    options: Operation = None
    head: Operation = None
    patch: Operation = None
    trace: Operation = None


# to match definition of apispec's core path API
@dataclass
class PathItem(DataclassHelperBase):
    operations: Operations

    summary: str = None
    description: str = None
    servers: List[Server] = None
    parameters: [str, ParameterType] = None
