# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class IDP:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class IDPArray:
    """

    Attributes
    ----------
    data: list[IDP]
      An array of IdPs.
    links: Links
      Contains pagination links.
    """

    data: list[IDP] = None
    links: Links = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]" == IDPArray.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [IDP(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == IDPArray.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = Links(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class IDPMeta:
    """

    Attributes
    ----------
    upgradeSubscriptionLink: str
      A link to direct you to where you can upgrade your trial or manage your subscriptions. Only available if the default identity provider is used (no custom interactive identity providers are active).
    userPortalLink: str
      A link to direct you to where you can manage your Qlik account. Only available if the default identity provider is used (no custom interactive identity providers are active).
    """

    upgradeSubscriptionLink: str = None
    userPortalLink: str = None

    def __init__(self_, **kvargs):
        if (
            "upgradeSubscriptionLink" in kvargs
            and kvargs["upgradeSubscriptionLink"] is not None
        ):
            self_.upgradeSubscriptionLink = kvargs["upgradeSubscriptionLink"]
        if "userPortalLink" in kvargs and kvargs["userPortalLink"] is not None:
            self_.userPortalLink = kvargs["userPortalLink"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class IDPPatchSchema:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class IDPPostSchema:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class IDPsStatus:
    """

    Attributes
    ----------
    active_interactive_idps_count: float
      The number of active interactive IdPs.
    idps_metadata: list[IDPsStatusIdpsMetadata]
      A list of IdP metadata.
    """

    active_interactive_idps_count: float = None
    idps_metadata: list[IDPsStatusIdpsMetadata] = None

    def __init__(self_, **kvargs):
        if (
            "active_interactive_idps_count" in kvargs
            and kvargs["active_interactive_idps_count"] is not None
        ):
            self_.active_interactive_idps_count = kvargs[
                "active_interactive_idps_count"
            ]
        if "idps_metadata" in kvargs and kvargs["idps_metadata"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == IDPsStatus.__annotations__["idps_metadata"]
                for e in kvargs["idps_metadata"]
            ):
                self_.idps_metadata = kvargs["idps_metadata"]
            else:
                self_.idps_metadata = [
                    IDPsStatusIdpsMetadata(**e) for e in kvargs["idps_metadata"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class IDPsStatusIdpsMetadata:
    """

    Attributes
    ----------
    active: bool
      Indicates whether the IdP is available for use.
    interactive: bool
      Indicates whether the IdP is meant for interactive login.
    provider: Literal["auth0", "okta", "qlik", "generic", "salesforce", "keycloak", "adfs", "external", "azureAD"]
      The identity provider to be used. If protocol is `OIDC`, the valid values are `auth0`, `okta`, `generic`, `salesforce`, `keycloak`, `adfs`, and `azureAD`. If protocol is `jwtAuth`, the valid value is `external`.
    """

    active: bool = None
    interactive: bool = None
    provider: Literal[
        "auth0",
        "okta",
        "qlik",
        "generic",
        "salesforce",
        "keycloak",
        "adfs",
        "external",
        "azureAD",
    ] = None

    def __init__(self_, **kvargs):
        if "active" in kvargs and kvargs["active"] is not None:
            self_.active = kvargs["active"]
        if "interactive" in kvargs and kvargs["interactive"] is not None:
            self_.interactive = kvargs["interactive"]
        if "provider" in kvargs and kvargs["provider"] is not None:
            self_.provider = kvargs["provider"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Links:
    """
    Contains pagination links.

    Attributes
    ----------
    next: LinksNext
    prev: LinksPrev
    self: LinksSelf
    """

    next: LinksNext = None
    prev: LinksPrev = None
    self: LinksSelf = None

    def __init__(self_, **kvargs):
        if "next" in kvargs and kvargs["next"] is not None:
            if type(kvargs["next"]).__name__ == Links.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = LinksNext(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if type(kvargs["prev"]).__name__ == Links.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = LinksPrev(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == Links.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = LinksSelf(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LinksNext:
    """

    Attributes
    ----------
    href: str
      Link to the next page of items.
    """

    href: str = None

    def __init__(self_, **kvargs):
        if "href" in kvargs and kvargs["href"] is not None:
            self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LinksPrev:
    """

    Attributes
    ----------
    href: str
      Link to the previous page of items.
    """

    href: str = None

    def __init__(self_, **kvargs):
        if "href" in kvargs and kvargs["href"] is not None:
            self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LinksSelf:
    """

    Attributes
    ----------
    href: str
      Link to the current page of items.
    """

    href: str = None

    def __init__(self_, **kvargs):
        if "href" in kvargs and kvargs["href"] is not None:
            self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class IdentityProviders:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_well_known_metadata_json(self) -> object:
        """
        Returns identity providers' metadata
        This endpoint retrieves identity providers' metadata.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/identity-providers/.well-known/metadata.json",
            method="GET",
            params={},
            data=None,
        )
        return response.json()

    def get_me_meta(self) -> IDPMeta:
        """
        Returns the active interactive IdP metadata
        This endpoint retrieves IdP metadata.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/identity-providers/me/meta",
            method="GET",
            params={},
            data=None,
        )
        obj = IDPMeta(**response.json())
        obj.auth = self.auth
        return obj

    def get_status(self) -> IDPsStatus:
        """
        Returns the current status of IdP configurations
        This endpoint retrieves the status of IdP configurations. Requires TenantAdmin role.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/identity-providers/status",
            method="GET",
            params={},
            data=None,
        )
        obj = IDPsStatus(**response.json())
        obj.auth = self.auth
        return obj

    def delete(self, id: str) -> None:
        """
        Deletes the IdP with the specified ID
        This endpoint deletes an identity provider from the service. It returns a valid 204 when the IdP is deleted. Only a user with the role of TenantAdmin and tenant access can delete an associated IdP. Edge-auth service can also delete.

        Parameters
        ----------
        id: str
          The identity provider ID.
        """
        self.auth.rest(
            path="/identity-providers/{id}".replace("{id}", id),
            method="DELETE",
            params={},
            data=None,
        )

    def get(self, id: str) -> IDP:
        """
        Returns the IdP with the specified ID
        This endpoint is used to retrieve an identity provider from the service. It returns a valid 200 OK response when the IdP exists and the user (TenantAdmin) or service (edge-auth) is authorized to view the contents. Additionally, returns a header "QLIK-IDP-POPTS" (A unique string representing a hash of the current configuration being tested). It returns a 404 Not Found if the criteria is not met.

        Parameters
        ----------
        id: str
          The identity provider ID.
        """
        response = self.auth.rest(
            path="/identity-providers/{id}".replace("{id}", id),
            method="GET",
            params={},
            data=None,
        )
        obj = IDP(**response.json())
        obj.auth = self.auth
        return obj

    def patch(self, id: str, data: IDPPatchSchema = None) -> None:
        """
        Updates the IdP with the specified ID
        This endpoint patches an identity provider from the service. It returns a valid 204 when the IdP is patched. Only an edge-auth service request or a user with the role of TenantAdmin can patch an associated IdP. Partial failure is treated as complete failure and returns an error.

        Parameters
        ----------
        id: str
          The identity provider ID.
        data: IDPPatchSchema = None
          Attributes that the user wants to patially update for an identity provider resource.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        self.auth.rest(
            path="/identity-providers/{id}".replace("{id}", id),
            method="PATCH",
            params={},
            data=data,
        )

    def get_identity_providers(
        self, active: bool = None, limit: float = 20, next: str = None, prev: str = None
    ) -> ListableResource[IDP]:
        """
        Retrieves one or more IdPs for a specified tenantId.
        This endpoint retrieves one or more identity providers from the service. The tenantID in the JWT will be used to fetch the identity provider.

        Parameters
        ----------
        active: bool = None
          If provided, filters the results by the active field.
        limit: float = 20
          The number of IdP entries to retrieve.
        next: str = None
          The next page cursor.
        prev: str = None
          The previous page cursor.
        """
        query_params = {}
        if active is not None:
            query_params["active"] = active
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        response = self.auth.rest(
            path="/identity-providers",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=IDP,
            auth=self.auth,
            path="/identity-providers",
            query_params=query_params,
        )

    def create(self, data: IDPPostSchema = None) -> IDP:
        """
        Creates a new IdP
        This endpoint creates an identity provider resource. It returns a 201 Created when creation is successful with a header "QLIK-IDP-POPTS" (A unique string representing a hash of the current configuration being tested), returns a 403 Forbidden for a non TenantAdmin user JWT or if the tenantID in the JWT does not match with any of the tenantIDs in the payload. An IdP can be created with Pending Options or options depending whether the IdP is interactive or not.

        Parameters
        ----------
        data: IDPPostSchema = None
          Attributes that the user wants to set for a new identity provider resource.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/identity-providers",
            method="POST",
            params={},
            data=data,
        )
        obj = IDP(**response.json())
        obj.auth = self.auth
        return obj
