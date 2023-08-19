from dataclasses import dataclass, field
from apispec_helper._internal_utils.dataclass_helper_base import DataclassHelperBase
from apispec_helper.basic_type.examples import ExamplesType
from typing import List, Dict
from typing import Union


@dataclass
class CommonTypeBase(DataclassHelperBase):
    type_: str
    description: str = None
    nullable: bool = None
    readOnly: bool = None
    writeOnly: bool = None
    enum: List = None

    example: dict = None
    examples: ExamplesType = None


@dataclass
class Object(DataclassHelperBase):
    type_: str = field(default="object", init=False)
    properties: Dict[str, CommonTypeBase]
    required: List[str] = None

    additionalProperties: bool | dict = None

    minProperties: int = None
    maxProperties: int = None

    example: dict = None
    examples: ExamplesType = None


@dataclass
class OneOf(DataclassHelperBase):
    oneOf: List[CommonTypeBase | str]
    example: dict = None
    examples: ExamplesType = None


class AnyOf:
    anyOf: dict | List[CommonTypeBase | Object] = {}
    nullable: bool = None
    description: str = None

    example: dict = None
    examples: ExamplesType = None


class IntegerFormat:
    INT32 = "int32"
    INT64 = "int64"


@dataclass
class Integer(CommonTypeBase):
    type_: str = field(default="integer", init=False)
    # refer to IntegerFormat
    format_: str = None

    minimum: int = None
    exclusiveMinimum: bool = None

    maximum: int = None
    exclusiveMaximum: bool = None

    multipleOf: int = None


class NumberFormat:
    FLOAT = "float"
    DOUBLE = "double"


@dataclass
class Number(CommonTypeBase):
    type_: str = field(default="number", init=False)
    # refer to NumberFormat
    format_: str = None

    minimum: int = None
    exclusiveMinimum: bool = None

    maximum: int = None
    exclusiveMaximum: bool = None

    multipleOf: int = None


class PreDefinedStringFormat:
    DATE = "date"
    DATETIME = "date-time"
    PASSWORD = "password"
    BYTE = "byte"
    BINARY = "binary"


@dataclass
class String(CommonTypeBase):
    type_: str = field(default="string", init=False)
    # refer to PreDefinedStringFormat
    format_: str = None
    pattern: str = None

    minLength: int = None
    maxLength: int = None


@dataclass
class Boolean(CommonTypeBase):
    type_: str = field(default="boolean", init=False)


@dataclass
class Null(CommonTypeBase):
    type_: str = field(default="null", init=False)


@dataclass
class Array(CommonTypeBase):
    """
    :param items: Check the "Mixed-Type Arrays" section in https://swagger.io/docs/specification/data-models/data-types
    """
    type_: str = field(default="array", init=False)

    minItems: int = None
    maxItems: int = None

    # dict for {}, empty dict
    # str for reference
    items: CommonTypeBase | dict | list | OneOf | str = None

    uniqueItems: bool = None


# str for reference
CommonType = Union[CommonTypeBase, str, Object, OneOf, AnyOf]
