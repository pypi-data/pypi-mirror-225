# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

import warnings
from dataclasses import asdict, dataclass
from typing import List, Literal

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class Space:
    """
    A space is a security context simplifying the management of access control by allowing users to control it on the containers instead of on the resources themselves.

    Attributes
    ----------
    createdAt: str
      The date and time when the space was created.
    createdBy: str
      The ID of the user who created the space.
    description: str
      The description of the space. Personal spaces do not have a description.
    id: str
      A unique identifier for the space, for example, 62716f4b39b865ece543cd45.
    links: SpaceLinks
    meta: SpaceMeta
      Information about the space settings.
    name: str
      The name of the space. Personal spaces do not have a name.
    ownerId: str
      The ID for the space owner.
    tenantId: str
      The ID for the tenant, for example, xqGQ0k66vSR8f9G7J-vYtHZQkiYrCpct.
    type: Literal["shared", "managed", "data"]
      The type of space such as shared, managed, and so on.
    updatedAt: str
      The date and time when the space was updated.
    """

    createdAt: str = None
    createdBy: str = None
    description: str = None
    id: str = None
    links: SpaceLinks = None
    meta: SpaceMeta = None
    name: str = None
    ownerId: str = None
    tenantId: str = None
    type: Literal["shared", "managed", "data"] = None
    updatedAt: str = None

    def __init__(self_, **kvargs):
        if "createdAt" in kvargs and kvargs["createdAt"] is not None:
            self_.createdAt = kvargs["createdAt"]
        if "createdBy" in kvargs and kvargs["createdBy"] is not None:
            self_.createdBy = kvargs["createdBy"]
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == Space.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = SpaceLinks(**kvargs["links"])
        if "meta" in kvargs and kvargs["meta"] is not None:
            if type(kvargs["meta"]).__name__ == Space.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = SpaceMeta(**kvargs["meta"])
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "ownerId" in kvargs and kvargs["ownerId"] is not None:
            self_.ownerId = kvargs["ownerId"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            self_.tenantId = kvargs["tenantId"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        if "updatedAt" in kvargs and kvargs["updatedAt"] is not None:
            self_.updatedAt = kvargs["updatedAt"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def delete_assignment(self, assignmentId: str) -> None:
        """
        Deletes an assignment.

        Parameters
        ----------
        assignmentId: str
          The ID of the assignment to delete.
        """
        self.auth.rest(
            path="/spaces/{spaceId}/assignments/{assignmentId}".replace(
                "{assignmentId}", assignmentId
            ).replace("{spaceId}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def get_assignment(self, assignmentId: str) -> Assignment:
        """
        Retrieves a single assignment by ID.

        Parameters
        ----------
        assignmentId: str
          The ID of the assignment to retrieve.
        """
        response = self.auth.rest(
            path="/spaces/{spaceId}/assignments/{assignmentId}".replace(
                "{assignmentId}", assignmentId
            ).replace("{spaceId}", self.id),
            method="GET",
            params={},
            data=None,
        )
        obj = Assignment(**response.json())
        obj.auth = self.auth
        return obj

    def set_assignment(self, assignmentId: str, data: AssignmentUpdate) -> Assignment:
        """
        Updates a single assignment by ID. The complete list of roles must be provided.

        Parameters
        ----------
        assignmentId: str
          The ID of the assignment to update.
        data: AssignmentUpdate
          Attributes that the user wants to update for the specified assignment.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/spaces/{spaceId}/assignments/{assignmentId}".replace(
                "{assignmentId}", assignmentId
            ).replace("{spaceId}", self.id),
            method="PUT",
            params={},
            data=data,
        )
        obj = Assignment(**response.json())
        obj.auth = self.auth
        return obj

    def get_assignments(
        self, limit: int = 10, next: str = None, prev: str = None
    ) -> ListableResource[Assignment]:
        """
        Retrieves the assignments of the space matching the query.

        Parameters
        ----------
        limit: int = 10
          Maximum number of assignments to return.
        next: str = None
          The next page cursor. Next links make use of this.
        prev: str = None
          The previous page cursor. Previous links make use of this.
        """
        query_params = {}
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        response = self.auth.rest(
            path="/spaces/{spaceId}/assignments".replace("{spaceId}", self.id),
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Assignment,
            auth=self.auth,
            path="/spaces/{spaceId}/assignments".replace("{spaceId}", self.id),
            query_params=query_params,
        )

    def create_assignment(self, data: AssignmentCreate) -> Assignment:
        """
        Creates an assignment.

        Parameters
        ----------
        data: AssignmentCreate
          Attributes that the user wants to set for the assignment for the space.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/spaces/{spaceId}/assignments".replace("{spaceId}", self.id),
            method="POST",
            params={},
            data=data,
        )
        obj = Assignment(**response.json())
        obj.auth = self.auth
        return obj

    def delete(self) -> None:
        """
        Deletes a space.

        Parameters
        ----------
        """
        self.auth.rest(
            path="/spaces/{spaceId}".replace("{spaceId}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def patch(self, data: SpacePatch) -> Space:
        """
        Patches (updates) a space (partially).

        Parameters
        ----------
        data: SpacePatch
          Attribute that the user wants to patch (update) for the specified space.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/spaces/{spaceId}".replace("{spaceId}", self.id),
            method="PATCH",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self

    def set(self, data: SpaceUpdate) -> Space:
        """
        Updates a space.

        Parameters
        ----------
        data: SpaceUpdate
          Attributes that the user wants to update for the specified space.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/spaces/{spaceId}".replace("{spaceId}", self.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self


@dataclass
class Assignment:
    """

    Attributes
    ----------
    assigneeId: str
      The userId or groupId based on the type.
    createdAt: str
      The date and time when the space was created.
    createdBy: str
      The ID of the user who created the assignment.
    id: str
    links: AssignmentLinks
    roles: list[str]
      The roles assigned to a user or group. Must not be empty.
    spaceId: str
      The unique identifier for the space.
    tenantId: str
      The unique identifier for the tenant.
    type: Literal["user", "group"]
    updatedAt: str
      The date and time when the space was updated.
    updatedBy: str
      The ID of the user who updated the assignment.
    """

    assigneeId: str = None
    createdAt: str = None
    createdBy: str = None
    id: str = None
    links: AssignmentLinks = None
    roles: list[str] = None
    spaceId: str = None
    tenantId: str = None
    type: Literal["user", "group"] = None
    updatedAt: str = None
    updatedBy: str = None

    def __init__(self_, **kvargs):
        if "assigneeId" in kvargs and kvargs["assigneeId"] is not None:
            self_.assigneeId = kvargs["assigneeId"]
        if "createdAt" in kvargs and kvargs["createdAt"] is not None:
            self_.createdAt = kvargs["createdAt"]
        if "createdBy" in kvargs and kvargs["createdBy"] is not None:
            self_.createdBy = kvargs["createdBy"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == Assignment.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = AssignmentLinks(**kvargs["links"])
        if "roles" in kvargs and kvargs["roles"] is not None:
            self_.roles = kvargs["roles"]
        if "spaceId" in kvargs and kvargs["spaceId"] is not None:
            self_.spaceId = kvargs["spaceId"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            self_.tenantId = kvargs["tenantId"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        if "updatedAt" in kvargs and kvargs["updatedAt"] is not None:
            self_.updatedAt = kvargs["updatedAt"]
        if "updatedBy" in kvargs and kvargs["updatedBy"] is not None:
            self_.updatedBy = kvargs["updatedBy"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentCreate:
    """

    Attributes
    ----------
    assigneeId: str
      The userId or groupId based on the type.
    roles: list[str]
      The roles assigned to the assigneeId.
    type: Literal["user", "group"]
      The type of assignment such as user or group
    """

    assigneeId: str = None
    roles: list[str] = None
    type: Literal["user", "group"] = None

    def __init__(self_, **kvargs):
        if "assigneeId" in kvargs and kvargs["assigneeId"] is not None:
            self_.assigneeId = kvargs["assigneeId"]
        if "roles" in kvargs and kvargs["roles"] is not None:
            self_.roles = kvargs["roles"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentLinks:
    """

    Attributes
    ----------
    self: Link
    space: Link
    """

    self: Link = None
    space: Link = None

    def __init__(self_, **kvargs):
        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == AssignmentLinks.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        if "space" in kvargs and kvargs["space"] is not None:
            if (
                type(kvargs["space"]).__name__
                == AssignmentLinks.__annotations__["space"]
            ):
                self_.space = kvargs["space"]
            else:
                self_.space = Link(**kvargs["space"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentUpdate:
    """

    Attributes
    ----------
    roles: list[str]
      The roles assigned to the assigneeId.
    """

    roles: list[str] = None

    def __init__(self_, **kvargs):
        if "roles" in kvargs and kvargs["roles"] is not None:
            self_.roles = kvargs["roles"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Assignments:
    """

    Attributes
    ----------
    data: list[Assignment]
    links: AssignmentsLinks
    meta: AssignmentsMeta
    """

    data: list[Assignment] = None
    links: AssignmentsLinks = None
    meta: AssignmentsMeta = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]" == Assignments.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [Assignment(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == Assignments.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = AssignmentsLinks(**kvargs["links"])
        if "meta" in kvargs and kvargs["meta"] is not None:
            if type(kvargs["meta"]).__name__ == Assignments.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = AssignmentsMeta(**kvargs["meta"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsLinks:
    """

    Attributes
    ----------
    next: Link
    prev: Link
    self: Link
    """

    next: Link = None
    prev: Link = None
    self: Link = None

    def __init__(self_, **kvargs):
        if "next" in kvargs and kvargs["next"] is not None:
            if (
                type(kvargs["next"]).__name__
                == AssignmentsLinks.__annotations__["next"]
            ):
                self_.next = kvargs["next"]
            else:
                self_.next = Link(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if (
                type(kvargs["prev"]).__name__
                == AssignmentsLinks.__annotations__["prev"]
            ):
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Link(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if (
                type(kvargs["self"]).__name__
                == AssignmentsLinks.__annotations__["self"]
            ):
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsMeta:
    """

    Attributes
    ----------
    count: int
      The total number of assignments matching the current filter.
    """

    count: int = None

    def __init__(self_, **kvargs):
        if "count" in kvargs and kvargs["count"] is not None:
            self_.count = kvargs["count"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Link:
    """

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
class SpaceCreate:
    """

    Attributes
    ----------
    description: str
      The description of the space. Personal spaces do not have a description.
    name: str
      The name of the space. Personal spaces do not have a name.
    type: Literal["shared", "managed", "data"]
      The type of space such as shared, managed, and so on.
    """

    description: str = None
    name: str = None
    type: Literal["shared", "managed", "data"] = None

    def __init__(self_, **kvargs):
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpaceLinks:
    """

    Attributes
    ----------
    assignments: Link
    self: Link
    """

    assignments: Link = None
    self: Link = None

    def __init__(self_, **kvargs):
        if "assignments" in kvargs and kvargs["assignments"] is not None:
            if (
                type(kvargs["assignments"]).__name__
                == SpaceLinks.__annotations__["assignments"]
            ):
                self_.assignments = kvargs["assignments"]
            else:
                self_.assignments = Link(**kvargs["assignments"])
        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == SpaceLinks.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpaceMeta:
    """
    Information about the space settings.

    Attributes
    ----------
    actions: list[str]
      The list of actions allowed by the current user in this space.
    assignableRoles: list[str]
      The list of roles that could be assigned in this space.
    roles: list[str]
      The list of roles assigned to the current user in this space.
    """

    actions: list[str] = None
    assignableRoles: list[str] = None
    roles: list[str] = None

    def __init__(self_, **kvargs):
        if "actions" in kvargs and kvargs["actions"] is not None:
            self_.actions = kvargs["actions"]
        if "assignableRoles" in kvargs and kvargs["assignableRoles"] is not None:
            self_.assignableRoles = kvargs["assignableRoles"]
        if "roles" in kvargs and kvargs["roles"] is not None:
            self_.roles = kvargs["roles"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpacePatch(List["SpacePatchElement"]):
    """

    Attributes
    ----------
    """

    def __init__(self_, elements):
        for e in elements:
            self_.append(SpacePatchElement(**e))


@dataclass
class SpacePatchElement:
    """
    A JSONPatch document as defined by RFC 6902.

    Attributes
    ----------
    op: Literal["replace"]
      The operation to be performed.
    path: Literal["/name", "/ownerId", "/description"]
      Field of space to be patched (updated).
    value: str
      The value to be used within the operations.
      - name: The name (string) of space of maxLength 256 of pattern: ^[^\"\*\?\\/\|\\\:]+$
      - description: The description (string) of the space. Personal spaces do not have a description.
      - ownerId: The user ID in uid format (string) of the space owner.

    """

    op: Literal["replace"] = None
    path: Literal["/name", "/ownerId", "/description"] = None
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
class SpaceTypes:
    """
    The distinct types of spaces (shared, managed, and so on).

    Attributes
    ----------
    data: list[str]
    """

    data: list[str] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            self_.data = kvargs["data"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpaceUpdate:
    """

    Attributes
    ----------
    description: str
      The description of the space. Personal spaces do not have a description.
    name: str
      The name of the space.
    ownerId: str
      The user ID of the space owner.
    """

    description: str = None
    name: str = None
    ownerId: str = None

    def __init__(self_, **kvargs):
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "ownerId" in kvargs and kvargs["ownerId"] is not None:
            self_.ownerId = kvargs["ownerId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpacesClass:
    """

    Attributes
    ----------
    data: list[Space]
    links: SpacesLinks
    meta: SpacesMeta
    """

    data: list[Space] = None
    links: SpacesLinks = None
    meta: SpacesMeta = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]" == SpacesClass.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [Space(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == SpacesClass.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = SpacesLinks(**kvargs["links"])
        if "meta" in kvargs and kvargs["meta"] is not None:
            if type(kvargs["meta"]).__name__ == SpacesClass.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = SpacesMeta(**kvargs["meta"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpacesLinks:
    """

    Attributes
    ----------
    next: Link
    prev: Link
    self: Link
    """

    next: Link = None
    prev: Link = None
    self: Link = None

    def __init__(self_, **kvargs):
        if "next" in kvargs and kvargs["next"] is not None:
            if type(kvargs["next"]).__name__ == SpacesLinks.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = Link(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if type(kvargs["prev"]).__name__ == SpacesLinks.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Link(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == SpacesLinks.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpacesMeta:
    """

    Attributes
    ----------
    count: int
      The total number of spaces matching the current filter.
    personalSpace: SpacesMetaPersonalSpace
      The meta related to personal space when applicable.
    """

    count: int = None
    personalSpace: SpacesMetaPersonalSpace = None

    def __init__(self_, **kvargs):
        if "count" in kvargs and kvargs["count"] is not None:
            self_.count = kvargs["count"]
        if "personalSpace" in kvargs and kvargs["personalSpace"] is not None:
            if (
                type(kvargs["personalSpace"]).__name__
                == SpacesMeta.__annotations__["personalSpace"]
            ):
                self_.personalSpace = kvargs["personalSpace"]
            else:
                self_.personalSpace = SpacesMetaPersonalSpace(**kvargs["personalSpace"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpacesMetaPersonalSpace:
    """
    The meta related to personal space when applicable.

    Attributes
    ----------
    actions: list[str]
      The list of actions allowed by the current user in this space.
    resourceType: str
      resource type
    """

    actions: list[str] = None
    resourceType: str = None

    def __init__(self_, **kvargs):
        if "actions" in kvargs and kvargs["actions"] is not None:
            self_.actions = kvargs["actions"]
        if "resourceType" in kvargs and kvargs["resourceType"] is not None:
            self_.resourceType = kvargs["resourceType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Spaces:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_types(self) -> SpaceTypes:
        """
        Gets a list of distinct space types.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/spaces/types",
            method="GET",
            params={},
            data=None,
        )
        obj = SpaceTypes(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, spaceId: str) -> Space:
        """
        Retrieves a single space by ID.

        Parameters
        ----------
        spaceId: str
          The ID of the space to retrieve.
        """
        response = self.auth.rest(
            path="/spaces/{spaceId}".replace("{spaceId}", spaceId),
            method="GET",
            params={},
            data=None,
        )
        obj = Space(**response.json())
        obj.auth = self.auth
        return obj

    def get_spaces(
        self,
        action: str = None,
        filter: str = None,
        limit: int = 10,
        name: str = None,
        next: str = None,
        ownerId: str = None,
        prev: str = None,
        sort: str = None,
        type: str = None,
    ) -> ListableResource[Space]:
        """
        Retrieves spaces that the current user has access to and match the query.

        Parameters
        ----------
        action: str = None
          Action on space. Supports only "?action=publish".
        filter: str = None
          Exact match filtering on space name using SCIM. Case insensitive on attribute name. For example ?filter=name eq "MySpace" and ?filter=NAME eq "MySpace" is both valid.
        limit: int = 10
          Maximum number of spaces to return.
        name: str = None
          Space name to search and filter for. Case-insensitive open search with wildcards both as prefix and suffix. For example, "?name=fin" will get "finance", "Final" and "Griffin".
        next: str = None
          The next page cursor. Next links make use of this.
        ownerId: str = None
          Space ownerId to filter by. For example, "?ownerId=123".
        prev: str = None
          The previous page cursor. Previous links make use of this.
        sort: str = None
          Field to sort by. Prefix with +/- to indicate asc/desc. For example, "?sort=+name" to sort ascending on Name. Supported fields are "type", "name" and "createdAt".
        type: str = None
          Type(s) of space to filter. For example, "?type=managed,shared".
        """
        query_params = {}
        if action is not None:
            query_params["action"] = action
        if filter is not None:
            query_params["filter"] = filter

            warnings.warn("filter is experimental", UserWarning, stacklevel=2)
        if limit is not None:
            query_params["limit"] = limit
        if name is not None:
            query_params["name"] = name
        if next is not None:
            query_params["next"] = next
        if ownerId is not None:
            query_params["ownerId"] = ownerId
        if prev is not None:
            query_params["prev"] = prev
        if sort is not None:
            query_params["sort"] = sort
        if type is not None:
            query_params["type"] = type
        response = self.auth.rest(
            path="/spaces",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Space,
            auth=self.auth,
            path="/spaces",
            query_params=query_params,
        )

    def create(self, data: SpaceCreate) -> Space:
        """
        Creates a space.

        Parameters
        ----------
        data: SpaceCreate
          Attributes that the user wants to set for a new space.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/spaces",
            method="POST",
            params={},
            data=data,
        )
        obj = Space(**response.json())
        obj.auth = self.auth
        return obj
