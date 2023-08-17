# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

from dataclasses import dataclass

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class GetByIDResult:
    """

    Attributes
    ----------
    contentType: str
      The type that content is encoded in, always "application/json".
    data: object
      Additional information about the event's details. The structure depends on the type and version of the event.
    eventId: str
      The event's unique identifier.
    eventTime: str
      The RFC3339 datetime when the event happened.
    eventType: str
      The type of event that describes committed action.
    eventTypeVersion: str
      The version of the event type.
    extensions: EventExtensions
      The availability of the properties depends on the event and the context it was triggered in.
    id: str
      The resource item's unique identifier.
    links: GetLinks
    source: str
      The source of the event message, usually the producing service.
    tenantId: str
      The ID of the tenant that owns the item. This is populated using the JWT.
    userId: str
      The ID of the user who performed the action that triggered the event.
    """

    contentType: str = None
    data: object = None
    eventId: str = None
    eventTime: str = None
    eventType: str = None
    eventTypeVersion: str = None
    extensions: EventExtensions = None
    id: str = None
    links: GetLinks = None
    source: str = None
    tenantId: str = None
    userId: str = None

    def __init__(self_, **kvargs):
        if "contentType" in kvargs and kvargs["contentType"] is not None:
            self_.contentType = kvargs["contentType"]
        if "data" in kvargs and kvargs["data"] is not None:
            self_.data = kvargs["data"]
        if "eventId" in kvargs and kvargs["eventId"] is not None:
            self_.eventId = kvargs["eventId"]
        if "eventTime" in kvargs and kvargs["eventTime"] is not None:
            self_.eventTime = kvargs["eventTime"]
        if "eventType" in kvargs and kvargs["eventType"] is not None:
            self_.eventType = kvargs["eventType"]
        if "eventTypeVersion" in kvargs and kvargs["eventTypeVersion"] is not None:
            self_.eventTypeVersion = kvargs["eventTypeVersion"]
        if "extensions" in kvargs and kvargs["extensions"] is not None:
            if (
                type(kvargs["extensions"]).__name__
                == GetByIDResult.__annotations__["extensions"]
            ):
                self_.extensions = kvargs["extensions"]
            else:
                self_.extensions = EventExtensions(**kvargs["extensions"])
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == GetByIDResult.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = GetLinks(**kvargs["links"])
        if "source" in kvargs and kvargs["source"] is not None:
            self_.source = kvargs["source"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            self_.tenantId = kvargs["tenantId"]
        if "userId" in kvargs and kvargs["userId"] is not None:
            self_.userId = kvargs["userId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EventExtensions:
    """
    The availability of the properties depends on the event and the context it was triggered in.

    Attributes
    ----------
    actor: EventExtensionsActor
      Specifies the entity performing the action on behalf of another party listed as triggering the action.
    ownerId: str
      Id of the owner of the resource affected by the eventContext.
    spaceId: str
      Id of the space related to the action performed on the eventContext.
    topLevelResourceId: str
      If the event originated from a sub resource the topLevelResourceId contains the id of the top level resource associated with the sub resource.
    updates: object
      Might be present if the action is of type "updated" and should contain information about the changes made to the resource.
    """

    actor: EventExtensionsActor = None
    ownerId: str = None
    spaceId: str = None
    topLevelResourceId: str = None
    updates: object = None

    def __init__(self_, **kvargs):
        if "actor" in kvargs and kvargs["actor"] is not None:
            if (
                type(kvargs["actor"]).__name__
                == EventExtensions.__annotations__["actor"]
            ):
                self_.actor = kvargs["actor"]
            else:
                self_.actor = EventExtensionsActor(**kvargs["actor"])
        if "ownerId" in kvargs and kvargs["ownerId"] is not None:
            self_.ownerId = kvargs["ownerId"]
        if "spaceId" in kvargs and kvargs["spaceId"] is not None:
            self_.spaceId = kvargs["spaceId"]
        if "topLevelResourceId" in kvargs and kvargs["topLevelResourceId"] is not None:
            self_.topLevelResourceId = kvargs["topLevelResourceId"]
        if "updates" in kvargs and kvargs["updates"] is not None:
            self_.updates = kvargs["updates"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EventExtensionsActor:
    """
    Specifies the entity performing the action on behalf of another party listed as triggering the action.

    Attributes
    ----------
    sub: str
      Opaque value identifying impersonating entity.
    subType: str
      The type of the impersonating entity.
    """

    sub: str = None
    subType: str = None

    def __init__(self_, **kvargs):
        if "sub" in kvargs and kvargs["sub"] is not None:
            self_.sub = kvargs["sub"]
        if "subType" in kvargs and kvargs["subType"] is not None:
            self_.subType = kvargs["subType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetArchiveResult:
    """

    Attributes
    ----------
    data: list[object]
      List of archived events. The structure of the events depend on their type and version.
    """

    data: list[object] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            self_.data = kvargs["data"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetLinks:
    """

    Attributes
    ----------
    Self: HrefDeprecated
    self: Href
    """

    Self: HrefDeprecated = None
    self: Href = None

    def __init__(self_, **kvargs):
        if "Self" in kvargs and kvargs["Self"] is not None:
            if type(kvargs["Self"]).__name__ == GetLinks.__annotations__["Self"]:
                self_.Self = kvargs["Self"]
            else:
                self_.Self = HrefDeprecated(**kvargs["Self"])
        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == GetLinks.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Href(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetObjectsResult:
    """

    Attributes
    ----------
    data: list[str]
      List of requested resources.
    links: ListLinks
    """

    data: list[str] = None
    links: ListLinks = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            self_.data = kvargs["data"]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == GetObjectsResult.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = ListLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetResult:
    """

    Attributes
    ----------
    data: list[GetByIDResult]
      List of audit items.
    links: ListLinks
    """

    data: list[GetByIDResult] = None
    links: ListLinks = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]" == GetResult.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [GetByIDResult(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == GetResult.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = ListLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetSettingsResult:
    """

    Attributes
    ----------
    data: GetSettingsResultData
      Server configuration options.
    """

    data: GetSettingsResultData = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if (
                type(kvargs["data"]).__name__
                == GetSettingsResult.__annotations__["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = GetSettingsResultData(**kvargs["data"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetSettingsResultData:
    """
    Server configuration options.

    Attributes
    ----------
    ArchiveEnabled: bool
      Is Long Term Storage archiving enabled?.
    EventTTL: int
      The events TTL in seconds.
    """

    ArchiveEnabled: bool = None
    EventTTL: int = None

    def __init__(self_, **kvargs):
        if "ArchiveEnabled" in kvargs and kvargs["ArchiveEnabled"] is not None:
            self_.ArchiveEnabled = kvargs["ArchiveEnabled"]
        if "EventTTL" in kvargs and kvargs["EventTTL"] is not None:
            self_.EventTTL = kvargs["EventTTL"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class HrefDeprecated:
    """

    Attributes
    ----------
    Href: str
    """

    Href: str = None

    def __init__(self_, **kvargs):
        if "Href" in kvargs and kvargs["Href"] is not None:
            self_.Href = kvargs["Href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ListLinks:
    """

    Attributes
    ----------
    Next: HrefDeprecated
    Prev: HrefDeprecated
    Self: HrefDeprecated
    next: Href
    prev: Href
    self: Href
    """

    Next: HrefDeprecated = None
    Prev: HrefDeprecated = None
    Self: HrefDeprecated = None
    next: Href = None
    prev: Href = None
    self: Href = None

    def __init__(self_, **kvargs):
        if "Next" in kvargs and kvargs["Next"] is not None:
            if type(kvargs["Next"]).__name__ == ListLinks.__annotations__["Next"]:
                self_.Next = kvargs["Next"]
            else:
                self_.Next = HrefDeprecated(**kvargs["Next"])
        if "Prev" in kvargs and kvargs["Prev"] is not None:
            if type(kvargs["Prev"]).__name__ == ListLinks.__annotations__["Prev"]:
                self_.Prev = kvargs["Prev"]
            else:
                self_.Prev = HrefDeprecated(**kvargs["Prev"])
        if "Self" in kvargs and kvargs["Self"] is not None:
            if type(kvargs["Self"]).__name__ == ListLinks.__annotations__["Self"]:
                self_.Self = kvargs["Self"]
            else:
                self_.Self = HrefDeprecated(**kvargs["Self"])
        if "next" in kvargs and kvargs["next"] is not None:
            if type(kvargs["next"]).__name__ == ListLinks.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = Href(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if type(kvargs["prev"]).__name__ == ListLinks.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Href(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == ListLinks.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Href(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Href:
    """

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


class Audits:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_archives(self, date: str) -> GetArchiveResult:
        """
        Retrieves audit events from long term storage.
        Finds and returns audit events from the archive, formatted as a JSON array, for the given date and tenant (in JWT).

        Parameters
        ----------
        date: str
          Date to be used as filter and criteria during extraction.
        """
        query_params = {}
        if date is not None:
            query_params["date"] = date
        response = self.auth.rest(
            path="/audits/archive",
            method="GET",
            params=query_params,
            data=None,
        )
        obj = GetArchiveResult(**response.json())
        obj.auth = self.auth
        return obj

    def get_settings(self) -> GetSettingsResult:
        """
        Returns the server configuration options.
        It includes options that represent the server configuration state and parameters that were used to run the server with certain functionality.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/audits/settings",
            method="GET",
            params={},
            data=None,
        )
        obj = GetSettingsResult(**response.json())
        obj.auth = self.auth
        return obj

    def get_sources(self) -> GetObjectsResult:
        """
        Finds and returns the distinct list of unique event sources.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/audits/sources",
            method="GET",
            params={},
            data=None,
        )
        obj = GetObjectsResult(**response.json())
        obj.auth = self.auth
        return obj

    def get_types(self) -> GetObjectsResult:
        """
        Finds and returns the distinct list of unique event types.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/audits/types",
            method="GET",
            params={},
            data=None,
        )
        obj = GetObjectsResult(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, id: str) -> GetByIDResult:
        """
        Finds and returns the persisted audit events for the given tenant.

        Parameters
        ----------
        id: str
          The audit item's unique identifier.
        """
        response = self.auth.rest(
            path="/audits/{id}".replace("{id}", id),
            method="GET",
            params={},
            data=None,
        )
        obj = GetByIDResult(**response.json())
        obj.auth = self.auth
        return obj

    def get_audits(
        self,
        eventTime: str = None,
        eventType: str = None,
        id: str = None,
        limit: int = 10,
        next: str = None,
        prev: str = None,
        sort: str = "-eventTime",
        source: str = None,
        userId: str = None,
    ) -> ListableResource[GetByIDResult]:
        """
        Finds and returns the persisted audit events for the given tenant.

        Parameters
        ----------
        eventTime: str = None
          The start/end time interval formatted in ISO 8601 to search by eventTime. For example, "?eventTime=2021-07-14T18:41:15.00Z/2021-07-14T18:41:15.99Z".
        eventType: str = None
          The case-sensitive string used to search by eventType.
        id: str = None
          The comma separated list of audit unique identifiers.
        limit: int = 10
          The maximum number of resources to return for a request. The limit must be an integer between 1 and 100 (inclusive).
        next: str = None
          The cursor to the next page of resources. Provide either the next or prev cursor, but not both.
        prev: str = None
          The cursor to the previous page of resources. Provide either the next or prev cursor, but not both.
        sort: str = "-eventTime"
          The property of a resource to sort on (default sort is -eventTime). The supported properties are source, eventType, and eventTime. A property must be prefixed by + or - to indicate ascending or descending sort order respectively.
        source: str = None
          The case-sensitive string used to search by source.
        userId: str = None
          The case-sensitive string used to search by userId.
        """
        query_params = {}
        if eventTime is not None:
            query_params["eventTime"] = eventTime
        if eventType is not None:
            query_params["eventType"] = eventType
        if id is not None:
            query_params["id"] = id
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if sort is not None:
            query_params["sort"] = sort
        if source is not None:
            query_params["source"] = source
        if userId is not None:
            query_params["userId"] = userId
        response = self.auth.rest(
            path="/audits",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=GetByIDResult,
            auth=self.auth,
            path="/audits",
            query_params=query_params,
        )
