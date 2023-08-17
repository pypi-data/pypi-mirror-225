# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import List, Literal

from ..auth import Auth, Config


@dataclass
class Tenant:
    """

    Attributes
    ----------
    autoAssignCreateSharedSpacesRoleToProfessionals: bool
    autoAssignDataServicesContributorRoleToProfessionals: bool
    autoAssignPrivateAnalyticsContentCreatorRoleToProfessionals: bool
    created: str
      The timestamp for when the tenant record was created (1970-01-01T00:00:00.001Z for static tenants).
    createdByUser: str
      The user ID who created the tenant.
    datacenter: str
      The datacenter where the tenant is located.
    enableAnalyticCreation: bool
    hostnames: list[str]
      List of case insensitive hostnames that are mapped to the tenant. The first record maps to the display name and the subsequent entries are aliases.
    id: str
      The unique tenant identifier.
    lastUpdated: str
      The timestamp for when the tenant record was last updated (1970-01-01T00:00:00.001Z for static tenants).
    links: TenantLinks
    name: str
      The display name of the tenant.
    status: Literal["active", "disabled", "deleted"]
      The status of the tenant.
    """

    autoAssignCreateSharedSpacesRoleToProfessionals: bool = True
    autoAssignDataServicesContributorRoleToProfessionals: bool = True
    autoAssignPrivateAnalyticsContentCreatorRoleToProfessionals: bool = True
    created: str = None
    createdByUser: str = None
    datacenter: str = None
    enableAnalyticCreation: bool = None
    hostnames: list[str] = None
    id: str = None
    lastUpdated: str = None
    links: TenantLinks = None
    name: str = None
    status: Literal["active", "disabled", "deleted"] = None

    def __init__(self_, **kvargs):
        if (
            "autoAssignCreateSharedSpacesRoleToProfessionals" in kvargs
            and kvargs["autoAssignCreateSharedSpacesRoleToProfessionals"] is not None
        ):
            self_.autoAssignCreateSharedSpacesRoleToProfessionals = kvargs[
                "autoAssignCreateSharedSpacesRoleToProfessionals"
            ]
        if (
            "autoAssignDataServicesContributorRoleToProfessionals" in kvargs
            and kvargs["autoAssignDataServicesContributorRoleToProfessionals"]
            is not None
        ):
            self_.autoAssignDataServicesContributorRoleToProfessionals = kvargs[
                "autoAssignDataServicesContributorRoleToProfessionals"
            ]
        if (
            "autoAssignPrivateAnalyticsContentCreatorRoleToProfessionals" in kvargs
            and kvargs["autoAssignPrivateAnalyticsContentCreatorRoleToProfessionals"]
            is not None
        ):
            self_.autoAssignPrivateAnalyticsContentCreatorRoleToProfessionals = kvargs[
                "autoAssignPrivateAnalyticsContentCreatorRoleToProfessionals"
            ]
        if "created" in kvargs and kvargs["created"] is not None:
            self_.created = kvargs["created"]
        if "createdByUser" in kvargs and kvargs["createdByUser"] is not None:
            self_.createdByUser = kvargs["createdByUser"]
        if "datacenter" in kvargs and kvargs["datacenter"] is not None:
            self_.datacenter = kvargs["datacenter"]
        if (
            "enableAnalyticCreation" in kvargs
            and kvargs["enableAnalyticCreation"] is not None
        ):
            self_.enableAnalyticCreation = kvargs["enableAnalyticCreation"]
        if "hostnames" in kvargs and kvargs["hostnames"] is not None:
            self_.hostnames = kvargs["hostnames"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "lastUpdated" in kvargs and kvargs["lastUpdated"] is not None:
            self_.lastUpdated = kvargs["lastUpdated"]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == Tenant.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = TenantLinks(**kvargs["links"])
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "status" in kvargs and kvargs["status"] is not None:
            self_.status = kvargs["status"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def patch(self, data: TenantPatchSchema) -> None:
        """
        Update a tenant by id.

        Parameters
        ----------
        data: TenantPatchSchema
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        self.auth.rest(
            path="/tenants/{tenantId}".replace("{tenantId}", self.id),
            method="PATCH",
            params={},
            data=data,
        )


@dataclass
class TenantCreationRequest:
    """

    Attributes
    ----------
    datacenter: str
      The datacenter where the tenant is located.
    hostnames: list[str]
      The hostnames of the created tenant. Can only create with a single entry that lines up wtih the tenant name.
    licenseKey: str
      The signed license key of the license that will be associated with the created tenant.
    name: str
      The name of the created tenant, provided by the onboarding service.
    """

    datacenter: str = None
    hostnames: list[str] = None
    licenseKey: str = None
    name: str = None

    def __init__(self_, **kvargs):
        if "datacenter" in kvargs and kvargs["datacenter"] is not None:
            self_.datacenter = kvargs["datacenter"]
        if "hostnames" in kvargs and kvargs["hostnames"] is not None:
            self_.hostnames = kvargs["hostnames"]
        if "licenseKey" in kvargs and kvargs["licenseKey"] is not None:
            self_.licenseKey = kvargs["licenseKey"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TenantLinks:
    """

    Attributes
    ----------
    self: TenantLinksSelf
      A link to this tenant.
    """

    self: TenantLinksSelf = None

    def __init__(self_, **kvargs):
        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == TenantLinks.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = TenantLinksSelf(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TenantLinksSelf:
    """
    A link to this tenant.

    Attributes
    ----------
    href: str
      URL that defines the resource.
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
class TenantPatchSchema(List["TenantPatchSchemaElement"]):
    """

    Attributes
    ----------
    """

    def __init__(self_, elements):
        for e in elements:
            self_.append(TenantPatchSchemaElement(**e))


@dataclass
class TenantPatchSchemaElement:
    """
    A JSON Patch document as defined in http://tools.ietf.org/html/rfc6902.

    Attributes
    ----------
    op: Literal["replace"]
      The operation to be performed.
    path: Literal["/name", "/hostnames/1", "/autoAssignCreateSharedSpacesRoleToProfessionals", "/autoAssignPrivateAnalyticsContentCreatorRoleToProfessionals", "/autoAssignDataServicesContributorRoleToProfessionals", "/enableAnalyticCreation"]
      A JSON Pointer value that references a location within the target document where the operation is performed.
    value: object
      The value to be used for this operation.
    """

    op: Literal["replace"] = None
    path: Literal[
        "/name",
        "/hostnames/1",
        "/autoAssignCreateSharedSpacesRoleToProfessionals",
        "/autoAssignPrivateAnalyticsContentCreatorRoleToProfessionals",
        "/autoAssignDataServicesContributorRoleToProfessionals",
        "/enableAnalyticCreation",
    ] = None
    value: str | bool = None

    def __init__(self_, **kvargs):
        if "op" in kvargs and kvargs["op"] is not None:
            self_.op = kvargs["op"]
        if "path" in kvargs and kvargs["path"] is not None:
            self_.path = kvargs["path"]
        if "value" in kvargs and kvargs["value"] is not None:
            self_.value = kvargs["value"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Tenants:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_me(self) -> Tenant:
        """
        Redirects to current tenant.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/tenants/me",
            method="GET",
            params={},
            data=None,
        )
        obj = Tenant(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, tenantId: str) -> Tenant:
        """
        Retrieve a single tenant by id.

        Parameters
        ----------
        tenantId: str
          The id of the tenant to retrieve
        """
        response = self.auth.rest(
            path="/tenants/{tenantId}".replace("{tenantId}", tenantId),
            method="GET",
            params={},
            data=None,
        )
        obj = Tenant(**response.json())
        obj.auth = self.auth
        return obj

    def create(self, data: TenantCreationRequest) -> Tenant:
        """
        Creates a Tenant

        Parameters
        ----------
        data: TenantCreationRequest
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/tenants",
            method="POST",
            params={},
            data=data,
        )
        obj = Tenant(**response.json())
        obj.auth = self.auth
        return obj
