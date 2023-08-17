# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

import io
import json
from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..utils import get_mime_type


@dataclass
class Extension:
    """
    The extension model.

    Attributes
    ----------
    author: str
      Author of the extension.
    bundle: BundleMeta
      Object containing meta data regarding the bundle the extension belongs to. If it does not belong to a bundle, this object is not defined.
    bundled: bool
      If the extension is part of an extension bundle.
    checksum: str
      Checksum of the extension contents.
    createdAt: str
    dependencies: object
      Map of dependencies describing version of the component it requires.
    deprecated: str
      A date noting when the extension was deprecated.
    description: str
      Description of the extension.
    file: object
      The file that was uploaded with the extension.
    homepage: str
      Home page of the extension.
    icon: str
      Icon to show in the client.
    id: str
    keywords: str
      Keywords for the extension.
    license: str
      Under which license this extension is published.
    loadpath: str
      Relative path to the extension's entry file, defaults to `filename` from the qext file.
    name: str
      The display name of this extension.
    preview: str
      Path to an image that enables users to preview the extension.
    qextFilename: str
      The name of the qext file that was uploaded with this extension.
    qextVersion: str
      The version from the qext file that was uploaded with this extension.
    repository: str
      Link to the extension source code.
    supernova: bool
      If the extension is a supernova extension or not.
    supplier: str
      Supplier of the extension.
    tags: list[str]
      List of tags.
    tenantId: str
    type: str
      The type of this extension (visualization, etc.).
    updateAt: str
    userId: str
    version: str
      Version of the extension.
    """

    author: str = None
    bundle: BundleMeta = None
    bundled: bool = None
    checksum: str = None
    createdAt: str = None
    dependencies: object = None
    deprecated: str = None
    description: str = None
    file: object = None
    homepage: str = None
    icon: str = None
    id: str = None
    keywords: str = None
    license: str = None
    loadpath: str = None
    name: str = None
    preview: str = None
    qextFilename: str = None
    qextVersion: str = None
    repository: str = None
    supernova: bool = None
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
        if "bundle" in kvargs and kvargs["bundle"] is not None:
            if type(kvargs["bundle"]).__name__ == Extension.__annotations__["bundle"]:
                self_.bundle = kvargs["bundle"]
            else:
                self_.bundle = BundleMeta(**kvargs["bundle"])
        if "bundled" in kvargs and kvargs["bundled"] is not None:
            self_.bundled = kvargs["bundled"]
        if "checksum" in kvargs and kvargs["checksum"] is not None:
            self_.checksum = kvargs["checksum"]
        if "createdAt" in kvargs and kvargs["createdAt"] is not None:
            self_.createdAt = kvargs["createdAt"]
        if "dependencies" in kvargs and kvargs["dependencies"] is not None:
            self_.dependencies = kvargs["dependencies"]
        if "deprecated" in kvargs and kvargs["deprecated"] is not None:
            self_.deprecated = kvargs["deprecated"]
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
        if "loadpath" in kvargs and kvargs["loadpath"] is not None:
            self_.loadpath = kvargs["loadpath"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "preview" in kvargs and kvargs["preview"] is not None:
            self_.preview = kvargs["preview"]
        if "qextFilename" in kvargs and kvargs["qextFilename"] is not None:
            self_.qextFilename = kvargs["qextFilename"]
        if "qextVersion" in kvargs and kvargs["qextVersion"] is not None:
            self_.qextVersion = kvargs["qextVersion"]
        if "repository" in kvargs and kvargs["repository"] is not None:
            self_.repository = kvargs["repository"]
        if "supernova" in kvargs and kvargs["supernova"] is not None:
            self_.supernova = kvargs["supernova"]
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
        Downloads a file from the extension archive.

        Parameters
        ----------
        filepath: str
          Path to the file archive for the specified extension archive. Folders separated with forward slashes.
        """
        self.auth.rest(
            path="/extensions/{id}/file/{filepath}".replace(
                "{filepath}", filepath
            ).replace("{id}", self.id),
            method="GET",
            params={},
            data=None,
        )

    def get_file(self) -> None:
        """
        Downloads the extension as an archive.

        Parameters
        ----------
        """
        self.auth.rest(
            path="/extensions/{id}/file".replace("{id}", self.id),
            method="GET",
            params={},
            data=None,
        )

    def delete(self) -> None:
        """
        Deletes a specific extension.

        Parameters
        ----------
        """
        self.auth.rest(
            path="/extensions/{id}".replace("{id}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def patch(
        self, data: ExtensionDef = None, file: io.BufferedReader = None
    ) -> Extension:
        """
        Updates a specific extension with provided data. If a file is provided, the data field is not required.

        Parameters
        ----------
        data: ExtensionDef = None
        file: str = None
          Extension archive.
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
            path="/extensions/{id}".replace("{id}", self.id),
            method="PATCH",
            params={},
            data=None,
            files=files_dict,
        )
        self.__init__(**response.json())
        return self


