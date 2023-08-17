# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class Reload:
    """

    Attributes
    ----------
    appId: str
      The ID of the app.
    creationTime: str
      The time the reload job was created.
    endTime: str
      The time the reload job finished.
    engineTime: str
      The timestamp returned from the Sense engine upon successful reload.
    id: str
      The ID of the reload.
    links: ReloadLinks
    log: str
      The log describing the result of the latest reload execution from the request.
    partial: bool
      The boolean value used to present the reload is partial or not
    startTime: str
      The time the reload job was consumed from the queue.
    status: Literal["QUEUED", "RELOADING", "CANCELING", "SUCCEEDED", "FAILED", "CANCELED", "EXCEEDED_LIMIT"]
      The status of the reload. There are seven statuses. `QUEUED`, `RELOADING`, `CANCELING` are the active statuses. `SUCCEEDED`, `FAILED`,`CANCELED`,`EXCEEDED_LIMIT` are the end statuses.
    tenantId: str
      The ID of the tenant who owns the reload.
    type: Literal["hub", "chronos", "external", "automations", "data-refresh"]
      What initiated the reload: hub = one-time reload manually triggered in hub, chronos = time based scheduled reload triggered by chronos, external = reload triggered via external API request, automations = reload triggered in automation, data-refresh = reload triggered by refresh of data.
    userId: str
      The ID of the user who created the reload.
    """

    appId: str = None
    creationTime: str = None
    endTime: str = None
    engineTime: str = None
    id: str = None
    links: ReloadLinks = None
    log: str = None
    partial: bool = None
    startTime: str = None
    status: Literal[
        "QUEUED",
        "RELOADING",
        "CANCELING",
        "SUCCEEDED",
        "FAILED",
        "CANCELED",
        "EXCEEDED_LIMIT",
    ] = None
    tenantId: str = None
    type: Literal["hub", "chronos", "external", "automations", "data-refresh"] = None
    userId: str = None

    def __init__(self_, **kvargs):
        if "appId" in kvargs and kvargs["appId"] is not None:
            self_.appId = kvargs["appId"]
        if "creationTime" in kvargs and kvargs["creationTime"] is not None:
            self_.creationTime = kvargs["creationTime"]
        if "endTime" in kvargs and kvargs["endTime"] is not None:
            self_.endTime = kvargs["endTime"]
        if "engineTime" in kvargs and kvargs["engineTime"] is not None:
            self_.engineTime = kvargs["engineTime"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == Reload.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = ReloadLinks(**kvargs["links"])
        if "log" in kvargs and kvargs["log"] is not None:
            self_.log = kvargs["log"]
        if "partial" in kvargs and kvargs["partial"] is not None:
            self_.partial = kvargs["partial"]
        if "startTime" in kvargs and kvargs["startTime"] is not None:
            self_.startTime = kvargs["startTime"]
        if "status" in kvargs and kvargs["status"] is not None:
            self_.status = kvargs["status"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            self_.tenantId = kvargs["tenantId"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        if "userId" in kvargs and kvargs["userId"] is not None:
            self_.userId = kvargs["userId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def cancel(self) -> None:
        """
        Cancels a reload
        Cancels a reload that is in progress or has been queued

        Parameters
        ----------
        """
        self.auth.rest(
            path="/reloads/{reloadId}/actions/cancel".replace("{reloadId}", self.id),
            method="POST",
            params={},
            data=None,
        )


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


@dataclass
class ReloadLinks:
    """

    Attributes
    ----------
    self: Href
    """

    self: Href = None

    def __init__(self_, **kvargs):
        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == ReloadLinks.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Href(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ReloadRequest:
    """

    Attributes
    ----------
    appId: str
      The ID of the app to be reloaded.
    partial: bool
      The boolean value used to present the reload is partial or not
    """

    appId: str = None
    partial: bool = None

    def __init__(self_, **kvargs):
        if "appId" in kvargs and kvargs["appId"] is not None:
            self_.appId = kvargs["appId"]
        if "partial" in kvargs and kvargs["partial"] is not None:
            self_.partial = kvargs["partial"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ReloadsClass:
    """

    Attributes
    ----------
    data: list[Reload]
    links: ReloadsLinks
    """

    data: list[Reload] = None
    links: ReloadsLinks = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]" == ReloadsClass.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [Reload(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == ReloadsClass.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = ReloadsLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ReloadsLinks:
    """

    Attributes
    ----------
    self: Href
    next: Href
    prev: Href
    """

    self: Href = None
    next: Href = None
    prev: Href = None

    def __init__(self_, **kvargs):
        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == ReloadsLinks.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Href(**kvargs["self"])
        if "next" in kvargs and kvargs["next"] is not None:
            if type(kvargs["next"]).__name__ == ReloadsLinks.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = Href(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if type(kvargs["prev"]).__name__ == ReloadsLinks.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Href(**kvargs["prev"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Reloads:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get(self, reloadId: str) -> Reload:
        """
        Get reload record
        Finds and returns a reload record

        Parameters
        ----------
        reloadId: str
          The unique identifier of the reload.
        """
        response = self.auth.rest(
            path="/reloads/{reloadId}".replace("{reloadId}", reloadId),
            method="GET",
            params={},
            data=None,
        )
        obj = Reload(**response.json())
        obj.auth = self.auth
        return obj

    def get_reloads(
        self,
        appId: str,
        limit: int = 10,
        next: str = None,
        partial: bool = None,
        prev: str = None,
    ) -> ListableResource[Reload]:
        """
        Finds and returns the reloads that the user has access to.

        Parameters
        ----------
        appId: str
          The UUID formatted string used to search for an app's reload history entries. TenantAdmin users may omit this parameter to list all reload history in the tenant.
        limit: int = 10
          The maximum number of resources to return for a request. The limit must be an integer between 1 and 100 (inclusive).
        next: str = None
          The cursor to the next page of resources. Provide either the next or prev cursor, but not both.
        partial: bool = None
          The boolean value used to search for a reload is partial or not.
        prev: str = None
          The cursor to the previous page of resources. Provide either the next or prev cursor, but not both.
        """
        query_params = {}
        if appId is not None:
            query_params["appId"] = appId
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if partial is not None:
            query_params["partial"] = partial
        if prev is not None:
            query_params["prev"] = prev
        response = self.auth.rest(
            path="/reloads",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Reload,
            auth=self.auth,
            path="/reloads",
            query_params=query_params,
        )

    def create(self, data: ReloadRequest) -> Reload:
        """
        Reloads an app specified by an app ID.

        Parameters
        ----------
        data: ReloadRequest
          Request body specifying ID of app to be reloaded.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/reloads",
            method="POST",
            params={},
            data=data,
        )
        obj = Reload(**response.json())
        obj.auth = self.auth
        return obj
