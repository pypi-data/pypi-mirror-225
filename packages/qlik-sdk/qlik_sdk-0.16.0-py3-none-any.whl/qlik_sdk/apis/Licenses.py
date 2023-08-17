# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class AssignmentsActionsAddRequest:
    """

    Attributes
    ----------
    add: list[AssignmentsActionsAddRequestAdd]
    """

    add: list[AssignmentsActionsAddRequestAdd] = None

    def __init__(self_, **kvargs):
        if "add" in kvargs and kvargs["add"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == AssignmentsActionsAddRequest.__annotations__["add"]
                for e in kvargs["add"]
            ):
                self_.add = kvargs["add"]
            else:
                self_.add = [
                    AssignmentsActionsAddRequestAdd(**e) for e in kvargs["add"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsAddRequestAdd:
    """

    Attributes
    ----------
    name: str
      User name
    subject: str
      User subject
    type: str
      Allotment type
    userId: str
      User ID
    """

    name: str = None
    subject: str = None
    type: str = None
    userId: str = None

    def __init__(self_, **kvargs):
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "subject" in kvargs and kvargs["subject"] is not None:
            self_.subject = kvargs["subject"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        if "userId" in kvargs and kvargs["userId"] is not None:
            self_.userId = kvargs["userId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsAddResponse:
    """

    Attributes
    ----------
    data: list[AssignmentsActionsAddResponseData]
    """

    data: list[AssignmentsActionsAddResponseData] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == AssignmentsActionsAddResponse.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [
                    AssignmentsActionsAddResponseData(**e) for e in kvargs["data"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsAddResponseData:
    """

    Attributes
    ----------
    code: str
      Error code
    status: int
      Response status
    subject: str
      Subject
    title: str
      Error title
    type: str
      Allotment type
    """

    code: str = None
    status: int = None
    subject: str = None
    title: str = None
    type: str = None

    def __init__(self_, **kvargs):
        if "code" in kvargs and kvargs["code"] is not None:
            self_.code = kvargs["code"]
        if "status" in kvargs and kvargs["status"] is not None:
            self_.status = kvargs["status"]
        if "subject" in kvargs and kvargs["subject"] is not None:
            self_.subject = kvargs["subject"]
        if "title" in kvargs and kvargs["title"] is not None:
            self_.title = kvargs["title"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsDeleteRequest:
    """

    Attributes
    ----------
    delete: list[AssignmentsActionsDeleteRequestDelete]
    """

    delete: list[AssignmentsActionsDeleteRequestDelete] = None

    def __init__(self_, **kvargs):
        if "delete" in kvargs and kvargs["delete"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == AssignmentsActionsDeleteRequest.__annotations__["delete"]
                for e in kvargs["delete"]
            ):
                self_.delete = kvargs["delete"]
            else:
                self_.delete = [
                    AssignmentsActionsDeleteRequestDelete(**e) for e in kvargs["delete"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsDeleteRequestDelete:
    """

    Attributes
    ----------
    subject: str
      User subject
    type: str
      Allotment type
    """

    subject: str = None
    type: str = None

    def __init__(self_, **kvargs):
        if "subject" in kvargs and kvargs["subject"] is not None:
            self_.subject = kvargs["subject"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsDeleteResponse:
    """

    Attributes
    ----------
    data: list[AssignmentsActionsDeleteResponseData]
    """

    data: list[AssignmentsActionsDeleteResponseData] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == AssignmentsActionsDeleteResponse.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [
                    AssignmentsActionsDeleteResponseData(**e) for e in kvargs["data"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsDeleteResponseData:
    """

    Attributes
    ----------
    code: str
      Error code
    status: int
      Response status
    subject: str
      Subject
    title: str
      Error title
    type: str
      Allotment type
    """

    code: str = None
    status: int = None
    subject: str = None
    title: str = None
    type: str = None

    def __init__(self_, **kvargs):
        if "code" in kvargs and kvargs["code"] is not None:
            self_.code = kvargs["code"]
        if "status" in kvargs and kvargs["status"] is not None:
            self_.status = kvargs["status"]
        if "subject" in kvargs and kvargs["subject"] is not None:
            self_.subject = kvargs["subject"]
        if "title" in kvargs and kvargs["title"] is not None:
            self_.title = kvargs["title"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsUpdateRequest:
    """

    Attributes
    ----------
    update: list[AssignmentsActionsUpdateRequestUpdate]
    """

    update: list[AssignmentsActionsUpdateRequestUpdate] = None

    def __init__(self_, **kvargs):
        if "update" in kvargs and kvargs["update"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == AssignmentsActionsUpdateRequest.__annotations__["update"]
                for e in kvargs["update"]
            ):
                self_.update = kvargs["update"]
            else:
                self_.update = [
                    AssignmentsActionsUpdateRequestUpdate(**e) for e in kvargs["update"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsUpdateRequestUpdate:
    """

    Attributes
    ----------
    sourceType: str
      Current assignment type.
    subject: str
      User subject
    type: str
      Target assignment type.
    """

    sourceType: str = None
    subject: str = None
    type: str = None

    def __init__(self_, **kvargs):
        if "sourceType" in kvargs and kvargs["sourceType"] is not None:
            self_.sourceType = kvargs["sourceType"]
        if "subject" in kvargs and kvargs["subject"] is not None:
            self_.subject = kvargs["subject"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsUpdateResponse:
    """

    Attributes
    ----------
    data: list[AssignmentsActionsUpdateResponseData]
    """

    data: list[AssignmentsActionsUpdateResponseData] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == AssignmentsActionsUpdateResponse.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [
                    AssignmentsActionsUpdateResponseData(**e) for e in kvargs["data"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsUpdateResponseData:
    """

    Attributes
    ----------
    code: str
      Error code
    sourceType: str
      Current allotment type.
    status: int
      Response status
    subject: str
      Subject
    title: str
      Error title
    type: str
      Target allotment type.
    """

    code: str = None
    sourceType: str = None
    status: int = None
    subject: str = None
    title: str = None
    type: str = None

    def __init__(self_, **kvargs):
        if "code" in kvargs and kvargs["code"] is not None:
            self_.code = kvargs["code"]
        if "sourceType" in kvargs and kvargs["sourceType"] is not None:
            self_.sourceType = kvargs["sourceType"]
        if "status" in kvargs and kvargs["status"] is not None:
            self_.status = kvargs["status"]
        if "subject" in kvargs and kvargs["subject"] is not None:
            self_.subject = kvargs["subject"]
        if "title" in kvargs and kvargs["title"] is not None:
            self_.title = kvargs["title"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsResponse:
    """

    Attributes
    ----------
    data: list[AssignmentsResponseData]
    links: AssignmentsResponseLinks
    """

    data: list[AssignmentsResponseData] = None
    links: AssignmentsResponseLinks = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == AssignmentsResponse.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [AssignmentsResponseData(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == AssignmentsResponse.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = AssignmentsResponseLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsResponseData:
    """

    Attributes
    ----------
    created: str
      Assignment created date.
    excess: bool
      Assignment excess status.
    name: str
      User name
    subject: str
      Subject
    type: str
      Allotment type
    userId: str
      User ID
    """

    created: str = None
    excess: bool = None
    name: str = None
    subject: str = None
    type: str = None
    userId: str = None

    def __init__(self_, **kvargs):
        if "created" in kvargs and kvargs["created"] is not None:
            self_.created = kvargs["created"]
        if "excess" in kvargs and kvargs["excess"] is not None:
            self_.excess = kvargs["excess"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "subject" in kvargs and kvargs["subject"] is not None:
            self_.subject = kvargs["subject"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        if "userId" in kvargs and kvargs["userId"] is not None:
            self_.userId = kvargs["userId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsResponseLinks:
    """

    Attributes
    ----------
    next: Href
    prev: Href
    """

    next: Href = None
    prev: Href = None

    def __init__(self_, **kvargs):
        if "next" in kvargs and kvargs["next"] is not None:
            if (
                type(kvargs["next"]).__name__
                == AssignmentsResponseLinks.__annotations__["next"]
            ):
                self_.next = kvargs["next"]
            else:
                self_.next = Href(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if (
                type(kvargs["prev"]).__name__
                == AssignmentsResponseLinks.__annotations__["prev"]
            ):
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Href(**kvargs["prev"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ConsumptionEventsResponse:
    """

    Attributes
    ----------
    data: list[ConsumptionEventsResponseData]
    links: ConsumptionEventsResponseLinks
    """

    data: list[ConsumptionEventsResponseData] = None
    links: ConsumptionEventsResponseLinks = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == ConsumptionEventsResponse.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [
                    ConsumptionEventsResponseData(**e) for e in kvargs["data"]
                ]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == ConsumptionEventsResponse.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = ConsumptionEventsResponseLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ConsumptionEventsResponseData:
    """

    Attributes
    ----------
    allotmentId: str
      Allotment ID
    appId: str
      App ID
    capacityUsed: int
      Analyzer capacity chunks consumed.
    duration: str
      Engine session duration.
    endTime: str
      Engine session end time.
    id: str
      ID
    licenseUsage: str
      License usage
    minutesUsed: int
      Analyzer capacity minutes consumed.
    sessionId: str
      Engine session ID.
    userId: str
      User ID
    """

    allotmentId: str = None
    appId: str = None
    capacityUsed: int = None
    duration: str = None
    endTime: str = None
    id: str = None
    licenseUsage: str = None
    minutesUsed: int = None
    sessionId: str = None
    userId: str = None

    def __init__(self_, **kvargs):
        if "allotmentId" in kvargs and kvargs["allotmentId"] is not None:
            self_.allotmentId = kvargs["allotmentId"]
        if "appId" in kvargs and kvargs["appId"] is not None:
            self_.appId = kvargs["appId"]
        if "capacityUsed" in kvargs and kvargs["capacityUsed"] is not None:
            self_.capacityUsed = kvargs["capacityUsed"]
        if "duration" in kvargs and kvargs["duration"] is not None:
            self_.duration = kvargs["duration"]
        if "endTime" in kvargs and kvargs["endTime"] is not None:
            self_.endTime = kvargs["endTime"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "licenseUsage" in kvargs and kvargs["licenseUsage"] is not None:
            self_.licenseUsage = kvargs["licenseUsage"]
        if "minutesUsed" in kvargs and kvargs["minutesUsed"] is not None:
            self_.minutesUsed = kvargs["minutesUsed"]
        if "sessionId" in kvargs and kvargs["sessionId"] is not None:
            self_.sessionId = kvargs["sessionId"]
        if "userId" in kvargs and kvargs["userId"] is not None:
            self_.userId = kvargs["userId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ConsumptionEventsResponseLinks:
    """

    Attributes
    ----------
    next: Href
    prev: Href
    """

    next: Href = None
    prev: Href = None

    def __init__(self_, **kvargs):
        if "next" in kvargs and kvargs["next"] is not None:
            if (
                type(kvargs["next"]).__name__
                == ConsumptionEventsResponseLinks.__annotations__["next"]
            ):
                self_.next = kvargs["next"]
            else:
                self_.next = Href(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if (
                type(kvargs["prev"]).__name__
                == ConsumptionEventsResponseLinks.__annotations__["prev"]
            ):
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Href(**kvargs["prev"])
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
      link
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
class LicenseOverview:
    """

    Attributes
    ----------
    allotments: list[LicenseOverviewAllotments]
    changeTime: str
      An ISO 8601 timestamp for when the license was last changed.
    latestValidTime: str
      An ISO 8601 timestamp for when the latest time the license has been known to be valid, a missing value indicates the indefinite future.
    licenseKey: str
    licenseNumber: str
    licenseType: str
    origin: Literal["Internal", "External"]
      Origin of license key.
    parameters: list[LicenseOverviewParameters]
      The license parameters.
    product: str
      The product the license is valid for.
    secondaryNumber: str
      The secondary number of a definition.
    status: Literal["Ok", "Blacklisted", "Expired"]
      Enum with status of license. Only status Ok grants license. access.
    trial: bool
      Boolean indicating if it is a trial license.
    updated: str
      An ISO 8601 timestamp for when the license was last updated.
    valid: str
      Period that the license is currently set to be active. Represented as an ISO 8601 time interval with start and end.
    """

    allotments: list[LicenseOverviewAllotments] = None
    changeTime: str = None
    latestValidTime: str = None
    licenseKey: str = None
    licenseNumber: str = None
    licenseType: str = None
    origin: Literal["Internal", "External"] = None
    parameters: list[LicenseOverviewParameters] = None
    product: str = None
    secondaryNumber: str = None
    status: Literal["Ok", "Blacklisted", "Expired"] = None
    trial: bool = None
    updated: str = None
    valid: str = None

    def __init__(self_, **kvargs):
        if "allotments" in kvargs and kvargs["allotments"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == LicenseOverview.__annotations__["allotments"]
                for e in kvargs["allotments"]
            ):
                self_.allotments = kvargs["allotments"]
            else:
                self_.allotments = [
                    LicenseOverviewAllotments(**e) for e in kvargs["allotments"]
                ]
        if "changeTime" in kvargs and kvargs["changeTime"] is not None:
            self_.changeTime = kvargs["changeTime"]
        if "latestValidTime" in kvargs and kvargs["latestValidTime"] is not None:
            self_.latestValidTime = kvargs["latestValidTime"]
        if "licenseKey" in kvargs and kvargs["licenseKey"] is not None:
            self_.licenseKey = kvargs["licenseKey"]
        if "licenseNumber" in kvargs and kvargs["licenseNumber"] is not None:
            self_.licenseNumber = kvargs["licenseNumber"]
        if "licenseType" in kvargs and kvargs["licenseType"] is not None:
            self_.licenseType = kvargs["licenseType"]
        if "origin" in kvargs and kvargs["origin"] is not None:
            self_.origin = kvargs["origin"]
        if "parameters" in kvargs and kvargs["parameters"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == LicenseOverview.__annotations__["parameters"]
                for e in kvargs["parameters"]
            ):
                self_.parameters = kvargs["parameters"]
            else:
                self_.parameters = [
                    LicenseOverviewParameters(**e) for e in kvargs["parameters"]
                ]
        if "product" in kvargs and kvargs["product"] is not None:
            self_.product = kvargs["product"]
        if "secondaryNumber" in kvargs and kvargs["secondaryNumber"] is not None:
            self_.secondaryNumber = kvargs["secondaryNumber"]
        if "status" in kvargs and kvargs["status"] is not None:
            self_.status = kvargs["status"]
        if "trial" in kvargs and kvargs["trial"] is not None:
            self_.trial = kvargs["trial"]
        if "updated" in kvargs and kvargs["updated"] is not None:
            self_.updated = kvargs["updated"]
        if "valid" in kvargs and kvargs["valid"] is not None:
            self_.valid = kvargs["valid"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LicenseOverviewAllotments:
    """

    Attributes
    ----------
    name: Literal["professional", "analyzer", "analyzer_time"]
    overage: int
      Overage value; -1 means unbounded overage.
    units: int
    unitsUsed: int
    usageClass: str
    """

    name: Literal["professional", "analyzer", "analyzer_time"] = None
    overage: int = None
    units: int = None
    unitsUsed: int = None
    usageClass: str = None

    def __init__(self_, **kvargs):
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "overage" in kvargs and kvargs["overage"] is not None:
            self_.overage = kvargs["overage"]
        if "units" in kvargs and kvargs["units"] is not None:
            self_.units = kvargs["units"]
        if "unitsUsed" in kvargs and kvargs["unitsUsed"] is not None:
            self_.unitsUsed = kvargs["unitsUsed"]
        if "usageClass" in kvargs and kvargs["usageClass"] is not None:
            self_.usageClass = kvargs["usageClass"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LicenseOverviewParameters:
    """

    Attributes
    ----------
    access: LicenseOverviewParametersAccess
      Parameters for licenses to control access to the parameters.
    name: str
      Parameter set (provision) name.
    valid: str
      Time interval for parameter validity.
    values: LicenseOverviewParametersValues
      Parameter values
    """

    access: LicenseOverviewParametersAccess = None
    name: str = None
    valid: str = None
    values: LicenseOverviewParametersValues = None

    def __init__(self_, **kvargs):
        if "access" in kvargs and kvargs["access"] is not None:
            if (
                type(kvargs["access"]).__name__
                == LicenseOverviewParameters.__annotations__["access"]
            ):
                self_.access = kvargs["access"]
            else:
                self_.access = LicenseOverviewParametersAccess(**kvargs["access"])
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "valid" in kvargs and kvargs["valid"] is not None:
            self_.valid = kvargs["valid"]
        if "values" in kvargs and kvargs["values"] is not None:
            if (
                type(kvargs["values"]).__name__
                == LicenseOverviewParameters.__annotations__["values"]
            ):
                self_.values = kvargs["values"]
            else:
                self_.values = LicenseOverviewParametersValues(**kvargs["values"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LicenseOverviewParametersAccess:
    """
    Parameters for licenses to control access to the parameters.

    Attributes
    ----------
    allotment: str
      Name of an allotment that the user must have access to. to
    """

    allotment: str = None

    def __init__(self_, **kvargs):
        if "allotment" in kvargs and kvargs["allotment"] is not None:
            self_.allotment = kvargs["allotment"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LicenseOverviewParametersValues:
    """
    Parameter values

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LicenseStatus:
    """

    Attributes
    ----------
    origin: Literal["Internal", "External"]
      Origin of license key.
    product: str
      The product the license is valid for.
    status: Literal["Ok", "Blacklisted", "Expired", "Missing"]
      Enum with status of license. Only status Ok grants license. access.
    trial: bool
      Boolean indicating if it is a trial license.
    type: Literal["Signed", "Plain"]
      Type of license key.
    valid: str
      Period that the license is currently set to be active. Represented as an ISO 8601 time interval with start and end.
    """

    origin: Literal["Internal", "External"] = None
    product: str = None
    status: Literal["Ok", "Blacklisted", "Expired", "Missing"] = None
    trial: bool = None
    type: Literal["Signed", "Plain"] = None
    valid: str = None

    def __init__(self_, **kvargs):
        if "origin" in kvargs and kvargs["origin"] is not None:
            self_.origin = kvargs["origin"]
        if "product" in kvargs and kvargs["product"] is not None:
            self_.product = kvargs["product"]
        if "status" in kvargs and kvargs["status"] is not None:
            self_.status = kvargs["status"]
        if "trial" in kvargs and kvargs["trial"] is not None:
            self_.trial = kvargs["trial"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        if "valid" in kvargs and kvargs["valid"] is not None:
            self_.valid = kvargs["valid"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SettingsBody:
    """

    Attributes
    ----------
    autoAssignAnalyzer: bool
      If analyzer users are available, they will be automatically assigned. Otherwise, analyzer capacity will be assigned, if available.
    autoAssignProfessional: bool
      If professional users are available, they will be automatically assigned. Otherwise, analyzer capacity will be assigned, if available.
    """

    autoAssignAnalyzer: bool = None
    autoAssignProfessional: bool = None

    def __init__(self_, **kvargs):
        if "autoAssignAnalyzer" in kvargs and kvargs["autoAssignAnalyzer"] is not None:
            self_.autoAssignAnalyzer = kvargs["autoAssignAnalyzer"]
        if (
            "autoAssignProfessional" in kvargs
            and kvargs["autoAssignProfessional"] is not None
        ):
            self_.autoAssignProfessional = kvargs["autoAssignProfessional"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Licenses:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def add_assignments(
        self, data: AssignmentsActionsAddRequest
    ) -> AssignmentsActionsAddResponse:
        """
        Assigns license access to the given users

        Parameters
        ----------
        data: AssignmentsActionsAddRequest
          List of subjects to allocate assignments for.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/licenses/assignments/actions/add",
            method="POST",
            params={},
            data=data,
        )
        obj = AssignmentsActionsAddResponse(**response.json())
        obj.auth = self.auth
        return obj

    def delete_assignments(
        self, data: AssignmentsActionsDeleteRequest
    ) -> AssignmentsActionsDeleteResponse:
        """
        Removes license access for the given users

        Parameters
        ----------
        data: AssignmentsActionsDeleteRequest
          List of assignments to delete.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/licenses/assignments/actions/delete",
            method="POST",
            params={},
            data=data,
        )
        obj = AssignmentsActionsDeleteResponse(**response.json())
        obj.auth = self.auth
        return obj

    def update_assignments(
        self, data: AssignmentsActionsUpdateRequest
    ) -> AssignmentsActionsUpdateResponse:
        """
        Updates license access for the given users

        Parameters
        ----------
        data: AssignmentsActionsUpdateRequest
          List of assignments to update.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/licenses/assignments/actions/update",
            method="POST",
            params={},
            data=data,
        )
        obj = AssignmentsActionsUpdateResponse(**response.json())
        obj.auth = self.auth
        return obj

    def get_assignments(
        self, filter: str = None, limit: int = 20, page: str = None, sort: str = None
    ) -> ListableResource[AssignmentsResponseData]:
        """
        Retrieves assignments for the current tenant

        Parameters
        ----------
        filter: str = None
          The filter for finding entries.
        limit: int = 20
          The preferred number of entries to return.
        page: str = None
          The requested page.
        sort: str = None
          The field to sort on; can be prefixed with +/- for ascending/descending sort order.
        """
        query_params = {}
        if filter is not None:
            query_params["filter"] = filter
        if limit is not None:
            query_params["limit"] = limit
        if page is not None:
            query_params["page"] = page
        if sort is not None:
            query_params["sort"] = sort
        response = self.auth.rest(
            path="/licenses/assignments",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=AssignmentsResponseData,
            auth=self.auth,
            path="/licenses/assignments",
            query_params=query_params,
        )

    def get_consumptions(
        self, filter: str = None, limit: int = 200, page: str = None, sort: str = None
    ) -> ListableResource[ConsumptionEventsResponseData]:
        """
        Retrieves license consumption for the current tenant

        Parameters
        ----------
        filter: str = None
          The filter for finding entries.
        limit: int = 200
          The preferred number of entries to return.
        page: str = None
          The requested page.
        sort: str = None
          The field to sort on; can be prefixed with +/- for ascending/descending sort order.
        """
        query_params = {}
        if filter is not None:
            query_params["filter"] = filter
        if limit is not None:
            query_params["limit"] = limit
        if page is not None:
            query_params["page"] = page
        if sort is not None:
            query_params["sort"] = sort
        response = self.auth.rest(
            path="/licenses/consumption",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=ConsumptionEventsResponseData,
            auth=self.auth,
            path="/licenses/consumption",
            query_params=query_params,
        )

    def get_overview(self) -> LicenseOverview:
        """
        Gets the general information of the license applied to the current tenant

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/licenses/overview",
            method="GET",
            params={},
            data=None,
        )
        obj = LicenseOverview(**response.json())
        obj.auth = self.auth
        return obj

    def get_settings(self) -> SettingsBody:
        """
        Get auto assign settings for tenant.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/licenses/settings",
            method="GET",
            params={},
            data=None,
        )
        obj = SettingsBody(**response.json())
        obj.auth = self.auth
        return obj

    def set_settings(self, data: SettingsBody = None) -> SettingsBody:
        """
        Set auto assign settings for tenant

        Parameters
        ----------
        data: SettingsBody = None
          Dynamic assignment settings for professional and analyzer users. If professional users and analyzer users are both set, professional users will be automatically assigned, if available. Otherwise, analyzer users will be assigned. If neither of those users are available, analyzer capacity will be assigned, if available.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/licenses/settings",
            method="PUT",
            params={},
            data=data,
        )
        obj = SettingsBody(**response.json())
        obj.auth = self.auth
        return obj

    def get_status(self) -> LicenseStatus:
        """
        Gets the license status information of the current tenant

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/licenses/status",
            method="GET",
            params={},
            data=None,
        )
        obj = LicenseStatus(**response.json())
        obj.auth = self.auth
        return obj
