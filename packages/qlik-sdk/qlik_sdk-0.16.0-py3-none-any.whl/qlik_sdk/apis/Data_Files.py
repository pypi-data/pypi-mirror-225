# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

import io
import json
from dataclasses import asdict, dataclass
from typing import Literal

from ..auth import Auth, Config
from ..listable import ListableResource
from ..utils import get_mime_type


@dataclass
class DataFileUploadResponse:
    """

    Attributes
    ----------
    appId: str
      If this file is bound to the lifecycle of a specific app, this is the ID of this app.
    createdDate: str
      The date that the uploaded file was created.
    id: str
      The ID for the uploaded file.
    modifiedDate: str
      The date that the updated file was last modified.
    name: str
      The name of the uploaded file.
    ownerId: str
      The 'owner' of a file is the user who last uploaded the file's content.
    size: int
      The size of the uploaded file, in bytes.
    spaceId: str
      If the file was uploaded to a team space, this is the ID of that space.
    """

    appId: str = None
    createdDate: str = None
    id: str = None
    modifiedDate: str = None
    name: str = None
    ownerId: str = None
    size: int = None
    spaceId: str = None

    def __init__(self_, **kvargs):
        if "appId" in kvargs and kvargs["appId"] is not None:
            self_.appId = kvargs["appId"]
        if "createdDate" in kvargs and kvargs["createdDate"] is not None:
            self_.createdDate = kvargs["createdDate"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "modifiedDate" in kvargs and kvargs["modifiedDate"] is not None:
            self_.modifiedDate = kvargs["modifiedDate"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "ownerId" in kvargs and kvargs["ownerId"] is not None:
            self_.ownerId = kvargs["ownerId"]
        if "size" in kvargs and kvargs["size"] is not None:
            self_.size = kvargs["size"]
        if "spaceId" in kvargs and kvargs["spaceId"] is not None:
            self_.spaceId = kvargs["spaceId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def change_owner(self, data: ChangeDataFileOwnerRequest) -> None:
        """
        Change the owner of an existing data file.
        This is primarily an admin type of operation.  In general, the owner of a data file is implicitly set as
        part of a data file upload.  For data files that reside in a personal space, changing the owner has the
        effect of moving the data file to the new owner's personal space.

        Parameters
        ----------
        data: ChangeDataFileOwnerRequest
          The request.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        self.auth.rest(
            path="/data-files/{id}/actions/change-owner".replace("{id}", self.id),
            method="POST",
            params={},
            data=data,
        )

    def change_space(self, data: ChangeDataFileSpaceRequest = None) -> None:
        """
        Change the space that an existing data file resides in.
        This is to allow for a separate admin type of operation that is more global in terms of access in cases
        where admin users may not explicitly have been granted full access to a given space within the declared
        space-level permissions.  If the space ID is set to null, then the datafile will end up residing in the
        personal space of the user who is the owner of the file.

        Parameters
        ----------
        data: ChangeDataFileSpaceRequest = None
          The request.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        self.auth.rest(
            path="/data-files/{id}/actions/change-space".replace("{id}", self.id),
            method="POST",
            params={},
            data=data,
        )

    def delete(self) -> None:
        """
        Delete the specified data file.

        Parameters
        ----------
        """
        self.auth.rest(
            path="/data-files/{id}".replace("{id}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def set(
        self,
        File: io.BufferedReader = None,
        name: str = None,
        appId: str = None,
        sourceId: str = None,
        connectionId: str = None,
        tempContentFileId: str = None,
    ) -> DataFileUploadResponse:
        """
        Re-upload an existing data file.

        Parameters
        ----------
        File: str = None
          IFormFile form multipart/form-data
        name: str = None
          Name that will be given to the uploaded file.  If this name is different than the name used when the file
          was last POSTed or PUT, this will result in a rename of the file.  It should be noted that the '/' character
          in a data file name indicates a 'path' separator in a logical folder hierarchy for the name.  Names that
          contain '/'s should be used with the assumption that a logical 'folder hierarchy' is being defined for the
          full pathname of that file.  '/' is a significant character in the data file name, and may impact the
          behavior of future APIs that take this folder hierarchy into account.
        appId: str = None
          If this file should be bound to the lifecycle of a specific app, this is the ID of this app.
        sourceId: str = None
          If a SourceId is specified, this is the ID of the existing data file whose content should be copied into
          the specified data file.  That is, instead of the file content being specified in the Data element,
          it is effectively copied from an existing, previously uploaded file.
        connectionId: str = None
          If present, this is the DataFiles connection that the upload should occur in the context of.  If absent,
          the default is that the upload will occur in the context of the MyDataFiles connection.  If the DataFiles
          connection is different from the one specified when the file was last POSTed or PUT, this will result in
          a logical move of this file into the new space.
        tempContentFileId: str = None
          If a TempContentFileId is specified, this is the ID of a previously uploaded temporary content file whose
          content should be copied into the specified data file.  That is, instead of the file content being specified
          in the Data element, it is effectively copied from an existing, previously uploaded file.  The expectation
          is that this file was previously uploaded to the temporary content service, and the ID specified here is
          the one returned from the temp content upload request.
        """
        files_dict = {}
        files_dict["File"] = ("File", File, get_mime_type(File))
        Json_dict = {}
        if name is not None:
            Json_dict["name"] = name
        if appId is not None:
            Json_dict["appId"] = appId
        if sourceId is not None:
            Json_dict["sourceId"] = sourceId
        if connectionId is not None:
            Json_dict["connectionId"] = connectionId
        if tempContentFileId is not None:
            Json_dict["tempContentFileId"] = tempContentFileId
        files_dict["Json"] = (None, json.dumps(Json_dict))
        response = self.auth.rest(
            path="/data-files/{id}".replace("{id}", self.id),
            method="PUT",
            params={},
            data=None,
            files=files_dict,
        )
        self.__init__(**response.json())
        return self


@dataclass
class BatchChangeSpaceItem:
    """

    Attributes
    ----------
    id: str
      The ID of the data file whose space will be changed.
    spaceId: str
      The ID of the new space.  Passing in a null will result in the data file being moved to the user's
      personal space.
    """

    id: str = None
    spaceId: str = None

    def __init__(self_, **kvargs):
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "spaceId" in kvargs and kvargs["spaceId"] is not None:
            self_.spaceId = kvargs["spaceId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BatchDeleteItem:
    """

    Attributes
    ----------
    id: str
      The ID of the data file to delete.
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
class ChangeDataFileOwnerRequest:
    """

    Attributes
    ----------
    ownerId: str
      The ID of the new owner.
    """

    ownerId: str = None

    def __init__(self_, **kvargs):
        if "ownerId" in kvargs and kvargs["ownerId"] is not None:
            self_.ownerId = kvargs["ownerId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ChangeDataFileSpaceRequest:
    """

    Attributes
    ----------
    spaceId: str
      The ID of the space.  If null, this data file will be moved to the user's personal space.
    """

    spaceId: str = None

    def __init__(self_, **kvargs):
        if "spaceId" in kvargs and kvargs["spaceId"] is not None:
            self_.spaceId = kvargs["spaceId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ConnectionsResponse:
    """

    Attributes
    ----------
    connectStatement: str
      The connect statement that will be passed to the connector when invoked.
    id: str
      The unique identifier of the connection.
    name: str
      The name of the connection.
    spaceId: str
      The team space that the given connection is associated with.  If null, the connection is not associated
      with any specific team space.
    type: str
      The type of the connection.
    """

    connectStatement: str = None
    id: str = None
    name: str = None
    spaceId: str = None
    type: str = None

    def __init__(self_, **kvargs):
        if "connectStatement" in kvargs and kvargs["connectStatement"] is not None:
            self_.connectStatement = kvargs["connectStatement"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "spaceId" in kvargs and kvargs["spaceId"] is not None:
            self_.spaceId = kvargs["spaceId"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DataFileBatchChangeSpaceRequest:
    """
    Specifies the list of data file change space operations in a single batch.

    Attributes
    ----------
    change_space: list[BatchChangeSpaceItem]
      The list of data files to delete.
    """

    change_space: list[BatchChangeSpaceItem] = None

    def __init__(self_, **kvargs):
        if "change-space" in kvargs and kvargs["change-space"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == DataFileBatchChangeSpaceRequest.__annotations__["change_space"]
                for e in kvargs["change-space"]
            ):
                self_.change_space = kvargs["change-space"]
            else:
                self_.change_space = [
                    BatchChangeSpaceItem(**e) for e in kvargs["change-space"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DataFileBatchDeleteRequest:
    """
    Specifies the list of data files to be deleted in a single batch.

    Attributes
    ----------
    delete: list[BatchDeleteItem]
      The list of data files to delete.
    """

    delete: list[BatchDeleteItem] = None

    def __init__(self_, **kvargs):
        if "delete" in kvargs and kvargs["delete"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == DataFileBatchDeleteRequest.__annotations__["delete"]
                for e in kvargs["delete"]
            ):
                self_.delete = kvargs["delete"]
            else:
                self_.delete = [BatchDeleteItem(**e) for e in kvargs["delete"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetConnectionsResponse:
    """

    Attributes
    ----------
    data: list[ConnectionsResponse]
      Properties of the connections to the tenant spaces.
    links: LinksResponse
    """

    data: list[ConnectionsResponse] = None
    links: LinksResponse = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == GetConnectionsResponse.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [ConnectionsResponse(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == GetConnectionsResponse.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = LinksResponse(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetDataFileInfosResponse:
    """

    Attributes
    ----------
    data: list[DataFileUploadResponse]
      Properties of the uploaded data files.
    links: LinksResponse
    """

    data: list[DataFileUploadResponse] = None
    links: LinksResponse = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == GetDataFileInfosResponse.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [DataFileUploadResponse(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == GetDataFileInfosResponse.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = LinksResponse(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LinkResponse:
    """

    Attributes
    ----------
    href: str
      The URL for the link.
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
class LinksResponse:
    """

    Attributes
    ----------
    next: LinkResponse
    prev: LinkResponse
    self: LinkResponse
    """

    next: LinkResponse = None
    prev: LinkResponse = None
    self: LinkResponse = None

    def __init__(self_, **kvargs):
        if "next" in kvargs and kvargs["next"] is not None:
            if type(kvargs["next"]).__name__ == LinksResponse.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = LinkResponse(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if type(kvargs["prev"]).__name__ == LinksResponse.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = LinkResponse(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == LinksResponse.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = LinkResponse(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class MultiStatusResponse:
    """

    Attributes
    ----------
    data: list[MultiStatusResponseItem]
      List of individual results for the items in the specified batch.
    """

    data: list[MultiStatusResponseItem] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == MultiStatusResponse.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [MultiStatusResponseItem(**e) for e in kvargs["data"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class MultiStatusResponseItem:
    """

    Attributes
    ----------
    code: str
      The error code.
    detail: str
      A human-readable explanation specific to this occurrence of the problem.
    id: str
      The unique identifier of the file.
    status: int
      The HTTP status code.
    title: str
      Summary of the problem.
    """

    code: str = None
    detail: str = None
    id: str = None
    status: int = None
    title: str = None

    def __init__(self_, **kvargs):
        if "code" in kvargs and kvargs["code"] is not None:
            self_.code = kvargs["code"]
        if "detail" in kvargs and kvargs["detail"] is not None:
            self_.detail = kvargs["detail"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "status" in kvargs and kvargs["status"] is not None:
            self_.status = kvargs["status"]
        if "title" in kvargs and kvargs["title"] is not None:
            self_.title = kvargs["title"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class QuotaResponse:
    """

    Attributes
    ----------
    allowedExtensions: list[str]
      The allowed file extensions on files that are uploaded.
    allowedInternalExtensions: list[str]
      The allowed file extensions for files that are only used internally by the system (and thus not typically
      shown to end users).
    maxFileSize: int
      Maximum allowable size of an uploaded file.
    maxLargeFileSize: int
      Maximum allowable size for a single uploaded large data file (in bytes).  This is a file that was indirectly
      uploaded using the temp content service chunked upload capability.
    maxSize: int
      The maximum aggregate size of all files uploaded by a given user.
    size: int
      The current aggregate size of all files uploaded by a given user.  If the current aggregate size is greater
      than the maximum aggregate size, this is a quota violation.
    """

    allowedExtensions: list[str] = None
    allowedInternalExtensions: list[str] = None
    maxFileSize: int = None
    maxLargeFileSize: int = None
    maxSize: int = None
    size: int = None

    def __init__(self_, **kvargs):
        if "allowedExtensions" in kvargs and kvargs["allowedExtensions"] is not None:
            self_.allowedExtensions = kvargs["allowedExtensions"]
        if (
            "allowedInternalExtensions" in kvargs
            and kvargs["allowedInternalExtensions"] is not None
        ):
            self_.allowedInternalExtensions = kvargs["allowedInternalExtensions"]
        if "maxFileSize" in kvargs and kvargs["maxFileSize"] is not None:
            self_.maxFileSize = kvargs["maxFileSize"]
        if "maxLargeFileSize" in kvargs and kvargs["maxLargeFileSize"] is not None:
            self_.maxLargeFileSize = kvargs["maxLargeFileSize"]
        if "maxSize" in kvargs and kvargs["maxSize"] is not None:
            self_.maxSize = kvargs["maxSize"]
        if "size" in kvargs and kvargs["size"] is not None:
            self_.size = kvargs["size"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class DataFiles:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def change_space(
        self, data: DataFileBatchChangeSpaceRequest
    ) -> MultiStatusResponse:
        """
        Change the spaces that a set of existing data files reside in a a single batch.
        This is to allow for a separate admin type of operation that is more global in terms of access in cases
        where admin users may not explicitly have been granted full access to a given space within the declared
        space-level permissions.  If the space ID is set to null, then the data file will end up residing in the
        personal space of the user who is the owner of the file.

        Parameters
        ----------
        data: DataFileBatchChangeSpaceRequest
          Specifies the list of data file change space operations in a single batch.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/data-files/actions/change-space",
            method="POST",
            params={},
            data=data,
        )
        obj = MultiStatusResponse(**response.json())
        obj.auth = self.auth
        return obj

    def delete(self, data: DataFileBatchDeleteRequest) -> MultiStatusResponse:
        """
        Delete the specified set of data files as a single batch.

        Parameters
        ----------
        data: DataFileBatchDeleteRequest
          Specifies the list of data files to be deleted in a single batch.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/data-files/actions/delete",
            method="POST",
            params={},
            data=data,
        )
        obj = MultiStatusResponse(**response.json())
        obj.auth = self.auth
        return obj

    def get_connection(self, id: str) -> ConnectionsResponse:
        """
        Get the built-in connection used by the engine to load/write data files given a connection ID.

        Parameters
        ----------
        id: str
          The ID of the connection.
        """
        response = self.auth.rest(
            path="/data-files/connections/{id}".replace("{id}", id),
            method="GET",
            params={},
            data=None,
        )
        obj = ConnectionsResponse(**response.json())
        obj.auth = self.auth
        return obj

    def get_connections(
        self,
        appId: str = None,
        limit: int = 20,
        name: str = None,
        page: str = None,
        personal: bool = False,
        sort: Literal["spaceId", "+spaceId", "-spaceId"] = None,
        spaceId: str = None,
    ) -> ListableResource[ConnectionsResponse]:
        """
        Get the list of built-in connections used by the engine to load/write data files.
        The non-filtered list contains a set of hardcoded connections, along with one connection per team space that
        the given user has access to.

        Parameters
        ----------
        appId: str = None
          If present, get connections with connection strings that are scoped to the given app ID.
        limit: int = 20
          If present, the maximum number of data file connection records to return.
        name: str = None
          If present, only return connections with the given name.
        page: str = None
          If present, the cursor that starts the page of data that is returned.
        personal: bool = False
          If true, only return the connections that access data in a personal space.  Default is false.
        sort: Literal["spaceId", "+spaceId", "-spaceId"] = None
          The name of the field used to sort the result.  By default, the sort is ascending.  Putting a '+' prefix on
          the sort field name explicitly indicates ascending sort order.  A '-' prefix indicates a descending sort order.
        spaceId: str = None
          If present, only return the connection that accesses data files in the specified space.
        """
        query_params = {}
        if appId is not None:
            query_params["appId"] = appId
        if limit is not None:
            query_params["limit"] = limit
        if name is not None:
            query_params["name"] = name
        if page is not None:
            query_params["page"] = page
        if personal is not None:
            query_params["personal"] = personal
        if sort is not None:
            query_params["sort"] = sort
        if spaceId is not None:
            query_params["spaceId"] = spaceId
        response = self.auth.rest(
            path="/data-files/connections",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=ConnectionsResponse,
            auth=self.auth,
            path="/data-files/connections",
            query_params=query_params,
        )

    def get_quotas(self) -> QuotaResponse:
        """
        Get quota information for the calling user.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/data-files/quotas",
            method="GET",
            params={},
            data=None,
        )
        obj = QuotaResponse(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, id: str) -> DataFileUploadResponse:
        """
        Get descriptive info for the specified data file.

        Parameters
        ----------
        id: str
          The ID of the data file.
        """
        response = self.auth.rest(
            path="/data-files/{id}".replace("{id}", id),
            method="GET",
            params={},
            data=None,
        )
        obj = DataFileUploadResponse(**response.json())
        obj.auth = self.auth
        return obj

    def get_data_files(
        self,
        allowInternalFiles: bool = False,
        appId: str = None,
        connectionId: str = None,
        limit: int = 20,
        name: str = None,
        ownerId: str = None,
        page: str = None,
        sort: Literal[
            "name",
            "+name",
            "-name",
            "size",
            "+size",
            "-size",
            "modifiedDate",
            "+modifiedDate",
            "-modifiedDate",
        ] = None,
    ) -> ListableResource[DataFileUploadResponse]:
        """
        Get descriptive info for the specified data files.

        Parameters
        ----------
        allowInternalFiles: bool = False
          If set to false, do not return data files with internal extensions else return all the data files.
        appId: str = None
          Only return files scoped to the specified app.  If this parameter is not specified, only files that are not
          scoped to any app are returned.  "*" implies all app-scoped files are returned.
        connectionId: str = None
          Return files that reside in the space referenced by the specified DataFiles connection.  If this parameter
          is not specified, the user's personal space is implied.
        limit: int = 20
          If present, the maximum number of data files to return.
        name: str = None
          Filter the list of files returned to the given file name.
        ownerId: str = None
          If present, fetch the data files for the specified owner.  If a connectionId is specified in this case, the
          returned list is constrained to the specified space.  If connectionId is not specified, then all files owned
          by the specified user are returned regardless of the personal space that a given file resides in.
        page: str = None
          If present, the cursor that starts the page of data that is returned.
        sort: Literal["name", "+name", "-name", "size", "+size", "-size", "modifiedDate", "+modifiedDate", "-modifiedDate"] = None
          The name of the field used to sort the result.  By default, the sort order is ascending.  Putting a '+' prefix on
          the sort field name explicitly indicates ascending sort order.  A '-' prefix indicates a descending sort order.
        """
        query_params = {}
        if allowInternalFiles is not None:
            query_params["allowInternalFiles"] = allowInternalFiles
        if appId is not None:
            query_params["appId"] = appId
        if connectionId is not None:
            query_params["connectionId"] = connectionId
        if limit is not None:
            query_params["limit"] = limit
        if name is not None:
            query_params["name"] = name
        if ownerId is not None:
            query_params["ownerId"] = ownerId
        if page is not None:
            query_params["page"] = page
        if sort is not None:
            query_params["sort"] = sort
        response = self.auth.rest(
            path="/data-files",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=DataFileUploadResponse,
            auth=self.auth,
            path="/data-files",
            query_params=query_params,
        )

    def create(
        self,
        File: io.BufferedReader = None,
        name: str = None,
        appId: str = None,
        sourceId: str = None,
        connectionId: str = None,
        tempContentFileId: str = None,
    ) -> DataFileUploadResponse:
        """
        Upload a new data file.

        Parameters
        ----------
        File: str = None
          IFormFile form multipart/form-data
        name: str = None
          Name that will be given to the uploaded file.  It should be noted that the '/' character
          in a data file name indicates a 'path' separator in a logical folder hierarchy for the name.  Names that
          contain '/'s should be used with the assumption that a logical 'folder hierarchy' is being defined for the
          full pathname of that file.  '/' is a significant character in the data file name, and may impact the
          behavior of future APIs which take this folder hierarchy into account.
        appId: str = None
          If this file should be bound to the lifecycle of a specific app, this is the ID of this app.
        sourceId: str = None
          If a SourceId is specified, this is the ID of the existing data file whose content should be copied into
          the specified data file.  That is, instead of the file content being specified in the Data element,
          it is effectively copied from an existing, previously uploaded file.
        connectionId: str = None
          If present, this is the DataFiles connection that the upload should occur in the context of.  If absent,
          the default is that the upload will occur in the context of the MyDataFiles connection.  If the DataFiles
          connection is different from the one specified when the file was last POSTed or PUT, this will result in
          a logical move of this file into the new space.
        tempContentFileId: str = None
          If a TempContentFileId is specified, this is the ID of a previously uploaded temporary content file whose
          content should be copied into the specified data file.  That is, instead of the file content being specified
          in the Data element, it is effectively copied from an existing, previously uploaded file.  The expectation
          is that this file was previously uploaded to the temporary content service, and the ID specified here is
          the one returned from the temp content upload request.
        """
        files_dict = {}
        files_dict["File"] = ("File", File, get_mime_type(File))
        Json_dict = {}
        if name is not None:
            Json_dict["name"] = name
        if appId is not None:
            Json_dict["appId"] = appId
        if sourceId is not None:
            Json_dict["sourceId"] = sourceId
        if connectionId is not None:
            Json_dict["connectionId"] = connectionId
        if tempContentFileId is not None:
            Json_dict["tempContentFileId"] = tempContentFileId
        files_dict["Json"] = (None, json.dumps(Json_dict))
        response = self.auth.rest(
            path="/data-files", method="POST", params={}, data=None, files=files_dict
        )
        obj = DataFileUploadResponse(**response.json())
        obj.auth = self.auth
        return obj
