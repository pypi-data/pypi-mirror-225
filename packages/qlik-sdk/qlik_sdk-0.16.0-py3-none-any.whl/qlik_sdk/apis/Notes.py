# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

from ..auth import Auth, Config


@dataclass
class NoteSettingsPutPayload:
    """

    Attributes
    ----------
    snapshotRelations: bool
      pass 'true' to enable the relations api to search notes for the tenant.
    toggledOn: bool
      pass 'true' to enable the note toggle for the tenant, 'false' to disable the toggle (other values are ignore).
    """

    snapshotRelations: bool = None
    toggledOn: bool = None

    def __init__(self_, **kvargs):
        if "snapshotRelations" in kvargs and kvargs["snapshotRelations"] is not None:
            self_.snapshotRelations = kvargs["snapshotRelations"]
        if "toggledOn" in kvargs and kvargs["toggledOn"] is not None:
            self_.toggledOn = kvargs["toggledOn"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NoteSettingsPutResponse:
    """

    Attributes
    ----------
    snapshotRelations: bool
      'true' if relations api to search notes for the tenant are enabled else false.
    toggleOn: bool
      'true' if the note feature is enabled for this tenant and user otherwise 'false'.
    """

    snapshotRelations: bool = None
    toggleOn: bool = None

    def __init__(self_, **kvargs):
        if "snapshotRelations" in kvargs and kvargs["snapshotRelations"] is not None:
            self_.snapshotRelations = kvargs["snapshotRelations"]
        if "toggleOn" in kvargs and kvargs["toggleOn"] is not None:
            self_.toggleOn = kvargs["toggleOn"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NotesUserSettings:
    """

    Attributes
    ----------
    available: bool
      'true' if the note feature is enabled for this tenant and user otherwise 'false'.
    lastFetch: str
      The timestamp for the last time this users notes settings were fetched from downstream services.
    reason: Literal["deployment", "toggle", "license"]
      The possible states for the status of notes configuration GET or POST operation
    """

    available: bool = None
    lastFetch: str = None
    reason: Literal["deployment", "toggle", "license"] = None

    def __init__(self_, **kvargs):
        if "available" in kvargs and kvargs["available"] is not None:
            self_.available = kvargs["available"]
        if "lastFetch" in kvargs and kvargs["lastFetch"] is not None:
            self_.lastFetch = kvargs["lastFetch"]
        if "reason" in kvargs and kvargs["reason"] is not None:
            self_.reason = kvargs["reason"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Notes:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_settings(self) -> NotesUserSettings:
        """
        Get the enablement status of the notes feature set for this tenant and user.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/notes/settings",
            method="GET",
            params={},
            data=None,
        )
        obj = NotesUserSettings(**response.json())
        obj.auth = self.auth
        return obj

    def set_settings(self, data: NoteSettingsPutPayload) -> NoteSettingsPutResponse:
        """
        update the settings

        Parameters
        ----------
        data: NoteSettingsPutPayload
          A JSON payload containing note settings to put.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/notes/settings",
            method="PUT",
            params={},
            data=data,
        )
        obj = NoteSettingsPutResponse(**response.json())
        obj.auth = self.auth
        return obj