@dataclass
class ExtensionDef:
    """
    The extension model.

    Attributes
    ----------
    author: str
      Author of the extension.
    bundle: BundleMeta
      Object containing meta data regarding the bundle the extension belongs to. If it does not belong to a bundle, this object is not defined.
    bundled: bool
      If the extension is part of an extension bundle.
    checksum: str
      Checksum of the extension contents.
    dependencies: object
      Map of dependencies describing version of the component it requires.
    deprecated: str
      A date noting when the extension was deprecated.
    description: str
      Description of the extension.
    file: object
      The file that was uploaded with the extension.
    homepage: str
      Home page of the extension.
    icon: str
      Icon to show in the client.
    keywords: str
      Keywords for the extension.
    license: str
      Under which license this extension is published.
    loadpath: str
      Relative path to the extension's entry file, defaults to `filename` from the qext file.
    name: str
      The display name of this extension.
    preview: str
      Path to an image that enables users to preview the extension.
    qextFilename: str
      The name of the qext file that was uploaded with this extension.
    qextVersion: str
      The version from the qext file that was uploaded with this extension.
    repository: str
      Link to the extension source code.
    supernova: bool
      If the extension is a supernova extension or not.
    supplier: str
      Supplier of the extension.
    tags: list[str]
      List of tags.
    type: str
      The type of this extension (visualization, etc.).
    version: str
      Version of the extension.
    """

    author: str = None
    bundle: BundleMeta = None
    bundled: bool = None
    checksum: str = None
    dependencies: object = None
    deprecated: str = None
    description: str = None
    file: object = None
    homepage: str = None
    icon: str = None
    keywords: str = None
    license: str = None
    loadpath: str = None
    name: str = None
    preview: str = None
    qextFilename: str = None
    qextVersion: str = None
    repository: str = None
    supernova: bool = None
    supplier: str = None
    tags: list[str] = None
    type: str = None
    version: str = None

    def __init__(self_, **kvargs):
        if "author" in kvargs and kvargs["author"] is not None:
            self_.author = kvargs["author"]
        if "bundle" in kvargs and kvargs["bundle"] is not None:
            if (
                type(kvargs["bundle"]).__name__
                == ExtensionDef.__annotations__["bundle"]
            ):
                self_.bundle = kvargs["bundle"]
            else:
                self_.bundle = BundleMeta(**kvargs["bundle"])
        if "bundled" in kvargs and kvargs["bundled"] is not None:
            self_.bundled = kvargs["bundled"]
        if "checksum" in kvargs and kvargs["checksum"] is not None:
            self_.checksum = kvargs["checksum"]
        if "dependencies" in kvargs and kvargs["dependencies"] is not None:
            self_.dependencies = kvargs["dependencies"]
        if "deprecated" in kvargs and kvargs["deprecated"] is not None:
            self_.deprecated = kvargs["deprecated"]
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
        if "loadpath" in kvargs and kvargs["loadpath"] is not None:
            self_.loadpath = kvargs["loadpath"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "preview" in kvargs and kvargs["preview"] is not None:
            self_.preview = kvargs["preview"]
        if "qextFilename" in kvargs and kvargs["qextFilename"] is not None:
            self_.qextFilename = kvargs["qextFilename"]
        if "qextVersion" in kvargs and kvargs["qextVersion"] is not None:
            self_.qextVersion = kvargs["qextVersion"]
        if "repository" in kvargs and kvargs["repository"] is not None:
            self_.repository = kvargs["repository"]
        if "supernova" in kvargs and kvargs["supernova"] is not None:
            self_.supernova = kvargs["supernova"]
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
class BundleMeta:
    """
    Object containing meta data regarding the bundle the extension belongs to. If it does not belong to a bundle, this object is not defined.

    Attributes
    ----------
    description: str
      Description of the bundle.
    id: str
      Unique identifier of the bundle.
    name: str
      Name of the bundle.
    """

    description: str = None
    id: str = None
    name: str = None

    def __init__(self_, **kvargs):
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ExtensionsClass:
    """

    Attributes
    ----------
    data: list[Extension]
    """

    data: list[Extension] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]" == ExtensionsClass.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [Extension(**e) for e in kvargs["data"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Extensions:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get(self, id: str) -> Extension:
        """
        Returns a specific extension.

        Parameters
        ----------
        id: str
          Extension identifier or its qextFilename.
        """
        response = self.auth.rest(
            path="/extensions/{id}".replace("{id}", id),
            method="GET",
            params={},
            data=None,
        )
        obj = Extension(**response.json())
        obj.auth = self.auth
        return obj

    def get_extensions(self) -> ExtensionsClass:
        """
        Lists all extensions.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/extensions",
            method="GET",
            params={},
            data=None,
        )
        obj = ExtensionsClass(**response.json())
        obj.auth = self.auth
        return obj

    def create(
        self, data: ExtensionDef = None, file: io.BufferedReader = None
    ) -> Extension:
        """
        Creates a new extension. If a file is provided, the data field is not required.

        Parameters
        ----------
        data: ExtensionDef = None
        file: str = None
          Extension archive.
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
            path="/extensions", method="POST", params={}, data=None, files=files_dict
        )
        obj = Extension(**response.json())
        obj.auth = self.auth
        return obj
