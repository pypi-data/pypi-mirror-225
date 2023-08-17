# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

from dataclasses import dataclass

from ..auth import Auth, Config


@dataclass
class GetQuotaByIdResult:
    """

    Attributes
    ----------
    data: list[Quota]
      Quota item.
    """

    data: list[Quota] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == GetQuotaByIdResult.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [Quota(**e) for e in kvargs["data"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetQuotasResult:
    """

    Attributes
    ----------
    data: list[Quota]
      Array of quota items.
    """

    data: list[Quota] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]" == GetQuotasResult.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [Quota(**e) for e in kvargs["data"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Quota:
    """

    Attributes
    ----------
    attributes: QuotaAttributes
      The attributes of the quota.
    id: str
      The unique identifier of the quota item. For example, "app_mem_size", "app_upload_disk_size", or "shared_spaces".
    type: str
      The resource type of the quota item. Always equal to "quotas".
    """

    attributes: QuotaAttributes = None
    id: str = None
    type: str = None

    def __init__(self_, **kvargs):
        if "attributes" in kvargs and kvargs["attributes"] is not None:
            if (
                type(kvargs["attributes"]).__name__
                == Quota.__annotations__["attributes"]
            ):
                self_.attributes = kvargs["attributes"]
            else:
                self_.attributes = QuotaAttributes(**kvargs["attributes"])
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class QuotaAttributes:
    """
    The attributes of the quota.

    Attributes
    ----------
    quota: float
      The quota limit. If there is no quota limit, -1 is returned.
    unit: str
      The unit of the quota limit. For memory quotas, the unit is always "bytes". For other discrete units, the item counted is used as unit, for example "spaces".
    usage: float
      The current quota usage, if applicable. This attribute is only present if it is requested using the reportUsage query parameter.
    warningThresholds: list[float]
      The warning thresholds at which "close to quota" warnings can be issued when exceeded. If omitted, no warning threshold shall be used. Currently, the array will contain only one threshold value. In the future, this may be extended. The threshold is a number between 0 and 1, relating to the quota limit. For example, a value of 0.9 means that a warning should be issued when exceeding 90% of the quota limit.
    """

    quota: float = None
    unit: str = None
    usage: float = None
    warningThresholds: list[float] = None

    def __init__(self_, **kvargs):
        if "quota" in kvargs and kvargs["quota"] is not None:
            self_.quota = kvargs["quota"]
        if "unit" in kvargs and kvargs["unit"] is not None:
            self_.unit = kvargs["unit"]
        if "usage" in kvargs and kvargs["usage"] is not None:
            self_.usage = kvargs["usage"]
        if "warningThresholds" in kvargs and kvargs["warningThresholds"] is not None:
            self_.warningThresholds = kvargs["warningThresholds"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Quotas:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def gets(self, id: str, reportUsage: bool = None) -> GetQuotaByIdResult:
        """
        Returns a specific quota item for the tenant (provided in JWT).

        Parameters
        ----------
        id: str
          The unique identifier of the quota item. For example, "app_mem_size", "app_upload_disk_size", or "shared_spaces".
        reportUsage: bool = None
          The Boolean flag indicating whether quota usage shall be part of the response. The default value is false (usage not included).
        """
        query_params = {}
        if reportUsage is not None:
            query_params["reportUsage"] = reportUsage
        response = self.auth.rest(
            path="/quotas/{id}".replace("{id}", id),
            method="GET",
            params=query_params,
            data=None,
        )
        obj = GetQuotaByIdResult(**response.json())
        obj.auth = self.auth
        return obj

    def get_quotas(self, reportUsage: bool = None) -> GetQuotasResult:
        """
        Returns all quota items for the tenant (provided in JWT).

        Parameters
        ----------
        reportUsage: bool = None
          The Boolean flag indicating whether quota usage shall be part of the response. The default value is false (only limits returned).
        """
        query_params = {}
        if reportUsage is not None:
            query_params["reportUsage"] = reportUsage
        response = self.auth.rest(
            path="/quotas",
            method="GET",
            params=query_params,
            data=None,
        )
        obj = GetQuotasResult(**response.json())
        obj.auth = self.auth
        return obj
