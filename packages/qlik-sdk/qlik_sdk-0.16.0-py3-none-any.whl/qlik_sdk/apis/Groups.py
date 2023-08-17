# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import List, Literal

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class Group:
    """
    represents a Group document

    Attributes
    ----------
    assignedRoles: list[GroupAssignedRoles]
    createdAt: str
      The timestamp for when the group record was created.
    id: str
      The unique identifier for the group
    idpId: str
      The unique identifier for the source IDP.
    lastUpdatedAt: str
      The timestamp for when the group record was last updated.
    links: GroupLinks
      Contains Links for current document
    name: str
      The name of the group.
    status: Literal["active", "disabled"]
      The state of the group.
    tenantId: str
      The tenant identifier associated with the given group
    """

    assignedRoles: list[GroupAssignedRoles] = None
    createdAt: str = None
    id: str = None
    idpId: str = None
    lastUpdatedAt: str = None
    links: GroupLinks = None
    name: str = None
    status: Literal["active", "disabled"] = None
    tenantId: str = None

    def __init__(self_, **kvargs):
        if "assignedRoles" in kvargs and kvargs["assignedRoles"] is not None:
            if all(
                f"list[{type(e).__name__}]" == Group.__annotations__["assignedRoles"]
                for e in kvargs["assignedRoles"]
            ):
                self_.assignedRoles = kvargs["assignedRoles"]
            else:
                self_.assignedRoles = [
                    GroupAssignedRoles(**e) for e in kvargs["assignedRoles"]
                ]
        if "createdAt" in kvargs and kvargs["createdAt"] is not None:
            self_.createdAt = kvargs["createdAt"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "idpId" in kvargs and kvargs["idpId"] is not None:
            self_.idpId = kvargs["idpId"]
        if "lastUpdatedAt" in kvargs and kvargs["lastUpdatedAt"] is not None:
            self_.lastUpdatedAt = kvargs["lastUpdatedAt"]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == Group.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = GroupLinks(**kvargs["links"])
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "status" in kvargs and kvargs["status"] is not None:
            self_.status = kvargs["status"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            self_.tenantId = kvargs["tenantId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def delete(self) -> None:
        """
        Delete group by id

        Parameters
        ----------
        """
        self.auth.rest(
            path="/groups/{groupId}".replace("{groupId}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def patch(self, data: GroupPatchSchema) -> None:
        """
        Update group by id

        Parameters
        ----------
        data: GroupPatchSchema
          An array of JSON Patches for a group.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        self.auth.rest(
            path="/groups/{groupId}".replace("{groupId}", self.id),
            method="PATCH",
            params={},
            data=data,
        )


@dataclass
class Filter:
    """
    An advanced query filter to be used for complex user querying in the tenant.

    Attributes
    ----------
    filter: str
      The advanced filtering to be applied the query. All conditional statements within this query parameter are case insensitive.
    """

    filter: str = None

    def __init__(self_, **kvargs):
        if "filter" in kvargs and kvargs["filter"] is not None:
            self_.filter = kvargs["filter"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupAssignedRoles:
    """
    represents a role entity to be stored on a Group entity, either default or custom role

    Attributes
    ----------
    id: str
    level: Literal["admin", "user"]
    name: str
    permissions: list[str]
    type: Literal["default"]
    """

    id: str = None
    level: Literal["admin", "user"] = None
    name: str = None
    permissions: list[str] = None
    type: Literal["default"] = None

    def __init__(self_, **kvargs):
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "level" in kvargs and kvargs["level"] is not None:
            self_.level = kvargs["level"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "permissions" in kvargs and kvargs["permissions"] is not None:
            self_.permissions = kvargs["permissions"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupLinks:
    """
    Contains Links for current document

    Attributes
    ----------
    self: GroupLinksSelf
    """

    self: GroupLinksSelf = None

    def __init__(self_, **kvargs):
        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == GroupLinks.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = GroupLinksSelf(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupLinksSelf:
    """

    Attributes
    ----------
    href: str
      Link to the current group document
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
class GroupPatch:
    """
    A JSON Patch document.

    Attributes
    ----------
    op: Literal["replace"]
      The operation to be performed. Currently "replace" is the only supported operation.
    path: Literal["assignedRoles"]
      Attribute name of a field of the Groups entity.
    value: object
      The roles to assign to the group (limit of 100 roles per group).
    """

    op: Literal["replace"] = None
    path: Literal["assignedRoles"] = None
    value: list[GroupPatchAssignedRolesRefIDs] | list[any] = None

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
class GroupPatchAssignedRolesRefIDs:
    """
    represents a role entity stored in the database

    Attributes
    ----------
    id: str
      The unique role identitier
    """

    id: str = None

    def __init__(self_, **kvargs):
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupPatchSchema(List["GroupPatch"]):
    """
    An array of JSON Patches for a group.

    Attributes
    ----------
    """

    def __init__(self_, elements):
        for e in elements:
            self_.append(GroupPatch(**e))


@dataclass
class GroupPostSchema:
    """

    Attributes
    ----------
    assignedRoles: object
      The roles to assign to the group (limit of 100 roles per group).
    name: str
      The name of the group (maximum length of 256 characters).
    status: Literal["active"]
      The status of the created group within the tenant. Defaults to active if empty.
    """

    assignedRoles: list[GroupPostSchemaAssignedRolesRefIDs] | list[any] = None
    name: str = None
    status: Literal["active"] = None

    def __init__(self_, **kvargs):
        if "assignedRoles" in kvargs and kvargs["assignedRoles"] is not None:
            self_.assignedRoles = kvargs["assignedRoles"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "status" in kvargs and kvargs["status"] is not None:
            self_.status = kvargs["status"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupPostSchemaAssignedRolesRefIDs:
    """
    represents a role entity stored in the database

    Attributes
    ----------
    id: str
      The unique role identitier
    """

    id: str = None

    def __init__(self_, **kvargs):
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupSettings:
    """
    represents a GroupSetting document

    Attributes
    ----------
    autoCreateGroups: bool
      Determines if groups should be created on login.
    links: GroupSettingsLinks
      Contains Links for current document
    syncIdpGroups: bool
      Determines if groups should be created on login.
    systemGroups: GroupSettingsSystemGroups
    tenantId: str
      The unique tenant identifier.
    """

    autoCreateGroups: bool = None
    links: GroupSettingsLinks = None
    syncIdpGroups: bool = None
    systemGroups: GroupSettingsSystemGroups = None
    tenantId: str = None

    def __init__(self_, **kvargs):
        if "autoCreateGroups" in kvargs and kvargs["autoCreateGroups"] is not None:
            self_.autoCreateGroups = kvargs["autoCreateGroups"]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == GroupSettings.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = GroupSettingsLinks(**kvargs["links"])
        if "syncIdpGroups" in kvargs and kvargs["syncIdpGroups"] is not None:
            self_.syncIdpGroups = kvargs["syncIdpGroups"]
        if "systemGroups" in kvargs and kvargs["systemGroups"] is not None:
            if (
                type(kvargs["systemGroups"]).__name__
                == GroupSettings.__annotations__["systemGroups"]
            ):
                self_.systemGroups = kvargs["systemGroups"]
            else:
                self_.systemGroups = GroupSettingsSystemGroups(**kvargs["systemGroups"])
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            self_.tenantId = kvargs["tenantId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupSettingsLinks:
    """
    Contains Links for current document

    Attributes
    ----------
    self: GroupSettingsLinksSelf
    """

    self: GroupSettingsLinksSelf = None

    def __init__(self_, **kvargs):
        if "self" in kvargs and kvargs["self"] is not None:
            if (
                type(kvargs["self"]).__name__
                == GroupSettingsLinks.__annotations__["self"]
            ):
                self_.self = kvargs["self"]
            else:
                self_.self = GroupSettingsLinksSelf(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupSettingsLinksSelf:
    """

    Attributes
    ----------
    href: str
      Link to the current group settings document
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
class GroupSettingsSystemGroups:
    """

    Attributes
    ----------
    _000000000000000000000001: GroupSettingsSystemGroups000000000000000000000001
    """

    _000000000000000000000001: GroupSettingsSystemGroups000000000000000000000001 = None

    def __init__(self_, **kvargs):
        if (
            "000000000000000000000001" in kvargs
            and kvargs["000000000000000000000001"] is not None
        ):
            if (
                type(kvargs["000000000000000000000001"]).__name__
                == GroupSettingsSystemGroups.__annotations__[
                    "_000000000000000000000001"
                ]
            ):
                self_._000000000000000000000001 = kvargs["000000000000000000000001"]
            else:
                self_._000000000000000000000001 = (
                    GroupSettingsSystemGroups000000000000000000000001(
                        **kvargs["000000000000000000000001"]
                    )
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupSettingsSystemGroups000000000000000000000001:
    """

    Attributes
    ----------
    assignedRoles: list[GroupSettingsSystemGroups000000000000000000000001AssignedRoles]
      An array of role references.
    createdAt: str
      The timestamp for when the Everyone group was created.
    enabled: bool
      For Everyone, this is always `true` and can't be patched.
    id: Literal["000000000000000000000001"]
      The ID of the Everyone group. This value will not change and is immutable.
    lastUpdatedAt: str
      The timestamp for when the Everyone group was last updated.
    name: Literal["com.qlik.Everyone"]
      The name of the Everyone group. This value will not change and is immutable.
    """

    assignedRoles: list[
        GroupSettingsSystemGroups000000000000000000000001AssignedRoles
    ] = None
    createdAt: str = None
    enabled: bool = True
    id: Literal["000000000000000000000001"] = None
    lastUpdatedAt: str = None
    name: Literal["com.qlik.Everyone"] = None

    def __init__(self_, **kvargs):
        if "assignedRoles" in kvargs and kvargs["assignedRoles"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == GroupSettingsSystemGroups000000000000000000000001.__annotations__[
                    "assignedRoles"
                ]
                for e in kvargs["assignedRoles"]
            ):
                self_.assignedRoles = kvargs["assignedRoles"]
            else:
                self_.assignedRoles = [
                    GroupSettingsSystemGroups000000000000000000000001AssignedRoles(**e)
                    for e in kvargs["assignedRoles"]
                ]
        if "createdAt" in kvargs and kvargs["createdAt"] is not None:
            self_.createdAt = kvargs["createdAt"]
        if "enabled" in kvargs and kvargs["enabled"] is not None:
            self_.enabled = kvargs["enabled"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "lastUpdatedAt" in kvargs and kvargs["lastUpdatedAt"] is not None:
            self_.lastUpdatedAt = kvargs["lastUpdatedAt"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupSettingsSystemGroups000000000000000000000001AssignedRoles:
    """
    represents a role entity stored in the database

    Attributes
    ----------
    id: str
      The unique role identitier
    level: Literal["admin", "user"]
      The role level
    name: str
      The role name
    permissions: list[str]
      An array of permissions associated to a given role.
    type: Literal["default"]
      The type of role
    """

    id: str = None
    level: Literal["admin", "user"] = None
    name: str = None
    permissions: list[str] = None
    type: Literal["default"] = None

    def __init__(self_, **kvargs):
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "level" in kvargs and kvargs["level"] is not None:
            self_.level = kvargs["level"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "permissions" in kvargs and kvargs["permissions"] is not None:
            self_.permissions = kvargs["permissions"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupsClass:
    """
    A result object when listing groups.

    Attributes
    ----------
    data: list[Group]
      An array of groups.
    links: GroupsLinks
    totalResults: int
      Indicates the total number of matching documents. Will only be returned if the query parameter "totalResults" is true.
    """

    data: list[Group] = None
    links: GroupsLinks = None
    totalResults: int = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]" == GroupsClass.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [Group(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == GroupsClass.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = GroupsLinks(**kvargs["links"])
        if "totalResults" in kvargs and kvargs["totalResults"] is not None:
            self_.totalResults = kvargs["totalResults"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupsLinks:
    """

    Attributes
    ----------
    next: GroupsLinksNext
    prev: GroupsLinksPrev
    self: GroupsLinksSelf
    """

    next: GroupsLinksNext = None
    prev: GroupsLinksPrev = None
    self: GroupsLinksSelf = None

    def __init__(self_, **kvargs):
        if "next" in kvargs and kvargs["next"] is not None:
            if type(kvargs["next"]).__name__ == GroupsLinks.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = GroupsLinksNext(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if type(kvargs["prev"]).__name__ == GroupsLinks.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = GroupsLinksPrev(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == GroupsLinks.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = GroupsLinksSelf(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupsLinksNext:
    """

    Attributes
    ----------
    href: str
      Link to the next page of items
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
class GroupsLinksPrev:
    """

    Attributes
    ----------
    href: str
      Link to the previous page of items
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
class GroupsLinksSelf:
    """

    Attributes
    ----------
    href: str
      Link to the current page of items
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
class SettingsPatch:
    """
    A JSON Patch document as defined in http://tools.ietf.org/html/rfc6902.

    Attributes
    ----------
    op: Literal["replace"]
      The operation to be performed.
    path: Literal["/autoCreateGroups", "/syncIdpGroups", "/systemGroups/{id}/assignedRoles"]
      A JSON Pointer.
    value: object
      The value to be used for this operation.
    """

    op: Literal["replace"] = None
    path: Literal[
        "/autoCreateGroups", "/syncIdpGroups", "/systemGroups/{id}/assignedRoles"
    ] = None
    value: bool | list[SettingsPatchAssignedRolesRefIDs] | list[any] = None

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
class SettingsPatchAssignedRolesRefIDs:
    """
    represents a role entity stored in the database

    Attributes
    ----------
    id: str
      The unique role identitier
    """

    id: str = None

    def __init__(self_, **kvargs):
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SettingsPatchSchema(List["SettingsPatch"]):
    """
    An array of JSON Patches for the groups settings.

    Attributes
    ----------
    """

    def __init__(self_, elements):
        for e in elements:
            self_.append(SettingsPatch(**e))


class Groups:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def filter(
        self,
        data: Filter = None,
        limit: float = 20,
        next: str = None,
        prev: str = None,
        sort: Literal["name", "+name", "-name"] = "+name",
    ) -> ListableResource[Group]:
        """
        Filter groups
        Retrieves a list of groups matching the filter using advanced query string.

        Parameters
        ----------
        limit: float = 20
          The number of user entries to retrieve.
        next: str = None
          Get users with IDs that are higher than the target user ID. Cannot be used in conjunction with prev.
        prev: str = None
          Get users with IDs that are lower than the target user ID. Cannot be used in conjunction with next.
        sort: Literal["name", "+name", "-name"] = "+name"
          The field to sort by, with +/- prefix indicating sort order
        data: Filter = None
          An advanced query filter to be used for complex user querying in the tenant.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        query_params = {}
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if sort is not None:
            query_params["sort"] = sort
        response = self.auth.rest(
            path="/groups/actions/filter",
            method="POST",
            params=query_params,
            data=data,
        )
        return ListableResource(
            response=response.json(),
            cls=Group,
            auth=self.auth,
            path="/groups/actions/filter",
            query_params=query_params,
        )

    def get_settings(self) -> GroupSettings:
        """
        Get group settings
        Returns the active tenant's group settings.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/groups/settings",
            method="GET",
            params={},
            data=None,
        )
        obj = GroupSettings(**response.json())
        obj.auth = self.auth
        return obj

    def patch_settings(self, data: SettingsPatchSchema) -> None:
        """
        Update group settings

        Parameters
        ----------
        data: SettingsPatchSchema
          An array of JSON Patches for the groups settings.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        self.auth.rest(
            path="/groups/settings",
            method="PATCH",
            params={},
            data=data,
        )

    def get(self, groupId: str) -> Group:
        """
        Get group by id
        Returns the requested group.

        Parameters
        ----------
        groupId: str
          The group's unique identifier
        """
        response = self.auth.rest(
            path="/groups/{groupId}".replace("{groupId}", groupId),
            method="GET",
            params={},
            data=None,
        )
        obj = Group(**response.json())
        obj.auth = self.auth
        return obj

    def get_groups(
        self,
        filter: str = None,
        limit: float = 20,
        next: str = None,
        prev: str = None,
        sort: str = None,
        systemGroups: bool = False,
        totalResults: bool = None,
    ) -> ListableResource[Group]:
        """
        List groups.
        Returns a list of groups with cursor-based pagination.

        Parameters
        ----------
        filter: str = None
          The advanced filtering to use for the query. Refer to RFC 7644 https://datatracker.ietf.org/doc/rfc7644/ for the syntax. Cannot be combined with any of the fields marked as deprecated. All conditional statements within this query parameter are case insensitive.
        limit: float = 20
          The number of groups to retrieve.
        next: str = None
          The next page cursor.
        prev: str = None
          The previous page cursor.
        sort: str = None
          Optional resource field name to sort on, eg. name. Can be prefixed with +/- to determine order, defaults to (+) ascending.
        systemGroups: bool = False
          Return system groups (e.g. Everyone) instead of regular groups. Cannot be combined with any other query parameters.
        totalResults: bool = None
          Whether to return a total match count in the result. Defaults to false.
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
        if systemGroups is not None:
            query_params["systemGroups"] = systemGroups
        if totalResults is not None:
            query_params["totalResults"] = totalResults
        response = self.auth.rest(
            path="/groups",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Group,
            auth=self.auth,
            path="/groups",
            query_params=query_params,
        )

    def create(self, data: GroupPostSchema) -> Group:
        """
        Create group.
        Creates a group. The maximum number of groups a tenant can have is 10,000.

        Parameters
        ----------
        data: GroupPostSchema
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/groups",
            method="POST",
            params={},
            data=data,
        )
        obj = Group(**response.json())
        obj.auth = self.auth
        return obj
