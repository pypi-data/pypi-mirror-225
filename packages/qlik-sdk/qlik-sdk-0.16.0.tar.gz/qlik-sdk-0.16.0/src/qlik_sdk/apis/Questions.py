# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class AppMetadata:
    """
    Metadata for app

    Attributes
    ----------
    id: str
    last_reload_date: str
    limited_access: bool
    name: str
    space_id: str
    space_name: str
    space_type: str
    """

    id: str = None
    last_reload_date: str = None
    limited_access: bool = None
    name: str = None
    space_id: str = None
    space_name: str = None
    space_type: str = None

    def __init__(self_, **kvargs):
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "last_reload_date" in kvargs and kvargs["last_reload_date"] is not None:
            self_.last_reload_date = kvargs["last_reload_date"]
        if "limited_access" in kvargs and kvargs["limited_access"] is not None:
            self_.limited_access = kvargs["limited_access"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "space_id" in kvargs and kvargs["space_id"] is not None:
            self_.space_id = kvargs["space_id"]
        if "space_name" in kvargs and kvargs["space_name"] is not None:
            self_.space_name = kvargs["space_name"]
        if "space_type" in kvargs and kvargs["space_type"] is not None:
            self_.space_type = kvargs["space_type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ConversationalResponsePart:
    """

    Attributes
    ----------
    errorMessage: str
    followupSentence: str
    imageUrl: str
    infoType: str
    infoValues: list[any]
    narrative: NarrativeResponse
    renderVisualization: RenderVisualization
    sentence: ConversationalResponsePartSentence
    type: str
    """

    errorMessage: str = None
    followupSentence: str = None
    imageUrl: str = None
    infoType: str = None
    infoValues: list[any] = None
    narrative: NarrativeResponse = None
    renderVisualization: RenderVisualization = None
    sentence: ConversationalResponsePartSentence = None
    type: str = None

    def __init__(self_, **kvargs):
        if "errorMessage" in kvargs and kvargs["errorMessage"] is not None:
            self_.errorMessage = kvargs["errorMessage"]
        if "followupSentence" in kvargs and kvargs["followupSentence"] is not None:
            self_.followupSentence = kvargs["followupSentence"]
        if "imageUrl" in kvargs and kvargs["imageUrl"] is not None:
            self_.imageUrl = kvargs["imageUrl"]
        if "infoType" in kvargs and kvargs["infoType"] is not None:
            self_.infoType = kvargs["infoType"]
        if "infoValues" in kvargs and kvargs["infoValues"] is not None:
            self_.infoValues = kvargs["infoValues"]
        if "narrative" in kvargs and kvargs["narrative"] is not None:
            if (
                type(kvargs["narrative"]).__name__
                == ConversationalResponsePart.__annotations__["narrative"]
            ):
                self_.narrative = kvargs["narrative"]
            else:
                self_.narrative = NarrativeResponse(**kvargs["narrative"])
        if (
            "renderVisualization" in kvargs
            and kvargs["renderVisualization"] is not None
        ):
            if (
                type(kvargs["renderVisualization"]).__name__
                == ConversationalResponsePart.__annotations__["renderVisualization"]
            ):
                self_.renderVisualization = kvargs["renderVisualization"]
            else:
                self_.renderVisualization = RenderVisualization(
                    **kvargs["renderVisualization"]
                )
        if "sentence" in kvargs and kvargs["sentence"] is not None:
            if (
                type(kvargs["sentence"]).__name__
                == ConversationalResponsePart.__annotations__["sentence"]
            ):
                self_.sentence = kvargs["sentence"]
            else:
                self_.sentence = ConversationalResponsePartSentence(
                    **kvargs["sentence"]
                )
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ConversationalResponsePartSentence:
    """

    Attributes
    ----------
    text: str
    """

    text: str = None

    def __init__(self_, **kvargs):
        if "text" in kvargs and kvargs["text"] is not None:
            self_.text = kvargs["text"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Error:
    """
    An error object.

    Attributes
    ----------
    code: str
      The error code.
    detail: str
      A human-readable explanation specific to this occurrence of the problem.
    meta: object
      Additional properties relating to the error.
    source: ErrorSource
      References to the source of the error.
    title: str
      Summary of the problem.
    """

    code: str = None
    detail: str = None
    meta: object = None
    source: ErrorSource = None
    title: str = None

    def __init__(self_, **kvargs):
        if "code" in kvargs and kvargs["code"] is not None:
            self_.code = kvargs["code"]
        if "detail" in kvargs and kvargs["detail"] is not None:
            self_.detail = kvargs["detail"]
        if "meta" in kvargs and kvargs["meta"] is not None:
            self_.meta = kvargs["meta"]
        if "source" in kvargs and kvargs["source"] is not None:
            if type(kvargs["source"]).__name__ == Error.__annotations__["source"]:
                self_.source = kvargs["source"]
            else:
                self_.source = ErrorSource(**kvargs["source"])
        if "title" in kvargs and kvargs["title"] is not None:
            self_.title = kvargs["title"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ErrorSource:
    """
    References to the source of the error.

    Attributes
    ----------
    parameter: str
      The URI query parameter that caused the error.
    pointer: str
      A JSON Pointer to the property that caused the error.
    """

    parameter: str = None
    pointer: str = None

    def __init__(self_, **kvargs):
        if "parameter" in kvargs and kvargs["parameter"] is not None:
            self_.parameter = kvargs["parameter"]
        if "pointer" in kvargs and kvargs["pointer"] is not None:
            self_.pointer = kvargs["pointer"]
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
class NLMetricRecommendation:
    """
    Visualisation recommendation specs for the query

    Attributes
    ----------
    analysis: Literal["breakdown", "changePoint", "comparison", "contribution", "correlation", "fact", "mutualInfo", "rank", "spike", "trend", "values"]
    analysisGroup: Literal["anomaly", "brekadown", "comparison", "correl", "fact", "list", "mutualInfo", "rank"]
    chartType: Literal["barchart", "combochart", "distributionplot", "kpi", "linechart", "map", "scatterplot", "table"]
      Chart type given to current recommendation
    dims: list[str]
      Dimension(s) considered for recommendation
    msrs: list[str]
      Measure(s) considered for recommendation
    relevance: float
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
    dims: list[str] = None
    msrs: list[str] = None
    relevance: float = None

    def __init__(self_, **kvargs):
        if "analysis" in kvargs and kvargs["analysis"] is not None:
            self_.analysis = kvargs["analysis"]
        if "analysisGroup" in kvargs and kvargs["analysisGroup"] is not None:
            self_.analysisGroup = kvargs["analysisGroup"]
        if "chartType" in kvargs and kvargs["chartType"] is not None:
            self_.chartType = kvargs["chartType"]
        if "dims" in kvargs and kvargs["dims"] is not None:
            self_.dims = kvargs["dims"]
        if "msrs" in kvargs and kvargs["msrs"] is not None:
            self_.msrs = kvargs["msrs"]
        if "relevance" in kvargs and kvargs["relevance"] is not None:
            self_.relevance = kvargs["relevance"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NLMetricRecord:
    """

    Attributes
    ----------
    appId: str
      Qlik sense app id that is being used to answer the question
    appName: str
      Qlik sense app name that is being used to answer the question
    apps: list[AppMetadata]
    channelId: str
      Source from which conversation is happening
    chartType: str
      Chart type for given query. For insight advisor it would be 'native' and for insight advisor chat, it could be 'static' or 'responsive'
    createdAt: str
      Record created date
    createdBy: str
      Qlik sense user id who is interacting with insight advisor or insight advisor chat or third party api
    feedback: list[RecFeedback]
    id: str
      Unique record id stored in database
    isContextualQuery: bool
      Boolean value indicates whether given query is contextual or not. It would be false for insight advisor
    lang: str
      language selected for query from insight advisor or insight advisor chat or third party api
    nluInfo: list[PartialNluInfo]
    queryError: bool
    queryOrigin: Literal["askQuestion", "iaAnalysis", "iaAssetsPanel"]
      Refers to source from where narrative request is called
    queryText: str
      Query asked by user in insight advisor or insight advisor or third party api
    queryType: Literal["appList", "appSuggested", "dimensionList", "exploreThisFurther", "followup", "greetings", "measureList", "query", "sampleQuestion"]
      Nature of query being asked during the conversation e.g. query, applist, measurelist, dimensionlist
    questionId: str
      Unique id assigned to user query
    recommendations: list[NLMetricRecommendation]
    responses: NLResponses
      Provides info what was included in response for given query
    stopWords: list[str]
      Tokens from question parsed which are ignored
    tenantId: str
      Qlik sense tenant Id
    unmatchedEntities: list[str]
      Tokens parsed as entities but not matched with app's field/dimension/measure
    updatedAt: str
      Record modified date
    version: str
      Version of the metric model
    """

    appId: str = None
    appName: str = None
    apps: list[AppMetadata] = None
    channelId: str = None
    chartType: str = None
    createdAt: str = None
    createdBy: str = None
    feedback: list[RecFeedback] = None
    id: str = None
    isContextualQuery: bool = None
    lang: str = None
    nluInfo: list[PartialNluInfo] = None
    queryError: bool = None
    queryOrigin: Literal["askQuestion", "iaAnalysis", "iaAssetsPanel"] = "askQuestion"
    queryText: str = None
    queryType: Literal[
        "appList",
        "appSuggested",
        "dimensionList",
        "exploreThisFurther",
        "followup",
        "greetings",
        "measureList",
        "query",
        "sampleQuestion",
    ] = None
    questionId: str = None
    recommendations: list[NLMetricRecommendation] = None
    responses: NLResponses = None
    stopWords: list[str] = None
    tenantId: str = None
    unmatchedEntities: list[str] = None
    updatedAt: str = None
    version: str = None

    def __init__(self_, **kvargs):
        if "appId" in kvargs and kvargs["appId"] is not None:
            self_.appId = kvargs["appId"]
        if "appName" in kvargs and kvargs["appName"] is not None:
            self_.appName = kvargs["appName"]
        if "apps" in kvargs and kvargs["apps"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NLMetricRecord.__annotations__["apps"]
                for e in kvargs["apps"]
            ):
                self_.apps = kvargs["apps"]
            else:
                self_.apps = [AppMetadata(**e) for e in kvargs["apps"]]
        if "channelId" in kvargs and kvargs["channelId"] is not None:
            self_.channelId = kvargs["channelId"]
        if "chartType" in kvargs and kvargs["chartType"] is not None:
            self_.chartType = kvargs["chartType"]
        if "createdAt" in kvargs and kvargs["createdAt"] is not None:
            self_.createdAt = kvargs["createdAt"]
        if "createdBy" in kvargs and kvargs["createdBy"] is not None:
            self_.createdBy = kvargs["createdBy"]
        if "feedback" in kvargs and kvargs["feedback"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NLMetricRecord.__annotations__["feedback"]
                for e in kvargs["feedback"]
            ):
                self_.feedback = kvargs["feedback"]
            else:
                self_.feedback = [RecFeedback(**e) for e in kvargs["feedback"]]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "isContextualQuery" in kvargs and kvargs["isContextualQuery"] is not None:
            self_.isContextualQuery = kvargs["isContextualQuery"]
        if "lang" in kvargs and kvargs["lang"] is not None:
            self_.lang = kvargs["lang"]
        if "nluInfo" in kvargs and kvargs["nluInfo"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NLMetricRecord.__annotations__["nluInfo"]
                for e in kvargs["nluInfo"]
            ):
                self_.nluInfo = kvargs["nluInfo"]
            else:
                self_.nluInfo = [PartialNluInfo(**e) for e in kvargs["nluInfo"]]
        if "queryError" in kvargs and kvargs["queryError"] is not None:
            self_.queryError = kvargs["queryError"]
        if "queryOrigin" in kvargs and kvargs["queryOrigin"] is not None:
            self_.queryOrigin = kvargs["queryOrigin"]
        if "queryText" in kvargs and kvargs["queryText"] is not None:
            self_.queryText = kvargs["queryText"]
        if "queryType" in kvargs and kvargs["queryType"] is not None:
            self_.queryType = kvargs["queryType"]
        if "questionId" in kvargs and kvargs["questionId"] is not None:
            self_.questionId = kvargs["questionId"]
        if "recommendations" in kvargs and kvargs["recommendations"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NLMetricRecord.__annotations__["recommendations"]
                for e in kvargs["recommendations"]
            ):
                self_.recommendations = kvargs["recommendations"]
            else:
                self_.recommendations = [
                    NLMetricRecommendation(**e) for e in kvargs["recommendations"]
                ]
        if "responses" in kvargs and kvargs["responses"] is not None:
            if (
                type(kvargs["responses"]).__name__
                == NLMetricRecord.__annotations__["responses"]
            ):
                self_.responses = kvargs["responses"]
            else:
                self_.responses = NLResponses(**kvargs["responses"])
        if "stopWords" in kvargs and kvargs["stopWords"] is not None:
            self_.stopWords = kvargs["stopWords"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            self_.tenantId = kvargs["tenantId"]
        if "unmatchedEntities" in kvargs and kvargs["unmatchedEntities"] is not None:
            self_.unmatchedEntities = kvargs["unmatchedEntities"]
        if "updatedAt" in kvargs and kvargs["updatedAt"] is not None:
            self_.updatedAt = kvargs["updatedAt"]
        if "version" in kvargs and kvargs["version"] is not None:
            self_.version = kvargs["version"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NLMetricsRequest:
    """

    Attributes
    ----------
    filter: str
      The advanced filtering to use for the query. Refer to RFC 7644 https://www.rfc-editor.org/rfc/rfc7644section-3.4.2.2 for the syntax.:

      Filter on createdAt and updatedAt fields are encouraged and support `eq`, `ne`, `gt`, `ge`, `lt`, `le` comparison operators along with `and` and `or` logical operators.

      Filter on tenantId field is not supported.

      `co`, `sw` and `ew` operators are not supported.

      Examples:
      ```
      appId eq "appId1"
      ```
      ```
      (appId eq "appId1" or appId eq "appId2")
      ```
      ```
      (appId eq "appId1" or appId eq "appId2") and (createdAt gt "2022-08-03T00:00:00.000Z" and createdAt lt "2022-08-04T00:00:00.000Z")
      ```

      ```
      (appId eq "appId1") and (createdAt ge "2022-08-03T00:00:00.000Z")
      ```

      ```
      (appId eq "appId1") and (createdAt le "2022-08-23:59:59.000Z")
      ```

      ```
      (appId eq "appId1") and (questionId eq "12345")
      ```

    """

    filter: str = None

    def __init__(self_, **kvargs):
        if "filter" in kvargs and kvargs["filter"] is not None:
            self_.filter = kvargs["filter"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NLMetricsResponse:
    """

    Attributes
    ----------
    data: list[NLMetricRecord]
    links: Links
    meta: NLMetricsResponseMeta
    """

    data: list[NLMetricRecord] = None
    links: Links = None
    meta: NLMetricsResponseMeta = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NLMetricsResponse.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [NLMetricRecord(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == NLMetricsResponse.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = Links(**kvargs["links"])
        if "meta" in kvargs and kvargs["meta"] is not None:
            if (
                type(kvargs["meta"]).__name__
                == NLMetricsResponse.__annotations__["meta"]
            ):
                self_.meta = kvargs["meta"]
            else:
                self_.meta = NLMetricsResponseMeta(**kvargs["meta"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NLMetricsResponseMeta:
    """

    Attributes
    ----------
    total: int
      The total number of metrics matching the current filter.
    """

    total: int = None

    def __init__(self_, **kvargs):
        if "total" in kvargs and kvargs["total"] is not None:
            self_.total = kvargs["total"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NLResponses:
    """
    Provides info what was included in response for given query

    Attributes
    ----------
    hasChart: bool
      Chart was provided
    hasInsights: bool
      Narrative was provided
    hasMetadataApps: bool
      App list was provided
    hasMetadataDimensions: bool
      Dimensions list was provided
    hasMetadataMeasures: bool
      Measures list was provided
    hasSampleQueries: bool
      Sample questions was provided
    hasSuggestions: bool
      Suggestion questions was provided
    """

    hasChart: bool = None
    hasInsights: bool = None
    hasMetadataApps: bool = None
    hasMetadataDimensions: bool = None
    hasMetadataMeasures: bool = None
    hasSampleQueries: bool = None
    hasSuggestions: bool = None

    def __init__(self_, **kvargs):
        if "hasChart" in kvargs and kvargs["hasChart"] is not None:
            self_.hasChart = kvargs["hasChart"]
        if "hasInsights" in kvargs and kvargs["hasInsights"] is not None:
            self_.hasInsights = kvargs["hasInsights"]
        if "hasMetadataApps" in kvargs and kvargs["hasMetadataApps"] is not None:
            self_.hasMetadataApps = kvargs["hasMetadataApps"]
        if (
            "hasMetadataDimensions" in kvargs
            and kvargs["hasMetadataDimensions"] is not None
        ):
            self_.hasMetadataDimensions = kvargs["hasMetadataDimensions"]
        if (
            "hasMetadataMeasures" in kvargs
            and kvargs["hasMetadataMeasures"] is not None
        ):
            self_.hasMetadataMeasures = kvargs["hasMetadataMeasures"]
        if "hasSampleQueries" in kvargs and kvargs["hasSampleQueries"] is not None:
            self_.hasSampleQueries = kvargs["hasSampleQueries"]
        if "hasSuggestions" in kvargs and kvargs["hasSuggestions"] is not None:
            self_.hasSuggestions = kvargs["hasSuggestions"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NarrativeResponse:
    """

    Attributes
    ----------
    text: str
    """

    text: str = None

    def __init__(self_, **kvargs):
        if "text" in kvargs and kvargs["text"] is not None:
            self_.text = kvargs["text"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NluInfo:
    """

    Attributes
    ----------
    elements: list[NluInfoElements]
    """

    elements: list[NluInfoElements] = None

    def __init__(self_, **kvargs):
        if "elements" in kvargs and kvargs["elements"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NluInfo.__annotations__["elements"]
                for e in kvargs["elements"]
            ):
                self_.elements = kvargs["elements"]
            else:
                self_.elements = [NluInfoElements(**e) for e in kvargs["elements"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NluInfoElements:
    """

    Attributes
    ----------
    entity: bool
    errorText: str
    filterFieldName: str
    filterText: str
    isFilter: bool
    text: str
    type: str
    typeName: str
    typeTranslated: str
    """

    entity: bool = None
    errorText: str = None
    filterFieldName: str = None
    filterText: str = None
    isFilter: bool = None
    text: str = None
    type: str = None
    typeName: str = None
    typeTranslated: str = None

    def __init__(self_, **kvargs):
        if "entity" in kvargs and kvargs["entity"] is not None:
            self_.entity = kvargs["entity"]
        if "errorText" in kvargs and kvargs["errorText"] is not None:
            self_.errorText = kvargs["errorText"]
        if "filterFieldName" in kvargs and kvargs["filterFieldName"] is not None:
            self_.filterFieldName = kvargs["filterFieldName"]
        if "filterText" in kvargs and kvargs["filterText"] is not None:
            self_.filterText = kvargs["filterText"]
        if "isFilter" in kvargs and kvargs["isFilter"] is not None:
            self_.isFilter = kvargs["isFilter"]
        if "text" in kvargs and kvargs["text"] is not None:
            self_.text = kvargs["text"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        if "typeName" in kvargs and kvargs["typeName"] is not None:
            self_.typeName = kvargs["typeName"]
        if "typeTranslated" in kvargs and kvargs["typeTranslated"] is not None:
            self_.typeTranslated = kvargs["typeTranslated"]
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
class QlikApp:
    """

    Attributes
    ----------
    id: str
    name: str
    """

    id: str = None
    name: str = None

    def __init__(self_, **kvargs):
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class QueryCreate:
    """

    Attributes
    ----------
    app: QlikApp
    clearEntityContext: bool
      Flag that clears the entity context.
    disableConversationContext: bool
      Flag that specifies either to enable converastion context.
    disableFollowups: bool
      The flag specifies whether to disable follow-up recommendations.
    disableNarrative: bool
      Flag that specifies whether the narratives should be generated for the user query or not.
    enableVisualizations: bool
      Flag that specifies whether visualization object should be provided or not.
    lang: str
      The language to assume when parsing, specified as an ISO-639-1 code.
      Defaults to 'en' (English).

    recommendationId: str
      property that contains the Id of the recommendation for which the response should be generated.
    text: str
      The sentence that will be parsed.
    visualizationTypes: list[str]
      Specify visualizationTypes for only which visualization object should be provided if enableVisualizations is set to true. For eg. ['linechart', 'barchart']
    """

    app: QlikApp = None
    clearEntityContext: bool = None
    disableConversationContext: bool = None
    disableFollowups: bool = None
    disableNarrative: bool = None
    enableVisualizations: bool = None
    lang: str = None
    recommendationId: str = None
    text: str = None
    visualizationTypes: list[str] = None

    def __init__(self_, **kvargs):
        if "app" in kvargs and kvargs["app"] is not None:
            if type(kvargs["app"]).__name__ == QueryCreate.__annotations__["app"]:
                self_.app = kvargs["app"]
            else:
                self_.app = QlikApp(**kvargs["app"])
        if "clearEntityContext" in kvargs and kvargs["clearEntityContext"] is not None:
            self_.clearEntityContext = kvargs["clearEntityContext"]
        if (
            "disableConversationContext" in kvargs
            and kvargs["disableConversationContext"] is not None
        ):
            self_.disableConversationContext = kvargs["disableConversationContext"]
        if "disableFollowups" in kvargs and kvargs["disableFollowups"] is not None:
            self_.disableFollowups = kvargs["disableFollowups"]
        if "disableNarrative" in kvargs and kvargs["disableNarrative"] is not None:
            self_.disableNarrative = kvargs["disableNarrative"]
        if (
            "enableVisualizations" in kvargs
            and kvargs["enableVisualizations"] is not None
        ):
            self_.enableVisualizations = kvargs["enableVisualizations"]
        if "lang" in kvargs and kvargs["lang"] is not None:
            self_.lang = kvargs["lang"]
        if "recommendationId" in kvargs and kvargs["recommendationId"] is not None:
            self_.recommendationId = kvargs["recommendationId"]
        if "text" in kvargs and kvargs["text"] is not None:
            self_.text = kvargs["text"]
        if "visualizationTypes" in kvargs and kvargs["visualizationTypes"] is not None:
            self_.visualizationTypes = kvargs["visualizationTypes"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class QueryCreated:
    """
    The attributes of sentences.

    Attributes
    ----------
    apps: list[QlikApp]
    conversationalResponse: list[QueryResponse]
      A list of conversational responses.
    nluInfo: NluInfo
    """

    apps: list[QlikApp] = None
    conversationalResponse: list[QueryResponse] = None
    nluInfo: NluInfo = None

    def __init__(self_, **kvargs):
        if "apps" in kvargs and kvargs["apps"] is not None:
            if all(
                f"list[{type(e).__name__}]" == QueryCreated.__annotations__["apps"]
                for e in kvargs["apps"]
            ):
                self_.apps = kvargs["apps"]
            else:
                self_.apps = [QlikApp(**e) for e in kvargs["apps"]]
        if (
            "conversationalResponse" in kvargs
            and kvargs["conversationalResponse"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == QueryCreated.__annotations__["conversationalResponse"]
                for e in kvargs["conversationalResponse"]
            ):
                self_.conversationalResponse = kvargs["conversationalResponse"]
            else:
                self_.conversationalResponse = [
                    QueryResponse(**e) for e in kvargs["conversationalResponse"]
                ]
        if "nluInfo" in kvargs and kvargs["nluInfo"] is not None:
            if (
                type(kvargs["nluInfo"]).__name__
                == QueryCreated.__annotations__["nluInfo"]
            ):
                self_.nluInfo = kvargs["nluInfo"]
            else:
                self_.nluInfo = NluInfo(**kvargs["nluInfo"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class QueryNotCreated:
    """

    Attributes
    ----------
    apps: list[QlikApp]
    conversationalResponse: QueryResponse
    errors: list[Error]
    nluInfo: NluInfo
    """

    apps: list[QlikApp] = None
    conversationalResponse: QueryResponse = None
    errors: list[Error] = None
    nluInfo: NluInfo = None

    def __init__(self_, **kvargs):
        if "apps" in kvargs and kvargs["apps"] is not None:
            if all(
                f"list[{type(e).__name__}]" == QueryNotCreated.__annotations__["apps"]
                for e in kvargs["apps"]
            ):
                self_.apps = kvargs["apps"]
            else:
                self_.apps = [QlikApp(**e) for e in kvargs["apps"]]
        if (
            "conversationalResponse" in kvargs
            and kvargs["conversationalResponse"] is not None
        ):
            if (
                type(kvargs["conversationalResponse"]).__name__
                == QueryNotCreated.__annotations__["conversationalResponse"]
            ):
                self_.conversationalResponse = kvargs["conversationalResponse"]
            else:
                self_.conversationalResponse = QueryResponse(
                    **kvargs["conversationalResponse"]
                )
        if "errors" in kvargs and kvargs["errors"] is not None:
            if all(
                f"list[{type(e).__name__}]" == QueryNotCreated.__annotations__["errors"]
                for e in kvargs["errors"]
            ):
                self_.errors = kvargs["errors"]
            else:
                self_.errors = [Error(**e) for e in kvargs["errors"]]
        if "nluInfo" in kvargs and kvargs["nluInfo"] is not None:
            if (
                type(kvargs["nluInfo"]).__name__
                == QueryNotCreated.__annotations__["nluInfo"]
            ):
                self_.nluInfo = kvargs["nluInfo"]
            else:
                self_.nluInfo = NluInfo(**kvargs["nluInfo"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class QueryResponse:
    """

    Attributes
    ----------
    apps: list[QlikApp]
    contextInfo: str
      For contextual responses, this string contains a list of entities that are used to produce the response.
    drillDownURI: str
      The URL with the query injected to insight advisor of the app to which the query belongs.
    responses: list[ConversationalResponsePart]
    sentenceWithMatches: str
    """

    apps: list[QlikApp] = None
    contextInfo: str = None
    drillDownURI: str = None
    responses: list[ConversationalResponsePart] = None
    sentenceWithMatches: str = None

    def __init__(self_, **kvargs):
        if "apps" in kvargs and kvargs["apps"] is not None:
            if all(
                f"list[{type(e).__name__}]" == QueryResponse.__annotations__["apps"]
                for e in kvargs["apps"]
            ):
                self_.apps = kvargs["apps"]
            else:
                self_.apps = [QlikApp(**e) for e in kvargs["apps"]]
        if "contextInfo" in kvargs and kvargs["contextInfo"] is not None:
            self_.contextInfo = kvargs["contextInfo"]
        if "drillDownURI" in kvargs and kvargs["drillDownURI"] is not None:
            self_.drillDownURI = kvargs["drillDownURI"]
        if "responses" in kvargs and kvargs["responses"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == QueryResponse.__annotations__["responses"]
                for e in kvargs["responses"]
            ):
                self_.responses = kvargs["responses"]
            else:
                self_.responses = [
                    ConversationalResponsePart(**e) for e in kvargs["responses"]
                ]
        if (
            "sentenceWithMatches" in kvargs
            and kvargs["sentenceWithMatches"] is not None
        ):
            self_.sentenceWithMatches = kvargs["sentenceWithMatches"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class RecFeedback:
    """
    Any feedback from the user about a given recommendation

    Attributes
    ----------
    analysisType: str
    chartType: str
    comment: str
    recommendationAddedToHub: bool
    recommendationAddedToSheet: bool
    recommendationDisliked: bool
    recommendationLiked: bool
    """

    analysisType: str = None
    chartType: str = None
    comment: str = None
    recommendationAddedToHub: bool = None
    recommendationAddedToSheet: bool = None
    recommendationDisliked: bool = None
    recommendationLiked: bool = None

    def __init__(self_, **kvargs):
        if "analysisType" in kvargs and kvargs["analysisType"] is not None:
            self_.analysisType = kvargs["analysisType"]
        if "chartType" in kvargs and kvargs["chartType"] is not None:
            self_.chartType = kvargs["chartType"]
        if "comment" in kvargs and kvargs["comment"] is not None:
            self_.comment = kvargs["comment"]
        if (
            "recommendationAddedToHub" in kvargs
            and kvargs["recommendationAddedToHub"] is not None
        ):
            self_.recommendationAddedToHub = kvargs["recommendationAddedToHub"]
        if (
            "recommendationAddedToSheet" in kvargs
            and kvargs["recommendationAddedToSheet"] is not None
        ):
            self_.recommendationAddedToSheet = kvargs["recommendationAddedToSheet"]
        if (
            "recommendationDisliked" in kvargs
            and kvargs["recommendationDisliked"] is not None
        ):
            self_.recommendationDisliked = kvargs["recommendationDisliked"]
        if (
            "recommendationLiked" in kvargs
            and kvargs["recommendationLiked"] is not None
        ):
            self_.recommendationLiked = kvargs["recommendationLiked"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class RenderVisualization:
    """

    Attributes
    ----------
    data: object
      Data object should be used to render visualization
    language: str
    """

    data: object = None
    language: str = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            self_.data = kvargs["data"]
        if "language" in kvargs and kvargs["language"] is not None:
            self_.language = kvargs["language"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Questions:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def ask(self, data: QueryCreate) -> any:
        """
        Returns the generated response for parsed chat queries, if no app was specified nor present in conversation context, suggests matching apps.

        Parameters
        ----------
        data: QueryCreate
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/questions/actions/ask",
            method="POST",
            params={},
            data=data,
        )
        obj = QueryNotCreated(**response.json())
        obj.auth = self.auth
        return obj

    def filter(
        self,
        data: NLMetricsRequest,
        limit: int = 100,
        page: str = None,
        sort: Literal[
            "createdAt",
            "updatedAt",
            "+createdAt",
            "+updatedAt",
            "-createdAt",
            "-updatedAt",
        ] = "+createdAt",
    ) -> ListableResource[NLMetricRecord]:
        """
        Returns NL metrics based on provided app IDs the user has access to.

        Parameters
        ----------
        limit: int = 100
          The preferred number of entries returned
        page: str = None
          A cursor pointing to the page of data to retrieve.
        sort: Literal["createdAt", "updatedAt", "+createdAt", "+updatedAt", "-createdAt", "-updatedAt"] = "+createdAt"
          A single field from the data model on which to sort the response. The '+' or '-' operator may be used to specify ascending or desending order.
        data: NLMetricsRequest
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        query_params = {}
        if limit is not None:
            query_params["limit"] = limit
        if page is not None:
            query_params["page"] = page
        if sort is not None:
            query_params["sort"] = sort
        response = self.auth.rest(
            path="/questions/actions/filter",
            method="POST",
            params=query_params,
            data=data,
        )
        return ListableResource(
            response=response.json(),
            cls=NLMetricRecord,
            auth=self.auth,
            path="/questions/actions/filter",
            query_params=query_params,
        )
