# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

import io
from dataclasses import asdict, dataclass
from typing import Literal

from ..auth import Auth, Config
from ..listable import ListableResource
from ..utils import get_mime_type


@dataclass
class Brand:
    """
    A brand is a collection of assets for applying custom branding. Only a single brand can be active in a tenant.

    Attributes
    ----------
    active: bool
    createdAt: str
      The UTC timestamp when the brand was created.
    createdBy: str
      ID of a user that created the brand.
    description: str
    files: list[BrandFile]
      Collection of resources that make up the brand.
    id: str
    name: str
    updatedAt: str
      The UTC timestamp when the brand was last updated.
    updatedBy: str
      ID of a user that last updated the brand.
    """

    active: bool = None
    createdAt: str = None
    createdBy: str = None
    description: str = None
    files: list[BrandFile] = None
    id: str = None
    name: str = None
    updatedAt: str = None
    updatedBy: str = None

    def __init__(self_, **kvargs):
        if "active" in kvargs and kvargs["active"] is not None:
            self_.active = kvargs["active"]
        if "createdAt" in kvargs and kvargs["createdAt"] is not None:
            self_.createdAt = kvargs["createdAt"]
        if "createdBy" in kvargs and kvargs["createdBy"] is not None:
            self_.createdBy = kvargs["createdBy"]
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "files" in kvargs and kvargs["files"] is not None:
            if all(
                f"list[{type(e).__name__}]" == Brand.__annotations__["files"]
                for e in kvargs["files"]
            ):
                self_.files = kvargs["files"]
            else:
                self_.files = [BrandFile(**e) for e in kvargs["files"]]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "updatedAt" in kvargs and kvargs["updatedAt"] is not None:
            self_.updatedAt = kvargs["updatedAt"]
        if "updatedBy" in kvargs and kvargs["updatedBy"] is not None:
            self_.updatedBy = kvargs["updatedBy"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BrandFile:
    """
    Represents one of the assets used as part of the brand. These include logos, favicons, and some styles.

    Attributes
    ----------
    contentType: str
    eTag: str
    id: Literal["logo", "favIcon", "styles"]
    path: str
    """

    contentType: str = None
    eTag: str = None
    id: Literal["logo", "favIcon", "styles"] = None
    path: str = None

    def __init__(self_, **kvargs):
        if "contentType" in kvargs and kvargs["contentType"] is not None:
            self_.contentType = kvargs["contentType"]
        if "eTag" in kvargs and kvargs["eTag"] is not None:
            self_.eTag = kvargs["eTag"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "path" in kvargs and kvargs["path"] is not None:
            self_.path = kvargs["path"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BrandPatch:
    """
    A JSON Patch document as defined in https://datatracker.ietf.org/doc/html/rfc6902.

    Attributes
    ----------
    op: Literal["add", "remove", "replace"]
      The operation to be performed.
    path: Literal["/name", "/description"]
      The path for the given resource field to patch.
    value: str
      The value to be used for this operation.
    """

    op: Literal["add", "remove", "replace"] = None
    path: Literal["/name", "/description"] = None
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
class BrandsList:
    """
    A collection of brands.

    Attributes
    ----------
    data: list[Brand]
    links: BrandsListLinks
    """

    data: list[Brand] = None
    links: BrandsListLinks = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]" == BrandsList.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [Brand(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == BrandsList.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = BrandsListLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BrandsListLinks:
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
            if type(kvargs["next"]).__name__ == BrandsListLinks.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = Link(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if type(kvargs["prev"]).__name__ == BrandsListLinks.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Link(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == BrandsListLinks.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
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
      URL of a resource request.
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
class NoActiveBrand:
    """
    Empty object inferring lack of active branding.

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Brands:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_active(self) -> any:
        """
        Retrieves the current active brand

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/brands/active",
            method="GET",
            params={},
            data=None,
        )
        obj = NoActiveBrand(**response.json())
        obj.auth = self.auth
        return obj

    def activate(self, brand_id: str) -> Brand:
        """
        Activates a brand
        Sets the brand active and de-activates any other active brand. If the brand is already active, no action is taken.

        Parameters
        ----------
        brand_id: str
          The brand's unique identifier.
        """
        response = self.auth.rest(
            path="/brands/{brand-id}/actions/activate".replace("{brand-id}", brand_id),
            method="POST",
            params={},
            data=None,
        )
        obj = Brand(**response.json())
        obj.auth = self.auth
        return obj

    def deactivate(self, brand_id: str) -> Brand:
        """
        Deactivates a brand
        Sets the brand so it is no longer active. If the brand is already inactive, no action is taken.

        Parameters
        ----------
        brand_id: str
          The brand's unique identifier.
        """
        response = self.auth.rest(
            path="/brands/{brand-id}/actions/deactivate".replace(
                "{brand-id}", brand_id
            ),
            method="POST",
            params={},
            data=None,
        )
        obj = Brand(**response.json())
        obj.auth = self.auth
        return obj

    def delete_file(
        self, brand_id: str, brand_file_id: Literal["logo", "favIcon", "styles"]
    ) -> None:
        """
        Deletes a specific brand file

        Parameters
        ----------
        brand_id: str
          The brand's unique identifier.
        brand_file_id: Literal["logo", "favIcon", "styles"]
          The unique identifier of a file within a brand.
        """
        self.auth.rest(
            path="/brands/{brand-id}/files/{brand-file-id}".replace(
                "{brand-id}", brand_id
            ).replace("{brand-file-id}", brand_file_id),
            method="DELETE",
            params={},
            data=None,
        )

    def get_file(
        self, brand_id: str, brand_file_id: Literal["logo", "favIcon", "styles"]
    ) -> str:
        """
        Downloads the brand file

        Parameters
        ----------
        brand_id: str
          The brand's unique identifier.
        brand_file_id: Literal["logo", "favIcon", "styles"]
          The unique identifier of a file within a brand.
        """
        response = self.auth.rest(
            path="/brands/{brand-id}/files/{brand-file-id}".replace(
                "{brand-id}", brand_id
            ).replace("{brand-file-id}", brand_file_id),
            method="GET",
            params={},
            data=None,
            stream=True,
        )
        return response

    def create_file(
        self,
        brand_id: str,
        brand_file_id: Literal["logo", "favIcon", "styles"],
        file: io.BufferedReader = None,
    ) -> BrandFile:
        """
        Creates a brand file

        Parameters
        ----------
        brand_id: str
          The brand's unique identifier.
        brand_file_id: Literal["logo", "favIcon", "styles"]
          The unique identifier of a file within a brand.
        file: str = None
          The path and name of a file to upload.
        """
        files_dict = {}
        files_dict["file"] = ("file", file, get_mime_type(file))
        response = self.auth.rest(
            path="/brands/{brand-id}/files/{brand-file-id}".replace(
                "{brand-id}", brand_id
            ).replace("{brand-file-id}", brand_file_id),
            method="POST",
            params={},
            data=None,
            files=files_dict,
        )
        obj = BrandFile(**response.json())
        obj.auth = self.auth
        return obj

    def set_file(
        self,
        brand_id: str,
        brand_file_id: Literal["logo", "favIcon", "styles"],
        file: io.BufferedReader = None,
    ) -> BrandFile:
        """
        Updates existing file

        Parameters
        ----------
        brand_id: str
          The brand's unique identifier.
        brand_file_id: Literal["logo", "favIcon", "styles"]
          The unique identifier of a file within a brand.
        file: str = None
          A file to upload.
        """
        files_dict = {}
        files_dict["file"] = ("file", file, get_mime_type(file))
        response = self.auth.rest(
            path="/brands/{brand-id}/files/{brand-file-id}".replace(
                "{brand-id}", brand_id
            ).replace("{brand-file-id}", brand_file_id),
            method="PUT",
            params={},
            data=None,
            files=files_dict,
        )
        obj = BrandFile(**response.json())
        obj.auth = self.auth
        return obj

    def delete(self, brand_id: str) -> None:
        """
        Deletes a specific brand

        Parameters
        ----------
        brand_id: str
          The brand's unique identifier.
        """
        self.auth.rest(
            path="/brands/{brand-id}".replace("{brand-id}", brand_id),
            method="DELETE",
            params={},
            data=None,
        )

    def get(self, brand_id: str) -> Brand:
        """
        Retrieves a specific brand

        Parameters
        ----------
        brand_id: str
          The brand's unique identifier.
        """
        response = self.auth.rest(
            path="/brands/{brand-id}".replace("{brand-id}", brand_id),
            method="GET",
            params={},
            data=None,
        )
        obj = Brand(**response.json())
        obj.auth = self.auth
        return obj

    def patch(self, brand_id: str, BrandPatchData: list[BrandPatch]) -> None:
        """
        Patches a brand

        Parameters
        ----------
        brand_id: str
          The brand's unique identifier.
        BrandPatchData: list[BrandPatch]
        """
        data = [asdict(elem) for elem in BrandPatchData]
        self.auth.rest(
            path="/brands/{brand-id}".replace("{brand-id}", brand_id),
            method="PATCH",
            params={},
            data=data,
        )

    def get_brands(
        self,
        endingBefore: str = None,
        limit: int = 5,
        sort: Literal[
            "id",
            "+id",
            "-id",
            "createdAt",
            "+createdAt",
            "-createdAt",
            "updatedAt",
            "+updatedAt",
            "-updatedAt",
        ] = "-id",
        startingAfter: str = None,
    ) -> ListableResource[Brand]:
        """
        Lists all brand entries for a tenant

        Parameters
        ----------
        endingBefore: str = None
          Cursor to previous.
        limit: int = 5
          Maximum number of brands to retrieve.
        sort: Literal["id", "+id", "-id", "createdAt", "+createdAt", "-createdAt", "updatedAt", "+updatedAt", "-updatedAt"] = "-id"
          Field to sort by, prefixed with -/+ to indicate the order.
        startingAfter: str = None
          Cursor to the next page.
        """
        query_params = {}
        if endingBefore is not None:
            query_params["endingBefore"] = endingBefore
        if limit is not None:
            query_params["limit"] = limit
        if sort is not None:
            query_params["sort"] = sort
        if startingAfter is not None:
            query_params["startingAfter"] = startingAfter
        response = self.auth.rest(
            path="/brands",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Brand,
            auth=self.auth,
            path="/brands",
            query_params=query_params,
        )

    def create(
        self,
        logo: io.BufferedReader = None,
        name: str = None,
        styles: io.BufferedReader = None,
        favIcon: io.BufferedReader = None,
        description: str = None,
    ) -> Brand:
        """
        Creates a new brand

        Parameters
        ----------
        logo: str = None
          The path and name of a JPG or PNG file that will be adjusted to fit in a 'box' measuring 109px in width and 62 px in height while maintaining aspect ratio. Maximum size of 300 KB, but smaller is recommended.
        name: str = None
          Name of the brand.
        styles: str = None
          The path and name of a JSON file to define brand style settings. Maximum size is 100 KB. This property is not currently operational.
        favIcon: str = None
          The path and name of a properly formatted ICO file. Maximum size is 100 KB.
        description: str = None
          Description of the brand.
        """
        files_dict = {}
        files_dict["logo"] = ("logo", logo, get_mime_type(logo))
        files_dict["styles"] = ("styles", styles, get_mime_type(styles))
        files_dict["favIcon"] = ("favIcon", favIcon, get_mime_type(favIcon))
        if name is not None:
            files_dict["name"] = name
        if description is not None:
            files_dict["description"] = description
        response = self.auth.rest(
            path="/brands", method="POST", params={}, data=None, files=files_dict
        )
        obj = Brand(**response.json())
        obj.auth = self.auth
        return obj
