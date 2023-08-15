from dataclasses import dataclass
from apispec_helper._internal_utils.dataclass_helper_base import DataclassHelperBase
from apispec_helper._internal_utils.post_init_base import PostInitBase


class OAuthFlowFieldNotSpecifiedError(Exception):
    def __init__(self, flow_name, field_name):
        super().__init__(f"{field_name} is required for the OAuth flow {flow_name} but not specified")


class FlowFieldChecker:
    def __init__(self, instance, flow_name: str, field_name_list: list[str]):
        self.__instance = instance
        self.__flow_name = flow_name
        self.__field_name_list = field_name_list

    def execute(self):
        if hasattr(self.__instance, self.__flow_name):
            self.__check_field_exist()

    def __check_field_exist(self):
        for field_name in self.__field_name_list:
            if hasattr(getattr(self.__instance, self.__flow_name), field_name) is False:
                raise OAuthFlowFieldNotSpecifiedError(flow_name=self.__flow_name, field_name=field_name)


class OAuthFlowsDataclassHelperBase(PostInitBase):
    def __post_init__(self):
        super().__post_init__()
        FlowFieldChecker(instance=self, flow_name="implicit", field_name_list=["authorizationUrl", ]).execute()
        FlowFieldChecker(instance=self, flow_name="password", field_name_list=["tokenUrl", ]).execute()
        FlowFieldChecker(instance=self, flow_name="clientCredentials", field_name_list=["tokenUrl", ]).execute()
        FlowFieldChecker(instance=self, flow_name="authorizationCode", field_name_list=["tokenUrl", "authorizationUrl"]).execute()


@dataclass
class OAuthFlow(DataclassHelperBase):
    scopes: dict[str, str]

    refreshUrl: str = None

    # used for implicit / authorizationCode
    authorizationUrl: str = None

    # used for password / authorizationCode / clientCredentials
    tokenUrl: str = None


@dataclass
class OAuthFlows(DataclassHelperBase, OAuthFlowsDataclassHelperBase):
    implicit: OAuthFlow = None
    password: OAuthFlow = None
    clientCredentials: OAuthFlow = None
    authorizationCode: OAuthFlow = None


class SecuritySchemeType:
    API_KEY = "apiKey"
    HTTP = "http"
    OAUTH2 = "oauth2"
    OPENID_Connect = "openIdConnect"


class APIKeyLocation:
    QUERY = "query"
    HEADER = "header"
    COOKIE = "cookie"


class HTTPAuthenticationScheme:
    # refer to https://www.iana.org/asignments/http-authschemes/http-authschemes.xhtml
    BASIC = "basic"
    BEARER = "bearer"
    DIGEST = "digest"
    DPOP = "dpop"
    HOBA = "hoba"
    MUTUAL = "mutual"
    NEGOTIATE = "negotiate"
    OAUTH = "oauth"
    SCRAM_SHA_1 = "scram-sha-1"
    SCRAM_SHA_256 = "scram-sha-256"
    VAPID = "vapid"


@dataclass
class SecurityScheme(DataclassHelperBase):
    # refer to SecuritySchemeType
    type_: str

    description: str = None

    # used for API Key
    name: str = None

    # refer to APIKeyLocation
    in_: str = None

    # used for HTTP
    scheme: str = None
    # required when scheme is "bearer
    bearerFormat: str = None

    # used for oauth2
    flows: OAuthFlows = None

    # used for OpenID Connect
    openIdConnectUrl: str = None
