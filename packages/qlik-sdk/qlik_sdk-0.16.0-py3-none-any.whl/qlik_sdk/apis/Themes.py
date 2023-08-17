# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

import io
import json
from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..utils import get_mime_type


@dataclass
class Theme:
    """
    The theme model.

    Attributes
    ----------
    author: str
      Author of the theme.
    createdAt: str
    dependencies: object
      Map of dependencies describing version of the component it requires.
    description: str
      Description of the theme.
    file: object
      The file that was uploaded with the theme.
    homepage: str
      Home page of the theme.
    icon: str
      Icon to show in the client.
    id: str
    keywords: str
      Keywords for the theme.
    license: str
      Under which license this theme is published.
    name: str
      The display name of this theme.
    qextFilename: str
      The name of the qext file that was uploaded with this theme.
    qextVersion: str
      The version from the qext file that was uploaded with this extension.
    repository: str
      Link to the theme source code.
    supplier: str
      Supplier of the theme.
    tags: list[str]
      List of tags.
    tenantId: str
    type: str
      The type of this theme (visualization, etc.).
    updateAt: str
    userId: str
    version: str
      Version of the theme.
    """

    author: str = None
    createdAt: str = None
    dependencies: object = None
    description: str = None
    file: object = None
    homepage: str = None
    icon: str = None
    id: str = None
    keywords: str = None
    license: str = None
    name: str = None
    qextFilename: str = None
    qextVersion: str = None
    repository: str = None
    supplier: str = None
    tags: list[str] = None
    tenantId: str = None
    type: str = None
    updateAt: str = None
    userId: str = None
    version: str = None

    def __init__(self_, **kvargs):
        if "author" in kvargs and kvargs["author"] is not None:
            self_.author = kvargs["author"]
        if "createdAt" in kvargs and kvargs["createdAt"] is not None:
            self_.createdAt = kvargs["createdAt"]
        if "dependencies" in kvargs and kvargs["dependencies"] is not None:
            self_.dependencies = kvargs["dependencies"]
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "file" in kvargs and kvargs["file"] is not None:
            self_.file = kvargs["file"]
        if "homepage" in kvargs and kvargs["homepage"] is not None:
            self_.homepage = kvargs["homepage"]
        if "icon" in kvargs and kvargs["icon"] is not None:
            self_.icon = kvargs["icon"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "keywords" in kvargs and kvargs["keywords"] is not None:
            self_.keywords = kvargs["keywords"]
        if "license" in kvargs and kvargs["license"] is not None:
            self_.license = kvargs["license"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "qextFilename" in kvargs and kvargs["qextFilename"] is not None:
            self_.qextFilename = kvargs["qextFilename"]
        if "qextVersion" in kvargs and kvargs["qextVersion"] is not None:
            self_.qextVersion = kvargs["qextVersion"]
        if "repository" in kvargs and kvargs["repository"] is not None:
            self_.repository = kvargs["repository"]
        if "supplier" in kvargs and kvargs["supplier"] is not None:
            self_.supplier = kvargs["supplier"]
        if "tags" in kvargs and kvargs["tags"] is not None:
            self_.tags = kvargs["tags"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            self_.tenantId = kvargs["tenantId"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        if "updateAt" in kvargs and kvargs["updateAt"] is not None:
            self_.updateAt = kvargs["updateAt"]
        if "userId" in kvargs and kvargs["userId"] is not None:
            self_.userId = kvargs["userId"]
        if "version" in kvargs and kvargs["version"] is not None:
            self_.version = kvargs["version"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def get_file_by_filepath(self, filepath: str) -> None:
        """
        Downloads a file from the theme archive.

        Parameters
        ----------
        filepath: str
          Path to the file archive for the specified theme archive. Folders separated with forward slashes.
        """
        self.auth.rest(
            path="/themes/{id}/file/{filepath}".replace("{filepath}", filepath).replace(
                "{id}", self.id
            ),
            method="GET",
            params={},
            data=None,
        )

    def get_file(self) -> None:
        """
        Downloads the theme as an archive.

        Parameters
        ----------
        """
        self.auth.rest(
            path="/themes/{id}/file".replace("{id}", self.id),
            method="GET",
            params={},
            data=None,
        )

    def delete(self) -> None:
        """
        Deletes a specific theme.

        Parameters
        ----------
        """
        self.auth.rest(
            path="/themes/{id}".replace("{id}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def patches(
        self, data: Theme = None, file: io.BufferedReader = None
    ) -> ThemesClass:
        """
        Updates a specific theme with provided data. If a file is provided, the data field is not required.

        Parameters
        ----------
        data: Theme = None
        file: str = None
          Theme archive.
        """
        files_dict = {}
        files_dict["file"] = ("file", file, get_mime_type(file))
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
            files_dict["data"] = (None, json.dumps(data))
        response = self.auth.rest(
            path="/themes/{id}".replace("{id}", self.id),
            method="PATCH",
            params={},
            data=None,
            files=files_dict,
        )
        obj = ThemesClass(**response.json())
        obj.auth = self.auth
        return obj


@dataclass
class ThemeDef:
    """
    The theme model.

    Attributes
    ----------
    author: str
      Author of the theme.
    dependencies: object
      Map of dependencies describing version of the component it requires.
    description: str
      Description of the theme.
    file: object
      The file that was uploaded with the theme.
    homepage: str
      Home page of the theme.
    icon: str
      Icon to show in the client.
    keywords: str
      Keywords for the theme.
    license: str
      Under which license this theme is published.
    name: str
      The display name of this theme.
    qextFilename: str
      The name of the qext file that was uploaded with this theme.
    qextVersion: str
      The version from the qext file that was uploaded with this extension.
    repository: str
      Link to the theme source code.
    supplier: str
      Supplier of the theme.
    tags: list[str]
      List of tags.
    type: str
      The type of this theme (visualization, etc.).
    version: str
      Version of the theme.
    """

    author: str = None
    dependencies: object = None
    description: str = None
    file: object = None
    homepage: str = None
    icon: str = None
    keywords: str = None
    license: str = None
    name: str = None
    qextFilename: str = None
    qextVersion: str = None
    repository: str = None
    supplier: str = None
    tags: list[str] = None
    type: str = None
    version: str = None

    def __init__(self_, **kvargs):
        if "author" in kvargs and kvargs["author"] is not None:
            self_.author = kvargs["author"]
        if "dependencies" in kvargs and kvargs["dependencies"] is not None:
            self_.dependencies = kvargs["dependencies"]
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "file" in kvargs and kvargs["file"] is not None:
            self_.file = kvargs["file"]
        if "homepage" in kvargs and kvargs["homepage"] is not None:
            self_.homepage = kvargs["homepage"]
        if "icon" in kvargs and kvargs["icon"] is not None:
            self_.icon = kvargs["icon"]
        if "keywords" in kvargs and kvargs["keywords"] is not None:
            self_.keywords = kvargs["keywords"]
        if "license" in kvargs and kvargs["license"] is not None:
            self_.license = kvargs["license"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "qextFilename" in kvargs and kvargs["qextFilename"] is not None:
            self_.qextFilename = kvargs["qextFilename"]
        if "qextVersion" in kvargs and kvargs["qextVersion"] is not None:
            self_.qextVersion = kvargs["qextVersion"]
        if "repository" in kvargs and kvargs["repository"] is not None:
            self_.repository = kvargs["repository"]
        if "supplier" in kvargs and kvargs["supplier"] is not None:
            self_.supplier = kvargs["supplier"]
        if "tags" in kvargs and kvargs["tags"] is not None:
            self_.tags = kvargs["tags"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        if "version" in kvargs and kvargs["version"] is not None:
            self_.version = kvargs["version"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ThemesClass:
    """

    Attributes
    ----------
    data: list[Theme]
    """

    data: list[Theme] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]" == ThemesClass.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [Theme(**e) for e in kvargs["data"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Themes:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get(self, id: str) -> Theme:
        """
        Returns a specific theme.

        Parameters
        ----------
        id: str
          Theme identifier or its qextFilename
        """
        response = self.auth.rest(
            path="/themes/{id}".replace("{id}", id),
            method="GET",
            params={},
            data=None,
        )
        obj = Theme(**response.json())
        obj.auth = self.auth
        return obj

    def get_themes(self) -> ThemesClass:
        """
        Lists all themes.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/themes",
            method="GET",
            params={},
            data=None,
        )
        obj = ThemesClass(**response.json())
        obj.auth = self.auth
        return obj

    def create(self, data: ThemeDef = None, file: io.BufferedReader = None) -> Theme:
        """
        Creates a new theme. If a file is provided, the data field is not required.

        Parameters
        ----------
        data: ThemeDef = None
        file: str = None
          Theme archive.
        """
        files_dict = {}
        files_dict["file"] = ("file", file, get_mime_type(file))
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
            files_dict["data"] = (None, json.dumps(data))
        response = self.auth.rest(
            path="/themes", method="POST", params={}, data=None, files=files_dict
        )
        obj = Theme(**response.json())
        obj.auth = self.auth
        return obj
