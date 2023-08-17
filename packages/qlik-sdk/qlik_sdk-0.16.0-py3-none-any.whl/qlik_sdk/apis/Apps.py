# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

import io
from dataclasses import asdict, dataclass
from typing import Literal

from ..auth import Auth, Config
from ..listable import ListableResource
from .Qix import Doc


@dataclass
class NxApp(Doc):
    """
    Application attributes and user privileges.

    Attributes
    ----------
    attributes: NxAttributes
      App attributes. This structure can also contain extra user-defined attributes.
    create: list[NxAppCreatePrivileges]
      Object create privileges. Hints to the client what type of objects the user is allowed to create.
    privileges: list[str]
      Application privileges.
      Hints to the client what actions the user is allowed to perform.
      Could be any of:

      • read

      • create

      • update

      • delete

      • reload

      • import

      • publish

      • duplicate

      • export

      • exportdata

      • change_owner

      • change_space
    """

    attributes: NxAttributes = None
    create: list[NxAppCreatePrivileges] = None
    privileges: list[str] = None

    def __init__(self_, **kvargs):
        if "attributes" in kvargs and kvargs["attributes"] is not None:
            if (
                type(kvargs["attributes"]).__name__
                == NxApp.__annotations__["attributes"]
            ):
                self_.attributes = kvargs["attributes"]
            else:
                self_.attributes = NxAttributes(**kvargs["attributes"])
        if "create" in kvargs and kvargs["create"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NxApp.__annotations__["create"]
                for e in kvargs["create"]
            ):
                self_.create = kvargs["create"]
            else:
                self_.create = [NxAppCreatePrivileges(**e) for e in kvargs["create"]]
        if "privileges" in kvargs and kvargs["privileges"] is not None:
            self_.privileges = kvargs["privileges"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def create_copy(self, data: CreateApp) -> NxApp:
        """
        Copies a specific app.

        Parameters
        ----------
        data: CreateApp
          Attributes that should be set in the copy.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/apps/{appId}/copy".replace("{appId}", self.attributes.id),
            method="POST",
            params={},
            data=data,
        )
        obj = NxApp(**response.json())
        obj.auth = self.auth
        return obj

    def get_data_lineages(self) -> list[LineageInfoRest]:
        """
        Retrieves the lineage for an app.
        Returns a JSON-formatted array of strings describing the lineage of the app.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/apps/{appId}/data/lineage".replace("{appId}", self.attributes.id),
            method="GET",
            params={},
            data=None,
        )
        return [LineageInfoRest(**e) for e in response.json()]

    def get_data_metadata(self) -> DataModelMetadata:
        """
        Retrieves the data model and reload statistics metadata of an app.
        An empty metadata structure is returned if the metadata is not available in the app.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/apps/{appId}/data/metadata".replace("{appId}", self.attributes.id),
            method="GET",
            params={},
            data=None,
        )
        obj = DataModelMetadata(**response.json())
        obj.auth = self.auth
        return obj

    def export(self, NoData: bool = None) -> str:
        """
        Exports a specific app.

        Parameters
        ----------
        NoData: bool = None
          The flag indicating if only object contents should be exported.
        """
        query_params = {}
        if NoData is not None:
            query_params["NoData"] = NoData
        response = self.auth.rest(
            path="/apps/{appId}/export".replace("{appId}", self.attributes.id),
            method="POST",
            params=query_params,
            data=None,
        )
        return response.headers["Location"]

    def recommend_insight_analyses(
        self, data: AnalysisRecommendRequest
    ) -> AnalysisRecommendationResponse:
        """
        Returns analysis recommendations in response to a natural language question, a set of fields and master items, or a set of fields and master items with an optional target analysis.

        Parameters
        ----------
        data: AnalysisRecommendRequest
          Request payload can be of two types, using natural language query or consist of fields or master items and optional target analysis.
          In below examples, consider sales as a master item and product as field, so to get recommendations using sales and product,
          you can utilize below three approaches, also you can set language parameter in headers as part of accept-language.
          Examples:
          ```
          {
            "text": "show me sales by product"
          }
          ```
          ```
          {
            "fields": [
              {
                "name": "product"
              }
            ],
            "libItems": [
              {
                libId: "NwQfJ"
              }
            ]
          }
          ```
          ```
          {
            "fields": [
              {
                "name": "product"
              }
            ],
            "libItems": [
              {
                "libId": "NwQfJ"
              }
            ],
            "targetAnalysis": {
              "id": "rank-rank"
            }
          }
          ```
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/apps/{appId}/insight-analyses/actions/recommend".replace(
                "{appId}", self.attributes.id
            ),
            method="POST",
            params={},
            data=data,
        )
        obj = AnalysisRecommendationResponse(**response.json())
        obj.auth = self.auth
        return obj

    def get_insight_analyses_models(
        self,
    ) -> ListableResource[AnalysisModelResponseDetail]:
        """
        Returns information about model used to make analysis recommendations. Lists all fields and master items in the logical model, along with an indication of the validity of the logical model if the default is not used.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/apps/{appId}/insight-analyses/model".replace(
                "{appId}", self.attributes.id
            ),
            method="GET",
            params={},
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=AnalysisModelResponseDetail,
            auth=self.auth,
            path="/apps/{appId}/insight-analyses/model".replace(
                "{appId}", self.attributes.id
            ),
            query_params={},
        )

    def get_insight_analyses(self) -> ListableResource[AnalysisDescriptor]:
        """
        Returns information about supported analyses for the app's data model. Lists available analysis types, along with minimum and maximum number of dimensions, measures, and fields.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/apps/{appId}/insight-analyses".replace(
                "{appId}", self.attributes.id
            ),
            method="GET",
            params={},
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=AnalysisDescriptor,
            auth=self.auth,
            path="/apps/{appId}/insight-analyses".replace(
                "{appId}", self.attributes.id
            ),
            query_params={},
        )

    def delete_media_file(self, path: str) -> None:
        """
        Deletes a media content file or complete directory.
        Returns OK if the bytes containing the media file (or the complete content of a directory) were successfully deleted, or error in case of failure or lack of permission.

        Parameters
        ----------
        path: str
          Path to file content.
        """
        self.auth.rest(
            path="/apps/{appId}/media/files/{path}".replace(
                "{appId}", self.attributes.id
            ).replace("{path}", path),
            method="DELETE",
            params={},
            data=None,
        )

    def get_media_file(self, path: str) -> str:
        """
        Gets media content from file.
        Returns a stream of bytes containing the media file content on success, or error if file is not found.

        Parameters
        ----------
        path: str
          Path to file content.
        """
        response = self.auth.rest(
            path="/apps/{appId}/media/files/{path}".replace(
                "{appId}", self.attributes.id
            ).replace("{path}", path),
            method="GET",
            params={},
            data=None,
            stream=True,
        )
        return response

    def set_media_file(self, path: str, data: io.BufferedReader) -> None:
        """
        Stores the media content file.
        Returns OK if the bytes containing the media file content were successfully stored, or error in case of failure, lack of permission or file already exists on the supplied path.

        Parameters
        ----------
        path: str
          Path to file content.
        data: object
        """
        self.auth.rest(
            path="/apps/{appId}/media/files/{path}".replace(
                "{appId}", self.attributes.id
            ).replace("{path}", path),
            method="PUT",
            params={},
            data=data,
            headers={"Content-Type": "application/octet-stream"},
        )

    def get_media_lists(self, path: str, show: str = None) -> AppContentList:
        """
        Lists media content.
        Returns a JSON formatted array of strings describing the available media content or error if the optional path supplied is not found.

        Parameters
        ----------
        path: str
          The path to sub folder with static content relative to the root folder. Use empty path to access the root folder.
        show: str = None
          Optional. List output can include files and folders in different ways:

          • Not recursive, default if show option is not supplied or incorrectly specified, results in output with files and empty directories for the path specified only.

          • Recursive(r), use ?show=r or ?show=recursive, results in a recursive output with files, all empty folders are excluded.

          • All(a), use ?show=a or ?show=all, results in a recursive output with files and empty directories.
        """
        query_params = {}
        if show is not None:
            query_params["show"] = show
        response = self.auth.rest(
            path="/apps/{appId}/media/list/{path}".replace(
                "{appId}", self.attributes.id
            ).replace("{path}", path),
            method="GET",
            params=query_params,
            data=None,
        )
        obj = AppContentList(**response.json())
        obj.auth = self.auth
        return obj

    def get_media_thumbnail(self) -> str:
        """
        Gets media content from file currently used as application thumbnail.
        Returns a stream of bytes containing the media file content on success, or error if file is not found.
        The image selected as thumbnail is only updated when application is saved.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/apps/{appId}/media/thumbnail".replace("{appId}", self.attributes.id),
            method="GET",
            params={},
            data=None,
            stream=True,
        )
        return response

    def change_owner_object(
        self, objectId: str, data: UpdateOwner = None
    ) -> NxAppObject:
        """
        Sets owner on an app object.

        Parameters
        ----------
        objectId: str
          Identifier of the object.
        data: UpdateOwner = None
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/apps/{appId}/objects/{objectId}/actions/change-owner".replace(
                "{appId}", self.attributes.id
            ).replace("{objectId}", objectId),
            method="POST",
            params={},
            data=data,
        )
        obj = NxAppObject(**response.json())
        obj.auth = self.auth
        return obj

    def set_owner(self, data: UpdateOwner = None) -> NxApp:
        """
        Changes owner of the app.

        Parameters
        ----------
        data: UpdateOwner = None
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/apps/{appId}/owner".replace("{appId}", self.attributes.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self

    def publish(self, data: PublishApp) -> NxApp:
        """
        Publishes a specific app to a managed space.

        Parameters
        ----------
        data: PublishApp
          Publish information for the app.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/apps/{appId}/publish".replace("{appId}", self.attributes.id),
            method="POST",
            params={},
            data=data,
        )
        obj = NxApp(**response.json())
        obj.auth = self.auth
        return obj

    def set_publish(self, data: RepublishApp) -> NxApp:
        """
        Republishes a published app to a managed space.

        Parameters
        ----------
        data: RepublishApp
          Republish information for the app.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/apps/{appId}/publish".replace("{appId}", self.attributes.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self

    def get_reloads_log(self, reloadId: str) -> str:
        """
        Retrieves the log of a specific reload.
        Returns the log as "text/plain; charset=UTF-8".

        Parameters
        ----------
        reloadId: str
          Identifier of the reload.
        """
        response = self.auth.rest(
            path="/apps/{appId}/reloads/logs/{reloadId}".replace(
                "{appId}", self.attributes.id
            ).replace("{reloadId}", reloadId),
            method="GET",
            params={},
            data=None,
            stream=True,
        )
        return response

    def get_reloads_logs(self) -> ScriptLogList:
        """
        Retrieves the metadata about all script logs stored for an app.
        Returns an array of ScriptLogMeta objects.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/apps/{appId}/reloads/logs".replace("{appId}", self.attributes.id),
            method="GET",
            params={},
            data=None,
        )
        obj = ScriptLogList(**response.json())
        obj.auth = self.auth
        return obj

    def delete_script(self, version: str) -> None:
        """
        Deletes a specific version of the script for an app.
        Fails if the version to delete is the current version.

        Parameters
        ----------
        version: str
          Identifier of the script version
        """
        self.auth.rest(
            path="/apps/{appId}/scripts/{version}".replace(
                "{appId}", self.attributes.id
            ).replace("{version}", version),
            method="DELETE",
            params={},
            data=None,
        )

    def get_script_by_version(self, version: str) -> ScriptVersion:
        """
        Retrieves a version of the script for an app.
        Returns the script text.

        Parameters
        ----------
        version: str
          Identifier of the script version, or 'current' for retrieving the current version.
        """
        response = self.auth.rest(
            path="/apps/{appId}/scripts/{version}".replace(
                "{appId}", self.attributes.id
            ).replace("{version}", version),
            method="GET",
            params={},
            data=None,
        )
        obj = ScriptVersion(**response.json())
        obj.auth = self.auth
        return obj

    def patch_script(self, version: str, data: NxPatch) -> None:
        """
        Updates a specific version of the script for an app.

        Parameters
        ----------
        version: str
          Identifier of the script version.
        data: NxPatch
          Array of patches for the object ScriptVersion.
          Only /versionMessage can be modified using operations add, remove and replace.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        self.auth.rest(
            path="/apps/{appId}/scripts/{version}".replace(
                "{appId}", self.attributes.id
            ).replace("{version}", version),
            method="PATCH",
            params={},
            data=data,
        )

    def get_script_versions(
        self, filter: str = None, limit: str = None, page: str = None
    ) -> ScriptMetaList:
        """
        Retrieves the script history for an app.
        Returns information about the saved versions of the script.

        Parameters
        ----------
        filter: str = None
          A scim filter expression defining which script versions should be retrieved. Filterable fields are:

          • ScriptId

          • ModifiedTime

          • ModifierId
        limit: str = None
          Maximum number of records to return from this request.
        page: str = None
          Opaque definition of which page of the result set to return. Returned from a previous call using the same filter. Not yet supported.
        """
        query_params = {}
        if filter is not None:
            query_params["filter"] = filter
        if limit is not None:
            query_params["limit"] = limit
        if page is not None:
            query_params["page"] = page
        response = self.auth.rest(
            path="/apps/{appId}/scripts".replace("{appId}", self.attributes.id),
            method="GET",
            params=query_params,
            data=None,
        )
        obj = ScriptMetaList(**response.json())
        obj.auth = self.auth
        return obj

    def create_script(self, data: ScriptVersion) -> None:
        """
        Sets script for an app.

        Parameters
        ----------
        data: ScriptVersion
          The script to set.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        self.auth.rest(
            path="/apps/{appId}/scripts".replace("{appId}", self.attributes.id),
            method="POST",
            params={},
            data=data,
        )

    def delete_space(self) -> NxApp:
        """
        Removes space from a specific app.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/apps/{appId}/space".replace("{appId}", self.attributes.id),
            method="DELETE",
            params={},
            data=None,
        )
        self.__init__(**response.json())
        return self

    def set_space(self, data: UpdateSpace) -> NxApp:
        """
        Sets space on a specific app.

        Parameters
        ----------
        data: UpdateSpace
          New space.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/apps/{appId}/space".replace("{appId}", self.attributes.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self

    def delete(self) -> None:
        """
        Deletes a specific app.

        Parameters
        ----------
        """
        self.auth.rest(
            path="/apps/{appId}".replace("{appId}", self.attributes.id),
            method="DELETE",
            params={},
            data=None,
        )

    def set(self, data: UpdateApp) -> NxApp:
        """
        Updates the information for a specific app.

        Parameters
        ----------
        data: UpdateApp
          Attributes that user wants to set.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/apps/{appId}".replace("{appId}", self.attributes.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self


@dataclass
class AnalysisComposition:
    """

    Attributes
    ----------
    description: AnalysisCompositionDescription
    dims: CompositionMinMax
      Upper and lower bounds for items of specific classification types
    geos: CompositionMinMax
      Upper and lower bounds for items of specific classification types
    items: CompositionMinMax
      Upper and lower bounds for items of specific classification types
    msrs: CompositionMinMax
      Upper and lower bounds for items of specific classification types
    temporals: CompositionMinMax
      Upper and lower bounds for items of specific classification types
    """

    description: AnalysisCompositionDescription = None
    dims: CompositionMinMax = None
    geos: CompositionMinMax = None
    items: CompositionMinMax = None
    msrs: CompositionMinMax = None
    temporals: CompositionMinMax = None

    def __init__(self_, **kvargs):
        if "description" in kvargs and kvargs["description"] is not None:
            if (
                type(kvargs["description"]).__name__
                == AnalysisComposition.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = AnalysisCompositionDescription(
                    **kvargs["description"]
                )
        if "dims" in kvargs and kvargs["dims"] is not None:
            if (
                type(kvargs["dims"]).__name__
                == AnalysisComposition.__annotations__["dims"]
            ):
                self_.dims = kvargs["dims"]
            else:
                self_.dims = CompositionMinMax(**kvargs["dims"])
        if "geos" in kvargs and kvargs["geos"] is not None:
            if (
                type(kvargs["geos"]).__name__
                == AnalysisComposition.__annotations__["geos"]
            ):
                self_.geos = kvargs["geos"]
            else:
                self_.geos = CompositionMinMax(**kvargs["geos"])
        if "items" in kvargs and kvargs["items"] is not None:
            if (
                type(kvargs["items"]).__name__
                == AnalysisComposition.__annotations__["items"]
            ):
                self_.items = kvargs["items"]
            else:
                self_.items = CompositionMinMax(**kvargs["items"])
        if "msrs" in kvargs and kvargs["msrs"] is not None:
            if (
                type(kvargs["msrs"]).__name__
                == AnalysisComposition.__annotations__["msrs"]
            ):
                self_.msrs = kvargs["msrs"]
            else:
                self_.msrs = CompositionMinMax(**kvargs["msrs"])
        if "temporals" in kvargs and kvargs["temporals"] is not None:
            if (
                type(kvargs["temporals"]).__name__
                == AnalysisComposition.__annotations__["temporals"]
            ):
                self_.temporals = kvargs["temporals"]
            else:
                self_.temporals = CompositionMinMax(**kvargs["temporals"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AnalysisCompositionDescription:
    """

    Attributes
    ----------
    long: str
    short: str
    """

    long: str = None
    short: str = None

    def __init__(self_, **kvargs):
        if "long" in kvargs and kvargs["long"] is not None:
            self_.long = kvargs["long"]
        if "short" in kvargs and kvargs["short"] is not None:
            self_.short = kvargs["short"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AnalysisDescriptor:
    """

    Attributes
    ----------
    compositions: list[AnalysisComposition]
    id: str
    requiresAutoCalendarPeriod: bool
      Used for period-specific analyses to indicate the defined or available calendar period must be of type autoCalendar
    requiresAvailableAnalysisPeriod: bool
      Used for period-specific analyses to indicate the temporal dimension must be associated with one or more analysis periods
    requiresDefinedAnalysisPeriod: bool
      Used for period-specific analyses to indicate the measure must be associated with one or more analysis periods
    supportsMasterItems: bool
      If analysis can work with master items (default is true)
    """

    compositions: list[AnalysisComposition] = None
    id: str = None
    requiresAutoCalendarPeriod: bool = None
    requiresAvailableAnalysisPeriod: bool = None
    requiresDefinedAnalysisPeriod: bool = None
    supportsMasterItems: bool = None

    def __init__(self_, **kvargs):
        if "compositions" in kvargs and kvargs["compositions"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == AnalysisDescriptor.__annotations__["compositions"]
                for e in kvargs["compositions"]
            ):
                self_.compositions = kvargs["compositions"]
            else:
                self_.compositions = [
                    AnalysisComposition(**e) for e in kvargs["compositions"]
                ]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if (
            "requiresAutoCalendarPeriod" in kvargs
            and kvargs["requiresAutoCalendarPeriod"] is not None
        ):
            self_.requiresAutoCalendarPeriod = kvargs["requiresAutoCalendarPeriod"]
        if (
            "requiresAvailableAnalysisPeriod" in kvargs
            and kvargs["requiresAvailableAnalysisPeriod"] is not None
        ):
            self_.requiresAvailableAnalysisPeriod = kvargs[
                "requiresAvailableAnalysisPeriod"
            ]
        if (
            "requiresDefinedAnalysisPeriod" in kvargs
            and kvargs["requiresDefinedAnalysisPeriod"] is not None
        ):
            self_.requiresDefinedAnalysisPeriod = kvargs[
                "requiresDefinedAnalysisPeriod"
            ]
        if (
            "supportsMasterItems" in kvargs
            and kvargs["supportsMasterItems"] is not None
        ):
            self_.supportsMasterItems = kvargs["supportsMasterItems"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AnalysisDescriptorResponse:
    """

    Attributes
    ----------
    data: list[AnalysisDescriptor]
    links: Links
    """

    data: list[AnalysisDescriptor] = None
    links: Links = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == AnalysisDescriptorResponse.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [AnalysisDescriptor(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == AnalysisDescriptorResponse.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = Links(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AnalysisDetails:
    """

    Attributes
    ----------
    analysis: Literal["breakdown", "changePoint", "comparison", "contribution", "correlation", "fact", "mutualInfo", "rank", "spike", "trend", "values"]
    analysisGroup: Literal["anomaly", "brekadown", "comparison", "correl", "fact", "list", "mutualInfo", "rank"]
    title: str
    """

    analysis: Literal[
        "breakdown",
        "changePoint",
        "comparison",
        "contribution",
        "correlation",
        "fact",
        "mutualInfo",
        "rank",
        "spike",
        "trend",
        "values",
    ] = None
    analysisGroup: Literal[
        "anomaly",
        "brekadown",
        "comparison",
        "correl",
        "fact",
        "list",
        "mutualInfo",
        "rank",
    ] = None
    title: str = None

    def __init__(self_, **kvargs):
        if "analysis" in kvargs and kvargs["analysis"] is not None:
            self_.analysis = kvargs["analysis"]
        if "analysisGroup" in kvargs and kvargs["analysisGroup"] is not None:
            self_.analysisGroup = kvargs["analysisGroup"]
        if "title" in kvargs and kvargs["title"] is not None:
            self_.title = kvargs["title"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AnalysisModelItemField:
    """

    Attributes
    ----------
    classifications: list[str]
      classification defines the default role that attribute can play in an analysis
    isHidden: bool
      whether the field is hidden in business logic
    name: str
      populated only for fields
    simplifiedClassifications: list[str]
    """

    classifications: list[str] = None
    isHidden: bool = None
    name: str = None
    simplifiedClassifications: list[str] = None

    def __init__(self_, **kvargs):
        if "classifications" in kvargs and kvargs["classifications"] is not None:
            self_.classifications = kvargs["classifications"]
        if "isHidden" in kvargs and kvargs["isHidden"] is not None:
            self_.isHidden = kvargs["isHidden"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if (
            "simplifiedClassifications" in kvargs
            and kvargs["simplifiedClassifications"] is not None
        ):
            self_.simplifiedClassifications = kvargs["simplifiedClassifications"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AnalysisModelItemMasterItem:
    """

    Attributes
    ----------
    caption: str
    classifications: list[str]
      classification defines the default role that attribute can play in an analysis
    isHidden: bool
      whether the master item is hidden in business logic
    libId: str
      only available for master items
    simplifiedClassifications: list[str]
    """

    caption: str = None
    classifications: list[str] = None
    isHidden: bool = None
    libId: str = None
    simplifiedClassifications: list[str] = None

    def __init__(self_, **kvargs):
        if "caption" in kvargs and kvargs["caption"] is not None:
            self_.caption = kvargs["caption"]
        if "classifications" in kvargs and kvargs["classifications"] is not None:
            self_.classifications = kvargs["classifications"]
        if "isHidden" in kvargs and kvargs["isHidden"] is not None:
            self_.isHidden = kvargs["isHidden"]
        if "libId" in kvargs and kvargs["libId"] is not None:
            self_.libId = kvargs["libId"]
        if (
            "simplifiedClassifications" in kvargs
            and kvargs["simplifiedClassifications"] is not None
        ):
            self_.simplifiedClassifications = kvargs["simplifiedClassifications"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AnalysisModelResponse:
    """

    Attributes
    ----------
    data: list[AnalysisModelResponseDetail]
    links: Links
    """

    data: list[AnalysisModelResponseDetail] = None
    links: Links = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == AnalysisModelResponse.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [AnalysisModelResponseDetail(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == AnalysisModelResponse.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = Links(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AnalysisModelResponseDetail:
    """

    Attributes
    ----------
    fields: list[AnalysisModelItemField]
    isDefinedLogicalModelValid: bool
      set only if previous property is true, to indicate if the business logic passes validation
    isLogicalModelEnabled: bool
      if the analysis model is constructed based on a user-defined business-logic (as opposed to a default one)
    masterItems: list[AnalysisModelItemMasterItem]
    """

    fields: list[AnalysisModelItemField] = None
    isDefinedLogicalModelValid: bool = None
    isLogicalModelEnabled: bool = None
    masterItems: list[AnalysisModelItemMasterItem] = None

    def __init__(self_, **kvargs):
        if "fields" in kvargs and kvargs["fields"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == AnalysisModelResponseDetail.__annotations__["fields"]
                for e in kvargs["fields"]
            ):
                self_.fields = kvargs["fields"]
            else:
                self_.fields = [AnalysisModelItemField(**e) for e in kvargs["fields"]]
        if (
            "isDefinedLogicalModelValid" in kvargs
            and kvargs["isDefinedLogicalModelValid"] is not None
        ):
            self_.isDefinedLogicalModelValid = kvargs["isDefinedLogicalModelValid"]
        if (
            "isLogicalModelEnabled" in kvargs
            and kvargs["isLogicalModelEnabled"] is not None
        ):
            self_.isLogicalModelEnabled = kvargs["isLogicalModelEnabled"]
        if "masterItems" in kvargs and kvargs["masterItems"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == AnalysisModelResponseDetail.__annotations__["masterItems"]
                for e in kvargs["masterItems"]
            ):
                self_.masterItems = kvargs["masterItems"]
            else:
                self_.masterItems = [
                    AnalysisModelItemMasterItem(**e) for e in kvargs["masterItems"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AnalysisRecommendRequest:
    """
    Request payload can be of two types, using natural language query or consist of fields or master items and optional target analysis.
    In below examples, consider sales as a master item and product as field, so to get recommendations using sales and product,
    you can utilize below three approaches, also you can set language parameter in headers as part of accept-language.
    Examples:
    ```
    {
      "text": "show me sales by product"
    }
    ```
    ```
    {
      "fields": [
        {
          "name": "product"
        }
      ],
      "libItems": [
        {
          libId: "NwQfJ"
        }
      ]
    }
    ```
    ```
    {
      "fields": [
        {
          "name": "product"
        }
      ],
      "libItems": [
        {
          "libId": "NwQfJ"
        }
      ],
      "targetAnalysis": {
        "id": "rank-rank"
      }
    }
    ```


    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AnalysisRecommendationResponse:
    """

    Attributes
    ----------
    data: list[AnalysisRecommendationResponseDetail]
    """

    data: list[AnalysisRecommendationResponseDetail] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == AnalysisRecommendationResponse.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [
                    AnalysisRecommendationResponseDetail(**e) for e in kvargs["data"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AnalysisRecommendationResponseDetail:
    """

    Attributes
    ----------
    nluInfo: list[PartialNluInfo]
    recAnalyses: list[RecommendedAnalysis]
    """

    nluInfo: list[PartialNluInfo] = None
    recAnalyses: list[RecommendedAnalysis] = None

    def __init__(self_, **kvargs):
        if "nluInfo" in kvargs and kvargs["nluInfo"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == AnalysisRecommendationResponseDetail.__annotations__["nluInfo"]
                for e in kvargs["nluInfo"]
            ):
                self_.nluInfo = kvargs["nluInfo"]
            else:
                self_.nluInfo = [PartialNluInfo(**e) for e in kvargs["nluInfo"]]
        if "recAnalyses" in kvargs and kvargs["recAnalyses"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == AnalysisRecommendationResponseDetail.__annotations__["recAnalyses"]
                for e in kvargs["recAnalyses"]
            ):
                self_.recAnalyses = kvargs["recAnalyses"]
            else:
                self_.recAnalyses = [
                    RecommendedAnalysis(**e) for e in kvargs["recAnalyses"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppAttributes:
    """

    Attributes
    ----------
    description: str
      The description of the application
    locale: str
      Set custom locale instead of the system default
    name: str
      The name (title) of the application
    spaceId: str
      The space ID of the application
    usage: Literal["ANALYTICS_USAGE", "DATA_PREPARATION_USAGE"]
      Indicates whether the app is used for Analytics or DataPreparation

      One of:

      • ANALYTICS or ANALYTICS_USAGE

      • DATA_PREPARATION or DATA_PREPARATION_USAGE
    """

    description: str = None
    locale: str = None
    name: str = None
    spaceId: str = None
    usage: Literal["ANALYTICS_USAGE", "DATA_PREPARATION_USAGE"] = None

    def __init__(self_, **kvargs):
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "locale" in kvargs and kvargs["locale"] is not None:
            self_.locale = kvargs["locale"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "spaceId" in kvargs and kvargs["spaceId"] is not None:
            self_.spaceId = kvargs["spaceId"]
        if "usage" in kvargs and kvargs["usage"] is not None:
            self_.usage = kvargs["usage"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppContentList:
    """

    Attributes
    ----------
    data: list[AppContentListItem]
      Content list items.
    library: str
      Content library name.
    subpath: str
      Content library relative listing path. Empty in case of root listed or representing actual subpath listed.
    """

    data: list[AppContentListItem] = None
    library: str = None
    subpath: str = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]" == AppContentList.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [AppContentListItem(**e) for e in kvargs["data"]]
        if "library" in kvargs and kvargs["library"] is not None:
            self_.library = kvargs["library"]
        if "subpath" in kvargs and kvargs["subpath"] is not None:
            self_.subpath = kvargs["subpath"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppContentListItem:
    """

    Attributes
    ----------
    id: str
      Unique content identifier.
    link: str
      Unique content link.
    name: str
      Content name.
    type: str
      Content type.
    """

    id: str = None
    link: str = None
    name: str = None
    type: str = None

    def __init__(self_, **kvargs):
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "link" in kvargs and kvargs["link"] is not None:
            self_.link = kvargs["link"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppUpdateAttributes:
    """

    Attributes
    ----------
    description: str
      The description of the application.
    name: str
      The name (title) of the application.
    """

    description: str = None
    name: str = None

    def __init__(self_, **kvargs):
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CompositionMinMax:
    """
    Upper and lower bounds for items of specific classification types

    Attributes
    ----------
    max: float
    min: float
    """

    max: float = None
    min: float = None

    def __init__(self_, **kvargs):
        if "max" in kvargs and kvargs["max"] is not None:
            self_.max = kvargs["max"]
        if "min" in kvargs and kvargs["min"] is not None:
            self_.min = kvargs["min"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CreateApp:
    """

    Attributes
    ----------
    attributes: AppAttributes
    """

    attributes: AppAttributes = None

    def __init__(self_, **kvargs):
        if "attributes" in kvargs and kvargs["attributes"] is not None:
            if (
                type(kvargs["attributes"]).__name__
                == CreateApp.__annotations__["attributes"]
            ):
                self_.attributes = kvargs["attributes"]
            else:
                self_.attributes = AppAttributes(**kvargs["attributes"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DataModelMetadata:
    """

    Attributes
    ----------
    fields: list[FieldMetadata]
      List of field descriptions.
    has_section_access: bool
      If set to true, the app has section access configured.
    is_direct_query_mode: bool
    reload_meta: LastReloadMetadata
    static_byte_size: int
      Static memory usage for the app.
    tables: list[TableMetadata]
      List of table descriptions.
    tables_profiling_data: list[TableProfilingData]
      Profiling data of the tables in the app.
    usage: Literal["ANALYTICS_USAGE", "DATA_PREPARATION_USAGE"]

      One of:

      • ANALYTICS or ANALYTICS_USAGE

      • DATA_PREPARATION or DATA_PREPARATION_USAGE
    """

    fields: list[FieldMetadata] = None
    has_section_access: bool = None
    is_direct_query_mode: bool = None
    reload_meta: LastReloadMetadata = None
    static_byte_size: int = None
    tables: list[TableMetadata] = None
    tables_profiling_data: list[TableProfilingData] = None
    usage: Literal["ANALYTICS_USAGE", "DATA_PREPARATION_USAGE"] = None

    def __init__(self_, **kvargs):
        if "fields" in kvargs and kvargs["fields"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == DataModelMetadata.__annotations__["fields"]
                for e in kvargs["fields"]
            ):
                self_.fields = kvargs["fields"]
            else:
                self_.fields = [FieldMetadata(**e) for e in kvargs["fields"]]
        if "has_section_access" in kvargs and kvargs["has_section_access"] is not None:
            self_.has_section_access = kvargs["has_section_access"]
        if (
            "is_direct_query_mode" in kvargs
            and kvargs["is_direct_query_mode"] is not None
        ):
            self_.is_direct_query_mode = kvargs["is_direct_query_mode"]
        if "reload_meta" in kvargs and kvargs["reload_meta"] is not None:
            if (
                type(kvargs["reload_meta"]).__name__
                == DataModelMetadata.__annotations__["reload_meta"]
            ):
                self_.reload_meta = kvargs["reload_meta"]
            else:
                self_.reload_meta = LastReloadMetadata(**kvargs["reload_meta"])
        if "static_byte_size" in kvargs and kvargs["static_byte_size"] is not None:
            self_.static_byte_size = kvargs["static_byte_size"]
        if "tables" in kvargs and kvargs["tables"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == DataModelMetadata.__annotations__["tables"]
                for e in kvargs["tables"]
            ):
                self_.tables = kvargs["tables"]
            else:
                self_.tables = [TableMetadata(**e) for e in kvargs["tables"]]
        if (
            "tables_profiling_data" in kvargs
            and kvargs["tables_profiling_data"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == DataModelMetadata.__annotations__["tables_profiling_data"]
                for e in kvargs["tables_profiling_data"]
            ):
                self_.tables_profiling_data = kvargs["tables_profiling_data"]
            else:
                self_.tables_profiling_data = [
                    TableProfilingData(**e) for e in kvargs["tables_profiling_data"]
                ]
        if "usage" in kvargs and kvargs["usage"] is not None:
            self_.usage = kvargs["usage"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldAttributes:
    """
    Sets the formatting of a field.
    The properties of qFieldAttributes and the formatting mechanism are described below.

     Formatting mechanism:
    The formatting mechanism depends on the type set in qType, as shown below:
    In case of inconsistencies between the type and the format pattern, the format pattern takes precedence over the type.

     Type is DATE, TIME, TIMESTAMP or INTERVAL:
    The following applies:

    • If a format pattern is defined in qFmt , the formatting is as defined in qFmt .

    • If qFmt is empty, the formatting is defined by the number interpretation variables included at the top of the script ( TimeFormat , DateFormat , TimeStampFormat ).

    • The properties qDec , qThou , qnDec , qUseThou are not used.

     Type is INTEGER:
    The following applies:

    • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the formatting mechanism uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

    • If no format pattern is defined in qFmt , no formatting is applied. The properties qDec , qThou , qnDec , qUseThou and the number interpretation variables defined in the script are not used .

     Type is REAL:
    The following applies:

    • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

    • If no format pattern is defined in qFmt , and if the value is almost an integer value (for example, 14,000012), the value is formatted as an integer. The properties qDec , qThou , qnDec , qUseThou are not used.

    • If no format pattern is defined in qFmt , and if qnDec is defined and not 0, the property qDec is used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

    • If no format pattern is defined in qFmt , and if qnDec is 0, the number of decimals is 14 and the property qDec is used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

     Type is FIX:
    The following applies:

    • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

    • If no format pattern is defined in qFmt , the properties qDec and qnDec are used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

     Type is MONEY:
    The following applies:

    • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of any script ( MoneyDecimalSep and MoneyThousandSep ).

    • If no format pattern is defined in qFmt , the engine uses the number interpretation variables included at the top of the script ( MoneyDecimalSep and MoneyThousandSep ).

     Type is ASCII:
    No formatting, qFmt is ignored.

    Attributes
    ----------
    Dec: str
      Defines the decimal separator.
      Example: .
    Fmt: str
      Defines the format pattern that applies to qText .
      Is used in connection to the type of the field (parameter qType ).
      For more information, see Formatting mechanism.
      Example: YYYY-MM-DD for a date.
    Thou: str
      Defines the thousand separator (if any).
      Is used if qUseThou is set to 1.
      Example: ,
    Type: Literal["UNKNOWN", "ASCII", "INTEGER", "REAL", "FIX", "MONEY", "DATE", "TIME", "TIMESTAMP", "INTERVAL"]
      Type of the field.
      Default is U.

      One of:

      • U or UNKNOWN

      • A or ASCII

      • I or INTEGER

      • R or REAL

      • F or FIX

      • M or MONEY

      • D or DATE

      • T or TIME

      • TS or TIMESTAMP

      • IV or INTERVAL
    UseThou: int
      Defines whether or not a thousands separator must be used.
      Default is 0.
    nDec: int
      Number of decimals.
      Default is 10.
    """

    Dec: str = None
    Fmt: str = None
    Thou: str = None
    Type: Literal[
        "UNKNOWN",
        "ASCII",
        "INTEGER",
        "REAL",
        "FIX",
        "MONEY",
        "DATE",
        "TIME",
        "TIMESTAMP",
        "INTERVAL",
    ] = "UNKNOWN"
    UseThou: int = None
    nDec: int = 10

    def __init__(self_, **kvargs):
        if "Dec" in kvargs and kvargs["Dec"] is not None:
            self_.Dec = kvargs["Dec"]
        if "Fmt" in kvargs and kvargs["Fmt"] is not None:
            self_.Fmt = kvargs["Fmt"]
        if "Thou" in kvargs and kvargs["Thou"] is not None:
            self_.Thou = kvargs["Thou"]
        if "Type" in kvargs and kvargs["Type"] is not None:
            self_.Type = kvargs["Type"]
        if "UseThou" in kvargs and kvargs["UseThou"] is not None:
            self_.UseThou = kvargs["UseThou"]
        if "nDec" in kvargs and kvargs["nDec"] is not None:
            self_.nDec = kvargs["nDec"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldInTableProfilingData:
    """

    Attributes
    ----------
    Average: float
      Average of all numerical values. NaN otherwise.
    AvgStringLen: float
      Average string length of textual values. 0 otherwise.
    DistinctNumericValues: int
      Number of distinct numeric values
    DistinctTextValues: int
      Number of distinct text values
    DistinctValues: int
      Number of distinct values
    EmptyStrings: int
      Number of empty strings
    FieldTags: list[str]
      List of tags related to the field.
    FirstSorted: str
      For textual values the first sorted string.
    Fractiles: list[float]
      The .01, .05, .1, .25, .5, .75, .9, .95, .99 fractiles. Array of NaN otherwise.
    FrequencyDistribution: FrequencyDistributionData
    Kurtosis: float
      Kurtosis of the numerical values. NaN otherwise.
    LastSorted: str
      For textual values the last sorted string.
    Max: float
      Maximum value of numerical values. NaN otherwise.
    MaxStringLen: int
      Maximum string length of textual values. 0 otherwise.
    Median: float
      Median of all numerical values. NaN otherwise.
    Min: float
      Minimum value of numerical values. NaN otherwise.
    MinStringLen: int
      Minimum string length of textual values. 0 otherwise.
    MostFrequent: list[SymbolFrequency]
      Three most frequent values and their frequencies
    Name: str
      Name of the field.
    NegValues: int
      Number of negative values
    NullValues: int
      Number of null values
    NumberFormat: FieldAttributes
      Sets the formatting of a field.
      The properties of qFieldAttributes and the formatting mechanism are described below.

       Formatting mechanism:
      The formatting mechanism depends on the type set in qType, as shown below:
      In case of inconsistencies between the type and the format pattern, the format pattern takes precedence over the type.

       Type is DATE, TIME, TIMESTAMP or INTERVAL:
      The following applies:

      • If a format pattern is defined in qFmt , the formatting is as defined in qFmt .

      • If qFmt is empty, the formatting is defined by the number interpretation variables included at the top of the script ( TimeFormat , DateFormat , TimeStampFormat ).

      • The properties qDec , qThou , qnDec , qUseThou are not used.

       Type is INTEGER:
      The following applies:

      • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the formatting mechanism uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

      • If no format pattern is defined in qFmt , no formatting is applied. The properties qDec , qThou , qnDec , qUseThou and the number interpretation variables defined in the script are not used .

       Type is REAL:
      The following applies:

      • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

      • If no format pattern is defined in qFmt , and if the value is almost an integer value (for example, 14,000012), the value is formatted as an integer. The properties qDec , qThou , qnDec , qUseThou are not used.

      • If no format pattern is defined in qFmt , and if qnDec is defined and not 0, the property qDec is used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

      • If no format pattern is defined in qFmt , and if qnDec is 0, the number of decimals is 14 and the property qDec is used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

       Type is FIX:
      The following applies:

      • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of the script ( DecimalSep and ThousandSep ).

      • If no format pattern is defined in qFmt , the properties qDec and qnDec are used. If qDec is not defined, the variable DecimalSep defined at the top of the script is used.

       Type is MONEY:
      The following applies:

      • If a format pattern is defined in qFmt , the engine looks at the values set in qDec and qThou . If these properties are not defined, the engine uses the number interpretation variables included at the top of any script ( MoneyDecimalSep and MoneyThousandSep ).

      • If no format pattern is defined in qFmt , the engine uses the number interpretation variables included at the top of the script ( MoneyDecimalSep and MoneyThousandSep ).

       Type is ASCII:
      No formatting, qFmt is ignored.
    NumericValues: int
      Number of numeric values
    PosValues: int
      Number of positive values
    Skewness: float
      Skewness of the numerical values. NaN otherwise.
    Std: float
      Standard deviation of numerical values. NaN otherwise.
    Sum: float
      Sum of all numerical values. NaN otherwise.
    Sum2: float
      Squared sum of all numerical values. NaN otherwise.
    SumStringLen: int
      Sum of all characters in strings in the field
    TextValues: int
      Number of textual values
    ZeroValues: int
      Number of zero values for numerical values
    """

    Average: float = None
    AvgStringLen: float = None
    DistinctNumericValues: int = None
    DistinctTextValues: int = None
    DistinctValues: int = None
    EmptyStrings: int = None
    FieldTags: list[str] = None
    FirstSorted: str = None
    Fractiles: list[float] = None
    FrequencyDistribution: FrequencyDistributionData = None
    Kurtosis: float = None
    LastSorted: str = None
    Max: float = None
    MaxStringLen: int = None
    Median: float = None
    Min: float = None
    MinStringLen: int = None
    MostFrequent: list[SymbolFrequency] = None
    Name: str = None
    NegValues: int = None
    NullValues: int = None
    NumberFormat: FieldAttributes = None
    NumericValues: int = None
    PosValues: int = None
    Skewness: float = None
    Std: float = None
    Sum: float = None
    Sum2: float = None
    SumStringLen: int = None
    TextValues: int = None
    ZeroValues: int = None

    def __init__(self_, **kvargs):
        if "Average" in kvargs and kvargs["Average"] is not None:
            self_.Average = kvargs["Average"]
        if "AvgStringLen" in kvargs and kvargs["AvgStringLen"] is not None:
            self_.AvgStringLen = kvargs["AvgStringLen"]
        if (
            "DistinctNumericValues" in kvargs
            and kvargs["DistinctNumericValues"] is not None
        ):
            self_.DistinctNumericValues = kvargs["DistinctNumericValues"]
        if "DistinctTextValues" in kvargs and kvargs["DistinctTextValues"] is not None:
            self_.DistinctTextValues = kvargs["DistinctTextValues"]
        if "DistinctValues" in kvargs and kvargs["DistinctValues"] is not None:
            self_.DistinctValues = kvargs["DistinctValues"]
        if "EmptyStrings" in kvargs and kvargs["EmptyStrings"] is not None:
            self_.EmptyStrings = kvargs["EmptyStrings"]
        if "FieldTags" in kvargs and kvargs["FieldTags"] is not None:
            self_.FieldTags = kvargs["FieldTags"]
        if "FirstSorted" in kvargs and kvargs["FirstSorted"] is not None:
            self_.FirstSorted = kvargs["FirstSorted"]
        if "Fractiles" in kvargs and kvargs["Fractiles"] is not None:
            self_.Fractiles = kvargs["Fractiles"]
        if (
            "FrequencyDistribution" in kvargs
            and kvargs["FrequencyDistribution"] is not None
        ):
            if (
                type(kvargs["FrequencyDistribution"]).__name__
                == FieldInTableProfilingData.__annotations__["FrequencyDistribution"]
            ):
                self_.FrequencyDistribution = kvargs["FrequencyDistribution"]
            else:
                self_.FrequencyDistribution = FrequencyDistributionData(
                    **kvargs["FrequencyDistribution"]
                )
        if "Kurtosis" in kvargs and kvargs["Kurtosis"] is not None:
            self_.Kurtosis = kvargs["Kurtosis"]
        if "LastSorted" in kvargs and kvargs["LastSorted"] is not None:
            self_.LastSorted = kvargs["LastSorted"]
        if "Max" in kvargs and kvargs["Max"] is not None:
            self_.Max = kvargs["Max"]
        if "MaxStringLen" in kvargs and kvargs["MaxStringLen"] is not None:
            self_.MaxStringLen = kvargs["MaxStringLen"]
        if "Median" in kvargs and kvargs["Median"] is not None:
            self_.Median = kvargs["Median"]
        if "Min" in kvargs and kvargs["Min"] is not None:
            self_.Min = kvargs["Min"]
        if "MinStringLen" in kvargs and kvargs["MinStringLen"] is not None:
            self_.MinStringLen = kvargs["MinStringLen"]
        if "MostFrequent" in kvargs and kvargs["MostFrequent"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == FieldInTableProfilingData.__annotations__["MostFrequent"]
                for e in kvargs["MostFrequent"]
            ):
                self_.MostFrequent = kvargs["MostFrequent"]
            else:
                self_.MostFrequent = [
                    SymbolFrequency(**e) for e in kvargs["MostFrequent"]
                ]
        if "Name" in kvargs and kvargs["Name"] is not None:
            self_.Name = kvargs["Name"]
        if "NegValues" in kvargs and kvargs["NegValues"] is not None:
            self_.NegValues = kvargs["NegValues"]
        if "NullValues" in kvargs and kvargs["NullValues"] is not None:
            self_.NullValues = kvargs["NullValues"]
        if "NumberFormat" in kvargs and kvargs["NumberFormat"] is not None:
            if (
                type(kvargs["NumberFormat"]).__name__
                == FieldInTableProfilingData.__annotations__["NumberFormat"]
            ):
                self_.NumberFormat = kvargs["NumberFormat"]
            else:
                self_.NumberFormat = FieldAttributes(**kvargs["NumberFormat"])
        if "NumericValues" in kvargs and kvargs["NumericValues"] is not None:
            self_.NumericValues = kvargs["NumericValues"]
        if "PosValues" in kvargs and kvargs["PosValues"] is not None:
            self_.PosValues = kvargs["PosValues"]
        if "Skewness" in kvargs and kvargs["Skewness"] is not None:
            self_.Skewness = kvargs["Skewness"]
        if "Std" in kvargs and kvargs["Std"] is not None:
            self_.Std = kvargs["Std"]
        if "Sum" in kvargs and kvargs["Sum"] is not None:
            self_.Sum = kvargs["Sum"]
        if "Sum2" in kvargs and kvargs["Sum2"] is not None:
            self_.Sum2 = kvargs["Sum2"]
        if "SumStringLen" in kvargs and kvargs["SumStringLen"] is not None:
            self_.SumStringLen = kvargs["SumStringLen"]
        if "TextValues" in kvargs and kvargs["TextValues"] is not None:
            self_.TextValues = kvargs["TextValues"]
        if "ZeroValues" in kvargs and kvargs["ZeroValues"] is not None:
            self_.ZeroValues = kvargs["ZeroValues"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldMetadata:
    """

    Attributes
    ----------
    always_one_selected: bool
      If set to true, the field has one and only one selection (not 0 and not more than 1).
      If this property is set to true, the field cannot be cleared anymore and no more selections can be performed in that field.
      The default value is false.
    byte_size: int
      Static RAM memory used in bytes.
    cardinal: int
      Number of distinct field values.
    comment: str
      Field comment.
    distinct_only: bool
      If set to true, only distinct field values are shown.
      The default value is false.
    hash: str
      Hash of the data in the field. If the data in a reload is the same, the hash will be consistent.
    is_hidden: bool
      If set to true, the field is hidden.
      The default value is false.
    is_locked: bool
      If set to true, the field is locked.
      The default value is false.
    is_numeric: bool
      Is set to true if the value is a numeric.
      The default value is false.
    is_semantic: bool
      If set to true, the field is semantic.
      The default value is false.
    is_system: bool
      If set to true, the field is a system field.
      The default value is false.
    name: str
      Name of the field.
    src_tables: list[str]
      List of table names.
    tags: list[str]
      Gives information on a field. For example, it can return the type of the field.
      Examples: key, text, ASCII.
    total_count: int
      Total number of field values.
    """

    always_one_selected: bool = None
    byte_size: int = None
    cardinal: int = None
    comment: str = None
    distinct_only: bool = None
    hash: str = None
    is_hidden: bool = None
    is_locked: bool = None
    is_numeric: bool = None
    is_semantic: bool = None
    is_system: bool = None
    name: str = None
    src_tables: list[str] = None
    tags: list[str] = None
    total_count: int = None

    def __init__(self_, **kvargs):
        if (
            "always_one_selected" in kvargs
            and kvargs["always_one_selected"] is not None
        ):
            self_.always_one_selected = kvargs["always_one_selected"]
        if "byte_size" in kvargs and kvargs["byte_size"] is not None:
            self_.byte_size = kvargs["byte_size"]
        if "cardinal" in kvargs and kvargs["cardinal"] is not None:
            self_.cardinal = kvargs["cardinal"]
        if "comment" in kvargs and kvargs["comment"] is not None:
            self_.comment = kvargs["comment"]
        if "distinct_only" in kvargs and kvargs["distinct_only"] is not None:
            self_.distinct_only = kvargs["distinct_only"]
        if "hash" in kvargs and kvargs["hash"] is not None:
            self_.hash = kvargs["hash"]
        if "is_hidden" in kvargs and kvargs["is_hidden"] is not None:
            self_.is_hidden = kvargs["is_hidden"]
        if "is_locked" in kvargs and kvargs["is_locked"] is not None:
            self_.is_locked = kvargs["is_locked"]
        if "is_numeric" in kvargs and kvargs["is_numeric"] is not None:
            self_.is_numeric = kvargs["is_numeric"]
        if "is_semantic" in kvargs and kvargs["is_semantic"] is not None:
            self_.is_semantic = kvargs["is_semantic"]
        if "is_system" in kvargs and kvargs["is_system"] is not None:
            self_.is_system = kvargs["is_system"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "src_tables" in kvargs and kvargs["src_tables"] is not None:
            self_.src_tables = kvargs["src_tables"]
        if "tags" in kvargs and kvargs["tags"] is not None:
            self_.tags = kvargs["tags"]
        if "total_count" in kvargs and kvargs["total_count"] is not None:
            self_.total_count = kvargs["total_count"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FrequencyDistributionData:
    """

    Attributes
    ----------
    BinsEdges: list[float]
      Bins edges.
    Frequencies: list[int]
      Bins frequencies.
    NumberOfBins: int
      Number of bins.
    """

    BinsEdges: list[float] = None
    Frequencies: list[int] = None
    NumberOfBins: int = None

    def __init__(self_, **kvargs):
        if "BinsEdges" in kvargs and kvargs["BinsEdges"] is not None:
            self_.BinsEdges = kvargs["BinsEdges"]
        if "Frequencies" in kvargs and kvargs["Frequencies"] is not None:
            self_.Frequencies = kvargs["Frequencies"]
        if "NumberOfBins" in kvargs and kvargs["NumberOfBins"] is not None:
            self_.NumberOfBins = kvargs["NumberOfBins"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class HardwareMeta:
    """

    Attributes
    ----------
    logical_cores: int
      Number of logical cores available.
    total_memory: int
      RAM available.
    """

    logical_cores: int = None
    total_memory: int = None

    def __init__(self_, **kvargs):
        if "logical_cores" in kvargs and kvargs["logical_cores"] is not None:
            self_.logical_cores = kvargs["logical_cores"]
        if "total_memory" in kvargs and kvargs["total_memory"] is not None:
            self_.total_memory = kvargs["total_memory"]
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


@dataclass
class JsonObject:
    """
    Contains dynamic JSON data specified by the client.

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LastReloadMetadata:
    """

    Attributes
    ----------
    cpu_time_spent_ms: int
      Number of CPU milliseconds it took to reload the app.
    hardware: HardwareMeta
    peak_memory_bytes: int
      Maximum number of bytes used during reload of the app.
    """

    cpu_time_spent_ms: int = None
    hardware: HardwareMeta = None
    peak_memory_bytes: int = None

    def __init__(self_, **kvargs):
        if "cpu_time_spent_ms" in kvargs and kvargs["cpu_time_spent_ms"] is not None:
            self_.cpu_time_spent_ms = kvargs["cpu_time_spent_ms"]
        if "hardware" in kvargs and kvargs["hardware"] is not None:
            if (
                type(kvargs["hardware"]).__name__
                == LastReloadMetadata.__annotations__["hardware"]
            ):
                self_.hardware = kvargs["hardware"]
            else:
                self_.hardware = HardwareMeta(**kvargs["hardware"])
        if "peak_memory_bytes" in kvargs and kvargs["peak_memory_bytes"] is not None:
            self_.peak_memory_bytes = kvargs["peak_memory_bytes"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LineageInfoRest:
    """

    Attributes
    ----------
    discriminator: str
      A string indicating the origin of the data:

      • [filename]: the data comes from a local file.

      • INLINE: the data is entered inline in the load script.

      • RESIDENT: the data comes from a resident table. The table name is listed.

      • AUTOGENERATE: the data is generated from the load script (no external table of data source).

      • Provider: the data comes from a data connection. The connector source name is listed.

      • [webfile]: the data comes from a web-based file.

      • STORE: path to QVD or TXT file where data is stored.

      • EXTENSION: the data comes from a Server Side Extension (SSE).
    statement: str
      The LOAD and SELECT script statements from the data load script.
    """

    discriminator: str = None
    statement: str = None

    def __init__(self_, **kvargs):
        if "discriminator" in kvargs and kvargs["discriminator"] is not None:
            self_.discriminator = kvargs["discriminator"]
        if "statement" in kvargs and kvargs["statement"] is not None:
            self_.statement = kvargs["statement"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Links:
    """

    Attributes
    ----------
    next: Href
    prev: Href
    self: Href
    """

    next: Href = None
    prev: Href = None
    self: Href = None

    def __init__(self_, **kvargs):
        if "next" in kvargs and kvargs["next"] is not None:
            if type(kvargs["next"]).__name__ == Links.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = Href(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if type(kvargs["prev"]).__name__ == Links.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Href(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == Links.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Href(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Log:
    """

    Attributes
    ----------
    log: str
      Provides a link to download the log file.
    """

    log: str = None

    def __init__(self_, **kvargs):
        if "log" in kvargs and kvargs["log"] is not None:
            self_.log = kvargs["log"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NavigationLink:
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
class NavigationLinks:
    """

    Attributes
    ----------
    next: NavigationLink
    prev: NavigationLink
    """

    next: NavigationLink = None
    prev: NavigationLink = None

    def __init__(self_, **kvargs):
        if "next" in kvargs and kvargs["next"] is not None:
            if type(kvargs["next"]).__name__ == NavigationLinks.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = NavigationLink(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if type(kvargs["prev"]).__name__ == NavigationLinks.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = NavigationLink(**kvargs["prev"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAppCreatePrivileges:
    """

    Attributes
    ----------
    canCreate: bool
      Is set to true if the user has privileges to create the resource.
    resource: str
      Type of resource. For example, sheet, story, bookmark, etc.
    """

    canCreate: bool = None
    resource: str = None

    def __init__(self_, **kvargs):
        if "canCreate" in kvargs and kvargs["canCreate"] is not None:
            self_.canCreate = kvargs["canCreate"]
        if "resource" in kvargs and kvargs["resource"] is not None:
            self_.resource = kvargs["resource"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAppObject:
    """
    Application object attributes and user privileges.

    Attributes
    ----------
    attributes: NxObjectAttributes
      App object attributes. This structure can also contain extra user-defined attributes.
    privileges: list[str]
      Application object privileges.
      Hints to the client what actions the user is allowed to perform.
      Could be any of:

      • read

      • create

      • update

      • delete

      • publish

      • exportdata

      • change_owner
    """

    attributes: NxObjectAttributes = None
    privileges: list[str] = None

    def __init__(self_, **kvargs):
        if "attributes" in kvargs and kvargs["attributes"] is not None:
            if (
                type(kvargs["attributes"]).__name__
                == NxAppObject.__annotations__["attributes"]
            ):
                self_.attributes = kvargs["attributes"]
            else:
                self_.attributes = NxObjectAttributes(**kvargs["attributes"])
        if "privileges" in kvargs and kvargs["privileges"] is not None:
            self_.privileges = kvargs["privileges"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAttributes:
    """
    App attributes. This structure can also contain extra user-defined attributes.

    Attributes
    ----------
    createdDate: str
      The date and time when the app was created.
    custom: JsonObject
      Contains dynamic JSON data specified by the client.
    description: str
      App description.
    dynamicColor: str
      The dynamic color of the app.
    encrypted: bool
      If set to true, the app is encrypted.
    hasSectionAccess: bool
      If set to true, the app has section access configured,
    id: str
      The App ID.
    isDirectQueryMode: bool
      True if the app is a Direct Query app, false if not
    lastReloadTime: str
      Date and time of the last reload of the app.
    modifiedDate: str
      The date and time when the app was modified.
    name: str
      App name.
    originAppId: str
      The Origin App ID for published apps.
    owner: str
      Deprecated. Use user api to fetch user metadata.
    ownerId: str
      Identifier of the app owner.
    publishTime: str
      The date and time when the app was published, empty if unpublished.
    published: bool
      True if the app is published on-prem, distributed in QCS, false if not.
    thumbnail: str
      App thumbnail.
    usage: Literal["ANALYTICS_USAGE", "DATA_PREPARATION_USAGE"]

      One of:

      • ANALYTICS or ANALYTICS_USAGE

      • DATA_PREPARATION or DATA_PREPARATION_USAGE
    """

    createdDate: str = None
    custom: JsonObject = None
    description: str = None
    dynamicColor: str = None
    encrypted: bool = None
    hasSectionAccess: bool = None
    id: str = None
    isDirectQueryMode: bool = None
    lastReloadTime: str = None
    modifiedDate: str = None
    name: str = None
    originAppId: str = None
    owner: str = None
    ownerId: str = None
    publishTime: str = None
    published: bool = None
    thumbnail: str = None
    usage: Literal["ANALYTICS_USAGE", "DATA_PREPARATION_USAGE"] = None

    def __init__(self_, **kvargs):
        if "createdDate" in kvargs and kvargs["createdDate"] is not None:
            self_.createdDate = kvargs["createdDate"]
        if "custom" in kvargs and kvargs["custom"] is not None:
            if (
                type(kvargs["custom"]).__name__
                == NxAttributes.__annotations__["custom"]
            ):
                self_.custom = kvargs["custom"]
            else:
                self_.custom = JsonObject(**kvargs["custom"])
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "dynamicColor" in kvargs and kvargs["dynamicColor"] is not None:
            self_.dynamicColor = kvargs["dynamicColor"]
        if "encrypted" in kvargs and kvargs["encrypted"] is not None:
            self_.encrypted = kvargs["encrypted"]
        if "hasSectionAccess" in kvargs and kvargs["hasSectionAccess"] is not None:
            self_.hasSectionAccess = kvargs["hasSectionAccess"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "isDirectQueryMode" in kvargs and kvargs["isDirectQueryMode"] is not None:
            self_.isDirectQueryMode = kvargs["isDirectQueryMode"]
        if "lastReloadTime" in kvargs and kvargs["lastReloadTime"] is not None:
            self_.lastReloadTime = kvargs["lastReloadTime"]
        if "modifiedDate" in kvargs and kvargs["modifiedDate"] is not None:
            self_.modifiedDate = kvargs["modifiedDate"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "originAppId" in kvargs and kvargs["originAppId"] is not None:
            self_.originAppId = kvargs["originAppId"]
        if "owner" in kvargs and kvargs["owner"] is not None:
            self_.owner = kvargs["owner"]
        if "ownerId" in kvargs and kvargs["ownerId"] is not None:
            self_.ownerId = kvargs["ownerId"]
        if "publishTime" in kvargs and kvargs["publishTime"] is not None:
            self_.publishTime = kvargs["publishTime"]
        if "published" in kvargs and kvargs["published"] is not None:
            self_.published = kvargs["published"]
        if "thumbnail" in kvargs and kvargs["thumbnail"] is not None:
            self_.thumbnail = kvargs["thumbnail"]
        if "usage" in kvargs and kvargs["usage"] is not None:
            self_.usage = kvargs["usage"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxObjectAttributes:
    """
    App object attributes. This structure can also contain extra user-defined attributes.

    Attributes
    ----------
    approved: bool
      True if the object is approved.
    createdAt: str
      The date and time when the object was created.
    description: str
      Object description.
    genericType: Literal["genericObject", "genericBookmark", "genericMeasure", "genericDimension", "genericVariable"]
      The generic type of the object.

      One of:

      • genericObject

      • genericBookmark

      • genericMeasure

      • genericDimension

      • genericVariable
    id: str
      The object Id.
    name: str
      Object name.
    objectType: str
      The type of the object.
    ownerId: str
      The object owner's Id.
    publishedAt: str
      The date and time when the object was published, empty if unpublished.
    updatedAt: str
      The date and time when the object was modified.
    """

    approved: bool = None
    createdAt: str = None
    description: str = None
    genericType: Literal[
        "genericObject",
        "genericBookmark",
        "genericMeasure",
        "genericDimension",
        "genericVariable",
    ] = None
    id: str = None
    name: str = None
    objectType: str = None
    ownerId: str = None
    publishedAt: str = None
    updatedAt: str = None

    def __init__(self_, **kvargs):
        if "approved" in kvargs and kvargs["approved"] is not None:
            self_.approved = kvargs["approved"]
        if "createdAt" in kvargs and kvargs["createdAt"] is not None:
            self_.createdAt = kvargs["createdAt"]
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "genericType" in kvargs and kvargs["genericType"] is not None:
            self_.genericType = kvargs["genericType"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "objectType" in kvargs and kvargs["objectType"] is not None:
            self_.objectType = kvargs["objectType"]
        if "ownerId" in kvargs and kvargs["ownerId"] is not None:
            self_.ownerId = kvargs["ownerId"]
        if "publishedAt" in kvargs and kvargs["publishedAt"] is not None:
            self_.publishedAt = kvargs["publishedAt"]
        if "updatedAt" in kvargs and kvargs["updatedAt"] is not None:
            self_.updatedAt = kvargs["updatedAt"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPatch:
    """

    Attributes
    ----------
    Op: Literal["Add", "Remove", "Replace"]
      Operation to perform.

      One of:

      • add or Add

      • remove or Remove

      • replace or Replace
    Path: str
      Path to the property to add, remove or replace.
    Value: str
      This parameter is not used in a remove operation.
      Corresponds to the value of the property to add or to the new value of the property to update.
      Examples:
      "false", "2", "\"New title\""
    """

    Op: Literal["Add", "Remove", "Replace"] = None
    Path: str = None
    Value: str = None

    def __init__(self_, **kvargs):
        if "Op" in kvargs and kvargs["Op"] is not None:
            self_.Op = kvargs["Op"]
        if "Path" in kvargs and kvargs["Path"] is not None:
            self_.Path = kvargs["Path"]
        if "Value" in kvargs and kvargs["Value"] is not None:
            self_.Value = kvargs["Value"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class PartialNluInfo:
    """
    Contains break down of the asked question in the form of tokens with their classification.

    Attributes
    ----------
    fieldName: str
      Qlik sense application field selected for given token or phrase
    fieldValue: str
      Filter value found from query
    role: Literal["dimension", "measure", "date"]
      Role of the token or phrase from query
    text: str
      Matching token or phrase from query
    type: Literal["field", "filter", "master_dimension", "master_measure", "custom_analysis"]
      Type of token from query
    """

    fieldName: str = None
    fieldValue: str = None
    role: Literal["dimension", "measure", "date"] = None
    text: str = None
    type: Literal[
        "field", "filter", "master_dimension", "master_measure", "custom_analysis"
    ] = None

    def __init__(self_, **kvargs):
        if "fieldName" in kvargs and kvargs["fieldName"] is not None:
            self_.fieldName = kvargs["fieldName"]
        if "fieldValue" in kvargs and kvargs["fieldValue"] is not None:
            self_.fieldValue = kvargs["fieldValue"]
        if "role" in kvargs and kvargs["role"] is not None:
            self_.role = kvargs["role"]
        if "text" in kvargs and kvargs["text"] is not None:
            self_.text = kvargs["text"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class PublishApp:
    """

    Attributes
    ----------
    attributes: AppUpdateAttributes
    data: Literal["source", "target"]
      The published app will have data from source or target app.
      The default is source.


      • source: Publish with source data

      • target: Publish with target data
    moveApp: bool
      The original is moved instead of copied. The current published state of all objects is kept.
    originAppId: str
      If app is moved, originAppId needs to be provided.
    spaceId: str
      The managed space ID where the app will be published.
    """

    attributes: AppUpdateAttributes = None
    data: Literal["source", "target"] = None
    moveApp: bool = None
    originAppId: str = None
    spaceId: str = None

    def __init__(self_, **kvargs):
        if "attributes" in kvargs and kvargs["attributes"] is not None:
            if (
                type(kvargs["attributes"]).__name__
                == PublishApp.__annotations__["attributes"]
            ):
                self_.attributes = kvargs["attributes"]
            else:
                self_.attributes = AppUpdateAttributes(**kvargs["attributes"])
        if "data" in kvargs and kvargs["data"] is not None:
            self_.data = kvargs["data"]
        if "moveApp" in kvargs and kvargs["moveApp"] is not None:
            self_.moveApp = kvargs["moveApp"]
        if "originAppId" in kvargs and kvargs["originAppId"] is not None:
            self_.originAppId = kvargs["originAppId"]
        if "spaceId" in kvargs and kvargs["spaceId"] is not None:
            self_.spaceId = kvargs["spaceId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class RecommendedAnalysis:
    """

    Attributes
    ----------
    analysis: AnalysisDetails
    chartType: Literal["barchart", "combochart", "distributionplot", "kpi", "linechart", "map", "scatterplot", "table"]
      Chart type given to current recommendation
    options: object
      (chart options + hypercube definition)
    relevance: float
      percentage of selected items in the analysis to the overall items passed to the endpoint
    parts: list[RecommendedAnalysisCore]
      part analyses (only for macro analyses)
    """

    analysis: AnalysisDetails = None
    chartType: Literal[
        "barchart",
        "combochart",
        "distributionplot",
        "kpi",
        "linechart",
        "map",
        "scatterplot",
        "table",
    ] = None
    options: object = None
    relevance: float = None
    parts: list[RecommendedAnalysisCore] = None

    def __init__(self_, **kvargs):
        if "analysis" in kvargs and kvargs["analysis"] is not None:
            if (
                type(kvargs["analysis"]).__name__
                == RecommendedAnalysis.__annotations__["analysis"]
            ):
                self_.analysis = kvargs["analysis"]
            else:
                self_.analysis = AnalysisDetails(**kvargs["analysis"])
        if "chartType" in kvargs and kvargs["chartType"] is not None:
            self_.chartType = kvargs["chartType"]
        if "options" in kvargs and kvargs["options"] is not None:
            self_.options = kvargs["options"]
        if "relevance" in kvargs and kvargs["relevance"] is not None:
            self_.relevance = kvargs["relevance"]
        if "parts" in kvargs and kvargs["parts"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == RecommendedAnalysis.__annotations__["parts"]
                for e in kvargs["parts"]
            ):
                self_.parts = kvargs["parts"]
            else:
                self_.parts = [RecommendedAnalysisCore(**e) for e in kvargs["parts"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class RecommendedAnalysisCore:
    """

    Attributes
    ----------
    analysis: AnalysisDetails
    chartType: Literal["barchart", "combochart", "distributionplot", "kpi", "linechart", "map", "scatterplot", "table"]
      Chart type given to current recommendation
    options: object
      (chart options + hypercube definition)
    relevance: float
      percentage of selected items in the analysis to the overall items passed to the endpoint
    """

    analysis: AnalysisDetails = None
    chartType: Literal[
        "barchart",
        "combochart",
        "distributionplot",
        "kpi",
        "linechart",
        "map",
        "scatterplot",
        "table",
    ] = None
    options: object = None
    relevance: float = None

    def __init__(self_, **kvargs):
        if "analysis" in kvargs and kvargs["analysis"] is not None:
            if (
                type(kvargs["analysis"]).__name__
                == RecommendedAnalysisCore.__annotations__["analysis"]
            ):
                self_.analysis = kvargs["analysis"]
            else:
                self_.analysis = AnalysisDetails(**kvargs["analysis"])
        if "chartType" in kvargs and kvargs["chartType"] is not None:
            self_.chartType = kvargs["chartType"]
        if "options" in kvargs and kvargs["options"] is not None:
            self_.options = kvargs["options"]
        if "relevance" in kvargs and kvargs["relevance"] is not None:
            self_.relevance = kvargs["relevance"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class RepublishApp:
    """

    Attributes
    ----------
    attributes: AppUpdateAttributes
    checkOriginAppId: bool
      Validate that source app is same as originally published.
    data: Literal["source", "target"]
      The republished app will have data from source or target app.
      The default is source.


      • source: Publish with source data

      • target: Publish with target data
    targetId: str
      The target ID to be republished.
    """

    attributes: AppUpdateAttributes = None
    checkOriginAppId: bool = True
    data: Literal["source", "target"] = None
    targetId: str = None

    def __init__(self_, **kvargs):
        if "attributes" in kvargs and kvargs["attributes"] is not None:
            if (
                type(kvargs["attributes"]).__name__
                == RepublishApp.__annotations__["attributes"]
            ):
                self_.attributes = kvargs["attributes"]
            else:
                self_.attributes = AppUpdateAttributes(**kvargs["attributes"])
        if "checkOriginAppId" in kvargs and kvargs["checkOriginAppId"] is not None:
            self_.checkOriginAppId = kvargs["checkOriginAppId"]
        if "data" in kvargs and kvargs["data"] is not None:
            self_.data = kvargs["data"]
        if "targetId" in kvargs and kvargs["targetId"] is not None:
            self_.targetId = kvargs["targetId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ScriptLogList:
    """

    Attributes
    ----------
    data: list[ScriptLogMeta]
      Array of scriptLogMeta.
    """

    data: list[ScriptLogMeta] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]" == ScriptLogList.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [ScriptLogMeta(**e) for e in kvargs["data"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ScriptLogMeta:
    """

    Attributes
    ----------
    duration: int
      Duration of reload (ms).
    endTime: str
      Time when reload ended.
    links: Log
    reloadId: str
      Reload identifier.
    success: bool
      True if the reload was successful.
    """

    duration: int = None
    endTime: str = None
    links: Log = None
    reloadId: str = None
    success: bool = None

    def __init__(self_, **kvargs):
        if "duration" in kvargs and kvargs["duration"] is not None:
            self_.duration = kvargs["duration"]
        if "endTime" in kvargs and kvargs["endTime"] is not None:
            self_.endTime = kvargs["endTime"]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == ScriptLogMeta.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = Log(**kvargs["links"])
        if "reloadId" in kvargs and kvargs["reloadId"] is not None:
            self_.reloadId = kvargs["reloadId"]
        if "success" in kvargs and kvargs["success"] is not None:
            self_.success = kvargs["success"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ScriptMeta:
    """

    Attributes
    ----------
    modifiedTime: str
      Script version last modification time.
    modifierId: str
      User last modifying script version.
    scriptId: str
      Script id.
    size: int
      Script size.
    versionMessage: str
      Description of this script version
    """

    modifiedTime: str = None
    modifierId: str = None
    scriptId: str = None
    size: int = None
    versionMessage: str = None

    def __init__(self_, **kvargs):
        if "modifiedTime" in kvargs and kvargs["modifiedTime"] is not None:
            self_.modifiedTime = kvargs["modifiedTime"]
        if "modifierId" in kvargs and kvargs["modifierId"] is not None:
            self_.modifierId = kvargs["modifierId"]
        if "scriptId" in kvargs and kvargs["scriptId"] is not None:
            self_.scriptId = kvargs["scriptId"]
        if "size" in kvargs and kvargs["size"] is not None:
            self_.size = kvargs["size"]
        if "versionMessage" in kvargs and kvargs["versionMessage"] is not None:
            self_.versionMessage = kvargs["versionMessage"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ScriptMetaList:
    """

    Attributes
    ----------
    links: NavigationLinks
    scripts: list[ScriptMeta]
      Script versions metadata.
    """

    links: NavigationLinks = None
    scripts: list[ScriptMeta] = None

    def __init__(self_, **kvargs):
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == ScriptMetaList.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = NavigationLinks(**kvargs["links"])
        if "scripts" in kvargs and kvargs["scripts"] is not None:
            if all(
                f"list[{type(e).__name__}]" == ScriptMetaList.__annotations__["scripts"]
                for e in kvargs["scripts"]
            ):
                self_.scripts = kvargs["scripts"]
            else:
                self_.scripts = [ScriptMeta(**e) for e in kvargs["scripts"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ScriptVersion:
    """

    Attributes
    ----------
    script: str
      Script text.
    versionMessage: str
      Description of this script version
    """

    script: str = None
    versionMessage: str = None

    def __init__(self_, **kvargs):
        if "script" in kvargs and kvargs["script"] is not None:
            self_.script = kvargs["script"]
        if "versionMessage" in kvargs and kvargs["versionMessage"] is not None:
            self_.versionMessage = kvargs["versionMessage"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SymbolFrequency:
    """

    Attributes
    ----------
    Frequency: int
      Frequency of the above symbol in the field
    Symbol: SymbolValue
    """

    Frequency: int = None
    Symbol: SymbolValue = None

    def __init__(self_, **kvargs):
        if "Frequency" in kvargs and kvargs["Frequency"] is not None:
            self_.Frequency = kvargs["Frequency"]
        if "Symbol" in kvargs and kvargs["Symbol"] is not None:
            if (
                type(kvargs["Symbol"]).__name__
                == SymbolFrequency.__annotations__["Symbol"]
            ):
                self_.Symbol = kvargs["Symbol"]
            else:
                self_.Symbol = SymbolValue(**kvargs["Symbol"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SymbolValue:
    """

    Attributes
    ----------
    Number: float
      Numeric value of the symbol. NaN otherwise.
    Text: str
      String value of the symbol. This parameter is optional and present only if Symbol is a string.
    """

    Number: float = None
    Text: str = None

    def __init__(self_, **kvargs):
        if "Number" in kvargs and kvargs["Number"] is not None:
            self_.Number = kvargs["Number"]
        if "Text" in kvargs and kvargs["Text"] is not None:
            self_.Text = kvargs["Text"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableMetadata:
    """

    Attributes
    ----------
    byte_size: int
      Static RAM memory used in bytes.
    comment: str
      Table comment.
    is_loose: bool
      If set to true, the table is loose due to circular connection.
      The default value is false.
    is_semantic: bool
      If set to true, the table is semantic.
      The default value is false.
    is_system: bool
      If set to true, the table is a system table.
      The default value is false.
    name: str
      Name of the table.
    no_of_fields: int
      Number of fields.
    no_of_key_fields: int
      Number of key fields.
    no_of_rows: int
      Number of rows.
    """

    byte_size: int = None
    comment: str = None
    is_loose: bool = None
    is_semantic: bool = None
    is_system: bool = None
    name: str = None
    no_of_fields: int = None
    no_of_key_fields: int = None
    no_of_rows: int = None

    def __init__(self_, **kvargs):
        if "byte_size" in kvargs and kvargs["byte_size"] is not None:
            self_.byte_size = kvargs["byte_size"]
        if "comment" in kvargs and kvargs["comment"] is not None:
            self_.comment = kvargs["comment"]
        if "is_loose" in kvargs and kvargs["is_loose"] is not None:
            self_.is_loose = kvargs["is_loose"]
        if "is_semantic" in kvargs and kvargs["is_semantic"] is not None:
            self_.is_semantic = kvargs["is_semantic"]
        if "is_system" in kvargs and kvargs["is_system"] is not None:
            self_.is_system = kvargs["is_system"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "no_of_fields" in kvargs and kvargs["no_of_fields"] is not None:
            self_.no_of_fields = kvargs["no_of_fields"]
        if "no_of_key_fields" in kvargs and kvargs["no_of_key_fields"] is not None:
            self_.no_of_key_fields = kvargs["no_of_key_fields"]
        if "no_of_rows" in kvargs and kvargs["no_of_rows"] is not None:
            self_.no_of_rows = kvargs["no_of_rows"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableProfilingData:
    """

    Attributes
    ----------
    FieldProfiling: list[FieldInTableProfilingData]
      Field values profiling info
    NoOfRows: int
      Number of rows in the table.
    """

    FieldProfiling: list[FieldInTableProfilingData] = None
    NoOfRows: int = None

    def __init__(self_, **kvargs):
        if "FieldProfiling" in kvargs and kvargs["FieldProfiling"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == TableProfilingData.__annotations__["FieldProfiling"]
                for e in kvargs["FieldProfiling"]
            ):
                self_.FieldProfiling = kvargs["FieldProfiling"]
            else:
                self_.FieldProfiling = [
                    FieldInTableProfilingData(**e) for e in kvargs["FieldProfiling"]
                ]
        if "NoOfRows" in kvargs and kvargs["NoOfRows"] is not None:
            self_.NoOfRows = kvargs["NoOfRows"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UpdateApp:
    """

    Attributes
    ----------
    attributes: AppUpdateAttributes
    """

    attributes: AppUpdateAttributes = None

    def __init__(self_, **kvargs):
        if "attributes" in kvargs and kvargs["attributes"] is not None:
            if (
                type(kvargs["attributes"]).__name__
                == UpdateApp.__annotations__["attributes"]
            ):
                self_.attributes = kvargs["attributes"]
            else:
                self_.attributes = AppUpdateAttributes(**kvargs["attributes"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UpdateOwner:
    """

    Attributes
    ----------
    ownerId: str
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
class UpdateSpace:
    """

    Attributes
    ----------
    spaceId: str
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
class Cmpbool:
    """

    Attributes
    ----------
    absoluteDiff: float
    diff: float
    trend: str
    baseline: bool
    comparison: bool
    """

    absoluteDiff: float = None
    diff: float = None
    trend: str = None
    baseline: bool = None
    comparison: bool = None

    def __init__(self_, **kvargs):
        if "absoluteDiff" in kvargs and kvargs["absoluteDiff"] is not None:
            self_.absoluteDiff = kvargs["absoluteDiff"]
        if "diff" in kvargs and kvargs["diff"] is not None:
            self_.diff = kvargs["diff"]
        if "trend" in kvargs and kvargs["trend"] is not None:
            self_.trend = kvargs["trend"]
        if "baseline" in kvargs and kvargs["baseline"] is not None:
            self_.baseline = kvargs["baseline"]
        if "comparison" in kvargs and kvargs["comparison"] is not None:
            self_.comparison = kvargs["comparison"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Cmpfloat:
    """

    Attributes
    ----------
    absoluteDiff: float
    diff: float
    trend: str
    baseline: float
    comparison: float
    """

    absoluteDiff: float = None
    diff: float = None
    trend: str = None
    baseline: float = None
    comparison: float = None

    def __init__(self_, **kvargs):
        if "absoluteDiff" in kvargs and kvargs["absoluteDiff"] is not None:
            self_.absoluteDiff = kvargs["absoluteDiff"]
        if "diff" in kvargs and kvargs["diff"] is not None:
            self_.diff = kvargs["diff"]
        if "trend" in kvargs and kvargs["trend"] is not None:
            self_.trend = kvargs["trend"]
        if "baseline" in kvargs and kvargs["baseline"] is not None:
            self_.baseline = kvargs["baseline"]
        if "comparison" in kvargs and kvargs["comparison"] is not None:
            self_.comparison = kvargs["comparison"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Cmpint:
    """

    Attributes
    ----------
    absoluteDiff: float
    diff: float
    trend: str
    baseline: float
    comparison: float
    """

    absoluteDiff: float = None
    diff: float = None
    trend: str = None
    baseline: float = None
    comparison: float = None

    def __init__(self_, **kvargs):
        if "absoluteDiff" in kvargs and kvargs["absoluteDiff"] is not None:
            self_.absoluteDiff = kvargs["absoluteDiff"]
        if "diff" in kvargs and kvargs["diff"] is not None:
            self_.diff = kvargs["diff"]
        if "trend" in kvargs and kvargs["trend"] is not None:
            self_.trend = kvargs["trend"]
        if "baseline" in kvargs and kvargs["baseline"] is not None:
            self_.baseline = kvargs["baseline"]
        if "comparison" in kvargs and kvargs["comparison"] is not None:
            self_.comparison = kvargs["comparison"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Comparison:
    """

    Attributes
    ----------
    appOpenTimeSeconds: Cmpfloat
    dataModelSizeMib: Cmpfloat
    documentSizeMib: Cmpfloat
    fileSizeMib: Cmpfloat
    hasSectionAccess: Cmpbool
    maxMemoryMib: Cmpfloat
    objHeavy: Sortedcomparisonoobjheavy
    objNoCache: Sortedcomparisonobjresponsetime
    objSingleThreaded: Sortedcomparisonobjresponsetime
    objSlowCached: Sortedcomparisonobjresponsetime
    objSlowUncached: Sortedcomparisonobjresponsetime
    objectCount: Cmpint
    rowCount: Cmpint
    sheetCount: Cmpint
    sheetsCached: Sortedcomparisonobjresponsetime
    sheetsUncached: Sortedcomparisonobjresponsetime
    topFieldsByBytes: Sortedcomparisonfields
    topTablesByBytes: Sortedcomparisontables
    """

    appOpenTimeSeconds: Cmpfloat = None
    dataModelSizeMib: Cmpfloat = None
    documentSizeMib: Cmpfloat = None
    fileSizeMib: Cmpfloat = None
    hasSectionAccess: Cmpbool = None
    maxMemoryMib: Cmpfloat = None
    objHeavy: Sortedcomparisonoobjheavy = None
    objNoCache: Sortedcomparisonobjresponsetime = None
    objSingleThreaded: Sortedcomparisonobjresponsetime = None
    objSlowCached: Sortedcomparisonobjresponsetime = None
    objSlowUncached: Sortedcomparisonobjresponsetime = None
    objectCount: Cmpint = None
    rowCount: Cmpint = None
    sheetCount: Cmpint = None
    sheetsCached: Sortedcomparisonobjresponsetime = None
    sheetsUncached: Sortedcomparisonobjresponsetime = None
    topFieldsByBytes: Sortedcomparisonfields = None
    topTablesByBytes: Sortedcomparisontables = None

    def __init__(self_, **kvargs):
        if "appOpenTimeSeconds" in kvargs and kvargs["appOpenTimeSeconds"] is not None:
            if (
                type(kvargs["appOpenTimeSeconds"]).__name__
                == Comparison.__annotations__["appOpenTimeSeconds"]
            ):
                self_.appOpenTimeSeconds = kvargs["appOpenTimeSeconds"]
            else:
                self_.appOpenTimeSeconds = Cmpfloat(**kvargs["appOpenTimeSeconds"])
        if "dataModelSizeMib" in kvargs and kvargs["dataModelSizeMib"] is not None:
            if (
                type(kvargs["dataModelSizeMib"]).__name__
                == Comparison.__annotations__["dataModelSizeMib"]
            ):
                self_.dataModelSizeMib = kvargs["dataModelSizeMib"]
            else:
                self_.dataModelSizeMib = Cmpfloat(**kvargs["dataModelSizeMib"])
        if "documentSizeMib" in kvargs and kvargs["documentSizeMib"] is not None:
            if (
                type(kvargs["documentSizeMib"]).__name__
                == Comparison.__annotations__["documentSizeMib"]
            ):
                self_.documentSizeMib = kvargs["documentSizeMib"]
            else:
                self_.documentSizeMib = Cmpfloat(**kvargs["documentSizeMib"])
        if "fileSizeMib" in kvargs and kvargs["fileSizeMib"] is not None:
            if (
                type(kvargs["fileSizeMib"]).__name__
                == Comparison.__annotations__["fileSizeMib"]
            ):
                self_.fileSizeMib = kvargs["fileSizeMib"]
            else:
                self_.fileSizeMib = Cmpfloat(**kvargs["fileSizeMib"])
        if "hasSectionAccess" in kvargs and kvargs["hasSectionAccess"] is not None:
            if (
                type(kvargs["hasSectionAccess"]).__name__
                == Comparison.__annotations__["hasSectionAccess"]
            ):
                self_.hasSectionAccess = kvargs["hasSectionAccess"]
            else:
                self_.hasSectionAccess = Cmpbool(**kvargs["hasSectionAccess"])
        if "maxMemoryMib" in kvargs and kvargs["maxMemoryMib"] is not None:
            if (
                type(kvargs["maxMemoryMib"]).__name__
                == Comparison.__annotations__["maxMemoryMib"]
            ):
                self_.maxMemoryMib = kvargs["maxMemoryMib"]
            else:
                self_.maxMemoryMib = Cmpfloat(**kvargs["maxMemoryMib"])
        if "objHeavy" in kvargs and kvargs["objHeavy"] is not None:
            if (
                type(kvargs["objHeavy"]).__name__
                == Comparison.__annotations__["objHeavy"]
            ):
                self_.objHeavy = kvargs["objHeavy"]
            else:
                self_.objHeavy = Sortedcomparisonoobjheavy(**kvargs["objHeavy"])
        if "objNoCache" in kvargs and kvargs["objNoCache"] is not None:
            if (
                type(kvargs["objNoCache"]).__name__
                == Comparison.__annotations__["objNoCache"]
            ):
                self_.objNoCache = kvargs["objNoCache"]
            else:
                self_.objNoCache = Sortedcomparisonobjresponsetime(
                    **kvargs["objNoCache"]
                )
        if "objSingleThreaded" in kvargs and kvargs["objSingleThreaded"] is not None:
            if (
                type(kvargs["objSingleThreaded"]).__name__
                == Comparison.__annotations__["objSingleThreaded"]
            ):
                self_.objSingleThreaded = kvargs["objSingleThreaded"]
            else:
                self_.objSingleThreaded = Sortedcomparisonobjresponsetime(
                    **kvargs["objSingleThreaded"]
                )
        if "objSlowCached" in kvargs and kvargs["objSlowCached"] is not None:
            if (
                type(kvargs["objSlowCached"]).__name__
                == Comparison.__annotations__["objSlowCached"]
            ):
                self_.objSlowCached = kvargs["objSlowCached"]
            else:
                self_.objSlowCached = Sortedcomparisonobjresponsetime(
                    **kvargs["objSlowCached"]
                )
        if "objSlowUncached" in kvargs and kvargs["objSlowUncached"] is not None:
            if (
                type(kvargs["objSlowUncached"]).__name__
                == Comparison.__annotations__["objSlowUncached"]
            ):
                self_.objSlowUncached = kvargs["objSlowUncached"]
            else:
                self_.objSlowUncached = Sortedcomparisonobjresponsetime(
                    **kvargs["objSlowUncached"]
                )
        if "objectCount" in kvargs and kvargs["objectCount"] is not None:
            if (
                type(kvargs["objectCount"]).__name__
                == Comparison.__annotations__["objectCount"]
            ):
                self_.objectCount = kvargs["objectCount"]
            else:
                self_.objectCount = Cmpint(**kvargs["objectCount"])
        if "rowCount" in kvargs and kvargs["rowCount"] is not None:
            if (
                type(kvargs["rowCount"]).__name__
                == Comparison.__annotations__["rowCount"]
            ):
                self_.rowCount = kvargs["rowCount"]
            else:
                self_.rowCount = Cmpint(**kvargs["rowCount"])
        if "sheetCount" in kvargs and kvargs["sheetCount"] is not None:
            if (
                type(kvargs["sheetCount"]).__name__
                == Comparison.__annotations__["sheetCount"]
            ):
                self_.sheetCount = kvargs["sheetCount"]
            else:
                self_.sheetCount = Cmpint(**kvargs["sheetCount"])
        if "sheetsCached" in kvargs and kvargs["sheetsCached"] is not None:
            if (
                type(kvargs["sheetsCached"]).__name__
                == Comparison.__annotations__["sheetsCached"]
            ):
                self_.sheetsCached = kvargs["sheetsCached"]
            else:
                self_.sheetsCached = Sortedcomparisonobjresponsetime(
                    **kvargs["sheetsCached"]
                )
        if "sheetsUncached" in kvargs and kvargs["sheetsUncached"] is not None:
            if (
                type(kvargs["sheetsUncached"]).__name__
                == Comparison.__annotations__["sheetsUncached"]
            ):
                self_.sheetsUncached = kvargs["sheetsUncached"]
            else:
                self_.sheetsUncached = Sortedcomparisonobjresponsetime(
                    **kvargs["sheetsUncached"]
                )
        if "topFieldsByBytes" in kvargs and kvargs["topFieldsByBytes"] is not None:
            if (
                type(kvargs["topFieldsByBytes"]).__name__
                == Comparison.__annotations__["topFieldsByBytes"]
            ):
                self_.topFieldsByBytes = kvargs["topFieldsByBytes"]
            else:
                self_.topFieldsByBytes = Sortedcomparisonfields(
                    **kvargs["topFieldsByBytes"]
                )
        if "topTablesByBytes" in kvargs and kvargs["topTablesByBytes"] is not None:
            if (
                type(kvargs["topTablesByBytes"]).__name__
                == Comparison.__annotations__["topTablesByBytes"]
            ):
                self_.topTablesByBytes = kvargs["topTablesByBytes"]
            else:
                self_.topTablesByBytes = Sortedcomparisontables(
                    **kvargs["topTablesByBytes"]
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Evaluation:
    """

    Attributes
    ----------
    appId: str
    appItemId: str
    appName: str
    details: EvaluationDetails
    ended: str
    events: list[Event]
    id: str
    metadata: Metadata
    result: Result
    sheetId: str
    sheetTitle: str
    started: str
    status: str
    tenantId: str
    timestamp: str
    version: float
    """

    appId: str = None
    appItemId: str = None
    appName: str = None
    details: EvaluationDetails = None
    ended: str = None
    events: list[Event] = None
    id: str = None
    metadata: Metadata = None
    result: Result = None
    sheetId: str = None
    sheetTitle: str = None
    started: str = None
    status: str = None
    tenantId: str = None
    timestamp: str = None
    version: float = None

    def __init__(self_, **kvargs):
        if "appId" in kvargs and kvargs["appId"] is not None:
            self_.appId = kvargs["appId"]
        if "appItemId" in kvargs and kvargs["appItemId"] is not None:
            self_.appItemId = kvargs["appItemId"]
        if "appName" in kvargs and kvargs["appName"] is not None:
            self_.appName = kvargs["appName"]
        if "details" in kvargs and kvargs["details"] is not None:
            if (
                type(kvargs["details"]).__name__
                == Evaluation.__annotations__["details"]
            ):
                self_.details = kvargs["details"]
            else:
                self_.details = EvaluationDetails(**kvargs["details"])
        if "ended" in kvargs and kvargs["ended"] is not None:
            self_.ended = kvargs["ended"]
        if "events" in kvargs and kvargs["events"] is not None:
            if all(
                f"list[{type(e).__name__}]" == Evaluation.__annotations__["events"]
                for e in kvargs["events"]
            ):
                self_.events = kvargs["events"]
            else:
                self_.events = [Event(**e) for e in kvargs["events"]]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "metadata" in kvargs and kvargs["metadata"] is not None:
            if (
                type(kvargs["metadata"]).__name__
                == Evaluation.__annotations__["metadata"]
            ):
                self_.metadata = kvargs["metadata"]
            else:
                self_.metadata = Metadata(**kvargs["metadata"])
        if "result" in kvargs and kvargs["result"] is not None:
            if type(kvargs["result"]).__name__ == Evaluation.__annotations__["result"]:
                self_.result = kvargs["result"]
            else:
                self_.result = Result(**kvargs["result"])
        if "sheetId" in kvargs and kvargs["sheetId"] is not None:
            self_.sheetId = kvargs["sheetId"]
        if "sheetTitle" in kvargs and kvargs["sheetTitle"] is not None:
            self_.sheetTitle = kvargs["sheetTitle"]
        if "started" in kvargs and kvargs["started"] is not None:
            self_.started = kvargs["started"]
        if "status" in kvargs and kvargs["status"] is not None:
            self_.status = kvargs["status"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            self_.tenantId = kvargs["tenantId"]
        if "timestamp" in kvargs and kvargs["timestamp"] is not None:
            self_.timestamp = kvargs["timestamp"]
        if "version" in kvargs and kvargs["version"] is not None:
            self_.version = kvargs["version"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def download(self) -> Evaluation:
        """
        Download a detailed XML log of a specific evaluation
        Find and download an evaluation log by a specific evaluation id.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/apps/evaluations/{id}/actions/download".replace("{id}", self.id),
            method="GET",
            params={},
            data=None,
        )
        obj = Evaluation(**response.json())
        obj.auth = self.auth
        return obj


@dataclass
class EvaluationDetails:
    """

    Attributes
    ----------
    concurrentReload: bool
    dedicated: bool
    engineHasCache: bool
    errors: list[str]
    objectMetrics: object
    warnings: list[str]
    """

    concurrentReload: bool = None
    dedicated: bool = None
    engineHasCache: bool = None
    errors: list[str] = None
    objectMetrics: object = None
    warnings: list[str] = None

    def __init__(self_, **kvargs):
        if "concurrentReload" in kvargs and kvargs["concurrentReload"] is not None:
            self_.concurrentReload = kvargs["concurrentReload"]
        if "dedicated" in kvargs and kvargs["dedicated"] is not None:
            self_.dedicated = kvargs["dedicated"]
        if "engineHasCache" in kvargs and kvargs["engineHasCache"] is not None:
            self_.engineHasCache = kvargs["engineHasCache"]
        if "errors" in kvargs and kvargs["errors"] is not None:
            self_.errors = kvargs["errors"]
        if "objectMetrics" in kvargs and kvargs["objectMetrics"] is not None:
            self_.objectMetrics = kvargs["objectMetrics"]
        if "warnings" in kvargs and kvargs["warnings"] is not None:
            self_.warnings = kvargs["warnings"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Evaluations:
    """

    Attributes
    ----------
    data: list[Evaluation]
    links: EvaluationsLinks
    """

    data: list[Evaluation] = None
    links: EvaluationsLinks = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]" == Evaluations.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [Evaluation(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == Evaluations.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = EvaluationsLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EvaluationsLinks:
    """

    Attributes
    ----------
    next: EvaluationsLinksNext
    prev: EvaluationsLinksPrev
    """

    next: EvaluationsLinksNext = None
    prev: EvaluationsLinksPrev = None

    def __init__(self_, **kvargs):
        if "next" in kvargs and kvargs["next"] is not None:
            if (
                type(kvargs["next"]).__name__
                == EvaluationsLinks.__annotations__["next"]
            ):
                self_.next = kvargs["next"]
            else:
                self_.next = EvaluationsLinksNext(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if (
                type(kvargs["prev"]).__name__
                == EvaluationsLinks.__annotations__["prev"]
            ):
                self_.prev = kvargs["prev"]
            else:
                self_.prev = EvaluationsLinksPrev(**kvargs["prev"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EvaluationsLinksNext:
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
class EvaluationsLinksPrev:
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
class Event:
    """

    Attributes
    ----------
    details: str
    errorCode: str
    objectId: str
    objectTitle: str
    objectType: str
    objectVisualization: str
    severity: str
    sheetId: str
    sheetTitle: str
    """

    details: str = None
    errorCode: str = None
    objectId: str = None
    objectTitle: str = None
    objectType: str = None
    objectVisualization: str = None
    severity: str = None
    sheetId: str = None
    sheetTitle: str = None

    def __init__(self_, **kvargs):
        if "details" in kvargs and kvargs["details"] is not None:
            self_.details = kvargs["details"]
        if "errorCode" in kvargs and kvargs["errorCode"] is not None:
            self_.errorCode = kvargs["errorCode"]
        if "objectId" in kvargs and kvargs["objectId"] is not None:
            self_.objectId = kvargs["objectId"]
        if "objectTitle" in kvargs and kvargs["objectTitle"] is not None:
            self_.objectTitle = kvargs["objectTitle"]
        if "objectType" in kvargs and kvargs["objectType"] is not None:
            self_.objectType = kvargs["objectType"]
        if (
            "objectVisualization" in kvargs
            and kvargs["objectVisualization"] is not None
        ):
            self_.objectVisualization = kvargs["objectVisualization"]
        if "severity" in kvargs and kvargs["severity"] is not None:
            self_.severity = kvargs["severity"]
        if "sheetId" in kvargs and kvargs["sheetId"] is not None:
            self_.sheetId = kvargs["sheetId"]
        if "sheetTitle" in kvargs and kvargs["sheetTitle"] is not None:
            self_.sheetTitle = kvargs["sheetTitle"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Metadata:
    """

    Attributes
    ----------
    amountofcardinalfieldvalues: float
    amountoffields: float
    amountoffieldvalues: float
    amountofrows: float
    amountoftables: float
    hassectionaccess: bool
    reloadmeta: MetadataReloadmeta
    staticbytesize: float
    """

    amountofcardinalfieldvalues: float = None
    amountoffields: float = None
    amountoffieldvalues: float = None
    amountofrows: float = None
    amountoftables: float = None
    hassectionaccess: bool = None
    reloadmeta: MetadataReloadmeta = None
    staticbytesize: float = None

    def __init__(self_, **kvargs):
        if (
            "amountofcardinalfieldvalues" in kvargs
            and kvargs["amountofcardinalfieldvalues"] is not None
        ):
            self_.amountofcardinalfieldvalues = kvargs["amountofcardinalfieldvalues"]
        if "amountoffields" in kvargs and kvargs["amountoffields"] is not None:
            self_.amountoffields = kvargs["amountoffields"]
        if (
            "amountoffieldvalues" in kvargs
            and kvargs["amountoffieldvalues"] is not None
        ):
            self_.amountoffieldvalues = kvargs["amountoffieldvalues"]
        if "amountofrows" in kvargs and kvargs["amountofrows"] is not None:
            self_.amountofrows = kvargs["amountofrows"]
        if "amountoftables" in kvargs and kvargs["amountoftables"] is not None:
            self_.amountoftables = kvargs["amountoftables"]
        if "hassectionaccess" in kvargs and kvargs["hassectionaccess"] is not None:
            self_.hassectionaccess = kvargs["hassectionaccess"]
        if "reloadmeta" in kvargs and kvargs["reloadmeta"] is not None:
            if (
                type(kvargs["reloadmeta"]).__name__
                == Metadata.__annotations__["reloadmeta"]
            ):
                self_.reloadmeta = kvargs["reloadmeta"]
            else:
                self_.reloadmeta = MetadataReloadmeta(**kvargs["reloadmeta"])
        if "staticbytesize" in kvargs and kvargs["staticbytesize"] is not None:
            self_.staticbytesize = kvargs["staticbytesize"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class MetadataReloadmeta:
    """

    Attributes
    ----------
    cpuspent: float
    peakmemorybytes: float
    """

    cpuspent: float = None
    peakmemorybytes: float = None

    def __init__(self_, **kvargs):
        if "cpuspent" in kvargs and kvargs["cpuspent"] is not None:
            self_.cpuspent = kvargs["cpuspent"]
        if "peakmemorybytes" in kvargs and kvargs["peakmemorybytes"] is not None:
            self_.peakmemorybytes = kvargs["peakmemorybytes"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Objectspec:
    """

    Attributes
    ----------
    id: str
    objectType: float
    sheetId: str
    title: str
    """

    id: str = None
    objectType: float = None
    sheetId: str = None
    title: str = None

    def __init__(self_, **kvargs):
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "objectType" in kvargs and kvargs["objectType"] is not None:
            self_.objectType = kvargs["objectType"]
        if "sheetId" in kvargs and kvargs["sheetId"] is not None:
            self_.sheetId = kvargs["sheetId"]
        if "title" in kvargs and kvargs["title"] is not None:
            self_.title = kvargs["title"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Result:
    """

    Attributes
    ----------
    documentSizeMiB: float
    hasSectionAccess: bool
    objNoCache: list[Resultobjresponsetime]
    objSingleThreaded: list[Resultsingle]
    objSlowCached: list[Resultobjsinglethreaded]
    objSlowUncached: list[Resultobjresponsetime]
    objectCount: float
    rowCount: float
    sheetCount: float
    sheets: list[Resultobjsheet]
    topFieldsByBytes: list[Resultmetadatatopfields]
    topTablesByBytes: list[Resultmetadatatoptables]
    """

    documentSizeMiB: float = None
    hasSectionAccess: bool = None
    objNoCache: list[Resultobjresponsetime] = None
    objSingleThreaded: list[Resultsingle] = None
    objSlowCached: list[Resultobjsinglethreaded] = None
    objSlowUncached: list[Resultobjresponsetime] = None
    objectCount: float = None
    rowCount: float = None
    sheetCount: float = None
    sheets: list[Resultobjsheet] = None
    topFieldsByBytes: list[Resultmetadatatopfields] = None
    topTablesByBytes: list[Resultmetadatatoptables] = None

    def __init__(self_, **kvargs):
        if "documentSizeMiB" in kvargs and kvargs["documentSizeMiB"] is not None:
            self_.documentSizeMiB = kvargs["documentSizeMiB"]
        if "hasSectionAccess" in kvargs and kvargs["hasSectionAccess"] is not None:
            self_.hasSectionAccess = kvargs["hasSectionAccess"]
        if "objNoCache" in kvargs and kvargs["objNoCache"] is not None:
            if all(
                f"list[{type(e).__name__}]" == Result.__annotations__["objNoCache"]
                for e in kvargs["objNoCache"]
            ):
                self_.objNoCache = kvargs["objNoCache"]
            else:
                self_.objNoCache = [
                    Resultobjresponsetime(**e) for e in kvargs["objNoCache"]
                ]
        if "objSingleThreaded" in kvargs and kvargs["objSingleThreaded"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == Result.__annotations__["objSingleThreaded"]
                for e in kvargs["objSingleThreaded"]
            ):
                self_.objSingleThreaded = kvargs["objSingleThreaded"]
            else:
                self_.objSingleThreaded = [
                    Resultsingle(**e) for e in kvargs["objSingleThreaded"]
                ]
        if "objSlowCached" in kvargs and kvargs["objSlowCached"] is not None:
            if all(
                f"list[{type(e).__name__}]" == Result.__annotations__["objSlowCached"]
                for e in kvargs["objSlowCached"]
            ):
                self_.objSlowCached = kvargs["objSlowCached"]
            else:
                self_.objSlowCached = [
                    Resultobjsinglethreaded(**e) for e in kvargs["objSlowCached"]
                ]
        if "objSlowUncached" in kvargs and kvargs["objSlowUncached"] is not None:
            if all(
                f"list[{type(e).__name__}]" == Result.__annotations__["objSlowUncached"]
                for e in kvargs["objSlowUncached"]
            ):
                self_.objSlowUncached = kvargs["objSlowUncached"]
            else:
                self_.objSlowUncached = [
                    Resultobjresponsetime(**e) for e in kvargs["objSlowUncached"]
                ]
        if "objectCount" in kvargs and kvargs["objectCount"] is not None:
            self_.objectCount = kvargs["objectCount"]
        if "rowCount" in kvargs and kvargs["rowCount"] is not None:
            self_.rowCount = kvargs["rowCount"]
        if "sheetCount" in kvargs and kvargs["sheetCount"] is not None:
            self_.sheetCount = kvargs["sheetCount"]
        if "sheets" in kvargs and kvargs["sheets"] is not None:
            if all(
                f"list[{type(e).__name__}]" == Result.__annotations__["sheets"]
                for e in kvargs["sheets"]
            ):
                self_.sheets = kvargs["sheets"]
            else:
                self_.sheets = [Resultobjsheet(**e) for e in kvargs["sheets"]]
        if "topFieldsByBytes" in kvargs and kvargs["topFieldsByBytes"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == Result.__annotations__["topFieldsByBytes"]
                for e in kvargs["topFieldsByBytes"]
            ):
                self_.topFieldsByBytes = kvargs["topFieldsByBytes"]
            else:
                self_.topFieldsByBytes = [
                    Resultmetadatatopfields(**e) for e in kvargs["topFieldsByBytes"]
                ]
        if "topTablesByBytes" in kvargs and kvargs["topTablesByBytes"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == Result.__annotations__["topTablesByBytes"]
                for e in kvargs["topTablesByBytes"]
            ):
                self_.topTablesByBytes = kvargs["topTablesByBytes"]
            else:
                self_.topTablesByBytes = [
                    Resultmetadatatoptables(**e) for e in kvargs["topTablesByBytes"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Resultmetadatatopfields:
    """

    Attributes
    ----------
    byte_size: float
    is_system: bool
    name: str
    """

    byte_size: float = None
    is_system: bool = None
    name: str = None

    def __init__(self_, **kvargs):
        if "byte_size" in kvargs and kvargs["byte_size"] is not None:
            self_.byte_size = kvargs["byte_size"]
        if "is_system" in kvargs and kvargs["is_system"] is not None:
            self_.is_system = kvargs["is_system"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Resultmetadatatoptables:
    """

    Attributes
    ----------
    byte_size: float
    is_system: bool
    name: str
    """

    byte_size: float = None
    is_system: bool = None
    name: str = None

    def __init__(self_, **kvargs):
        if "byte_size" in kvargs and kvargs["byte_size"] is not None:
            self_.byte_size = kvargs["byte_size"]
        if "is_system" in kvargs and kvargs["is_system"] is not None:
            self_.is_system = kvargs["is_system"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Resultobjresponsetime:
    """

    Attributes
    ----------
    id: str
    objectType: float
    sheetId: str
    title: str
    responseTimeSeconds: float
    """

    id: str = None
    objectType: float = None
    sheetId: str = None
    title: str = None
    responseTimeSeconds: float = None

    def __init__(self_, **kvargs):
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "objectType" in kvargs and kvargs["objectType"] is not None:
            self_.objectType = kvargs["objectType"]
        if "sheetId" in kvargs and kvargs["sheetId"] is not None:
            self_.sheetId = kvargs["sheetId"]
        if "title" in kvargs and kvargs["title"] is not None:
            self_.title = kvargs["title"]
        if (
            "responseTimeSeconds" in kvargs
            and kvargs["responseTimeSeconds"] is not None
        ):
            self_.responseTimeSeconds = kvargs["responseTimeSeconds"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Resultobjsheet:
    """

    Attributes
    ----------
    objectCount: float
    sheet: Resultobjresponsetime
    sheetObjects: list[Resultobjresponsetime]
    """

    objectCount: float = None
    sheet: Resultobjresponsetime = None
    sheetObjects: list[Resultobjresponsetime] = None

    def __init__(self_, **kvargs):
        if "objectCount" in kvargs and kvargs["objectCount"] is not None:
            self_.objectCount = kvargs["objectCount"]
        if "sheet" in kvargs and kvargs["sheet"] is not None:
            if (
                type(kvargs["sheet"]).__name__
                == Resultobjsheet.__annotations__["sheet"]
            ):
                self_.sheet = kvargs["sheet"]
            else:
                self_.sheet = Resultobjresponsetime(**kvargs["sheet"])
        if "sheetObjects" in kvargs and kvargs["sheetObjects"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == Resultobjsheet.__annotations__["sheetObjects"]
                for e in kvargs["sheetObjects"]
            ):
                self_.sheetObjects = kvargs["sheetObjects"]
            else:
                self_.sheetObjects = [
                    Resultobjresponsetime(**e) for e in kvargs["sheetObjects"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Resultobjsinglethreaded:
    """

    Attributes
    ----------
    id: str
    objectType: float
    sheetId: str
    title: str
    cpuQuotients: list[float]
    responseTimeSeconds: float
    schema: Objectspec
    """

    id: str = None
    objectType: float = None
    sheetId: str = None
    title: str = None
    cpuQuotients: list[float] = None
    responseTimeSeconds: float = None
    schema: Objectspec = None

    def __init__(self_, **kvargs):
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "objectType" in kvargs and kvargs["objectType"] is not None:
            self_.objectType = kvargs["objectType"]
        if "sheetId" in kvargs and kvargs["sheetId"] is not None:
            self_.sheetId = kvargs["sheetId"]
        if "title" in kvargs and kvargs["title"] is not None:
            self_.title = kvargs["title"]
        if "cpuQuotients" in kvargs and kvargs["cpuQuotients"] is not None:
            self_.cpuQuotients = kvargs["cpuQuotients"]
        if (
            "responseTimeSeconds" in kvargs
            and kvargs["responseTimeSeconds"] is not None
        ):
            self_.responseTimeSeconds = kvargs["responseTimeSeconds"]
        if "schema" in kvargs and kvargs["schema"] is not None:
            if (
                type(kvargs["schema"]).__name__
                == Resultobjsinglethreaded.__annotations__["schema"]
            ):
                self_.schema = kvargs["schema"]
            else:
                self_.schema = Objectspec(**kvargs["schema"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Resultsingle:
    """

    Attributes
    ----------
    id: str
    objectType: float
    sheetId: str
    title: str
    cpuQuotient1: float
    """

    id: str = None
    objectType: float = None
    sheetId: str = None
    title: str = None
    cpuQuotient1: float = None

    def __init__(self_, **kvargs):
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "objectType" in kvargs and kvargs["objectType"] is not None:
            self_.objectType = kvargs["objectType"]
        if "sheetId" in kvargs and kvargs["sheetId"] is not None:
            self_.sheetId = kvargs["sheetId"]
        if "title" in kvargs and kvargs["title"] is not None:
            self_.title = kvargs["title"]
        if "cpuQuotient1" in kvargs and kvargs["cpuQuotient1"] is not None:
            self_.cpuQuotient1 = kvargs["cpuQuotient1"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Sortedcomparisonfields:
    """

    Attributes
    ----------
    absoluteDiffAsc: list[any]
    absoluteDiffDesc: list[any]
    dataSourceStatus: Literal["full", "none", "baselinemissing", "comparisonmissing"]
    list: list[any]
    relativeDiffAsc: list[any]
    relativeDiffDesc: list[any]
    """

    absoluteDiffAsc: list[any] = None
    absoluteDiffDesc: list[any] = None
    dataSourceStatus: Literal[
        "full", "none", "baselinemissing", "comparisonmissing"
    ] = None
    list: list[any] = None
    relativeDiffAsc: list[any] = None
    relativeDiffDesc: list[any] = None

    def __init__(self_, **kvargs):
        if "absoluteDiffAsc" in kvargs and kvargs["absoluteDiffAsc"] is not None:
            self_.absoluteDiffAsc = kvargs["absoluteDiffAsc"]
        if "absoluteDiffDesc" in kvargs and kvargs["absoluteDiffDesc"] is not None:
            self_.absoluteDiffDesc = kvargs["absoluteDiffDesc"]
        if "dataSourceStatus" in kvargs and kvargs["dataSourceStatus"] is not None:
            self_.dataSourceStatus = kvargs["dataSourceStatus"]
        if "list" in kvargs and kvargs["list"] is not None:
            self_.list = kvargs["list"]
        if "relativeDiffAsc" in kvargs and kvargs["relativeDiffAsc"] is not None:
            self_.relativeDiffAsc = kvargs["relativeDiffAsc"]
        if "relativeDiffDesc" in kvargs and kvargs["relativeDiffDesc"] is not None:
            self_.relativeDiffDesc = kvargs["relativeDiffDesc"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Sortedcomparisonobjresponsetime:
    """

    Attributes
    ----------
    absoluteDiffAsc: list[any]
    absoluteDiffDesc: list[any]
    dataSourceStatus: Literal["full", "none", "baselinemissing", "comparisonmissing"]
    list: list[any]
    relativeDiffAsc: list[any]
    relativeDiffDesc: list[any]
    """

    absoluteDiffAsc: list[any] = None
    absoluteDiffDesc: list[any] = None
    dataSourceStatus: Literal[
        "full", "none", "baselinemissing", "comparisonmissing"
    ] = None
    list: list[any] = None
    relativeDiffAsc: list[any] = None
    relativeDiffDesc: list[any] = None

    def __init__(self_, **kvargs):
        if "absoluteDiffAsc" in kvargs and kvargs["absoluteDiffAsc"] is not None:
            self_.absoluteDiffAsc = kvargs["absoluteDiffAsc"]
        if "absoluteDiffDesc" in kvargs and kvargs["absoluteDiffDesc"] is not None:
            self_.absoluteDiffDesc = kvargs["absoluteDiffDesc"]
        if "dataSourceStatus" in kvargs and kvargs["dataSourceStatus"] is not None:
            self_.dataSourceStatus = kvargs["dataSourceStatus"]
        if "list" in kvargs and kvargs["list"] is not None:
            self_.list = kvargs["list"]
        if "relativeDiffAsc" in kvargs and kvargs["relativeDiffAsc"] is not None:
            self_.relativeDiffAsc = kvargs["relativeDiffAsc"]
        if "relativeDiffDesc" in kvargs and kvargs["relativeDiffDesc"] is not None:
            self_.relativeDiffDesc = kvargs["relativeDiffDesc"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Sortedcomparisonoobjheavy:
    """

    Attributes
    ----------
    absoluteDiffAsc: list[any]
    absoluteDiffDesc: list[any]
    dataSourceStatus: Literal["full", "none", "baselinemissing", "comparisonmissing"]
    list: list[any]
    relativeDiffAsc: list[any]
    relativeDiffDesc: list[any]
    """

    absoluteDiffAsc: list[any] = None
    absoluteDiffDesc: list[any] = None
    dataSourceStatus: Literal[
        "full", "none", "baselinemissing", "comparisonmissing"
    ] = None
    list: list[any] = None
    relativeDiffAsc: list[any] = None
    relativeDiffDesc: list[any] = None

    def __init__(self_, **kvargs):
        if "absoluteDiffAsc" in kvargs and kvargs["absoluteDiffAsc"] is not None:
            self_.absoluteDiffAsc = kvargs["absoluteDiffAsc"]
        if "absoluteDiffDesc" in kvargs and kvargs["absoluteDiffDesc"] is not None:
            self_.absoluteDiffDesc = kvargs["absoluteDiffDesc"]
        if "dataSourceStatus" in kvargs and kvargs["dataSourceStatus"] is not None:
            self_.dataSourceStatus = kvargs["dataSourceStatus"]
        if "list" in kvargs and kvargs["list"] is not None:
            self_.list = kvargs["list"]
        if "relativeDiffAsc" in kvargs and kvargs["relativeDiffAsc"] is not None:
            self_.relativeDiffAsc = kvargs["relativeDiffAsc"]
        if "relativeDiffDesc" in kvargs and kvargs["relativeDiffDesc"] is not None:
            self_.relativeDiffDesc = kvargs["relativeDiffDesc"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Sortedcomparisontables:
    """

    Attributes
    ----------
    absoluteDiffAsc: list[any]
    absoluteDiffDesc: list[any]
    dataSourceStatus: Literal["full", "none", "baselinemissing", "comparisonmissing"]
    list: list[any]
    relativeDiffAsc: list[any]
    relativeDiffDesc: list[any]
    """

    absoluteDiffAsc: list[any] = None
    absoluteDiffDesc: list[any] = None
    dataSourceStatus: Literal[
        "full", "none", "baselinemissing", "comparisonmissing"
    ] = None
    list: list[any] = None
    relativeDiffAsc: list[any] = None
    relativeDiffDesc: list[any] = None

    def __init__(self_, **kvargs):
        if "absoluteDiffAsc" in kvargs and kvargs["absoluteDiffAsc"] is not None:
            self_.absoluteDiffAsc = kvargs["absoluteDiffAsc"]
        if "absoluteDiffDesc" in kvargs and kvargs["absoluteDiffDesc"] is not None:
            self_.absoluteDiffDesc = kvargs["absoluteDiffDesc"]
        if "dataSourceStatus" in kvargs and kvargs["dataSourceStatus"] is not None:
            self_.dataSourceStatus = kvargs["dataSourceStatus"]
        if "list" in kvargs and kvargs["list"] is not None:
            self_.list = kvargs["list"]
        if "relativeDiffAsc" in kvargs and kvargs["relativeDiffAsc"] is not None:
            self_.relativeDiffAsc = kvargs["relativeDiffAsc"]
        if "relativeDiffDesc" in kvargs and kvargs["relativeDiffDesc"] is not None:
            self_.relativeDiffDesc = kvargs["relativeDiffDesc"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Apps:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def download_apps_evaluations_compare(
        self, baseid: str, comparisonid: str
    ) -> Comparison:
        """
        Download a comparison log of two evaluations
        Accepts two evaluation ids and downloads a log, in XML format, denoting the differences between the two.

        Parameters
        ----------
        baseid: str
          Id of the baseline evaluation
        comparisonid: str
          Id of the comparison evaluation
        """
        response = self.auth.rest(
            path="/apps/evaluations/{baseid}/actions/compare/{comparisonid}/actions/download".replace(
                "{baseid}", baseid
            ).replace(
                "{comparisonid}", comparisonid
            ),
            method="GET",
            params={},
            data=None,
        )
        obj = Comparison(**response.json())
        obj.auth = self.auth
        return obj

    def compare_apps_evaluations(
        self, baseid: str, comparisonid: str, all: bool = None, format: str = None
    ) -> Comparison:
        """
        Compare two evaluations
        Accepts two evaluation ids and returns a comparison denoting the differences between the two.

        Parameters
        ----------
        baseid: str
          Id of the baseline evaluation
        comparisonid: str
          Id of the comparison evaluation
        all: bool = None
          Get the full list of comparisons including non-significant diffs
        format: str = None
          Specify output format, currently supported are 'json' and 'xml'
        """
        query_params = {}
        if all is not None:
            query_params["all"] = all
        if format is not None:
            query_params["format"] = format
        response = self.auth.rest(
            path="/apps/evaluations/{baseid}/actions/compare/{comparisonid}".replace(
                "{baseid}", baseid
            ).replace("{comparisonid}", comparisonid),
            method="GET",
            params=query_params,
            data=None,
        )
        obj = Comparison(**response.json())
        obj.auth = self.auth
        return obj

    def get_evaluation(
        self, id: str, all: bool = None, format: str = None
    ) -> Evaluation:
        """
        Retrieve a specific evaluation
        Find an evaluation by a specific id.

        Parameters
        ----------
        id: str
          Id of the desired evaluation.
        all: bool = None
          Get the full data of the evaluation
        format: str = None
          Specify output format, currently supported are 'json' and 'xml'
        """
        query_params = {}
        if all is not None:
            query_params["all"] = all
        if format is not None:
            query_params["format"] = format
        response = self.auth.rest(
            path="/apps/evaluations/{id}".replace("{id}", id),
            method="GET",
            params=query_params,
            data=None,
        )
        obj = Evaluation(**response.json())
        obj.auth = self.auth
        return obj

    def import_app(
        self,
        data: io.BufferedReader = None,
        appId: str = None,
        fallbackName: str = None,
        fileId: str = None,
        mode: str = None,
        name: str = None,
        NoData: bool = None,
        spaceId: str = None,
    ) -> NxApp:
        """
        Imports an app into the system.

        Parameters
        ----------
        appId: str = None
          The app ID of the target app when source is qvw file.
        fallbackName: str = None
          The name of the target app when source does not have a specified name, applicable if source is qvw file.
        fileId: str = None
          The file ID to be downloaded from Temporary Content Service (TCS) and used during import.
        mode: str = None
          The import mode. In `new` mode (default), the source app will be imported as a new app.The `autoreplace` mode is an internal mode only and is not permitted for external use.

          One of:

          • NEW

          • AUTOREPLACE
        name: str = None
          The name of the target app.
        NoData: bool = None
          If NoData is true, the data of the existing app will be kept as is, otherwise it will be replaced by the new incoming data.
        spaceId: str = None
          The space ID of the target app.
        data: object = None
          Path of the source app.
        """
        query_params = {}
        if appId is not None:
            query_params["appId"] = appId
        if fallbackName is not None:
            query_params["fallbackName"] = fallbackName
        if fileId is not None:
            query_params["fileId"] = fileId
        if mode is not None:
            query_params["mode"] = mode
        if name is not None:
            query_params["name"] = name
        if NoData is not None:
            query_params["NoData"] = NoData
        if spaceId is not None:
            query_params["spaceId"] = spaceId
        response = self.auth.rest(
            path="/apps/import",
            method="POST",
            params=query_params,
            data=data,
            headers={"Content-Type": "application/octet-stream"},
        )
        obj = NxApp(**response.json())
        obj.auth = self.auth
        return obj

    def get_privileges(self) -> list[str]:
        """
        Gets the app privileges for the current user, such as create app and import app. Empty means that the current user has no app privileges.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/apps/privileges",
            method="GET",
            params={},
            data=None,
        )
        return response.json()

    def get(self, appId: str) -> NxApp:
        """
        Retrieves information for a specific app.

        Parameters
        ----------
        appId: str
          Identifier of the app.
        """
        response = self.auth.rest(
            path="/apps/{appId}".replace("{appId}", appId),
            method="GET",
            params={},
            data=None,
        )
        obj = NxApp(**response.json())
        obj.auth = self.auth
        return obj

    def get_evaluations(
        self,
        guid: str,
        all: bool = None,
        fileMode: bool = None,
        format: str = None,
        limit: int = 20,
        next: str = None,
        prev: str = None,
        sort: str = None,
    ) -> ListableResource[Evaluation]:
        """
        Retrieve a list of all historic evaluations for an app GUID
        Find all evaluations for an app GUID.
        Supports paging via next, prev which are sent in the response body

        Parameters
        ----------
        guid: str
          The app guid.
        all: bool = None
          Get the full data of the evaluation
        fileMode: bool = None
          Add file transfer headers to response
        format: str = None
          Specify output format, currently supported are 'json' and 'xml'
        limit: int = 20
          Number of results to return per page.
        next: str = None
          The app evaluation id to get next page from
        prev: str = None
          The app evaluation id to get previous page from
        sort: str = None
          Property to sort list on
        """
        query_params = {}
        if all is not None:
            query_params["all"] = all
        if fileMode is not None:
            query_params["fileMode"] = fileMode
        if format is not None:
            query_params["format"] = format
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if sort is not None:
            query_params["sort"] = sort
        response = self.auth.rest(
            path="/apps/{guid}/evaluations".replace("{guid}", guid),
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Evaluation,
            auth=self.auth,
            path="/apps/{guid}/evaluations",
            query_params=query_params,
        )

    def create_evaluation(self, guid: str) -> Evaluation:
        """
        Queue an app evaluation
        Queue an app evaluation by its app guid.

        Parameters
        ----------
        guid: str
          Guid of the app.
        """
        response = self.auth.rest(
            path="/apps/{guid}/evaluations".replace("{guid}", guid),
            method="POST",
            params={},
            data=None,
        )
        obj = Evaluation(**response.json())
        obj.auth = self.auth
        return obj

    def create(self, data: CreateApp) -> NxApp:
        """
        Creates a new app.

        Parameters
        ----------
        data: CreateApp
          Attributes that the user wants to set in new app.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/apps",
            method="POST",
            params={},
            data=data,
        )
        obj = NxApp(**response.json())
        obj.auth = self.auth
        return obj

    def create_session_app(self, session_app_id: str) -> NxApp:
        """
        creates an empty session app

        Parameters
        ----------
        session_app_id: string the a self generated "app_id" prefixed with SessionApp_

        Examples
        ----------
        >>> session_app_id = "SessionApp_" + str(uuid.uuid2())
        ... session_app = apps.create_session_app(session_app_id)
        ... with session_app.open():
        ...     script = "Load RecNo() as N autogenerate(200);"
        ...     session_app.set_script(script)
        ...     session_app.do_reload()
        """
        obj = NxApp(attributes={"id": session_app_id})
        obj.auth = self.auth
        return obj
