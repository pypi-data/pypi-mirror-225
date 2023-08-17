# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class Role:
    """

    Attributes
    ----------
    createdAt: str
      The timestamp for when the role was created.
    description: str
      Descriptive text for the role.
    id: str
      The unique identifier for the role.
    lastUpdatedAt: str
      The timestamp for when the role was last updated.
    level: Literal["admin", "user"]
      The level of access associated to the role.
    links: RoleLinks
      Contains links for the role.
    name: str
      The name of the role.
    permissions: list[str]
      An array of permissions associated with the role.
    tenantId: str
      The tenant unique identifier associated with the given Role.
    type: Literal["default"]
      The type of role.
    """

    createdAt: str = None
    description: str = None
    id: str = None
    lastUpdatedAt: str = None
    level: Literal["admin", "user"] = None
    links: RoleLinks = None
    name: str = None
    permissions: list[str] = None
    tenantId: str = None
    type: Literal["default"] = None

    def __init__(self_, **kvargs):
        if "createdAt" in kvargs and kvargs["createdAt"] is not None:
            self_.createdAt = kvargs["createdAt"]
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "lastUpdatedAt" in kvargs and kvargs["lastUpdatedAt"] is not None:
            self_.lastUpdatedAt = kvargs["lastUpdatedAt"]
        if "level" in kvargs and kvargs["level"] is not None:
            self_.level = kvargs["level"]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == Role.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = RoleLinks(**kvargs["links"])
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "permissions" in kvargs and kvargs["permissions"] is not None:
            self_.permissions = kvargs["permissions"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            self_.tenantId = kvargs["tenantId"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Links:
    """
    Contains pagination links

    Attributes
    ----------
    next: LinksNext
      Link to the next page of items
    prev: LinksPrev
      Link to the previous page of items
    self: LinksSelf
      Link to the current page of items
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
    Link to the next page of items

    Attributes
    ----------
    href: str
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
    Link to the previous page of items

    Attributes
    ----------
    href: str
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
    Link to the current page of items

    Attributes
    ----------
    href: str
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
class ListRolesResult:
    """

    Attributes
    ----------
    data: list[Role]
      An array of roles.
    links: Links
      Contains pagination links
    totalResults: int
      Indicates the total number of matching documents. Will only be returned if the query parameter "totalResults" is true.
    """

    data: list[Role] = None
    links: Links = None
    totalResults: int = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]" == ListRolesResult.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [Role(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == ListRolesResult.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = Links(**kvargs["links"])
        if "totalResults" in kvargs and kvargs["totalResults"] is not None:
            self_.totalResults = kvargs["totalResults"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class RoleLinks:
    """
    Contains links for the role.

    Attributes
    ----------
    self: RoleLinksSelf
    """

    self: RoleLinksSelf = None

    def __init__(self_, **kvargs):
        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == RoleLinks.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = RoleLinksSelf(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class RoleLinksSelf:
    """

    Attributes
    ----------
    href: str
      Link to the role.
    """

    href: str = None

    def __init__(self_, **kvargs):
        if "href" in kvargs and kvargs["href"] is not None:
            self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Roles:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get(self, id: str) -> Role:
        """
        Get role by ID
        Returns the requested role.

        Parameters
        ----------
        id: str
          The role's unique identifier
        """
        response = self.auth.rest(
            path="/roles/{id}".replace("{id}", id),
            method="GET",
            params={},
            data=None,
        )
        obj = Role(**response.json())
        obj.auth = self.auth
        return obj

    def get_roles(
        self,
        filter: str = None,
        limit: float = 20,
        next: str = None,
        prev: str = None,
        sort: str = None,
        totalResults: bool = None,
    ) -> ListableResource[Role]:
        """
        List roles
        Returns a list of roles using cursor-based pagination.

        Parameters
        ----------
        filter: str = None
          The advanced filtering to use for the query. Refer to RFC 7644 https://datatracker.ietf.org/doc/rfc7644/ for the syntax. All conditional statements within this query parameter are case insensitive.
        limit: float = 20
          The number of roles to retrieve.
        next: str = None
          The next page cursor.
        prev: str = None
          The previous page cursor.
        sort: str = None
          Optional resource field name to sort on, eg. name. Can be prefixed with +/- to determine order, defaults to (+) ascending.
        totalResults: bool = None
          Determines wether to return a count of the total records matched in the query. Defaults to false.
        """
        query_params = {}
        if filter is not None:
            query_params["filter"] = filter
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if sort is not None:
            query_params["sort"] = sort
        if totalResults is not None:
            query_params["totalResults"] = totalResults
        response = self.auth.rest(
            path="/roles",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Role,
            auth=self.auth,
            path="/roles",
            query_params=query_params,
        )
