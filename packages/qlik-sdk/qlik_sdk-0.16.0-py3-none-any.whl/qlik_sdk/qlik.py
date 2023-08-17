from .apis import (
    Api_Keys,
    Apps,
    Audits,
    Automations,
    Brands,
    Collections,
    Csp_Origins,
    Data_Files,
    Extensions,
    Groups,
    Identity_Providers,
    Items,
    Licenses,
    Notes,
    Oauth_Tokens,
    Questions,
    Quotas,
    Reload_Tasks,
    Reloads,
    Roles,
    Spaces,
    Tenants,
    Themes,
    Transports,
    Users,
    Web_Integrations,
    Webhooks,
)
from .auth import Auth
from .config import Config
from .rest import RestClientInstance
from .rpc import RpcClientInstance


class Qlik:
    """
    Qlik Class is the entry-point for the Qlik python Platform SDK

    Parameters
    ----------
    config: Config
        the required configuration object

    Examples
    --------
    >>> from qlik_sdk import Qlik
    ...
    ... qlik = Qlik(Config(host=base_url, auth_type=AuthType.APIKey, api_key=api_key))
    ... user_me = qlik.users.get_me()
    """

    config: Config
    auth: Auth
    rpc: RpcClientInstance
    """
    rpc returns an RpcClient that can be used to
    connect to the engine for a specific app

    Parameters
    ----------
    app_id: str

    Attributes
    ----------
    interceptors: Interceptors

    Examples
    ----------
    >>> rpc_session = auth.rpc(app_id=session_app_id)
    ... with rpc_session.opn() as rpc_client:
    ...     app = rpc_client.send("OpenDoc", -1, session_app_id)
    # And with interceptors.
    >>> auth.rpc.interceptors["request"].use(log_req)
    ... rpc_session = auth.rpc(app_id=session_app_id)
    ...
    ... with rpc_session.open() as rpc_client:
    ...     app = rpc_client.send("OpenDoc", -1, session_app_id)
    """

    rest: RestClientInstance
    """
    rest method can be used to make raw calls against Qlik Cloud

    Parameters
    ----------
    app_id: str
    method: str
        HTTP verb default GET
    path: str
        represents the api endpoint ex: "/users/me"
    data: dict, optional
        Dictionary, list of tuples, bytes, or file-like object to send in the body of the Request.
    params: dict, optional
        Dictionary, list of tuples or bytes to send in the query string for the Request.
    headers: dict, optional
        Dictionary of HTTP Headers to send with the Request
    files: dict, optional
        Dictionary of {filename: fileobject} files to multipart upload.

    Attributes
    ----------
    interceptors: Interceptors

    Examples
    ----------
    >>> auth = Auth(Config(host=self.base_url, auth_type=AuthType.APIKey, api_key=self.api_key))
    ... user_me = auth.rest(path="/users/me")
    # And with interceptors.
    >>> auth = Auth(Config(host=self.base_url, auth_type=AuthType.APIKey, api_key=self.api_key))
    ... def log_req(req: requests.Request) -> requests.Request:
    ...     print(req)
    ...     return req
    ...
    ... auth.rpc.interceptors["request"].use(log_req)
    ... app_list = auth.rest(path="/items", params={"resourceType":"app", "limit": 100})
    """

    api_keys: Api_Keys.ApiKeys
    apps: Apps.Apps
    audits: Audits.Audits
    automations: Automations.Automations
    brands: Brands.Brands
    collections: Collections.Collections
    csp_origins: Csp_Origins.CspOrigins
    data_files: Data_Files.DataFiles
    extensions: Extensions.Extensions
    groups: Groups.Groups
    identity_providers: Identity_Providers.IdentityProviders
    items: Items.Items
    licenses: Licenses.Licenses
    notes: Notes.Notes
    oauth_tokens: Oauth_Tokens.OauthTokens
    questions: Questions.Questions
    quotas: Quotas.Quotas
    reload_tasks: Reload_Tasks.ReloadTasks
    reloads: Reloads.Reloads
    roles: Roles.Roles
    spaces: Spaces.Spaces
    tenants: Tenants.Tenants
    themes: Themes.Themes
    transports: Transports.Transports
    users: Users.Users
    web_integrations: Web_Integrations.WebIntegrations
    webhooks: Webhooks.Webhooks

    apikeys: Api_Keys.ApiKeys
    "attribute Qlik.apikeys deprecated"
    csporigins: Csp_Origins.CspOrigins
    "attribute Qlik.csporigins deprecated"
    datafiles: Data_Files.DataFiles
    "attribute Qlik.datafiles deprecated"
    identityproviders: Identity_Providers.IdentityProviders
    "attribute Qlik.identityproviders deprecated"
    oauth_tokens: Oauth_Tokens.OauthTokens
    "attribute Qlik.oauth_tokens deprecated"
    webintegrations: Web_Integrations.WebIntegrations
    "attribute Qlik.webintegrations deprecated"

    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config=config)
        self.rest = self.auth.rest
        self.rpc = self.auth.rpc
        # deprecated properties
        self.apikeys = Api_Keys.ApiKeys(config=config)
        self.csporigins = Csp_Origins.CspOrigins(config=config)
        self.datafiles = Data_Files.DataFiles(config=config)
        self.identityproviders = Identity_Providers.IdentityProviders(config=config)
        self.oauth_tokens = Oauth_Tokens.OauthTokens(config=config)
        self.webintegrations = Web_Integrations.WebIntegrations(config=config)

        self.api_keys = Api_Keys.ApiKeys(config=config)
        self.apps = Apps.Apps(config=config)
        self.audits = Audits.Audits(config=config)
        self.automations = Automations.Automations(config=config)
        self.brands = Brands.Brands(config=config)
        self.collections = Collections.Collections(config=config)
        self.csp_origins = Csp_Origins.CspOrigins(config=config)
        self.data_files = Data_Files.DataFiles(config=config)
        self.extensions = Extensions.Extensions(config=config)
        self.groups = Groups.Groups(config=config)
        self.identity_providers = Identity_Providers.IdentityProviders(config=config)
        self.items = Items.Items(config=config)
        self.licenses = Licenses.Licenses(config=config)
        self.notes = Notes.Notes(config=config)
        self.oauth_tokens = Oauth_Tokens.OauthTokens(config=config)
        self.questions = Questions.Questions(config=config)
        self.quotas = Quotas.Quotas(config=config)
        self.reload_tasks = Reload_Tasks.ReloadTasks(config=config)
        self.reloads = Reloads.Reloads(config=config)
        self.roles = Roles.Roles(config=config)
        self.spaces = Spaces.Spaces(config=config)
        self.tenants = Tenants.Tenants(config=config)
        self.themes = Themes.Themes(config=config)
        self.transports = Transports.Transports(config=config)
        self.users = Users.Users(config=config)
        self.web_integrations = Web_Integrations.WebIntegrations(config=config)
        self.webhooks = Webhooks.Webhooks(config=config)
