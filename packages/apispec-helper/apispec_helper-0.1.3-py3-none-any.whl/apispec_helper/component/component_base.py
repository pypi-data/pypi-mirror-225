from dataclasses import asdict
from apispec_helper.basic_type import CommonType
from apispec_helper.component.parameter import Parameter
from apispec_helper.component.request_body import RequestBody
from typing import Union


ComponentType = Union[CommonType, Parameter, RequestBody]


class ComponentBase:
    def __init__(self, component_definition: ComponentType):
        self.__component_definition = component_definition

    @property
    def component_definition(self):
        return asdict(self.__component_definition)

    @property
    def component_name(self):
        return self.__class__.__name__

    @property
    def apispec_parameter(self) -> dict:
        return {
            "component_id": self.component_name,
            "component": self.component_definition
        }
