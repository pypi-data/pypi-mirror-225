# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import List, Literal

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class WebIntegration:
    """
    A web integration object.

    Attributes
    ----------
    created: str
      The time the web integration was created.
    createdBy: str
      The user that created the web integration.
    id: str
      The unique web integration identifier.
    lastUpdated: str
      The time the web integration was last updated.
    name: str
      The name of the web integration.
    tenantId: str
      The tenant that the web integration belongs to.
    validOrigins: list[str]
      The origins that are allowed to make requests to the tenant.
    """

    created: str = None
    createdBy: str = None
    id: str = None
    lastUpdated: str = None
    name: str = None
    tenantId: str = None
    validOrigins: list[str] = None

    def __init__(self_, **kvargs):
        if "created" in kvargs and kvargs["created"] is not None:
            self_.created = kvargs["created"]
        if "createdBy" in kvargs and kvargs["createdBy"] is not None:
            self_.createdBy = kvargs["createdBy"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "lastUpdated" in kvargs and kvargs["lastUpdated"] is not None:
            self_.lastUpdated = kvargs["lastUpdated"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            self_.tenantId = kvargs["tenantId"]
        if "validOrigins" in kvargs and kvargs["validOrigins"] is not None:
            self_.validOrigins = kvargs["validOrigins"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def delete(self) -> None:
        """
        Delete web integration by ID
        Deletes a single web integration by ID.

        Parameters
        ----------
        """
        self.auth.rest(
            path="/web-integrations/{id}".replace("{id}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def patch(self, data: WebIntegrationPatchSchema) -> None:
        """
        Update web integration by ID
        Updates a single web integration by ID.

        Parameters
        ----------
        data: WebIntegrationPatchSchema
          Properties that the user wants to update for the web integration.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        self.auth.rest(
            path="/web-integrations/{id}".replace("{id}", self.id),
            method="PATCH",
            params={},
            data=data,
        )


@dataclass
class WebIntegrationPatch:
    """
    A JSON Patch document as defined in http://tools.ietf.org/html/rfc6902.

    Attributes
    ----------
    op: Literal["replace"]
      The operation to be performed.
    path: Literal["/name", "/validOrigins"]
      A JSON Pointer.
    value: str
      New value to be used for this operation.
    """

    op: Literal["replace"] = None
    path: Literal["/name", "/validOrigins"] = None
    value: str = None

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


@dataclass
class WebIntegrationPatchSchema(List["WebIntegrationPatch"]):
    """

    Attributes
    ----------
    """

    def __init__(self_, elements):
        for e in elements:
            self_.append(WebIntegrationPatch(**e))


@dataclass
class WebIntegrationPost:
    """
    The creation of a web integration response.

    Attributes
    ----------
    created: str
      The time the web integration was created.
    createdBy: str
      The user that created the web integration.
    id: str
      The unique web integration identifier.
    lastUpdated: str
      The time the web integration was last updated.
    links: WebIntegrationPostLinks
      Pagination links
    name: str
      The name of the newly created web integration.
    tenantId: str
      The tenant that the web integration belongs to.
    validOrigins: list[str]
      The origins that are allowed to make requests to the tenant.
    """

    created: str = None
    createdBy: str = None
    id: str = None
    lastUpdated: str = None
    links: WebIntegrationPostLinks = None
    name: str = None
    tenantId: str = None
    validOrigins: list[str] = None

    def __init__(self_, **kvargs):
        if "created" in kvargs and kvargs["created"] is not None:
            self_.created = kvargs["created"]
        if "createdBy" in kvargs and kvargs["createdBy"] is not None:
            self_.createdBy = kvargs["createdBy"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "lastUpdated" in kvargs and kvargs["lastUpdated"] is not None:
            self_.lastUpdated = kvargs["lastUpdated"]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == WebIntegrationPost.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = WebIntegrationPostLinks(**kvargs["links"])
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            self_.tenantId = kvargs["tenantId"]
        if "validOrigins" in kvargs and kvargs["validOrigins"] is not None:
            self_.validOrigins = kvargs["validOrigins"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class WebIntegrationPostLinks:
    """
    Pagination links

    Attributes
    ----------
    self: WebIntegrationPostLinksSelf
      Link information for current page.
    """

    self: WebIntegrationPostLinksSelf = None

    def __init__(self_, **kvargs):
        if "self" in kvargs and kvargs["self"] is not None:
            if (
                type(kvargs["self"]).__name__
                == WebIntegrationPostLinks.__annotations__["self"]
            ):
                self_.self = kvargs["self"]
            else:
                self_.self = WebIntegrationPostLinksSelf(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class WebIntegrationPostLinksSelf:
    """
    Link information for current page.

    Attributes
    ----------
    href: str
      URL to the current page of records.
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
class WebIntegrationPostSchema:
    """

    Attributes
    ----------
    name: str
      The name of the web integration to create.
    validOrigins: list[str]
      The origins that are allowed to make requests to the tenant.
    """

    name: str = None
    validOrigins: list[str] = None

    def __init__(self_, **kvargs):
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "validOrigins" in kvargs and kvargs["validOrigins"] is not None:
            self_.validOrigins = kvargs["validOrigins"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class WebIntegrationsClass:
    """
    An array of web integration objects.

    Attributes
    ----------
    data: list[WebIntegration]
      Properties of web integrations in a given tenant.
    links: WebIntegrationsLinks
      Pagination links
    """

    data: list[WebIntegration] = None
    links: WebIntegrationsLinks = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == WebIntegrationsClass.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [WebIntegration(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == WebIntegrationsClass.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = WebIntegrationsLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class WebIntegrationsLinks:
    """
    Pagination links

    Attributes
    ----------
    next: WebIntegrationsLinksNext
      Link information for next page.
    prev: WebIntegrationsLinksPrev
      Link information for previous page.
    self: WebIntegrationsLinksSelf
      Link information for current page.
    """

    next: WebIntegrationsLinksNext = None
    prev: WebIntegrationsLinksPrev = None
    self: WebIntegrationsLinksSelf = None

    def __init__(self_, **kvargs):
        if "next" in kvargs and kvargs["next"] is not None:
            if (
                type(kvargs["next"]).__name__
                == WebIntegrationsLinks.__annotations__["next"]
            ):
                self_.next = kvargs["next"]
            else:
                self_.next = WebIntegrationsLinksNext(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if (
                type(kvargs["prev"]).__name__
                == WebIntegrationsLinks.__annotations__["prev"]
            ):
                self_.prev = kvargs["prev"]
            else:
                self_.prev = WebIntegrationsLinksPrev(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if (
                type(kvargs["self"]).__name__
                == WebIntegrationsLinks.__annotations__["self"]
            ):
                self_.self = kvargs["self"]
            else:
                self_.self = WebIntegrationsLinksSelf(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class WebIntegrationsLinksNext:
    """
    Link information for next page.

    Attributes
    ----------
    href: str
      URL to the next page of records.
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
class WebIntegrationsLinksPrev:
    """
    Link information for previous page.

    Attributes
    ----------
    href: str
      URL to the previous page of records.
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
class WebIntegrationsLinksSelf:
    """
    Link information for current page.

    Attributes
    ----------
    href: str
      URL to the current page of records.
    """

    href: str = None

    def __init__(self_, **kvargs):
        if "href" in kvargs and kvargs["href"] is not None:
            self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class WebIntegrations:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get(self, id: str) -> WebIntegration:
        """
        Get web integration by ID
        Retrieves a single web integration by ID.

        Parameters
        ----------
        id: str
          The ID of the web integration to retrieve.
        """
        response = self.auth.rest(
            path="/web-integrations/{id}".replace("{id}", id),
            method="GET",
            params={},
            data=None,
        )
        obj = WebIntegration(**response.json())
        obj.auth = self.auth
        return obj

    def get_web_integrations(
        self,
        endingBefore: str = None,
        limit: float = 10,
        sort: Literal["name", "+name", "-name"] = "+name",
        startingAfter: str = None,
        tenantId: str = None,
    ) -> ListableResource[WebIntegration]:
        """
        List web integrations
        Retrieves web integrations matching the query.

        Parameters
        ----------
        endingBefore: str = None
          The target web integration ID to start looking before for web integrations. Cannot be used in conjunction with startingAfter.
        limit: float = 10
          The number of web integration entries to retrieve.
        sort: Literal["name", "+name", "-name"] = "+name"
          The field to sort by. Prefix with +/- to indicate ascending/descending order.
        startingAfter: str = None
          The target web integration ID to start looking after for web integrations. Cannot be used in conjunction with endingBefore.
        tenantId: str = None
          The tenant ID to filter by.
        """
        query_params = {}
        if endingBefore is not None:
            query_params["endingBefore"] = endingBefore
        if limit is not None:
            query_params["limit"] = limit
        if sort is not None:
            query_params["sort"] = sort
        if startingAfter is not None:
            query_params["startingAfter"] = startingAfter
        if tenantId is not None:
            query_params["tenantId"] = tenantId
        response = self.auth.rest(
            path="/web-integrations",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=WebIntegration,
            auth=self.auth,
            path="/web-integrations",
            query_params=query_params,
        )

    def create(self, data: WebIntegrationPostSchema) -> WebIntegrationPost:
        """
        Create web integration
        Creates a web integration.

        Parameters
        ----------
        data: WebIntegrationPostSchema
          Properties that the user wants to set for the web integration.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/web-integrations",
            method="POST",
            params={},
            data=data,
        )
        obj = WebIntegrationPost(**response.json())
        obj.auth = self.auth
        return obj
