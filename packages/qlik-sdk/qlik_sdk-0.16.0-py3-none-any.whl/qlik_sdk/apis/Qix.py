# This is spectacularly generated code by spectacular based on
# QIX

from __future__ import annotations

import warnings
from dataclasses import dataclass
from typing import List, Literal

from ..rpc import RpcSession


@dataclass
class AlfaNumString:
    """

    Attributes
    ----------
    qIsNum: bool
      Is set to true if the value is a numeric.
    qString: str
      Calculated value.
    """

    qIsNum: bool = None
    qString: str = None

    def __init__(self_, **kvargs):
        if "qIsNum" in kvargs and kvargs["qIsNum"] is not None:
            self_.qIsNum = kvargs["qIsNum"]
        if "qString" in kvargs and kvargs["qString"] is not None:
            self_.qString = kvargs["qString"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AlternateStateData:
    """

    Attributes
    ----------
    qFieldItems: list[BookmarkFieldItem]
      List of the selections.
    qStateName: str
      Name of the alternate state.
      Default is current selections: $
    """

    qFieldItems: list[BookmarkFieldItem] = None
    qStateName: str = None

    def __init__(self_, **kvargs):
        if "qFieldItems" in kvargs and kvargs["qFieldItems"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == AlternateStateData.__annotations__["qFieldItems"]
                for e in kvargs["qFieldItems"]
            ):
                self_.qFieldItems = kvargs["qFieldItems"]
            else:
                self_.qFieldItems = [
                    BookmarkFieldItem(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qFieldItems"]
                ]
        if "qStateName" in kvargs and kvargs["qStateName"] is not None:
            self_.qStateName = kvargs["qStateName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppEntry:
    """

    Attributes
    ----------
    qFileSize: int
    qHasSectionAccess: bool
      If true the app has section access configured.
    qID: str
      Identifier of the app.
    qLastReloadTime: str
      Last reload time of the app.
    qMeta: NxMeta
      Meta data.
    qPath: str
      Path of the app.
    qReadOnly: bool
      Is set to true if the app is read-only.
    qThumbnail: StaticContentUrl
      App thumbnail.
    qTitle: str
      Title of the app.
    """

    qFileSize: int = None
    qHasSectionAccess: bool = None
    qID: str = None
    qLastReloadTime: str = None
    qMeta: NxMeta = None
    qPath: str = None
    qReadOnly: bool = None
    qThumbnail: StaticContentUrl = None
    qTitle: str = None

    def __init__(self_, **kvargs):
        if "qFileSize" in kvargs and kvargs["qFileSize"] is not None:
            self_.qFileSize = kvargs["qFileSize"]
        if "qHasSectionAccess" in kvargs and kvargs["qHasSectionAccess"] is not None:
            self_.qHasSectionAccess = kvargs["qHasSectionAccess"]
        if "qID" in kvargs and kvargs["qID"] is not None:
            self_.qID = kvargs["qID"]
        if "qLastReloadTime" in kvargs and kvargs["qLastReloadTime"] is not None:
            self_.qLastReloadTime = kvargs["qLastReloadTime"]
        if "qMeta" in kvargs and kvargs["qMeta"] is not None:
            if type(kvargs["qMeta"]).__name__ == AppEntry.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeta"],
                )
        if "qPath" in kvargs and kvargs["qPath"] is not None:
            self_.qPath = kvargs["qPath"]
        if "qReadOnly" in kvargs and kvargs["qReadOnly"] is not None:
            self_.qReadOnly = kvargs["qReadOnly"]
        if "qThumbnail" in kvargs and kvargs["qThumbnail"] is not None:
            if (
                type(kvargs["qThumbnail"]).__name__
                == AppEntry.__annotations__["qThumbnail"]
            ):
                self_.qThumbnail = kvargs["qThumbnail"]
            else:
                self_.qThumbnail = StaticContentUrl(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qThumbnail"],
                )
        if "qTitle" in kvargs and kvargs["qTitle"] is not None:
            self_.qTitle = kvargs["qTitle"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppObjectList:
    """
    Lists the app objects. Is the layout for AppObjectListDef.
    An app object is a generic object created at app level.

    Attributes
    ----------
    qItems: list[NxContainerEntry]
      Information about the list of dimensions.
    """

    qItems: list[NxContainerEntry] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs and kvargs["qItems"] is not None:
            if all(
                f"list[{type(e).__name__}]" == AppObjectList.__annotations__["qItems"]
                for e in kvargs["qItems"]
            ):
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [
                    NxContainerEntry(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qItems"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppObjectListDef:
    """
    Defines the list of objects in an app.
    An app object is a generic object created at app level.

    Attributes
    ----------
    qData: JsonObject
      Data that you want to include in the app list definition.
      You need to enter the paths to the information you want to retrieve.
    qType: str
      Type of the app list.
    """

    qData: JsonObject = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qData" in kvargs and kvargs["qData"] is not None:
            if (
                type(kvargs["qData"]).__name__
                == AppObjectListDef.__annotations__["qData"]
            ):
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qData"],
                )
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppScript:
    """

    Attributes
    ----------
    qIsLocked: bool
      True if user is temporarily locked from modifying the script. Meta contains the ID of the last modifier. Only applicable to QCS.
    qMeta: NxMeta
      Information about publishing and permissions.
      This parameter is optional.
    qScript: str
      Script text.
    """

    qIsLocked: bool = None
    qMeta: NxMeta = None
    qScript: str = None

    def __init__(self_, **kvargs):
        if "qIsLocked" in kvargs and kvargs["qIsLocked"] is not None:
            self_.qIsLocked = kvargs["qIsLocked"]
        if "qMeta" in kvargs and kvargs["qMeta"] is not None:
            if type(kvargs["qMeta"]).__name__ == AppScript.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeta"],
                )
        if "qScript" in kvargs and kvargs["qScript"] is not None:
            self_.qScript = kvargs["qScript"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AppScriptMeta:
    """

    Attributes
    ----------
    qIsLocked: bool
      True if user is temporarily locked from modifying the script. Meta contains the ID of the last modifier. Only applicable to QCS.
    qMeta: NxMeta
      Information about publishing and permissions.
      This parameter is optional.
    """

    qIsLocked: bool = None
    qMeta: NxMeta = None

    def __init__(self_, **kvargs):
        if "qIsLocked" in kvargs and kvargs["qIsLocked"] is not None:
            self_.qIsLocked = kvargs["qIsLocked"]
        if "qMeta" in kvargs and kvargs["qMeta"] is not None:
            if type(kvargs["qMeta"]).__name__ == AppScriptMeta.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeta"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ArrayOfNxValuePoint(List["NxPivotValuePoint"]):
    """

    Attributes
    ----------
    """

    def __init__(self_, elements):
        for e in elements:
            self_.append(NxPivotValuePoint(**e))


@dataclass
class AssociationScore:
    """

    Attributes
    ----------
    qField1Scores: FieldScores
      Association information about the field FieldName1 defined in qFieldPairName .
    qField2Scores: FieldScores
      Association information about the field FieldName2 defined in qFieldPairName .
    qFieldPairName: str
      Pair of fields.
      < FieldName1> / < FieldName2>
      Where:
      < FieldName1 > is a field in the table 1 (defined in qTable1 )
      < FieldName2 > is a field in the table 2 (defined in qTable2 )
      If the field is a synthetic key, the name of the field is preceded by [Synthetic key]: .
    qScoreSummary: int
      Flag used to interpret calculated scores.
      One of the following values or sum of values that apply:

      • 0: The cardinal ratio cannot be zero but the symbol score and the row score can be zero.

      • -1: The fields do not have the same type.

      • -2: The number of rows of the field FieldName1 is zero.

      • -4: The number of distinct values of the field FieldName1 is zero.

      • -8: The number of rows of the field FieldName2 is zero.

      • -16: The number of distinct values of the field FieldName2 is zero.

      Example:
      The number of rows of the field FieldName1 is zero, and the number of distinct values of the field FieldName2 is zero, then qScoreSummary is -18.
    """

    qField1Scores: FieldScores = None
    qField2Scores: FieldScores = None
    qFieldPairName: str = None
    qScoreSummary: int = None

    def __init__(self_, **kvargs):
        if "qField1Scores" in kvargs and kvargs["qField1Scores"] is not None:
            if (
                type(kvargs["qField1Scores"]).__name__
                == AssociationScore.__annotations__["qField1Scores"]
            ):
                self_.qField1Scores = kvargs["qField1Scores"]
            else:
                self_.qField1Scores = FieldScores(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qField1Scores"],
                )
        if "qField2Scores" in kvargs and kvargs["qField2Scores"] is not None:
            if (
                type(kvargs["qField2Scores"]).__name__
                == AssociationScore.__annotations__["qField2Scores"]
            ):
                self_.qField2Scores = kvargs["qField2Scores"]
            else:
                self_.qField2Scores = FieldScores(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qField2Scores"],
                )
        if "qFieldPairName" in kvargs and kvargs["qFieldPairName"] is not None:
            self_.qFieldPairName = kvargs["qFieldPairName"]
        if "qScoreSummary" in kvargs and kvargs["qScoreSummary"] is not None:
            self_.qScoreSummary = kvargs["qScoreSummary"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BNFDef:
    """

    Attributes
    ----------
    qAggrFunc: bool
      If set to true, the definition is related to an aggregation function.
      This parameter is optional. The default value is false.
    qBnf: list[int]
      Array of token references that all together build up the definition of the current token.
      Generally, if the array is not empty, the definition is a BNF rule (qIsBnfRule is set to true). However, some BNF  rules do have an empty array (qIsBnfRule is set to true, but qBnf is empty).
    qBnfLiteral: bool
      If set to true, the definition specifies a literal token.
      This parameter is optional. The default value is false.
    qControlStatement: bool
      If set to true, the definition specifies a control statement.
      This parameter is optional. The default value is false.
    qDepr: bool
      Indicates whether a script statement, a chart or a script function is deprecated (not recommended for use).
      If set to true, the script statement or the function is not recommended for use in Qlik Sense.
      This parameter is optional. The default value is false.
    qFG: Literal["FUNC_GROUP_ALL", "FUNC_GROUP_UNKNOWN", "FUNC_GROUP_NONE", "FUNC_GROUP_AGGR", "FUNC_GROUP_NUMERIC", "FUNC_GROUP_RANGE", "FUNC_GROUP_EXPONENTIAL_AND_LOGARITHMIC", "FUNC_GROUP_TRIGONOMETRIC_AND_HYPERBOLIC", "FUNC_GROUP_FINANCIAL", "FUNC_GROUP_MATH_CONSTANT_AND_PARAM_FREE", "FUNC_GROUP_COUNTER", "FUNC_GROUP_STRING", "FUNC_GROUP_MAPPING", "FUNC_GROUP_INTER_RECORD", "FUNC_GROUP_CONDITIONAL", "FUNC_GROUP_LOGICAL", "FUNC_GROUP_NULL", "FUNC_GROUP_SYSTEM", "FUNC_GROUP_FILE", "FUNC_GROUP_TABLE", "FUNC_GROUP_DATE_AND_TIME", "FUNC_GROUP_NUMBER_INTERPRET", "FUNC_GROUP_FORMATTING", "FUNC_GROUP_COLOR", "FUNC_GROUP_RANKING", "FUNC_GROUP_GEO", "FUNC_GROUP_EXTERNAL", "FUNC_GROUP_PROBABILITY", "FUNC_GROUP_ARRAY", "FUNC_GROUP_LEGACY", "FUNC_GROUP_DB_NATIVE"]
      Group of the function.

      One of:

      • ALL or FUNC_GROUP_ALL

      • U or FUNC_GROUP_UNKNOWN

      • NONE or FUNC_GROUP_NONE

      • AGGR or FUNC_GROUP_AGGR

      • NUM or FUNC_GROUP_NUMERIC

      • RNG or FUNC_GROUP_RANGE

      • EXP or FUNC_GROUP_EXPONENTIAL_AND_LOGARITHMIC

      • TRIG or FUNC_GROUP_TRIGONOMETRIC_AND_HYPERBOLIC

      • FIN or FUNC_GROUP_FINANCIAL

      • MATH or FUNC_GROUP_MATH_CONSTANT_AND_PARAM_FREE

      • COUNT or FUNC_GROUP_COUNTER

      • STR or FUNC_GROUP_STRING

      • MAPP or FUNC_GROUP_MAPPING

      • RCRD or FUNC_GROUP_INTER_RECORD

      • CND or FUNC_GROUP_CONDITIONAL

      • LOG or FUNC_GROUP_LOGICAL

      • NULL or FUNC_GROUP_NULL

      • SYS or FUNC_GROUP_SYSTEM

      • FILE or FUNC_GROUP_FILE

      • TBL or FUNC_GROUP_TABLE

      • DATE or FUNC_GROUP_DATE_AND_TIME

      • NUMI or FUNC_GROUP_NUMBER_INTERPRET

      • FRMT or FUNC_GROUP_FORMATTING

      • CLR or FUNC_GROUP_COLOR

      • RNK or FUNC_GROUP_RANKING

      • GEO or FUNC_GROUP_GEO

      • EXT or FUNC_GROUP_EXTERNAL

      • PROB or FUNC_GROUP_PROBABILITY

      • ARRAY or FUNC_GROUP_ARRAY

      • LEG or FUNC_GROUP_LEGACY

      • DB or FUNC_GROUP_DB_NATIVE
    qFGList: list[str]
      List of groups the function belongs to.
    qFieldFlag: bool
      If set to true, the definition is related to a field.
      This parameter is optional. The default value is false.
    qHelpId: int
      Reference identifier to a function described in the documentation. The identifier is stored in the definition of the token containing the function name.
      Is not used in Qlik Sense.
    qIsBnfRule: bool
      If set to true, a list of related rule tokens is assigned to qBnf .
      This parameter is optional. The default value is false.
    qMT: Literal["NOT_META", "META_DOC_NAME", "META_RET_TYPE", "META_DEFAULT_VALUE"]
      Type of the data.

      One of:

      • N or NOT_META

      • D or META_DOC_NAME

      • R or META_RET_TYPE

      • V or META_DEFAULT_VALUE
    qName: str
      Token name.
      One of:

      • A rule name

      • An identifier

      • A literal value
    qNbr: int
      Number of the current token definition.
    qPNbr: int
      Number of the parent rule definition.
    qQvFunc: bool
      If set to true, the definition is related to a Qlik Sense function. It cannot be an aggregation function.
      This parameter is optional. The default value is false.
    qScriptStatement: bool
      If set to true, the definition specifies a script statement.
      This parameter is optional. The default value is false.
    qStr: str
      Literal string of the token.
      Examples: 'Round' and '('.
    """

    qAggrFunc: bool = None
    qBnf: list[int] = None
    qBnfLiteral: bool = None
    qControlStatement: bool = None
    qDepr: bool = None
    qFG: Literal[
        "FUNC_GROUP_ALL",
        "FUNC_GROUP_UNKNOWN",
        "FUNC_GROUP_NONE",
        "FUNC_GROUP_AGGR",
        "FUNC_GROUP_NUMERIC",
        "FUNC_GROUP_RANGE",
        "FUNC_GROUP_EXPONENTIAL_AND_LOGARITHMIC",
        "FUNC_GROUP_TRIGONOMETRIC_AND_HYPERBOLIC",
        "FUNC_GROUP_FINANCIAL",
        "FUNC_GROUP_MATH_CONSTANT_AND_PARAM_FREE",
        "FUNC_GROUP_COUNTER",
        "FUNC_GROUP_STRING",
        "FUNC_GROUP_MAPPING",
        "FUNC_GROUP_INTER_RECORD",
        "FUNC_GROUP_CONDITIONAL",
        "FUNC_GROUP_LOGICAL",
        "FUNC_GROUP_NULL",
        "FUNC_GROUP_SYSTEM",
        "FUNC_GROUP_FILE",
        "FUNC_GROUP_TABLE",
        "FUNC_GROUP_DATE_AND_TIME",
        "FUNC_GROUP_NUMBER_INTERPRET",
        "FUNC_GROUP_FORMATTING",
        "FUNC_GROUP_COLOR",
        "FUNC_GROUP_RANKING",
        "FUNC_GROUP_GEO",
        "FUNC_GROUP_EXTERNAL",
        "FUNC_GROUP_PROBABILITY",
        "FUNC_GROUP_ARRAY",
        "FUNC_GROUP_LEGACY",
        "FUNC_GROUP_DB_NATIVE",
    ] = None
    qFGList: list[str] = None
    qFieldFlag: bool = None
    qHelpId: int = None
    qIsBnfRule: bool = None
    qMT: Literal[
        "NOT_META", "META_DOC_NAME", "META_RET_TYPE", "META_DEFAULT_VALUE"
    ] = None
    qName: str = None
    qNbr: int = None
    qPNbr: int = None
    qQvFunc: bool = None
    qScriptStatement: bool = None
    qStr: str = None

    def __init__(self_, **kvargs):
        if "qAggrFunc" in kvargs and kvargs["qAggrFunc"] is not None:
            self_.qAggrFunc = kvargs["qAggrFunc"]
        if "qBnf" in kvargs and kvargs["qBnf"] is not None:
            self_.qBnf = kvargs["qBnf"]
        if "qBnfLiteral" in kvargs and kvargs["qBnfLiteral"] is not None:
            self_.qBnfLiteral = kvargs["qBnfLiteral"]
        if "qControlStatement" in kvargs and kvargs["qControlStatement"] is not None:
            self_.qControlStatement = kvargs["qControlStatement"]
        if "qDepr" in kvargs and kvargs["qDepr"] is not None:
            self_.qDepr = kvargs["qDepr"]
        if "qFG" in kvargs and kvargs["qFG"] is not None:
            self_.qFG = kvargs["qFG"]
        if "qFGList" in kvargs and kvargs["qFGList"] is not None:
            self_.qFGList = kvargs["qFGList"]
        if "qFieldFlag" in kvargs and kvargs["qFieldFlag"] is not None:
            self_.qFieldFlag = kvargs["qFieldFlag"]
        if "qHelpId" in kvargs and kvargs["qHelpId"] is not None:
            self_.qHelpId = kvargs["qHelpId"]
        if "qIsBnfRule" in kvargs and kvargs["qIsBnfRule"] is not None:
            self_.qIsBnfRule = kvargs["qIsBnfRule"]
        if "qMT" in kvargs and kvargs["qMT"] is not None:
            self_.qMT = kvargs["qMT"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qNbr" in kvargs and kvargs["qNbr"] is not None:
            self_.qNbr = kvargs["qNbr"]
        if "qPNbr" in kvargs and kvargs["qPNbr"] is not None:
            self_.qPNbr = kvargs["qPNbr"]
        if "qQvFunc" in kvargs and kvargs["qQvFunc"] is not None:
            self_.qQvFunc = kvargs["qQvFunc"]
        if "qScriptStatement" in kvargs and kvargs["qScriptStatement"] is not None:
            self_.qScriptStatement = kvargs["qScriptStatement"]
        if "qStr" in kvargs and kvargs["qStr"] is not None:
            self_.qStr = kvargs["qStr"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BNFDefMetaType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BNFType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Blob:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Bookmark:
    """

    Attributes
    ----------
    qAlternateStateData: list[AlternateStateData]
    qApplyAdditive: bool
    qApplyInputFieldValues: bool
    qApplyLayoutState: bool
    qFieldItems: list[BookmarkFieldItem]
    qForAnnotations: bool
    qGroups: list[GroupBookmarkData]
    qId: str
    qIncludeAllVariables: bool
    qIncludeScrollPosition: bool
    qIncludeSelectionState: bool
    qInfoText: str
    qInputFieldItems: list[InputFieldItem]
    qName: str
    qObjects: list[LayoutBookmarkData]
    qObjectsLayout: list[ExtendedLayoutBookmarkData]
    qOwner: str
    qRecallCount: int
    qSheetId: str
    qShow: CondDef
    qShowPopupInfo: bool
    qUtcModifyTime: float
    qUtcRecallTime: float
    qVariableItems: list[BookmarkVariableItem]
    """

    qAlternateStateData: list[AlternateStateData] = None
    qApplyAdditive: bool = None
    qApplyInputFieldValues: bool = True
    qApplyLayoutState: bool = None
    qFieldItems: list[BookmarkFieldItem] = None
    qForAnnotations: bool = None
    qGroups: list[GroupBookmarkData] = None
    qId: str = None
    qIncludeAllVariables: bool = None
    qIncludeScrollPosition: bool = None
    qIncludeSelectionState: bool = True
    qInfoText: str = None
    qInputFieldItems: list[InputFieldItem] = None
    qName: str = None
    qObjects: list[LayoutBookmarkData] = None
    qObjectsLayout: list[ExtendedLayoutBookmarkData] = None
    qOwner: str = None
    qRecallCount: int = None
    qSheetId: str = None
    qShow: CondDef = None
    qShowPopupInfo: bool = None
    qUtcModifyTime: float = None
    qUtcRecallTime: float = None
    qVariableItems: list[BookmarkVariableItem] = None

    def __init__(self_, **kvargs):
        if (
            "qAlternateStateData" in kvargs
            and kvargs["qAlternateStateData"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == Bookmark.__annotations__["qAlternateStateData"]
                for e in kvargs["qAlternateStateData"]
            ):
                self_.qAlternateStateData = kvargs["qAlternateStateData"]
            else:
                self_.qAlternateStateData = [
                    AlternateStateData(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qAlternateStateData"]
                ]
        if "qApplyAdditive" in kvargs and kvargs["qApplyAdditive"] is not None:
            self_.qApplyAdditive = kvargs["qApplyAdditive"]
        if (
            "qApplyInputFieldValues" in kvargs
            and kvargs["qApplyInputFieldValues"] is not None
        ):
            self_.qApplyInputFieldValues = kvargs["qApplyInputFieldValues"]
        if "qApplyLayoutState" in kvargs and kvargs["qApplyLayoutState"] is not None:
            self_.qApplyLayoutState = kvargs["qApplyLayoutState"]
        if "qFieldItems" in kvargs and kvargs["qFieldItems"] is not None:
            if all(
                f"list[{type(e).__name__}]" == Bookmark.__annotations__["qFieldItems"]
                for e in kvargs["qFieldItems"]
            ):
                self_.qFieldItems = kvargs["qFieldItems"]
            else:
                self_.qFieldItems = [
                    BookmarkFieldItem(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qFieldItems"]
                ]
        if "qForAnnotations" in kvargs and kvargs["qForAnnotations"] is not None:
            self_.qForAnnotations = kvargs["qForAnnotations"]
        if "qGroups" in kvargs and kvargs["qGroups"] is not None:
            if all(
                f"list[{type(e).__name__}]" == Bookmark.__annotations__["qGroups"]
                for e in kvargs["qGroups"]
            ):
                self_.qGroups = kvargs["qGroups"]
            else:
                self_.qGroups = [
                    GroupBookmarkData(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qGroups"]
                ]
        if "qId" in kvargs and kvargs["qId"] is not None:
            self_.qId = kvargs["qId"]
        if (
            "qIncludeAllVariables" in kvargs
            and kvargs["qIncludeAllVariables"] is not None
        ):
            self_.qIncludeAllVariables = kvargs["qIncludeAllVariables"]
        if (
            "qIncludeScrollPosition" in kvargs
            and kvargs["qIncludeScrollPosition"] is not None
        ):
            self_.qIncludeScrollPosition = kvargs["qIncludeScrollPosition"]
        if (
            "qIncludeSelectionState" in kvargs
            and kvargs["qIncludeSelectionState"] is not None
        ):
            self_.qIncludeSelectionState = kvargs["qIncludeSelectionState"]
        if "qInfoText" in kvargs and kvargs["qInfoText"] is not None:
            self_.qInfoText = kvargs["qInfoText"]
        if "qInputFieldItems" in kvargs and kvargs["qInputFieldItems"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == Bookmark.__annotations__["qInputFieldItems"]
                for e in kvargs["qInputFieldItems"]
            ):
                self_.qInputFieldItems = kvargs["qInputFieldItems"]
            else:
                self_.qInputFieldItems = [
                    InputFieldItem(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qInputFieldItems"]
                ]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qObjects" in kvargs and kvargs["qObjects"] is not None:
            if all(
                f"list[{type(e).__name__}]" == Bookmark.__annotations__["qObjects"]
                for e in kvargs["qObjects"]
            ):
                self_.qObjects = kvargs["qObjects"]
            else:
                self_.qObjects = [
                    LayoutBookmarkData(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qObjects"]
                ]
        if "qObjectsLayout" in kvargs and kvargs["qObjectsLayout"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == Bookmark.__annotations__["qObjectsLayout"]
                for e in kvargs["qObjectsLayout"]
            ):
                self_.qObjectsLayout = kvargs["qObjectsLayout"]
            else:
                self_.qObjectsLayout = [
                    ExtendedLayoutBookmarkData(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qObjectsLayout"]
                ]
        if "qOwner" in kvargs and kvargs["qOwner"] is not None:
            self_.qOwner = kvargs["qOwner"]
        if "qRecallCount" in kvargs and kvargs["qRecallCount"] is not None:
            self_.qRecallCount = kvargs["qRecallCount"]
        if "qSheetId" in kvargs and kvargs["qSheetId"] is not None:
            self_.qSheetId = kvargs["qSheetId"]
        if "qShow" in kvargs and kvargs["qShow"] is not None:
            if type(kvargs["qShow"]).__name__ == Bookmark.__annotations__["qShow"]:
                self_.qShow = kvargs["qShow"]
            else:
                self_.qShow = CondDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qShow"],
                )
        if "qShowPopupInfo" in kvargs and kvargs["qShowPopupInfo"] is not None:
            self_.qShowPopupInfo = kvargs["qShowPopupInfo"]
        if "qUtcModifyTime" in kvargs and kvargs["qUtcModifyTime"] is not None:
            self_.qUtcModifyTime = kvargs["qUtcModifyTime"]
        if "qUtcRecallTime" in kvargs and kvargs["qUtcRecallTime"] is not None:
            self_.qUtcRecallTime = kvargs["qUtcRecallTime"]
        if "qVariableItems" in kvargs and kvargs["qVariableItems"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == Bookmark.__annotations__["qVariableItems"]
                for e in kvargs["qVariableItems"]
            ):
                self_.qVariableItems = kvargs["qVariableItems"]
            else:
                self_.qVariableItems = [
                    BookmarkVariableItem(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qVariableItems"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BookmarkApplyAndVerifyResult:
    """

    Attributes
    ----------
    qApplySuccess: bool
      Apply successfully or not *
    qWarnings: list[BookmarkFieldVerifyWarning]
      Field values verfication result *
    """

    qApplySuccess: bool = None
    qWarnings: list[BookmarkFieldVerifyWarning] = None

    def __init__(self_, **kvargs):
        if "qApplySuccess" in kvargs and kvargs["qApplySuccess"] is not None:
            self_.qApplySuccess = kvargs["qApplySuccess"]
        if "qWarnings" in kvargs and kvargs["qWarnings"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == BookmarkApplyAndVerifyResult.__annotations__["qWarnings"]
                for e in kvargs["qWarnings"]
            ):
                self_.qWarnings = kvargs["qWarnings"]
            else:
                self_.qWarnings = [
                    BookmarkFieldVerifyWarning(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qWarnings"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BookmarkFieldItem:
    """

    Attributes
    ----------
    qAndMode: bool
      If set to true, selections within a list object are made in AND mode; If you have a list object that lists all customers, by selecting Customer 1 and Customer 2 while in and-mode, all records that are associated with Customer 1 and Customer 2 are selected.
      The default value is false; selections within a list object are made in OR mode. If you have a list object that lists all customers, by selecting Customer 1 and Customer 2 while in or-mode, all records that are associated with either Customer 1 or Customer 2 are selected.
      This parameter is not returned if set to false.
    qDef: FieldDefEx
      Name and type of the field.
    qExcludedValues: list[FieldValue]
      List of excluded values.
      Either the list of selected values or the list of excluded values is displayed.
    qLocked: bool
      Indicates if the field is locked.
      Default is false.
    qOneAndOnlyOne: bool
      If set to true, the field has always one selection (not 0 and not more than 1). If another value is selected, the previous one is unselected.
      The default value is false. This parameter is not returned if set to false.
    qSelectInfo: SelectInfo
      Information on the selections criteria.
    qValues: list[FieldValue]
    """

    qAndMode: bool = None
    qDef: FieldDefEx = None
    qExcludedValues: list[FieldValue] = None
    qLocked: bool = None
    qOneAndOnlyOne: bool = None
    qSelectInfo: SelectInfo = None
    qValues: list[FieldValue] = None

    def __init__(self_, **kvargs):
        if "qAndMode" in kvargs and kvargs["qAndMode"] is not None:
            self_.qAndMode = kvargs["qAndMode"]
        if "qDef" in kvargs and kvargs["qDef"] is not None:
            if (
                type(kvargs["qDef"]).__name__
                == BookmarkFieldItem.__annotations__["qDef"]
            ):
                self_.qDef = kvargs["qDef"]
            else:
                self_.qDef = FieldDefEx(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qDef"],
                )
        if "qExcludedValues" in kvargs and kvargs["qExcludedValues"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == BookmarkFieldItem.__annotations__["qExcludedValues"]
                for e in kvargs["qExcludedValues"]
            ):
                self_.qExcludedValues = kvargs["qExcludedValues"]
            else:
                self_.qExcludedValues = [
                    FieldValue(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qExcludedValues"]
                ]
        if "qLocked" in kvargs and kvargs["qLocked"] is not None:
            self_.qLocked = kvargs["qLocked"]
        if "qOneAndOnlyOne" in kvargs and kvargs["qOneAndOnlyOne"] is not None:
            self_.qOneAndOnlyOne = kvargs["qOneAndOnlyOne"]
        if "qSelectInfo" in kvargs and kvargs["qSelectInfo"] is not None:
            if (
                type(kvargs["qSelectInfo"]).__name__
                == BookmarkFieldItem.__annotations__["qSelectInfo"]
            ):
                self_.qSelectInfo = kvargs["qSelectInfo"]
            else:
                self_.qSelectInfo = SelectInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qSelectInfo"],
                )
        if "qValues" in kvargs and kvargs["qValues"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == BookmarkFieldItem.__annotations__["qValues"]
                for e in kvargs["qValues"]
            ):
                self_.qValues = kvargs["qValues"]
            else:
                self_.qValues = [
                    FieldValue(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qValues"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BookmarkFieldPage:
    """
    Defines the range of the bookmark fields that are returned.

    Attributes
    ----------
    qEndIndex: int
      The end value of the range.
    qStartIndex: int
      The start value of the range.
    """

    qEndIndex: int = None
    qStartIndex: int = None

    def __init__(self_, **kvargs):
        if "qEndIndex" in kvargs and kvargs["qEndIndex"] is not None:
            self_.qEndIndex = kvargs["qEndIndex"]
        if "qStartIndex" in kvargs and kvargs["qStartIndex"] is not None:
            self_.qStartIndex = kvargs["qStartIndex"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BookmarkFieldVerifyResultState:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BookmarkFieldVerifyWarning:
    """

    Attributes
    ----------
    qField: str
      Field Name *
    qMissingValues: list[str]
    qState: str
      Alternate State *
    qVerifyResult: Literal["NOT_VERIFIED", "FIELD_VALUE_MATCH_ALL", "FIELD_MISSING", "FIELD_VALUE_MISSING", "STATE_MISSING"]
      Field/values verfication result *
      Defines result of ApplyAndVerify.
      One of:

      • NOT_VERIFIED

      • FIELD_VALUE_MATCH_ALL

      • FIELD_MISSING

      • FIELD_VALUE_MISSING

      • STATE_MISSING
    """

    qField: str = None
    qMissingValues: list[str] = None
    qState: str = None
    qVerifyResult: Literal[
        "NOT_VERIFIED",
        "FIELD_VALUE_MATCH_ALL",
        "FIELD_MISSING",
        "FIELD_VALUE_MISSING",
        "STATE_MISSING",
    ] = "NOT_VERIFIED"

    def __init__(self_, **kvargs):
        if "qField" in kvargs and kvargs["qField"] is not None:
            self_.qField = kvargs["qField"]
        if "qMissingValues" in kvargs and kvargs["qMissingValues"] is not None:
            self_.qMissingValues = kvargs["qMissingValues"]
        if "qState" in kvargs and kvargs["qState"] is not None:
            self_.qState = kvargs["qState"]
        if "qVerifyResult" in kvargs and kvargs["qVerifyResult"] is not None:
            self_.qVerifyResult = kvargs["qVerifyResult"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BookmarkList:
    """
    Lists the bookmarks. Is the layout for BookmarkListDef.

    Attributes
    ----------
    qItems: list[NxContainerEntry]
      Information about the list of bookmarks.
    """

    qItems: list[NxContainerEntry] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs and kvargs["qItems"] is not None:
            if all(
                f"list[{type(e).__name__}]" == BookmarkList.__annotations__["qItems"]
                for e in kvargs["qItems"]
            ):
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [
                    NxContainerEntry(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qItems"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BookmarkListDef:
    """
    Defines the list of bookmarks.

    Attributes
    ----------
    qData: JsonObject
      Data
    qIncludePatches: bool
      Include the bookmark patches. Patches can be very large and may make the list result unmanageable.
    qType: str
      Type of the list.
    """

    qData: JsonObject = None
    qIncludePatches: bool = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qData" in kvargs and kvargs["qData"] is not None:
            if (
                type(kvargs["qData"]).__name__
                == BookmarkListDef.__annotations__["qData"]
            ):
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qData"],
                )
        if "qIncludePatches" in kvargs and kvargs["qIncludePatches"] is not None:
            self_.qIncludePatches = kvargs["qIncludePatches"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BookmarkVariableItem:
    """

    Attributes
    ----------
    qDefinition: str
      The Reporting mode definition of the variable.
    qName: str
      Name of the variable.
    qValue: FieldValue
      Value of the variable.
    """

    qDefinition: str = None
    qName: str = None
    qValue: FieldValue = None

    def __init__(self_, **kvargs):
        if "qDefinition" in kvargs and kvargs["qDefinition"] is not None:
            self_.qDefinition = kvargs["qDefinition"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qValue" in kvargs and kvargs["qValue"] is not None:
            if (
                type(kvargs["qValue"]).__name__
                == BookmarkVariableItem.__annotations__["qValue"]
            ):
                self_.qValue = kvargs["qValue"]
            else:
                self_.qValue = FieldValue(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qValue"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CalendarStrings:
    """

    Attributes
    ----------
    qDayNames: list[str]
      List of short day names.
    qLongDayNames: list[str]
      List of long day names.
    qLongMonthNames: list[str]
      List of long month names.
    qMonthNames: list[str]
      List of short month names.
    """

    qDayNames: list[str] = None
    qLongDayNames: list[str] = None
    qLongMonthNames: list[str] = None
    qMonthNames: list[str] = None

    def __init__(self_, **kvargs):
        if "qDayNames" in kvargs and kvargs["qDayNames"] is not None:
            self_.qDayNames = kvargs["qDayNames"]
        if "qLongDayNames" in kvargs and kvargs["qLongDayNames"] is not None:
            self_.qLongDayNames = kvargs["qLongDayNames"]
        if "qLongMonthNames" in kvargs and kvargs["qLongMonthNames"] is not None:
            self_.qLongMonthNames = kvargs["qLongMonthNames"]
        if "qMonthNames" in kvargs and kvargs["qMonthNames"] is not None:
            self_.qMonthNames = kvargs["qMonthNames"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CharEncodingType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CharRange:
    """

    Attributes
    ----------
    qCharCount: int
      Number of occurrences found.
    qCharPos: int
      Position of the first search occurrence.
    """

    qCharCount: int = None
    qCharPos: int = None

    def __init__(self_, **kvargs):
        if "qCharCount" in kvargs and kvargs["qCharCount"] is not None:
            self_.qCharCount = kvargs["qCharCount"]
        if "qCharPos" in kvargs and kvargs["qCharPos"] is not None:
            self_.qCharPos = kvargs["qCharPos"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CheckExpressionReturn:
    """

    Attributes
    ----------
    qBadFieldNames: list[NxRange]
    qDangerousFieldNames: list[NxRange]
    qErrorMsg: str
    """

    qBadFieldNames: list[NxRange] = None
    qDangerousFieldNames: list[NxRange] = None
    qErrorMsg: str = None

    def __init__(self_, **kvargs):
        if "qBadFieldNames" in kvargs and kvargs["qBadFieldNames"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == CheckExpressionReturn.__annotations__["qBadFieldNames"]
                for e in kvargs["qBadFieldNames"]
            ):
                self_.qBadFieldNames = kvargs["qBadFieldNames"]
            else:
                self_.qBadFieldNames = [
                    NxRange(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qBadFieldNames"]
                ]
        if (
            "qDangerousFieldNames" in kvargs
            and kvargs["qDangerousFieldNames"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == CheckExpressionReturn.__annotations__["qDangerousFieldNames"]
                for e in kvargs["qDangerousFieldNames"]
            ):
                self_.qDangerousFieldNames = kvargs["qDangerousFieldNames"]
            else:
                self_.qDangerousFieldNames = [
                    NxRange(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qDangerousFieldNames"]
                ]
        if "qErrorMsg" in kvargs and kvargs["qErrorMsg"] is not None:
            self_.qErrorMsg = kvargs["qErrorMsg"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CheckNumberOrExpressionReturn:
    """

    Attributes
    ----------
    qBadFieldNames: list[NxRange]
    qErrorMsg: str
    """

    qBadFieldNames: list[NxRange] = None
    qErrorMsg: str = None

    def __init__(self_, **kvargs):
        if "qBadFieldNames" in kvargs and kvargs["qBadFieldNames"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == CheckNumberOrExpressionReturn.__annotations__["qBadFieldNames"]
                for e in kvargs["qBadFieldNames"]
            ):
                self_.qBadFieldNames = kvargs["qBadFieldNames"]
            else:
                self_.qBadFieldNames = [
                    NxRange(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qBadFieldNames"]
                ]
        if "qErrorMsg" in kvargs and kvargs["qErrorMsg"] is not None:
            self_.qErrorMsg = kvargs["qErrorMsg"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ChildList:
    """
    Lists the children of a generic object. Is the layout for ChildListDef.
    ChildList is used by the GetLayout Method to list the children of a generic object.

    Attributes
    ----------
    qItems: list[NxContainerEntry]
      Information about the items in the app object.
    """

    qItems: list[NxContainerEntry] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs and kvargs["qItems"] is not None:
            if all(
                f"list[{type(e).__name__}]" == ChildList.__annotations__["qItems"]
                for e in kvargs["qItems"]
            ):
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [
                    NxContainerEntry(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qItems"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ChildListDef:
    """
    Defines the list of children of a generic object.
    What is defined in ChildListDef has an impact on what the GetLayout method returns. See Example for more information.

    Attributes
    ----------
    qData: JsonObject
      Data that you want to include in the child list definition.
      You need to enter the paths to the information you want to retrieve.
    """

    qData: JsonObject = None

    def __init__(self_, **kvargs):
        if "qData" in kvargs and kvargs["qData"] is not None:
            if type(kvargs["qData"]).__name__ == ChildListDef.__annotations__["qData"]:
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qData"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CodePage:
    """

    Attributes
    ----------
    qDescription: str
      Description of the code page.
    qName: str
      Name of the code page.
    qNumber: int
      Number of the code page.
    """

    qDescription: str = None
    qName: str = None
    qNumber: int = None

    def __init__(self_, **kvargs):
        if "qDescription" in kvargs and kvargs["qDescription"] is not None:
            self_.qDescription = kvargs["qDescription"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qNumber" in kvargs and kvargs["qNumber"] is not None:
            self_.qNumber = kvargs["qNumber"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CondDef:
    """

    Attributes
    ----------
    qAlways: bool
    qExpression: ValueExpr
    """

    qAlways: bool = True
    qExpression: ValueExpr = None

    def __init__(self_, **kvargs):
        if "qAlways" in kvargs and kvargs["qAlways"] is not None:
            self_.qAlways = kvargs["qAlways"]
        if "qExpression" in kvargs and kvargs["qExpression"] is not None:
            if (
                type(kvargs["qExpression"]).__name__
                == CondDef.__annotations__["qExpression"]
            ):
                self_.qExpression = kvargs["qExpression"]
            else:
                self_.qExpression = ValueExpr(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qExpression"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Connection:
    """

    Attributes
    ----------
    qConnectionString: str
      One of:

      • ODBC CONNECT TO [<provider name>]

      • OLEDB CONNECT TO [<provider name>]

      • CUSTOM CONNECT TO [<provider name>]

      • "<local absolute or relative path, UNC path>"

      • "<URL>"

      Connection string.
      This parameter is mandatory and must be set when creating or modifying a connection.
    qId: str
      Identifier of the connection.
      Is generated by the engine and is unique.
    qLogOn: Literal["LOG_ON_SERVICE_USER", "LOG_ON_CURRENT_USER"]
      Select which user credentials to use to connect to the source.

      • LOG_ON_SERVICE_USER: Disables

      • LOG_ON_CURRENT_USER: Enables

      One of:

      • LOG_ON_SERVICE_USER

      • LOG_ON_CURRENT_USER
    qMeta: NxMeta
      Information about the connection.
    qModifiedDate: str
      Is generated by the engine.
      Creation date of the connection or last modification date of the connection.
    qName: str
      Name of the connection.
      This parameter is mandatory and must be set when creating or modifying a connection.
    qPassword: str
      Password of the user who creates the connection.
      This parameter is optional; it is only used for OLEDB, ODBC and CUSTOM connections.
      A call to GetConnection Method does not return the password.
    qType: str
      One of:

      • ODBC

      • OLEDB

      • <Name of the custom connection file>

      • folder

      • internet

      Type of the connection.
      This parameter is mandatory and must be set when creating or modifying a connection.
      For ODBC, OLEDB and custom connections, the engine checks that the connection type matches the connection string.
      The type is not case sensitive.
    qUserName: str
      Name of the user who creates the connection.
      This parameter is optional; it is only used for OLEDB, ODBC and CUSTOM connections.
      A call to GetConnection Method does not return the user name.
    """

    qConnectionString: str = None
    qId: str = None
    qLogOn: Literal["LOG_ON_SERVICE_USER", "LOG_ON_CURRENT_USER"] = None
    qMeta: NxMeta = None
    qModifiedDate: str = None
    qName: str = None
    qPassword: str = None
    qType: str = None
    qUserName: str = None

    def __init__(self_, **kvargs):
        if "qConnectionString" in kvargs and kvargs["qConnectionString"] is not None:
            self_.qConnectionString = kvargs["qConnectionString"]
        if "qId" in kvargs and kvargs["qId"] is not None:
            self_.qId = kvargs["qId"]
        if "qLogOn" in kvargs and kvargs["qLogOn"] is not None:
            self_.qLogOn = kvargs["qLogOn"]
        if "qMeta" in kvargs and kvargs["qMeta"] is not None:
            if type(kvargs["qMeta"]).__name__ == Connection.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeta"],
                )
        if "qModifiedDate" in kvargs and kvargs["qModifiedDate"] is not None:
            self_.qModifiedDate = kvargs["qModifiedDate"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qPassword" in kvargs and kvargs["qPassword"] is not None:
            self_.qPassword = kvargs["qPassword"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        if "qUserName" in kvargs and kvargs["qUserName"] is not None:
            self_.qUserName = kvargs["qUserName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ContentLibraryList:
    """

    Attributes
    ----------
    qItems: list[ContentLibraryListItem]
      Information about the content library.
    """

    qItems: list[ContentLibraryListItem] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs and kvargs["qItems"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == ContentLibraryList.__annotations__["qItems"]
                for e in kvargs["qItems"]
            ):
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [
                    ContentLibraryListItem(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qItems"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ContentLibraryListItem:
    """

    Attributes
    ----------
    qAppSpecific: bool
      Is set to true if the library is specific to the app (not a global content library).
    qMeta: NxMeta
      Information about publishing and permissions.
    qName: str
      Name of the library.
    """

    qAppSpecific: bool = None
    qMeta: NxMeta = None
    qName: str = None

    def __init__(self_, **kvargs):
        if "qAppSpecific" in kvargs and kvargs["qAppSpecific"] is not None:
            self_.qAppSpecific = kvargs["qAppSpecific"]
        if "qMeta" in kvargs and kvargs["qMeta"] is not None:
            if (
                type(kvargs["qMeta"]).__name__
                == ContentLibraryListItem.__annotations__["qMeta"]
            ):
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeta"],
                )
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CreateTemporaryBookmarkReturn:
    """

    Attributes
    ----------
    qId: str
    qReturn: bool
    """

    qId: str = None
    qReturn: bool = None

    def __init__(self_, **kvargs):
        if "qId" in kvargs and kvargs["qId"] is not None:
            self_.qId = kvargs["qId"]
        if "qReturn" in kvargs and kvargs["qReturn"] is not None:
            self_.qReturn = kvargs["qReturn"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CustomConnector:
    """

    Attributes
    ----------
    qDisplayName: str
      Name of the custom connector as displayed in the Qlik interface.
    qMachineMode: Literal["CONNECT_DEFAULT", "CONNECT_64", "CONNECT_32"]
      Mode of the machine (64 or 32 bits).

      One of:

      • CONNECT_DEFAULT

      • CONNECT_64

      • CONNECT_32
    qParent: str
      Name of the parent folder that contains the custom connector file.
    qProvider: str
      Name of the custom connector file.
    qSupportFileStreaming: bool
    """

    qDisplayName: str = None
    qMachineMode: Literal["CONNECT_DEFAULT", "CONNECT_64", "CONNECT_32"] = None
    qParent: str = None
    qProvider: str = None
    qSupportFileStreaming: bool = None

    def __init__(self_, **kvargs):
        if "qDisplayName" in kvargs and kvargs["qDisplayName"] is not None:
            self_.qDisplayName = kvargs["qDisplayName"]
        if "qMachineMode" in kvargs and kvargs["qMachineMode"] is not None:
            self_.qMachineMode = kvargs["qMachineMode"]
        if "qParent" in kvargs and kvargs["qParent"] is not None:
            self_.qParent = kvargs["qParent"]
        if "qProvider" in kvargs and kvargs["qProvider"] is not None:
            self_.qProvider = kvargs["qProvider"]
        if (
            "qSupportFileStreaming" in kvargs
            and kvargs["qSupportFileStreaming"] is not None
        ):
            self_.qSupportFileStreaming = kvargs["qSupportFileStreaming"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DataField:
    """

    Attributes
    ----------
    qIsKey: bool
      Is set to true if the field is a primary key.
    qName: str
      Name of the field.
    qOriginalFieldName: str
      Is shown for fixed records.
      qOriginalFieldName and qName are identical if no field names are used in the file.
      qOriginalFieldName differs from qName if embedded file names are used in the file.
    """

    qIsKey: bool = None
    qName: str = None
    qOriginalFieldName: str = None

    def __init__(self_, **kvargs):
        if "qIsKey" in kvargs and kvargs["qIsKey"] is not None:
            self_.qIsKey = kvargs["qIsKey"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qOriginalFieldName" in kvargs and kvargs["qOriginalFieldName"] is not None:
            self_.qOriginalFieldName = kvargs["qOriginalFieldName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DataRecord:
    """

    Attributes
    ----------
    qValues: list[str]
      List of values inside the table.
      The first values (in result/qPreview/0/qValues ) correspond to the field names in the table.
      The following values (from result/qPreview/1/qValues ) are the values of the fields in the table.
    """

    qValues: list[str] = None

    def __init__(self_, **kvargs):
        if "qValues" in kvargs and kvargs["qValues"] is not None:
            self_.qValues = kvargs["qValues"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DataTable:
    """

    Attributes
    ----------
    qName: str
      Name of the table.
    qType: str
      Type of the table.
      For example: Table or View.
    """

    qName: str = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DataTableEx:
    """

    Attributes
    ----------
    qFields: list[DataField]
      List of the fields in the table.
    qFormatSpec: str
      List of format specification items, within brackets.
      Examples of specification items:

      • file type

      • embedded labels, no labels

      • table is <table name>
    qName: str
      Name of the table.
    """

    qFields: list[DataField] = None
    qFormatSpec: str = None
    qName: str = None

    def __init__(self_, **kvargs):
        if "qFields" in kvargs and kvargs["qFields"] is not None:
            if all(
                f"list[{type(e).__name__}]" == DataTableEx.__annotations__["qFields"]
                for e in kvargs["qFields"]
            ):
                self_.qFields = kvargs["qFields"]
            else:
                self_.qFields = [
                    DataField(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qFields"]
                ]
        if "qFormatSpec" in kvargs and kvargs["qFormatSpec"] is not None:
            self_.qFormatSpec = kvargs["qFormatSpec"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Database:
    """

    Attributes
    ----------
    qIsDefault: bool
      Is set to true if the database is set by default.
    qName: str
      Name of the database.
    """

    qIsDefault: bool = None
    qName: str = None

    def __init__(self_, **kvargs):
        if "qIsDefault" in kvargs and kvargs["qIsDefault"] is not None:
            self_.qIsDefault = kvargs["qIsDefault"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DatabaseInfo:
    """

    Attributes
    ----------
    qDBFirst: bool
      If set to true, it means that the database is displayed first, before the owners and tables.
    qDBMSName: str
      Name of the product accessed by the provider.
    qDBSeparator: str
      Character string used after the database name.
      Example with separator " . ":
      FROM LinkedTablesData.dbo.Months
      Where:

      • LinkedTablesData is the database name

      • dbo is the owner name

      • Months is the table name
    qDBUsage: bool
      If set to true, it means that the data source contains some databases.
    qDefaultDatabase: str
      Name of the default database.
    qKeywords: list[str]
      List of the script keywords.
    qOwnerSeparator: str
      Character string used after the owner name.
      Example with separator " . ":
      FROM LinkedTablesData.dbo.Months
      Where:

      • LinkedTablesData is the database name

      • dbo is the owner name

      • Months is the table name
    qOwnerUsage: bool
      If set to true, it means that the data source contains some owners.
    qQuotePreffix: str
      Prefix used with field, database or owner names that contain special characters or keywords.
    qQuoteSuffix: str
      Suffix used with field, database or owner names that contain special characters or keywords.
    qSpecialChars: str
      List of the special characters.
    """

    qDBFirst: bool = None
    qDBMSName: str = None
    qDBSeparator: str = None
    qDBUsage: bool = None
    qDefaultDatabase: str = None
    qKeywords: list[str] = None
    qOwnerSeparator: str = None
    qOwnerUsage: bool = None
    qQuotePreffix: str = None
    qQuoteSuffix: str = None
    qSpecialChars: str = None

    def __init__(self_, **kvargs):
        if "qDBFirst" in kvargs and kvargs["qDBFirst"] is not None:
            self_.qDBFirst = kvargs["qDBFirst"]
        if "qDBMSName" in kvargs and kvargs["qDBMSName"] is not None:
            self_.qDBMSName = kvargs["qDBMSName"]
        if "qDBSeparator" in kvargs and kvargs["qDBSeparator"] is not None:
            self_.qDBSeparator = kvargs["qDBSeparator"]
        if "qDBUsage" in kvargs and kvargs["qDBUsage"] is not None:
            self_.qDBUsage = kvargs["qDBUsage"]
        if "qDefaultDatabase" in kvargs and kvargs["qDefaultDatabase"] is not None:
            self_.qDefaultDatabase = kvargs["qDefaultDatabase"]
        if "qKeywords" in kvargs and kvargs["qKeywords"] is not None:
            self_.qKeywords = kvargs["qKeywords"]
        if "qOwnerSeparator" in kvargs and kvargs["qOwnerSeparator"] is not None:
            self_.qOwnerSeparator = kvargs["qOwnerSeparator"]
        if "qOwnerUsage" in kvargs and kvargs["qOwnerUsage"] is not None:
            self_.qOwnerUsage = kvargs["qOwnerUsage"]
        if "qQuotePreffix" in kvargs and kvargs["qQuotePreffix"] is not None:
            self_.qQuotePreffix = kvargs["qQuotePreffix"]
        if "qQuoteSuffix" in kvargs and kvargs["qQuoteSuffix"] is not None:
            self_.qQuoteSuffix = kvargs["qQuoteSuffix"]
        if "qSpecialChars" in kvargs and kvargs["qSpecialChars"] is not None:
            self_.qSpecialChars = kvargs["qSpecialChars"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DatabaseOwner:
    """

    Attributes
    ----------
    qName: str
      Name of the owner.
    """

    qName: str = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DelimiterInfo:
    """

    Attributes
    ----------
    qIsMultiple: bool
      Is set to true if multiple spaces are used to separate the values.
    qName: str
      Name of the delimiter.
      Example:
      "Tab_DELIMITER"
    qNumber: int
      Delimiter character number used by the engine to determine how to separate the values.
    qScriptCode: str
      Representation of the delimiter value that is used in the script.
      Example:
      "'\t'"
    """

    qIsMultiple: bool = None
    qName: str = None
    qNumber: int = None
    qScriptCode: str = None

    def __init__(self_, **kvargs):
        if "qIsMultiple" in kvargs and kvargs["qIsMultiple"] is not None:
            self_.qIsMultiple = kvargs["qIsMultiple"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qNumber" in kvargs and kvargs["qNumber"] is not None:
            self_.qNumber = kvargs["qNumber"]
        if "qScriptCode" in kvargs and kvargs["qScriptCode"] is not None:
            self_.qScriptCode = kvargs["qScriptCode"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DerivedFieldsInTableData:
    """

    Attributes
    ----------
    qActive: bool
      Is set to true is the derived field is in use.
    qDefinitionName: str
      Name of the derived definition.
    qTags: list[str]
      List of tags.
    """

    qActive: bool = None
    qDefinitionName: str = None
    qTags: list[str] = None

    def __init__(self_, **kvargs):
        if "qActive" in kvargs and kvargs["qActive"] is not None:
            self_.qActive = kvargs["qActive"]
        if "qDefinitionName" in kvargs and kvargs["qDefinitionName"] is not None:
            self_.qDefinitionName = kvargs["qDefinitionName"]
        if "qTags" in kvargs and kvargs["qTags"] is not None:
            self_.qTags = kvargs["qTags"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DimensionList:
    """
    Lists the dimensions. Is the layout for DimensionListDef.

    Attributes
    ----------
    qItems: list[NxContainerEntry]
      Information about the list of dimensions.
    """

    qItems: list[NxContainerEntry] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs and kvargs["qItems"] is not None:
            if all(
                f"list[{type(e).__name__}]" == DimensionList.__annotations__["qItems"]
                for e in kvargs["qItems"]
            ):
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [
                    NxContainerEntry(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qItems"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DimensionListDef:
    """
    Defines the lists of dimensions.

    Attributes
    ----------
    qData: JsonObject
      Data
    qType: str
      Type of the list.
    """

    qData: JsonObject = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qData" in kvargs and kvargs["qData"] is not None:
            if (
                type(kvargs["qData"]).__name__
                == DimensionListDef.__annotations__["qData"]
            ):
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qData"],
                )
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DoReloadExParams:
    """
    Parameters for a reload.

    Attributes
    ----------
    qDebug: bool
      Set to true to debug reload.
      The default value is false.
    qMode: int
      0: for default mode.
      1: for ABEND; the reload of the script ends if an error occurs.
      2: for ignore; the reload of the script continues even if an error is detected in the script.
    qPartial: bool
      Set to true for partial reload.
      The default value is false.
    qReloadId: str
      Optional reload ID.
      ID will be automatically generated if not set.
    qRowLimit: int
      If greater than or equal 0, defines max number of rows loaded from a data source.
    qSkipStore: bool
      Set to true to skip Store statements.
      The default value is false.
    """

    qDebug: bool = None
    qMode: int = None
    qPartial: bool = None
    qReloadId: str = None
    qRowLimit: int = -1
    qSkipStore: bool = None

    def __init__(self_, **kvargs):
        if "qDebug" in kvargs and kvargs["qDebug"] is not None:
            self_.qDebug = kvargs["qDebug"]
        if "qMode" in kvargs and kvargs["qMode"] is not None:
            self_.qMode = kvargs["qMode"]
        if "qPartial" in kvargs and kvargs["qPartial"] is not None:
            self_.qPartial = kvargs["qPartial"]
        if "qReloadId" in kvargs and kvargs["qReloadId"] is not None:
            self_.qReloadId = kvargs["qReloadId"]
        if "qRowLimit" in kvargs and kvargs["qRowLimit"] is not None:
            self_.qRowLimit = kvargs["qRowLimit"]
        if "qSkipStore" in kvargs and kvargs["qSkipStore"] is not None:
            self_.qSkipStore = kvargs["qSkipStore"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DoReloadExResult:
    """
    The result and path to script log for a reload.

    Attributes
    ----------
    qEndedWithMemoryConstraint: bool
      true if memory limits were exhausted during reload.
    qScriptLogFile: str
      Path to the script log file.
    qSuccess: bool
      The reload is successful if True.
    """

    qEndedWithMemoryConstraint: bool = None
    qScriptLogFile: str = None
    qSuccess: bool = None

    def __init__(self_, **kvargs):
        if (
            "qEndedWithMemoryConstraint" in kvargs
            and kvargs["qEndedWithMemoryConstraint"] is not None
        ):
            self_.qEndedWithMemoryConstraint = kvargs["qEndedWithMemoryConstraint"]
        if "qScriptLogFile" in kvargs and kvargs["qScriptLogFile"] is not None:
            self_.qScriptLogFile = kvargs["qScriptLogFile"]
        if "qSuccess" in kvargs and kvargs["qSuccess"] is not None:
            self_.qSuccess = kvargs["qSuccess"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Doc:
    """

    Attributes
    ----------
    qGenericId: str
      Object ID.
    qGenericType: str
      The type of the object.
    qHandle: int
      The handle used to connect to object.
    qType: str
      The native type of the object.
    """

    _session: RpcSession = None
    qGenericId: str = None
    qGenericType: str = None
    qHandle: int = None
    qType: str = None
    Global: Global = None

    def get_field(self, qFieldName: str, qStateName: str = None) -> Field:
        """
        Returns a handle to a field.

        Parameters
        ----------
        qFieldName: str
          Name of the field.
        qStateName: str = None
          Name of the alternate state.
          Default state is current selections.
        """
        params = {}
        params["qFieldName"] = qFieldName
        if qStateName is not None:
            params["qStateName"] = qStateName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetField", handle, **params)["qReturn"]
        obj = Field(_session=self._session, **response)
        return obj

    def get_field_description(self, qFieldName: str) -> FieldDescription:
        """
        Returns the description of a field.

        Parameters
        ----------
        qFieldName: str
          Name of the field.
        """
        params = {}
        params["qFieldName"] = qFieldName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFieldDescription", handle, **params)[
            "qReturn"
        ]
        obj = FieldDescription(**response)
        return obj

    def get_variable(self, qName: str) -> GenericVariable:
        """
        Returns a handle to a variable.

        Parameters
        ----------
        qName: str
          Name of the variable.
        """
        warnings.warn("GetVariable is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qName"] = qName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetVariable", handle, **params)["qReturn"]
        obj = GenericVariable(_session=self._session, **response)
        return obj

    def get_loosely_coupled_vector(self) -> list[int]:
        """
        Returns a list of table states.

        The following states apply:

        • 0 The table is not loosely coupled.

        • 1 The table is loosely coupled.

        • 2 The table is loosely coupled and cannot be changed to another state using the Qlik Engine API.

        The last three values in the vector are for internal use.
        In case of circular references, the engine automatically sets the table state to loosely coupled to avoid creating loops.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLooselyCoupledVector", handle)["qv"]
        return response

    def set_loosely_coupled_vector(self, qv: list[int]) -> bool:
        """
        Sets a list of table states, one for each table.

        The following states apply:

        • 0 The table is not loosely coupled.

        • 1 The table is loosely coupled.

        • 2 The table is loosely coupled and cannot be changed to another state using the Qlik Engine API.

        The last three values in the vector are for internal use.

        Parameters
        ----------
        qv: list[int]
          The list of table states to set. A state will not be changed if already set to 2.
        """
        params = {}
        params["qv"] = qv
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetLooselyCoupledVector", handle, **params)[
            "qReturn"
        ]
        return response

    def evaluate(self, qExpression: str) -> str:
        """
        Evaluates an expression and returns the result as a string.

         Example:
        The client sends:
        ```
        {
            "handle": 1,
            "method": "Evaluate",
            "params": {
                "qExpression": "Sum(Holes)"
            },
            "id": 6,
            "jsonrpc": "2.0"
        }
        ```
        The engine returns:
        ```
        {
            "jsonrpc": "2.0",
            "id": 6,
            "result": {
                "qReturn": "361716"
            }
        }
        ```

        Parameters
        ----------
        qExpression: str
          Expression to evaluate.
        """
        params = {}
        params["qExpression"] = qExpression
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Evaluate", handle, **params)["qReturn"]
        return response

    def evaluate_ex(self, qExpression: str) -> FieldValue:
        """
        Evaluates an expression and returns the result as a dual.

         Example:
        The client sends:
        ```
        {
            "handle": 1,
            "method": "EvaluateEx",
            "params": {
                "qExpression": "Sum(Holes)"
            },
            "id": 7,
            "jsonrpc": "2.0"
        }
        ```
        The engine returns:
        ```
        {
            "jsonrpc": "2.0",
            "id": 7,
            "result": {
                "qReturn": "361716"
            }
        }
        ```

        Parameters
        ----------
        qExpression: str
          Expression to evaluate.
        """
        params = {}
        params["qExpression"] = qExpression
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("EvaluateEx", handle, **params)["qValue"]
        obj = FieldValue(**response)
        return obj

    def clear_all(self, qLockedAlso: bool = None, qStateName: str = None) -> object:
        """
        Clear selections in fields for current state. Locked fields are not cleared by default.

        Parameters
        ----------
        qLockedAlso: bool = None
          When true, clears the selection for locked fields.
        qStateName: str = None
          Alternate state name. When set, applies to alternate state instead of current
        """
        params = {}
        if qLockedAlso is not None:
            params["qLockedAlso"] = qLockedAlso
        if qStateName is not None:
            params["qStateName"] = qStateName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ClearAll", handle, **params)
        return response

    def lock_all(self, qStateName: str = None) -> object:
        """
        Locks all selections in fields for current state.

        Parameters
        ----------
        qStateName: str = None
          Alternate state name. When set, applies to alternate state instead of current.
        """
        params = {}
        if qStateName is not None:
            params["qStateName"] = qStateName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("LockAll", handle, **params)
        return response

    def unlock_all(self, qStateName: str = None) -> object:
        """
        Unlocks all selections in fields for current state.

        Parameters
        ----------
        qStateName: str = None
          Alternate state name. When set, applies to alternate state instead of current.
        """
        params = {}
        if qStateName is not None:
            params["qStateName"] = qStateName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnlockAll", handle, **params)
        return response

    def back(self) -> object:
        """
        Loads the last logical operation (if any).

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Back", handle)
        return response

    def forward(self) -> object:
        """
        Loads the next logical operation (if any).

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Forward", handle)
        return response

    def create_variable(self, qName: str) -> bool:
        """
        Creates a variable.

        Parameters
        ----------
        qName: str
          Name of the variable. Variable names are case sensitive.
        """
        warnings.warn("CreateVariable is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qName"] = qName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateVariable", handle, **params)["qReturn"]
        return response

    def remove_variable(self, qName: str) -> bool:
        """
        Removes a variable.

        Parameters
        ----------
        qName: str
          Name of the variable. Variable names are case sensitive.
        """
        warnings.warn("RemoveVariable is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qName"] = qName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("RemoveVariable", handle, **params)["qReturn"]
        return response

    def get_locale_info(self) -> LocaleInfo:
        """
        Returns locale information.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLocaleInfo", handle)["qReturn"]
        obj = LocaleInfo(**response)
        return obj

    def get_tables_and_keys(
        self,
        qWindowSize: Size,
        qNullSize: Size,
        qCellHeight: int,
        qSyntheticMode: bool,
        qIncludeSysVars: bool,
        qIncludeProfiling: bool = None,
    ) -> GetTablesAndKeysReturn:
        """
        Returns:

        • The list of tables in an app and the fields inside each table.

        • The list of derived fields.

        • The list of key fields.

        Parameters
        ----------
        qWindowSize: Size
          Size of the window that is used to display the results.
        qNullSize: Size
        qCellHeight: int
          Height of a cell in a table in pixels.
        qSyntheticMode: bool
          One of:

          • true for internal table viewer:
          Shows a more detailed view on how the Qlik engine defines the relations between fields and the quality of the keys.

          • false for source table viewer:
          Shows the natural relation between fields without reference to synthetic keys and resultant linking synthetic tables. Instead synthetic keys are represented by multiple connectors between tables.
        qIncludeSysVars: bool
          If set to true, the system variables are included.
        qIncludeProfiling: bool = None
          If set to true, profiling information is included.
        """
        params = {}
        params["qWindowSize"] = qWindowSize
        params["qNullSize"] = qNullSize
        params["qCellHeight"] = qCellHeight
        params["qSyntheticMode"] = qSyntheticMode
        params["qIncludeSysVars"] = qIncludeSysVars
        if qIncludeProfiling is not None:
            params["qIncludeProfiling"] = qIncludeProfiling
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetTablesAndKeys", handle, **params)
        obj = GetTablesAndKeysReturn(**response)
        return obj

    def get_view_dlg_save_info(self) -> TableViewDlgSaveInfo:
        """
        Returns information about the position of the tables in the data model viewer.
        The position of the broom points and the position of the connection points cannot be retrieved in Qlik Sense.

         Representation of tables, broom points and connection points:

        The green circles represent the broom points.
        The red circle represents a connection point.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetViewDlgSaveInfo", handle)["qReturn"]
        obj = TableViewDlgSaveInfo(**response)
        return obj

    def set_view_dlg_save_info(self, qInfo: TableViewDlgSaveInfo) -> object:
        """
        Sets the positions of the tables in the data model viewer.
        The position of the broom points and the position of the connection points cannot be set in Qlik Sense.

         Representation of tables, broom points and connection points:

        The green circles represent the broom points.
        The red circle represents a connection point.

        Parameters
        ----------
        qInfo: TableViewDlgSaveInfo
          Information about the table.
        """
        params = {}
        params["qInfo"] = qInfo
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetViewDlgSaveInfo", handle, **params)
        return response

    def get_empty_script(self, qLocalizedMainSection: str = None) -> str:
        """
        Creates a script that contains one section. This section contains SET statements that give localized information from the regional settings of the computer.
        The computer regional settings are retrieved when the engine starts.

        Parameters
        ----------
        qLocalizedMainSection: str = None
          Name of the script section.
          The default value is Main .
        """
        params = {}
        if qLocalizedMainSection is not None:
            params["qLocalizedMainSection"] = qLocalizedMainSection
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetEmptyScript", handle, **params)["qReturn"]
        return response

    def do_reload(
        self, qMode: int = None, qPartial: bool = None, qDebug: bool = None
    ) -> bool:
        """
        Reloads the script that is set in an app.

         Logs:
        When this method is called, audit activity logs are produced to track the user activity.
        In the case of errors, both audit activity logs and system services logs are produced.
        The log files are named as follows:
        | Audit activity log                                                                                                                        | System service log                                                                                                            |
        |-------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
        | _\_AuditActivity\_Engine.txt_ in Qlik Sense Enterprise  _\_AuditActivity\_Engine.log_ in Qlik Sense Desktop | _\_Service\_Engine.txt_ in Qlik Sense Enterprise  _\_Service\_Engine.log_ in Qlik Sense Desktop |

         Where to find the log files:
        The location of the log files depends on whether you have installed Qlik Sense Enterprise or Qlik Sense Desktop.
        | Qlik Sense Enterprise                 | Qlik Sense Desktop                       |
        |---------------------------------------|------------------------------------------|
        | _%ProgramData%/Qlik/Sense/Log/Engine_ | _%UserProfile%/Documents/Qlik/Sense/Log_ |

        Parameters
        ----------
        qMode: int = None
          Error handling mode
          One of:

          • 0: for default mode.

          • 1: for ABEND; the reload of the script ends if an error occurs.

          • 2: for ignore; the reload of the script continues even if an error is detected in the script.
        qPartial: bool = None
          Set to true for partial reload.
          The default value is false.
        qDebug: bool = None
          Set to true if debug breakpoints are to be honored. The execution of the script will be in debug mode.
          The default value is false.
        """
        params = {}
        if qMode is not None:
            params["qMode"] = qMode
        if qPartial is not None:
            params["qPartial"] = qPartial
        if qDebug is not None:
            params["qDebug"] = qDebug
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DoReload", handle, **params)["qReturn"]
        return response

    def get_script_breakpoints(self) -> list[EditorBreakpoint]:
        """
        Lists the breakpoints in the script of an app.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetScriptBreakpoints", handle)["qBreakpoints"]
        return [EditorBreakpoint(**e) for e in response]

    def set_script_breakpoints(self, qBreakpoints: list[EditorBreakpoint]) -> object:
        """
        Set some breakpoints in the script of an app.

        Parameters
        ----------
        qBreakpoints: list[EditorBreakpoint]
          Information about the breakpoints.
        """
        params = {}
        params["qBreakpoints"] = qBreakpoints
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetScriptBreakpoints", handle, **params)
        return response

    def get_script(self) -> str:
        """
        Gets values in script.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetScript", handle)["qScript"]
        return response

    def get_text_macros(self) -> list[TextMacro]:
        """
        Fetches updated variables after a statement execution.

        If qRefSeqNo and qSetSeqNo are set to 0, it means that the variables were not updated.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetTextMacros", handle)["qMacros"]
        return [TextMacro(**e) for e in response]

    def set_fetch_limit(self, qLimit: int) -> object:
        """
        Limits the number of rows of data to load from a data source.
        This method works when reloading in debug mode.

        Parameters
        ----------
        qLimit: int
          Fetch limit.
          Number of rows to load.
        """
        params = {}
        params["qLimit"] = qLimit
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetFetchLimit", handle, **params)
        return response

    def do_save(self, qFileName: str = None) -> object:
        """
        Saves an app. All objects and data in the data model are saved.

        Parameters
        ----------
        qFileName: str = None
          Name of the file to save.
        """
        params = {}
        if qFileName is not None:
            params["qFileName"] = qFileName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DoSave", handle, **params)
        return response

    def get_table_data(
        self, qOffset: int, qRows: int, qSyntheticMode: bool, qTableName: str
    ) -> list[TableRow]:
        """
        Retrieves the data of a specific table.

        Parameters
        ----------
        qOffset: int
          Position from the top, starting from 0.
          If the offset is set to 0, the rows starting from the position/index 0 are shown.
        qRows: int
          Number of rows to show.
        qSyntheticMode: bool
          If this parameter is set to true, the internal data/table representation is shown. Synthetic fields are present (if any).
        qTableName: str
          Name of the table.
        """
        params = {}
        params["qOffset"] = qOffset
        params["qRows"] = qRows
        params["qSyntheticMode"] = qSyntheticMode
        params["qTableName"] = qTableName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetTableData", handle, **params)["qData"]
        return [TableRow(**e) for e in response]

    def get_app_layout(self) -> NxAppLayout:
        """
        Evaluates an app.
        Returns dynamic properties (if any) in addition to the engine (fixed) properties.
        A data set is returned.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetAppLayout", handle)["qLayout"]
        obj = NxAppLayout(**response)
        return obj

    def set_app_properties(self, qProp: NxAppProperties) -> object:
        """
        Sets properties to an app.
        The qLastReloadTime, qMigrationHash and qSavedInProductVersion properties does not need to be set but if they are, they should match the current values in the app layout.

        Parameters
        ----------
        qProp: NxAppProperties
          Information about the properties of an app.
        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetAppProperties", handle, **params)
        return response

    def get_app_properties(self) -> NxAppProperties:
        """
        Gets the properties of an app.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetAppProperties", handle)["qProp"]
        obj = NxAppProperties(**response)
        return obj

    def get_lineage(self) -> list[LineageInfo]:
        """
        Gets the lineage information of the app. The lineage information includes the LOAD and STORE statements from the data load script associated with this app.
        An array of lineage information.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLineage", handle)["qLineage"]
        return [LineageInfo(**e) for e in response]

    def create_session_object(self, qProp: GenericObjectProperties) -> GenericObject:
        """
        Creates a transient object. For example, you can use a transient object to create an app overview or a story overview.
        It is possible to create a transient object that is linked to another object.
        A linked object is an object that points to a linking object. The linking object is defined in the properties of the linked object (in qExtendsId ).
        The linked object has the same properties as the linking object.
        The linking object cannot be a transient object.

        Parameters
        ----------
        qProp: GenericObjectProperties
          Information about the object.
        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateSessionObject", handle, **params)[
            "qReturn"
        ]
        obj = GenericObject(_session=self._session, **response)
        return obj

    def destroy_session_object(self, qId: str) -> bool:
        """
        Removes a transient object.

        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        qId: str
          Identifier of the transient object to remove.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroySessionObject", handle, **params)[
            "qSuccess"
        ]
        return response

    def create_object(self, qProp: GenericObjectProperties) -> GenericObject:
        """
        Creates a generic object at app level. For more information on generic objects, see Generic object.
        It is possible to create a generic object that is linked to another object.
        A linked object is an object that points to a linking object. The linking object is defined in the properties of the linked object (in qExtendsId ).
        The linked object has the same properties as the linking object.
        The linking object cannot be a transient object.

        Parameters
        ----------
        qProp: GenericObjectProperties
          Information about the object.
        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateObject", handle, **params)["qReturn"]
        obj = GenericObject(_session=self._session, **response)
        return obj

    def destroy_object(self, qId: str) -> bool:
        """
        Removes an app object.
        The children of the object (if any) are removed as well.

        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        qId: str
          Identifier of the object to remove.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyObject", handle, **params)["qSuccess"]
        return response

    def get_object(self, qId: str) -> GenericObject:
        """
        Returns the type of the app object and the corresponding handle.

        Parameters
        ----------
        qId: str
          Identifier of the object to retrieve.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetObject", handle, **params)["qReturn"]
        obj = GenericObject(_session=self._session, **response)
        return obj

    def get_objects(self, qOptions: NxGetObjectOptions) -> list[NxContainerEntry]:
        """
        Returns all objects compatible with options.

        Parameters
        ----------
        qOptions: NxGetObjectOptions
          Object type filter and requested properties.
        """
        params = {}
        params["qOptions"] = qOptions
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetObjects", handle, **params)["qList"]
        return [NxContainerEntry(**e) for e in response]

    def get_bookmarks(self, qOptions: NxGetBookmarkOptions) -> list[NxContainerEntry]:
        """
        Returns all bookmarks compatible with options.

        Parameters
        ----------
        qOptions: NxGetBookmarkOptions
          Bookmark type filter and requested properties.
        """
        params = {}
        params["qOptions"] = qOptions
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetBookmarks", handle, **params)["qList"]
        return [NxContainerEntry(**e) for e in response]

    def clone_object(self, qId: str) -> str:
        """
        Clones root level objects, such as sheets and stories. The CloneObject method works for both app objects and child objects.
        When you clone an object that contains children, the children are cloned as well.
        If you for example want to clone a visualization, you must provide the qID of the root object, in this case the sheet since CloneObject clones root level objects.
        It is not possible to clone a session object.

        The identifier is set by the engine.

        Parameters
        ----------
        qId: str
          Identifier of the object to clone. The identifier must be a root object.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CloneObject", handle, **params)["qCloneId"]
        return response

    def create_draft(self, qId: str) -> str:
        """
        Creates a draft of an object.
        This method can be used to create a draft of a sheet or a story that is published. This is a way to continue working on a sheet or a story that is published.
        Replace the published object by the content of the draft by invoking the CommitDraft method.

        The identifier is set by the engine.

        Parameters
        ----------
        qId: str
          Identifier of the object to create a draft from.
        """
        warnings.warn("CreateDraft is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateDraft", handle, **params)["qDraftId"]
        return response

    def commit_draft(self, qId: str) -> object:
        """
        Commits the draft of an object that was previously created by invoking the CreateDraft method.
        Committing a draft replaces the corresponding published object.

        Parameters
        ----------
        qId: str
          Identifier of the draft to commit.
        """
        warnings.warn("CommitDraft is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CommitDraft", handle, **params)
        return response

    def destroy_draft(self, qId: str, qSourceId: str) -> bool:
        """
        Removes the draft of an object.
        The children of the draft object (if any) are removed as well.
        This method can be used to cancel the work on the draft of an object. For example, if you had created a draft of a sheet that is published, you might not want anymore to replace the published sheet.

        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        qId: str
          Identifier of the draft object to remove.
        qSourceId: str
          Identifier of the source object (the object from which a draft was created).
        """
        warnings.warn("DestroyDraft is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qId"] = qId
        params["qSourceId"] = qSourceId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyDraft", handle, **params)["qSuccess"]
        return response

    def undo(self) -> bool:
        """
        Undoes the previous operation.

        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Undo", handle)["qSuccess"]
        return response

    def redo(self) -> bool:
        """
        Redoes the previous operation.

        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Redo", handle)["qSuccess"]
        return response

    def clear_undo_buffer(self) -> object:
        """
        Clears entirely the undo and redo buffer.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ClearUndoBuffer", handle)
        return response

    def create_dimension(self, qProp: GenericDimensionProperties) -> GenericDimension:
        """
        Creates a master dimension.
        A master dimension is stored in the library of an app and can be used in many objects. Several generic objects can contain the same dimension.

        Parameters
        ----------
        qProp: GenericDimensionProperties
          Information about the properties.
        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateDimension", handle, **params)["qReturn"]
        obj = GenericDimension(_session=self._session, **response)
        return obj

    def destroy_dimension(self, qId: str) -> bool:
        """
        Removes a dimension.

        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        qId: str
          Identifier of the dimension to remove.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyDimension", handle, **params)["qSuccess"]
        return response

    def get_dimension(self, qId: str) -> GenericDimension:
        """
        Returns the handle of a dimension.

        Parameters
        ----------
        qId: str
          Identifier of the dimension.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDimension", handle, **params)["qReturn"]
        obj = GenericDimension(_session=self._session, **response)
        return obj

    def clone_dimension(self, qId: str) -> str:
        """
        Clones a dimension.

        The identifier is set by the engine.

        Parameters
        ----------
        qId: str
          Identifier of the object to clone.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CloneDimension", handle, **params)["qCloneId"]
        return response

    def create_measure(self, qProp: GenericMeasureProperties) -> GenericMeasure:
        """
        Creates a master measure.
        A master measure is stored in the library of an app and can be used in many objects. Several generic objects can contain the same measure.

        Parameters
        ----------
        qProp: GenericMeasureProperties
          Information about the properties.
        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateMeasure", handle, **params)["qReturn"]
        obj = GenericMeasure(_session=self._session, **response)
        return obj

    def destroy_measure(self, qId: str) -> bool:
        """
        Removes a generic measure.

        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        qId: str
          Identifier of the measure to remove.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyMeasure", handle, **params)["qSuccess"]
        return response

    def get_measure(self, qId: str) -> GenericMeasure:
        """
        Returns the handle of a measure.

        Parameters
        ----------
        qId: str
          Identifier of the measure.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetMeasure", handle, **params)["qReturn"]
        obj = GenericMeasure(_session=self._session, **response)
        return obj

    def clone_measure(self, qId: str) -> str:
        """
        Clones a measure.

        The identifier is set by the engine.

        Parameters
        ----------
        qId: str
          Identifier of the object to clone.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CloneMeasure", handle, **params)["qCloneId"]
        return response

    def create_session_variable(
        self, qProp: GenericVariableProperties
    ) -> GenericVariable:
        """
        Creates a transient variable.
        To set some properties to the variable, use the SetProperties method.

         Definition:
        A variable in Qlik Sense is a named entity, containing a data value. This value can be static or be the result of a calculation. A variable acquires its value at the same time that the variable is created or after when updating the properties of the variable. Variables can be used in bookmarks and can contain numeric or alphanumeric data. Any change made to the variable is applied everywhere the variable is used.
        When a variable is used in an expression, it is substituted by its value or the variable's definition.

         Example:
        The variable x contains the text string Sum(Sales) .
        In a chart, you define the expression $(x)/12 . The effect is exactly the same as having the chart expression Sum(Sales)/12 .
        However, if you change the value of the variable x to Sum(Budget) , the data in the chart are immediately recalculated with the expression interpreted as Sum(Budget)/12 .

        Parameters
        ----------
        qProp: GenericVariableProperties
          Name of the variable. Variable names are case sensitive.
        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateSessionVariable", handle, **params)[
            "qReturn"
        ]
        obj = GenericVariable(_session=self._session, **response)
        return obj

    def destroy_session_variable(self, qId: str) -> bool:
        """
        Removes a transient variable.

        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        qId: str
          Identifier of the variable.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroySessionVariable", handle, **params)[
            "qSuccess"
        ]
        return response

    def create_variable_ex(self, qProp: GenericVariableProperties) -> GenericVariable:
        """
        Creates a variable.
        To create a variable via a script, you need to use the SetScript method. For more information, see Create a variable.
        To set some properties to the variable, use the SetProperties method.  In a published app, only transient variables can be created. See CreateSessionVariable method.

         Definition:
        A variable in Qlik Sense is a named entity, containing a data value. This value can be static or be the result of a calculation. A variable acquires its value at the same time that the variable is created or after when updating the properties of the variable. Variables can be used in bookmarks and can contain numeric or alphanumeric data. Any change made to the variable is applied everywhere the variable is used.
        When a variable is used in an expression, it is substituted by its value or the variable's definition.

         Example:
        The variable x contains the text string Sum(Sales) .
        In a chart, you define the expression $(x)/12 . The effect is exactly the same as having the chart expression Sum(Sales)/12 .
        However, if you change the value of the variable x to Sum(Budget) , the data in the chart are immediately recalculated with the expression interpreted as Sum(Budget)/12 .

        Parameters
        ----------
        qProp: GenericVariableProperties
          Name of the variable. Variable names are case sensitive and must be unique.
        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateVariableEx", handle, **params)["qReturn"]
        obj = GenericVariable(_session=self._session, **response)
        return obj

    def destroy_variable_by_id(self, qId: str) -> bool:
        """
        Removes a variable.
        Script-defined variables cannot be removed using the DestroyVariableById method or the DestroyVariableByName method. For more information, see Remove a variable.

        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        qId: str
          Identifier of the variable.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyVariableById", handle, **params)[
            "qSuccess"
        ]
        return response

    def destroy_variable_by_name(self, qName: str) -> bool:
        """
        Removes a variable.
        Script-defined variables cannot be removed using the DestroyVariableById method or the DestroyVariableByName method. For more information, see Remove a variable.

        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        qName: str
          Name of the variable.
        """
        params = {}
        params["qName"] = qName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyVariableByName", handle, **params)[
            "qSuccess"
        ]
        return response

    def get_variable_by_id(self, qId: str) -> GenericVariable:
        """
        Gets the handle of a variable.

        Parameters
        ----------
        qId: str
          Identifier of the variable.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetVariableById", handle, **params)["qReturn"]
        obj = GenericVariable(_session=self._session, **response)
        return obj

    def get_variable_by_name(self, qName: str) -> GenericVariable:
        """
        Gets the handle of a variable.

        Parameters
        ----------
        qName: str
          Name of the variable.
        """
        params = {}
        params["qName"] = qName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetVariableByName", handle, **params)["qReturn"]
        obj = GenericVariable(_session=self._session, **response)
        return obj

    def check_expression(
        self, qExpr: str, qLabels: list[str] = None
    ) -> CheckExpressionReturn:
        """
        Checks if a given expression is valid.
        The expression is correct if the parameters qErrorMsg , qBadFieldNames and qDangerousFieldNames are empty.

        Parameters
        ----------
        qExpr: str
          Expression to check.
        qLabels: list[str] = None
          List of labels.
        """
        params = {}
        params["qExpr"] = qExpr
        if qLabels is not None:
            params["qLabels"] = qLabels
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CheckExpression", handle, **params)
        obj = CheckExpressionReturn(**response)
        return obj

    def check_number_or_expression(self, qExpr: str) -> CheckNumberOrExpressionReturn:
        """
        Checks if:

        • A given expression is valid.

        • A number is correct according to the locale.

        Parameters
        ----------
        qExpr: str
          Expression to check.
        """
        params = {}
        params["qExpr"] = qExpr
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CheckNumberOrExpression", handle, **params)
        obj = CheckNumberOrExpressionReturn(**response)
        return obj

    def add_alternate_state(self, qStateName: str) -> object:
        """
        Adds an alternate state in the app.
        You can create multiple states within a Qlik Sense app and apply these states to specific objects within the app. Objects in a given state are not affected by user selections in the other states.

        Parameters
        ----------
        qStateName: str
          Name of the alternate state.
        """
        params = {}
        params["qStateName"] = qStateName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AddAlternateState", handle, **params)
        return response

    def remove_alternate_state(self, qStateName: str) -> object:
        """
        Removes an alternate state in the app.

        Parameters
        ----------
        qStateName: str
          Name of the alternate state.
        """
        params = {}
        params["qStateName"] = qStateName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("RemoveAlternateState", handle, **params)
        return response

    def add_session_alternate_state(
        self, qStateName: str, qSourceStateName: str = None
    ) -> object:
        """
        Adds an session alternate state in the app.
        You can create multiple states within a Qlik Sense app and apply these states to specific objects within the app. Objects in a given state are not affected by user selections in the other states.
        A session alternate state is not persisted and is not included in the StateNames array in the AppLayout.
        You can use the optional second parameter to choose any other state to get the initial selection on the new state from

        Parameters
        ----------
        qStateName: str
          Name of the alternate state.
        qSourceStateName: str = None
          Name of existing state to copy the initial selections from
        """
        params = {}
        params["qStateName"] = qStateName
        if qSourceStateName is not None:
            params["qSourceStateName"] = qSourceStateName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AddSessionAlternateState", handle, **params)
        return response

    def remove_session_alternate_state(self, qStateName: str) -> bool:
        """
        Removes an session alternate state in the app.
        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        qStateName: str
          Name of the alternate state.
        """
        params = {}
        params["qStateName"] = qStateName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("RemoveSessionAlternateState", handle, **params)[
            "qSuccess"
        ]
        return response

    def create_bookmark(self, qProp: GenericBookmarkProperties) -> GenericBookmark:
        """
        Creates a bookmark.

        Parameters
        ----------
        qProp: GenericBookmarkProperties
          Properties for the object.
        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateBookmark", handle, **params)["qReturn"]
        obj = GenericBookmark(_session=self._session, **response)
        return obj

    def destroy_bookmark(self, qId: str) -> bool:
        """
        Removes a bookmark.
        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        qId: str
          Identifier of the bookmark.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyBookmark", handle, **params)["qSuccess"]
        return response

    def get_bookmark(self, qId: str) -> GenericBookmark:
        """
        Returns the handle of a bookmark.

        Parameters
        ----------
        qId: str
          Identifier of the bookmark.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetBookmark", handle, **params)["qReturn"]
        obj = GenericBookmark(_session=self._session, **response)
        return obj

    def apply_bookmark(self, qId: str) -> bool:
        """
        Applies a bookmark.
        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        qId: str
          Identifier of the bookmark.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ApplyBookmark", handle, **params)["qSuccess"]
        return response

    def apply_and_verify_bookmark(self, qId: str) -> BookmarkApplyAndVerifyResult:
        """
        Experimental
        Applies a bookmark and verifies result dataset against originally selected values.
        The operation is successful if qApplySuccess is set to true. qWarnings lists state and field with unmatching values

        Parameters
        ----------
        qId: str
          Identifier of the bookmark.
        """
        warnings.warn(
            "ApplyAndVerifyBookmark is experimental", UserWarning, stacklevel=2
        )
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ApplyAndVerifyBookmark", handle, **params)[
            "qResult"
        ]
        obj = BookmarkApplyAndVerifyResult(**response)
        return obj

    def clone_bookmark(self, qId: str) -> str:
        """
        Clones a bookmark.
        The identifier is set by the engine.

        Parameters
        ----------
        qId: str
          Identifier of the object to clone.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CloneBookmark", handle, **params)["qCloneId"]
        return response

    def add_field_from_expression(self, qName: str, qExpr: str) -> bool:
        """
        Adds a field on the fly.
        The expression of a field on the fly is persisted but not its values.
        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        qName: str
          Name of the field.
        qExpr: str
          Expression value.
          It is not possible to use all aggregation functions. For example, you cannot add a field on the fly with an expression that uses the Sum or Count aggregation functions.
        """
        params = {}
        params["qName"] = qName
        params["qExpr"] = qExpr
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AddFieldFromExpression", handle, **params)[
            "qSuccess"
        ]
        return response

    def get_field_on_the_fly_by_name(self, qReadableName: str) -> str:
        """
        Find the field-on-the-fly by passing its readable name.

        Parameters
        ----------
        qReadableName: str
          Readable name of the field-on-the-fly.
        """
        params = {}
        params["qReadableName"] = qReadableName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFieldOnTheFlyByName", handle, **params)[
            "qName"
        ]
        return response

    def get_all_infos(self) -> list[NxInfo]:
        """
        Returns the identifier and the type of any generic object in the app.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetAllInfos", handle)["qInfos"]
        return [NxInfo(**e) for e in response]

    def resume(self) -> object:
        """
        Resumes the app as the user left it.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Resume", handle)
        return response

    def abort_modal(self, qAccept: bool) -> object:
        """
        Aborts any selection mode in an app. For more information about selection mode, see BeginSelections method.

        Parameters
        ----------
        qAccept: bool
          Set this parameter to true to accept the selections before exiting the selection mode.
        """
        params = {}
        params["qAccept"] = qAccept
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AbortModal", handle, **params)
        return response

    def get_matching_fields(
        self, qTags: list[str], qMatchingFieldMode: str = None
    ) -> list[NxMatchingFieldInfo]:
        """
        Retrieves any fields that match all of the specified tags or just one of them in the data model of an app.
        Tags set by Qlik Sense are prefixed by the $ sign.

        Parameters
        ----------
        qTags: list[str]
          List of tags.
          The GetMatchingFields method looks for fields that match one or all of the tags in this list, depending on the value of qMatchingFieldMode .
        qMatchingFieldMode: str = None
          Matching field mode.
          The default value is MATCHINGFIELDMODE_MATCH_ALL.

          One of:

          • MATCHINGFIELDMODE_MATCH_ALL

          • MATCHINGFIELDMODE_MATCH_ONE
        """
        params = {}
        params["qTags"] = qTags
        if qMatchingFieldMode is not None:
            params["qMatchingFieldMode"] = qMatchingFieldMode
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetMatchingFields", handle, **params)[
            "qFieldNames"
        ]
        return [NxMatchingFieldInfo(**e) for e in response]

    def find_matching_fields(
        self, qFieldName: str, qTags: list[str]
    ) -> list[NxMatchingFieldInfo]:
        """
        Retrieves any fields that belong to the same archipelago as the specified field and that match at least one of the specified tags.
        Tags set by Qlik Sense are prefixed by the $ sign.

        Parameters
        ----------
        qFieldName: str
          Name of the field.
          This method looks for fields that belong to the same archipelago as this specified field.
        qTags: list[str]
          List of tags.
          This method looks for fields that match at least one of the tags in this list.
        """
        params = {}
        params["qFieldName"] = qFieldName
        params["qTags"] = qTags
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("FindMatchingFields", handle, **params)[
            "qFieldNames"
        ]
        return [NxMatchingFieldInfo(**e) for e in response]

    def scramble(self, qFieldName: str) -> object:
        """
        Scrambles a field so the data is not recognizable. Some properties are retained to help debugging. For example, special characters are not changed, and small numbers are scrambled to another small number.
        Update access is required to use the function in Qlik Sense Enterprise.

        Parameters
        ----------
        qFieldName: str
          Name of the field to scramble.
        """
        params = {}
        params["qFieldName"] = qFieldName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Scramble", handle, **params)
        return response

    def save_objects(self) -> object:
        """
        Saves all objects that were modified in the app.
        Data from the data model are not saved. This operation is possible only in Qlik Sense Enterprise.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SaveObjects", handle)
        return response

    def get_association_scores(
        self, qTable1: str, qTable2: str
    ) -> list[AssociationScore]:
        """
        Computes a set of association scores for each pair of fields between two given tables that have been loaded in an app.
        When a table contains some synthetic keys, all fields in the synthetic key tables are analyzed against fields in other tables. To denote that a field is a synthetic key, the field name is prefixed by [Synthetic Key]: .

        Parameters
        ----------
        qTable1: str
          Name of the first table.
        qTable2: str
          Name of the second table.
        """
        params = {}
        params["qTable1"] = qTable1
        params["qTable2"] = qTable2
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetAssociationScores", handle, **params)[
            "qScore"
        ]
        return [AssociationScore(**e) for e in response]

    def get_media_list(self) -> GetMediaListReturn:
        """
        Lists the media files.

        Parameters
        ----------
        """
        warnings.warn("GetMediaList is deprecated", DeprecationWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetMediaList", handle)
        obj = GetMediaListReturn(**response)
        return obj

    def get_content_libraries(self) -> ContentLibraryList:
        """
        Lists the content libraries.
        To differentiate a global content library from an app specific content library, you can check the property qAppSpecific . If this property is set to true, it means that the content library is app specific.
        There is always one specific content library per app.

         Qlik Sense:
        Returns the global content libraries and the app specific content library.
        When using Qlik Sense, you can have more than one global content library. The global content libraries are common to all apps in the Qlik Sense repository.
        By default, there is one global content library named Default .

         Qlik Sense Desktop:
        Returns the global content library and the app specific content library from the disk.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetContentLibraries", handle)["qList"]
        obj = ContentLibraryList(**response)
        return obj

    def get_library_content(self, qName: str) -> StaticContentList:
        """
        Returns the content of a library.

         Global content library:
        In Qlik Sense Desktop, the content files are retrieved from:
        %userprofile%\Documents\Qlik\Sense\Content\Default
        In Qlik Sense Enterprise, the content files are retrieved from the Qlik Sense repository.

         App specific content library:
        The embedded files are returned.

        Parameters
        ----------
        qName: str
          Name of the content library.
          It corresponds to the property qContentLibraryListItem/qName returned by the GetContentLibraries method.
        """
        params = {}
        params["qName"] = qName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLibraryContent", handle, **params)["qList"]
        obj = StaticContentList(**response)
        return obj

    def do_reload_ex(self, qParams: DoReloadExParams = None) -> DoReloadExResult:
        """
        Reloads the script that is set in an app and returns the path to the script log file.
        A log file is created per reload.

         Logs:
        When this method is called, audit activity logs are produced to track the user activity.
        In the case of errors, both audit activity logs and system services logs are produced.
        The log files are named as follows:
        | Audit activity log                                                                                                                      | System service log                                                                                                          |
        |-----------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
        | __AuditActivity_Engine.txt_ in Qlik Sense Enterprise  __AuditActivity_Engine.log_ in Qlik Sense Desktop | __Service_Engine.txt_ in Qlik Sense Enterprise  __Service_Engine.log_ in Qlik Sense Desktop |

         Where to find the log files:
        The location of the log files depends on whether you have installed Qlik Sense Enterprise or Qlik Sense Desktop.
        | Qlik Sense Enterprise                 | Qlik Sense Desktop                       |
        |---------------------------------------|------------------------------------------|
        | _%ProgramData%/Qlik/Sense/Log/Engine_ | _%UserProfile%/Documents/Qlik/Sense/Log_ |

         DoReloadExParams:
        | Name     | Description                                                                                                                                                                                                                                    | Type    |
        |----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
        | qMode    | Error handling mode  One of:  *   0: for default mode.*   1: for ABEND; the reload of the script ends if an error occurs.*   2: for ignore; the reload of the script continues even if an error is detected in the script. | Integer |
        | qPartial | Set to true for partial reload.  The default value is false.                                                                                                                                                                               | Boolean |
        | qDebug   | Set to true if debug breakpoints are to be honored. The execution of the script will be in debug mode.  The default value is false.                                                                                                        | Boolean |

         DoReloadExResult:
        | Name           | Description                                               | Type    |
        |----------------|-----------------------------------------------------------|---------|
        | qSuccess       | The operation is successful if _qSuccess_ is set to True. | Boolean |
        | qScriptLogFile | Path to the script log file.                              | String  |

        If the data load has successfully finished, no matter how the indexing behaves, true is returned. This happens even if there is a timeout, a memory limit is reached or any other error occurs during the indexing.

        Parameters
        ----------
        qParams: DoReloadExParams = None
        """
        params = {}
        if qParams is not None:
            params["qParams"] = qParams
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DoReloadEx", handle, **params)["qResult"]
        obj = DoReloadExResult(**response)
        return obj

    def back_count(self) -> int:
        """
        Returns the number of entries on the back stack.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("BackCount", handle)["qReturn"]
        return response

    def forward_count(self) -> int:
        """
        Returns the number of entries on the Forward stack.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ForwardCount", handle)["qReturn"]
        return response

    def export_reduced_data(self, qOptions: NxDownloadOptions = None) -> NxDownloadInfo:
        """
        Applies a bookmark to reduce (slice) the data on. Returns a url and file size to the reduced application. Section Access is always applied.
        This API is only available on Sense Enterprise on Windows

        Parameters
        ----------
        qOptions: NxDownloadOptions = None
          BookmarkId used to reduced the app on and an expire time.
        """
        params = {}
        if qOptions is not None:
            params["qOptions"] = qOptions
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ExportReducedData", handle, **params)[
            "qDownloadInfo"
        ]
        obj = NxDownloadInfo(**response)
        return obj

    def get_set_analysis(self, qStateName: str = None, qBookmarkId: str = None) -> str:
        """
        Returns a set analysis expression from active selections or from a saved bookmark. Fields on the fly and Calculated dimensions will not be included in the generated expressions, instead a message indicating 'missing fields' will provided within the expression.
        |                       | BookmarkId empty                     | BookmarkId set                                     |
        |-----------------------|--------------------------------------|----------------------------------------------------|
        |StateName empty (or $) | Default selections state is returned.| Default state ($) in bookmark with id is returned. |
        |StateName set          | State selections is returned.        | State in bookmark with id is returned.             |

        Parameters
        ----------
        qStateName: str = None
          Optional. The name of the state to get set analysis expression for. If left empty, the default state will be retrieved.
        qBookmarkId: str = None
          Optional. The Id of the bookmark to get the set analysis expression for. If left empty, the current selection will be retrieved.
        """
        params = {}
        if qStateName is not None:
            params["qStateName"] = qStateName
        if qBookmarkId is not None:
            params["qBookmarkId"] = qBookmarkId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetSetAnalysis", handle, **params)[
            "qSetExpression"
        ]
        return response

    def set_script(self, qScript: str) -> object:
        """
        Sets values in script.

        Parameters
        ----------
        qScript: str
          Script content.
        """
        params = {}
        params["qScript"] = qScript
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetScript", handle, **params)
        return response

    def check_script_syntax(self) -> list[ScriptSyntaxError]:
        """
        Checks the syntax of a script.

         Example:
        "result": { "qErrors": [ { "qErrLen": 3, "qTabIx": 0, "qLineInTab": 0, "qColInLine": 0, "qTextPos": 0 }, { "qErrLen": 5, "qTabIx": 0, "qLineInTab": 0, "qColInLine": 1, "qTextPos": 4, "qSecondaryFailure": true } ] }
        The first area is the primary error area, the second area is the secondary error area. The second area is optional and is shown only if qSecondaryFailure is set to true. The second area ends when the next statement in the script begins.
        The list of syntax errors in the script.
        If there are no errors, the engine returns:
        If there are errors, the engine returns the following properties in the response:
        | Name              | Description                                                      | Type    |
        |-------------------|------------------------------------------------------------------|---------|
        | qErrLen           | Length of the word where the error is located.                   | Integer |
        | qTabIx            | Number of the faulty section.                                    | Integer |
        | qLineInTab        | Line number in the section where the error is located.           | Integer |
        | qColInLine        | Position of the erroneous text from the beginning of the line.   | Integer |
        | qTextPos          | Position of the erroneous text from the beginning of the script. | Integer |
        | qSecondaryFailure | The default value is false.                                      | Boolean |

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CheckScriptSyntax", handle)["qErrors"]
        return [ScriptSyntaxError(**e) for e in response]

    def get_favorite_variables(self) -> list[str]:
        """
        Retrieves the variables that are tagged as favorite.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFavoriteVariables", handle)["qNames"]
        return response

    def set_favorite_variables(self, qNames: list[str]) -> object:
        """
        Set some variables as favorite.

        Parameters
        ----------
        qNames: list[str]
          Variables to set as favorite.
        """
        params = {}
        params["qNames"] = qNames
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetFavoriteVariables", handle, **params)
        return response

    def get_include_file_content(self, qPath: str) -> str:
        """
        Gets the content of a file.

        Parameters
        ----------
        qPath: str
          ["lib://CONNECTION_NAME\\\<the name of the file you want to use>.txt"]
          OR
          ["lib://Connection_Name\\\<Folder under your connection>\\\<the name of the file you want to use>.txt"]
          [ ] should be used when the first variable contains a lib reference.
        """
        params = {}
        params["qPath"] = qPath
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetIncludeFileContent", handle, **params)[
            "qContent"
        ]
        return response

    def create_connection(self, qConnection: Connection) -> str:
        """
        Creates a connection.
        A connection indicates from which data source the data should be taken.

        Parameters
        ----------
        qConnection: Connection
          Information about the connection.
        """
        params = {}
        params["qConnection"] = qConnection
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateConnection", handle, **params)[
            "qConnectionId"
        ]
        return response

    def modify_connection(
        self,
        qConnectionId: str,
        qConnection: Connection,
        qOverrideCredentials: bool = None,
    ) -> object:
        """
        Updates a connection.
        The identifier of a connection cannot be updated. qType cannot be modified with the ModifyConnection method.

        Parameters
        ----------
        qConnectionId: str
          Identifier of the connection.
        qConnection: Connection
          Information about the connection.
          Properties that can be updated.
        qOverrideCredentials: bool = None
          Set this parameter to true to override the user name and password.
        """
        params = {}
        params["qConnectionId"] = qConnectionId
        params["qConnection"] = qConnection
        if qOverrideCredentials is not None:
            params["qOverrideCredentials"] = qOverrideCredentials
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ModifyConnection", handle, **params)
        return response

    def delete_connection(self, qConnectionId: str) -> object:
        """
        Deletes a connection.
        In Qlik Sense Enterprise, there is an additional file connection named AttachedFiles . The AttachedFiles connection can only be removed by the administrator of the system.

        Parameters
        ----------
        qConnectionId: str
          Identifier of the connection to remove.
        """
        params = {}
        params["qConnectionId"] = qConnectionId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DeleteConnection", handle, **params)
        return response

    def get_connection(self, qConnectionId: str) -> Connection:
        """
        Retrieves a connection and returns:

        • The creation time of the connection.

        • The identifier of the connection.

        • The type of the connection.

        • The name of the connection.

        • The connection string.

        Parameters
        ----------
        qConnectionId: str
          Identifier of the connection.
        """
        params = {}
        params["qConnectionId"] = qConnectionId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetConnection", handle, **params)["qConnection"]
        obj = Connection(**response)
        return obj

    def get_connections(self) -> list[Connection]:
        """
        Lists the connections in an app.
        In Qlik Sense Enterprise, there is an additional file connection named AttachedFiles . This connection is stored in the Qlik Sense repository.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetConnections", handle)["qConnections"]
        return [Connection(**e) for e in response]

    def get_database_info(self, qConnectionId: str) -> DatabaseInfo:
        """
        Gives information about an ODBC, OLEDB or CUSTOM connection. See Outputs for more details.

        Parameters
        ----------
        qConnectionId: str
          Name of the connection.
        """
        params = {}
        params["qConnectionId"] = qConnectionId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDatabaseInfo", handle, **params)["qInfo"]
        obj = DatabaseInfo(**response)
        return obj

    def get_databases(self, qConnectionId: str) -> list[Database]:
        """
        Lists the databases inside a ODBC, OLEDB or CUSTOM data source.

        Parameters
        ----------
        qConnectionId: str
          Identifier of the connection.
        """
        params = {}
        params["qConnectionId"] = qConnectionId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDatabases", handle, **params)["qDatabases"]
        return [Database(**e) for e in response]

    def get_database_owners(
        self, qConnectionId: str, qDatabase: str = None
    ) -> list[DatabaseOwner]:
        """
        Lists the owners of a database for a ODBC, OLEDB or CUSTOM connection.

        Parameters
        ----------
        qConnectionId: str
          Identifier of the connection.
        qDatabase: str = None
          Name of the database.
        """
        params = {}
        params["qConnectionId"] = qConnectionId
        if qDatabase is not None:
            params["qDatabase"] = qDatabase
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDatabaseOwners", handle, **params)["qOwners"]
        return [DatabaseOwner(**e) for e in response]

    def get_database_tables(
        self, qConnectionId: str, qDatabase: str = None, qOwner: str = None
    ) -> list[DataTable]:
        """
        Lists the tables inside a database for a ODBC, OLEDB or CUSTOM connection.

        Parameters
        ----------
        qConnectionId: str
          Identifier of the connection.
        qDatabase: str = None
          Name of the database.
          If qDatabase is not set then qOwner must be set.
        qOwner: str = None
          Owner of the database.
          If qOwner is not set then qDatabase must be set.
        """
        params = {}
        params["qConnectionId"] = qConnectionId
        if qDatabase is not None:
            params["qDatabase"] = qDatabase
        if qOwner is not None:
            params["qOwner"] = qOwner
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDatabaseTables", handle, **params)["qTables"]
        return [DataTable(**e) for e in response]

    def get_database_table_fields(
        self, qConnectionId: str, qTable: str, qDatabase: str = None, qOwner: str = None
    ) -> list[DataField]:
        """
        Lists the fields inside a table of a database for a ODBC, OLEDB or CUSTOM connection.

        Parameters
        ----------
        qConnectionId: str
          Identifier of the connection.
        qTable: str
          Name of the table.
        qDatabase: str = None
          Name of the database.
          If qDatabase is not set then qOwner must be set.
        qOwner: str = None
          Owner of the database.
          If qOwner is not set then qDatabase must be set.
        """
        params = {}
        params["qConnectionId"] = qConnectionId
        params["qTable"] = qTable
        if qDatabase is not None:
            params["qDatabase"] = qDatabase
        if qOwner is not None:
            params["qOwner"] = qOwner
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDatabaseTableFields", handle, **params)[
            "qFields"
        ]
        return [DataField(**e) for e in response]

    def get_database_table_preview(
        self,
        qConnectionId: str,
        qTable: str,
        qDatabase: str = None,
        qOwner: str = None,
        qConditions: FilterInfo = None,
    ) -> GetDatabaseTablePreviewReturn:
        """
        Retrieves the values of the specified table of a database for a ODBC, OLEDB or CUSTOM connection.

        Parameters
        ----------
        qConnectionId: str
          Identifier of the connection.
        qTable: str
          Name of the table.
        qDatabase: str = None
          Name of the database.
          If qDatabase is not set then qOwner must be set.
        qOwner: str = None
          Owner of the database.
          If qOwner is not set then qDatabase must be set.
        qConditions: FilterInfo = None
        """
        params = {}
        params["qConnectionId"] = qConnectionId
        params["qTable"] = qTable
        if qDatabase is not None:
            params["qDatabase"] = qDatabase
        if qOwner is not None:
            params["qOwner"] = qOwner
        if qConditions is not None:
            params["qConditions"] = qConditions
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDatabaseTablePreview", handle, **params)
        obj = GetDatabaseTablePreviewReturn(**response)
        return obj

    def get_folder_items_for_connection(
        self, qConnectionId: str, qRelativePath: str = None
    ) -> list[FolderItem]:
        """
        Lists the items for a folder connection.

        Parameters
        ----------
        qConnectionId: str
          Identifier of the connection.
        qRelativePath: str = None
          Relative path of the connection.
        """
        params = {}
        params["qConnectionId"] = qConnectionId
        if qRelativePath is not None:
            params["qRelativePath"] = qRelativePath
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFolderItemsForConnection", handle, **params)[
            "qFolderItems"
        ]
        return [FolderItem(**e) for e in response]

    def guess_file_type(
        self, qConnectionId: str, qRelativePath: str = None
    ) -> FileDataFormat:
        """
        Guesses the data format for a given file.
        Recognized file formats are:

        • CSV for Delimited

        • FIX for Fixed Record

        • DIF for Data Interchange Format

        • EXCEL_BIFF for Microsoft Excel (XLS)

        • EXCEL_OOXML for Microsoft Excel (XLSX)

        • HTML for HTML

        • QVD for QVD file

        • XML for XML

        • QVX for QVX file

        • JSON for JSON format

        • KML for KML file

        • PARQUET for PARQUET file

         FileType:
        Recognized file formats are:

        • CSV for Delimited

        • FIX for Fixed Record

        • DIF for Data Interchange Format

        • EXCEL_BIFF for Microsoft Excel (XLS)

        • EXCEL_OOXML for Microsoft Excel (XLSX)

        • HTML for HTML

        • QVD for QVD file

        • XML for XML

        • QVX for QVX file

        • JSON for JSON format

        • KML for KML file

        • PARQUET for PARQUET file

        Parameters
        ----------
        qConnectionId: str
          Identifier of the connection file.
        qRelativePath: str = None
          Path of the connection file.
        """
        params = {}
        params["qConnectionId"] = qConnectionId
        if qRelativePath is not None:
            params["qRelativePath"] = qRelativePath
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GuessFileType", handle, **params)["qDataFormat"]
        obj = FileDataFormat(**response)
        return obj

    def get_file_tables(
        self, qConnectionId: str, qDataFormat: FileDataFormat, qRelativePath: str = None
    ) -> list[DataTable]:
        """
        Lists the tables for a folder connection.

         FileType:
        Recognized file formats are:

        • CSV for Delimited

        • FIX for Fixed Record

        • DIF for Data Interchange Format

        • EXCEL_BIFF for Microsoft Excel (XLS)

        • EXCEL_OOXML for Microsoft Excel (XLSX)

        • HTML for HTML

        • QVD for QVD file

        • XML for XML

        • QVX for QVX file

        • JSON for JSON format

        • KML for KML file

        • PARQUET for PARQUET file

        Parameters
        ----------
        qConnectionId: str
          Identifier of the connection.
        qDataFormat: FileDataFormat
          Type of the file.
        qRelativePath: str = None
          Path of the connection file.
        """
        params = {}
        params["qConnectionId"] = qConnectionId
        params["qDataFormat"] = qDataFormat
        if qRelativePath is not None:
            params["qRelativePath"] = qRelativePath
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFileTables", handle, **params)["qTables"]
        return [DataTable(**e) for e in response]

    def get_file_table_fields(
        self,
        qConnectionId: str,
        qDataFormat: FileDataFormat,
        qTable: str,
        qRelativePath: str = None,
    ) -> GetFileTableFieldsReturn:
        """
        Lists the fields of a table for a folder connection.

         FileType:
        Recognized file formats are:

        • CSV for Delimited

        • FIX for Fixed Record

        • DIF for Data Interchange Format

        • EXCEL_BIFF for Microsoft Excel (XLS)

        • EXCEL_OOXML for Microsoft Excel (XLSX)

        • HTML for HTML

        • QVD for QVD file

        • XML for XML

        • QVX for QVX file

        • JSON for JSON format

        • KML for KML file

        • PARQUET for PARQUET file

        Parameters
        ----------
        qConnectionId: str
          Identifier of the connection.
        qDataFormat: FileDataFormat
          Type of the file.
        qTable: str
          Name of the table.
          This parameter must be set for XLS , XLSX , HTML  _ and _XML files.
        qRelativePath: str = None
          Path of the connection file.
        """
        params = {}
        params["qConnectionId"] = qConnectionId
        params["qDataFormat"] = qDataFormat
        params["qTable"] = qTable
        if qRelativePath is not None:
            params["qRelativePath"] = qRelativePath
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFileTableFields", handle, **params)
        obj = GetFileTableFieldsReturn(**response)
        return obj

    def get_file_table_preview(
        self,
        qConnectionId: str,
        qDataFormat: FileDataFormat,
        qTable: str,
        qRelativePath: str = None,
    ) -> GetFileTablePreviewReturn:
        """
        Lists the values in a table for a folder connection.

         FileType:
        Recognized file formats are:

        • CSV for Delimited

        • FIX for Fixed Record

        • DIF for Data Interchange Format

        • EXCEL_BIFF for Microsoft Excel (XLS)

        • EXCEL_OOXML for Microsoft Excel (XLSX)

        • HTML for HTML

        • QVD for QVD file

        • XML for XML

        • QVX for QVX file

        • JSON for JSON format

        • KML for KML file

        • PARQUET for PARQUET file

        Parameters
        ----------
        qConnectionId: str
          Identifier of the connection.
        qDataFormat: FileDataFormat
          Type of the file.
        qTable: str
          Name of the table.
          This parameter must be set for XLS , XLSX , HTML  _ and _XML files.
        qRelativePath: str = None
          Path of the connection file.
        """
        params = {}
        params["qConnectionId"] = qConnectionId
        params["qDataFormat"] = qDataFormat
        params["qTable"] = qTable
        if qRelativePath is not None:
            params["qRelativePath"] = qRelativePath
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFileTablePreview", handle, **params)
        obj = GetFileTablePreviewReturn(**response)
        return obj

    def get_file_tables_ex(
        self, qConnectionId: str, qDataFormat: FileDataFormat, qRelativePath: str = None
    ) -> list[DataTableEx]:
        """
        Lists the tables and fields of a JSON or XML file for a folder connection.

        Parameters
        ----------
        qConnectionId: str
          Identifier of the connection.
        qDataFormat: FileDataFormat
          Type of the file.
        qRelativePath: str = None
          Path of the connection file.
        """
        params = {}
        params["qConnectionId"] = qConnectionId
        params["qDataFormat"] = qDataFormat
        if qRelativePath is not None:
            params["qRelativePath"] = qRelativePath
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFileTablesEx", handle, **params)["qTables"]
        return [DataTableEx(**e) for e in response]

    def send_generic_command_to_custom_connector(
        self,
        qProvider: str,
        qCommand: str,
        qMethod: str,
        qParameters: list[str],
        qAppendConnection: str,
    ) -> str:
        """
        Sends a generic command to a custom connector.
        For more information on the commands that can be sent to a custom connector, see the QVX SDK help.

        Parameters
        ----------
        qProvider: str
          Connector file name.
          Command to be executed by the connector.
        qCommand: str
          One of:

          • JsonRequest

          • GetCustomCaption

          • IsConnected

          • DisableQlikViewSelectButton

          • HaveStarField
        qMethod: str
          Method name to be used within the command.
          The available methods depend on the chosen connector.
        qParameters: list[str]
          Parameters of the command.
          No parameters are required.
        qAppendConnection: str
          Name of the connection.
        """
        params = {}
        params["qProvider"] = qProvider
        params["qCommand"] = qCommand
        params["qMethod"] = qMethod
        params["qParameters"] = qParameters
        params["qAppendConnection"] = qAppendConnection
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send(
            "SendGenericCommandToCustomConnector", handle, **params
        )["qResult"]
        return response

    def search_suggest(
        self, qOptions: SearchCombinationOptions, qTerms: list[str]
    ) -> SearchSuggestionResult:
        """
        Returns search terms suggestions.

        Parameters
        ----------
        qOptions: SearchCombinationOptions
          Information about the search combinations.
        qTerms: list[str]
          Terms to search for.
        """
        params = {}
        params["qOptions"] = qOptions
        params["qTerms"] = qTerms
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SearchSuggest", handle, **params)["qResult"]
        obj = SearchSuggestionResult(**response)
        return obj

    def search_associations(
        self, qOptions: SearchCombinationOptions, qTerms: list[str], qPage: SearchPage
    ) -> SearchAssociationResult:
        """
        Returns the search matches for one or more search terms.
        The search results depend on the search context.
        SearchCombinationOptions

         SearchMatchCombinations:
        | Name                     | Description                   | Type                              |
        |--------------------------|-------------------------------|-----------------------------------|
        | qSearchMatchCombinations | Array of search combinations. | Array of _SearchMatchCombination_ |

        Parameters
        ----------
        qOptions: SearchCombinationOptions
          Information about the search fields and the search context.
        qTerms: list[str]
          List of terms to search for.
        qPage: SearchPage
          Array of pages to retrieve.
        """
        warnings.warn(
            "SearchAssociations is deprecated", DeprecationWarning, stacklevel=2
        )
        params = {}
        params["qOptions"] = qOptions
        params["qTerms"] = qTerms
        params["qPage"] = qPage
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SearchAssociations", handle, **params)[
            "qResults"
        ]
        obj = SearchAssociationResult(**response)
        return obj

    def select_associations(
        self,
        qOptions: SearchCombinationOptions,
        qTerms: list[str],
        qMatchIx: int,
        qSoftLock: bool = None,
    ) -> object:
        """
        Selects all search hits for a specified group.
        The results depend on the search context.
        SearchCombinationOptions.

        Parameters
        ----------
        qOptions: SearchCombinationOptions
          Information about the search fields and the search context.
        qTerms: list[str]
          List of terms to search for.
        qMatchIx: int
          Index (value of qId ) of the search result to select.
        qSoftLock: bool = None
          This parameter is deprecated and should not be set.
        """
        params = {}
        params["qOptions"] = qOptions
        params["qTerms"] = qTerms
        params["qMatchIx"] = qMatchIx
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectAssociations", handle, **params)
        return response

    def search_results(
        self, qOptions: SearchCombinationOptions, qTerms: list[str], qPage: SearchPage
    ) -> SearchResult:
        """
        Returns the search matches for one or more search terms.
        Search results are organized in search groups. The type of search group indicates where the search matches come from (from data for example).
        Each search group contains search results that correspond to a combination of search terms.
        For example, if the search terms are organic , pasta , and America , the possible combination of search groups are:

        • organic

        • pasta

        • America

        • organic, pasta, America

        • organic, pasta

        • organic, America

        • pasta, America

        For every search group, there are one or more search group items. Each subgroup item contains results that correspond to an item type (for example a field).
        For every search group item, there are one or several search matches. The position of the match in each search result is given.

        Parameters
        ----------
        qOptions: SearchCombinationOptions
          Information about the search combinations.
        qTerms: list[str]
          Terms to search for.
        qPage: SearchPage
          Array of pages to retrieve.
        """
        params = {}
        params["qOptions"] = qOptions
        params["qTerms"] = qTerms
        params["qPage"] = qPage
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SearchResults", handle, **params)["qResult"]
        obj = SearchResult(**response)
        return obj

    def search_objects(
        self, qOptions: SearchObjectOptions, qTerms: list[str], qPage: SearchPage
    ) -> SearchResult:
        """
        Returns the generic objects corresponding to one or more search terms. The search is performed within the title, subtitle, footnote and type. In addition, associated dimension values are also searched in. For example, if the country “Japan” is selected and the object contains the dimension City, the object will appear in the results for “Osaka” but not for “Johannesburg”. The generic objects with the following types will never appear in the results: slideitem , sheet , story , slide , masterobject , snapshot , LoadModel , appprops and searchhistory .

        Parameters
        ----------
        qOptions: SearchObjectOptions
          Information about attributes.
        qTerms: list[str]
          Terms to search for.
        qPage: SearchPage
          Array of pages to retrieve.
        """
        params = {}
        params["qOptions"] = qOptions
        params["qTerms"] = qTerms
        params["qPage"] = qPage
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SearchObjects", handle, **params)["qResult"]
        obj = SearchResult(**response)
        return obj

    def get_field_and_column_samples(
        self,
        qFieldsOrColumnsWithWildcards: list[FieldOrColumn],
        qMaxNumberOfValues: int,
        qRandSeed: int = None,
    ) -> list[SampleResult]:
        """
        Get sample values from either a column in a table or from a field.
        Supports wildcard matches in tables or field names:
        - '*' for zero or more characters.
        - '?' for one character.

        Parameters
        ----------
        qFieldsOrColumnsWithWildcards: list[FieldOrColumn]
          Pairs of table (optionally) and field names. Support wildcard matches.
        qMaxNumberOfValues: int
          Max number of sample values returned. Depending on the column or field size the number of returned samples can be less than MaxNumberOfValues. If MaxNumberOfValues is negative all sample values are returned.
        qRandSeed: int = None
          Optional. Sets the random number seed. Should only be set for test purposes.
        """
        params = {}
        params["qFieldsOrColumnsWithWildcards"] = qFieldsOrColumnsWithWildcards
        params["qMaxNumberOfValues"] = qMaxNumberOfValues
        if qRandSeed is not None:
            params["qRandSeed"] = qRandSeed
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFieldAndColumnSamples", handle, **params)[
            "qResult"
        ]
        return [SampleResult(**e) for e in response]

    def get_script_ex(self) -> AppScript:
        """
        Gets script and script meta-data.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetScriptEx", handle)["qScript"]
        obj = AppScript(**response)
        return obj

    def get_variables(self, qListDef: VariableListDef) -> list[NxVariableListItem]:
        """
        Parameters
        ----------
        qListDef: VariableListDef
        """
        params = {}
        params["qListDef"] = qListDef
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetVariables", handle, **params)["qList"]
        return [NxVariableListItem(**e) for e in response]

    def expand_expression(self, qExpression: str) -> str:
        """
        Expands the expression.

        Parameters
        ----------
        qExpression: str
          The expression string to expand.
        """
        params = {}
        params["qExpression"] = qExpression
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ExpandExpression", handle, **params)[
            "qExpandedExpression"
        ]
        return response

    def destroy_session_variable_by_id(self, qId: str) -> bool:
        """
        Removes a transient variable.

        qSuccess is set to true if the operation is successful.

        Parameters
        ----------
        qId: str
          Identifier of the variable.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroySessionVariableById", handle, **params)[
            "qSuccess"
        ]
        return response

    def destroy_session_variable_by_name(self, qName: str) -> bool:
        """
        Removes a transient variable.

        qSuccess is set to true if the operation is successful.

        Parameters
        ----------
        qName: str
          Name of the variable.
        """
        params = {}
        params["qName"] = qName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroySessionVariableByName", handle, **params)[
            "qSuccess"
        ]
        return response

    def create_bookmark_ex(
        self, qProp: GenericBookmarkProperties, qObjectIdsToPatch: list[str] = None
    ) -> GenericBookmark:
        """
        Experimental
        Creates a bookmark with softpatches.

        Parameters
        ----------
        qProp: GenericBookmarkProperties
          Properties for the object.
        qObjectIdsToPatch: list[str] = None
          Add softpatches for this objects if available. If empty all softpatches are added to the bookmark.
        """
        warnings.warn("CreateBookmarkEx is experimental", UserWarning, stacklevel=2)
        params = {}
        params["qProp"] = qProp
        if qObjectIdsToPatch is not None:
            params["qObjectIdsToPatch"] = qObjectIdsToPatch
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateBookmarkEx", handle, **params)["qReturn"]
        obj = GenericBookmark(_session=self._session, **response)
        return obj

    def save_as(self, qNewAppName: str) -> str:
        """
        Save a copy of an app with a different name.
        Can be used to save a session app as an ordinary app.

        Parameters
        ----------
        qNewAppName: str
          <Name of the saved app>
        """
        params = {}
        params["qNewAppName"] = qNewAppName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SaveAs", handle, **params)["qNewAppId"]
        return response

    def store_temp_selection_state(
        self, qTTLOfTempState: int = None
    ) -> StoreTempSelectionStateReturn:
        """
        Store current selection state temporarily.
        The temporary selection state will be stored for 30min by default if TTL parameter is not present or positive.
        StoreTempSelectionState method is only supported in SaaS Editions of Qlik Sense.

        Parameters
        ----------
        qTTLOfTempState: int = None
          Time to live in seconds for stored selection state
        """
        params = {}
        if qTTLOfTempState is not None:
            params["qTTLOfTempState"] = qTTLOfTempState
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("StoreTempSelectionState", handle, **params)
        obj = StoreTempSelectionStateReturn(**response)
        return obj

    def restore_temp_selection_state(self, qId: str) -> bool:
        """
        Restore a temporary selection state identified by Id.
        RestoreTempSelectionState method is only supported in SaaS Editions of Qlik Sense.

        Parameters
        ----------
        qId: str
          Identifier of the temporary selection state
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("RestoreTempSelectionState", handle, **params)[
            "qReturn"
        ]
        return response

    def change_session_app_owner(self, qNewOwnerId: str) -> bool:
        """
        Experimental
        Change the owner of a session app.
        Can be used by a privileged user when creating a session app to be consumed by another user.
        Only useful in environments where it is possible to reconnect to a session app, currently only in cloud deployments.

        Parameters
        ----------
        qNewOwnerId: str
          Identifier of the new app owner.
        """
        warnings.warn(
            "ChangeSessionAppOwner is experimental", UserWarning, stacklevel=2
        )
        params = {}
        params["qNewOwnerId"] = qNewOwnerId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ChangeSessionAppOwner", handle, **params)[
            "qSuccess"
        ]
        return response

    def change_session_app_space(self, qSpaceId: str) -> bool:
        """
        Experimental
        Add a session app to a space.
        Can be used by a privileged user when creating a session app to be consumed by other users.
        Only useful in environments where it is possible to reconnect to a session app, currently only in cloud deployments.

        Parameters
        ----------
        qSpaceId: str
          Identifier of the new space.
        """
        warnings.warn(
            "ChangeSessionAppSpace is experimental", UserWarning, stacklevel=2
        )
        params = {}
        params["qSpaceId"] = qSpaceId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ChangeSessionAppSpace", handle, **params)[
            "qSuccess"
        ]
        return response

    def get_table_profile_data(self, qTableName: str) -> TableProfilingData:
        """
        Experimental
        Returns profile data for a given table.

        Parameters
        ----------
        qTableName: str
          Name of the table
        """
        warnings.warn("GetTableProfileData is experimental", UserWarning, stacklevel=2)
        params = {}
        params["qTableName"] = qTableName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetTableProfileData", handle, **params)[
            "qProfiling"
        ]
        obj = TableProfilingData(**response)
        return obj

    def get_measure_with_label(self, qLabel: str) -> GenericMeasure:
        """
        Returns the handle of a measure with a label.
        If multiple measures has the same label the first is returned.

        Parameters
        ----------
        qLabel: str
          is the label of the measure to be returned.
        """
        params = {}
        params["qLabel"] = qLabel
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetMeasureWithLabel", handle, **params)[
            "qReturn"
        ]
        obj = GenericMeasure(_session=self._session, **response)
        return obj

    def search_values(
        self, qOptions: SearchValueOptions, qTerms: list[str], qPage: SearchValuePage
    ) -> SearchValueResult:
        """
        Experimental
        Parameters
        ----------
        qOptions: SearchValueOptions
        qTerms: list[str]
        qPage: SearchValuePage
        """
        warnings.warn("SearchValues is experimental", UserWarning, stacklevel=2)
        params = {}
        params["qOptions"] = qOptions
        params["qTerms"] = qTerms
        params["qPage"] = qPage
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SearchValues", handle, **params)["qResult"]
        obj = SearchValueResult(**response)
        return obj

    def get_fields_from_expression(self, qExpr: str) -> list[str]:
        """
        Retrives any fields from an expression.

        Parameters
        ----------
        qExpr: str
          Expression to get fields from.
        """
        params = {}
        params["qExpr"] = qExpr
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFieldsFromExpression", handle, **params)[
            "qFieldNames"
        ]
        return response

    def get_fields_resource_ids(
        self, qFieldNames: list[str]
    ) -> list[NxFieldResourceId]:
        """
        Returns a list of resource ids (QRI) for fields that belongs to the datamodel.
        Key fields (that belongs to multiple tables), returns one resource identifier per table.
        GetFieldsResourceIds method is only supported in SaaS Editions of Qlik Sense.

        Parameters
        ----------
        qFieldNames: list[str]
          List of fields names that resource ids should be returned from.
        """
        params = {}
        params["qFieldNames"] = qFieldNames
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFieldsResourceIds", handle, **params)[
            "qFields"
        ]
        return [NxFieldResourceId(**e) for e in response]

    def get_expression_bnf(self) -> GetExpressionBNFReturn:
        """
        Experimental
        Gets the current Backus-Naur Form (BNF) grammar of the Qlik chart expressions supported within a given App.

        Parameters
        ----------
        """
        warnings.warn("GetExpressionBNF is experimental", UserWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetExpressionBNF", handle)
        obj = GetExpressionBNFReturn(**response)
        return obj

    def get_expression_bnf_hash(self) -> str:
        """
        Experimental
        Gets a string hash calculated from the current Backus-Naur Form (BNF) grammar  of the Qlik chart expressions supported within a given App.

        Parameters
        ----------
        """
        warnings.warn("GetExpressionBNFHash is experimental", UserWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetExpressionBNFHash", handle)["qBnfHash"]
        return response

    def set_prohibit_binary_load(self, qProhibit: bool) -> object:
        """
        Prohibit binary load of this app.
        An app with prohibit binary load set cannot be loaded binary. For the setting to have effect a save is required.

        Parameters
        ----------
        qProhibit: bool
          True or false.
        """
        params = {}
        params["qProhibit"] = qProhibit
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetProhibitBinaryLoad", handle, **params)
        return response

    def transform_app(
        self, qDstParameters: TransformAppParameters
    ) -> TransformAppResult:
        """
        Transform current app into an instance of the targeted mode

        Parameters
        ----------
        qDstParameters: TransformAppParameters
          Attributes that should be set in the new app.
        """
        params = {}
        params["qDstParameters"] = qDstParameters
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("TransformApp", handle, **params)["qResult"]
        obj = TransformAppResult(**response)
        return obj

    def create_temporary_bookmark(
        self, qOptions: NxTempBookmarkOptions, qObjectIdsToPatch: list[str] = None
    ) -> CreateTemporaryBookmarkReturn:
        """
        Create temporary bookmark
        CreateTemporaryBookmark method is only supported in SaaS Editions of Qlik Sense.

        Parameters
        ----------
        qOptions: NxTempBookmarkOptions
          Options for the temporary bookmark
        qObjectIdsToPatch: list[str] = None
          Add softpatches for this objects if available. If empty all softpatches are added to the bookmark. This is ignored if IncludePatches is false.
        """
        params = {}
        params["qOptions"] = qOptions
        if qObjectIdsToPatch is not None:
            params["qObjectIdsToPatch"] = qObjectIdsToPatch
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateTemporaryBookmark", handle, **params)
        obj = CreateTemporaryBookmarkReturn(**response)
        return obj

    def apply_temporary_bookmark(self, qId: str) -> bool:
        """
        Apply temporary bookmark identified by Id.
        ApplyTemporaryBookmark method is only supported in SaaS Editions of Qlik Sense.

        Parameters
        ----------
        qId: str
          Identifier of the temporary selection state
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ApplyTemporaryBookmark", handle, **params)[
            "qReturn"
        ]
        return response

    def get_script_meta(self) -> AppScriptMeta:
        """
        Experimental
        Gets script meta-data.

        Parameters
        ----------
        """
        warnings.warn("GetScriptMeta is experimental", UserWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetScriptMeta", handle)["qMeta"]
        obj = AppScriptMeta(**response)
        return obj

    def replace_bookmark(
        self, qId: str, qIgnorePatches: bool = None, qObjectIdsToPatch: list[str] = None
    ) -> ObjectInterface:
        """
        Experimental
        Replace a bookmark. Optional inparams to change the original bookmarks properties, original are kept if left out.

        Parameters
        ----------
        qId: str
          Identifier of the bookmark.
        qIgnorePatches: bool = None
          Set to true to exclude patches from the bookmark. Default is false.
        qObjectIdsToPatch: list[str] = None
          Add softpatches for this objects if available. If empty all softpatches are added to the bookmark. Ignored if IgnorePatches is set to true.
        """
        warnings.warn("ReplaceBookmark is experimental", UserWarning, stacklevel=2)
        params = {}
        params["qId"] = qId
        if qIgnorePatches is not None:
            params["qIgnorePatches"] = qIgnorePatches
        if qObjectIdsToPatch is not None:
            params["qObjectIdsToPatch"] = qObjectIdsToPatch
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ReplaceBookmark", handle, **params)["qReturn"]
        obj = ObjectInterface(**response)
        return obj

    def clear_all_soft_patches(self) -> object:
        """
        Experimental
        Clear the soft properties of all generic objects in the app

        Parameters
        ----------
        """
        warnings.warn("ClearAllSoftPatches is experimental", UserWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ClearAllSoftPatches", handle)
        return response

    def commit_script(self, qCommitMessage: str = None) -> object:
        """
        Experimental
        Commits the current script version so that any future changes will be part of a new version.

        Parameters
        ----------
        qCommitMessage: str = None
          Name of the version.
           Only applicable to QCS.
        """
        warnings.warn("CommitScript is experimental", UserWarning, stacklevel=2)
        params = {}
        if qCommitMessage is not None:
            params["qCommitMessage"] = qCommitMessage
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CommitScript", handle, **params)
        return response

    def open(self, qNoData: bool = None) -> RpcSession:
        if not hasattr(self, "_session") or self._session is None:
            self._session = self.auth.rpc(self.attributes.id)
        session = self._session.open()
        params = {"qDocName": self.attributes.id}
        if qNoData is not None:
            params["qNoData"] = qNoData
        response = self._session.send("OpenDoc", -1, **params)["qReturn"]
        self.qGenericType = response["qType"]
        self.qGenericId = response["qGenericId"]
        self.qHandle = response["qHandle"]
        self.Global = Global(qType="global", qHandle=-1)
        self.Global._session = session
        return session

    def close(self) -> None:
        self._session.close()

    def on(self, event_name, listener):
        self._session.on_handle(self.qHandle, event_name, listener)


@dataclass
class DocListEntry:
    """

    Attributes
    ----------
    qConnectedUsers: int
      Not used.
    qDocId: str
      Identifier of the app.

      • In Qlik Sense Desktop, the identifier is the path and name of the app.

      • In Qlik Sense Enterprise, the identifier is the app's GUID.
    qDocName: str
      Name of the app.
    qFileSize: float
      Size of remote app.
      This property is used only with Qlik Sense Desktop.
      It is set to 0 for Qlik Sense Enterprise.
    qFileTime: float
      Last modified time stamp of the app.
      This property is used only with Qlik Sense Desktop.
      It is set to 0 for Qlik Sense Enterprise.
    qHasSectionAccess: bool
      If true the app has section access configured.
    qIsDirectQueryMode: bool
      Is the app a Direct Query app?
    qLastReloadTime: str
      Last reload time of the app.
    qMeta: NxMeta
      Meta data related to the app.
    qReadOnly: bool
      If set to true, the app is read-only.
    qThumbnail: StaticContentUrl
      Thumbnail of the app.
    qTitle: str
      Title of the app.
    qUsage: Literal["ANALYTICS_USAGE", "DATA_PREPARATION_USAGE"]

      One of:

      • ANALYTICS or ANALYTICS_USAGE

      • DATA_PREPARATION or DATA_PREPARATION_USAGE
    """

    qConnectedUsers: int = None
    qDocId: str = None
    qDocName: str = None
    qFileSize: float = None
    qFileTime: float = None
    qHasSectionAccess: bool = None
    qIsDirectQueryMode: bool = None
    qLastReloadTime: str = None
    qMeta: NxMeta = None
    qReadOnly: bool = None
    qThumbnail: StaticContentUrl = None
    qTitle: str = None
    qUsage: Literal["ANALYTICS_USAGE", "DATA_PREPARATION_USAGE"] = None

    def __init__(self_, **kvargs):
        if "qConnectedUsers" in kvargs and kvargs["qConnectedUsers"] is not None:
            self_.qConnectedUsers = kvargs["qConnectedUsers"]
        if "qDocId" in kvargs and kvargs["qDocId"] is not None:
            self_.qDocId = kvargs["qDocId"]
        if "qDocName" in kvargs and kvargs["qDocName"] is not None:
            self_.qDocName = kvargs["qDocName"]
        if "qFileSize" in kvargs and kvargs["qFileSize"] is not None:
            self_.qFileSize = kvargs["qFileSize"]
        if "qFileTime" in kvargs and kvargs["qFileTime"] is not None:
            self_.qFileTime = kvargs["qFileTime"]
        if "qHasSectionAccess" in kvargs and kvargs["qHasSectionAccess"] is not None:
            self_.qHasSectionAccess = kvargs["qHasSectionAccess"]
        if "qIsDirectQueryMode" in kvargs and kvargs["qIsDirectQueryMode"] is not None:
            self_.qIsDirectQueryMode = kvargs["qIsDirectQueryMode"]
        if "qLastReloadTime" in kvargs and kvargs["qLastReloadTime"] is not None:
            self_.qLastReloadTime = kvargs["qLastReloadTime"]
        if "qMeta" in kvargs and kvargs["qMeta"] is not None:
            if type(kvargs["qMeta"]).__name__ == DocListEntry.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeta"],
                )
        if "qReadOnly" in kvargs and kvargs["qReadOnly"] is not None:
            self_.qReadOnly = kvargs["qReadOnly"]
        if "qThumbnail" in kvargs and kvargs["qThumbnail"] is not None:
            if (
                type(kvargs["qThumbnail"]).__name__
                == DocListEntry.__annotations__["qThumbnail"]
            ):
                self_.qThumbnail = kvargs["qThumbnail"]
            else:
                self_.qThumbnail = StaticContentUrl(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qThumbnail"],
                )
        if "qTitle" in kvargs and kvargs["qTitle"] is not None:
            self_.qTitle = kvargs["qTitle"]
        if "qUsage" in kvargs and kvargs["qUsage"] is not None:
            self_.qUsage = kvargs["qUsage"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DriveInfo:
    """
  
  Attributes
  ----------
  qDrive: str
    Value of the drive.
    Examples:
    C:\\\, E:\\\
  qName: str
    Name of the drive.
  qType: str
    Type of the drive.
    Fixed means physical drive.
  qTypeIdentifier: Literal["REMOVABLE", "FIXED", "NETWORK", "CD_ROM", "RAM", "UNKNOWN_TYPE"]
    Information about the drive type.
    
    One of:
    
    • REMOVABLE
    
    • FIXED
    
    • NETWORK
    
    • CD_ROM
    
    • RAM
    
    • UNKNOWN_TYPE
  qUnnamedDrive: bool
  """

    qDrive: str = None
    qName: str = None
    qType: str = None
    qTypeIdentifier: Literal[
        "REMOVABLE", "FIXED", "NETWORK", "CD_ROM", "RAM", "UNKNOWN_TYPE"
    ] = None
    qUnnamedDrive: bool = None

    def __init__(self_, **kvargs):
        if "qDrive" in kvargs and kvargs["qDrive"] is not None:
            self_.qDrive = kvargs["qDrive"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        if "qTypeIdentifier" in kvargs and kvargs["qTypeIdentifier"] is not None:
            self_.qTypeIdentifier = kvargs["qTypeIdentifier"]
        if "qUnnamedDrive" in kvargs and kvargs["qUnnamedDrive"] is not None:
            self_.qUnnamedDrive = kvargs["qUnnamedDrive"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DriveType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EditorBreakpoint:
    """

    Attributes
    ----------
    qEnabled: bool
      If set to true then the breakpoint is enabled (in use).
    qbufferName: str
      Name of the breakpoint.
    qlineIx: int
      Line number in the script where the breakpoint is set.
    """

    qEnabled: bool = None
    qbufferName: str = None
    qlineIx: int = None

    def __init__(self_, **kvargs):
        if "qEnabled" in kvargs and kvargs["qEnabled"] is not None:
            self_.qEnabled = kvargs["qEnabled"]
        if "qbufferName" in kvargs and kvargs["qbufferName"] is not None:
            self_.qbufferName = kvargs["qbufferName"]
        if "qlineIx" in kvargs and kvargs["qlineIx"] is not None:
            self_.qlineIx = kvargs["qlineIx"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EmbeddedSnapshot:
    """
    Renders the embedded snapshot in an object.
    The following is returned:

    • Any dynamic properties defined in the bookmark

    • Any properties defined in qEmbeddedSnapshot

     Properties:
    "qEmbeddedSnapshot": {}

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EmbeddedSnapshotDef:
    """
    Defines the embedded snapshot in a generic object.

     Properties:
    "EmbeddedSnapshotDef": {}

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ErrorData:
    """

    Attributes
    ----------
    qErrorDataCode: Literal["EDC_ERROR", "EDC_WARNING", "EDC_CIRCULAR_REFERENCE"]
      Type of the error messages.

      One of:

      • EDC_ERROR

      • EDC_WARNING

      • EDC_CIRCULAR_REFERENCE
    qErrorString: str
      Detailed information about the error message.
    qLine: str
      Script statement where the error occurs.
    qLineEnd: str
      Line termination characters.
    qMessage: ProgressMessage
    """

    qErrorDataCode: Literal["EDC_ERROR", "EDC_WARNING", "EDC_CIRCULAR_REFERENCE"] = None
    qErrorString: str = None
    qLine: str = None
    qLineEnd: str = None
    qMessage: ProgressMessage = None

    def __init__(self_, **kvargs):
        if "qErrorDataCode" in kvargs and kvargs["qErrorDataCode"] is not None:
            self_.qErrorDataCode = kvargs["qErrorDataCode"]
        if "qErrorString" in kvargs and kvargs["qErrorString"] is not None:
            self_.qErrorString = kvargs["qErrorString"]
        if "qLine" in kvargs and kvargs["qLine"] is not None:
            self_.qLine = kvargs["qLine"]
        if "qLineEnd" in kvargs and kvargs["qLineEnd"] is not None:
            self_.qLineEnd = kvargs["qLineEnd"]
        if "qMessage" in kvargs and kvargs["qMessage"] is not None:
            if (
                type(kvargs["qMessage"]).__name__
                == ErrorData.__annotations__["qMessage"]
            ):
                self_.qMessage = kvargs["qMessage"]
            else:
                self_.qMessage = ProgressMessage(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMessage"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ErrorDataCode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ExpansionData:
    """

    Attributes
    ----------
    qExcludeList: bool
    qPos: PositionMark
    """

    qExcludeList: bool = None
    qPos: PositionMark = None

    def __init__(self_, **kvargs):
        if "qExcludeList" in kvargs and kvargs["qExcludeList"] is not None:
            self_.qExcludeList = kvargs["qExcludeList"]
        if "qPos" in kvargs and kvargs["qPos"] is not None:
            if type(kvargs["qPos"]).__name__ == ExpansionData.__annotations__["qPos"]:
                self_.qPos = kvargs["qPos"]
            else:
                self_.qPos = PositionMark(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qPos"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ExportDataReturn:
    """

    Attributes
    ----------
    qUrl: str
    qWarnings: list[int]
    """

    qUrl: str = None
    qWarnings: list[int] = None

    def __init__(self_, **kvargs):
        if "qUrl" in kvargs and kvargs["qUrl"] is not None:
            self_.qUrl = kvargs["qUrl"]
        if "qWarnings" in kvargs and kvargs["qWarnings"] is not None:
            self_.qWarnings = kvargs["qWarnings"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ExtendedLayoutBookmarkData:
    """

    Attributes
    ----------
    qActive: bool
    qActiveContainerChildObjectId: str
    qDimensionGroupPos: list[GroupStateInfo]
    qExpansionInfo: list[ExpansionData]
    qExpressionGroupPos: list[GroupStateInfo]
    qExtendedPivotState: ExtendedPivotStateData
    qGraphMode: Literal["GRAPH_MODE_BAR", "GRAPH_MODE_PIE", "GRAPH_MODE_PIVOTTABLE", "GRAPH_MODE_SCATTER", "GRAPH_MODE_LINE", "GRAPH_MODE_STRAIGHTTABLE", "GRAPH_MODE_COMBO", "GRAPH_MODE_RADAR", "GRAPH_MODE_GAUGE", "GRAPH_MODE_GRID", "GRAPH_MODE_BLOCK", "GRAPH_MODE_FUNNEL", "GRAPH_MODE_MEKKO", "GRAPH_MODE_LAST"]

      One of:

      • GRAPH_MODE_BAR

      • GRAPH_MODE_PIE

      • GRAPH_MODE_PIVOTTABLE

      • GRAPH_MODE_SCATTER

      • GRAPH_MODE_LINE

      • GRAPH_MODE_STRAIGHTTABLE

      • GRAPH_MODE_COMBO

      • GRAPH_MODE_RADAR

      • GRAPH_MODE_GAUGE

      • GRAPH_MODE_GRID

      • GRAPH_MODE_BLOCK

      • GRAPH_MODE_FUNNEL

      • GRAPH_MODE_MEKKO

      • GRAPH_MODE_LAST
    qId: str
    qLeftCollapsed: bool
    qScrollPos: ScrollPosition
    qShowMode: int
    qSortData: list[InterFieldSortData]
    qTopCollapsed: bool
    qUseGraphMode: bool
    """

    qActive: bool = None
    qActiveContainerChildObjectId: str = None
    qDimensionGroupPos: list[GroupStateInfo] = None
    qExpansionInfo: list[ExpansionData] = None
    qExpressionGroupPos: list[GroupStateInfo] = None
    qExtendedPivotState: ExtendedPivotStateData = None
    qGraphMode: Literal[
        "GRAPH_MODE_BAR",
        "GRAPH_MODE_PIE",
        "GRAPH_MODE_PIVOTTABLE",
        "GRAPH_MODE_SCATTER",
        "GRAPH_MODE_LINE",
        "GRAPH_MODE_STRAIGHTTABLE",
        "GRAPH_MODE_COMBO",
        "GRAPH_MODE_RADAR",
        "GRAPH_MODE_GAUGE",
        "GRAPH_MODE_GRID",
        "GRAPH_MODE_BLOCK",
        "GRAPH_MODE_FUNNEL",
        "GRAPH_MODE_MEKKO",
        "GRAPH_MODE_LAST",
    ] = None
    qId: str = None
    qLeftCollapsed: bool = None
    qScrollPos: ScrollPosition = None
    qShowMode: int = None
    qSortData: list[InterFieldSortData] = None
    qTopCollapsed: bool = None
    qUseGraphMode: bool = None

    def __init__(self_, **kvargs):
        if "qActive" in kvargs and kvargs["qActive"] is not None:
            self_.qActive = kvargs["qActive"]
        if (
            "qActiveContainerChildObjectId" in kvargs
            and kvargs["qActiveContainerChildObjectId"] is not None
        ):
            self_.qActiveContainerChildObjectId = kvargs[
                "qActiveContainerChildObjectId"
            ]
        if "qDimensionGroupPos" in kvargs and kvargs["qDimensionGroupPos"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == ExtendedLayoutBookmarkData.__annotations__["qDimensionGroupPos"]
                for e in kvargs["qDimensionGroupPos"]
            ):
                self_.qDimensionGroupPos = kvargs["qDimensionGroupPos"]
            else:
                self_.qDimensionGroupPos = [
                    GroupStateInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qDimensionGroupPos"]
                ]
        if "qExpansionInfo" in kvargs and kvargs["qExpansionInfo"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == ExtendedLayoutBookmarkData.__annotations__["qExpansionInfo"]
                for e in kvargs["qExpansionInfo"]
            ):
                self_.qExpansionInfo = kvargs["qExpansionInfo"]
            else:
                self_.qExpansionInfo = [
                    ExpansionData(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qExpansionInfo"]
                ]
        if (
            "qExpressionGroupPos" in kvargs
            and kvargs["qExpressionGroupPos"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == ExtendedLayoutBookmarkData.__annotations__["qExpressionGroupPos"]
                for e in kvargs["qExpressionGroupPos"]
            ):
                self_.qExpressionGroupPos = kvargs["qExpressionGroupPos"]
            else:
                self_.qExpressionGroupPos = [
                    GroupStateInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qExpressionGroupPos"]
                ]
        if (
            "qExtendedPivotState" in kvargs
            and kvargs["qExtendedPivotState"] is not None
        ):
            if (
                type(kvargs["qExtendedPivotState"]).__name__
                == ExtendedLayoutBookmarkData.__annotations__["qExtendedPivotState"]
            ):
                self_.qExtendedPivotState = kvargs["qExtendedPivotState"]
            else:
                self_.qExtendedPivotState = ExtendedPivotStateData(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qExtendedPivotState"],
                )
        if "qGraphMode" in kvargs and kvargs["qGraphMode"] is not None:
            self_.qGraphMode = kvargs["qGraphMode"]
        if "qId" in kvargs and kvargs["qId"] is not None:
            self_.qId = kvargs["qId"]
        if "qLeftCollapsed" in kvargs and kvargs["qLeftCollapsed"] is not None:
            self_.qLeftCollapsed = kvargs["qLeftCollapsed"]
        if "qScrollPos" in kvargs and kvargs["qScrollPos"] is not None:
            if (
                type(kvargs["qScrollPos"]).__name__
                == ExtendedLayoutBookmarkData.__annotations__["qScrollPos"]
            ):
                self_.qScrollPos = kvargs["qScrollPos"]
            else:
                self_.qScrollPos = ScrollPosition(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qScrollPos"],
                )
        if "qShowMode" in kvargs and kvargs["qShowMode"] is not None:
            self_.qShowMode = kvargs["qShowMode"]
        if "qSortData" in kvargs and kvargs["qSortData"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == ExtendedLayoutBookmarkData.__annotations__["qSortData"]
                for e in kvargs["qSortData"]
            ):
                self_.qSortData = kvargs["qSortData"]
            else:
                self_.qSortData = [
                    InterFieldSortData(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qSortData"]
                ]
        if "qTopCollapsed" in kvargs and kvargs["qTopCollapsed"] is not None:
            self_.qTopCollapsed = kvargs["qTopCollapsed"]
        if "qUseGraphMode" in kvargs and kvargs["qUseGraphMode"] is not None:
            self_.qUseGraphMode = kvargs["qUseGraphMode"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ExtendedPivotStateData:
    """

    Attributes
    ----------
    qDimensionNames: list[str]
    qEnableConditions: list[str]
    qExpressionPosition: int
    qNumberOfLeftDimensions: int
    """

    qDimensionNames: list[str] = None
    qEnableConditions: list[str] = None
    qExpressionPosition: int = None
    qNumberOfLeftDimensions: int = None

    def __init__(self_, **kvargs):
        if "qDimensionNames" in kvargs and kvargs["qDimensionNames"] is not None:
            self_.qDimensionNames = kvargs["qDimensionNames"]
        if "qEnableConditions" in kvargs and kvargs["qEnableConditions"] is not None:
            self_.qEnableConditions = kvargs["qEnableConditions"]
        if (
            "qExpressionPosition" in kvargs
            and kvargs["qExpressionPosition"] is not None
        ):
            self_.qExpressionPosition = kvargs["qExpressionPosition"]
        if (
            "qNumberOfLeftDimensions" in kvargs
            and kvargs["qNumberOfLeftDimensions"] is not None
        ):
            self_.qNumberOfLeftDimensions = kvargs["qNumberOfLeftDimensions"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ExtensionList:
    """
    Obsolete, use qrs API's to fetch extensions.

    Attributes
    ----------
    qItems: list[str]
    """

    qItems: list[str] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs and kvargs["qItems"] is not None:
            self_.qItems = kvargs["qItems"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ExtensionListDef:
    """
    Obsolete, use qrs API's to fetch extensions.

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Field:
    """

    Attributes
    ----------
    qGenericId: str
      Object ID.
    qGenericType: str
      The type of the object.
    qHandle: int
      The handle used to connect to object.
    qType: str
      The native type of the object.
    """

    _session: RpcSession = None
    qGenericId: str = None
    qGenericType: str = None
    qHandle: int = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qGenericId" in kvargs and kvargs["qGenericId"] is not None:
            self_.qGenericId = kvargs["qGenericId"]
        if "qGenericType" in kvargs and kvargs["qGenericType"] is not None:
            self_.qGenericType = kvargs["qGenericType"]
        if "qHandle" in kvargs and kvargs["qHandle"] is not None:
            self_.qHandle = kvargs["qHandle"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}) or k == "_session":
                self_.__setattr__(k, v)

    def get_cardinal(self) -> int:
        """
        Retrieves the number of distinct values in a field.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetCardinal", handle)["qReturn"]
        return response

    def get_and_mode(self) -> bool:
        """
        Returns the AND mode status of a field.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetAndMode", handle)["qReturn"]
        return response

    def select_values(
        self,
        qFieldValues: list[FieldValue],
        qToggleMode: bool = None,
        qSoftLock: bool = None,
    ) -> bool:
        """
        Selects some values in a field, by entering the values to select.

        Parameters
        ----------
        qFieldValues: list[FieldValue]
          List of the values to select.
        qToggleMode: bool = None
          The default value is false.
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.
        """
        params = {}
        params["qFieldValues"] = qFieldValues
        if qToggleMode is not None:
            params["qToggleMode"] = qToggleMode
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectValues", handle, **params)["qReturn"]
        return response

    def select(
        self, qMatch: str, qSoftLock: bool = None, qExcludedValuesMode: int = None
    ) -> bool:
        """
        Selects field values matching a search string.

        Parameters
        ----------
        qMatch: str
          String to search for.
          Can contain wild cards or numeric search criteria.
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.
        qExcludedValuesMode: int = None
          Include excluded values in search.
        """
        params = {}
        params["qMatch"] = qMatch
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        if qExcludedValuesMode is not None:
            params["qExcludedValuesMode"] = qExcludedValuesMode
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Select", handle, **params)["qReturn"]
        return response

    def toggle_select(
        self, qMatch: str, qSoftLock: bool = None, qExcludedValuesMode: int = None
    ) -> bool:
        """
        Toggle selects field values matching a search string.

        Parameters
        ----------
        qMatch: str
          String to search for.
          Can contain wild cards or numeric search criteria.
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.
        qExcludedValuesMode: int = None
          Include excluded values in search.
        """
        params = {}
        params["qMatch"] = qMatch
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        if qExcludedValuesMode is not None:
            params["qExcludedValuesMode"] = qExcludedValuesMode
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ToggleSelect", handle, **params)["qReturn"]
        return response

    def clear_all_but_this(self, qSoftLock: bool = None) -> bool:
        """
        Maintains the selections in the current field while clearing the selections in the other fields.

        Parameters
        ----------
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.
        """
        params = {}
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ClearAllButThis", handle, **params)["qReturn"]
        return response

    def select_possible(self, qSoftLock: bool = None) -> bool:
        """
        Selects all possible values in a specific field.

        Parameters
        ----------
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.
        """
        params = {}
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectPossible", handle, **params)["qReturn"]
        return response

    def select_excluded(self, qSoftLock: bool = None) -> bool:
        """
        Inverts the current selections.

        Parameters
        ----------
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.
        """
        params = {}
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectExcluded", handle, **params)["qReturn"]
        return response

    def select_all(self, qSoftLock: bool = None) -> bool:
        """
        Selects all values of a field. Excluded values are also selected.

        Parameters
        ----------
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.
        """
        params = {}
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectAll", handle, **params)["qReturn"]
        return response

    def lock(self) -> bool:
        """
        Locks all selected values of a specific field.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Lock", handle)["qReturn"]
        return response

    def unlock(self) -> bool:
        """
        Unlocks all selected values of a specific field if the target (or handle ) is a field.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Unlock", handle)["qReturn"]
        return response

    def get_nx_properties(self) -> NxFieldProperties:
        """
        Gets the properties of a field.

        The property OneAndOnlyOne is set to true if one and only value has been selected in the field prior setting the property.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetNxProperties", handle)["qProperties"]
        obj = NxFieldProperties(**response)
        return obj

    def set_nx_properties(self, qProperties: NxFieldProperties) -> object:
        """
        Sets some properties to a field.

        Parameters
        ----------
        qProperties: NxFieldProperties
          Information about the properties of the field.
        """
        params = {}
        params["qProperties"] = qProperties
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetNxProperties", handle, **params)
        return response

    def set_and_mode(self, qAndMode: bool) -> object:
        """
        Sets a field in the AND mode.

        Parameters
        ----------
        qAndMode: bool
          Specifies if the AND mode applies to the field.
          Set this parameter to true to enter the AND mode.
        """
        params = {}
        params["qAndMode"] = qAndMode
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetAndMode", handle, **params)
        return response

    def select_alternative(self, qSoftLock: bool = None) -> bool:
        """
        Selects all alternatives values in a specific field.
        In a field that contains at least one selected value, the values that are neither selected nor excluded are alternatives values.

        Parameters
        ----------
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.
        """
        params = {}
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectAlternative", handle, **params)["qReturn"]
        return response

    def low_level_select(
        self, qValues: list[int], qToggleMode: bool, qSoftLock: bool = None
    ) -> bool:
        """
        Selects some values in a field, by entering the element numbers related to the values to select.

        Parameters
        ----------
        qValues: list[int]
          Indexes (or element numbers) of the values to select.
        qToggleMode: bool
          Set to true to keep any selections present in the list object.
          If this parameter is set to false, selections made before accepting the list object search become alternative.
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.
        """
        params = {}
        params["qValues"] = qValues
        params["qToggleMode"] = qToggleMode
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("LowLevelSelect", handle, **params)["qReturn"]
        return response

    def clear(self) -> bool:
        """
        Clears the selections in a specific field.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Clear", handle)["qReturn"]
        return response

    def on(self, event_name, listener):
        self._session.on_handle(self.qHandle, event_name, listener)


@dataclass
class FieldAttrType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
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
    qDec: str
      Defines the decimal separator.
      Example: .
    qFmt: str
      Defines the format pattern that applies to qText .
      Is used in connection to the type of the field (parameter qType ).
      For more information, see Formatting mechanism.
      Example: YYYY-MM-DD for a date.
    qThou: str
      Defines the thousand separator (if any).
      Is used if qUseThou is set to 1.
      Example: ,
    qType: Literal["UNKNOWN", "ASCII", "INTEGER", "REAL", "FIX", "MONEY", "DATE", "TIME", "TIMESTAMP", "INTERVAL"]
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
    qUseThou: int
      Defines whether or not a thousands separator must be used.
      Default is 0.
    qnDec: int
      Number of decimals.
      Default is 10.
    """

    qDec: str = None
    qFmt: str = None
    qThou: str = None
    qType: Literal[
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
    qUseThou: int = None
    qnDec: int = 10

    def __init__(self_, **kvargs):
        if "qDec" in kvargs and kvargs["qDec"] is not None:
            self_.qDec = kvargs["qDec"]
        if "qFmt" in kvargs and kvargs["qFmt"] is not None:
            self_.qFmt = kvargs["qFmt"]
        if "qThou" in kvargs and kvargs["qThou"] is not None:
            self_.qThou = kvargs["qThou"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        if "qUseThou" in kvargs and kvargs["qUseThou"] is not None:
            self_.qUseThou = kvargs["qUseThou"]
        if "qnDec" in kvargs and kvargs["qnDec"] is not None:
            self_.qnDec = kvargs["qnDec"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldDefEx:
    """

    Attributes
    ----------
    qName: str
      Name of the field.
    qType: Literal["NOT_PRESENT", "PRESENT", "IS_CYCLIC_GROUP", "IS_DRILL_GROUP", "IS_VAR", "IS_EXPR", "IS_IMPLICIT", "IS_DETAIL"]
      Type of data entity.

      One of:

      • NOT_PRESENT

      • PRESENT

      • IS_CYCLIC_GROUP

      • IS_DRILL_GROUP

      • IS_VAR

      • IS_EXPR

      • IS_IMPLICIT

      • IS_DETAIL
    """

    qName: str = None
    qType: Literal[
        "NOT_PRESENT",
        "PRESENT",
        "IS_CYCLIC_GROUP",
        "IS_DRILL_GROUP",
        "IS_VAR",
        "IS_EXPR",
        "IS_IMPLICIT",
        "IS_DETAIL",
    ] = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldDescription:
    """

    Attributes
    ----------
    qAlwaysOneSelected: bool
      If set to true, it means that the field has one and only one selection (not 0 and not more than 1).
      If this property is set to true, the field cannot be cleared anymore and no more selections can be performed in that field.
      The default value is false.
    qAndMode: bool
      If set to true a logical AND (instead of a logical OR) is used when making selections in a field.
      The default value is false.
    qByteSize: int
      Static RAM memory used in bytes.
    qCardinal: int
      Number of distinct field values.
    qComment: str
      Field comment.
    qDistinctOnly: bool
      If set to true, only distinct field values are shown.
      The default value is false.
    qHasInfo_OBSOLETE: bool
    qInternalNumber: int
      Internal number of the field.
    qIsDefinitionOnly: bool
      If set to true, it means that the field is a field on the fly.
      The default value is false.
    qIsHidden: bool
      If set to true, it means that the field is hidden.
      The default value is false.
    qIsLocked: bool
      If set to true, it means that the field is locked.
      The default value is false.
    qIsNumeric: bool
      Is set to true if the value is a numeric.
      The default value is false.
    qIsSemantic: bool
      If set to true, it means that the field is a semantic.
      The default value is false.
    qIsSystem: bool
      If set to true, it means that the field is a system field.
      The default value is false.
    qName: str
      Name of the field.
    qPossibleCount_OBSOLETE: int
    qSrcTables: list[str]
      List of table names.
    qTags: list[str]
      Gives information on a field. For example, it can return the type of the field.
      Examples: key, text, ASCII.
    qTotalCount: int
      Total number of field values.
    """

    qAlwaysOneSelected: bool = None
    qAndMode: bool = None
    qByteSize: int = None
    qCardinal: int = None
    qComment: str = None
    qDistinctOnly: bool = None
    qHasInfo_OBSOLETE: bool = None
    qInternalNumber: int = None
    qIsDefinitionOnly: bool = None
    qIsHidden: bool = None
    qIsLocked: bool = None
    qIsNumeric: bool = None
    qIsSemantic: bool = None
    qIsSystem: bool = None
    qName: str = None
    qPossibleCount_OBSOLETE: int = None
    qSrcTables: list[str] = None
    qTags: list[str] = None
    qTotalCount: int = None

    def __init__(self_, **kvargs):
        if "qAlwaysOneSelected" in kvargs and kvargs["qAlwaysOneSelected"] is not None:
            self_.qAlwaysOneSelected = kvargs["qAlwaysOneSelected"]
        if "qAndMode" in kvargs and kvargs["qAndMode"] is not None:
            self_.qAndMode = kvargs["qAndMode"]
        if "qByteSize" in kvargs and kvargs["qByteSize"] is not None:
            self_.qByteSize = kvargs["qByteSize"]
        if "qCardinal" in kvargs and kvargs["qCardinal"] is not None:
            self_.qCardinal = kvargs["qCardinal"]
        if "qComment" in kvargs and kvargs["qComment"] is not None:
            self_.qComment = kvargs["qComment"]
        if "qDistinctOnly" in kvargs and kvargs["qDistinctOnly"] is not None:
            self_.qDistinctOnly = kvargs["qDistinctOnly"]
        if "qHasInfo_OBSOLETE" in kvargs and kvargs["qHasInfo_OBSOLETE"] is not None:
            self_.qHasInfo_OBSOLETE = kvargs["qHasInfo_OBSOLETE"]
        if "qInternalNumber" in kvargs and kvargs["qInternalNumber"] is not None:
            self_.qInternalNumber = kvargs["qInternalNumber"]
        if "qIsDefinitionOnly" in kvargs and kvargs["qIsDefinitionOnly"] is not None:
            self_.qIsDefinitionOnly = kvargs["qIsDefinitionOnly"]
        if "qIsHidden" in kvargs and kvargs["qIsHidden"] is not None:
            self_.qIsHidden = kvargs["qIsHidden"]
        if "qIsLocked" in kvargs and kvargs["qIsLocked"] is not None:
            self_.qIsLocked = kvargs["qIsLocked"]
        if "qIsNumeric" in kvargs and kvargs["qIsNumeric"] is not None:
            self_.qIsNumeric = kvargs["qIsNumeric"]
        if "qIsSemantic" in kvargs and kvargs["qIsSemantic"] is not None:
            self_.qIsSemantic = kvargs["qIsSemantic"]
        if "qIsSystem" in kvargs and kvargs["qIsSystem"] is not None:
            self_.qIsSystem = kvargs["qIsSystem"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if (
            "qPossibleCount_OBSOLETE" in kvargs
            and kvargs["qPossibleCount_OBSOLETE"] is not None
        ):
            self_.qPossibleCount_OBSOLETE = kvargs["qPossibleCount_OBSOLETE"]
        if "qSrcTables" in kvargs and kvargs["qSrcTables"] is not None:
            self_.qSrcTables = kvargs["qSrcTables"]
        if "qTags" in kvargs and kvargs["qTags"] is not None:
            self_.qTags = kvargs["qTags"]
        if "qTotalCount" in kvargs and kvargs["qTotalCount"] is not None:
            self_.qTotalCount = kvargs["qTotalCount"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldInTableData:
    """

    Attributes
    ----------
    qComment: str
      Comment related to the field.
    qDerivedFields: list[DerivedFieldsInTableData]
      List of the derived fields.
    qHasDuplicates: bool
      This property is set to true if the field contains some duplicate values.
    qHasNull: bool
      This property is set to true if the field contains some Null values.
    qHasWild: bool
    qInformationDensity: float
      Number of records that have values (for example, not NULL) in the field as compared to the total number of records in the table.
    qIsFieldOnTheFly: bool
    qIsSynthetic: bool
      This property is set to true if the field contains a synthetic key.
    qKeyType: Literal["NOT_KEY", "ANY_KEY", "PRIMARY_KEY", "PERFECT_KEY"]
      Tells if the field is a key field.

      One of:

      • NOT_KEY

      • ANY_KEY

      • PRIMARY_KEY

      • PERFECT_KEY
    qName: str
      Name of the field.
    qOriginalFields: list[str]
      Is shown for fixed records.
      qOriginalFieldName and qName are identical if no field names are used in the file.
      qOriginalFieldName differs from qName if embedded file names are used in the file.
    qPresent: bool
    qReadableName: str
    qSubsetRatio: float
      Number of distinct values in the field (in the current table) as compared to the total number of distinct values of this field (in all tables).
    qTags: list[str]
      List of tags related to the field.
    qnNonNulls: int
      Number of values that are non Null.
    qnPresentDistinctValues: int
    qnRows: int
      Number of rows in the field.
    qnTotalDistinctValues: int
      Number of distinct values in the field.
    """

    qComment: str = None
    qDerivedFields: list[DerivedFieldsInTableData] = None
    qHasDuplicates: bool = None
    qHasNull: bool = None
    qHasWild: bool = None
    qInformationDensity: float = None
    qIsFieldOnTheFly: bool = None
    qIsSynthetic: bool = None
    qKeyType: Literal["NOT_KEY", "ANY_KEY", "PRIMARY_KEY", "PERFECT_KEY"] = None
    qName: str = None
    qOriginalFields: list[str] = None
    qPresent: bool = None
    qReadableName: str = None
    qSubsetRatio: float = None
    qTags: list[str] = None
    qnNonNulls: int = None
    qnPresentDistinctValues: int = None
    qnRows: int = None
    qnTotalDistinctValues: int = None

    def __init__(self_, **kvargs):
        if "qComment" in kvargs and kvargs["qComment"] is not None:
            self_.qComment = kvargs["qComment"]
        if "qDerivedFields" in kvargs and kvargs["qDerivedFields"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == FieldInTableData.__annotations__["qDerivedFields"]
                for e in kvargs["qDerivedFields"]
            ):
                self_.qDerivedFields = kvargs["qDerivedFields"]
            else:
                self_.qDerivedFields = [
                    DerivedFieldsInTableData(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qDerivedFields"]
                ]
        if "qHasDuplicates" in kvargs and kvargs["qHasDuplicates"] is not None:
            self_.qHasDuplicates = kvargs["qHasDuplicates"]
        if "qHasNull" in kvargs and kvargs["qHasNull"] is not None:
            self_.qHasNull = kvargs["qHasNull"]
        if "qHasWild" in kvargs and kvargs["qHasWild"] is not None:
            self_.qHasWild = kvargs["qHasWild"]
        if (
            "qInformationDensity" in kvargs
            and kvargs["qInformationDensity"] is not None
        ):
            self_.qInformationDensity = kvargs["qInformationDensity"]
        if "qIsFieldOnTheFly" in kvargs and kvargs["qIsFieldOnTheFly"] is not None:
            self_.qIsFieldOnTheFly = kvargs["qIsFieldOnTheFly"]
        if "qIsSynthetic" in kvargs and kvargs["qIsSynthetic"] is not None:
            self_.qIsSynthetic = kvargs["qIsSynthetic"]
        if "qKeyType" in kvargs and kvargs["qKeyType"] is not None:
            self_.qKeyType = kvargs["qKeyType"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qOriginalFields" in kvargs and kvargs["qOriginalFields"] is not None:
            self_.qOriginalFields = kvargs["qOriginalFields"]
        if "qPresent" in kvargs and kvargs["qPresent"] is not None:
            self_.qPresent = kvargs["qPresent"]
        if "qReadableName" in kvargs and kvargs["qReadableName"] is not None:
            self_.qReadableName = kvargs["qReadableName"]
        if "qSubsetRatio" in kvargs and kvargs["qSubsetRatio"] is not None:
            self_.qSubsetRatio = kvargs["qSubsetRatio"]
        if "qTags" in kvargs and kvargs["qTags"] is not None:
            self_.qTags = kvargs["qTags"]
        if "qnNonNulls" in kvargs and kvargs["qnNonNulls"] is not None:
            self_.qnNonNulls = kvargs["qnNonNulls"]
        if (
            "qnPresentDistinctValues" in kvargs
            and kvargs["qnPresentDistinctValues"] is not None
        ):
            self_.qnPresentDistinctValues = kvargs["qnPresentDistinctValues"]
        if "qnRows" in kvargs and kvargs["qnRows"] is not None:
            self_.qnRows = kvargs["qnRows"]
        if (
            "qnTotalDistinctValues" in kvargs
            and kvargs["qnTotalDistinctValues"] is not None
        ):
            self_.qnTotalDistinctValues = kvargs["qnTotalDistinctValues"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldInTableProfilingData:
    """

    Attributes
    ----------
    qAverage: float
      Average of all numerical values. NaN otherwise.
    qAvgStringLen: float
      Average string length of textual values. 0 otherwise.
    qDistinctNumericValues: int
      Number of distinct numeric values
    qDistinctTextValues: int
      Number of distinct text values
    qDistinctValues: int
      Number of distinct values
    qEmptyStrings: int
      Number of empty strings
    qFieldTags: list[str]
      List of tags related to the field.
    qFirstSorted: str
      For textual values the first sorted string.
    qFractiles: list[float]
      The .01, .05, .1, .25, .5, .75, .9, .95, .99 fractiles. Array of NaN otherwise.
    qFrequencyDistribution: FrequencyDistributionData
      Frequency Distribution for numeric fields.
    qKurtosis: float
      Kurtosis of the numerical values. NaN otherwise.
    qLastSorted: str
      For textual values the last sorted string.
    qMax: float
      Maximum value of numerical values. NaN otherwise.
    qMaxStringLen: int
      Maximum string length of textual values. 0 otherwise.
    qMedian: float
      Median of all numerical values. NaN otherwise.
    qMin: float
      Minimum value of numerical values. NaN otherwise.
    qMinStringLen: int
      Minimum string length of textual values. 0 otherwise.
    qMostFrequent: list[SymbolFrequency]
      Three most frequent values and their frequencies
    qName: str
      Name of the field.
    qNegValues: int
      Number of negative values
    qNullValues: int
      Number of null values
    qNumberFormat: FieldAttributes
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
    qNumericValues: int
      Number of numeric values
    qPosValues: int
      Number of positive values
    qSkewness: float
      Skewness of the numerical values. NaN otherwise.
    qStd: float
      Standard deviation of numerical values. NaN otherwise.
    qSum: float
      Sum of all numerical values. NaN otherwise.
    qSum2: float
      Squared sum of all numerical values. NaN otherwise.
    qSumStringLen: int
      Sum of all characters in strings in the field
    qTextValues: int
      Number of textual values
    qZeroValues: int
      Number of zero values for numerical values
    """

    qAverage: float = None
    qAvgStringLen: float = None
    qDistinctNumericValues: int = None
    qDistinctTextValues: int = None
    qDistinctValues: int = None
    qEmptyStrings: int = None
    qFieldTags: list[str] = None
    qFirstSorted: str = None
    qFractiles: list[float] = None
    qFrequencyDistribution: FrequencyDistributionData = None
    qKurtosis: float = None
    qLastSorted: str = None
    qMax: float = None
    qMaxStringLen: int = None
    qMedian: float = None
    qMin: float = None
    qMinStringLen: int = None
    qMostFrequent: list[SymbolFrequency] = None
    qName: str = None
    qNegValues: int = None
    qNullValues: int = None
    qNumberFormat: FieldAttributes = None
    qNumericValues: int = None
    qPosValues: int = None
    qSkewness: float = None
    qStd: float = None
    qSum: float = None
    qSum2: float = None
    qSumStringLen: int = None
    qTextValues: int = None
    qZeroValues: int = None

    def __init__(self_, **kvargs):
        if "qAverage" in kvargs and kvargs["qAverage"] is not None:
            self_.qAverage = kvargs["qAverage"]
        if "qAvgStringLen" in kvargs and kvargs["qAvgStringLen"] is not None:
            self_.qAvgStringLen = kvargs["qAvgStringLen"]
        if (
            "qDistinctNumericValues" in kvargs
            and kvargs["qDistinctNumericValues"] is not None
        ):
            self_.qDistinctNumericValues = kvargs["qDistinctNumericValues"]
        if (
            "qDistinctTextValues" in kvargs
            and kvargs["qDistinctTextValues"] is not None
        ):
            self_.qDistinctTextValues = kvargs["qDistinctTextValues"]
        if "qDistinctValues" in kvargs and kvargs["qDistinctValues"] is not None:
            self_.qDistinctValues = kvargs["qDistinctValues"]
        if "qEmptyStrings" in kvargs and kvargs["qEmptyStrings"] is not None:
            self_.qEmptyStrings = kvargs["qEmptyStrings"]
        if "qFieldTags" in kvargs and kvargs["qFieldTags"] is not None:
            self_.qFieldTags = kvargs["qFieldTags"]
        if "qFirstSorted" in kvargs and kvargs["qFirstSorted"] is not None:
            self_.qFirstSorted = kvargs["qFirstSorted"]
        if "qFractiles" in kvargs and kvargs["qFractiles"] is not None:
            self_.qFractiles = kvargs["qFractiles"]
        if (
            "qFrequencyDistribution" in kvargs
            and kvargs["qFrequencyDistribution"] is not None
        ):
            if (
                type(kvargs["qFrequencyDistribution"]).__name__
                == FieldInTableProfilingData.__annotations__["qFrequencyDistribution"]
            ):
                self_.qFrequencyDistribution = kvargs["qFrequencyDistribution"]
            else:
                self_.qFrequencyDistribution = FrequencyDistributionData(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qFrequencyDistribution"],
                )
        if "qKurtosis" in kvargs and kvargs["qKurtosis"] is not None:
            self_.qKurtosis = kvargs["qKurtosis"]
        if "qLastSorted" in kvargs and kvargs["qLastSorted"] is not None:
            self_.qLastSorted = kvargs["qLastSorted"]
        if "qMax" in kvargs and kvargs["qMax"] is not None:
            self_.qMax = kvargs["qMax"]
        if "qMaxStringLen" in kvargs and kvargs["qMaxStringLen"] is not None:
            self_.qMaxStringLen = kvargs["qMaxStringLen"]
        if "qMedian" in kvargs and kvargs["qMedian"] is not None:
            self_.qMedian = kvargs["qMedian"]
        if "qMin" in kvargs and kvargs["qMin"] is not None:
            self_.qMin = kvargs["qMin"]
        if "qMinStringLen" in kvargs and kvargs["qMinStringLen"] is not None:
            self_.qMinStringLen = kvargs["qMinStringLen"]
        if "qMostFrequent" in kvargs and kvargs["qMostFrequent"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == FieldInTableProfilingData.__annotations__["qMostFrequent"]
                for e in kvargs["qMostFrequent"]
            ):
                self_.qMostFrequent = kvargs["qMostFrequent"]
            else:
                self_.qMostFrequent = [
                    SymbolFrequency(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qMostFrequent"]
                ]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qNegValues" in kvargs and kvargs["qNegValues"] is not None:
            self_.qNegValues = kvargs["qNegValues"]
        if "qNullValues" in kvargs and kvargs["qNullValues"] is not None:
            self_.qNullValues = kvargs["qNullValues"]
        if "qNumberFormat" in kvargs and kvargs["qNumberFormat"] is not None:
            if (
                type(kvargs["qNumberFormat"]).__name__
                == FieldInTableProfilingData.__annotations__["qNumberFormat"]
            ):
                self_.qNumberFormat = kvargs["qNumberFormat"]
            else:
                self_.qNumberFormat = FieldAttributes(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qNumberFormat"],
                )
        if "qNumericValues" in kvargs and kvargs["qNumericValues"] is not None:
            self_.qNumericValues = kvargs["qNumericValues"]
        if "qPosValues" in kvargs and kvargs["qPosValues"] is not None:
            self_.qPosValues = kvargs["qPosValues"]
        if "qSkewness" in kvargs and kvargs["qSkewness"] is not None:
            self_.qSkewness = kvargs["qSkewness"]
        if "qStd" in kvargs and kvargs["qStd"] is not None:
            self_.qStd = kvargs["qStd"]
        if "qSum" in kvargs and kvargs["qSum"] is not None:
            self_.qSum = kvargs["qSum"]
        if "qSum2" in kvargs and kvargs["qSum2"] is not None:
            self_.qSum2 = kvargs["qSum2"]
        if "qSumStringLen" in kvargs and kvargs["qSumStringLen"] is not None:
            self_.qSumStringLen = kvargs["qSumStringLen"]
        if "qTextValues" in kvargs and kvargs["qTextValues"] is not None:
            self_.qTextValues = kvargs["qTextValues"]
        if "qZeroValues" in kvargs and kvargs["qZeroValues"] is not None:
            self_.qZeroValues = kvargs["qZeroValues"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldList:
    """
    Lists the fields present in the data model viewer. Is the layout for FieldListDef.

    Attributes
    ----------
    qItems: list[NxFieldDescription]
      Array of items.
    """

    qItems: list[NxFieldDescription] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs and kvargs["qItems"] is not None:
            if all(
                f"list[{type(e).__name__}]" == FieldList.__annotations__["qItems"]
                for e in kvargs["qItems"]
            ):
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [
                    NxFieldDescription(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qItems"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldListDef:
    """
    Defines the fields to show.

    Attributes
    ----------
    qShowDefinitionOnly: bool
      Shows the fields defined on the fly if set to true.
      Default is false.
    qShowDerivedFields: bool
      Shows the fields and derived fields if set to true.
      Default is false.
    qShowHidden: bool
      Shows the hidden fields if set to true.
      Default is false.
    qShowImplicit: bool
      Shows the Direct Discovery measure fields if set to true.
      Default is false.
    qShowSemantic: bool
      Show the semantic fields if set to true.
      Default is false.
    qShowSrcTables: bool
      Shows the tables and fields present in the data model viewer if set to true.
      Default is false.
    qShowSystem: bool
      Shows the system tables if set to true.
      Default is false.
    """

    qShowDefinitionOnly: bool = None
    qShowDerivedFields: bool = None
    qShowHidden: bool = None
    qShowImplicit: bool = None
    qShowSemantic: bool = None
    qShowSrcTables: bool = None
    qShowSystem: bool = None

    def __init__(self_, **kvargs):
        if (
            "qShowDefinitionOnly" in kvargs
            and kvargs["qShowDefinitionOnly"] is not None
        ):
            self_.qShowDefinitionOnly = kvargs["qShowDefinitionOnly"]
        if "qShowDerivedFields" in kvargs and kvargs["qShowDerivedFields"] is not None:
            self_.qShowDerivedFields = kvargs["qShowDerivedFields"]
        if "qShowHidden" in kvargs and kvargs["qShowHidden"] is not None:
            self_.qShowHidden = kvargs["qShowHidden"]
        if "qShowImplicit" in kvargs and kvargs["qShowImplicit"] is not None:
            self_.qShowImplicit = kvargs["qShowImplicit"]
        if "qShowSemantic" in kvargs and kvargs["qShowSemantic"] is not None:
            self_.qShowSemantic = kvargs["qShowSemantic"]
        if "qShowSrcTables" in kvargs and kvargs["qShowSrcTables"] is not None:
            self_.qShowSrcTables = kvargs["qShowSrcTables"]
        if "qShowSystem" in kvargs and kvargs["qShowSystem"] is not None:
            self_.qShowSystem = kvargs["qShowSystem"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldOrColumn:
    """

    Attributes
    ----------
    qFieldName: str
      Name of the field or column to be matched.
    qTableName: str
      Name of the table to be matched on. This parameter is optional. If TableName is set, FieldName represent the Table column with that name. If TableName is not set, FieldName represents the the field with that name.
    """

    qFieldName: str = None
    qTableName: str = None

    def __init__(self_, **kvargs):
        if "qFieldName" in kvargs and kvargs["qFieldName"] is not None:
            self_.qFieldName = kvargs["qFieldName"]
        if "qTableName" in kvargs and kvargs["qTableName"] is not None:
            self_.qTableName = kvargs["qTableName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldScores:
    """

    Attributes
    ----------
    qCardinalRatio: float
      Cardinality of a column/field divided by the number of rows in the table.
      If the cardinal ratio is 1, it means that the column is a candidate/primary key.
    qFieldName: str
      Field name.
      One of the field names defined in qFieldPairName.
    qReadableName: str
    qRowScore: float
      Number of matches between the two fields defined in qFieldPairName divided by the number of values in the field qFieldName .
      If 0, it means that there are no common values between the two fields defined in qFieldPairName .
    qSymbolScore: float
      Number of distinct matches between the two fields defined in qFieldPairName divided by the number of distinct values in the field qFieldName .
      If 0, it means that there are no common values between the two fields defined in qFieldPairName .
    """

    qCardinalRatio: float = None
    qFieldName: str = None
    qReadableName: str = None
    qRowScore: float = None
    qSymbolScore: float = None

    def __init__(self_, **kvargs):
        if "qCardinalRatio" in kvargs and kvargs["qCardinalRatio"] is not None:
            self_.qCardinalRatio = kvargs["qCardinalRatio"]
        if "qFieldName" in kvargs and kvargs["qFieldName"] is not None:
            self_.qFieldName = kvargs["qFieldName"]
        if "qReadableName" in kvargs and kvargs["qReadableName"] is not None:
            self_.qReadableName = kvargs["qReadableName"]
        if "qRowScore" in kvargs and kvargs["qRowScore"] is not None:
            self_.qRowScore = kvargs["qRowScore"]
        if "qSymbolScore" in kvargs and kvargs["qSymbolScore"] is not None:
            self_.qSymbolScore = kvargs["qSymbolScore"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FieldValue:
    """

    Attributes
    ----------
    qIsNumeric: bool
      Is set to true if the value is a numeric.
      This parameter is optional. Default is false.
    qNumber: float
      Numeric value of the field.
      This parameter is displayed if qIsNumeric is set to true.
      This parameter is optional.
    qText: str
      Text related to the field value.
      This parameter is optional.
    """

    qIsNumeric: bool = None
    qNumber: float = None
    qText: str = None

    def __init__(self_, **kvargs):
        if "qIsNumeric" in kvargs and kvargs["qIsNumeric"] is not None:
            self_.qIsNumeric = kvargs["qIsNumeric"]
        if "qNumber" in kvargs and kvargs["qNumber"] is not None:
            self_.qNumber = kvargs["qNumber"]
        if "qText" in kvargs and kvargs["qText"] is not None:
            self_.qText = kvargs["qText"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FileDataFormat:
    """
     FileType:
    Recognized file formats are:

    • CSV for Delimited

    • FIX for Fixed Record

    • DIF for Data Interchange Format

    • EXCEL_BIFF for Microsoft Excel (XLS)

    • EXCEL_OOXML for Microsoft Excel (XLSX)

    • HTML for HTML

    • QVD for QVD file

    • XML for XML

    • QVX for QVX file

    • JSON for JSON format

    • KML for KML file

    • PARQUET for PARQUET file

    Attributes
    ----------
    qCodePage: int
      Character set used in the file.
    qComment: str
      String that marks the beginning of the comment line.
      Example: “” or “//”:
      The engine ignores the commented lines during the data load.
      This property is only used for delimited files.
    qDelimiter: DelimiterInfo
      Information about the delimiter.
      This property is used for delimited files.
    qFixedWidthDelimiters: str
      Positions of the field breaks in the table.
      This property is used for fixed record data files.
    qHeaderSize: int
      Size of the header.
      Example: If the header size is 2, the first two rows in the file are considered as header and not as data. The header can contain the field names.
    qIgnoreEOF: bool
      Is set to true, the end-of-file character is not taken into account during reload.
      This property is used for delimited files and fixed record data files.
    qLabel: str
      One of:

      • Embedded labels (field names are present in the file)

      • No labels

      • Explicit labels (for DIFfiles)
    qQuote: str
      One of:

      • None (no quotes)

      • MSQ (Modern Style Quoting)

      • Standard (quotes " " or ' ' can be used, but only if they are the first and last non blank characters of a field value)

      This property is used for delimited files.
    qRecordSize: int
      Record length.
      Each record (row of data) contains a number of columns with a fixed field size.
      This property is used for fixed record data files.
    qTabSize: int
      Number of spaces that one tab character represents in the table file.
      This property is used for fixed record data files.
    qType: Literal["FILE_TYPE_CSV", "FILE_TYPE_FIX", "FILE_TYPE_DIF", "FILE_TYPE_EXCEL_BIFF", "FILE_TYPE_EXCEL_OOXML", "FILE_TYPE_HTML", "FILE_TYPE_QVD", "FILE_TYPE_XML", "FILE_TYPE_QVX", "FILE_TYPE_JSON", "FILE_TYPE_KML", "FILE_TYPE_PARQUET"]
      Type of the file.

      One of:

      • CSV or FILE_TYPE_CSV

      • FIX or FILE_TYPE_FIX

      • DIF or FILE_TYPE_DIF

      • EXCEL_BIFF or FILE_TYPE_EXCEL_BIFF

      • EXCEL_OOXML or FILE_TYPE_EXCEL_OOXML

      • HTML or FILE_TYPE_HTML

      • QVD or FILE_TYPE_QVD

      • XML or FILE_TYPE_XML

      • QVX or FILE_TYPE_QVX

      • JSON or FILE_TYPE_JSON

      • KML or FILE_TYPE_KML

      • PARQUET or FILE_TYPE_PARQUET
    """

    qCodePage: int = None
    qComment: str = None
    qDelimiter: DelimiterInfo = None
    qFixedWidthDelimiters: str = None
    qHeaderSize: int = None
    qIgnoreEOF: bool = None
    qLabel: str = None
    qQuote: str = None
    qRecordSize: int = None
    qTabSize: int = None
    qType: Literal[
        "FILE_TYPE_CSV",
        "FILE_TYPE_FIX",
        "FILE_TYPE_DIF",
        "FILE_TYPE_EXCEL_BIFF",
        "FILE_TYPE_EXCEL_OOXML",
        "FILE_TYPE_HTML",
        "FILE_TYPE_QVD",
        "FILE_TYPE_XML",
        "FILE_TYPE_QVX",
        "FILE_TYPE_JSON",
        "FILE_TYPE_KML",
        "FILE_TYPE_PARQUET",
    ] = None

    def __init__(self_, **kvargs):
        if "qCodePage" in kvargs and kvargs["qCodePage"] is not None:
            self_.qCodePage = kvargs["qCodePage"]
        if "qComment" in kvargs and kvargs["qComment"] is not None:
            self_.qComment = kvargs["qComment"]
        if "qDelimiter" in kvargs and kvargs["qDelimiter"] is not None:
            if (
                type(kvargs["qDelimiter"]).__name__
                == FileDataFormat.__annotations__["qDelimiter"]
            ):
                self_.qDelimiter = kvargs["qDelimiter"]
            else:
                self_.qDelimiter = DelimiterInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qDelimiter"],
                )
        if (
            "qFixedWidthDelimiters" in kvargs
            and kvargs["qFixedWidthDelimiters"] is not None
        ):
            self_.qFixedWidthDelimiters = kvargs["qFixedWidthDelimiters"]
        if "qHeaderSize" in kvargs and kvargs["qHeaderSize"] is not None:
            self_.qHeaderSize = kvargs["qHeaderSize"]
        if "qIgnoreEOF" in kvargs and kvargs["qIgnoreEOF"] is not None:
            self_.qIgnoreEOF = kvargs["qIgnoreEOF"]
        if "qLabel" in kvargs and kvargs["qLabel"] is not None:
            self_.qLabel = kvargs["qLabel"]
        if "qQuote" in kvargs and kvargs["qQuote"] is not None:
            self_.qQuote = kvargs["qQuote"]
        if "qRecordSize" in kvargs and kvargs["qRecordSize"] is not None:
            self_.qRecordSize = kvargs["qRecordSize"]
        if "qTabSize" in kvargs and kvargs["qTabSize"] is not None:
            self_.qTabSize = kvargs["qTabSize"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FileType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FilterInfo:
    """

    Attributes
    ----------
    qType: Literal["FILTER_TYPE_NONE", "FILTER_TYPE_RAW"]

      One of:

      • NONE or FILTER_TYPE_NONE

      • RAW or FILTER_TYPE_RAW
    qWherePredicate: str
    """

    qType: Literal["FILTER_TYPE_NONE", "FILTER_TYPE_RAW"] = None
    qWherePredicate: str = None

    def __init__(self_, **kvargs):
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        if "qWherePredicate" in kvargs and kvargs["qWherePredicate"] is not None:
            self_.qWherePredicate = kvargs["qWherePredicate"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FilterType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FolderItem:
    """

    Attributes
    ----------
    qName: str
      Name of the folder item.
    qType: Literal["FOLDER_ITEM_FOLDER", "FOLDER_ITEM_FILE", "FOLDER_ITEM_OTHER"]
      Type of the folder item.

      One of:

      • FOLDER or FOLDER_ITEM_FOLDER

      • FILE or FOLDER_ITEM_FILE

      • OTHER or FOLDER_ITEM_OTHER
    """

    qName: str = None
    qType: Literal["FOLDER_ITEM_FOLDER", "FOLDER_ITEM_FILE", "FOLDER_ITEM_OTHER"] = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FolderItemType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FrequencyDistributionData:
    """

    Attributes
    ----------
    qBinsEdges: list[float]
      Bins edges.
    qFrequencies: list[int]
      Bins frequencies.
    qNumberOfBins: int
      Number of bins.
    """

    qBinsEdges: list[float] = None
    qFrequencies: list[int] = None
    qNumberOfBins: int = None

    def __init__(self_, **kvargs):
        if "qBinsEdges" in kvargs and kvargs["qBinsEdges"] is not None:
            self_.qBinsEdges = kvargs["qBinsEdges"]
        if "qFrequencies" in kvargs and kvargs["qFrequencies"] is not None:
            self_.qFrequencies = kvargs["qFrequencies"]
        if "qNumberOfBins" in kvargs and kvargs["qNumberOfBins"] is not None:
            self_.qNumberOfBins = kvargs["qNumberOfBins"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Function:
    """

    Attributes
    ----------
    qGroup: Literal["FUNC_GROUP_ALL", "FUNC_GROUP_UNKNOWN", "FUNC_GROUP_NONE", "FUNC_GROUP_AGGR", "FUNC_GROUP_NUMERIC", "FUNC_GROUP_RANGE", "FUNC_GROUP_EXPONENTIAL_AND_LOGARITHMIC", "FUNC_GROUP_TRIGONOMETRIC_AND_HYPERBOLIC", "FUNC_GROUP_FINANCIAL", "FUNC_GROUP_MATH_CONSTANT_AND_PARAM_FREE", "FUNC_GROUP_COUNTER", "FUNC_GROUP_STRING", "FUNC_GROUP_MAPPING", "FUNC_GROUP_INTER_RECORD", "FUNC_GROUP_CONDITIONAL", "FUNC_GROUP_LOGICAL", "FUNC_GROUP_NULL", "FUNC_GROUP_SYSTEM", "FUNC_GROUP_FILE", "FUNC_GROUP_TABLE", "FUNC_GROUP_DATE_AND_TIME", "FUNC_GROUP_NUMBER_INTERPRET", "FUNC_GROUP_FORMATTING", "FUNC_GROUP_COLOR", "FUNC_GROUP_RANKING", "FUNC_GROUP_GEO", "FUNC_GROUP_EXTERNAL", "FUNC_GROUP_PROBABILITY", "FUNC_GROUP_ARRAY", "FUNC_GROUP_LEGACY", "FUNC_GROUP_DB_NATIVE"]
      Group of the script function.

      One of:

      • ALL or FUNC_GROUP_ALL

      • U or FUNC_GROUP_UNKNOWN

      • NONE or FUNC_GROUP_NONE

      • AGGR or FUNC_GROUP_AGGR

      • NUM or FUNC_GROUP_NUMERIC

      • RNG or FUNC_GROUP_RANGE

      • EXP or FUNC_GROUP_EXPONENTIAL_AND_LOGARITHMIC

      • TRIG or FUNC_GROUP_TRIGONOMETRIC_AND_HYPERBOLIC

      • FIN or FUNC_GROUP_FINANCIAL

      • MATH or FUNC_GROUP_MATH_CONSTANT_AND_PARAM_FREE

      • COUNT or FUNC_GROUP_COUNTER

      • STR or FUNC_GROUP_STRING

      • MAPP or FUNC_GROUP_MAPPING

      • RCRD or FUNC_GROUP_INTER_RECORD

      • CND or FUNC_GROUP_CONDITIONAL

      • LOG or FUNC_GROUP_LOGICAL

      • NULL or FUNC_GROUP_NULL

      • SYS or FUNC_GROUP_SYSTEM

      • FILE or FUNC_GROUP_FILE

      • TBL or FUNC_GROUP_TABLE

      • DATE or FUNC_GROUP_DATE_AND_TIME

      • NUMI or FUNC_GROUP_NUMBER_INTERPRET

      • FRMT or FUNC_GROUP_FORMATTING

      • CLR or FUNC_GROUP_COLOR

      • RNK or FUNC_GROUP_RANKING

      • GEO or FUNC_GROUP_GEO

      • EXT or FUNC_GROUP_EXTERNAL

      • PROB or FUNC_GROUP_PROBABILITY

      • ARRAY or FUNC_GROUP_ARRAY

      • LEG or FUNC_GROUP_LEGACY

      • DB or FUNC_GROUP_DB_NATIVE
    qName: str
      Name of the script function.
    qSignature: str
      Signature of the script function.
      Gives general information about the function.
    """

    qGroup: Literal[
        "FUNC_GROUP_ALL",
        "FUNC_GROUP_UNKNOWN",
        "FUNC_GROUP_NONE",
        "FUNC_GROUP_AGGR",
        "FUNC_GROUP_NUMERIC",
        "FUNC_GROUP_RANGE",
        "FUNC_GROUP_EXPONENTIAL_AND_LOGARITHMIC",
        "FUNC_GROUP_TRIGONOMETRIC_AND_HYPERBOLIC",
        "FUNC_GROUP_FINANCIAL",
        "FUNC_GROUP_MATH_CONSTANT_AND_PARAM_FREE",
        "FUNC_GROUP_COUNTER",
        "FUNC_GROUP_STRING",
        "FUNC_GROUP_MAPPING",
        "FUNC_GROUP_INTER_RECORD",
        "FUNC_GROUP_CONDITIONAL",
        "FUNC_GROUP_LOGICAL",
        "FUNC_GROUP_NULL",
        "FUNC_GROUP_SYSTEM",
        "FUNC_GROUP_FILE",
        "FUNC_GROUP_TABLE",
        "FUNC_GROUP_DATE_AND_TIME",
        "FUNC_GROUP_NUMBER_INTERPRET",
        "FUNC_GROUP_FORMATTING",
        "FUNC_GROUP_COLOR",
        "FUNC_GROUP_RANKING",
        "FUNC_GROUP_GEO",
        "FUNC_GROUP_EXTERNAL",
        "FUNC_GROUP_PROBABILITY",
        "FUNC_GROUP_ARRAY",
        "FUNC_GROUP_LEGACY",
        "FUNC_GROUP_DB_NATIVE",
    ] = None
    qName: str = None
    qSignature: str = None

    def __init__(self_, **kvargs):
        if "qGroup" in kvargs and kvargs["qGroup"] is not None:
            self_.qGroup = kvargs["qGroup"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qSignature" in kvargs and kvargs["qSignature"] is not None:
            self_.qSignature = kvargs["qSignature"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FunctionGroup:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericBookmark:
    """

    Attributes
    ----------
    qGenericId: str
      Object ID.
    qGenericType: str
      The type of the object.
    qHandle: int
      The handle used to connect to object.
    qType: str
      The native type of the object.
    """

    _session: RpcSession = None
    qGenericId: str = None
    qGenericType: str = None
    qHandle: int = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qGenericId" in kvargs and kvargs["qGenericId"] is not None:
            self_.qGenericId = kvargs["qGenericId"]
        if "qGenericType" in kvargs and kvargs["qGenericType"] is not None:
            self_.qGenericType = kvargs["qGenericType"]
        if "qHandle" in kvargs and kvargs["qHandle"] is not None:
            self_.qHandle = kvargs["qHandle"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}) or k == "_session":
                self_.__setattr__(k, v)

    def get_field_values(
        self, qField: str, qGetExcludedValues: bool, qDataPage: BookmarkFieldPage
    ) -> list[FieldValue]:
        """
        Retrieves the values of a field.

         Fieldvalue:
        | Name       | Description                                                                                  | Type    |
        |------------|----------------------------------------------------------------------------------------------|---------|
        | qText      | Text related to the field value.                                                             | String  |
        | qIsNumeric | Is set to true if the value is a numeric.  Default is false.                             | Boolean |
        | qNumber    | Numeric value of the field.  This parameter is displayed if _qIsNumeric_ is set to true. | Double  |

        Parameters
        ----------
        qField: str
          Name of the field.
        qGetExcludedValues: bool
          If set to true, only excluded values are returned.
        qDataPage: BookmarkFieldPage
          Range of returned values.
        """
        params = {}
        params["qField"] = qField
        params["qGetExcludedValues"] = qGetExcludedValues
        params["qDataPage"] = qDataPage
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFieldValues", handle, **params)[
            "qFieldValues"
        ]
        return [FieldValue(**e) for e in response]

    def get_layout(self) -> GenericBookmarkLayout:
        """
        Evaluates an object and displays its properties including the dynamic properties.
        If the member delta is set to true in the request object, only the delta is evaluated.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLayout", handle)["qLayout"]
        obj = GenericBookmarkLayout(**response)
        return obj

    def apply_patches(self, qPatches: list[NxPatch]) -> object:
        """
        Applies a patch to the properties of an object. Allows an update to some of the properties. It should not be possible to patch "/qInfo/qId",
        and it will be forbidden in the near future.
        Applying a patch takes less time than resetting all the properties.

        Parameters
        ----------
        qPatches: list[NxPatch]
          Array of patches.
        """
        params = {}
        params["qPatches"] = qPatches
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ApplyPatches", handle, **params)
        return response

    def set_properties(self, qProp: GenericBookmarkProperties) -> object:
        """
        Sets some properties for a bookmark.

        Parameters
        ----------
        qProp: GenericBookmarkProperties
          Information about the bookmark.
        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetProperties", handle, **params)
        return response

    def get_properties(self) -> GenericBookmarkProperties:
        """
        Shows the properties of an object.
        If the member delta is set to true in the request object, only the delta is retrieved.
        The following is always returned in the output:

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetProperties", handle)["qProp"]
        obj = GenericBookmarkProperties(**response)
        return obj

    def get_info(self) -> NxInfo:
        """
        Returns:

        • The type of the object.

        • The identifier of the object.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetInfo", handle)["qInfo"]
        obj = NxInfo(**response)
        return obj

    def apply(self) -> bool:
        """
        Applies a bookmark.

        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Apply", handle)["qSuccess"]
        return response

    def apply_and_verify(self) -> BookmarkApplyAndVerifyResult:
        """
        Experimental
        Applies a bookmark and verify result dataset against originally selected values.

        The operation is successful if qApplySuccess is set to true. qWarnings lists state and field with unmatching values

        Parameters
        ----------
        """
        warnings.warn("ApplyAndVerify is experimental", UserWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ApplyAndVerify", handle)["qResult"]
        obj = BookmarkApplyAndVerifyResult(**response)
        return obj

    def publish(self) -> object:
        """
        Publishes a bookmark.
        This operation is not applicable for Qlik Sense Desktop.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Publish", handle)
        return response

    def un_publish(self) -> object:
        """
        Unpublishes a bookmark.
        This operation is not applicable for Qlik Sense Desktop.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnPublish", handle)
        return response

    def approve(self) -> object:
        """
        Adds the generic bookmark to the list of approved objects
        This operation is possible only in Qlik Sense Enterprise.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Approve", handle)
        return response

    def un_approve(self) -> object:
        """
        Removes the generic bookmark from the list of approved objects
        This operation is possible only in Qlik Sense Enterprise.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnApprove", handle)
        return response

    def on(self, event_name, listener):
        self._session.on_handle(self.qHandle, event_name, listener)


@dataclass
class GenericBookmarkEntry:
    """

    Attributes
    ----------
    qBookmark: NxBookmark
      Information about the bookmark.
    qClassicBookmark: Bookmark
      Information about the Classic bookmark.
    qClassicMetadata: MetaData
      Information about the Classic bookmark metadata.
    qProperties: GenericBookmarkProperties
      Information about the properties of the bookmark.
    """

    qBookmark: NxBookmark = None
    qClassicBookmark: Bookmark = None
    qClassicMetadata: MetaData = None
    qProperties: GenericBookmarkProperties = None

    def __init__(self_, **kvargs):
        if "qBookmark" in kvargs and kvargs["qBookmark"] is not None:
            if (
                type(kvargs["qBookmark"]).__name__
                == GenericBookmarkEntry.__annotations__["qBookmark"]
            ):
                self_.qBookmark = kvargs["qBookmark"]
            else:
                self_.qBookmark = NxBookmark(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qBookmark"],
                )
        if "qClassicBookmark" in kvargs and kvargs["qClassicBookmark"] is not None:
            if (
                type(kvargs["qClassicBookmark"]).__name__
                == GenericBookmarkEntry.__annotations__["qClassicBookmark"]
            ):
                self_.qClassicBookmark = kvargs["qClassicBookmark"]
            else:
                self_.qClassicBookmark = Bookmark(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qClassicBookmark"],
                )
        if "qClassicMetadata" in kvargs and kvargs["qClassicMetadata"] is not None:
            if (
                type(kvargs["qClassicMetadata"]).__name__
                == GenericBookmarkEntry.__annotations__["qClassicMetadata"]
            ):
                self_.qClassicMetadata = kvargs["qClassicMetadata"]
            else:
                self_.qClassicMetadata = MetaData(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qClassicMetadata"],
                )
        if "qProperties" in kvargs and kvargs["qProperties"] is not None:
            if (
                type(kvargs["qProperties"]).__name__
                == GenericBookmarkEntry.__annotations__["qProperties"]
            ):
                self_.qProperties = kvargs["qProperties"]
            else:
                self_.qProperties = GenericBookmarkProperties(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qProperties"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericBookmarkLayout:
    """
    Is the layout for GenericBookmarkProperties.

    Attributes
    ----------
    qBookmark: NxBookmark
      Information about the bookmark.
    qFieldInfos: list[LayoutFieldInfo]
      Information about the field selections associated with the bookmark.
    qInfo: NxInfo
      Information about the object.
    qMeta: NxMeta
      Information on publishing and permissions.
    """

    qBookmark: NxBookmark = None
    qFieldInfos: list[LayoutFieldInfo] = None
    qInfo: NxInfo = None
    qMeta: NxMeta = None

    def __init__(self_, **kvargs):
        if "qBookmark" in kvargs and kvargs["qBookmark"] is not None:
            if (
                type(kvargs["qBookmark"]).__name__
                == GenericBookmarkLayout.__annotations__["qBookmark"]
            ):
                self_.qBookmark = kvargs["qBookmark"]
            else:
                self_.qBookmark = NxBookmark(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qBookmark"],
                )
        if "qFieldInfos" in kvargs and kvargs["qFieldInfos"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == GenericBookmarkLayout.__annotations__["qFieldInfos"]
                for e in kvargs["qFieldInfos"]
            ):
                self_.qFieldInfos = kvargs["qFieldInfos"]
            else:
                self_.qFieldInfos = [
                    LayoutFieldInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qFieldInfos"]
                ]
        if "qInfo" in kvargs and kvargs["qInfo"] is not None:
            if (
                type(kvargs["qInfo"]).__name__
                == GenericBookmarkLayout.__annotations__["qInfo"]
            ):
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qInfo"],
                )
        if "qMeta" in kvargs and kvargs["qMeta"] is not None:
            if (
                type(kvargs["qMeta"]).__name__
                == GenericBookmarkLayout.__annotations__["qMeta"]
            ):
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeta"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericBookmarkProperties:
    """

    Attributes
    ----------
    qDistinctValues: bool
      If true all selected values will be stored distinct, i.e. searchstrings will not be kept.
    qIncludeVariables: bool
      If true all variables will be stored in the bookmark.
    qInfo: NxInfo
      Information about the bookmark.
      This parameter is mandatory.
    qMetaDef: NxMetaDef
      Definition of the dynamic properties.
    """

    qDistinctValues: bool = None
    qIncludeVariables: bool = None
    qInfo: NxInfo = None
    qMetaDef: NxMetaDef = None

    def __init__(self_, **kvargs):
        if "qDistinctValues" in kvargs and kvargs["qDistinctValues"] is not None:
            self_.qDistinctValues = kvargs["qDistinctValues"]
        if "qIncludeVariables" in kvargs and kvargs["qIncludeVariables"] is not None:
            self_.qIncludeVariables = kvargs["qIncludeVariables"]
        if "qInfo" in kvargs and kvargs["qInfo"] is not None:
            if (
                type(kvargs["qInfo"]).__name__
                == GenericBookmarkProperties.__annotations__["qInfo"]
            ):
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qInfo"],
                )
        if "qMetaDef" in kvargs and kvargs["qMetaDef"] is not None:
            if (
                type(kvargs["qMetaDef"]).__name__
                == GenericBookmarkProperties.__annotations__["qMetaDef"]
            ):
                self_.qMetaDef = kvargs["qMetaDef"]
            else:
                self_.qMetaDef = NxMetaDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMetaDef"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericConnectMachine:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericDimension:
    """

    Attributes
    ----------
    qGenericId: str
      Object ID.
    qGenericType: str
      The type of the object.
    qHandle: int
      The handle used to connect to object.
    qType: str
      The native type of the object.
    """

    _session: RpcSession = None
    qGenericId: str = None
    qGenericType: str = None
    qHandle: int = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qGenericId" in kvargs and kvargs["qGenericId"] is not None:
            self_.qGenericId = kvargs["qGenericId"]
        if "qGenericType" in kvargs and kvargs["qGenericType"] is not None:
            self_.qGenericType = kvargs["qGenericType"]
        if "qHandle" in kvargs and kvargs["qHandle"] is not None:
            self_.qHandle = kvargs["qHandle"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}) or k == "_session":
                self_.__setattr__(k, v)

    def get_layout(self) -> GenericDimensionLayout:
        """
        Evaluates a dimension and displays its properties, including the dynamic properties.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLayout", handle)["qLayout"]
        obj = GenericDimensionLayout(**response)
        return obj

    def apply_patches(self, qPatches: list[NxPatch]) -> object:
        """
        Applies a patch to the properties of an object. Allows an update to some of the properties. It should not be possible to patch "/qInfo/qId",
        and it will be forbidden in the near future.
        Applying a patch takes less time than resetting all the properties.

        Parameters
        ----------
        qPatches: list[NxPatch]
          Array of patches.
        """
        params = {}
        params["qPatches"] = qPatches
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ApplyPatches", handle, **params)
        return response

    def set_properties(self, qProp: GenericDimensionProperties) -> object:
        """
        Sets some properties for a dimension.

        Parameters
        ----------
        qProp: GenericDimensionProperties
          Information about the dimension.
        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetProperties", handle, **params)
        return response

    def get_properties(self) -> GenericDimensionProperties:
        """
        Shows the properties of an object.
        Returns the identifier and the definition of the dimension.
        If the member delta is set to true in the request object, only the delta is retrieved.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetProperties", handle)["qProp"]
        obj = GenericDimensionProperties(**response)
        return obj

    def get_info(self) -> NxInfo:
        """
        Returns the type and identifier of the object.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetInfo", handle)["qInfo"]
        obj = NxInfo(**response)
        return obj

    def get_dimension(self) -> NxLibraryDimensionDef:
        """
        Returns the definition of a dimension.

        The definition of the dimension is returned.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDimension", handle)["qDim"]
        obj = NxLibraryDimensionDef(**response)
        return obj

    def get_linked_objects(self) -> list[NxLinkedObjectInfo]:
        """
        Lists the linked objects to a generic object, a dimension or a measure.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLinkedObjects", handle)["qItems"]
        return [NxLinkedObjectInfo(**e) for e in response]

    def publish(self) -> object:
        """
        Publishes a dimension.
        This operation is not applicable for Qlik Sense Desktop.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Publish", handle)
        return response

    def un_publish(self) -> object:
        """
        Unpublishes a dimension.
        This operation is not applicable for Qlik Sense Desktop.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnPublish", handle)
        return response

    def approve(self) -> object:
        """
        Adds the generic dimension to the list of approved objects
        This operation is possible only in Qlik Sense Enterprise.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Approve", handle)
        return response

    def un_approve(self) -> object:
        """
        Removes the generic dimension from the list of approved objects
        This operation is possible only in Qlik Sense Enterprise.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnApprove", handle)
        return response

    def on(self, event_name, listener):
        self._session.on_handle(self.qHandle, event_name, listener)


@dataclass
class GenericDimensionInfo:
    """

    Attributes
    ----------
    qAndMode: bool
      If set to true a logical AND (instead of a logical OR) is used when making selections in a field.
      The default value is false.
    qApprMaxGlyphCount: int
      Length of the longest value in the field.
    qCardinal: int
      Number of distinct field values
    qIsSemantic: bool
      If set to true, it means that the field is a semantic.
    qTags: list[str]
      Gives information on a field. For example, it can return the type of the field.
      Examples: key, text, ASCII
    """

    qAndMode: bool = None
    qApprMaxGlyphCount: int = None
    qCardinal: int = None
    qIsSemantic: bool = None
    qTags: list[str] = None

    def __init__(self_, **kvargs):
        if "qAndMode" in kvargs and kvargs["qAndMode"] is not None:
            self_.qAndMode = kvargs["qAndMode"]
        if "qApprMaxGlyphCount" in kvargs and kvargs["qApprMaxGlyphCount"] is not None:
            self_.qApprMaxGlyphCount = kvargs["qApprMaxGlyphCount"]
        if "qCardinal" in kvargs and kvargs["qCardinal"] is not None:
            self_.qCardinal = kvargs["qCardinal"]
        if "qIsSemantic" in kvargs and kvargs["qIsSemantic"] is not None:
            self_.qIsSemantic = kvargs["qIsSemantic"]
        if "qTags" in kvargs and kvargs["qTags"] is not None:
            self_.qTags = kvargs["qTags"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericDimensionLayout:
    """
    Is the layout for GenericDimensionProperties.

    Attributes
    ----------
    qDim: NxLibraryDimension
      Name and label of the dimension, information about grouping.
    qDimInfos: list[GenericDimensionInfo]
      Cardinal and tags related to the dimension.
      Length of the longest value in the field.
    qInfo: NxInfo
      Identifier and type of the dimension.
    qMeta: NxMeta
      Information about publishing and permissions.
    """

    qDim: NxLibraryDimension = None
    qDimInfos: list[GenericDimensionInfo] = None
    qInfo: NxInfo = None
    qMeta: NxMeta = None

    def __init__(self_, **kvargs):
        if "qDim" in kvargs and kvargs["qDim"] is not None:
            if (
                type(kvargs["qDim"]).__name__
                == GenericDimensionLayout.__annotations__["qDim"]
            ):
                self_.qDim = kvargs["qDim"]
            else:
                self_.qDim = NxLibraryDimension(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qDim"],
                )
        if "qDimInfos" in kvargs and kvargs["qDimInfos"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == GenericDimensionLayout.__annotations__["qDimInfos"]
                for e in kvargs["qDimInfos"]
            ):
                self_.qDimInfos = kvargs["qDimInfos"]
            else:
                self_.qDimInfos = [
                    GenericDimensionInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qDimInfos"]
                ]
        if "qInfo" in kvargs and kvargs["qInfo"] is not None:
            if (
                type(kvargs["qInfo"]).__name__
                == GenericDimensionLayout.__annotations__["qInfo"]
            ):
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qInfo"],
                )
        if "qMeta" in kvargs and kvargs["qMeta"] is not None:
            if (
                type(kvargs["qMeta"]).__name__
                == GenericDimensionLayout.__annotations__["qMeta"]
            ):
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeta"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericDimensionProperties:
    """

    Attributes
    ----------
    qDim: NxLibraryDimensionDef
      Definition of the dimension.
      This parameter is mandatory.
    qInfo: NxInfo
      Identifier and type of the dimension.
      This parameter is mandatory.
    qMetaDef: NxMetaDef
      Definition of the dynamic properties.
    """

    qDim: NxLibraryDimensionDef = None
    qInfo: NxInfo = None
    qMetaDef: NxMetaDef = None

    def __init__(self_, **kvargs):
        if "qDim" in kvargs and kvargs["qDim"] is not None:
            if (
                type(kvargs["qDim"]).__name__
                == GenericDimensionProperties.__annotations__["qDim"]
            ):
                self_.qDim = kvargs["qDim"]
            else:
                self_.qDim = NxLibraryDimensionDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qDim"],
                )
        if "qInfo" in kvargs and kvargs["qInfo"] is not None:
            if (
                type(kvargs["qInfo"]).__name__
                == GenericDimensionProperties.__annotations__["qInfo"]
            ):
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qInfo"],
                )
        if "qMetaDef" in kvargs and kvargs["qMetaDef"] is not None:
            if (
                type(kvargs["qMetaDef"]).__name__
                == GenericDimensionProperties.__annotations__["qMetaDef"]
            ):
                self_.qMetaDef = kvargs["qMetaDef"]
            else:
                self_.qMetaDef = NxMetaDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMetaDef"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericMeasure:
    """

    Attributes
    ----------
    qGenericId: str
      Object ID.
    qGenericType: str
      The type of the object.
    qHandle: int
      The handle used to connect to object.
    qType: str
      The native type of the object.
    """

    _session: RpcSession = None
    qGenericId: str = None
    qGenericType: str = None
    qHandle: int = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qGenericId" in kvargs and kvargs["qGenericId"] is not None:
            self_.qGenericId = kvargs["qGenericId"]
        if "qGenericType" in kvargs and kvargs["qGenericType"] is not None:
            self_.qGenericType = kvargs["qGenericType"]
        if "qHandle" in kvargs and kvargs["qHandle"] is not None:
            self_.qHandle = kvargs["qHandle"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}) or k == "_session":
                self_.__setattr__(k, v)

    def get_layout(self) -> GenericMeasureLayout:
        """
        Evaluates a measure and displays its properties, including the dynamic properties.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLayout", handle)["qLayout"]
        obj = GenericMeasureLayout(**response)
        return obj

    def apply_patches(self, qPatches: list[NxPatch]) -> object:
        """
        Applies a patch to the properties of an object. Allows an update to some of the properties. It should not be possible to patch "/qInfo/qId",
        and it will be forbidden in the near future.
        Applying a patch takes less time than resetting all the properties.

        Parameters
        ----------
        qPatches: list[NxPatch]
          Array of patches.
        """
        params = {}
        params["qPatches"] = qPatches
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ApplyPatches", handle, **params)
        return response

    def set_properties(self, qProp: GenericMeasureProperties) -> object:
        """
        Sets some properties for a measure.

        Parameters
        ----------
        qProp: GenericMeasureProperties
          Information about the measure.
        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetProperties", handle, **params)
        return response

    def get_properties(self) -> GenericMeasureProperties:
        """
        Shows the properties of an object.
        Returns the identifier and the definition of the measure.
        If the member delta is set to true in the request object, only the delta is retrieved.
        The following is always returned in the output:

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetProperties", handle)["qProp"]
        obj = GenericMeasureProperties(**response)
        return obj

    def get_info(self) -> NxInfo:
        """
        Returns the type and identifier of the object.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetInfo", handle)["qInfo"]
        obj = NxInfo(**response)
        return obj

    def get_measure(self) -> NxLibraryMeasureDef:
        """
        Returns the definition of a measure.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetMeasure", handle)["qMeasure"]
        obj = NxLibraryMeasureDef(**response)
        return obj

    def get_linked_objects(self) -> list[NxLinkedObjectInfo]:
        """
        Lists the linked objects to a generic object, a dimension or a measure.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLinkedObjects", handle)["qItems"]
        return [NxLinkedObjectInfo(**e) for e in response]

    def publish(self) -> object:
        """
        Publishes a measure.
        This operation is not applicable for Qlik Sense Desktop.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Publish", handle)
        return response

    def un_publish(self) -> object:
        """
        Unpublishes a measure.
        This operation is not applicable for Qlik Sense Desktop.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnPublish", handle)
        return response

    def approve(self) -> object:
        """
        Adds the generic measure to the list of approved objects
        This operation is possible only in Qlik Sense Enterprise.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Approve", handle)
        return response

    def un_approve(self) -> object:
        """
        Removes the generic measure from the list of approved objects
        This operation is possible only in Qlik Sense Enterprise.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnApprove", handle)
        return response

    def on(self, event_name, listener):
        self._session.on_handle(self.qHandle, event_name, listener)


@dataclass
class GenericMeasureLayout:
    """
    Is the layout for GenericMeasureProperties.

    Attributes
    ----------
    qInfo: NxInfo
      Information about the object.
    qMeasure: NxLibraryMeasure
      Information about the measure.
    qMeta: NxMeta
      Information on publishing and permissions.
    """

    qInfo: NxInfo = None
    qMeasure: NxLibraryMeasure = None
    qMeta: NxMeta = None

    def __init__(self_, **kvargs):
        if "qInfo" in kvargs and kvargs["qInfo"] is not None:
            if (
                type(kvargs["qInfo"]).__name__
                == GenericMeasureLayout.__annotations__["qInfo"]
            ):
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qInfo"],
                )
        if "qMeasure" in kvargs and kvargs["qMeasure"] is not None:
            if (
                type(kvargs["qMeasure"]).__name__
                == GenericMeasureLayout.__annotations__["qMeasure"]
            ):
                self_.qMeasure = kvargs["qMeasure"]
            else:
                self_.qMeasure = NxLibraryMeasure(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeasure"],
                )
        if "qMeta" in kvargs and kvargs["qMeta"] is not None:
            if (
                type(kvargs["qMeta"]).__name__
                == GenericMeasureLayout.__annotations__["qMeta"]
            ):
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeta"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericMeasureProperties:
    """

    Attributes
    ----------
    qInfo: NxInfo
      Information about the measure.
      This parameter is mandatory.
    qMeasure: NxLibraryMeasureDef
      Definition of the measure.
      This parameter is mandatory.
    qMetaDef: NxMetaDef
      Definition of the dynamic properties.
    """

    qInfo: NxInfo = None
    qMeasure: NxLibraryMeasureDef = None
    qMetaDef: NxMetaDef = None

    def __init__(self_, **kvargs):
        if "qInfo" in kvargs and kvargs["qInfo"] is not None:
            if (
                type(kvargs["qInfo"]).__name__
                == GenericMeasureProperties.__annotations__["qInfo"]
            ):
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qInfo"],
                )
        if "qMeasure" in kvargs and kvargs["qMeasure"] is not None:
            if (
                type(kvargs["qMeasure"]).__name__
                == GenericMeasureProperties.__annotations__["qMeasure"]
            ):
                self_.qMeasure = kvargs["qMeasure"]
            else:
                self_.qMeasure = NxLibraryMeasureDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeasure"],
                )
        if "qMetaDef" in kvargs and kvargs["qMetaDef"] is not None:
            if (
                type(kvargs["qMetaDef"]).__name__
                == GenericMeasureProperties.__annotations__["qMetaDef"]
            ):
                self_.qMetaDef = kvargs["qMetaDef"]
            else:
                self_.qMetaDef = NxMetaDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMetaDef"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericObject:
    """

    Attributes
    ----------
    qGenericId: str
      Object ID.
    qGenericType: str
      The type of the object.
    qHandle: int
      The handle used to connect to object.
    qType: str
      The native type of the object.
    """

    _session: RpcSession = None
    qGenericId: str = None
    qGenericType: str = None
    qHandle: int = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qGenericId" in kvargs and kvargs["qGenericId"] is not None:
            self_.qGenericId = kvargs["qGenericId"]
        if "qGenericType" in kvargs and kvargs["qGenericType"] is not None:
            self_.qGenericType = kvargs["qGenericType"]
        if "qHandle" in kvargs and kvargs["qHandle"] is not None:
            self_.qHandle = kvargs["qHandle"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}) or k == "_session":
                self_.__setattr__(k, v)

    def get_layout(self) -> GenericObjectLayout:
        """
        Evaluates an object and displays its properties including the dynamic properties.
        If the member delta is set to true in the request object, only the delta is evaluated. A GetLayout call on a generic object, returns up to one level down in the hierarchy.

         Example::
        A is a generic object and is the parent of the objects B and C. B is the parent of the objects D and E.

        A GetLayout call on A returns information on the objects A, B and C.
        A GetLayout call on B returns information on the objects B, D and E.
        A  GetLayout call on C returns information on the object C.


        In addition to the parameters displayed above, the GetLayout method can return other properties according to what is defined in the generic object.
        For example, if qHyperCubeDef is defined in the generic object, the GetLayout method returns the properties described in HyperCube.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLayout", handle)["qLayout"]
        obj = GenericObjectLayout(**response)
        return obj

    def get_list_object_data(
        self, qPath: str, qPages: list[NxPage]
    ) -> list[NxDataPage]:
        """
        Retrieves the values of a list object.
        A data set is returned.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be selected.
          For example, /qListObjectDef .
        qPages: list[NxPage]
          Array of pages you are interested in.
        """
        params = {}
        params["qPath"] = qPath
        params["qPages"] = qPages
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetListObjectData", handle, **params)[
            "qDataPages"
        ]
        return [NxDataPage(**e) for e in response]

    def get_hyper_cube_data(self, qPath: str, qPages: list[NxPage]) -> list[NxDataPage]:
        """
        Retrieves the calculated data for a chart, a table, or a scatter plot. It is possible to retrieve specific pages of data.
        This method works for a hypercube in DATA_MODE_STRAIGHT.
        A data set is returned.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .
        qPages: list[NxPage]
          Array of pages to retrieve.
        """
        params = {}
        params["qPath"] = qPath
        params["qPages"] = qPages
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetHyperCubeData", handle, **params)[
            "qDataPages"
        ]
        return [NxDataPage(**e) for e in response]

    def get_hyper_cube_reduced_data(
        self, qPath: str, qPages: list[NxPage], qZoomFactor: int, qReductionMode: str
    ) -> list[NxDataPage]:
        """
        Reduces the data of a bar chart, a line chart or a scatter plot chart and retrieves them.
        The reduction is dependent on the zoom factor (parameter qZoomFactor ) and on the reduction mode.
        This method can be used to create mini charts.

         Bar chart or line chart data reduction:
        For the data reduction to happen, the following conditions must be fulfilled:

        • The values cannot fit in the defined page (parameter qPages ).

        • The zoom factor is not 0 (parameter qZoomFactor ).

        • The reduction mode must be set to D1.

        The reduction algorithm keeps the shape of the visualizations and works whatever the number of dimensions in the chart. The global profile of the chart is reduced, and not only a specific dimension. A visualization that has been reduced contains fewer values but its shape is the same. Data of all types can be reduced. Therefore it is hard to relate the values before and after a reduction especially when reducing string values.

         Example:
        If you have a chart with 1 million data, and you have set the zoom factor to 5, the GetHyperCubeReducedData method reduces the chart and retrieves 200 000 data.

         Scatter plot chart data reduction:
        The reduction mode must be set to C.
        This reduction mechanism follows the 2D K-Means algorithm. Data are reduced into a number of clusters. Each data is assigned to a specific centroid.
        The number of centroids can be defined in the parameter qZoomFactor.

         Scatter plot chart resolution reduction:
        The reduction mode must be set to S.
        The resolution is reduced according to the zoom factor (parameter qZoomFactor ).

         Example:
        If you have a scatter plot chart and the zoom factor is set to 2, the scatter plot chart resolution is reduced by 4.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .
        qPages: list[NxPage]
          Array of pages.
        qZoomFactor: int
          Defines the zoom factor.
          If set to -1, the engine decides of the zoom factor.

          • If the reduction mode is D1 or S , the zoom factor is 2ⁿ. If the zoom factor is 5, the data are reduced by a factor 32.

          • If the reduction mode is C , the zoom factor defines the number of centroids.
        qReductionMode: str
          Defines the reduction mode.

          One of:

          • N or DATA_REDUCTION_NONE

          • D1 or DATA_REDUCTION_ONEDIM

          • S or DATA_REDUCTION_SCATTERED

          • C or DATA_REDUCTION_CLUSTERED

          • ST or DATA_REDUCTION_STACKED
        """
        params = {}
        params["qPath"] = qPath
        params["qPages"] = qPages
        params["qZoomFactor"] = qZoomFactor
        params["qReductionMode"] = qReductionMode
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetHyperCubeReducedData", handle, **params)[
            "qDataPages"
        ]
        return [NxDataPage(**e) for e in response]

    def get_hyper_cube_pivot_data(
        self, qPath: str, qPages: list[NxPage]
    ) -> list[NxPivotPage]:
        """
        Retrieves the values of a pivot table. It is possible to retrieve specific pages of data.
        This method works for a hypercube in DATA_MODE_PIVOT.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .
        qPages: list[NxPage]
          Array of pages to retrieve.
        """
        params = {}
        params["qPath"] = qPath
        params["qPages"] = qPages
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetHyperCubePivotData", handle, **params)[
            "qDataPages"
        ]
        return [NxPivotPage(**e) for e in response]

    def get_hyper_cube_stack_data(
        self, qPath: str, qPages: list[NxPage], qMaxNbrCells: int = None
    ) -> list[NxStackPage]:
        """
        Retrieves the values of a stacked pivot table. It is possible to retrieve specific pages of data.
        This method works for a hypercube in DATA_MODE_PIVOT_STACK.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .
        qPages: list[NxPage]
          Array of pages to retrieve.
        qMaxNbrCells: int = None
          Maximum number of cells at outer level.
          The default value is 10 000.
        """
        params = {}
        params["qPath"] = qPath
        params["qPages"] = qPages
        if qMaxNbrCells is not None:
            params["qMaxNbrCells"] = qMaxNbrCells
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetHyperCubeStackData", handle, **params)[
            "qDataPages"
        ]
        return [NxStackPage(**e) for e in response]

    def get_hyper_cube_continuous_data(
        self, qPath: str, qOptions: NxContinuousDataOptions, qReverseSort: bool = None
    ) -> GetHyperCubeContinuousDataReturn:
        """
        Retrieves and packs compressed hypercube and axis data. It is possible to retrieve specific pages of data.
        Binning is done on the time stamp data as well as the date. This means that you can zoom in to a level of granularity as low as seconds.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object.
          For example, /qHyperCubeDef .
        qOptions: NxContinuousDataOptions
          Defines the data to return.
        qReverseSort: bool = None
          If set to true the returned data pages are reverse sorted.
          Optional.
        """
        params = {}
        params["qPath"] = qPath
        params["qOptions"] = qOptions
        if qReverseSort is not None:
            params["qReverseSort"] = qReverseSort
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetHyperCubeContinuousData", handle, **params)
        obj = GetHyperCubeContinuousDataReturn(**response)
        return obj

    def get_hyper_cube_tree_data(
        self, qPath: str, qNodeOptions: NxTreeDataOption = None
    ) -> list[NxTreeNode]:
        """
        Retrieves data for nodes in a tree structure. It is possible to retrieve specific pages of data.
        This method works for a treedata object or a hypercube in DATA_MODE_TREE.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be selected.
        qNodeOptions: NxTreeDataOption = None
          Specifies all the paging filters needed to define the tree to be fetched. If left out the complete tree is returned.
        """
        params = {}
        params["qPath"] = qPath
        if qNodeOptions is not None:
            params["qNodeOptions"] = qNodeOptions
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetHyperCubeTreeData", handle, **params)[
            "qNodes"
        ]
        return [NxTreeNode(**e) for e in response]

    def get_hyper_cube_binned_data(
        self,
        qPath: str,
        qPages: list[NxPage],
        qViewport: NxViewPort,
        qDataRanges: list[NxDataAreaPage],
        qMaxNbrCells: int,
        qQueryLevel: int,
        qBinningMethod: int,
    ) -> list[NxDataPage]:
        """
        This method supports data binning.
        When a generic object with two or three measures and one dimension contains a lot of data, groups of points (for example, cells) can be rendered instead of points.
        A zone of interest can be refined (for zooming in) up to a maximum refinement level (set in the qQueryLevel parameter) or coarsened (for zoom out).
        The grid of cells is adaptive (not static), meaning that it adapts to different length scales.
        The GetHyperCubeBinnedData method gives information about the adaptive grid and the values of the generic object.
        The number of points in a cell and the coordinates (expressed in the measure range) of each cell are returned.
        Dimension values and measure values are rendered at point level (highest detailed level).
        The generic object should contain two or three measures and one dimension. When the refinement is high, the first two measures are represented on the x-axis and on the y-axis, while the third measure is visualized as color or point size.

         Adaptive Grid:
        More details about the properties of the adaptive grid are given in this paragraph.
        When the refinement is not the highest (cells are rendered), information about the adaptive grid is returned through several arrays.
        The first array contains the following properties:
        | Name        | Description                                       | Type                                                                                                                                                                                                             |
        |-------------|---------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
        | qNum        | Maximum number of points that a cell can contain. | String                                                                                                                                                                                                           |
        | qElemNumber | Is set to 0.                                      | Boolean                                                                                                                                                                                                          |
        | qState      | The default value is L.                           | One of:*   L for Locked*   S for Selected*   O for Optional*   D for Deselected*   A for Alternative*   X for eXcluded*   XS for eXcluded Selected*   XL for eXcluded Locked |

        The next arrays give the coordinates of each cell in the page.
        Each array contains the following properties:
        | Name        | Description                                                                                                                                                                                                                                                                                                     | Type                                                                                                                                                                                                             |
        |-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
        | qText       | Coordinates of a cell in the measure range.  “qText”: “\[\[, , , \], \[, , , \], .... \[, , , \]\]  Where:  , _,  and  are the coordinates of the cell in the measure range. | String                                                                                                                                                                                                           |
        | qNum        | Number of points in the cell.                                                                                                                                                                                                                                                                                   | Double precision floating point                                                                                                                                                                                  |
        | qElemNumber | Unique identifier for each cell, calculated by the engine during the construction of the grid.  This element number is not stored in the database and can have a positive or a negative value.                                                                                                              | Integer                                                                                                                                                                                                          |
        | qState      | The default value is L.                                                                                                                                                                                                                                                                                         | One of:*   L for Locked*   S for Selected*   O for Optional*   D for Deselected*   A for Alternative*   X for eXcluded*   XS for eXcluded Selected*   XL for eXcluded Locked |

        Cells are represented as rectangles.

         Dimension values and measures values:
        More details about the properties, when dimension and measure values are returned, are given in this paragraph.
        When the refinement is high, points are rendered (not cells) and dimension and measure values for each cell are returned.
        The first array is empty because no information on the adaptive grid is needed.
        The next arrays bring information about the dimension and the measure values.
        | Name        | Description                                                                                                                                                                                        | Type                                                                                                                                                                                                             |
        |-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
        | qText       | Text value of the dimension or the measure.                                                                                                                                                        | String                                                                                                                                                                                                           |
        | qNum        | Numerical value of the dimension or the measure.  Is set to 0 if the value is only text.                                                                                                       | Double precision floating point                                                                                                                                                                                  |
        | qElemNumber | Unique identifier for each cell, calculated by the engine during the construction of the grid.  This element number is not stored in the database and can have a positive or a negative value. | Integer                                                                                                                                                                                                          |
        | qState      | The default value is L.                                                                                                                                                                            | One of:*   L for Locked*   S for Selected*   O for Optional*   D for Deselected*   A for Alternative*   X for eXcluded*   XS for eXcluded Selected*   XL for eXcluded Locked |

        Parameters
        ----------
        qPath: str
          Path to the definition of the object.
          For example, /qHyperCubeDef .
        qPages: list[NxPage]
          Array of pages to retrieve.
          Since the generic object contains two measures and one dimension, qWidth should be set to 3.
          If the value of a measure is Null, the value cannot be rendered. Therefore, the number of elements rendered in a page can be less than the number defined in the property qHeight .
        qViewport: NxViewPort
          Defines the canvas and the zoom level.
          This parameter is not yet used and is optional.
        qDataRanges: list[NxDataAreaPage]
          Range of the data to render.
          This range applies to the measure values.
          The lowest and highest values of a measure can be retrieved by using the GetLayout method (in /qHyperCube/qMeasureInfo ).
        qMaxNbrCells: int
          Maximum number of cells in the grid.
        qQueryLevel: int
          Level of details. The higher the level, the more detailed information you get (zoom-in).
          When the number of points to render falls below a certain threshold, the values are no longer rendered as cells but as points.
          The query level should be no greater than 20.
        qBinningMethod: int
          Selects the algorithm.
          The default value is 0.
          One of:

          • 0: Adaptive grid

          • 1: Hexagonal grid

          • 2: Uniform grid
        """
        params = {}
        params["qPath"] = qPath
        params["qPages"] = qPages
        params["qViewport"] = qViewport
        params["qDataRanges"] = qDataRanges
        params["qMaxNbrCells"] = qMaxNbrCells
        params["qQueryLevel"] = qQueryLevel
        params["qBinningMethod"] = qBinningMethod
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetHyperCubeBinnedData", handle, **params)[
            "qDataPages"
        ]
        return [NxDataPage(**e) for e in response]

    def apply_patches(self, qPatches: list[NxPatch], qSoftPatch: bool = None) -> object:
        """
        Applies a patch to the properties of an object. Allows an update to some of the properties.
        It is possible to apply a patch to the properties of a generic object, that is not persistent. Such a patch is called a soft patch.
        In that case, the result of the operation on the properties (add, remove or delete) is not shown when doing GetProperties , and only a GetLayout call shows the result of the operation.
        Properties that are not persistent are called soft properties. Once the engine session is over, soft properties are cleared. It should not be possible to patch "/qInfo/qId",
        and it will be forbidden in the near future.
        Soft properties apply only to generic objects.

        Parameters
        ----------
        qPatches: list[NxPatch]
          Array of patches.
        qSoftPatch: bool = None
          If set to true, it means that the properties to be applied are not persistent. The patch is a soft patch.
          The default value is false.
        """
        params = {}
        params["qPatches"] = qPatches
        if qSoftPatch is not None:
            params["qSoftPatch"] = qSoftPatch
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ApplyPatches", handle, **params)
        return response

    def clear_soft_patches(self) -> object:
        """
        Clears the soft properties of a generic object.
        For more information on how to add soft properties to a generic object, see ApplyPatches Method.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ClearSoftPatches", handle)
        return response

    def set_properties(self, qProp: GenericObjectProperties) -> object:
        """
        Sets some properties for a generic object.
        The properties depends on the generic object type, see properties genericobject-property.html.

        Parameters
        ----------
        qProp: GenericObjectProperties
          Information about the generic object.
        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetProperties", handle, **params)
        return response

    def get_properties(self) -> GenericObjectProperties:
        """
        Returns the identifier, the type and the properties of the object.
        Because it is not mandatory to set all properties when you define an object, the GetProperties method may show properties that were not set. In that case, default values are given.
        If the object contains some soft properties, the soft properties are not returned by the GetProperties method. Use the GetEffectiveProperties method instead.
        If the object is linked to another object, the properties of the linking object are not returned by the GetProperties method. Use the GetEffectiveProperties method instead.
        The properties depends on the generic object type, see properties genericobject-layout.html.
        If the member delta is set to true in the request object, only the delta is retrieved.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetProperties", handle)["qProp"]
        obj = GenericObjectProperties(**response)
        return obj

    def get_effective_properties(self) -> GenericObjectProperties:
        """
        Returns the identifier, the type and the properties of the object.
        If the object contains some soft properties, the soft properties are returned.
        If the object is linked to another object, the properties of the linking object are returned.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetEffectiveProperties", handle)["qProp"]
        obj = GenericObjectProperties(**response)
        return obj

    def set_full_property_tree(self, qPropEntry: GenericObjectEntry) -> object:
        """
        Sets the properties of:

        • A generic object.

        • The children of the generic object.

        • The bookmarks/embedded snapshots of the generic object.

        If the SetFullPropertyTree method is asked to set some properties to a child that does not exist, it creates the child.  The type of an object cannot be updated.

        Parameters
        ----------
        qPropEntry: GenericObjectEntry
          Information about the generic object entry.
        """
        params = {}
        params["qPropEntry"] = qPropEntry
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetFullPropertyTree", handle, **params)
        return response

    def get_full_property_tree(self) -> GenericObjectEntry:
        """
        Gets the properties of:

        • A generic object.

        • The children of the generic object.

        • The bookmarks/embedded snapshots of the generic object.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFullPropertyTree", handle)["qPropEntry"]
        obj = GenericObjectEntry(**response)
        return obj

    def get_info(self) -> NxInfo:
        """
        Returns the type and identifier of the object.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetInfo", handle)["qInfo"]
        obj = NxInfo(**response)
        return obj

    def clear_selections(self, qPath: str, qColIndices: list[int] = None) -> object:
        """
        Clears the selections in a dimension of a visualization.

        Parameters
        ----------
        qPath: str
          Path to the definition of the visualization.
          For example, /qListObjectDef .
        qColIndices: list[int] = None
          Array of dimension numbers or indexes. The selections are cleared in the specified dimensions.
          Dimension numbers/indexes start from 0.
          If this parameter is not set, all dimensions are cleared.
        """
        params = {}
        params["qPath"] = qPath
        if qColIndices is not None:
            params["qColIndices"] = qColIndices
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ClearSelections", handle, **params)
        return response

    def export_data(
        self,
        qFileType: str,
        qPath: str = None,
        qFileName: str = None,
        qExportState: str = None,
        qServeOnce: bool = None,
    ) -> ExportDataReturn:
        """
        Exports the data of any generic object to an Excel file or a open XML file. If the object contains excluded values, those excluded values are not exported.
        This API has limited functionality and will not support CSV export from all types of objects. Consider using Excel export instead. Treemap and bar chart are not supported.
        ExportData method is not supported in SaaS Editions of Qlik Sense.

         Default limitations in number of rows and columns:
        The default maximum number of rows and columns in the Excel export file is:

        • 1048566 rows per sheet. For pivot tables: 1048566 column dimensions. 10 rows can be added after the export.

        • 16384 columns per sheet. If the number of columns exceeds the limit, the exported file is truncated and a warning message is sent.

         Default limitation in number of columns:
        The default maximum number of columns in the export file is:

        • 1000 to export to a CSV file

         Default limitations in number of cells:
        The default maximum number of cells in the export file is:

        • 5000000 to export to a CSV file

        The exported file is truncated if the number of cells exceeds the limit. A warning message with code 1000 is sent.
        There is an option to export only the possible values ( qExportState is P).

         Default limitation in size:
        If the exported file is larger than the maximum value, then an out-of-memory error with code 13000 is returned.

        Exported files are temporary and are available only for a certain time span and only to the user who created them.

        Parameters
        ----------
        qFileType: str
          Type of the file to export.

          One of:

          • CSV_C or EXPORT_CSV_C

          • CSV_T or EXPORT_CSV_T

          • OOXML or EXPORT_OOXML

          • PARQUET or EXPORT_PARQUET
        qPath: str = None
          Path to the definition of the object to be exported.
          For example, /qHyperCubeDef .
          This parameter is mandatory if the file type is CSV_C or CSV_T .
        qFileName: str = None
          Name of the exported file after download from browser.
          This parameter is optional and only used in Qlik Sense Desktop.
        qExportState: str = None
          Defines the values to be exported.
          The default value is A.

          One of:

          • P or EXPORT_POSSIBLE

          • A or EXPORT_ALL
        qServeOnce: bool = None
          If the exported file should be served only once
          This parameter is optional and only used in Qlik Sense Enterprise (Windows)
          Default value: false
        """
        params = {}
        params["qFileType"] = qFileType
        if qPath is not None:
            params["qPath"] = qPath
        if qFileName is not None:
            params["qFileName"] = qFileName
        if qExportState is not None:
            params["qExportState"] = qExportState
        if qServeOnce is not None:
            params["qServeOnce"] = qServeOnce
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ExportData", handle, **params)
        obj = ExportDataReturn(**response)
        return obj

    def select_list_object_values(
        self, qPath: str, qValues: list[int], qToggleMode: bool, qSoftLock: bool = None
    ) -> bool:
        """
        Makes single selections in dimensions.
        This method applies to list objects only.
        The member Change returns the handles of the objects that are updated following the selections.
        qSuccess is set to true if the selections are successful and is set to false in the following cases:

        • The object contains invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be selected.
          For example, /qListObjectDef .
        qValues: list[int]
          Element numbers to select.
          You can select multiple values; the separator is the comma.
        qToggleMode: bool
          Set to true to toggle.
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.
        """
        params = {}
        params["qPath"] = qPath
        params["qValues"] = qValues
        params["qToggleMode"] = qToggleMode
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectListObjectValues", handle, **params)[
            "qSuccess"
        ]
        return response

    def select_list_object_possible(self, qPath: str, qSoftLock: bool = None) -> bool:
        """
        Selects all possible values of a list object.
        This method applies to list objects (objects with one dimension).
        The member Change returns the handles of the objects that are updated following the selections.
        qSuccess is set to true if the selections are successful and is set to false in the following cases:

        • The object contains invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be selected.
          For example, /qListObjectDef .
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.
        """
        params = {}
        params["qPath"] = qPath
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectListObjectPossible", handle, **params)[
            "qSuccess"
        ]
        return response

    def select_list_object_excluded(self, qPath: str, qSoftLock: bool = None) -> bool:
        """
        Inverts the current selections in a specific field.
        This method applies to list objects (objects with one dimension).
        The member Change returns the handles of the objects that are updated following the selections.
        qSuccess is set to true if the selections are successful and is set to false in the following cases:

        • The object contains some invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be selected.
          For example, /qListObjectDef .
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.
        """
        params = {}
        params["qPath"] = qPath
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectListObjectExcluded", handle, **params)[
            "qSuccess"
        ]
        return response

    def select_list_object_alternative(
        self, qPath: str, qSoftLock: bool = None
    ) -> bool:
        """
        Selects all alternative values in a specific field.
        This method applies to list objects (objects with one dimension). If a field contains at least one selected value, the values that are neither selected nor excluded are alternatives values.
        The member Change returns the handles of the objects that are updated following the selections.
        qSuccess is set to true if the selections are successful and is set to false in the following cases:

        • The object contains some invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be selected.
          For example, /qListObjectDef .
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.
        """
        params = {}
        params["qPath"] = qPath
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectListObjectAlternative", handle, **params)[
            "qSuccess"
        ]
        return response

    def select_list_object_all(self, qPath: str, qSoftLock: bool = None) -> bool:
        """
        Selects all values of a field.
        This method applies to list objects (objects with one dimension).
        The member Change returns the handles of the objects that are updated following the selections.
        qSuccess is set to true if the selections are successful and is set to false in the following cases:

        • The object contains some invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be selected.
          For example, /qListObjectDef .
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.
        """
        params = {}
        params["qPath"] = qPath
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectListObjectAll", handle, **params)[
            "qSuccess"
        ]
        return response

    def select_list_object_continuous_range(
        self, qPath: str, qRanges: list[Range], qSoftLock: bool = None
    ) -> bool:
        """
        The following is returned in the output:
        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object.
          For example, /qHyperCubeDef .
        qRanges: list[Range]
          Selects ranges in a hypercube in (Ranges[N].Min,Ranges[N].Max) intervals.
          If either Ranges[N].MinInclEq or Ranges[N].MaxInclEq, or both flags are set to true then Min and Max values will be selected.
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.
        """
        params = {}
        params["qPath"] = qPath
        params["qRanges"] = qRanges
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send(
            "SelectListObjectContinuousRange", handle, **params
        )["qSuccess"]
        return response

    def search_list_object_for(self, qPath: str, qMatch: str) -> bool:
        """
        Searches for a string in a list object.
        This method applies to list objects (objects with one dimension). The search results can be displayed using the GetLayout Method.

        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        qPath: str
          Path to the definition of the list object.
          For example, /qListObjectDef .
        qMatch: str
          Search string.
          Wild card characters are allowed. The search is not case sensitive.
          Examples:

          • `P*U*`: retrieves only values that start with P and contain U

          • `P U S`: retrieves values that start with P, U or S
        """
        params = {}
        params["qPath"] = qPath
        params["qMatch"] = qMatch
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SearchListObjectFor", handle, **params)[
            "qSuccess"
        ]
        return response

    def abort_list_object_search(self, qPath: str) -> object:
        """
        Aborts the results of a search in a list object.
        This method applies to list objects (objects with one dimension).  After an abort on a list object search, the GetLayout Method does not return any more search results but it does return the values in the field.

        Parameters
        ----------
        qPath: str
          Path to the definition of the list object.
          For example, /qListObjectDef .
        """
        params = {}
        params["qPath"] = qPath
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AbortListObjectSearch", handle, **params)
        return response

    def accept_list_object_search(
        self, qPath: str, qToggleMode: bool, qSoftLock: bool = None
    ) -> object:
        """
        Accept the results of a search in a list object. The search results become selected in the field.
        This method applies to list objects (objects with one dimension). The search results are displayed using the GetLayout Method.

        Parameters
        ----------
        qPath: str
          Path to the definition of the list object.
          For example, /qListObjectDef .
        qToggleMode: bool
          Set to true to keep any selections present in the list object.
          If this parameter is set to false, selections made before accepting the list object search become alternative.
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.
        """
        params = {}
        params["qPath"] = qPath
        params["qToggleMode"] = qToggleMode
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AcceptListObjectSearch", handle, **params)
        return response

    def expand_left(self, qPath: str, qRow: int, qCol: int, qAll: bool) -> object:
        """
        Expands the left dimensions of a pivot table. This method applies only to pivot tables that are not always fully expanded.
        In the definition of the hypercube (in HyperCubeDef ), the parameter qAlwaysFullyExpanded must be set to false.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be expanded.
          For example, /qHyperCubeDef .
        qRow: int
          Row index in the data matrix to expand.
          Indexing starts from 0.
        qCol: int
          Column index. The index is based on the left dimension indexes.
          Indexing starts from 0.
        qAll: bool
          If set to true, it expands all cells.
          Parameters qRow and qCol are not used if qAll is set to true, but they need to be set (for example to 0).
        """
        params = {}
        params["qPath"] = qPath
        params["qRow"] = qRow
        params["qCol"] = qCol
        params["qAll"] = qAll
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ExpandLeft", handle, **params)
        return response

    def expand_top(self, qPath: str, qRow: int, qCol: int, qAll: bool) -> object:
        """
        Expands the top dimensions of a pivot table. This method applies only to pivot tables that are not always fully expanded.
        In the definition of the hypercube (in HyperCubeDef ), the parameter qAlwaysFullyExpanded must be set to false.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be expanded.
          For example, /qHyperCubeDef .
        qRow: int
          Row index. The index is based on the top dimension indexes.
          Indexing starts from 0.
        qCol: int
          Column index in the data matrix.
          Indexing starts from 0.
        qAll: bool
          If set to true, it expands all cells.
          Parameters qRow and qCol are not used if qAll is set to true, but they need to be set (for example to 0).
        """
        params = {}
        params["qPath"] = qPath
        params["qRow"] = qRow
        params["qCol"] = qCol
        params["qAll"] = qAll
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ExpandTop", handle, **params)
        return response

    def collapse_left(self, qPath: str, qRow: int, qCol: int, qAll: bool) -> object:
        """
        Collapses the left dimensions of a pivot table. This method applies only to pivot tables that are not always fully expanded.
        In the definition of the hypercube (in HyperCubeDef ), the parameter qAlwaysFullyExpanded must be set to false.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be collapsed.
          For example, /qHyperCubeDef .
        qRow: int
          Row index in the data matrix.
          Indexing starts from 0.
        qCol: int
          Column index. The index is based on the left dimension indexes.
          Indexing starts from 0.
        qAll: bool
          If set to true, it collapses all cells.
          Parameters qRow and qCol are not used if qAll is set to true, but they need to be set (for example to 0).
        """
        params = {}
        params["qPath"] = qPath
        params["qRow"] = qRow
        params["qCol"] = qCol
        params["qAll"] = qAll
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CollapseLeft", handle, **params)
        return response

    def collapse_top(self, qPath: str, qRow: int, qCol: int, qAll: bool) -> object:
        """
        Collapses the top dimensions of a pivot table. This method applies only to pivot tables that are not always fully expanded.
        In the definition of the hypercube (in HyperCubeDef ), the parameter qAlwaysFullyExpanded must be set to false.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be collapsed
          For example, /qHyperCubeDef .
        qRow: int
          Row index. The index is based on the top dimension indexes.
          Indexing starts from 0.
        qCol: int
          Column index in the data matrix.
          Indexing starts from 0.
        qAll: bool
          If set to true, it collapses all cells.
          Parameters qRow and qCol are not used if qAll is set to true, but they need to be set (for example to 0).
        """
        params = {}
        params["qPath"] = qPath
        params["qRow"] = qRow
        params["qCol"] = qCol
        params["qAll"] = qAll
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CollapseTop", handle, **params)
        return response

    def drill_up(self, qPath: str, qDimNo: int, qNbrSteps: int) -> object:
        """
        You can use the drillUp method with any object that contains a drill-down group as a dimension.
        This method allows you to move between different levels of information (from a detailed level to a less detailed level of information). You can go back to previous visualizations up to the highest level of the hierarchy.
        If you try to drill up more steps than there are available levels, the first level of the hierarchy is displayed.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .
        qDimNo: int
          Dimension number or index starting from 0.
          The default value is 0.
        qNbrSteps: int
          Number of steps you want to drill up.
          The default value is 0.
        """
        params = {}
        params["qPath"] = qPath
        params["qDimNo"] = qDimNo
        params["qNbrSteps"] = qNbrSteps
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DrillUp", handle, **params)
        return response

    def lock(self, qPath: str, qColIndices: list[int] = None) -> object:
        """
        Locks the selected values of a generic object.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object.
          For example, /qListObjectDef .
        qColIndices: list[int] = None
          Dimension numbers or dimension indexes where the lock should apply.
          Dimension numbers/indexes start from 0.
          If this parameter is not set, the selected values in all dimensions are locked.
        """
        params = {}
        params["qPath"] = qPath
        if qColIndices is not None:
            params["qColIndices"] = qColIndices
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Lock", handle, **params)
        return response

    def unlock(self, qPath: str, qColIndices: list[int] = None) -> object:
        """
        Unlocks the selected values of a generic object if the target (or handle ) is a generic object

        Parameters
        ----------
        qPath: str
          Path to the definition of the object.
          For example, /qListObjectDef .
        qColIndices: list[int] = None
          Dimension numbers/indexes where the unlock should apply.
          Dimension numbers/indexes start from 0.
          If this parameter is not set, the locked values in all dimensions are unlocked.
        """
        params = {}
        params["qPath"] = qPath
        if qColIndices is not None:
            params["qColIndices"] = qColIndices
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Unlock", handle, **params)
        return response

    def select_hyper_cube_values(
        self, qPath: str, qDimNo: int, qValues: list[int], qToggleMode: bool
    ) -> bool:
        """
        Selects some values in one dimension.
        The values are identified by their element numbers.
        This method applies to charts, tables and scatter plots.
        The member Change returns the handles of the objects that are updated following the selections.
        qSuccess is set to true if the selections are successful and is set to false in the following cases:

        • The object contains some invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .
        qDimNo: int
          Dimension number or index to select.
          Dimension numbers/index start from 0.
        qValues: list[int]
          Element numbers of the field to select.
          You can select multiple elements; the separator is the comma.
        qToggleMode: bool
          Set to true to toggle.
        """
        params = {}
        params["qPath"] = qPath
        params["qDimNo"] = qDimNo
        params["qValues"] = qValues
        params["qToggleMode"] = qToggleMode
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectHyperCubeValues", handle, **params)[
            "qSuccess"
        ]
        return response

    def select_hyper_cube_cells(
        self,
        qPath: str,
        qRowIndices: list[int],
        qColIndices: list[int],
        qSoftLock: bool = None,
        qDeselectOnlyOneSelected: bool = None,
    ) -> bool:
        """
        Makes selections in multiple dimensions and measures.
         This method applies to hypercubes, such as bar charts, tables and scatter plots.
        The member Change returns the handles of the objects that are updated following the selections.
        qSuccess is set to true if the selections are successful and is set to false in the following cases:

        • The object contains some invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .
        qRowIndices: list[int]
          Array of row indexes to select, starting from 0.
          If the array is empty [ ] , all rows are selected.
        qColIndices: list[int]
          Indexes of the columns to select, starting from 0.
          A column corresponds to a dimension in the order they are added to the hypercube.
          If a column is hidden it is ignored, qColIndex n refers to the n:th visible column (starting from zero).
          Example:
          If the hypercube has two dimensions:

          • [0] selects the first column (i.e the first dimension).

          • [1] selects the second column (i.e the second dimension).

          If the array is empty [ ] , all columns are selected.
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
        qDeselectOnlyOneSelected: bool = None
          Set this parameter to true to unselect the last single selected value. There must be only one selected value in the field.
          The default value is false.
        """
        params = {}
        params["qPath"] = qPath
        params["qRowIndices"] = qRowIndices
        params["qColIndices"] = qColIndices
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        if qDeselectOnlyOneSelected is not None:
            params["qDeselectOnlyOneSelected"] = qDeselectOnlyOneSelected
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectHyperCubeCells", handle, **params)[
            "qSuccess"
        ]
        return response

    def select_pivot_cells(
        self,
        qPath: str,
        qSelections: list[NxSelectionCell],
        qSoftLock: bool = None,
        qDeselectOnlyOneSelected: bool = None,
    ) -> bool:
        """
        This method only applies to hypercubes that are not represented as straight tables. The parameter qMode in HyperCubeDef must be set either to P  or K .

         Pivot table:
        Makes selections in the top or left dimension cells of a pivot table or in the data matrix. Only expanded dimensions can be selected.

         Stacked table:
        Makes selections in the left dimension cells of a stacked table or in the data matrix.
        There is no top dimensions in a stacked table. A stacked table can only contain one measure.

         Example of a pivot table:

        In the representation above:
        |                                        |                                                                                     |
        |----------------------------------------|-------------------------------------------------------------------------------------|
        | Sum(OrderTotal)  Count(OrderTotal) | Are pseudo dimensions.                                                              |
        | CategoryName                           | Is a left dimension.  _Beverages_ , _Condiments_ ... are left dimension values. |
        | ProductName                            | Is a top dimension.  _Chef Anton's Cajun Seasoning_ is a top dimension value.   |
        | Numeric values                         | Are calculated values in the data matrix.  _626291,832_ is a calculated value.  |

        The member Change returns the handles of the objects that are updated following the selections.
        qSuccess is set to true if the selections are successful and is set to false in the following cases:

        • The object contains some invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object.
          For example, /qHyperCubeDef .
        qSelections: list[NxSelectionCell]
          Information about the selections to perform.
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
        qDeselectOnlyOneSelected: bool = None
          Set this parameter to true to unselect the last single selected value. There must be only one selected value in the field.
          The default value is false.
        """
        params = {}
        params["qPath"] = qPath
        params["qSelections"] = qSelections
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        if qDeselectOnlyOneSelected is not None:
            params["qDeselectOnlyOneSelected"] = qDeselectOnlyOneSelected
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SelectPivotCells", handle, **params)["qSuccess"]
        return response

    def range_select_hyper_cube_values(
        self,
        qPath: str,
        qRanges: list[NxRangeSelectInfo],
        qColumnsToSelect: list[int] = None,
        qOrMode: bool = None,
        qDeselectOnlyOneSelected: bool = None,
    ) -> bool:
        """
        Makes range selections in measures.
         This method applies to hypercubes. For example, bar charts, tables and scatter plots.
        The member Change returns the handles of the objects that are updated following the selections.
        qSuccess is set to true if the selections are successful and is set to false in the following cases:

        • The object contains some invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .
        qRanges: list[NxRangeSelectInfo]
          Ranges of selections.
        qColumnsToSelect: list[int] = None
          Indicates which dimensions to select.
          The dimensions numbering starts at 0 (first dimension is 0).
          If the array is empty, all dimensions are selected.
        qOrMode: bool = None
          Applies to hypercubes with multiple measures.
          If set to true, it means that at least one of the measures must be in the range of selections for the group of measures to be selected.
          If set to false, it means that all measures must be in the range of selections for the group of measures to be selected.
          The default value is false.
        qDeselectOnlyOneSelected: bool = None
          Set this parameter to true to unselect the last single selected value. There must be only one selected value in the field.
          The default value is false.
        """
        params = {}
        params["qPath"] = qPath
        params["qRanges"] = qRanges
        if qColumnsToSelect is not None:
            params["qColumnsToSelect"] = qColumnsToSelect
        if qOrMode is not None:
            params["qOrMode"] = qOrMode
        if qDeselectOnlyOneSelected is not None:
            params["qDeselectOnlyOneSelected"] = qDeselectOnlyOneSelected
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("RangeSelectHyperCubeValues", handle, **params)[
            "qSuccess"
        ]
        return response

    def multi_range_select_hyper_cube_values(
        self,
        qPath: str,
        qRanges: list[NxMultiRangeSelectInfo],
        qOrMode: bool = None,
        qDeselectOnlyOneSelected: bool = None,
    ) -> bool:
        """
        Makes multiple range selections in measures.
         This method applies to hypercubes. For example, bar charts, tables and scatter plots.
        The member Change returns the handles of the objects that are updated following the selections.
        qSuccess is set to true if the selections are successful and is set to false in the following cases:

        • The object contains some invalid fields (fields that are not in the data model).

        • The selection applies to a locked field.

        • A range selection is performed and the parameter OneAndOnlyOne is set to true in the definition of the object.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object to be selected.
          For example, /qHyperCubeDef .
        qRanges: list[NxMultiRangeSelectInfo]
          Ranges of selections.
        qOrMode: bool = None
          Applies to hypercubes with multiple measures.
          If set to true, it means that at least one of the measures must be in the range of selections for the group of measures to be selected.
          If set to false, it means that all measures must be in the range of selections for the group of measures to be selected.
          The default value is false.
        qDeselectOnlyOneSelected: bool = None
          Set this parameter to true to unselect the last single selected value. There must be only one selected value in the field.
          The default value is false.
        """
        params = {}
        params["qPath"] = qPath
        params["qRanges"] = qRanges
        if qOrMode is not None:
            params["qOrMode"] = qOrMode
        if qDeselectOnlyOneSelected is not None:
            params["qDeselectOnlyOneSelected"] = qDeselectOnlyOneSelected
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send(
            "MultiRangeSelectHyperCubeValues", handle, **params
        )["qSuccess"]
        return response

    def multi_range_select_tree_data_values(
        self,
        qPath: str,
        qRanges: list[NxTreeMultiRangeSelectInfo],
        qOrMode: bool = None,
        qDeselectOnlyOneSelected: bool = None,
    ) -> bool:
        """
        Parameters
        ----------
        qPath: str
        qRanges: list[NxTreeMultiRangeSelectInfo]
        qOrMode: bool = None
        qDeselectOnlyOneSelected: bool = None
        """
        params = {}
        params["qPath"] = qPath
        params["qRanges"] = qRanges
        if qOrMode is not None:
            params["qOrMode"] = qOrMode
        if qDeselectOnlyOneSelected is not None:
            params["qDeselectOnlyOneSelected"] = qDeselectOnlyOneSelected
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send(
            "MultiRangeSelectTreeDataValues", handle, **params
        )["qSuccess"]
        return response

    def select_hyper_cube_continuous_range(
        self,
        qPath: str,
        qRanges: list[NxContinuousRangeSelectInfo],
        qSoftLock: bool = None,
    ) -> bool:
        """
        The following is returned in the output:
        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        qPath: str
          Path to the definition of the object.
          For example, /qHyperCubeDef .
        qRanges: list[NxContinuousRangeSelectInfo]
          Selects ranges in a hypercube in (Ranges[N].Min,Ranges[N].Max) intervals.
          If either Ranges[N].MinInclEq or Ranges[N].MaxInclEq, or both flags are set to true then Min and Max values will be selected.
        qSoftLock: bool = None
          Set to true to ignore locks; in that case, locked fields can be selected.
          The default value is false.
        """
        params = {}
        params["qPath"] = qPath
        params["qRanges"] = qRanges
        if qSoftLock is not None:
            params["qSoftLock"] = qSoftLock
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send(
            "SelectHyperCubeContinuousRange", handle, **params
        )["qSuccess"]
        return response

    def get_child(self, qId: str) -> GenericObject:
        """
        Returns the type of the object and the corresponding handle.

        Parameters
        ----------
        qId: str
          Identifier of the object.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetChild", handle, **params)["qReturn"]
        obj = GenericObject(_session=self._session, **response)
        return obj

    def get_parent(self) -> GenericObject:
        """
        Returns the type of the object and the corresponding handle to the parent object in the hiearchy.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetParent", handle)["qReturn"]
        obj = GenericObject(_session=self._session, **response)
        return obj

    def get_child_infos(self) -> list[NxInfo]:
        """
        Returns the identifier and the type for each child in an app object. If the child contains extra properties in qInfos , these properties are returned.

        Full dynamic properties are optional and are returned if they exist in the definition of the object.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetChildInfos", handle)["qInfos"]
        return [NxInfo(**e) for e in response]

    def create_child(
        self,
        qProp: GenericObjectProperties,
        qPropForThis: GenericObjectProperties = None,
    ) -> GenericObject:
        """
        Creates a generic object that is a child of another generic object.
        It is possible to update the properties of the child's parent at the same time that the child is created. Both operations are performed by the same call. It is possible to create a child that is linked to another generic object. The two objects have the same properties.

        Parameters
        ----------
        qProp: GenericObjectProperties
          Information about the child.
          It is possible to create a child that is linked to another object.
        qPropForThis: GenericObjectProperties = None
          Identifier of the parent's object.
          Should be set to update the properties of the parent's object at the same time the child is created.
        """
        params = {}
        params["qProp"] = qProp
        if qPropForThis is not None:
            params["qPropForThis"] = qPropForThis
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CreateChild", handle, **params)["qReturn"]
        obj = GenericObject(_session=self._session, **response)
        return obj

    def destroy_child(
        self, qId: str, qPropForThis: GenericObjectProperties = None
    ) -> bool:
        """
        Removes a child object.
        It is possible to update the properties of the child's parent at the same time that the child is removed. Both operations are performed by the same call. Removing a linked object, invalidate the linking object.

        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        qId: str
          Identifier of the child to remove.
        qPropForThis: GenericObjectProperties = None
          Identifier of the parent's object and property to update.
          Should be set to update the properties of the parent's object at the same time the child is created.
        """
        params = {}
        params["qId"] = qId
        if qPropForThis is not None:
            params["qPropForThis"] = qPropForThis
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyChild", handle, **params)["qSuccess"]
        return response

    def destroy_all_children(
        self, qPropForThis: GenericObjectProperties = None
    ) -> object:
        """
        Removes all children and all children to the children on an object.

        Parameters
        ----------
        qPropForThis: GenericObjectProperties = None
          Identifier of the parent's object and property to update.
          Should be set to update the properties of the parent's object at the same time the child is created.
        """
        params = {}
        if qPropForThis is not None:
            params["qPropForThis"] = qPropForThis
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("DestroyAllChildren", handle, **params)
        return response

    def set_child_array_order(self, qIds: list[str]) -> object:
        """
        Sets the order of the children in a generic object.
        To change the order of the children in a generic object, the identifiers of all the children must be included in the list of the identifiers (in qIds ).

        Parameters
        ----------
        qIds: list[str]
          List of the children identifiers.
        """
        params = {}
        params["qIds"] = qIds
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetChildArrayOrder", handle, **params)
        return response

    def get_linked_objects(self) -> list[NxLinkedObjectInfo]:
        """
        Lists the linked objects to a generic object, a dimension or a measure.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLinkedObjects", handle)["qItems"]
        return [NxLinkedObjectInfo(**e) for e in response]

    def copy_from(self, qFromId: str) -> object:
        """
        Copies the properties of a generic object and its children.
        The source object is specified by the parameter qFromId and the destination object is referenced by its handle.
        The identifier of the destination object is the same as before the copy takes place.

        Parameters
        ----------
        qFromId: str
          Identifier of the object to copy.
        """
        params = {}
        params["qFromId"] = qFromId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CopyFrom", handle, **params)
        return response

    def begin_selections(self, qPaths: list[str]) -> object:
        """
        Begins the selection mode. The app enters the modal state. The specified object enters the selection mode and a modal window is opened. The selection mode can apply to only one object in an app at a time.
        When a visualization is in selection mode, selections can be made in this visualization. The visualization is not sorted until the selection mode is ended. Once the selection mode is ended and if the selections are accepted, the visualization is sorted according to the sort criteria. For more information about:

        • Ending the selection mode, see EndSelections Method.

        • The sort criteria, see ListObjectDef or HyperCubeDef.

         Example:
        A sheet contains a list object and a chart. If the list object is in selection mode then the chart cannot be in selection mode. No selection on the chart can be made until the list object exits the selection mode.

        Parameters
        ----------
        qPaths: list[str]
          List of the paths to the definition of the objects to enter selection mode.
          For example, /qListObjectDef .
        """
        params = {}
        params["qPaths"] = qPaths
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("BeginSelections", handle, **params)
        return response

    def end_selections(self, qAccept: bool) -> object:
        """
        Ends the selection mode on a visualization. The selections are accepted or aborted when exiting the selection mode, depending on the qAccept parameter value.

        Parameters
        ----------
        qAccept: bool
          Set this parameter to true to accept the selections before exiting the selection mode.
        """
        params = {}
        params["qAccept"] = qAccept
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("EndSelections", handle, **params)
        return response

    def reset_made_selections(self) -> object:
        """
        Resets all selections made in selection mode.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ResetMadeSelections", handle)
        return response

    def embed_snapshot_object(self, qId: str) -> object:
        """
        Adds a snapshot to a generic object.
        Only one snapshot can be embedded in a generic object. If you embed a snapshot in an object that already contains a snapshot, the new snapshot overwrites the previous one.

        Parameters
        ----------
        qId: str
          Identifier of the bookmark.
        """
        params = {}
        params["qId"] = qId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("EmbedSnapshotObject", handle, **params)
        return response

    def get_snapshot_object(self) -> GenericObject:
        """
        Returns the type of the object and the corresponding handle.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetSnapshotObject", handle)["qReturn"]
        obj = GenericObject(_session=self._session, **response)
        return obj

    def publish(self) -> object:
        """
        Publishes a generic object.
        This operation is not applicable for Qlik Sense Desktop.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Publish", handle)
        return response

    def un_publish(self) -> object:
        """
        Unpublishes a generic object.
        This operation is not applicable for Qlik Sense Desktop.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnPublish", handle)
        return response

    def approve(self) -> object:
        """
        Adds the generic object to the list of approved objects
        This operation is possible only in Qlik Sense Enterprise.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("Approve", handle)
        return response

    def un_approve(self) -> object:
        """
        Removes the generic object from the list of approved objects
        This operation is possible only in Qlik Sense Enterprise.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("UnApprove", handle)
        return response

    def on(self, event_name, listener):
        self._session.on_handle(self.qHandle, event_name, listener)


@dataclass
class GenericObjectEntry:
    """

    Attributes
    ----------
    qChildren: list[GenericObjectEntry]
      Information about the children of the generic object.
    qEmbeddedSnapshotRef: GenericBookmarkEntry
      Reference to a bookmark/snapshot that is embedded in the generic object.
    qProperty: GenericObjectProperties
      Information about the generic object properties.
    """

    qChildren: list[GenericObjectEntry] = None
    qEmbeddedSnapshotRef: GenericBookmarkEntry = None
    qProperty: GenericObjectProperties = None

    def __init__(self_, **kvargs):
        if "qChildren" in kvargs and kvargs["qChildren"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == GenericObjectEntry.__annotations__["qChildren"]
                for e in kvargs["qChildren"]
            ):
                self_.qChildren = kvargs["qChildren"]
            else:
                self_.qChildren = [
                    GenericObjectEntry(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qChildren"]
                ]
        if (
            "qEmbeddedSnapshotRef" in kvargs
            and kvargs["qEmbeddedSnapshotRef"] is not None
        ):
            if (
                type(kvargs["qEmbeddedSnapshotRef"]).__name__
                == GenericObjectEntry.__annotations__["qEmbeddedSnapshotRef"]
            ):
                self_.qEmbeddedSnapshotRef = kvargs["qEmbeddedSnapshotRef"]
            else:
                self_.qEmbeddedSnapshotRef = GenericBookmarkEntry(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qEmbeddedSnapshotRef"],
                )
        if "qProperty" in kvargs and kvargs["qProperty"] is not None:
            if (
                type(kvargs["qProperty"]).__name__
                == GenericObjectEntry.__annotations__["qProperty"]
            ):
                self_.qProperty = kvargs["qProperty"]
            else:
                self_.qProperty = GenericObjectProperties(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qProperty"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericObjectLayout:
    """
    Is the layout for GenericObjectProperties.

    Attributes
    ----------
    qError: NxLayoutErrors
      Gives information on the error.
      This parameter is optional.
    qExtendsId: str
      Should be set to create an object that is linked to another object. Enter the identifier of the object you want to link to.
      If you do not want to link your object, set this parameter to an empty string.
    qHasSoftPatches: bool
      Is set to true if the generic object contains some properties that are not persistent (a soft patch was applied).
    qInfo: NxInfo
      Identifier and type of the generic object.
    qMeta: NxMeta
      Information about publishing and permissions.
      This parameter is optional.
    qSelectionInfo: NxSelectionInfo
      Information about the selections.
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    qAppObjectList: AppObjectList
      Lists the app objects. Is the layout for AppObjectListDef.
      An app object is a generic object created at app level.
    qBookmarkList: BookmarkList
      Lists the bookmarks. Is the layout for BookmarkListDef.
    qChildList: ChildList
      Lists the children of a generic object. Is the layout for ChildListDef.
      ChildList is used by the GetLayout Method to list the children of a generic object.
    qDimensionList: DimensionList
      Lists the dimensions. Is the layout for DimensionListDef.
    qEmbeddedSnapshot: EmbeddedSnapshot
      Renders the embedded snapshot in an object.
      The following is returned:

      • Any dynamic properties defined in the bookmark

      • Any properties defined in qEmbeddedSnapshot

       Properties:
      "qEmbeddedSnapshot": {}
    qExtensionList: ExtensionList
      Obsolete, use qrs API's to fetch extensions.
    qFieldList: FieldList
      Lists the fields present in the data model viewer. Is the layout for FieldListDef.
    qHyperCube: HyperCube
      Renders the properties of a hypercube. Is the layout for HyperCubeDef.
      For more information about the definition of a hypercube, see Generic object.
      What is returned in HyperCube depends on the type of the hypercube (straight, pivot or stacked table, or tree) and on the method called (GetLayout, GetHyperCubeData, GetHyperCubePivotData, GetHyperCubeStackData, GetHyperCubeTreeData).
    qListObject: ListObject
      Renders the properties of a list object. Is the layout for ListObjectDef.
      For more information about the definition of a list object, see Generic object.
      ListObject is used by the GetLayout Method to display the properties of a list object.
    qMeasureList: MeasureList
      Lists the measures. Is the layout for MeasureListDef.
    qMediaList: MediaList
      Lists the media files. Is the layout for MediaListDef.
      This struct is deprecated.
    qNxLibraryDimension: NxLibraryDimension
    qNxLibraryMeasure: NxLibraryMeasure
      Information about the library measure. Is the layout for NxLibraryMeasureDef.
    qSelectionObject: SelectionObject
      Indicates which selections are currently applied. It gives the current selections. Is the layout for SelectionObjectDef.
    qStaticContentUrl: StaticContentUrl
      In addition, this structure can return dynamic properties.
    qTreeData: TreeData
      Renders the properties of a TreeData object. Is the layout for TreeDataDef.
      For more information about the definition of TreeData, see Generic object.
      To retrieve data from the TreeData object, use the method called GetHyperCubeTreeData.
    qUndoInfo: UndoInfo
      Displays information about the number of possible undos and redos. Is the layout for UndoInfoDef.
    qVariableList: VariableList
      Lists the variables in an app. Is the layout for VariableListDef.
    """

    qError: NxLayoutErrors = None
    qExtendsId: str = None
    qHasSoftPatches: bool = None
    qInfo: NxInfo = None
    qMeta: NxMeta = None
    qSelectionInfo: NxSelectionInfo = None
    qStateName: str = None
    qAppObjectList: AppObjectList = None
    qBookmarkList: BookmarkList = None
    qChildList: ChildList = None
    qDimensionList: DimensionList = None
    qEmbeddedSnapshot: EmbeddedSnapshot = None
    qExtensionList: ExtensionList = None
    qFieldList: FieldList = None
    qHyperCube: HyperCube = None
    qListObject: ListObject = None
    qMeasureList: MeasureList = None
    qMediaList: MediaList = None
    qNxLibraryDimension: NxLibraryDimension = None
    qNxLibraryMeasure: NxLibraryMeasure = None
    qSelectionObject: SelectionObject = None
    qStaticContentUrl: StaticContentUrl = None
    qTreeData: TreeData = None
    qUndoInfo: UndoInfo = None
    qVariableList: VariableList = None

    def __init__(self_, **kvargs):
        if "qError" in kvargs and kvargs["qError"] is not None:
            if (
                type(kvargs["qError"]).__name__
                == GenericObjectLayout.__annotations__["qError"]
            ):
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxLayoutErrors(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qError"],
                )
        if "qExtendsId" in kvargs and kvargs["qExtendsId"] is not None:
            self_.qExtendsId = kvargs["qExtendsId"]
        if "qHasSoftPatches" in kvargs and kvargs["qHasSoftPatches"] is not None:
            self_.qHasSoftPatches = kvargs["qHasSoftPatches"]
        if "qInfo" in kvargs and kvargs["qInfo"] is not None:
            if (
                type(kvargs["qInfo"]).__name__
                == GenericObjectLayout.__annotations__["qInfo"]
            ):
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qInfo"],
                )
        if "qMeta" in kvargs and kvargs["qMeta"] is not None:
            if (
                type(kvargs["qMeta"]).__name__
                == GenericObjectLayout.__annotations__["qMeta"]
            ):
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeta"],
                )
        if "qSelectionInfo" in kvargs and kvargs["qSelectionInfo"] is not None:
            if (
                type(kvargs["qSelectionInfo"]).__name__
                == GenericObjectLayout.__annotations__["qSelectionInfo"]
            ):
                self_.qSelectionInfo = kvargs["qSelectionInfo"]
            else:
                self_.qSelectionInfo = NxSelectionInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qSelectionInfo"],
                )
        if "qStateName" in kvargs and kvargs["qStateName"] is not None:
            self_.qStateName = kvargs["qStateName"]
        if "qAppObjectList" in kvargs and kvargs["qAppObjectList"] is not None:
            if (
                type(kvargs["qAppObjectList"]).__name__
                == GenericObjectLayout.__annotations__["qAppObjectList"]
            ):
                self_.qAppObjectList = kvargs["qAppObjectList"]
            else:
                self_.qAppObjectList = AppObjectList(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qAppObjectList"],
                )
        if "qBookmarkList" in kvargs and kvargs["qBookmarkList"] is not None:
            if (
                type(kvargs["qBookmarkList"]).__name__
                == GenericObjectLayout.__annotations__["qBookmarkList"]
            ):
                self_.qBookmarkList = kvargs["qBookmarkList"]
            else:
                self_.qBookmarkList = BookmarkList(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qBookmarkList"],
                )
        if "qChildList" in kvargs and kvargs["qChildList"] is not None:
            if (
                type(kvargs["qChildList"]).__name__
                == GenericObjectLayout.__annotations__["qChildList"]
            ):
                self_.qChildList = kvargs["qChildList"]
            else:
                self_.qChildList = ChildList(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qChildList"],
                )
        if "qDimensionList" in kvargs and kvargs["qDimensionList"] is not None:
            if (
                type(kvargs["qDimensionList"]).__name__
                == GenericObjectLayout.__annotations__["qDimensionList"]
            ):
                self_.qDimensionList = kvargs["qDimensionList"]
            else:
                self_.qDimensionList = DimensionList(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qDimensionList"],
                )
        if "qEmbeddedSnapshot" in kvargs and kvargs["qEmbeddedSnapshot"] is not None:
            if (
                type(kvargs["qEmbeddedSnapshot"]).__name__
                == GenericObjectLayout.__annotations__["qEmbeddedSnapshot"]
            ):
                self_.qEmbeddedSnapshot = kvargs["qEmbeddedSnapshot"]
            else:
                self_.qEmbeddedSnapshot = EmbeddedSnapshot(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qEmbeddedSnapshot"],
                )
        if "qExtensionList" in kvargs and kvargs["qExtensionList"] is not None:
            if (
                type(kvargs["qExtensionList"]).__name__
                == GenericObjectLayout.__annotations__["qExtensionList"]
            ):
                self_.qExtensionList = kvargs["qExtensionList"]
            else:
                self_.qExtensionList = ExtensionList(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qExtensionList"],
                )
        if "qFieldList" in kvargs and kvargs["qFieldList"] is not None:
            if (
                type(kvargs["qFieldList"]).__name__
                == GenericObjectLayout.__annotations__["qFieldList"]
            ):
                self_.qFieldList = kvargs["qFieldList"]
            else:
                self_.qFieldList = FieldList(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qFieldList"],
                )
        if "qHyperCube" in kvargs and kvargs["qHyperCube"] is not None:
            if (
                type(kvargs["qHyperCube"]).__name__
                == GenericObjectLayout.__annotations__["qHyperCube"]
            ):
                self_.qHyperCube = kvargs["qHyperCube"]
            else:
                self_.qHyperCube = HyperCube(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qHyperCube"],
                )
        if "qListObject" in kvargs and kvargs["qListObject"] is not None:
            if (
                type(kvargs["qListObject"]).__name__
                == GenericObjectLayout.__annotations__["qListObject"]
            ):
                self_.qListObject = kvargs["qListObject"]
            else:
                self_.qListObject = ListObject(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qListObject"],
                )
        if "qMeasureList" in kvargs and kvargs["qMeasureList"] is not None:
            if (
                type(kvargs["qMeasureList"]).__name__
                == GenericObjectLayout.__annotations__["qMeasureList"]
            ):
                self_.qMeasureList = kvargs["qMeasureList"]
            else:
                self_.qMeasureList = MeasureList(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeasureList"],
                )
        if "qMediaList" in kvargs and kvargs["qMediaList"] is not None:
            if (
                type(kvargs["qMediaList"]).__name__
                == GenericObjectLayout.__annotations__["qMediaList"]
            ):
                self_.qMediaList = kvargs["qMediaList"]
            else:
                self_.qMediaList = MediaList(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMediaList"],
                )
        if (
            "qNxLibraryDimension" in kvargs
            and kvargs["qNxLibraryDimension"] is not None
        ):
            if (
                type(kvargs["qNxLibraryDimension"]).__name__
                == GenericObjectLayout.__annotations__["qNxLibraryDimension"]
            ):
                self_.qNxLibraryDimension = kvargs["qNxLibraryDimension"]
            else:
                self_.qNxLibraryDimension = NxLibraryDimension(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qNxLibraryDimension"],
                )
        if "qNxLibraryMeasure" in kvargs and kvargs["qNxLibraryMeasure"] is not None:
            if (
                type(kvargs["qNxLibraryMeasure"]).__name__
                == GenericObjectLayout.__annotations__["qNxLibraryMeasure"]
            ):
                self_.qNxLibraryMeasure = kvargs["qNxLibraryMeasure"]
            else:
                self_.qNxLibraryMeasure = NxLibraryMeasure(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qNxLibraryMeasure"],
                )
        if "qSelectionObject" in kvargs and kvargs["qSelectionObject"] is not None:
            if (
                type(kvargs["qSelectionObject"]).__name__
                == GenericObjectLayout.__annotations__["qSelectionObject"]
            ):
                self_.qSelectionObject = kvargs["qSelectionObject"]
            else:
                self_.qSelectionObject = SelectionObject(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qSelectionObject"],
                )
        if "qStaticContentUrl" in kvargs and kvargs["qStaticContentUrl"] is not None:
            if (
                type(kvargs["qStaticContentUrl"]).__name__
                == GenericObjectLayout.__annotations__["qStaticContentUrl"]
            ):
                self_.qStaticContentUrl = kvargs["qStaticContentUrl"]
            else:
                self_.qStaticContentUrl = StaticContentUrl(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qStaticContentUrl"],
                )
        if "qTreeData" in kvargs and kvargs["qTreeData"] is not None:
            if (
                type(kvargs["qTreeData"]).__name__
                == GenericObjectLayout.__annotations__["qTreeData"]
            ):
                self_.qTreeData = kvargs["qTreeData"]
            else:
                self_.qTreeData = TreeData(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qTreeData"],
                )
        if "qUndoInfo" in kvargs and kvargs["qUndoInfo"] is not None:
            if (
                type(kvargs["qUndoInfo"]).__name__
                == GenericObjectLayout.__annotations__["qUndoInfo"]
            ):
                self_.qUndoInfo = kvargs["qUndoInfo"]
            else:
                self_.qUndoInfo = UndoInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qUndoInfo"],
                )
        if "qVariableList" in kvargs and kvargs["qVariableList"] is not None:
            if (
                type(kvargs["qVariableList"]).__name__
                == GenericObjectLayout.__annotations__["qVariableList"]
            ):
                self_.qVariableList = kvargs["qVariableList"]
            else:
                self_.qVariableList = VariableList(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qVariableList"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericObjectProperties:
    """

    Attributes
    ----------
    qExtendsId: str
      Should be set to create an object that is linked to another object. Enter the identifier of the linking object (i.e the object you want to link to).
      If you do not want to link your object, set this parameter to an empty string.
    qInfo: NxInfo
      Identifier and type of the object.
      This parameter is mandatory.
    qMetaDef: NxMetaDef
      Definition of the dynamic properties.
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    qAppObjectListDef: AppObjectListDef
      Defines the list of objects in an app.
      An app object is a generic object created at app level.
    qBookmarkListDef: BookmarkListDef
      Defines the list of bookmarks.
    qChildListDef: ChildListDef
      Defines the list of children of a generic object.
      What is defined in ChildListDef has an impact on what the GetLayout method returns. See Example for more information.
    qDimensionListDef: DimensionListDef
      Defines the lists of dimensions.
    qEmbeddedSnapshotDef: EmbeddedSnapshotDef
      Defines the embedded snapshot in a generic object.

       Properties:
      "EmbeddedSnapshotDef": {}
    qExtensionListDef: ExtensionListDef
      Obsolete, use qrs API's to fetch extensions.
    qFieldListDef: FieldListDef
      Defines the fields to show.
    qHyperCubeDef: HyperCubeDef
      Defines the properties of a hypercube.
      For more information about the definition of a hypercube, see Generic object.
    qLayoutExclude: LayoutExclude
      Contains JSON to be excluded from validation.
    qListObjectDef: ListObjectDef
      Defines the properties of a list object.
      For more information about the definition of a list object, see Generic object.
    qMeasureListDef: MeasureListDef
      Defines the list of measures.
    qMediaListDef: MediaListDef
      Defines the list of media files.
      This struct is deprecated.

       Properties:
      "qMediaListDef": {}
      qMediaListDef has an empty structure. No properties need to be set.
    qNxLibraryDimensionDef: NxLibraryDimensionDef
    qNxLibraryMeasureDef: NxLibraryMeasureDef
    qSelectionObjectDef: SelectionObjectDef
      To display the current selections.
      Can be added to any generic object but is particularly meaningful when using session objects to monitor an app.

       Properties:
      "qSelectionObjectDef": {}
    qStaticContentUrlDef: StaticContentUrlDef
      In addition, this structure can contain dynamic properties.
    qStringExpression: StringExpression
       Properties:
      Abbreviated syntax:
      "qStringExpression":"=<expression>"
      Extended object syntax:
      "qStringExpression":{"qExpr":"=<expression>"}
      Where:

      • < expression > is a string

      The "=" sign in the string expression is not mandatory. Even if the "=" sign is not given, the expression is evaluated. A string expression is not evaluated, if the expression is surrounded by simple quotes.
      The result of the evaluation of the expression can be of any type, as it is returned as a JSON (quoted) string.
    qTreeDataDef: TreeDataDef
      Defines the properties of a TreeData object.
      For more information about the definition of a TreeData object, see Generic object.
    qUndoInfoDef: UndoInfoDef
      Defines if an object should contain information on the number of possible undo and redo.

       Properties:
      "qUndoInfoDef": {}
      The numbers of undos and redos are empty when an object is created. The number of possible undos is increased every time an action (for example, create a child, set some properties) on the object is performed. The number of possible redos is increased every time an undo action is performed.
    qValueExpression: ValueExpression
       Properties:
      Abbreviated syntax:
      "qValueExpression":"=<expression>"
      Extended object syntax:
      "qValueExpression":{"qExpr":"=<expression>"}
      Where:

      • < expression > is a string.

      The "=" sign in the value expression is not mandatory. Even if the "=" sign is not given, the expression is evaluated.
      The expression is evaluated as a numeric.
    qVariableListDef: VariableListDef
      Defines the list of variables in an app.
    """

    qExtendsId: str = None
    qInfo: NxInfo = None
    qMetaDef: NxMetaDef = None
    qStateName: str = None
    qAppObjectListDef: AppObjectListDef = None
    qBookmarkListDef: BookmarkListDef = None
    qChildListDef: ChildListDef = None
    qDimensionListDef: DimensionListDef = None
    qEmbeddedSnapshotDef: EmbeddedSnapshotDef = None
    qExtensionListDef: ExtensionListDef = None
    qFieldListDef: FieldListDef = None
    qHyperCubeDef: HyperCubeDef = None
    qLayoutExclude: LayoutExclude = None
    qListObjectDef: ListObjectDef = None
    qMeasureListDef: MeasureListDef = None
    qMediaListDef: MediaListDef = None
    qNxLibraryDimensionDef: NxLibraryDimensionDef = None
    qNxLibraryMeasureDef: NxLibraryMeasureDef = None
    qSelectionObjectDef: SelectionObjectDef = None
    qStaticContentUrlDef: StaticContentUrlDef = None
    qStringExpression: StringExpression = None
    qTreeDataDef: TreeDataDef = None
    qUndoInfoDef: UndoInfoDef = None
    qValueExpression: ValueExpression = None
    qVariableListDef: VariableListDef = None

    def __init__(self_, **kvargs):
        if "qExtendsId" in kvargs and kvargs["qExtendsId"] is not None:
            self_.qExtendsId = kvargs["qExtendsId"]
        if "qInfo" in kvargs and kvargs["qInfo"] is not None:
            if (
                type(kvargs["qInfo"]).__name__
                == GenericObjectProperties.__annotations__["qInfo"]
            ):
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qInfo"],
                )
        if "qMetaDef" in kvargs and kvargs["qMetaDef"] is not None:
            if (
                type(kvargs["qMetaDef"]).__name__
                == GenericObjectProperties.__annotations__["qMetaDef"]
            ):
                self_.qMetaDef = kvargs["qMetaDef"]
            else:
                self_.qMetaDef = NxMetaDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMetaDef"],
                )
        if "qStateName" in kvargs and kvargs["qStateName"] is not None:
            self_.qStateName = kvargs["qStateName"]
        if "qAppObjectListDef" in kvargs and kvargs["qAppObjectListDef"] is not None:
            if (
                type(kvargs["qAppObjectListDef"]).__name__
                == GenericObjectProperties.__annotations__["qAppObjectListDef"]
            ):
                self_.qAppObjectListDef = kvargs["qAppObjectListDef"]
            else:
                self_.qAppObjectListDef = AppObjectListDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qAppObjectListDef"],
                )
        if "qBookmarkListDef" in kvargs and kvargs["qBookmarkListDef"] is not None:
            if (
                type(kvargs["qBookmarkListDef"]).__name__
                == GenericObjectProperties.__annotations__["qBookmarkListDef"]
            ):
                self_.qBookmarkListDef = kvargs["qBookmarkListDef"]
            else:
                self_.qBookmarkListDef = BookmarkListDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qBookmarkListDef"],
                )
        if "qChildListDef" in kvargs and kvargs["qChildListDef"] is not None:
            if (
                type(kvargs["qChildListDef"]).__name__
                == GenericObjectProperties.__annotations__["qChildListDef"]
            ):
                self_.qChildListDef = kvargs["qChildListDef"]
            else:
                self_.qChildListDef = ChildListDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qChildListDef"],
                )
        if "qDimensionListDef" in kvargs and kvargs["qDimensionListDef"] is not None:
            if (
                type(kvargs["qDimensionListDef"]).__name__
                == GenericObjectProperties.__annotations__["qDimensionListDef"]
            ):
                self_.qDimensionListDef = kvargs["qDimensionListDef"]
            else:
                self_.qDimensionListDef = DimensionListDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qDimensionListDef"],
                )
        if (
            "qEmbeddedSnapshotDef" in kvargs
            and kvargs["qEmbeddedSnapshotDef"] is not None
        ):
            if (
                type(kvargs["qEmbeddedSnapshotDef"]).__name__
                == GenericObjectProperties.__annotations__["qEmbeddedSnapshotDef"]
            ):
                self_.qEmbeddedSnapshotDef = kvargs["qEmbeddedSnapshotDef"]
            else:
                self_.qEmbeddedSnapshotDef = EmbeddedSnapshotDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qEmbeddedSnapshotDef"],
                )
        if "qExtensionListDef" in kvargs and kvargs["qExtensionListDef"] is not None:
            if (
                type(kvargs["qExtensionListDef"]).__name__
                == GenericObjectProperties.__annotations__["qExtensionListDef"]
            ):
                self_.qExtensionListDef = kvargs["qExtensionListDef"]
            else:
                self_.qExtensionListDef = ExtensionListDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qExtensionListDef"],
                )
        if "qFieldListDef" in kvargs and kvargs["qFieldListDef"] is not None:
            if (
                type(kvargs["qFieldListDef"]).__name__
                == GenericObjectProperties.__annotations__["qFieldListDef"]
            ):
                self_.qFieldListDef = kvargs["qFieldListDef"]
            else:
                self_.qFieldListDef = FieldListDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qFieldListDef"],
                )
        if "qHyperCubeDef" in kvargs and kvargs["qHyperCubeDef"] is not None:
            if (
                type(kvargs["qHyperCubeDef"]).__name__
                == GenericObjectProperties.__annotations__["qHyperCubeDef"]
            ):
                self_.qHyperCubeDef = kvargs["qHyperCubeDef"]
            else:
                self_.qHyperCubeDef = HyperCubeDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qHyperCubeDef"],
                )
        if "qLayoutExclude" in kvargs and kvargs["qLayoutExclude"] is not None:
            if (
                type(kvargs["qLayoutExclude"]).__name__
                == GenericObjectProperties.__annotations__["qLayoutExclude"]
            ):
                self_.qLayoutExclude = kvargs["qLayoutExclude"]
            else:
                self_.qLayoutExclude = LayoutExclude(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qLayoutExclude"],
                )
        if "qListObjectDef" in kvargs and kvargs["qListObjectDef"] is not None:
            if (
                type(kvargs["qListObjectDef"]).__name__
                == GenericObjectProperties.__annotations__["qListObjectDef"]
            ):
                self_.qListObjectDef = kvargs["qListObjectDef"]
            else:
                self_.qListObjectDef = ListObjectDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qListObjectDef"],
                )
        if "qMeasureListDef" in kvargs and kvargs["qMeasureListDef"] is not None:
            if (
                type(kvargs["qMeasureListDef"]).__name__
                == GenericObjectProperties.__annotations__["qMeasureListDef"]
            ):
                self_.qMeasureListDef = kvargs["qMeasureListDef"]
            else:
                self_.qMeasureListDef = MeasureListDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeasureListDef"],
                )
        if "qMediaListDef" in kvargs and kvargs["qMediaListDef"] is not None:
            if (
                type(kvargs["qMediaListDef"]).__name__
                == GenericObjectProperties.__annotations__["qMediaListDef"]
            ):
                self_.qMediaListDef = kvargs["qMediaListDef"]
            else:
                self_.qMediaListDef = MediaListDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMediaListDef"],
                )
        if (
            "qNxLibraryDimensionDef" in kvargs
            and kvargs["qNxLibraryDimensionDef"] is not None
        ):
            if (
                type(kvargs["qNxLibraryDimensionDef"]).__name__
                == GenericObjectProperties.__annotations__["qNxLibraryDimensionDef"]
            ):
                self_.qNxLibraryDimensionDef = kvargs["qNxLibraryDimensionDef"]
            else:
                self_.qNxLibraryDimensionDef = NxLibraryDimensionDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qNxLibraryDimensionDef"],
                )
        if (
            "qNxLibraryMeasureDef" in kvargs
            and kvargs["qNxLibraryMeasureDef"] is not None
        ):
            if (
                type(kvargs["qNxLibraryMeasureDef"]).__name__
                == GenericObjectProperties.__annotations__["qNxLibraryMeasureDef"]
            ):
                self_.qNxLibraryMeasureDef = kvargs["qNxLibraryMeasureDef"]
            else:
                self_.qNxLibraryMeasureDef = NxLibraryMeasureDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qNxLibraryMeasureDef"],
                )
        if (
            "qSelectionObjectDef" in kvargs
            and kvargs["qSelectionObjectDef"] is not None
        ):
            if (
                type(kvargs["qSelectionObjectDef"]).__name__
                == GenericObjectProperties.__annotations__["qSelectionObjectDef"]
            ):
                self_.qSelectionObjectDef = kvargs["qSelectionObjectDef"]
            else:
                self_.qSelectionObjectDef = SelectionObjectDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qSelectionObjectDef"],
                )
        if (
            "qStaticContentUrlDef" in kvargs
            and kvargs["qStaticContentUrlDef"] is not None
        ):
            if (
                type(kvargs["qStaticContentUrlDef"]).__name__
                == GenericObjectProperties.__annotations__["qStaticContentUrlDef"]
            ):
                self_.qStaticContentUrlDef = kvargs["qStaticContentUrlDef"]
            else:
                self_.qStaticContentUrlDef = StaticContentUrlDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qStaticContentUrlDef"],
                )
        if "qStringExpression" in kvargs and kvargs["qStringExpression"] is not None:
            if (
                type(kvargs["qStringExpression"]).__name__
                == GenericObjectProperties.__annotations__["qStringExpression"]
            ):
                self_.qStringExpression = kvargs["qStringExpression"]
            else:
                self_.qStringExpression = StringExpression(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qStringExpression"],
                )
        if "qTreeDataDef" in kvargs and kvargs["qTreeDataDef"] is not None:
            if (
                type(kvargs["qTreeDataDef"]).__name__
                == GenericObjectProperties.__annotations__["qTreeDataDef"]
            ):
                self_.qTreeDataDef = kvargs["qTreeDataDef"]
            else:
                self_.qTreeDataDef = TreeDataDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qTreeDataDef"],
                )
        if "qUndoInfoDef" in kvargs and kvargs["qUndoInfoDef"] is not None:
            if (
                type(kvargs["qUndoInfoDef"]).__name__
                == GenericObjectProperties.__annotations__["qUndoInfoDef"]
            ):
                self_.qUndoInfoDef = kvargs["qUndoInfoDef"]
            else:
                self_.qUndoInfoDef = UndoInfoDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qUndoInfoDef"],
                )
        if "qValueExpression" in kvargs and kvargs["qValueExpression"] is not None:
            if (
                type(kvargs["qValueExpression"]).__name__
                == GenericObjectProperties.__annotations__["qValueExpression"]
            ):
                self_.qValueExpression = kvargs["qValueExpression"]
            else:
                self_.qValueExpression = ValueExpression(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qValueExpression"],
                )
        if "qVariableListDef" in kvargs and kvargs["qVariableListDef"] is not None:
            if (
                type(kvargs["qVariableListDef"]).__name__
                == GenericObjectProperties.__annotations__["qVariableListDef"]
            ):
                self_.qVariableListDef = kvargs["qVariableListDef"]
            else:
                self_.qVariableListDef = VariableListDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qVariableListDef"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericVariable:
    """

    Attributes
    ----------
    qGenericId: str
      Object ID.
    qGenericType: str
      The type of the object.
    qHandle: int
      The handle used to connect to object.
    qType: str
      The native type of the object.
    """

    _session: RpcSession = None
    qGenericId: str = None
    qGenericType: str = None
    qHandle: int = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qGenericId" in kvargs and kvargs["qGenericId"] is not None:
            self_.qGenericId = kvargs["qGenericId"]
        if "qGenericType" in kvargs and kvargs["qGenericType"] is not None:
            self_.qGenericType = kvargs["qGenericType"]
        if "qHandle" in kvargs and kvargs["qHandle"] is not None:
            self_.qHandle = kvargs["qHandle"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}) or k == "_session":
                self_.__setattr__(k, v)

    def get_layout(self) -> GenericVariableLayout:
        """
        Evaluates an object and displays its properties including the dynamic properties.
        If the member delta is set to true in the request object, only the delta is evaluated.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLayout", handle)["qLayout"]
        obj = GenericVariableLayout(**response)
        return obj

    def apply_patches(self, qPatches: list[NxPatch]) -> object:
        """
        Applies a patch to the properties of a variable. Allows an update to some of the properties. It should not be possible to patch "/qInfo/qId",
        and it will be forbidden in the near future.
        Applying a patch takes less time than resetting all the properties.

        Parameters
        ----------
        qPatches: list[NxPatch]
          Array of patches.
        """
        params = {}
        params["qPatches"] = qPatches
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ApplyPatches", handle, **params)
        return response

    def set_properties(self, qProp: GenericVariableProperties) -> object:
        """
        Sets some properties for a variable.
        The identifier of a variable cannot be modified. You cannot update the properties of a script-defined variable using the SetProperties method.

        Parameters
        ----------
        qProp: GenericVariableProperties
          Information about the variable.
        """
        params = {}
        params["qProp"] = qProp
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetProperties", handle, **params)
        return response

    def get_properties(self) -> GenericVariableProperties:
        """
        Shows the properties of an object.
        If the member delta is set to true in the request, only the delta is retrieved.
        The following is always returned in the output:

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetProperties", handle)["qProp"]
        obj = GenericVariableProperties(**response)
        return obj

    def get_info(self) -> NxInfo:
        """
        Returns the type and identifier of the object.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetInfo", handle)["qInfo"]
        obj = NxInfo(**response)
        return obj

    def set_string_value(self, qVal: str) -> object:
        """
        Sets a string value to a variable.
        These changes are not persistent. They only last the duration of the engine session.

        Parameters
        ----------
        qVal: str
          Value of the variable. The string can contain an expression.
        """
        params = {}
        params["qVal"] = qVal
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetStringValue", handle, **params)
        return response

    def set_num_value(self, qVal: float) -> object:
        """
        Sets a numerical value to a variable.
        These changes are not persistent. They only last the duration of the engine session.

        Parameters
        ----------
        qVal: float
          Value of the variable.
        """
        params = {}
        params["qVal"] = qVal
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetNumValue", handle, **params)
        return response

    def set_dual_value(self, qText: str, qNum: float) -> object:
        """
        Sets the value of a dual variable.
        These changes are not persistent. They only last the duration of the engine session.

        Parameters
        ----------
        qText: str
          String representation of a dual value. Set this parameter to "", if the string representation is to be Null.
        qNum: float
          Numeric representation of a dual value.
        """
        params = {}
        params["qText"] = qText
        params["qNum"] = qNum
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetDualValue", handle, **params)
        return response

    def get_raw_content(self) -> str:
        """
        Returns the raw value of a variable.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetRawContent", handle)["qReturn"]
        return response

    def on(self, event_name, listener):
        self._session.on_handle(self.qHandle, event_name, listener)


@dataclass
class GenericVariableLayout:
    """
    Is the layout for GenericVariableProperties.

    Attributes
    ----------
    qInfo: NxInfo
      Identifier and type of the object.
      This parameter is mandatory.
    qIsScriptCreated: bool
      If set to true, it means that the variable was defined via script.
    qMeta: NxMeta
      Information about publishing and permissions.
      This parameter is optional.
    qNum: float
      A value.
    qText: str
      Some text.
    """

    qInfo: NxInfo = None
    qIsScriptCreated: bool = None
    qMeta: NxMeta = None
    qNum: float = None
    qText: str = None

    def __init__(self_, **kvargs):
        if "qInfo" in kvargs and kvargs["qInfo"] is not None:
            if (
                type(kvargs["qInfo"]).__name__
                == GenericVariableLayout.__annotations__["qInfo"]
            ):
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qInfo"],
                )
        if "qIsScriptCreated" in kvargs and kvargs["qIsScriptCreated"] is not None:
            self_.qIsScriptCreated = kvargs["qIsScriptCreated"]
        if "qMeta" in kvargs and kvargs["qMeta"] is not None:
            if (
                type(kvargs["qMeta"]).__name__
                == GenericVariableLayout.__annotations__["qMeta"]
            ):
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeta"],
                )
        if "qNum" in kvargs and kvargs["qNum"] is not None:
            self_.qNum = kvargs["qNum"]
        if "qText" in kvargs and kvargs["qText"] is not None:
            self_.qText = kvargs["qText"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GenericVariableProperties:
    """

    Attributes
    ----------
    qComment: str
      Comment related to the variable.
      This parameter is optional.
    qDefinition: str
      Definition of the variable.
    qIncludeInBookmark: bool
      Set this property to true to update the variable when applying a bookmark. The variable value will be persisted in the bookmark.
      The value of a variable can affect the state of the selections.
      Script variables cannot be persisted in the bookmark.
      The default value is false.
    qInfo: NxInfo
      Identifier and type of the object.
      This parameter is mandatory.
    qMetaDef: NxMetaDef
      Meta data.
    qName: str
      Name of the variable.
      The name must be unique.
      This parameter is mandatory.
    qNumberPresentation: FieldAttributes
      Defines the format of the value.
      This parameter is optional.
    """

    qComment: str = None
    qDefinition: str = None
    qIncludeInBookmark: bool = None
    qInfo: NxInfo = None
    qMetaDef: NxMetaDef = None
    qName: str = None
    qNumberPresentation: FieldAttributes = None

    def __init__(self_, **kvargs):
        if "qComment" in kvargs and kvargs["qComment"] is not None:
            self_.qComment = kvargs["qComment"]
        if "qDefinition" in kvargs and kvargs["qDefinition"] is not None:
            self_.qDefinition = kvargs["qDefinition"]
        if "qIncludeInBookmark" in kvargs and kvargs["qIncludeInBookmark"] is not None:
            self_.qIncludeInBookmark = kvargs["qIncludeInBookmark"]
        if "qInfo" in kvargs and kvargs["qInfo"] is not None:
            if (
                type(kvargs["qInfo"]).__name__
                == GenericVariableProperties.__annotations__["qInfo"]
            ):
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qInfo"],
                )
        if "qMetaDef" in kvargs and kvargs["qMetaDef"] is not None:
            if (
                type(kvargs["qMetaDef"]).__name__
                == GenericVariableProperties.__annotations__["qMetaDef"]
            ):
                self_.qMetaDef = kvargs["qMetaDef"]
            else:
                self_.qMetaDef = NxMetaDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMetaDef"],
                )
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if (
            "qNumberPresentation" in kvargs
            and kvargs["qNumberPresentation"] is not None
        ):
            if (
                type(kvargs["qNumberPresentation"]).__name__
                == GenericVariableProperties.__annotations__["qNumberPresentation"]
            ):
                self_.qNumberPresentation = kvargs["qNumberPresentation"]
            else:
                self_.qNumberPresentation = FieldAttributes(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qNumberPresentation"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetBaseBNFReturn:
    """

    Attributes
    ----------
    qBnfDefs: list[BNFDef]
    qBnfHash: str
    """

    qBnfDefs: list[BNFDef] = None
    qBnfHash: str = None

    def __init__(self_, **kvargs):
        if "qBnfDefs" in kvargs and kvargs["qBnfDefs"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == GetBaseBNFReturn.__annotations__["qBnfDefs"]
                for e in kvargs["qBnfDefs"]
            ):
                self_.qBnfDefs = kvargs["qBnfDefs"]
            else:
                self_.qBnfDefs = [
                    BNFDef(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qBnfDefs"]
                ]
        if "qBnfHash" in kvargs and kvargs["qBnfHash"] is not None:
            self_.qBnfHash = kvargs["qBnfHash"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetBaseBNFStringReturn:
    """

    Attributes
    ----------
    qBnfHash: str
    qBnfStr: str
    """

    qBnfHash: str = None
    qBnfStr: str = None

    def __init__(self_, **kvargs):
        if "qBnfHash" in kvargs and kvargs["qBnfHash"] is not None:
            self_.qBnfHash = kvargs["qBnfHash"]
        if "qBnfStr" in kvargs and kvargs["qBnfStr"] is not None:
            self_.qBnfStr = kvargs["qBnfStr"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetDatabaseTablePreviewReturn:
    """

    Attributes
    ----------
    qPreview: list[DataRecord]
    qRowCount: int
    """

    qPreview: list[DataRecord] = None
    qRowCount: int = None

    def __init__(self_, **kvargs):
        if "qPreview" in kvargs and kvargs["qPreview"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == GetDatabaseTablePreviewReturn.__annotations__["qPreview"]
                for e in kvargs["qPreview"]
            ):
                self_.qPreview = kvargs["qPreview"]
            else:
                self_.qPreview = [
                    DataRecord(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qPreview"]
                ]
        if "qRowCount" in kvargs and kvargs["qRowCount"] is not None:
            self_.qRowCount = kvargs["qRowCount"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetExpressionBNFReturn:
    """

    Attributes
    ----------
    qBnfDefs: list[BNFDef]
    qBnfHash: str
    """

    qBnfDefs: list[BNFDef] = None
    qBnfHash: str = None

    def __init__(self_, **kvargs):
        if "qBnfDefs" in kvargs and kvargs["qBnfDefs"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == GetExpressionBNFReturn.__annotations__["qBnfDefs"]
                for e in kvargs["qBnfDefs"]
            ):
                self_.qBnfDefs = kvargs["qBnfDefs"]
            else:
                self_.qBnfDefs = [
                    BNFDef(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qBnfDefs"]
                ]
        if "qBnfHash" in kvargs and kvargs["qBnfHash"] is not None:
            self_.qBnfHash = kvargs["qBnfHash"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetFileTableFieldsReturn:
    """

    Attributes
    ----------
    qFields: list[DataField]
    qFormatSpec: str
    """

    qFields: list[DataField] = None
    qFormatSpec: str = None

    def __init__(self_, **kvargs):
        if "qFields" in kvargs and kvargs["qFields"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == GetFileTableFieldsReturn.__annotations__["qFields"]
                for e in kvargs["qFields"]
            ):
                self_.qFields = kvargs["qFields"]
            else:
                self_.qFields = [
                    DataField(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qFields"]
                ]
        if "qFormatSpec" in kvargs and kvargs["qFormatSpec"] is not None:
            self_.qFormatSpec = kvargs["qFormatSpec"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetFileTablePreviewReturn:
    """

    Attributes
    ----------
    qFormatSpec: str
    qPreview: list[DataRecord]
    """

    qFormatSpec: str = None
    qPreview: list[DataRecord] = None

    def __init__(self_, **kvargs):
        if "qFormatSpec" in kvargs and kvargs["qFormatSpec"] is not None:
            self_.qFormatSpec = kvargs["qFormatSpec"]
        if "qPreview" in kvargs and kvargs["qPreview"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == GetFileTablePreviewReturn.__annotations__["qPreview"]
                for e in kvargs["qPreview"]
            ):
                self_.qPreview = kvargs["qPreview"]
            else:
                self_.qPreview = [
                    DataRecord(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qPreview"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetHyperCubeContinuousDataReturn:
    """

    Attributes
    ----------
    qAxisData: NxAxisData
    qDataPages: list[NxDataPage]
    """

    qAxisData: NxAxisData = None
    qDataPages: list[NxDataPage] = None

    def __init__(self_, **kvargs):
        if "qAxisData" in kvargs and kvargs["qAxisData"] is not None:
            if (
                type(kvargs["qAxisData"]).__name__
                == GetHyperCubeContinuousDataReturn.__annotations__["qAxisData"]
            ):
                self_.qAxisData = kvargs["qAxisData"]
            else:
                self_.qAxisData = NxAxisData(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qAxisData"],
                )
        if "qDataPages" in kvargs and kvargs["qDataPages"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == GetHyperCubeContinuousDataReturn.__annotations__["qDataPages"]
                for e in kvargs["qDataPages"]
            ):
                self_.qDataPages = kvargs["qDataPages"]
            else:
                self_.qDataPages = [
                    NxDataPage(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qDataPages"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetInteractReturn:
    """

    Attributes
    ----------
    qDef: InteractDef
    qReturn: bool
    """

    qDef: InteractDef = None
    qReturn: bool = None

    def __init__(self_, **kvargs):
        if "qDef" in kvargs and kvargs["qDef"] is not None:
            if (
                type(kvargs["qDef"]).__name__
                == GetInteractReturn.__annotations__["qDef"]
            ):
                self_.qDef = kvargs["qDef"]
            else:
                self_.qDef = InteractDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qDef"],
                )
        if "qReturn" in kvargs and kvargs["qReturn"] is not None:
            self_.qReturn = kvargs["qReturn"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetMediaListReturn:
    """

    Attributes
    ----------
    qList: MediaList
      Lists the media files. Is the layout for MediaListDef.
      This struct is deprecated.
    qReturn: bool
    """

    qList: MediaList = None
    qReturn: bool = None

    def __init__(self_, **kvargs):
        if "qList" in kvargs and kvargs["qList"] is not None:
            if (
                type(kvargs["qList"]).__name__
                == GetMediaListReturn.__annotations__["qList"]
            ):
                self_.qList = kvargs["qList"]
            else:
                self_.qList = MediaList(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qList"],
                )
        if "qReturn" in kvargs and kvargs["qReturn"] is not None:
            self_.qReturn = kvargs["qReturn"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetTablesAndKeysReturn:
    """

    Attributes
    ----------
    qk: list[SourceKeyRecord]
    qtr: list[TableRecord]
    """

    qk: list[SourceKeyRecord] = None
    qtr: list[TableRecord] = None

    def __init__(self_, **kvargs):
        if "qk" in kvargs and kvargs["qk"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == GetTablesAndKeysReturn.__annotations__["qk"]
                for e in kvargs["qk"]
            ):
                self_.qk = kvargs["qk"]
            else:
                self_.qk = [
                    SourceKeyRecord(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qk"]
                ]
        if "qtr" in kvargs and kvargs["qtr"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == GetTablesAndKeysReturn.__annotations__["qtr"]
                for e in kvargs["qtr"]
            ):
                self_.qtr = kvargs["qtr"]
            else:
                self_.qtr = [
                    TableRecord(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qtr"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Global:
    """

    Attributes
    ----------
    qGenericId: str
      Object ID.
    qGenericType: str
      The type of the object.
    qHandle: int
      The handle used to connect to object.
    qType: str
      The native type of the object.
    """

    _session: RpcSession = None
    qGenericId: str = None
    qGenericType: str = None
    qHandle: int = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qGenericId" in kvargs and kvargs["qGenericId"] is not None:
            self_.qGenericId = kvargs["qGenericId"]
        if "qGenericType" in kvargs and kvargs["qGenericType"] is not None:
            self_.qGenericType = kvargs["qGenericType"]
        if "qHandle" in kvargs and kvargs["qHandle"] is not None:
            self_.qHandle = kvargs["qHandle"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}) or k == "_session":
                self_.__setattr__(k, v)

    def abort_request(self, qRequestId: int) -> object:
        """
        Sets an abort flag on a specific request in the current engine session.

        • If an abort flag is set on a pending request, the request is aborted.

        • If an abort flag is set on an ongoing request, the engine checks to see if it is possible to abort the request.

        Parameters
        ----------
        qRequestId: int
          Identifier of request to abort.
        """
        params = {}
        params["qRequestId"] = qRequestId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AbortRequest", handle, **params)
        return response

    def abort_all(self) -> object:
        """
        Sets an abort flag on all pending and ongoing requests in the current engine session.

        • If an abort flag is set on a pending request, the request is aborted.

        • If an abort flag is set on an ongoing request, the engine checks to see if it is possible to abort the request.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AbortAll", handle)
        return response

    def get_progress(self, qRequestId: int) -> ProgressData:
        """
        Gives information about the progress of the DoReload and DoSave calls.
        For more information on DoReload and DoSave, see the DoReload Method and DoSave Method.

        Parameters
        ----------
        qRequestId: int
          Identifier of the DoReload or DoSave request or 0.
          Complete information is returned if the identifier of the request is given.
          If the identifier is 0, less information is given. Progress messages and error messages are returned but information like when the request started and finished is not returned.
        """
        params = {}
        params["qRequestId"] = qRequestId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetProgress", handle, **params)["qProgressData"]
        obj = ProgressData(**response)
        return obj

    def get_interact(self, qRequestId: int) -> GetInteractReturn:
        """
        Retrieves information on the user interaction that is requested by the engine.
        Engine can request user interactions only during script reload and when the reload is performed in debug mode ( qDebug is set to true when using the DoReload method ).
        When running reload in debug mode, the engine pauses the script execution to receive data about user interaction. The engine can pause:

        • Before executing a new script statement.

        • When an error occurs while executing the script.

        • When the script execution is finished.

        To know if the engine is paused and waits for a response to an interaction request, the GetProgress method should be used. The engine waits for a response if the property qUserInteractionWanted is set to true in the response of the GetProgress request.

        Parameters
        ----------
        qRequestId: int
          Identifier of the request.
          Corresponds to the identifier of the DoReload request.
        """
        params = {}
        params["qRequestId"] = qRequestId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetInteract", handle, **params)
        obj = GetInteractReturn(**response)
        return obj

    def interact_done(self, qRequestId: int, qDef: InteractDef) -> object:
        """
        Informs the engine that a user interaction (which was earlier requested by the engine) was performed and indicates to the engine what to do next.

        Parameters
        ----------
        qRequestId: int
          Identifier of the request.
          Corresponds to the identifier of the DoReload request.
        qDef: InteractDef
          User response to the current interaction.
        """
        params = {}
        params["qRequestId"] = qRequestId
        params["qDef"] = qDef
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("InteractDone", handle, **params)
        return response

    def get_authenticated_user(self) -> str:
        """
        Retrieves information about the authenticated user.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetAuthenticatedUser", handle)["qReturn"]
        return response

    def get_active_doc(self) -> Doc:
        """
        Returns the handle of the current app.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetActiveDoc", handle)["qReturn"]
        obj = Doc(_session=self._session, **response)
        return obj

    def allow_create_app(self) -> bool:
        """
        Indicates whether or not a user is able to create an app.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("AllowCreateApp", handle)["qReturn"]
        return response

    def is_desktop_mode(self) -> bool:
        """
        Indicates whether the user is working in Qlik Sense Desktop.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("IsDesktopMode", handle)["qReturn"]
        return response

    def cancel_request(self, qRequestId: int) -> object:
        """
        Cancels an ongoing request. The request is stopped.

        Parameters
        ----------
        qRequestId: int
          Identifier of the request to stop.
        """
        params = {}
        params["qRequestId"] = qRequestId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CancelRequest", handle, **params)
        return response

    def shutdown_process(self) -> object:
        """
        Shuts down the Qlik engine.
        This operation is possible only in Qlik Sense Desktop.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ShutdownProcess", handle)
        return response

    def replace_app_from_id(
        self, qTargetAppId: str, qSrcAppID: str, qIds: list[str]
    ) -> bool:
        """
        Replaces objects of a target app with the objects from a source app.
        The list of objects in the app to be replaced must be defined in qIds.
        The data model of the app cannot be updated.  This operation is possible only in Qlik Sense Enterprise.

        The operation is successful if qSuccess is set to true.

        Parameters
        ----------
        qTargetAppId: str
          Identifier (GUID) of the target app.
          The target app is the app to be replaced.
        qSrcAppID: str
          Identifier (GUID) of the source app.
          The objects in the source app will replace the objects in the target app.
        qIds: list[str]
          QRS identifiers (GUID) of the objects in the target app to be replaced. Only QRS-approved GUIDs are applicable.
          An object that is QRS-approved, is for example an object that has been published (for example, not private anymore).
          If an object is private, it should not be included in this list.
          If the array of identifiers contains objects that are not present in the source app, the objects related to these identifiers are removed from the target app.
          If qIds is empty, no objects are deleted in the target app.
        """
        params = {}
        params["qTargetAppId"] = qTargetAppId
        params["qSrcAppID"] = qSrcAppID
        params["qIds"] = qIds
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ReplaceAppFromID", handle, **params)["qSuccess"]
        return response

    def publish_app(self, qAppId: str, qName: str, qStreamId: str) -> object:
        """
        Publishes an app to the supplied stream.

        Parameters
        ----------
        qAppId: str
          The Id of the app to publish.
        qName: str
          The name of the app to publish.
        qStreamId: str
          The stream Id of the app to publish.
        """
        params = {}
        params["qAppId"] = qAppId
        params["qName"] = qName
        params["qStreamId"] = qStreamId
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("PublishApp", handle, **params)
        return response

    def is_personal_mode(self) -> bool:
        """
        Indicates whether or not the user is working in personal mode (Qlik Sense Desktop).

        Parameters
        ----------
        """
        warnings.warn("IsPersonalMode is deprecated", DeprecationWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("IsPersonalMode", handle)["qReturn"]
        return response

    def get_unique_id(self) -> str:
        """
        Returns the unique identifier of the endpoint for the current user in the current app.
        This unique identifier can be used for logging purposes.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetUniqueID", handle)["qUniqueID"]
        return response

    def open_doc(
        self,
        qDocName: str,
        qUserName: str = None,
        qPassword: str = None,
        qSerial: str = None,
        qNoData: bool = None,
    ) -> Doc:
        """
        Opens an app and checks if the app needs to be migrated (if the app is deprecated).
        The OpenDoc method compares the version of the app with the version of Qlik Sense and migrates the app to the current version of Qlik Sense if necessary. Once the migration is done, the app is opened.
        If no migration is needed, the app is opened immediately.
        The following applies:

        • The app version is lower than 0.95: no migration is done. Apps older than the version 0.95 are not supported.

        • The app version is at least 0.95 and less than the Qlik Sense version: the app is migrated and then opened.

        • Qlik Sense and the app have the same version: the app is opened, no migration is needed.

        If the app is read-only, the app migration cannot occur. An error message is sent.

         Backups:
        In Qlik Sense Desktop, apps are automatically backed up before a migration.
        The backup files are located in %userprofile%\Documents\Qlik\Sense\AppsBackup\<Qlik Sense Desktop version>.
        In Qlik Sense Enterprise, no automatic back up is run. The back up should be done manually.

        Parameters
        ----------
        qDocName: str
          The GUID (in Qlik Sense Enterprise) or Name (in Qlik Sense Desktop) of the app to retrieve.
        qUserName: str = None
          Name of the user that opens the app.
        qPassword: str = None
          Password of the user.
        qSerial: str = None
          Current Qlik Sense serial number.
        qNoData: bool = None
          Set this parameter to true to be able to open an app without loading its data.
          When this parameter is set to true, the objects in the app are present but contain no data. The script can be edited and reloaded.
          The default value is false.
        """
        params = {}
        params["qDocName"] = qDocName
        if qUserName is not None:
            params["qUserName"] = qUserName
        if qPassword is not None:
            params["qPassword"] = qPassword
        if qSerial is not None:
            params["qSerial"] = qSerial
        if qNoData is not None:
            params["qNoData"] = qNoData
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("OpenDoc", handle, **params)["qReturn"]
        obj = Doc(_session=self._session, **response)
        return obj

    def product_version(self) -> str:
        """
        Returns the Qlik Sense version number.

        Parameters
        ----------
        """
        warnings.warn("ProductVersion is deprecated", DeprecationWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ProductVersion", handle)["qReturn"]
        return response

    def get_app_entry(self, qAppID: str) -> AppEntry:
        """
        Retrieves the meta data of an app.

        Parameters
        ----------
        qAppID: str
          Identifier of the app, as returned by the CreateApp method.
          One of:

          • Path and name of the app (Qlik Sense Desktop)

          • GUID (Qlik Sense Enterprise)
        """
        params = {}
        params["qAppID"] = qAppID
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetAppEntry", handle, **params)["qEntry"]
        obj = AppEntry(**response)
        return obj

    def configure_reload(
        self, qCancelOnScriptError: bool, qUseErrorData: bool, qInteractOnError: bool
    ) -> object:
        """
        Configures the engine's behavior during a reload.
        The ConfigureReload method should be run before the DoReload method.

        Parameters
        ----------
        qCancelOnScriptError: bool
          If set to true, the script execution is halted on error.
          Otherwise, the engine continues the script execution.
          This parameter is relevant only if the variable ErrorMode is set to 1.
        qUseErrorData: bool
          If set to true, any script execution error is returned in qErrorData by the GetProgress method.
        qInteractOnError: bool
          If set to true, the script execution is halted on error and the engine is waiting for an interaction to be performed. If the result from the interaction is 1 (qDef.qResult is 1), the engine continues the script execution otherwise the execution is halted.
          This parameter is relevant only if the variable ErrorMode is set to 1 and the script is run in debug mode (qDebug is set to true when calling the DoReload method).
        """
        params = {}
        params["qCancelOnScriptError"] = qCancelOnScriptError
        params["qUseErrorData"] = qUseErrorData
        params["qInteractOnError"] = qInteractOnError
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ConfigureReload", handle, **params)
        return response

    def cancel_reload(self, qReason: str = None) -> object:
        """
        Cancels an ongoing reload. The reload of the app is stopped. The indexation can be canceled and true is still the return value of the reload task.

        Parameters
        ----------
        qReason: str = None
          Reason for why the reload was cancelled. This will be echoed back to the user in the script log.
        """
        params = {}
        if qReason is not None:
            params["qReason"] = qReason
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("CancelReload", handle, **params)
        return response

    def get_bnf(self, qBnfType: str) -> list[BNFDef]:
        """
        Gets the current Backus-Naur Form (BNF) grammar of the Qlik engine scripting language. The BNF rules define the syntax for the script statements and the script or chart functions.
        In the Qlik engine BNF grammar, a token is a string of one or more characters that is significant as a group. For example, a token could be a function name, a number, a letter, a parenthesis, and so on.

        Parameters
        ----------
        qBnfType: str
          Returns a set of rules defining the syntax for:

          • The script statements and the script functions if qBnfType is set to S.

          • The chart functions if qBnfType is set to E.

          One of:

          • S or SCRIPT_TEXT_SCRIPT

          • E or SCRIPT_TEXT_EXPRESSION
        """
        warnings.warn("GetBNF is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qBnfType"] = qBnfType
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetBNF", handle, **params)["qBnfDefs"]
        return [BNFDef(**e) for e in response]

    def get_functions(self, qGroup: str = None) -> list[Function]:
        """
        Gets the list of all the script functions.

        Parameters
        ----------
        qGroup: str = None
          Name of the group.
          Default is all groups.

          One of:

          • ALL or FUNC_GROUP_ALL

          • U or FUNC_GROUP_UNKNOWN

          • NONE or FUNC_GROUP_NONE

          • AGGR or FUNC_GROUP_AGGR

          • NUM or FUNC_GROUP_NUMERIC

          • RNG or FUNC_GROUP_RANGE

          • EXP or FUNC_GROUP_EXPONENTIAL_AND_LOGARITHMIC

          • TRIG or FUNC_GROUP_TRIGONOMETRIC_AND_HYPERBOLIC

          • FIN or FUNC_GROUP_FINANCIAL

          • MATH or FUNC_GROUP_MATH_CONSTANT_AND_PARAM_FREE

          • COUNT or FUNC_GROUP_COUNTER

          • STR or FUNC_GROUP_STRING

          • MAPP or FUNC_GROUP_MAPPING

          • RCRD or FUNC_GROUP_INTER_RECORD

          • CND or FUNC_GROUP_CONDITIONAL

          • LOG or FUNC_GROUP_LOGICAL

          • NULL or FUNC_GROUP_NULL

          • SYS or FUNC_GROUP_SYSTEM

          • FILE or FUNC_GROUP_FILE

          • TBL or FUNC_GROUP_TABLE

          • DATE or FUNC_GROUP_DATE_AND_TIME

          • NUMI or FUNC_GROUP_NUMBER_INTERPRET

          • FRMT or FUNC_GROUP_FORMATTING

          • CLR or FUNC_GROUP_COLOR

          • RNK or FUNC_GROUP_RANKING

          • GEO or FUNC_GROUP_GEO

          • EXT or FUNC_GROUP_EXTERNAL

          • PROB or FUNC_GROUP_PROBABILITY

          • ARRAY or FUNC_GROUP_ARRAY

          • LEG or FUNC_GROUP_LEGACY

          • DB or FUNC_GROUP_DB_NATIVE
        """
        params = {}
        if qGroup is not None:
            params["qGroup"] = qGroup
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFunctions", handle, **params)["qFunctions"]
        return [Function(**e) for e in response]

    def get_odbc_dsns(self) -> list[OdbcDsn]:
        """
        Returns the list of the ODBC connectors that are installed in the system.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetOdbcDsns", handle)["qOdbcDsns"]
        return [OdbcDsn(**e) for e in response]

    def get_ole_db_providers(self) -> list[OleDbProvider]:
        """
        Returns the list of the OLEDB providers installed on the system.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetOleDbProviders", handle)["qOleDbProviders"]
        return [OleDbProvider(**e) for e in response]

    def get_databases_from_connection_string(
        self, qConnection: Connection
    ) -> list[Database]:
        """
        Lists the databases in a ODBC, OLEDB or CUSTOM data source.

        Parameters
        ----------
        qConnection: Connection
          Information about the connection.
        """
        params = {}
        params["qConnection"] = qConnection
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send(
            "GetDatabasesFromConnectionString", handle, **params
        )["qDatabases"]
        return [Database(**e) for e in response]

    def is_valid_connection_string(self, qConnection: Connection) -> bool:
        """
        Checks if a connection string is valid.

        Parameters
        ----------
        qConnection: Connection
          Information about the connection.
        """
        params = {}
        params["qConnection"] = qConnection
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("IsValidConnectionString", handle, **params)[
            "qReturn"
        ]
        return response

    def get_default_app_folder(self) -> str:
        """
        Returns the folder where the apps are stored.
        This method applies only if running Qlik Sense Desktop.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetDefaultAppFolder", handle)["qPath"]
        return response

    def get_logical_drive_strings(self) -> list[DriveInfo]:
        """
        Lists the logical drives in the system.
        This method applies only if running Qlik Sense Desktop.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetLogicalDriveStrings", handle)["qDrives"]
        return [DriveInfo(**e) for e in response]

    def get_folder_items_for_path(self, qPath: str) -> list[FolderItem]:
        """
        Returns the files and folders located at a specified path.

        Parameters
        ----------
        qPath: str
          Absolute or relative path.
          Relative paths are relative to the default Apps folder.

          In Qlik Sense Enterprise:

          The list is generated by the QRS. The GetDocList method only returns documents the current user is allowed to access.

          In Qlik Sense Desktop:

          The apps are located in C:\\Users\<user name>\Documents\Qlik\Sense\Apps.
        """
        params = {}
        params["qPath"] = qPath
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetFolderItemsForPath", handle, **params)[
            "qFolderItems"
        ]
        return [FolderItem(**e) for e in response]

    def get_supported_code_pages(self) -> list[CodePage]:
        """
        Lists the supported code pages.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetSupportedCodePages", handle)["qCodePages"]
        return [CodePage(**e) for e in response]

    def get_custom_connectors(self, qReloadList: bool = None) -> list[CustomConnector]:
        """
        List the custom connectors available in the system.

        Parameters
        ----------
        qReloadList: bool = None
          Sets if the list of custom connectors should be reloaded or not.
          If set to false, only the connectors that were returned the previous time are returned. If new connectors have been added since the last call to the GetCustomConnectors method was made, the new connectors are not returned.
          If set to true, the GetCustomConnectors method looks for new connectors in the file system.
          The default value is false.
        """
        params = {}
        if qReloadList is not None:
            params["qReloadList"] = qReloadList
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetCustomConnectors", handle, **params)[
            "qConnectors"
        ]
        return [CustomConnector(**e) for e in response]

    def get_stream_list(self) -> list[NxStreamListEntry]:
        """
        Lists the streams.

        Parameters
        ----------
        """
        warnings.warn("GetStreamList is deprecated", DeprecationWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetStreamList", handle)["qStreamList"]
        return [NxStreamListEntry(**e) for e in response]

    def engine_version(self) -> NxEngineVersion:
        """
        Returns the version number of the Qlik engine component.

        Parameters
        ----------
        """
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("EngineVersion", handle)["qVersion"]
        obj = NxEngineVersion(**response)
        return obj

    def get_base_bnf(self, qBnfType: str) -> GetBaseBNFReturn:
        """
        Gets the current Backus-Naur Form (BNF) grammar of the Qlik engine scripting language, as well as a string hash calculated from that grammar. The BNF rules define the syntax for the script statements and the script or chart functions. If the hash changes between subsequent calls to this method, this indicates that the BNF has changed.
        In the Qlik engine grammars, a token is a string of one or more characters that is significant as a group. For example, a token could be a function name, a number, a letter, a parenthesis, and so on.

        Parameters
        ----------
        qBnfType: str
          The type of grammar to return:

          • The script statements and the script functions if qBnfType is set to S.

          • The chart functions if qBnfType is set to E.

          One of:

          • S or SCRIPT_TEXT_SCRIPT

          • E or SCRIPT_TEXT_EXPRESSION
        """
        params = {}
        params["qBnfType"] = qBnfType
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetBaseBNF", handle, **params)
        obj = GetBaseBNFReturn(**response)
        return obj

    def get_base_bnf_hash(self, qBnfType: str) -> str:
        """
        Gets a string hash calculated from the current Backus-Naur Form (BNF) grammar of the Qlik engine scripting language. If the hash changes between subsequent calls to this method, this indicates that the BNF grammar has changed.

        Parameters
        ----------
        qBnfType: str
          The type of grammar to return:

          • The script statements and the script functions if qBnfType is set to S.

          • The chart functions if qBnfType is set to E.

          One of:

          • S or SCRIPT_TEXT_SCRIPT

          • E or SCRIPT_TEXT_EXPRESSION
        """
        params = {}
        params["qBnfType"] = qBnfType
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetBaseBNFHash", handle, **params)["qBnfHash"]
        return response

    def get_base_bnf_string(self, qBnfType: str) -> GetBaseBNFStringReturn:
        """
        Gets the current Backus-Naur Form (BNF) grammar of the Qlik engine scripting language, as well as a string hash calculated from that grammar. The BNF rules define the syntax for the script statements and the script or chart functions. If the hash changes between subsequent calls to this method, this indicates that the BNF has changed.
        In the Qlik engine grammars, a token is a string of one or more characters that is significant as a group. For example, a token could be a function name, a number, a letter, a parenthesis, and so on.

        Parameters
        ----------
        qBnfType: str
          The type of grammar to return:

          • S: returns the script statements and the script functions.

          • E: returns the chart functions.

          One of:

          • S or SCRIPT_TEXT_SCRIPT

          • E or SCRIPT_TEXT_EXPRESSION
        """
        params = {}
        params["qBnfType"] = qBnfType
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetBaseBNFString", handle, **params)
        obj = GetBaseBNFStringReturn(**response)
        return obj

    def save_as(self, qNewAppName: str) -> str:
        """
        Save a copy of an app with a different name.
        Can be used to save a session app as an ordinary app.

        Parameters
        ----------
        qNewAppName: str
          <Name of the saved app>
        """
        warnings.warn("SaveAs is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qNewAppName"] = qNewAppName
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SaveAs", handle, **params)["qNewAppId"]
        return response

    def on(self, event_name, listener):
        self._session.on_handle(self.qHandle, event_name, listener)


@dataclass
class GraphMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupBookmarkData:
    """

    Attributes
    ----------
    qCyclePos: int
    qId: str
    """

    qCyclePos: int = None
    qId: str = None

    def __init__(self_, **kvargs):
        if "qCyclePos" in kvargs and kvargs["qCyclePos"] is not None:
            self_.qCyclePos = kvargs["qCyclePos"]
        if "qId" in kvargs and kvargs["qId"] is not None:
            self_.qId = kvargs["qId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupStateInfo:
    """

    Attributes
    ----------
    qCurrentItemName: str
    qGroupName: str
    """

    qCurrentItemName: str = None
    qGroupName: str = None

    def __init__(self_, **kvargs):
        if "qCurrentItemName" in kvargs and kvargs["qCurrentItemName"] is not None:
            self_.qCurrentItemName = kvargs["qCurrentItemName"]
        if "qGroupName" in kvargs and kvargs["qGroupName"] is not None:
            self_.qGroupName = kvargs["qGroupName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class HyperCube:
    """
    Renders the properties of a hypercube. Is the layout for HyperCubeDef.
    For more information about the definition of a hypercube, see Generic object.
    What is returned in HyperCube depends on the type of the hypercube (straight, pivot or stacked table, or tree) and on the method called (GetLayout, GetHyperCubeData, GetHyperCubePivotData, GetHyperCubeStackData, GetHyperCubeTreeData).

    Attributes
    ----------
    qCalcCondMsg: str
      The message displayed if calculation condition is not fulfilled.
    qColumnOrder: list[int]
      The order of the columns.
    qDataPages: list[NxDataPage]
      Set of data.
      Is empty if nothing has been defined in qInitialDataFetch in HyperCubeDef.
    qDimensionInfo: list[NxDimensionInfo]
      Information on the dimension.
    qEffectiveInterColumnSortOrder: list[int]
      Sort order of the columns in the hypercube.
      Column numbers are separated by a comma.
      Example: [1,0,2] means that the first column to be sorted was the column 1, followed by the column 0 and the column 2.
    qError: NxValidationError
      This parameter is optional and is displayed in case of error.
    qGrandTotalRow: list[NxCell]
      Aggregate for measures of all values in the field.
      The result value depends on the qAggrFunc defined in HyperCubeDef.
    qHasOtherValues: bool
      True if other row exists.
    qIndentMode: bool
      Is used for pivot tables only.
      If set to true, the formatting of the results is slightly different.
      This property is optional.
    qLastExpandedPos: NxCellPosition
      Is used for pivot tables only.
      Position of the last expended cell.
      This property is optional.
    qMeasureInfo: list[NxMeasureInfo]
      Information on the measure.
    qMode: Literal["DATA_MODE_STRAIGHT", "DATA_MODE_PIVOT", "DATA_MODE_PIVOT_STACK", "DATA_MODE_TREE", "DATA_MODE_DYNAMIC"]
      Information about the mode of the visualization.

      One of:

      • S or DATA_MODE_STRAIGHT

      • P or DATA_MODE_PIVOT

      • K or DATA_MODE_PIVOT_STACK

      • T or DATA_MODE_TREE

      • D or DATA_MODE_DYNAMIC
    qNoOfLeftDims: int
      Number of left dimensions.
      Default value is -1.
      The index related to each left dimension depends on the position of the pseudo dimension (if any).
      For example, a pivot table with:

      • Four dimensions in the following order: Country, City, Product and Category

      • One pseudo dimension in position 1

      • Three left dimensions.

      implies that:

      • The index 0 corresponds to the left dimension Country.

      • The index 1 corresponds to the pseudo dimension.

      • The index 2 corresponds to the left dimension City.

      • Product and Category are top dimensions.

      Another example:

      • Four dimensions in the following order: Country, City, Product and Category.

      • One pseudo dimension in position -1.

      • Three left dimensions.

      implies that:

      • The index -1 corresponds to the pseudo dimension; the pseudo dimension is the most to the right.

      • The index 0 corresponds to the left dimension Country.

      • The index 1 corresponds to the left dimension City.

      • The index 2 corresponds to the left dimension Product.

      • Category is a top dimension.
    qPivotDataPages: list[NxPivotPage]
      Set of data for pivot tables.
      Is empty if nothing has been defined in qInitialDataFetch in HyperCubeDef.
    qSize: Size
      Defines the size of the hypercube.
    qStackedDataPages: list[NxStackPage]
      Set of data for stacked tables.
      Is empty if nothing has been defined in qInitialDataFetch in HyperCubeDef.
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    qTitle: str
      Title of the hypercube, for example the title of a chart.
    qTreeNodesOnDim: list[int]
      The total number of nodes on each dimension (only applicable when qMode = T ).
    """

    qCalcCondMsg: str = None
    qColumnOrder: list[int] = None
    qDataPages: list[NxDataPage] = None
    qDimensionInfo: list[NxDimensionInfo] = None
    qEffectiveInterColumnSortOrder: list[int] = None
    qError: NxValidationError = None
    qGrandTotalRow: list[NxCell] = None
    qHasOtherValues: bool = None
    qIndentMode: bool = None
    qLastExpandedPos: NxCellPosition = None
    qMeasureInfo: list[NxMeasureInfo] = None
    qMode: Literal[
        "DATA_MODE_STRAIGHT",
        "DATA_MODE_PIVOT",
        "DATA_MODE_PIVOT_STACK",
        "DATA_MODE_TREE",
        "DATA_MODE_DYNAMIC",
    ] = None
    qNoOfLeftDims: int = None
    qPivotDataPages: list[NxPivotPage] = None
    qSize: Size = None
    qStackedDataPages: list[NxStackPage] = None
    qStateName: str = None
    qTitle: str = None
    qTreeNodesOnDim: list[int] = None

    def __init__(self_, **kvargs):
        if "qCalcCondMsg" in kvargs and kvargs["qCalcCondMsg"] is not None:
            self_.qCalcCondMsg = kvargs["qCalcCondMsg"]
        if "qColumnOrder" in kvargs and kvargs["qColumnOrder"] is not None:
            self_.qColumnOrder = kvargs["qColumnOrder"]
        if "qDataPages" in kvargs and kvargs["qDataPages"] is not None:
            if all(
                f"list[{type(e).__name__}]" == HyperCube.__annotations__["qDataPages"]
                for e in kvargs["qDataPages"]
            ):
                self_.qDataPages = kvargs["qDataPages"]
            else:
                self_.qDataPages = [
                    NxDataPage(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qDataPages"]
                ]
        if "qDimensionInfo" in kvargs and kvargs["qDimensionInfo"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == HyperCube.__annotations__["qDimensionInfo"]
                for e in kvargs["qDimensionInfo"]
            ):
                self_.qDimensionInfo = kvargs["qDimensionInfo"]
            else:
                self_.qDimensionInfo = [
                    NxDimensionInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qDimensionInfo"]
                ]
        if (
            "qEffectiveInterColumnSortOrder" in kvargs
            and kvargs["qEffectiveInterColumnSortOrder"] is not None
        ):
            self_.qEffectiveInterColumnSortOrder = kvargs[
                "qEffectiveInterColumnSortOrder"
            ]
        if "qError" in kvargs and kvargs["qError"] is not None:
            if type(kvargs["qError"]).__name__ == HyperCube.__annotations__["qError"]:
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qError"],
                )
        if "qGrandTotalRow" in kvargs and kvargs["qGrandTotalRow"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == HyperCube.__annotations__["qGrandTotalRow"]
                for e in kvargs["qGrandTotalRow"]
            ):
                self_.qGrandTotalRow = kvargs["qGrandTotalRow"]
            else:
                self_.qGrandTotalRow = [
                    NxCell(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qGrandTotalRow"]
                ]
        if "qHasOtherValues" in kvargs and kvargs["qHasOtherValues"] is not None:
            self_.qHasOtherValues = kvargs["qHasOtherValues"]
        if "qIndentMode" in kvargs and kvargs["qIndentMode"] is not None:
            self_.qIndentMode = kvargs["qIndentMode"]
        if "qLastExpandedPos" in kvargs and kvargs["qLastExpandedPos"] is not None:
            if (
                type(kvargs["qLastExpandedPos"]).__name__
                == HyperCube.__annotations__["qLastExpandedPos"]
            ):
                self_.qLastExpandedPos = kvargs["qLastExpandedPos"]
            else:
                self_.qLastExpandedPos = NxCellPosition(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qLastExpandedPos"],
                )
        if "qMeasureInfo" in kvargs and kvargs["qMeasureInfo"] is not None:
            if all(
                f"list[{type(e).__name__}]" == HyperCube.__annotations__["qMeasureInfo"]
                for e in kvargs["qMeasureInfo"]
            ):
                self_.qMeasureInfo = kvargs["qMeasureInfo"]
            else:
                self_.qMeasureInfo = [
                    NxMeasureInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qMeasureInfo"]
                ]
        if "qMode" in kvargs and kvargs["qMode"] is not None:
            self_.qMode = kvargs["qMode"]
        if "qNoOfLeftDims" in kvargs and kvargs["qNoOfLeftDims"] is not None:
            self_.qNoOfLeftDims = kvargs["qNoOfLeftDims"]
        if "qPivotDataPages" in kvargs and kvargs["qPivotDataPages"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == HyperCube.__annotations__["qPivotDataPages"]
                for e in kvargs["qPivotDataPages"]
            ):
                self_.qPivotDataPages = kvargs["qPivotDataPages"]
            else:
                self_.qPivotDataPages = [
                    NxPivotPage(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qPivotDataPages"]
                ]
        if "qSize" in kvargs and kvargs["qSize"] is not None:
            if type(kvargs["qSize"]).__name__ == HyperCube.__annotations__["qSize"]:
                self_.qSize = kvargs["qSize"]
            else:
                self_.qSize = Size(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qSize"],
                )
        if "qStackedDataPages" in kvargs and kvargs["qStackedDataPages"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == HyperCube.__annotations__["qStackedDataPages"]
                for e in kvargs["qStackedDataPages"]
            ):
                self_.qStackedDataPages = kvargs["qStackedDataPages"]
            else:
                self_.qStackedDataPages = [
                    NxStackPage(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qStackedDataPages"]
                ]
        if "qStateName" in kvargs and kvargs["qStateName"] is not None:
            self_.qStateName = kvargs["qStateName"]
        if "qTitle" in kvargs and kvargs["qTitle"] is not None:
            self_.qTitle = kvargs["qTitle"]
        if "qTreeNodesOnDim" in kvargs and kvargs["qTreeNodesOnDim"] is not None:
            self_.qTreeNodesOnDim = kvargs["qTreeNodesOnDim"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class HyperCubeDef:
    """
    Defines the properties of a hypercube.
    For more information about the definition of a hypercube, see Generic object.

    Attributes
    ----------
    qAlwaysFullyExpanded: bool
      If this property is set to true, the cells are always expanded. It implies that it is not possible to collapse any cells.
      The default value is false.
    qCalcCond: ValueExpr
      Specifies a calculation condition, which must be fulfilled for the hypercube to be (re)calculated.
      As long as the condition is not met, the engine does not perform a new calculation.
      This property is optional. By default, there is no calculation condition.
    qCalcCondition: NxCalcCond
      Specifies a calculation condition object.
      If CalcCondition.Cond is not fulfilled, the hypercube is not calculated and CalcCondition.Msg is evaluated.
      By default, there is no calculation condition.
      This property is optional.
    qColumnOrder: list[int]
      The order of the columns.
    qContextSetExpression: str
      Set Expression valid for the whole cube. Used to limit computations to the set specified.
    qDimensions: list[NxDimension]
      Array of dimensions.
    qDynamicScript: list[str]
      Hypercube Modifier Dynamic script string
    qExpansionState: list[ExpansionData]
      Expansion state per dimension for pivot mode ( qMode is P).
    qIndentMode: bool
      This property applies for pivot tables and allows to change the layout of the table. An indentation is added to the beginning of each row.
      The default value is false.
    qInitialDataFetch: list[NxPage]
      Initial data set.
    qInterColumnSortOrder: list[int]
      Defines the sort order of the columns in the hypercube.
      Column numbers are separated by a comma.
      Example: [1,0,2] means that the first column to be sorted should be the column 1, followed by the column 0 and the column 2.
      The default sort order is the order in which the dimensions and measures have been defined in the hypercube. By default, the pseudo-dimension (if any) is the most to the right in the array.
      The index of the pseudo-dimension (if any) is -1.
      Pseudo dimensions only apply for pivot tables with more than one measure.
      A pseudo dimension groups together the measures defined in a pivot table. You can neither collapse/expand a pseudo dimension nor make any selections in it.
      Stacked pivot tables can only contain one measure.
    qMaxStackedCells: int
      Maximum number of cells for an initial data fetch (set in qInitialDataFetch ) when in stacked mode ( qMode is K).
      The default value is 5000.
    qMeasures: list[NxMeasure]
      Array of measures.
    qMode: Literal["DATA_MODE_STRAIGHT", "DATA_MODE_PIVOT", "DATA_MODE_PIVOT_STACK", "DATA_MODE_TREE", "DATA_MODE_DYNAMIC"]
      Defines the way the data are handled internally by the engine.
      Default value is DATA_MODE_STRAIGHT .
      A pivot table can contain several dimensions and measures whereas a stacked pivot table can contain several dimensions but only one measure.

      One of:

      • S or DATA_MODE_STRAIGHT

      • P or DATA_MODE_PIVOT

      • K or DATA_MODE_PIVOT_STACK

      • T or DATA_MODE_TREE

      • D or DATA_MODE_DYNAMIC
    qNoOfLeftDims: int
      Number of left dimensions.
      Default value is -1. In that case, all dimensions are left dimensions.
      Hidden dimensions (e.g. due to unfulfilled calc condition on dimension level) is still counted in this context.
      The index related to each left dimension depends on the position of the pseudo dimension (if any).
      For example, a pivot table with:

      • Four dimensions in the following order: Country, City, Product and Category.

      • One pseudo dimension in position 1 (the position is defined in qInterColumnSortOrder )
      qInterColumnSortOrder is (0,-1,1,2,3).

      • Three left dimensions ( qNoOfLeftDims is set to 3).

      implies that:

      • The index 0 corresponds to the left dimension Country.

      • The index 1 corresponds to the pseudo dimension.

      • The index 2 corresponds to the left dimension City.

      • Product and Category are top dimensions.

      Another example:

      • Four dimensions in the following order: Country, City, Product and Category.

      • Three left dimensions ( qNoOfLeftDims is set to 3).

      • One pseudo dimension.

      • The property qInterColumnSortOrder is left empty.

      Implies that:

      • The index 0 corresponds to the left dimension Country.

      • The index 1 corresponds to the left dimension City.

      • The index 2 corresponds to the left dimension Product.

      • Category is a top dimension.

      • The pseudo dimension is a top dimension.
    qPopulateMissing: bool
      If this property is set to true, the missing symbols (if any) are replaced by 0 if the value is a numeric and by an empty string if the value is a string.
      The default value is false.
    qPseudoDimPos: int
    qReductionMode: Literal["DATA_REDUCTION_NONE", "DATA_REDUCTION_ONEDIM", "DATA_REDUCTION_SCATTERED", "DATA_REDUCTION_CLUSTERED", "DATA_REDUCTION_STACKED"]

      One of:

      • N or DATA_REDUCTION_NONE

      • D1 or DATA_REDUCTION_ONEDIM

      • S or DATA_REDUCTION_SCATTERED

      • C or DATA_REDUCTION_CLUSTERED

      • ST or DATA_REDUCTION_STACKED
    qShowTotalsAbove: bool
      If set to true, the total (if any) is shown on the first row.
      The default value is false.
    qSortbyYValue: int
      To enable the sorting by ascending or descending order in the values of a measure.
      This property applies to pivot tables and stacked pivot tables.
      In the case of a pivot table, the measure or pseudo dimension should be defined as a top dimension. The sorting is restricted to the values of the first measure in a pivot table.
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    qSuppressMissing: bool
      Removes missing values.
    qSuppressZero: bool
      Removes zero values.
    qTitle: StringExpr
      Title of the hypercube, for example the title of a chart.
    """

    qAlwaysFullyExpanded: bool = None
    qCalcCond: ValueExpr = None
    qCalcCondition: NxCalcCond = None
    qColumnOrder: list[int] = None
    qContextSetExpression: str = None
    qDimensions: list[NxDimension] = None
    qDynamicScript: list[str] = None
    qExpansionState: list[ExpansionData] = None
    qIndentMode: bool = None
    qInitialDataFetch: list[NxPage] = None
    qInterColumnSortOrder: list[int] = None
    qMaxStackedCells: int = 5000
    qMeasures: list[NxMeasure] = None
    qMode: Literal[
        "DATA_MODE_STRAIGHT",
        "DATA_MODE_PIVOT",
        "DATA_MODE_PIVOT_STACK",
        "DATA_MODE_TREE",
        "DATA_MODE_DYNAMIC",
    ] = "DATA_MODE_STRAIGHT"
    qNoOfLeftDims: int = -1
    qPopulateMissing: bool = None
    qPseudoDimPos: int = -1
    qReductionMode: Literal[
        "DATA_REDUCTION_NONE",
        "DATA_REDUCTION_ONEDIM",
        "DATA_REDUCTION_SCATTERED",
        "DATA_REDUCTION_CLUSTERED",
        "DATA_REDUCTION_STACKED",
    ] = None
    qShowTotalsAbove: bool = None
    qSortbyYValue: int = None
    qStateName: str = None
    qSuppressMissing: bool = None
    qSuppressZero: bool = None
    qTitle: StringExpr = None

    def __init__(self_, **kvargs):
        if (
            "qAlwaysFullyExpanded" in kvargs
            and kvargs["qAlwaysFullyExpanded"] is not None
        ):
            self_.qAlwaysFullyExpanded = kvargs["qAlwaysFullyExpanded"]
        if "qCalcCond" in kvargs and kvargs["qCalcCond"] is not None:
            if (
                type(kvargs["qCalcCond"]).__name__
                == HyperCubeDef.__annotations__["qCalcCond"]
            ):
                self_.qCalcCond = kvargs["qCalcCond"]
            else:
                self_.qCalcCond = ValueExpr(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qCalcCond"],
                )
        if "qCalcCondition" in kvargs and kvargs["qCalcCondition"] is not None:
            if (
                type(kvargs["qCalcCondition"]).__name__
                == HyperCubeDef.__annotations__["qCalcCondition"]
            ):
                self_.qCalcCondition = kvargs["qCalcCondition"]
            else:
                self_.qCalcCondition = NxCalcCond(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qCalcCondition"],
                )
        if "qColumnOrder" in kvargs and kvargs["qColumnOrder"] is not None:
            self_.qColumnOrder = kvargs["qColumnOrder"]
        if (
            "qContextSetExpression" in kvargs
            and kvargs["qContextSetExpression"] is not None
        ):
            self_.qContextSetExpression = kvargs["qContextSetExpression"]
        if "qDimensions" in kvargs and kvargs["qDimensions"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == HyperCubeDef.__annotations__["qDimensions"]
                for e in kvargs["qDimensions"]
            ):
                self_.qDimensions = kvargs["qDimensions"]
            else:
                self_.qDimensions = [
                    NxDimension(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qDimensions"]
                ]
        if "qDynamicScript" in kvargs and kvargs["qDynamicScript"] is not None:
            self_.qDynamicScript = kvargs["qDynamicScript"]
        if "qExpansionState" in kvargs and kvargs["qExpansionState"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == HyperCubeDef.__annotations__["qExpansionState"]
                for e in kvargs["qExpansionState"]
            ):
                self_.qExpansionState = kvargs["qExpansionState"]
            else:
                self_.qExpansionState = [
                    ExpansionData(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qExpansionState"]
                ]
        if "qIndentMode" in kvargs and kvargs["qIndentMode"] is not None:
            self_.qIndentMode = kvargs["qIndentMode"]
        if "qInitialDataFetch" in kvargs and kvargs["qInitialDataFetch"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == HyperCubeDef.__annotations__["qInitialDataFetch"]
                for e in kvargs["qInitialDataFetch"]
            ):
                self_.qInitialDataFetch = kvargs["qInitialDataFetch"]
            else:
                self_.qInitialDataFetch = [
                    NxPage(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qInitialDataFetch"]
                ]
        if (
            "qInterColumnSortOrder" in kvargs
            and kvargs["qInterColumnSortOrder"] is not None
        ):
            self_.qInterColumnSortOrder = kvargs["qInterColumnSortOrder"]
        if "qMaxStackedCells" in kvargs and kvargs["qMaxStackedCells"] is not None:
            self_.qMaxStackedCells = kvargs["qMaxStackedCells"]
        if "qMeasures" in kvargs and kvargs["qMeasures"] is not None:
            if all(
                f"list[{type(e).__name__}]" == HyperCubeDef.__annotations__["qMeasures"]
                for e in kvargs["qMeasures"]
            ):
                self_.qMeasures = kvargs["qMeasures"]
            else:
                self_.qMeasures = [
                    NxMeasure(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qMeasures"]
                ]
        if "qMode" in kvargs and kvargs["qMode"] is not None:
            self_.qMode = kvargs["qMode"]
        if "qNoOfLeftDims" in kvargs and kvargs["qNoOfLeftDims"] is not None:
            self_.qNoOfLeftDims = kvargs["qNoOfLeftDims"]
        if "qPopulateMissing" in kvargs and kvargs["qPopulateMissing"] is not None:
            self_.qPopulateMissing = kvargs["qPopulateMissing"]
        if "qPseudoDimPos" in kvargs and kvargs["qPseudoDimPos"] is not None:
            self_.qPseudoDimPos = kvargs["qPseudoDimPos"]
        if "qReductionMode" in kvargs and kvargs["qReductionMode"] is not None:
            self_.qReductionMode = kvargs["qReductionMode"]
        if "qShowTotalsAbove" in kvargs and kvargs["qShowTotalsAbove"] is not None:
            self_.qShowTotalsAbove = kvargs["qShowTotalsAbove"]
        if "qSortbyYValue" in kvargs and kvargs["qSortbyYValue"] is not None:
            self_.qSortbyYValue = kvargs["qSortbyYValue"]
        if "qStateName" in kvargs and kvargs["qStateName"] is not None:
            self_.qStateName = kvargs["qStateName"]
        if "qSuppressMissing" in kvargs and kvargs["qSuppressMissing"] is not None:
            self_.qSuppressMissing = kvargs["qSuppressMissing"]
        if "qSuppressZero" in kvargs and kvargs["qSuppressZero"] is not None:
            self_.qSuppressZero = kvargs["qSuppressZero"]
        if "qTitle" in kvargs and kvargs["qTitle"] is not None:
            if (
                type(kvargs["qTitle"]).__name__
                == HyperCubeDef.__annotations__["qTitle"]
            ):
                self_.qTitle = kvargs["qTitle"]
            else:
                self_.qTitle = StringExpr(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qTitle"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class InputFieldItem:
    """

    Attributes
    ----------
    qFieldName: str
    qPackedHashKeys: list[int]
    qValues: list[FieldValue]
    """

    qFieldName: str = None
    qPackedHashKeys: list[int] = None
    qValues: list[FieldValue] = None

    def __init__(self_, **kvargs):
        if "qFieldName" in kvargs and kvargs["qFieldName"] is not None:
            self_.qFieldName = kvargs["qFieldName"]
        if "qPackedHashKeys" in kvargs and kvargs["qPackedHashKeys"] is not None:
            self_.qPackedHashKeys = kvargs["qPackedHashKeys"]
        if "qValues" in kvargs and kvargs["qValues"] is not None:
            if all(
                f"list[{type(e).__name__}]" == InputFieldItem.__annotations__["qValues"]
                for e in kvargs["qValues"]
            ):
                self_.qValues = kvargs["qValues"]
            else:
                self_.qValues = [
                    FieldValue(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qValues"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class InterFieldSortData:
    """

    Attributes
    ----------
    qName: str
    qReversed: bool
    """

    qName: str = None
    qReversed: bool = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qReversed" in kvargs and kvargs["qReversed"] is not None:
            self_.qReversed = kvargs["qReversed"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class InteractDef:
    """

    Attributes
    ----------
    qButtons: int
      Buttons displayed in the message box dialog.
      This property is relevant if qType is *IT_MSGBOX*.
      One of:

      • 0 means that the qButtons property is not relevant.

      • 17 means that the message box contains the OK and Cancel buttons or the stop -sign icon.
    qHidden: bool
      This property is set to true if the returned statement is an hidden script statement.
    qInput: str
      Is not used in Qlik Sense.
    qLine: str
      Next script statement to be executed.
      This property is used if the type of interaction is *IT_SCRIPTLINE*.
    qMsg: str
      Message used in the message box dialog.
      This property is relevant if qType is *IT_MSGBOX*.
    qNewLineNr: int
      First line number of the next statement to be executed.
      This property is used if the type of interaction is *IT_SCRIPTLINE*.
    qOldLineNr: int
      First line number of the previously executed statement.
      This property is used if the type of interaction is *IT_SCRIPTLINE*.
    qPath: str
      Path specified by the Include script variable.
      This property is used if the type of interaction is *IT_SCRIPTLINE*.
      Example of an Include variable:
      $(Include=lib:\\\MyDataFiles\abc.txt);
    qResult: int
      Not relevant for describing the requested user interaction.
    qTitle: str
      Title used in the message box dialog.
      This property is relevant if qType is *IT_MSGBOX*.
    qType: Literal["IT_MSGBOX", "IT_SCRIPTLINE", "IT_BREAK", "IT_INPUT", "IT_END", "IT_PASSWD", "IT_USERNAME"]
      Interaction type.

      One of:

      • IT_MSGBOX

      • IT_SCRIPTLINE

      • IT_BREAK

      • IT_INPUT

      • IT_END

      • IT_PASSWD

      • IT_USERNAME
    """

    qButtons: int = None
    qHidden: bool = None
    qInput: str = None
    qLine: str = None
    qMsg: str = None
    qNewLineNr: int = None
    qOldLineNr: int = None
    qPath: str = None
    qResult: int = None
    qTitle: str = None
    qType: Literal[
        "IT_MSGBOX",
        "IT_SCRIPTLINE",
        "IT_BREAK",
        "IT_INPUT",
        "IT_END",
        "IT_PASSWD",
        "IT_USERNAME",
    ] = None

    def __init__(self_, **kvargs):
        if "qButtons" in kvargs and kvargs["qButtons"] is not None:
            self_.qButtons = kvargs["qButtons"]
        if "qHidden" in kvargs and kvargs["qHidden"] is not None:
            self_.qHidden = kvargs["qHidden"]
        if "qInput" in kvargs and kvargs["qInput"] is not None:
            self_.qInput = kvargs["qInput"]
        if "qLine" in kvargs and kvargs["qLine"] is not None:
            self_.qLine = kvargs["qLine"]
        if "qMsg" in kvargs and kvargs["qMsg"] is not None:
            self_.qMsg = kvargs["qMsg"]
        if "qNewLineNr" in kvargs and kvargs["qNewLineNr"] is not None:
            self_.qNewLineNr = kvargs["qNewLineNr"]
        if "qOldLineNr" in kvargs and kvargs["qOldLineNr"] is not None:
            self_.qOldLineNr = kvargs["qOldLineNr"]
        if "qPath" in kvargs and kvargs["qPath"] is not None:
            self_.qPath = kvargs["qPath"]
        if "qResult" in kvargs and kvargs["qResult"] is not None:
            self_.qResult = kvargs["qResult"]
        if "qTitle" in kvargs and kvargs["qTitle"] is not None:
            self_.qTitle = kvargs["qTitle"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class InteractType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
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
class KeyType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LayoutBookmarkData:
    """

    Attributes
    ----------
    qActive: bool
    qId: str
    qScrollPos: ScrollPosition
    qShowMode: int
    """

    qActive: bool = None
    qId: str = None
    qScrollPos: ScrollPosition = None
    qShowMode: int = None

    def __init__(self_, **kvargs):
        if "qActive" in kvargs and kvargs["qActive"] is not None:
            self_.qActive = kvargs["qActive"]
        if "qId" in kvargs and kvargs["qId"] is not None:
            self_.qId = kvargs["qId"]
        if "qScrollPos" in kvargs and kvargs["qScrollPos"] is not None:
            if (
                type(kvargs["qScrollPos"]).__name__
                == LayoutBookmarkData.__annotations__["qScrollPos"]
            ):
                self_.qScrollPos = kvargs["qScrollPos"]
            else:
                self_.qScrollPos = ScrollPosition(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qScrollPos"],
                )
        if "qShowMode" in kvargs and kvargs["qShowMode"] is not None:
            self_.qShowMode = kvargs["qShowMode"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LayoutExclude:
    """
    Contains JSON to be excluded from validation.

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LayoutFieldInfo:
    """
    Meta data about the selection in a field.

    Attributes
    ----------
    qExcludedValuesCount: int
      Number of excluded values in the field.
    qFieldName: str
      The name of the field.
    qValuesCount: int
      Number of selected values in the field.
    """

    qExcludedValuesCount: int = None
    qFieldName: str = None
    qValuesCount: int = None

    def __init__(self_, **kvargs):
        if (
            "qExcludedValuesCount" in kvargs
            and kvargs["qExcludedValuesCount"] is not None
        ):
            self_.qExcludedValuesCount = kvargs["qExcludedValuesCount"]
        if "qFieldName" in kvargs and kvargs["qFieldName"] is not None:
            self_.qFieldName = kvargs["qFieldName"]
        if "qValuesCount" in kvargs and kvargs["qValuesCount"] is not None:
            self_.qValuesCount = kvargs["qValuesCount"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LineageInfo:
    """

    Attributes
    ----------
    qDiscriminator: str
      A string indicating the origin of the data:

      • [filename]: the data comes from a local file.

      • INLINE: the data is entered inline in the load script.

      • RESIDENT: the data comes from a resident table. The table name is listed.

      • AUTOGENERATE: the data is generated from the load script (no external table of data source).

      • Provider: the data comes from a data connection. The connector source name is listed.

      • [webfile]: the data comes from a web-based file.

      • STORE: path to QVD or TXT file where data is stored.

      • EXTENSION: the data comes from a Server Side Extension (SSE).
    qStatement: str
      The LOAD and SELECT script statements from the data load script.
    """

    qDiscriminator: str = None
    qStatement: str = None

    def __init__(self_, **kvargs):
        if "qDiscriminator" in kvargs and kvargs["qDiscriminator"] is not None:
            self_.qDiscriminator = kvargs["qDiscriminator"]
        if "qStatement" in kvargs and kvargs["qStatement"] is not None:
            self_.qStatement = kvargs["qStatement"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ListObject:
    """
    Renders the properties of a list object. Is the layout for ListObjectDef.
    For more information about the definition of a list object, see Generic object.
    ListObject is used by the GetLayout Method to display the properties of a list object.

    Attributes
    ----------
    qDataPages: list[NxDataPage]
      Set of data.
      Is empty if nothing has been defined in qInitialDataFetch in ListObjectDef.
    qDimensionInfo: NxDimensionInfo
      Information about the dimension.
    qError: NxValidationError
      This parameter is optional and is displayed in case of error.
    qExpressions: list[NxListObjectExpression]
      Lists the expressions in the list object.
    qSize: Size
      Defines the size of a list object.
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    """

    qDataPages: list[NxDataPage] = None
    qDimensionInfo: NxDimensionInfo = None
    qError: NxValidationError = None
    qExpressions: list[NxListObjectExpression] = None
    qSize: Size = None
    qStateName: str = None

    def __init__(self_, **kvargs):
        if "qDataPages" in kvargs and kvargs["qDataPages"] is not None:
            if all(
                f"list[{type(e).__name__}]" == ListObject.__annotations__["qDataPages"]
                for e in kvargs["qDataPages"]
            ):
                self_.qDataPages = kvargs["qDataPages"]
            else:
                self_.qDataPages = [
                    NxDataPage(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qDataPages"]
                ]
        if "qDimensionInfo" in kvargs and kvargs["qDimensionInfo"] is not None:
            if (
                type(kvargs["qDimensionInfo"]).__name__
                == ListObject.__annotations__["qDimensionInfo"]
            ):
                self_.qDimensionInfo = kvargs["qDimensionInfo"]
            else:
                self_.qDimensionInfo = NxDimensionInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qDimensionInfo"],
                )
        if "qError" in kvargs and kvargs["qError"] is not None:
            if type(kvargs["qError"]).__name__ == ListObject.__annotations__["qError"]:
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qError"],
                )
        if "qExpressions" in kvargs and kvargs["qExpressions"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == ListObject.__annotations__["qExpressions"]
                for e in kvargs["qExpressions"]
            ):
                self_.qExpressions = kvargs["qExpressions"]
            else:
                self_.qExpressions = [
                    NxListObjectExpression(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qExpressions"]
                ]
        if "qSize" in kvargs and kvargs["qSize"] is not None:
            if type(kvargs["qSize"]).__name__ == ListObject.__annotations__["qSize"]:
                self_.qSize = kvargs["qSize"]
            else:
                self_.qSize = Size(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qSize"],
                )
        if "qStateName" in kvargs and kvargs["qStateName"] is not None:
            self_.qStateName = kvargs["qStateName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ListObjectDef:
    """
    Defines the properties of a list object.
    For more information about the definition of a list object, see Generic object.

    Attributes
    ----------
    qAutoSortByState: NxAutoSortByStateDef
      Defines the sorting by state.
    qDef: NxInlineDimensionDef
      Refers to a dimension stored in the list object.
    qDirectQuerySimplifiedView: bool
      If set to true, reduces the set of states returned.
      Supported for Direct Query mode only.
      Default is false.
    qExpressions: list[NxListObjectExpressionDef]
      Lists the expressions in the list object.
      This parameter is optional.
    qFrequencyMode: Literal["NX_FREQUENCY_NONE", "NX_FREQUENCY_VALUE", "NX_FREQUENCY_PERCENT", "NX_FREQUENCY_RELATIVE"]
      Defines the frequency mode. The frequency mode is used to calculate the frequency of a value in a list object.
      Default is NX_FREQUENCY_NONE .
      This parameter is optional.

      One of:

      • N or NX_FREQUENCY_NONE

      • V or NX_FREQUENCY_VALUE

      • P or NX_FREQUENCY_PERCENT

      • R or NX_FREQUENCY_RELATIVE
    qInitialDataFetch: list[NxPage]
      Fetches an initial data set.
    qLibraryId: str
      Refers to a dimension stored in the library.
    qShowAlternatives: bool
      If set to true, alternative values are allowed in qData .
      If set to false, no alternative values are displayed in qData . Values are excluded instead.
      The default value is false.
      Note that on the contrary, the qStateCounts parameter counts the excluded values as alternative values.
      This parameter is optional.
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    """

    qAutoSortByState: NxAutoSortByStateDef = None
    qDef: NxInlineDimensionDef = None
    qDirectQuerySimplifiedView: bool = None
    qExpressions: list[NxListObjectExpressionDef] = None
    qFrequencyMode: Literal[
        "NX_FREQUENCY_NONE",
        "NX_FREQUENCY_VALUE",
        "NX_FREQUENCY_PERCENT",
        "NX_FREQUENCY_RELATIVE",
    ] = "NX_FREQUENCY_NONE"
    qInitialDataFetch: list[NxPage] = None
    qLibraryId: str = None
    qShowAlternatives: bool = None
    qStateName: str = None

    def __init__(self_, **kvargs):
        if "qAutoSortByState" in kvargs and kvargs["qAutoSortByState"] is not None:
            if (
                type(kvargs["qAutoSortByState"]).__name__
                == ListObjectDef.__annotations__["qAutoSortByState"]
            ):
                self_.qAutoSortByState = kvargs["qAutoSortByState"]
            else:
                self_.qAutoSortByState = NxAutoSortByStateDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qAutoSortByState"],
                )
        if "qDef" in kvargs and kvargs["qDef"] is not None:
            if type(kvargs["qDef"]).__name__ == ListObjectDef.__annotations__["qDef"]:
                self_.qDef = kvargs["qDef"]
            else:
                self_.qDef = NxInlineDimensionDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qDef"],
                )
        if (
            "qDirectQuerySimplifiedView" in kvargs
            and kvargs["qDirectQuerySimplifiedView"] is not None
        ):
            self_.qDirectQuerySimplifiedView = kvargs["qDirectQuerySimplifiedView"]
        if "qExpressions" in kvargs and kvargs["qExpressions"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == ListObjectDef.__annotations__["qExpressions"]
                for e in kvargs["qExpressions"]
            ):
                self_.qExpressions = kvargs["qExpressions"]
            else:
                self_.qExpressions = [
                    NxListObjectExpressionDef(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qExpressions"]
                ]
        if "qFrequencyMode" in kvargs and kvargs["qFrequencyMode"] is not None:
            self_.qFrequencyMode = kvargs["qFrequencyMode"]
        if "qInitialDataFetch" in kvargs and kvargs["qInitialDataFetch"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == ListObjectDef.__annotations__["qInitialDataFetch"]
                for e in kvargs["qInitialDataFetch"]
            ):
                self_.qInitialDataFetch = kvargs["qInitialDataFetch"]
            else:
                self_.qInitialDataFetch = [
                    NxPage(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qInitialDataFetch"]
                ]
        if "qLibraryId" in kvargs and kvargs["qLibraryId"] is not None:
            self_.qLibraryId = kvargs["qLibraryId"]
        if "qShowAlternatives" in kvargs and kvargs["qShowAlternatives"] is not None:
            self_.qShowAlternatives = kvargs["qShowAlternatives"]
        if "qStateName" in kvargs and kvargs["qStateName"] is not None:
            self_.qStateName = kvargs["qStateName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LocaleInfo:
    """

    Attributes
    ----------
    qBrokenWeeks: bool
      Is set to true if broken weeks are allowed in a year.
      According to ISO 8601, no broken weeks should be allowed.
      This property is not shown if set to false.
      If qBrokenWeeks is set to true, qReferenceDay is irrelevant.
      If this property has not been set in a script, the returned value comes from the Windows operating system.
    qCalendarStrings: CalendarStrings
      Information about the calendar.
    qCollation: str
      Locale name (following language tagging convention RFC 4646):
      < language>-<REGION>
      Where:

      • language is a lowercase ISO  639 language code

      • REGION specifies an uppercase ISO 3166 country code.

      If this property has not been set in a script, the returned value comes from the Windows operating system.
    qCurrentYear: int
      Current year.
    qDateFmt: str
      Date format.
      Example: YYYY-MM-DD
    qDecimalSep: str
      Decimal separator.
    qFirstMonthOfYear: int
      First month of the year, starting from 1.
      According to ISO 8601, January is the first month of the year.

      • 1 = January

      • 2 = February

      • 12 = January

      If this property has not been set in a script, the returned value comes from the Windows operating system.
    qFirstWeekDay: int
      First day of the week, starting from 0.
      According to ISO 8601, Monday is the first day of the week.

      • 0 = Monday

      • 1 = Tuesday

      • ...

      • 6 = Sunday

      If this property has not been set in a script, the returned value comes from the Windows operating system.
    qListSep: str
      List separator.
    qMoneyDecimalSep: str
      Money decimal separator.
    qMoneyFmt: str
      Money format.
      Example: .0,00 kr;-#.##0,00 kr::
    qMoneyThousandSep: str
      Money thousand separator.
    qNumericalAbbreviation: str
      Number format.
      Example: 3:k;6:M;9:G;12:T;15:P;18:E;21:Z;24:Y;-3:m;-6:μ;-9:n;-12:p;-15:f;-18:a;-21:z;-24:y
    qReferenceDay: int
      Day in the year that is always in week 1.
      According to ISO 8601, January 4th should always be part of the first week of the year ( qReferenceDay =4).
      Recommended values are in the range 1 and 7.
      If this property has not been set in a script, the returned value comes from the Windows operating system.
      This property is not relevant if there are broken weeks in the year.
    qThousandSep: str
      Thousand separator.
    qTimeFmt: str
      Time format.
      Example: hh:mm:ss
    qTimestampFmt: str
      Time stamp format.
      Example: YYYY-MM-DD hh:mm:ss[.fff]
    """

    qBrokenWeeks: bool = None
    qCalendarStrings: CalendarStrings = None
    qCollation: str = None
    qCurrentYear: int = None
    qDateFmt: str = None
    qDecimalSep: str = None
    qFirstMonthOfYear: int = None
    qFirstWeekDay: int = None
    qListSep: str = None
    qMoneyDecimalSep: str = None
    qMoneyFmt: str = None
    qMoneyThousandSep: str = None
    qNumericalAbbreviation: str = None
    qReferenceDay: int = None
    qThousandSep: str = None
    qTimeFmt: str = None
    qTimestampFmt: str = None

    def __init__(self_, **kvargs):
        if "qBrokenWeeks" in kvargs and kvargs["qBrokenWeeks"] is not None:
            self_.qBrokenWeeks = kvargs["qBrokenWeeks"]
        if "qCalendarStrings" in kvargs and kvargs["qCalendarStrings"] is not None:
            if (
                type(kvargs["qCalendarStrings"]).__name__
                == LocaleInfo.__annotations__["qCalendarStrings"]
            ):
                self_.qCalendarStrings = kvargs["qCalendarStrings"]
            else:
                self_.qCalendarStrings = CalendarStrings(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qCalendarStrings"],
                )
        if "qCollation" in kvargs and kvargs["qCollation"] is not None:
            self_.qCollation = kvargs["qCollation"]
        if "qCurrentYear" in kvargs and kvargs["qCurrentYear"] is not None:
            self_.qCurrentYear = kvargs["qCurrentYear"]
        if "qDateFmt" in kvargs and kvargs["qDateFmt"] is not None:
            self_.qDateFmt = kvargs["qDateFmt"]
        if "qDecimalSep" in kvargs and kvargs["qDecimalSep"] is not None:
            self_.qDecimalSep = kvargs["qDecimalSep"]
        if "qFirstMonthOfYear" in kvargs and kvargs["qFirstMonthOfYear"] is not None:
            self_.qFirstMonthOfYear = kvargs["qFirstMonthOfYear"]
        if "qFirstWeekDay" in kvargs and kvargs["qFirstWeekDay"] is not None:
            self_.qFirstWeekDay = kvargs["qFirstWeekDay"]
        if "qListSep" in kvargs and kvargs["qListSep"] is not None:
            self_.qListSep = kvargs["qListSep"]
        if "qMoneyDecimalSep" in kvargs and kvargs["qMoneyDecimalSep"] is not None:
            self_.qMoneyDecimalSep = kvargs["qMoneyDecimalSep"]
        if "qMoneyFmt" in kvargs and kvargs["qMoneyFmt"] is not None:
            self_.qMoneyFmt = kvargs["qMoneyFmt"]
        if "qMoneyThousandSep" in kvargs and kvargs["qMoneyThousandSep"] is not None:
            self_.qMoneyThousandSep = kvargs["qMoneyThousandSep"]
        if (
            "qNumericalAbbreviation" in kvargs
            and kvargs["qNumericalAbbreviation"] is not None
        ):
            self_.qNumericalAbbreviation = kvargs["qNumericalAbbreviation"]
        if "qReferenceDay" in kvargs and kvargs["qReferenceDay"] is not None:
            self_.qReferenceDay = kvargs["qReferenceDay"]
        if "qThousandSep" in kvargs and kvargs["qThousandSep"] is not None:
            self_.qThousandSep = kvargs["qThousandSep"]
        if "qTimeFmt" in kvargs and kvargs["qTimeFmt"] is not None:
            self_.qTimeFmt = kvargs["qTimeFmt"]
        if "qTimestampFmt" in kvargs and kvargs["qTimestampFmt"] is not None:
            self_.qTimestampFmt = kvargs["qTimestampFmt"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LogOnType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class MeasureList:
    """
    Lists the measures. Is the layout for MeasureListDef.

    Attributes
    ----------
    qItems: list[NxContainerEntry]
      Information about the list of measures.
    """

    qItems: list[NxContainerEntry] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs and kvargs["qItems"] is not None:
            if all(
                f"list[{type(e).__name__}]" == MeasureList.__annotations__["qItems"]
                for e in kvargs["qItems"]
            ):
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [
                    NxContainerEntry(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qItems"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class MeasureListDef:
    """
    Defines the list of measures.

    Attributes
    ----------
    qData: JsonObject
      Data
    qType: str
      Type of the list.
    """

    qData: JsonObject = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qData" in kvargs and kvargs["qData"] is not None:
            if (
                type(kvargs["qData"]).__name__
                == MeasureListDef.__annotations__["qData"]
            ):
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qData"],
                )
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class MediaList:
    """
    Lists the media files. Is the layout for MediaListDef.
    This struct is deprecated.

    Attributes
    ----------
    qItems: list[MediaListItem]
      Information about the list of media files.
      In Qlik Sense Desktop, the media files are retrieved from:
      %userprofile%\Documents\Qlik\Sense\Content\Default
      In Qlik Sense Enterprise, the media files are retrieved from:
      <installation_directory>\Qlik\Sense\Repository\Content\Default
      The default installation directory is ProgramData .
    """

    qItems: list[MediaListItem] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs and kvargs["qItems"] is not None:
            if all(
                f"list[{type(e).__name__}]" == MediaList.__annotations__["qItems"]
                for e in kvargs["qItems"]
            ):
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [
                    MediaListItem(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qItems"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class MediaListDef:
    """
    Defines the list of media files.
    This struct is deprecated.

     Properties:
    "qMediaListDef": {}
    qMediaListDef has an empty structure. No properties need to be set.

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class MediaListItem:
    """
    In addition, this structure can return dynamic properties.

    Attributes
    ----------
    qUrl: str
      Relative path to the media file.
      Media files located:

      • in the /content/default/ folder are outside the qvf file.

      • in the /media/ folder are embedded in the qvf file.
    qUrlDef: str
      Relative path to the media file. The URL is static.
      Media files located:

      • in the /content/default/ folder are outside the qvf file.

      • in the /media/ folder are embedded in the qvf file.
    """

    qUrl: str = None
    qUrlDef: str = None

    def __init__(self_, **kvargs):
        if "qUrl" in kvargs and kvargs["qUrl"] is not None:
            self_.qUrl = kvargs["qUrl"]
        if "qUrlDef" in kvargs and kvargs["qUrlDef"] is not None:
            self_.qUrlDef = kvargs["qUrlDef"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class MetaData:
    """

    Attributes
    ----------
    qAccessList: list[str]
    qHidden: bool
    qLinkedTo: list[str]
    qPersonalEditionHash_OBSOLETE: str
    qRestrictedAccess: bool
    qShared: bool
    qSheetId: str
    qTemporary: bool
    qUtcModifyTime: float
    """

    qAccessList: list[str] = None
    qHidden: bool = None
    qLinkedTo: list[str] = None
    qPersonalEditionHash_OBSOLETE: str = None
    qRestrictedAccess: bool = None
    qShared: bool = None
    qSheetId: str = None
    qTemporary: bool = None
    qUtcModifyTime: float = None

    def __init__(self_, **kvargs):
        if "qAccessList" in kvargs and kvargs["qAccessList"] is not None:
            self_.qAccessList = kvargs["qAccessList"]
        if "qHidden" in kvargs and kvargs["qHidden"] is not None:
            self_.qHidden = kvargs["qHidden"]
        if "qLinkedTo" in kvargs and kvargs["qLinkedTo"] is not None:
            self_.qLinkedTo = kvargs["qLinkedTo"]
        if (
            "qPersonalEditionHash_OBSOLETE" in kvargs
            and kvargs["qPersonalEditionHash_OBSOLETE"] is not None
        ):
            self_.qPersonalEditionHash_OBSOLETE = kvargs[
                "qPersonalEditionHash_OBSOLETE"
            ]
        if "qRestrictedAccess" in kvargs and kvargs["qRestrictedAccess"] is not None:
            self_.qRestrictedAccess = kvargs["qRestrictedAccess"]
        if "qShared" in kvargs and kvargs["qShared"] is not None:
            self_.qShared = kvargs["qShared"]
        if "qSheetId" in kvargs and kvargs["qSheetId"] is not None:
            self_.qSheetId = kvargs["qSheetId"]
        if "qTemporary" in kvargs and kvargs["qTemporary"] is not None:
            self_.qTemporary = kvargs["qTemporary"]
        if "qUtcModifyTime" in kvargs and kvargs["qUtcModifyTime"] is not None:
            self_.qUtcModifyTime = kvargs["qUtcModifyTime"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAppLayout:
    """
     Qlik Sense Desktop:
    In Qlik Sense Desktop, this structure can contain dynamic properties.

     Qlik Sense Enterprise:
    In Qlik Sense Enterprise, only a few dynamic properties at the app level are persisted.
    The persisted dynamic properties are the following:

    • modifiedDate

    • published

    • publishTime

    • privileges

    • description

    • dynamicColor

    Attributes
    ----------
    qFileName: str
      In Qlik Sense Enterprise, this property corresponds to the app identifier (GUID).
      In Qlik Sense Desktop, this property corresponds to the full path of the app.
    qHasData: bool
      Is set to true if the app contains data following a script reload.
    qHasScript: bool
      Is set to true if a script is defined in the app.
    qIsBDILiveMode: bool
      If set to true, the app is in BDI Direct Query Mode.
    qIsDirectQueryMode: bool
      If set to true, the app is in Direct Query Mode.
    qIsOpenedWithoutData: bool
      If set to true, it means that the app was opened without loading its data.
    qIsSessionApp: bool
      If set to true, the app is a Session App, i.e. not persistent.
    qLastReloadTime: str
      Date and time of the last reload of the app in ISO format.
    qLocaleInfo: LocaleInfo
      Information about the locale.
    qMeta: NxMeta
      Information on publishing and permissions.
    qModified: bool
      Is set to true if the app has been updated since the last save.
    qProhibitBinaryLoad: bool
      If set to true, the persisted app cannot be used in a Binary load statement in Qlik load script.
    qReadOnly: bool
      If set to true, it means that the app is read-only.
    qStateNames: list[str]
      Array of alternate states.
    qThumbnail: StaticContentUrl
      App thumbnail.
    qTitle: str
      Title of the app.
    qUnsupportedFeatures: list[str]
      Array of features not supported by the app.
    qUsage: Literal["ANALYTICS_USAGE", "DATA_PREPARATION_USAGE"]

      One of:

      • ANALYTICS or ANALYTICS_USAGE

      • DATA_PREPARATION or DATA_PREPARATION_USAGE
    """

    qFileName: str = None
    qHasData: bool = None
    qHasScript: bool = None
    qIsBDILiveMode: bool = None
    qIsDirectQueryMode: bool = None
    qIsOpenedWithoutData: bool = None
    qIsSessionApp: bool = None
    qLastReloadTime: str = None
    qLocaleInfo: LocaleInfo = None
    qMeta: NxMeta = None
    qModified: bool = None
    qProhibitBinaryLoad: bool = None
    qReadOnly: bool = None
    qStateNames: list[str] = None
    qThumbnail: StaticContentUrl = None
    qTitle: str = None
    qUnsupportedFeatures: list[str] = None
    qUsage: Literal["ANALYTICS_USAGE", "DATA_PREPARATION_USAGE"] = None

    def __init__(self_, **kvargs):
        if "qFileName" in kvargs and kvargs["qFileName"] is not None:
            self_.qFileName = kvargs["qFileName"]
        if "qHasData" in kvargs and kvargs["qHasData"] is not None:
            self_.qHasData = kvargs["qHasData"]
        if "qHasScript" in kvargs and kvargs["qHasScript"] is not None:
            self_.qHasScript = kvargs["qHasScript"]
        if "qIsBDILiveMode" in kvargs and kvargs["qIsBDILiveMode"] is not None:
            self_.qIsBDILiveMode = kvargs["qIsBDILiveMode"]
        if "qIsDirectQueryMode" in kvargs and kvargs["qIsDirectQueryMode"] is not None:
            self_.qIsDirectQueryMode = kvargs["qIsDirectQueryMode"]
        if (
            "qIsOpenedWithoutData" in kvargs
            and kvargs["qIsOpenedWithoutData"] is not None
        ):
            self_.qIsOpenedWithoutData = kvargs["qIsOpenedWithoutData"]
        if "qIsSessionApp" in kvargs and kvargs["qIsSessionApp"] is not None:
            self_.qIsSessionApp = kvargs["qIsSessionApp"]
        if "qLastReloadTime" in kvargs and kvargs["qLastReloadTime"] is not None:
            self_.qLastReloadTime = kvargs["qLastReloadTime"]
        if "qLocaleInfo" in kvargs and kvargs["qLocaleInfo"] is not None:
            if (
                type(kvargs["qLocaleInfo"]).__name__
                == NxAppLayout.__annotations__["qLocaleInfo"]
            ):
                self_.qLocaleInfo = kvargs["qLocaleInfo"]
            else:
                self_.qLocaleInfo = LocaleInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qLocaleInfo"],
                )
        if "qMeta" in kvargs and kvargs["qMeta"] is not None:
            if type(kvargs["qMeta"]).__name__ == NxAppLayout.__annotations__["qMeta"]:
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeta"],
                )
        if "qModified" in kvargs and kvargs["qModified"] is not None:
            self_.qModified = kvargs["qModified"]
        if (
            "qProhibitBinaryLoad" in kvargs
            and kvargs["qProhibitBinaryLoad"] is not None
        ):
            self_.qProhibitBinaryLoad = kvargs["qProhibitBinaryLoad"]
        if "qReadOnly" in kvargs and kvargs["qReadOnly"] is not None:
            self_.qReadOnly = kvargs["qReadOnly"]
        if "qStateNames" in kvargs and kvargs["qStateNames"] is not None:
            self_.qStateNames = kvargs["qStateNames"]
        if "qThumbnail" in kvargs and kvargs["qThumbnail"] is not None:
            if (
                type(kvargs["qThumbnail"]).__name__
                == NxAppLayout.__annotations__["qThumbnail"]
            ):
                self_.qThumbnail = kvargs["qThumbnail"]
            else:
                self_.qThumbnail = StaticContentUrl(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qThumbnail"],
                )
        if "qTitle" in kvargs and kvargs["qTitle"] is not None:
            self_.qTitle = kvargs["qTitle"]
        if (
            "qUnsupportedFeatures" in kvargs
            and kvargs["qUnsupportedFeatures"] is not None
        ):
            self_.qUnsupportedFeatures = kvargs["qUnsupportedFeatures"]
        if "qUsage" in kvargs and kvargs["qUsage"] is not None:
            self_.qUsage = kvargs["qUsage"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAppProperties:
    """
     Qlik Sense Desktop:
    In Qlik Sense Desktop, this structure can contain dynamic properties.

     Qlik Sense Enterprise:
    In Qlik Sense Enterprise, only a few dynamic properties at the app level are persisted.
    The persisted dynamic properties are the following:

    • modifiedDate

    • published

    • publishTime

    • privileges

    • description

    • dynamicColor

    Attributes
    ----------
    qHasSectionAccess: bool
      If true the app has section access configured.
    qLastReloadTime: str
      Last reload time of the app.
    qMigrationHash: str
      Internal property reserved for app migration.
      Patch version of the app.
      Do not update.
    qSavedInProductVersion: str
      Internal property reserved for app migration.
      The app is saved in this version of the product.
      Do not update.
    qThumbnail: StaticContentUrlDef
      App thumbnail.
    qTitle: str
      App title.
    qUsage: Literal["ANALYTICS_USAGE", "DATA_PREPARATION_USAGE"]
      Indicates whether the app is used for Analytics or DataPreparation

      One of:

      • ANALYTICS or ANALYTICS_USAGE

      • DATA_PREPARATION or DATA_PREPARATION_USAGE
    """

    qHasSectionAccess: bool = None
    qLastReloadTime: str = None
    qMigrationHash: str = None
    qSavedInProductVersion: str = None
    qThumbnail: StaticContentUrlDef = None
    qTitle: str = None
    qUsage: Literal["ANALYTICS_USAGE", "DATA_PREPARATION_USAGE"] = None

    def __init__(self_, **kvargs):
        if "qHasSectionAccess" in kvargs and kvargs["qHasSectionAccess"] is not None:
            self_.qHasSectionAccess = kvargs["qHasSectionAccess"]
        if "qLastReloadTime" in kvargs and kvargs["qLastReloadTime"] is not None:
            self_.qLastReloadTime = kvargs["qLastReloadTime"]
        if "qMigrationHash" in kvargs and kvargs["qMigrationHash"] is not None:
            self_.qMigrationHash = kvargs["qMigrationHash"]
        if (
            "qSavedInProductVersion" in kvargs
            and kvargs["qSavedInProductVersion"] is not None
        ):
            self_.qSavedInProductVersion = kvargs["qSavedInProductVersion"]
        if "qThumbnail" in kvargs and kvargs["qThumbnail"] is not None:
            if (
                type(kvargs["qThumbnail"]).__name__
                == NxAppProperties.__annotations__["qThumbnail"]
            ):
                self_.qThumbnail = kvargs["qThumbnail"]
            else:
                self_.qThumbnail = StaticContentUrlDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qThumbnail"],
                )
        if "qTitle" in kvargs and kvargs["qTitle"] is not None:
            self_.qTitle = kvargs["qTitle"]
        if "qUsage" in kvargs and kvargs["qUsage"] is not None:
            self_.qUsage = kvargs["qUsage"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAttrDimDef:
    """
    Layout for NxAttrDimDef.

    Attributes
    ----------
    qAttribute: bool
      If set to true, this attribute will not affect the number of rows in the cube.
    qDef: str
      Expression or field name.
    qLibraryId: str
      LibraryId for dimension.
    qSortBy: SortCriteria
      Sorting.
    """

    qAttribute: bool = None
    qDef: str = None
    qLibraryId: str = None
    qSortBy: SortCriteria = None

    def __init__(self_, **kvargs):
        if "qAttribute" in kvargs and kvargs["qAttribute"] is not None:
            self_.qAttribute = kvargs["qAttribute"]
        if "qDef" in kvargs and kvargs["qDef"] is not None:
            self_.qDef = kvargs["qDef"]
        if "qLibraryId" in kvargs and kvargs["qLibraryId"] is not None:
            self_.qLibraryId = kvargs["qLibraryId"]
        if "qSortBy" in kvargs and kvargs["qSortBy"] is not None:
            if (
                type(kvargs["qSortBy"]).__name__
                == NxAttrDimDef.__annotations__["qSortBy"]
            ):
                self_.qSortBy = kvargs["qSortBy"]
            else:
                self_.qSortBy = SortCriteria(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qSortBy"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAttrDimInfo:
    """
    Layout for NxAttrDimDef.

    Attributes
    ----------
    qCardinal: int
      Cardinality of the attribute expression.
    qError: NxValidationError
      Validation error.
    qFallbackTitle: str
      The title for the attribute dimension.
    qIsCalculated: bool
      True if this is a calculated dimension.
    qLocked: bool
      The Locked value of the dimension.
    qSize: Size
      Number of rows.
    """

    qCardinal: int = None
    qError: NxValidationError = None
    qFallbackTitle: str = None
    qIsCalculated: bool = None
    qLocked: bool = None
    qSize: Size = None

    def __init__(self_, **kvargs):
        if "qCardinal" in kvargs and kvargs["qCardinal"] is not None:
            self_.qCardinal = kvargs["qCardinal"]
        if "qError" in kvargs and kvargs["qError"] is not None:
            if (
                type(kvargs["qError"]).__name__
                == NxAttrDimInfo.__annotations__["qError"]
            ):
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qError"],
                )
        if "qFallbackTitle" in kvargs and kvargs["qFallbackTitle"] is not None:
            self_.qFallbackTitle = kvargs["qFallbackTitle"]
        if "qIsCalculated" in kvargs and kvargs["qIsCalculated"] is not None:
            self_.qIsCalculated = kvargs["qIsCalculated"]
        if "qLocked" in kvargs and kvargs["qLocked"] is not None:
            self_.qLocked = kvargs["qLocked"]
        if "qSize" in kvargs and kvargs["qSize"] is not None:
            if type(kvargs["qSize"]).__name__ == NxAttrDimInfo.__annotations__["qSize"]:
                self_.qSize = kvargs["qSize"]
            else:
                self_.qSize = Size(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qSize"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAttrExprDef:
    """

    Attributes
    ----------
    qAttribute: bool
      If set to true, this measure will not affect the number of rows in the cube.
    qExpression: str
      Definition of the attribute expression.
      Example: "Max(OrderID)"
    qLabel: str
      Label of the attribute expression.
    qLabelExpression: str
      Optional expression used for dynamic label.
    qLibraryId: str
      Definition of the attribute expression stored in the library.
      Example: "MyGenericMeasure"
    qNumFormat: FieldAttributes
      Format of the field.
      This parameter is optional.
    """

    qAttribute: bool = None
    qExpression: str = None
    qLabel: str = None
    qLabelExpression: str = None
    qLibraryId: str = None
    qNumFormat: FieldAttributes = None

    def __init__(self_, **kvargs):
        if "qAttribute" in kvargs and kvargs["qAttribute"] is not None:
            self_.qAttribute = kvargs["qAttribute"]
        if "qExpression" in kvargs and kvargs["qExpression"] is not None:
            self_.qExpression = kvargs["qExpression"]
        if "qLabel" in kvargs and kvargs["qLabel"] is not None:
            self_.qLabel = kvargs["qLabel"]
        if "qLabelExpression" in kvargs and kvargs["qLabelExpression"] is not None:
            self_.qLabelExpression = kvargs["qLabelExpression"]
        if "qLibraryId" in kvargs and kvargs["qLibraryId"] is not None:
            self_.qLibraryId = kvargs["qLibraryId"]
        if "qNumFormat" in kvargs and kvargs["qNumFormat"] is not None:
            if (
                type(kvargs["qNumFormat"]).__name__
                == NxAttrExprDef.__annotations__["qNumFormat"]
            ):
                self_.qNumFormat = kvargs["qNumFormat"]
            else:
                self_.qNumFormat = FieldAttributes(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qNumFormat"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAttrExprInfo:
    """
    Layout for NxAttrExprDef.

    Attributes
    ----------
    qFallbackTitle: str
    qIsAutoFormat: bool
      This parameter is set to true if qNumFormat is set to U (unknown). The engine guesses the type of the field based on the field's expression.
    qMax: float
      Maximum value.
    qMaxText: str
      String version of the maximum Value.
    qMin: float
      Minimum value.
    qMinText: str
      String version of the minimum Value.
    qNumFormat: FieldAttributes
      Format of the field.
      This parameter is optional.
    """

    qFallbackTitle: str = None
    qIsAutoFormat: bool = None
    qMax: float = None
    qMaxText: str = None
    qMin: float = None
    qMinText: str = None
    qNumFormat: FieldAttributes = None

    def __init__(self_, **kvargs):
        if "qFallbackTitle" in kvargs and kvargs["qFallbackTitle"] is not None:
            self_.qFallbackTitle = kvargs["qFallbackTitle"]
        if "qIsAutoFormat" in kvargs and kvargs["qIsAutoFormat"] is not None:
            self_.qIsAutoFormat = kvargs["qIsAutoFormat"]
        if "qMax" in kvargs and kvargs["qMax"] is not None:
            self_.qMax = kvargs["qMax"]
        if "qMaxText" in kvargs and kvargs["qMaxText"] is not None:
            self_.qMaxText = kvargs["qMaxText"]
        if "qMin" in kvargs and kvargs["qMin"] is not None:
            self_.qMin = kvargs["qMin"]
        if "qMinText" in kvargs and kvargs["qMinText"] is not None:
            self_.qMinText = kvargs["qMinText"]
        if "qNumFormat" in kvargs and kvargs["qNumFormat"] is not None:
            if (
                type(kvargs["qNumFormat"]).__name__
                == NxAttrExprInfo.__annotations__["qNumFormat"]
            ):
                self_.qNumFormat = kvargs["qNumFormat"]
            else:
                self_.qNumFormat = FieldAttributes(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qNumFormat"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAttributeDimValues:
    """

    Attributes
    ----------
    qValues: list[NxSimpleDimValue]
      List of values.
    """

    qValues: list[NxSimpleDimValue] = None

    def __init__(self_, **kvargs):
        if "qValues" in kvargs and kvargs["qValues"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxAttributeDimValues.__annotations__["qValues"]
                for e in kvargs["qValues"]
            ):
                self_.qValues = kvargs["qValues"]
            else:
                self_.qValues = [
                    NxSimpleDimValue(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qValues"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAttributeExpressionValues:
    """

    Attributes
    ----------
    qValues: list[NxSimpleValue]
      List of attribute expressions values.
    """

    qValues: list[NxSimpleValue] = None

    def __init__(self_, **kvargs):
        if "qValues" in kvargs and kvargs["qValues"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxAttributeExpressionValues.__annotations__["qValues"]
                for e in kvargs["qValues"]
            ):
                self_.qValues = kvargs["qValues"]
            else:
                self_.qValues = [
                    NxSimpleValue(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qValues"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAutoSortByStateDef:
    """

    Attributes
    ----------
    qDisplayNumberOfRows: int
      This parameter applies to list objects.
      If the total number of values in the list object is greater than the value set in qDisplayNumberOfRows , the selected lines are promoted at the top of the list object.
      If qDisplayNumberOfRows is set to a negative value or to 0, the sort by state is disabled.
    """

    qDisplayNumberOfRows: int = None

    def __init__(self_, **kvargs):
        if (
            "qDisplayNumberOfRows" in kvargs
            and kvargs["qDisplayNumberOfRows"] is not None
        ):
            self_.qDisplayNumberOfRows = kvargs["qDisplayNumberOfRows"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAxisData:
    """

    Attributes
    ----------
    qAxis: list[NxAxisTicks]
      List of axis data.
    """

    qAxis: list[NxAxisTicks] = None

    def __init__(self_, **kvargs):
        if "qAxis" in kvargs and kvargs["qAxis"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NxAxisData.__annotations__["qAxis"]
                for e in kvargs["qAxis"]
            ):
                self_.qAxis = kvargs["qAxis"]
            else:
                self_.qAxis = [
                    NxAxisTicks(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qAxis"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxAxisTicks:
    """

    Attributes
    ----------
    qName: str
      Name of the derived definition.
    qTags: list[str]
      List of tags.
    qTicks: list[NxTickCell]
      List of ticks.
    """

    qName: str = None
    qTags: list[str] = None
    qTicks: list[NxTickCell] = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qTags" in kvargs and kvargs["qTags"] is not None:
            self_.qTags = kvargs["qTags"]
        if "qTicks" in kvargs and kvargs["qTicks"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NxAxisTicks.__annotations__["qTicks"]
                for e in kvargs["qTicks"]
            ):
                self_.qTicks = kvargs["qTicks"]
            else:
                self_.qTicks = [
                    NxTickCell(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qTicks"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxBookmark:
    """

    Attributes
    ----------
    qPatches: list[NxPatches]
      Softpatches to be applied with this bookmark.
    qStateData: list[AlternateStateData]
      List of selections for each state.
    qUtcModifyTime: float
      Time when the bookmark was created.
    qVariableItems: list[BookmarkVariableItem]
      List of the variables in the app at the time the bookmark was created.
    """

    qPatches: list[NxPatches] = None
    qStateData: list[AlternateStateData] = None
    qUtcModifyTime: float = None
    qVariableItems: list[BookmarkVariableItem] = None

    def __init__(self_, **kvargs):
        if "qPatches" in kvargs and kvargs["qPatches"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NxBookmark.__annotations__["qPatches"]
                for e in kvargs["qPatches"]
            ):
                self_.qPatches = kvargs["qPatches"]
            else:
                self_.qPatches = [
                    NxPatches(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qPatches"]
                ]
        if "qStateData" in kvargs and kvargs["qStateData"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NxBookmark.__annotations__["qStateData"]
                for e in kvargs["qStateData"]
            ):
                self_.qStateData = kvargs["qStateData"]
            else:
                self_.qStateData = [
                    AlternateStateData(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qStateData"]
                ]
        if "qUtcModifyTime" in kvargs and kvargs["qUtcModifyTime"] is not None:
            self_.qUtcModifyTime = kvargs["qUtcModifyTime"]
        if "qVariableItems" in kvargs and kvargs["qVariableItems"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxBookmark.__annotations__["qVariableItems"]
                for e in kvargs["qVariableItems"]
            ):
                self_.qVariableItems = kvargs["qVariableItems"]
            else:
                self_.qVariableItems = [
                    BookmarkVariableItem(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qVariableItems"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxCalcCond:
    """

    Attributes
    ----------
    qCond: ValueExpr
      Condition for calculating an hypercube, dimension or measure.
    qMsg: StringExpr
      Evaluated if Cond is not fullfilled.
    """

    qCond: ValueExpr = None
    qMsg: StringExpr = None

    def __init__(self_, **kvargs):
        if "qCond" in kvargs and kvargs["qCond"] is not None:
            if type(kvargs["qCond"]).__name__ == NxCalcCond.__annotations__["qCond"]:
                self_.qCond = kvargs["qCond"]
            else:
                self_.qCond = ValueExpr(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qCond"],
                )
        if "qMsg" in kvargs and kvargs["qMsg"] is not None:
            if type(kvargs["qMsg"]).__name__ == NxCalcCond.__annotations__["qMsg"]:
                self_.qMsg = kvargs["qMsg"]
            else:
                self_.qMsg = StringExpr(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMsg"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxCardinalities:
    """

    Attributes
    ----------
    qAllValuesCardinal: int
      Number of distinct values when paging for AllValues in a Tree Structure.
      Default is -1 if not part of a Tree structure.
    qCardinal: int
      Number of distinct field values.
    qHypercubeCardinal: int
      Number of distinct hypercube values.
    """

    qAllValuesCardinal: int = -1
    qCardinal: int = None
    qHypercubeCardinal: int = None

    def __init__(self_, **kvargs):
        if "qAllValuesCardinal" in kvargs and kvargs["qAllValuesCardinal"] is not None:
            self_.qAllValuesCardinal = kvargs["qAllValuesCardinal"]
        if "qCardinal" in kvargs and kvargs["qCardinal"] is not None:
            self_.qCardinal = kvargs["qCardinal"]
        if "qHypercubeCardinal" in kvargs and kvargs["qHypercubeCardinal"] is not None:
            self_.qHypercubeCardinal = kvargs["qHypercubeCardinal"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxCell:
    """

    Attributes
    ----------
    qAttrDims: NxAttributeDimValues
      Attribute dimensions values.
    qAttrExps: NxAttributeExpressionValues
      Attribute expression values.
    qElemNumber: int
      Rank number of the value, starting from 0.
      If the element number is a negative number, it means that the returned value is not an element number.
      You can get the following negative values:

      • -1: the cell is a Total cell. It shows a total.

      • -2: the cell is a Null cell.

      • -3: the cell belongs to the group Others .

      • -4: the cell is empty. Applies to pivot tables.
    qFrequency: str
      Frequency of the value.
      This parameter is optional.
    qHighlightRanges: NxHighlightRanges
      Search hits.
      The search hits are highlighted.
      This parameter is optional.
    qInExtRow: bool
    qIsEmpty: bool
      Is set to true , if qText and qNum are empty.
      This parameter is optional. The default value is false .
    qIsNull: bool
      Is set to true if the value is Null.
    qIsOtherCell: bool
      Is set to true if the cell belongs to the group Others .
      Dimension values can be set as Others depending on what has been defined in OtherTotalSpecProp .
      This parameter is optional. The default value is false .
      Not applicable to list objects.
    qIsTotalCell: bool
      Is set to true if a total is displayed in the cell.
      This parameter is optional. The default value is false .
      Not applicable to list objects.
    qMiniChart: NxMiniChartData
    qNum: float
      A value.
      This parameter is optional.
    qState: Literal["LOCKED", "SELECTED", "OPTION", "DESELECTED", "ALTERNATIVE", "EXCLUDED", "EXCL_SELECTED", "EXCL_LOCKED", "NSTATES"]
      State of the value.
      The default state for a measure is L.

      One of:

      • L or LOCKED

      • S or SELECTED

      • O or OPTION

      • D or DESELECTED

      • A or ALTERNATIVE

      • X or EXCLUDED

      • XS or EXCL_SELECTED

      • XL or EXCL_LOCKED

      • NSTATES
    qText: str
      Some text.
      This parameter is optional.
    """

    qAttrDims: NxAttributeDimValues = None
    qAttrExps: NxAttributeExpressionValues = None
    qElemNumber: int = None
    qFrequency: str = None
    qHighlightRanges: NxHighlightRanges = None
    qInExtRow: bool = None
    qIsEmpty: bool = None
    qIsNull: bool = None
    qIsOtherCell: bool = None
    qIsTotalCell: bool = None
    qMiniChart: NxMiniChartData = None
    qNum: float = None
    qState: Literal[
        "LOCKED",
        "SELECTED",
        "OPTION",
        "DESELECTED",
        "ALTERNATIVE",
        "EXCLUDED",
        "EXCL_SELECTED",
        "EXCL_LOCKED",
        "NSTATES",
    ] = None
    qText: str = None

    def __init__(self_, **kvargs):
        if "qAttrDims" in kvargs and kvargs["qAttrDims"] is not None:
            if (
                type(kvargs["qAttrDims"]).__name__
                == NxCell.__annotations__["qAttrDims"]
            ):
                self_.qAttrDims = kvargs["qAttrDims"]
            else:
                self_.qAttrDims = NxAttributeDimValues(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qAttrDims"],
                )
        if "qAttrExps" in kvargs and kvargs["qAttrExps"] is not None:
            if (
                type(kvargs["qAttrExps"]).__name__
                == NxCell.__annotations__["qAttrExps"]
            ):
                self_.qAttrExps = kvargs["qAttrExps"]
            else:
                self_.qAttrExps = NxAttributeExpressionValues(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qAttrExps"],
                )
        if "qElemNumber" in kvargs and kvargs["qElemNumber"] is not None:
            self_.qElemNumber = kvargs["qElemNumber"]
        if "qFrequency" in kvargs and kvargs["qFrequency"] is not None:
            self_.qFrequency = kvargs["qFrequency"]
        if "qHighlightRanges" in kvargs and kvargs["qHighlightRanges"] is not None:
            if (
                type(kvargs["qHighlightRanges"]).__name__
                == NxCell.__annotations__["qHighlightRanges"]
            ):
                self_.qHighlightRanges = kvargs["qHighlightRanges"]
            else:
                self_.qHighlightRanges = NxHighlightRanges(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qHighlightRanges"],
                )
        if "qInExtRow" in kvargs and kvargs["qInExtRow"] is not None:
            self_.qInExtRow = kvargs["qInExtRow"]
        if "qIsEmpty" in kvargs and kvargs["qIsEmpty"] is not None:
            self_.qIsEmpty = kvargs["qIsEmpty"]
        if "qIsNull" in kvargs and kvargs["qIsNull"] is not None:
            self_.qIsNull = kvargs["qIsNull"]
        if "qIsOtherCell" in kvargs and kvargs["qIsOtherCell"] is not None:
            self_.qIsOtherCell = kvargs["qIsOtherCell"]
        if "qIsTotalCell" in kvargs and kvargs["qIsTotalCell"] is not None:
            self_.qIsTotalCell = kvargs["qIsTotalCell"]
        if "qMiniChart" in kvargs and kvargs["qMiniChart"] is not None:
            if (
                type(kvargs["qMiniChart"]).__name__
                == NxCell.__annotations__["qMiniChart"]
            ):
                self_.qMiniChart = kvargs["qMiniChart"]
            else:
                self_.qMiniChart = NxMiniChartData(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMiniChart"],
                )
        if "qNum" in kvargs and kvargs["qNum"] is not None:
            self_.qNum = kvargs["qNum"]
        if "qState" in kvargs and kvargs["qState"] is not None:
            self_.qState = kvargs["qState"]
        if "qText" in kvargs and kvargs["qText"] is not None:
            self_.qText = kvargs["qText"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxCellPosition:
    """

    Attributes
    ----------
    qx: int
      Position of the cell on the x-axis.
    qy: int
      Position of the cell on the y-axis.
    """

    qx: int = None
    qy: int = None

    def __init__(self_, **kvargs):
        if "qx" in kvargs and kvargs["qx"] is not None:
            self_.qx = kvargs["qx"]
        if "qy" in kvargs and kvargs["qy"] is not None:
            self_.qy = kvargs["qy"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxCellRows(List["NxCell"]):
    """

    Attributes
    ----------
    """

    def __init__(self_, elements):
        for e in elements:
            self_.append(NxCell(**e))


@dataclass
class NxContainerEntry:
    """

    Attributes
    ----------
    qData: JsonObject
      Set of data.
    qInfo: NxInfo
      Information about the object.
    qMeta: NxMeta
      Information on publishing and permissions.
    """

    qData: JsonObject = None
    qInfo: NxInfo = None
    qMeta: NxMeta = None

    def __init__(self_, **kvargs):
        if "qData" in kvargs and kvargs["qData"] is not None:
            if (
                type(kvargs["qData"]).__name__
                == NxContainerEntry.__annotations__["qData"]
            ):
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qData"],
                )
        if "qInfo" in kvargs and kvargs["qInfo"] is not None:
            if (
                type(kvargs["qInfo"]).__name__
                == NxContainerEntry.__annotations__["qInfo"]
            ):
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qInfo"],
                )
        if "qMeta" in kvargs and kvargs["qMeta"] is not None:
            if (
                type(kvargs["qMeta"]).__name__
                == NxContainerEntry.__annotations__["qMeta"]
            ):
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeta"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxContinuousDataOptions:
    """

    Attributes
    ----------
    qEnd: float
      End value.
    qMaxNbrTicks: int
      Maximum number of ticks.
    qMaxNumberLines: int
      Maximum number of lines.
    qNbrPoints: int
      Number of bins for binning.
    qStart: float
      Start value.
    """

    qEnd: float = None
    qMaxNbrTicks: int = None
    qMaxNumberLines: int = -1
    qNbrPoints: int = None
    qStart: float = None

    def __init__(self_, **kvargs):
        if "qEnd" in kvargs and kvargs["qEnd"] is not None:
            self_.qEnd = kvargs["qEnd"]
        if "qMaxNbrTicks" in kvargs and kvargs["qMaxNbrTicks"] is not None:
            self_.qMaxNbrTicks = kvargs["qMaxNbrTicks"]
        if "qMaxNumberLines" in kvargs and kvargs["qMaxNumberLines"] is not None:
            self_.qMaxNumberLines = kvargs["qMaxNumberLines"]
        if "qNbrPoints" in kvargs and kvargs["qNbrPoints"] is not None:
            self_.qNbrPoints = kvargs["qNbrPoints"]
        if "qStart" in kvargs and kvargs["qStart"] is not None:
            self_.qStart = kvargs["qStart"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxContinuousMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxContinuousRangeSelectInfo:
    """

    Attributes
    ----------
    qDimIx: int
      Dimension index.
    qRange: Range
      Range information.
    """

    qDimIx: int = None
    qRange: Range = None

    def __init__(self_, **kvargs):
        if "qDimIx" in kvargs and kvargs["qDimIx"] is not None:
            self_.qDimIx = kvargs["qDimIx"]
        if "qRange" in kvargs and kvargs["qRange"] is not None:
            if (
                type(kvargs["qRange"]).__name__
                == NxContinuousRangeSelectInfo.__annotations__["qRange"]
            ):
                self_.qRange = kvargs["qRange"]
            else:
                self_.qRange = Range(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qRange"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxCurrentSelectionItem:
    """

    Attributes
    ----------
    qField: str
      Name of the field that is selected.
    qIsHidden: bool
      Optional parameter. Indicates if the selection is to be hidden in the Selections bar.
      Is set to true if the current selection is hidden.
    qIsNum: bool
      This parameter is displayed if its value is true.
      Is set to true if the field is a numeric.
      This parameter is optional.
    qLocked: bool
      This parameter is displayed if its value is true.
      Is set to true if the field is locked.
      This parameter is optional.
    qNotSelectedFieldSelectionInfo: list[NxFieldSelectionInfo]
      Information about the fields that are not selected.
    qOneAndOnlyOne: bool
      This parameter is displayed if its value is true.
      Property that is set to a field. Is set to true if the field cannot be unselected.
      This parameter is optional.
    qRangeInfo: list[RangeSelectInfo]
      Information about the range of selected values.
      Is empty if there is no range of selected values.
    qReadableName: str
      Label that, if defined, is displayed in current selections instead of the actual expression.
    qSelected: str
      Values that are selected.
    qSelectedCount: int
      Number of values that are selected.
    qSelectedFieldSelectionInfo: list[NxFieldSelectionInfo]
      Information about the fields that are selected.
    qSelectionThreshold: int
      Maximum values to show in the current selections.
      The default value is 6.
    qSortIndex: int
      Sort index of the field. Indexing starts from 0.
    qStateCounts: NxStateCounts
      Number of values in a particular state.
    qTextSearch: str
      Text that was used for the search. This parameter is filled when searching for a value and selecting it.
      This parameter is optional.
    qTotal: int
      Number of values in the field.
    """

    qField: str = None
    qIsHidden: bool = None
    qIsNum: bool = None
    qLocked: bool = None
    qNotSelectedFieldSelectionInfo: list[NxFieldSelectionInfo] = None
    qOneAndOnlyOne: bool = None
    qRangeInfo: list[RangeSelectInfo] = None
    qReadableName: str = None
    qSelected: str = None
    qSelectedCount: int = None
    qSelectedFieldSelectionInfo: list[NxFieldSelectionInfo] = None
    qSelectionThreshold: int = None
    qSortIndex: int = None
    qStateCounts: NxStateCounts = None
    qTextSearch: str = None
    qTotal: int = None

    def __init__(self_, **kvargs):
        if "qField" in kvargs and kvargs["qField"] is not None:
            self_.qField = kvargs["qField"]
        if "qIsHidden" in kvargs and kvargs["qIsHidden"] is not None:
            self_.qIsHidden = kvargs["qIsHidden"]
        if "qIsNum" in kvargs and kvargs["qIsNum"] is not None:
            self_.qIsNum = kvargs["qIsNum"]
        if "qLocked" in kvargs and kvargs["qLocked"] is not None:
            self_.qLocked = kvargs["qLocked"]
        if (
            "qNotSelectedFieldSelectionInfo" in kvargs
            and kvargs["qNotSelectedFieldSelectionInfo"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == NxCurrentSelectionItem.__annotations__[
                    "qNotSelectedFieldSelectionInfo"
                ]
                for e in kvargs["qNotSelectedFieldSelectionInfo"]
            ):
                self_.qNotSelectedFieldSelectionInfo = kvargs[
                    "qNotSelectedFieldSelectionInfo"
                ]
            else:
                self_.qNotSelectedFieldSelectionInfo = [
                    NxFieldSelectionInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qNotSelectedFieldSelectionInfo"]
                ]
        if "qOneAndOnlyOne" in kvargs and kvargs["qOneAndOnlyOne"] is not None:
            self_.qOneAndOnlyOne = kvargs["qOneAndOnlyOne"]
        if "qRangeInfo" in kvargs and kvargs["qRangeInfo"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxCurrentSelectionItem.__annotations__["qRangeInfo"]
                for e in kvargs["qRangeInfo"]
            ):
                self_.qRangeInfo = kvargs["qRangeInfo"]
            else:
                self_.qRangeInfo = [
                    RangeSelectInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qRangeInfo"]
                ]
        if "qReadableName" in kvargs and kvargs["qReadableName"] is not None:
            self_.qReadableName = kvargs["qReadableName"]
        if "qSelected" in kvargs and kvargs["qSelected"] is not None:
            self_.qSelected = kvargs["qSelected"]
        if "qSelectedCount" in kvargs and kvargs["qSelectedCount"] is not None:
            self_.qSelectedCount = kvargs["qSelectedCount"]
        if (
            "qSelectedFieldSelectionInfo" in kvargs
            and kvargs["qSelectedFieldSelectionInfo"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == NxCurrentSelectionItem.__annotations__["qSelectedFieldSelectionInfo"]
                for e in kvargs["qSelectedFieldSelectionInfo"]
            ):
                self_.qSelectedFieldSelectionInfo = kvargs[
                    "qSelectedFieldSelectionInfo"
                ]
            else:
                self_.qSelectedFieldSelectionInfo = [
                    NxFieldSelectionInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qSelectedFieldSelectionInfo"]
                ]
        if (
            "qSelectionThreshold" in kvargs
            and kvargs["qSelectionThreshold"] is not None
        ):
            self_.qSelectionThreshold = kvargs["qSelectionThreshold"]
        if "qSortIndex" in kvargs and kvargs["qSortIndex"] is not None:
            self_.qSortIndex = kvargs["qSortIndex"]
        if "qStateCounts" in kvargs and kvargs["qStateCounts"] is not None:
            if (
                type(kvargs["qStateCounts"]).__name__
                == NxCurrentSelectionItem.__annotations__["qStateCounts"]
            ):
                self_.qStateCounts = kvargs["qStateCounts"]
            else:
                self_.qStateCounts = NxStateCounts(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qStateCounts"],
                )
        if "qTextSearch" in kvargs and kvargs["qTextSearch"] is not None:
            self_.qTextSearch = kvargs["qTextSearch"]
        if "qTotal" in kvargs and kvargs["qTotal"] is not None:
            self_.qTotal = kvargs["qTotal"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDataAreaPage:
    """

    Attributes
    ----------
    qHeight: float
      Height of the page.
      The difference between qTop and qHeight gives the lowest possible value of the second measure (the measure on the y-axis).
    qLeft: float
      Position from the left.
      Corresponds to the lowest possible value of the first measure (the measure on the x-axis).
    qTop: float
      Position from the top.
      Corresponds to the highest possible value of the second measure (the measure on the y-axis).
    qWidth: float
      Width of the page.
      Corresponds to the highest possible value of the first measure (the measure on the x-axis).
    """

    qHeight: float = None
    qLeft: float = None
    qTop: float = None
    qWidth: float = None

    def __init__(self_, **kvargs):
        if "qHeight" in kvargs and kvargs["qHeight"] is not None:
            self_.qHeight = kvargs["qHeight"]
        if "qLeft" in kvargs and kvargs["qLeft"] is not None:
            self_.qLeft = kvargs["qLeft"]
        if "qTop" in kvargs and kvargs["qTop"] is not None:
            self_.qTop = kvargs["qTop"]
        if "qWidth" in kvargs and kvargs["qWidth"] is not None:
            self_.qWidth = kvargs["qWidth"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDataPage:
    """

    Attributes
    ----------
    qArea: Rect
      Size and offset of the data in the matrix.
    qIsReduced: bool
      Is set to true, if the data have been reduced.
      The default value is false.
    qMatrix: list[NxCellRows]
      Array of data.
    qTails: list[NxGroupTail]
      Array of tails.
      Is used for hypercube objects with multiple dimensions. It might happen that due to the window size some elements in a group cannot be displayed in the same page as the other elements of the group. Elements of a group of dimensions can be part of the previous or the next tail.
      If there is no tail, the array is empty [ ] .
    """

    qArea: Rect = None
    qIsReduced: bool = None
    qMatrix: list[NxCellRows] = None
    qTails: list[NxGroupTail] = None

    def __init__(self_, **kvargs):
        if "qArea" in kvargs and kvargs["qArea"] is not None:
            if type(kvargs["qArea"]).__name__ == NxDataPage.__annotations__["qArea"]:
                self_.qArea = kvargs["qArea"]
            else:
                self_.qArea = Rect(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qArea"],
                )
        if "qIsReduced" in kvargs and kvargs["qIsReduced"] is not None:
            self_.qIsReduced = kvargs["qIsReduced"]
        if "qMatrix" in kvargs and kvargs["qMatrix"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NxDataPage.__annotations__["qMatrix"]
                for e in kvargs["qMatrix"]
            ):
                self_.qMatrix = kvargs["qMatrix"]
            else:
                self_.qMatrix = [NxCellRows(e) for e in kvargs["qMatrix"]]
        if "qTails" in kvargs and kvargs["qTails"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NxDataPage.__annotations__["qTails"]
                for e in kvargs["qTails"]
            ):
                self_.qTails = kvargs["qTails"]
            else:
                self_.qTails = [
                    NxGroupTail(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qTails"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDataReductionMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDerivedField:
    """

    Attributes
    ----------
    qExpr: str
      Expression of the derived field.
      Example:
      If qName is OrderDate.MyDefinition.Year , the expression is as follows:
      =${Mydefinition(OrderDate).Year}
    qId: str
      Identifier of the derived field.
      The identifier is unique.
    qMethod: str
      Method name associated to the derived field.
    qName: str
      Combination of field name, definition and method.
      Example:
      OrderDate.MyDefinition.Year
    qTags: list[str]
      List of tags.
    """

    qExpr: str = None
    qId: str = None
    qMethod: str = None
    qName: str = None
    qTags: list[str] = None

    def __init__(self_, **kvargs):
        if "qExpr" in kvargs and kvargs["qExpr"] is not None:
            self_.qExpr = kvargs["qExpr"]
        if "qId" in kvargs and kvargs["qId"] is not None:
            self_.qId = kvargs["qId"]
        if "qMethod" in kvargs and kvargs["qMethod"] is not None:
            self_.qMethod = kvargs["qMethod"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qTags" in kvargs and kvargs["qTags"] is not None:
            self_.qTags = kvargs["qTags"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDerivedFieldDescriptionList:
    """

    Attributes
    ----------
    qDerivedFieldLists: list[NxDerivedFieldsData]
      Information about the derived fields.
    """

    qDerivedFieldLists: list[NxDerivedFieldsData] = None

    def __init__(self_, **kvargs):
        if "qDerivedFieldLists" in kvargs and kvargs["qDerivedFieldLists"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxDerivedFieldDescriptionList.__annotations__["qDerivedFieldLists"]
                for e in kvargs["qDerivedFieldLists"]
            ):
                self_.qDerivedFieldLists = kvargs["qDerivedFieldLists"]
            else:
                self_.qDerivedFieldLists = [
                    NxDerivedFieldsData(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qDerivedFieldLists"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDerivedFieldsData:
    """

    Attributes
    ----------
    qDerivedDefinitionName: str
      Name of the derived definition.
    qFieldDefs: list[NxDerivedField]
      List of the derived fields.
    qGroupDefs: list[NxDerivedGroup]
      List of the derived groups.
    qTags: list[str]
      List of tags on the derived fields.
    """

    qDerivedDefinitionName: str = None
    qFieldDefs: list[NxDerivedField] = None
    qGroupDefs: list[NxDerivedGroup] = None
    qTags: list[str] = None

    def __init__(self_, **kvargs):
        if (
            "qDerivedDefinitionName" in kvargs
            and kvargs["qDerivedDefinitionName"] is not None
        ):
            self_.qDerivedDefinitionName = kvargs["qDerivedDefinitionName"]
        if "qFieldDefs" in kvargs and kvargs["qFieldDefs"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxDerivedFieldsData.__annotations__["qFieldDefs"]
                for e in kvargs["qFieldDefs"]
            ):
                self_.qFieldDefs = kvargs["qFieldDefs"]
            else:
                self_.qFieldDefs = [
                    NxDerivedField(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qFieldDefs"]
                ]
        if "qGroupDefs" in kvargs and kvargs["qGroupDefs"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxDerivedFieldsData.__annotations__["qGroupDefs"]
                for e in kvargs["qGroupDefs"]
            ):
                self_.qGroupDefs = kvargs["qGroupDefs"]
            else:
                self_.qGroupDefs = [
                    NxDerivedGroup(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qGroupDefs"]
                ]
        if "qTags" in kvargs and kvargs["qTags"] is not None:
            self_.qTags = kvargs["qTags"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDerivedGroup:
    """

    Attributes
    ----------
    qFieldDefs: list[str]
      List of the derived fields in the group.
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"]
      Grouping type.
      The grouping should be either H or C (Grouping is mandatory for derived definitions).
      The parameter is mandatory.

      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qId: str
      Identifier of the group.
    qName: str
      Name of the derived group.
    """

    qFieldDefs: list[str] = None
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"] = None
    qId: str = None
    qName: str = None

    def __init__(self_, **kvargs):
        if "qFieldDefs" in kvargs and kvargs["qFieldDefs"] is not None:
            self_.qFieldDefs = kvargs["qFieldDefs"]
        if "qGrouping" in kvargs and kvargs["qGrouping"] is not None:
            self_.qGrouping = kvargs["qGrouping"]
        if "qId" in kvargs and kvargs["qId"] is not None:
            self_.qId = kvargs["qId"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDimCellType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDimension:
    """
    Either qDef or qLibraryId must be set, but not both.  If the dimension is set in the hypercube and not in the library, this dimension cannot be shared with other objects. A dimension that is set in the library can be used by many objects.

    Attributes
    ----------
    qAttributeDimensions: list[NxAttrDimDef]
      List of attribute dimensions.
    qAttributeExpressions: list[NxAttrExprDef]
      List of attribute expressions.
    qCalcCond: ValueExpr
      Specifies a calculation condition, which must be fulfilled for the dimension to be calculated.
      If the calculation condition is not met, the dimension is excluded from the calculation.
      By default, there is no calculation condition.
      This property is optional.
    qCalcCondition: NxCalcCond
      Specifies a calculation condition object.
      If CalcCondition.Cond is not fulfilled, the dimension is excluded from the calculation and CalcCondition.Msg is evaluated.
      By default, there is no calculation condition.
      This property is optional.
    qDef: NxInlineDimensionDef
      Refers to a dimension stored in the hypercube.
    qIncludeElemValue: bool
    qLibraryId: str
      Refers to a dimension stored in the library.
    qNullSuppression: bool
      If set to true, no null values are returned.
    qOtherLabel: StringExpr
      This property is used when some dimension limits are set.
      Label of the Others group. The default label is Others .
      Example:
      "qOtherLabel":"= <label>"
      or
      "qOtherLabel":{"qExpr":"= <label>"}
      Where:

      • < label > is the label of the Others group.
    qOtherTotalSpec: OtherTotalSpecProp
      Sets the dimension limits. Each dimension of a hypercube is configured separately.
      Defines if some values (grouped as Others ) should be grouped together in the visualization.
      For example in a pie chart all values lower than 200 could be grouped together.
    qShowAll: bool
      If set to true, all dimension values are shown.
    qShowTotal: bool
    qTotalLabel: StringExpr
      If this property is set, the total of the calculated values is returned.
      The default label is Total .
      Example:
      "qTotalLabel":"= <label>"
      or
      "qTotalLabel":{"qExpr":"= <label>"}
      Where:

      • < label > is the label of the Total group.
    """

    qAttributeDimensions: list[NxAttrDimDef] = None
    qAttributeExpressions: list[NxAttrExprDef] = None
    qCalcCond: ValueExpr = None
    qCalcCondition: NxCalcCond = None
    qDef: NxInlineDimensionDef = None
    qIncludeElemValue: bool = None
    qLibraryId: str = None
    qNullSuppression: bool = None
    qOtherLabel: StringExpr = None
    qOtherTotalSpec: OtherTotalSpecProp = None
    qShowAll: bool = None
    qShowTotal: bool = None
    qTotalLabel: StringExpr = None

    def __init__(self_, **kvargs):
        if (
            "qAttributeDimensions" in kvargs
            and kvargs["qAttributeDimensions"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == NxDimension.__annotations__["qAttributeDimensions"]
                for e in kvargs["qAttributeDimensions"]
            ):
                self_.qAttributeDimensions = kvargs["qAttributeDimensions"]
            else:
                self_.qAttributeDimensions = [
                    NxAttrDimDef(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qAttributeDimensions"]
                ]
        if (
            "qAttributeExpressions" in kvargs
            and kvargs["qAttributeExpressions"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == NxDimension.__annotations__["qAttributeExpressions"]
                for e in kvargs["qAttributeExpressions"]
            ):
                self_.qAttributeExpressions = kvargs["qAttributeExpressions"]
            else:
                self_.qAttributeExpressions = [
                    NxAttrExprDef(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qAttributeExpressions"]
                ]
        if "qCalcCond" in kvargs and kvargs["qCalcCond"] is not None:
            if (
                type(kvargs["qCalcCond"]).__name__
                == NxDimension.__annotations__["qCalcCond"]
            ):
                self_.qCalcCond = kvargs["qCalcCond"]
            else:
                self_.qCalcCond = ValueExpr(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qCalcCond"],
                )
        if "qCalcCondition" in kvargs and kvargs["qCalcCondition"] is not None:
            if (
                type(kvargs["qCalcCondition"]).__name__
                == NxDimension.__annotations__["qCalcCondition"]
            ):
                self_.qCalcCondition = kvargs["qCalcCondition"]
            else:
                self_.qCalcCondition = NxCalcCond(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qCalcCondition"],
                )
        if "qDef" in kvargs and kvargs["qDef"] is not None:
            if type(kvargs["qDef"]).__name__ == NxDimension.__annotations__["qDef"]:
                self_.qDef = kvargs["qDef"]
            else:
                self_.qDef = NxInlineDimensionDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qDef"],
                )
        if "qIncludeElemValue" in kvargs and kvargs["qIncludeElemValue"] is not None:
            self_.qIncludeElemValue = kvargs["qIncludeElemValue"]
        if "qLibraryId" in kvargs and kvargs["qLibraryId"] is not None:
            self_.qLibraryId = kvargs["qLibraryId"]
        if "qNullSuppression" in kvargs and kvargs["qNullSuppression"] is not None:
            self_.qNullSuppression = kvargs["qNullSuppression"]
        if "qOtherLabel" in kvargs and kvargs["qOtherLabel"] is not None:
            if (
                type(kvargs["qOtherLabel"]).__name__
                == NxDimension.__annotations__["qOtherLabel"]
            ):
                self_.qOtherLabel = kvargs["qOtherLabel"]
            else:
                self_.qOtherLabel = StringExpr(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qOtherLabel"],
                )
        if "qOtherTotalSpec" in kvargs and kvargs["qOtherTotalSpec"] is not None:
            if (
                type(kvargs["qOtherTotalSpec"]).__name__
                == NxDimension.__annotations__["qOtherTotalSpec"]
            ):
                self_.qOtherTotalSpec = kvargs["qOtherTotalSpec"]
            else:
                self_.qOtherTotalSpec = OtherTotalSpecProp(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qOtherTotalSpec"],
                )
        if "qShowAll" in kvargs and kvargs["qShowAll"] is not None:
            self_.qShowAll = kvargs["qShowAll"]
        if "qShowTotal" in kvargs and kvargs["qShowTotal"] is not None:
            self_.qShowTotal = kvargs["qShowTotal"]
        if "qTotalLabel" in kvargs and kvargs["qTotalLabel"] is not None:
            if (
                type(kvargs["qTotalLabel"]).__name__
                == NxDimension.__annotations__["qTotalLabel"]
            ):
                self_.qTotalLabel = kvargs["qTotalLabel"]
            else:
                self_.qTotalLabel = StringExpr(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qTotalLabel"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDimensionInfo:
    """

    Attributes
    ----------
    qApprMaxGlyphCount: int
      Length of the longest value in the field.
    qAttrDimInfo: list[NxAttrDimInfo]
      Array of attribute dimensions.
    qAttrExprInfo: list[NxAttrExprInfo]
      Array of attribute expressions.
    qCalcCondMsg: str
      The message displayed if calculation condition is not fulfilled.
    qCardinal: int
      Number of distinct field values.
    qCardinalities: NxCardinalities
      Dimension Cardinalities
    qContinuousAxes: bool
      Is continuous axis used.
    qDerivedField: bool
      Is derived field is used as a dimension.
    qDimensionType: Literal["NX_DIMENSION_TYPE_DISCRETE", "NX_DIMENSION_TYPE_NUMERIC", "NX_DIMENSION_TYPE_TIME"]
      Binary format of the field.

      One of:

      • D or NX_DIMENSION_TYPE_DISCRETE

      • N or NX_DIMENSION_TYPE_NUMERIC

      • T or NX_DIMENSION_TYPE_TIME
    qError: NxValidationError
      This parameter is optional.
      Gives information on the error.
    qFallbackTitle: str
      Corresponds to the label of the dimension that is selected.
      If the label is not defined then the field name is used.
    qGroupFallbackTitles: list[str]
      Array of dimension labels.
      Contains the labels of all dimensions in a hierarchy group (for example the labels of all dimensions in a drill down group).
    qGroupFieldDefs: list[str]
      Array of field names.
    qGroupPos: int
      Index of the dimension that is currently in use.
      qGroupPos is set to 0 if there are no hierarchical groups (drill-down groups) or cycle groups.
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"]
      Defines the grouping.

      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qIsAutoFormat: bool
      This parameter is set to true if qNumFormat is set to U (unknown). The engine guesses the type of the field based on the field's definition.
    qIsCalculated: bool
      True if this is a calculated dimension.
    qIsCyclic: bool
      Is a cyclic dimension used.
    qIsOneAndOnlyOne: bool
      If set to true, it means that the field always has one and only one selected value.
    qIsSemantic: bool
      If set to true, it means that the field is a semantic.
    qLibraryId: str
      Refers to a dimension stored in the library.
    qLocked: bool
      Is set to true if the field is locked.
    qMax: float
      Maximum value.
    qMin: float
      Minimum value.
    qNumFormat: FieldAttributes
      Format of the field.
      This parameter is optional.
    qReverseSort: bool
      If set to true, it inverts the sort criteria in the field.
    qSortIndicator: Literal["NX_SORT_INDICATE_NONE", "NX_SORT_INDICATE_ASC", "NX_SORT_INDICATE_DESC"]
      Sort indicator.
      The default value is no sorting.
      This parameter is optional.

      One of:

      • N or NX_SORT_INDICATE_NONE

      • A or NX_SORT_INDICATE_ASC

      • D or NX_SORT_INDICATE_DESC
    qStateCounts: NxStateCounts
      Number of values in a particular state.
    qTags: list[str]
      Gives information on a field. For example, it can return the type of the field.
      Examples: key, text, ASCII
    """

    qApprMaxGlyphCount: int = None
    qAttrDimInfo: list[NxAttrDimInfo] = None
    qAttrExprInfo: list[NxAttrExprInfo] = None
    qCalcCondMsg: str = None
    qCardinal: int = None
    qCardinalities: NxCardinalities = None
    qContinuousAxes: bool = None
    qDerivedField: bool = None
    qDimensionType: Literal[
        "NX_DIMENSION_TYPE_DISCRETE",
        "NX_DIMENSION_TYPE_NUMERIC",
        "NX_DIMENSION_TYPE_TIME",
    ] = None
    qError: NxValidationError = None
    qFallbackTitle: str = None
    qGroupFallbackTitles: list[str] = None
    qGroupFieldDefs: list[str] = None
    qGroupPos: int = None
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"] = None
    qIsAutoFormat: bool = None
    qIsCalculated: bool = None
    qIsCyclic: bool = None
    qIsOneAndOnlyOne: bool = None
    qIsSemantic: bool = None
    qLibraryId: str = None
    qLocked: bool = None
    qMax: float = None
    qMin: float = None
    qNumFormat: FieldAttributes = None
    qReverseSort: bool = None
    qSortIndicator: Literal[
        "NX_SORT_INDICATE_NONE", "NX_SORT_INDICATE_ASC", "NX_SORT_INDICATE_DESC"
    ] = None
    qStateCounts: NxStateCounts = None
    qTags: list[str] = None

    def __init__(self_, **kvargs):
        if "qApprMaxGlyphCount" in kvargs and kvargs["qApprMaxGlyphCount"] is not None:
            self_.qApprMaxGlyphCount = kvargs["qApprMaxGlyphCount"]
        if "qAttrDimInfo" in kvargs and kvargs["qAttrDimInfo"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxDimensionInfo.__annotations__["qAttrDimInfo"]
                for e in kvargs["qAttrDimInfo"]
            ):
                self_.qAttrDimInfo = kvargs["qAttrDimInfo"]
            else:
                self_.qAttrDimInfo = [
                    NxAttrDimInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qAttrDimInfo"]
                ]
        if "qAttrExprInfo" in kvargs and kvargs["qAttrExprInfo"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxDimensionInfo.__annotations__["qAttrExprInfo"]
                for e in kvargs["qAttrExprInfo"]
            ):
                self_.qAttrExprInfo = kvargs["qAttrExprInfo"]
            else:
                self_.qAttrExprInfo = [
                    NxAttrExprInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qAttrExprInfo"]
                ]
        if "qCalcCondMsg" in kvargs and kvargs["qCalcCondMsg"] is not None:
            self_.qCalcCondMsg = kvargs["qCalcCondMsg"]
        if "qCardinal" in kvargs and kvargs["qCardinal"] is not None:
            self_.qCardinal = kvargs["qCardinal"]
        if "qCardinalities" in kvargs and kvargs["qCardinalities"] is not None:
            if (
                type(kvargs["qCardinalities"]).__name__
                == NxDimensionInfo.__annotations__["qCardinalities"]
            ):
                self_.qCardinalities = kvargs["qCardinalities"]
            else:
                self_.qCardinalities = NxCardinalities(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qCardinalities"],
                )
        if "qContinuousAxes" in kvargs and kvargs["qContinuousAxes"] is not None:
            self_.qContinuousAxes = kvargs["qContinuousAxes"]
        if "qDerivedField" in kvargs and kvargs["qDerivedField"] is not None:
            self_.qDerivedField = kvargs["qDerivedField"]
        if "qDimensionType" in kvargs and kvargs["qDimensionType"] is not None:
            self_.qDimensionType = kvargs["qDimensionType"]
        if "qError" in kvargs and kvargs["qError"] is not None:
            if (
                type(kvargs["qError"]).__name__
                == NxDimensionInfo.__annotations__["qError"]
            ):
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qError"],
                )
        if "qFallbackTitle" in kvargs and kvargs["qFallbackTitle"] is not None:
            self_.qFallbackTitle = kvargs["qFallbackTitle"]
        if (
            "qGroupFallbackTitles" in kvargs
            and kvargs["qGroupFallbackTitles"] is not None
        ):
            self_.qGroupFallbackTitles = kvargs["qGroupFallbackTitles"]
        if "qGroupFieldDefs" in kvargs and kvargs["qGroupFieldDefs"] is not None:
            self_.qGroupFieldDefs = kvargs["qGroupFieldDefs"]
        if "qGroupPos" in kvargs and kvargs["qGroupPos"] is not None:
            self_.qGroupPos = kvargs["qGroupPos"]
        if "qGrouping" in kvargs and kvargs["qGrouping"] is not None:
            self_.qGrouping = kvargs["qGrouping"]
        if "qIsAutoFormat" in kvargs and kvargs["qIsAutoFormat"] is not None:
            self_.qIsAutoFormat = kvargs["qIsAutoFormat"]
        if "qIsCalculated" in kvargs and kvargs["qIsCalculated"] is not None:
            self_.qIsCalculated = kvargs["qIsCalculated"]
        if "qIsCyclic" in kvargs and kvargs["qIsCyclic"] is not None:
            self_.qIsCyclic = kvargs["qIsCyclic"]
        if "qIsOneAndOnlyOne" in kvargs and kvargs["qIsOneAndOnlyOne"] is not None:
            self_.qIsOneAndOnlyOne = kvargs["qIsOneAndOnlyOne"]
        if "qIsSemantic" in kvargs and kvargs["qIsSemantic"] is not None:
            self_.qIsSemantic = kvargs["qIsSemantic"]
        if "qLibraryId" in kvargs and kvargs["qLibraryId"] is not None:
            self_.qLibraryId = kvargs["qLibraryId"]
        if "qLocked" in kvargs and kvargs["qLocked"] is not None:
            self_.qLocked = kvargs["qLocked"]
        if "qMax" in kvargs and kvargs["qMax"] is not None:
            self_.qMax = kvargs["qMax"]
        if "qMin" in kvargs and kvargs["qMin"] is not None:
            self_.qMin = kvargs["qMin"]
        if "qNumFormat" in kvargs and kvargs["qNumFormat"] is not None:
            if (
                type(kvargs["qNumFormat"]).__name__
                == NxDimensionInfo.__annotations__["qNumFormat"]
            ):
                self_.qNumFormat = kvargs["qNumFormat"]
            else:
                self_.qNumFormat = FieldAttributes(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qNumFormat"],
                )
        if "qReverseSort" in kvargs and kvargs["qReverseSort"] is not None:
            self_.qReverseSort = kvargs["qReverseSort"]
        if "qSortIndicator" in kvargs and kvargs["qSortIndicator"] is not None:
            self_.qSortIndicator = kvargs["qSortIndicator"]
        if "qStateCounts" in kvargs and kvargs["qStateCounts"] is not None:
            if (
                type(kvargs["qStateCounts"]).__name__
                == NxDimensionInfo.__annotations__["qStateCounts"]
            ):
                self_.qStateCounts = kvargs["qStateCounts"]
            else:
                self_.qStateCounts = NxStateCounts(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qStateCounts"],
                )
        if "qTags" in kvargs and kvargs["qTags"] is not None:
            self_.qTags = kvargs["qTags"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDimensionType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDownloadInfo:
    """

    Attributes
    ----------
    qFileSize: int
      The filesize of the reduced app.
    qUrl: str
      URL to download the reduced app on.
    """

    qFileSize: int = -1
    qUrl: str = None

    def __init__(self_, **kvargs):
        if "qFileSize" in kvargs and kvargs["qFileSize"] is not None:
            self_.qFileSize = kvargs["qFileSize"]
        if "qUrl" in kvargs and kvargs["qUrl"] is not None:
            self_.qUrl = kvargs["qUrl"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxDownloadOptions:
    """

    Attributes
    ----------
    qBookmarkId: str
      Bookmark Id to apply before reducing the application.
    qExpires: int
      Time in seconds for how long the download link is valid.
    qServeOnce: bool
    """

    qBookmarkId: str = None
    qExpires: int = 3600
    qServeOnce: bool = None

    def __init__(self_, **kvargs):
        if "qBookmarkId" in kvargs and kvargs["qBookmarkId"] is not None:
            self_.qBookmarkId = kvargs["qBookmarkId"]
        if "qExpires" in kvargs and kvargs["qExpires"] is not None:
            self_.qExpires = kvargs["qExpires"]
        if "qServeOnce" in kvargs and kvargs["qServeOnce"] is not None:
            self_.qServeOnce = kvargs["qServeOnce"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxEngineVersion:
    """

    Attributes
    ----------
    qComponentVersion: str
      Version number of the Qlik engine component.
    """

    qComponentVersion: str = None

    def __init__(self_, **kvargs):
        if "qComponentVersion" in kvargs and kvargs["qComponentVersion"] is not None:
            self_.qComponentVersion = kvargs["qComponentVersion"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxExportFileType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxExportState:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxFeature:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxFieldDescription:
    """
     NxDerivedFieldsdata:
    | Name                   | Description                         | Type                      |
    |------------------------|-------------------------------------|---------------------------|
    | qDerivedDefinitionName | Name of the derived definition.     | String                    |
    | qFieldDefs             | List of the derived fields.         | Array of _NxDerivedField_ |
    | qGroupDefs             | List of the derived groups.         | Array of _NxDerivedGroup_ |
    | qTags                  | List of tags on the derived fields. | Array of _String_         |

    Attributes
    ----------
    qAndMode: bool
      If set to true a logical AND (instead of a logical OR) is used when making selections in a field.
      The default value is false.
    qCardinal: int
      Number of distinct field values
    qDerivedFieldData: NxDerivedFieldDescriptionList
      Lists the derived fields if any.
    qIsDefinitionOnly: bool
      If set to true, it means that the field is a field on the fly.
    qIsDetail: bool
      Is used for Direct Discovery.
      If set to true, it means that the type of the field is detail.
    qIsHidden: bool
      If set to true, it means that the field is hidden.
    qIsImplicit: bool
      Is used for Direct Discovery.
      If set to true, it means that the type of the field is measure.
    qIsSemantic: bool
      If set to true, it means that the field is a semantic.
    qIsSystem: bool
      If set to true, it means that the field is a system field.
    qName: str
      Name of the field
    qReadableName: str
    qTags: list[str]
      Gives information on a field. For example, it can return the type of the field.
      Examples: key, text, ASCII
    """

    qAndMode: bool = None
    qCardinal: int = None
    qDerivedFieldData: NxDerivedFieldDescriptionList = None
    qIsDefinitionOnly: bool = None
    qIsDetail: bool = None
    qIsHidden: bool = None
    qIsImplicit: bool = None
    qIsSemantic: bool = None
    qIsSystem: bool = None
    qName: str = None
    qReadableName: str = None
    qTags: list[str] = None

    def __init__(self_, **kvargs):
        if "qAndMode" in kvargs and kvargs["qAndMode"] is not None:
            self_.qAndMode = kvargs["qAndMode"]
        if "qCardinal" in kvargs and kvargs["qCardinal"] is not None:
            self_.qCardinal = kvargs["qCardinal"]
        if "qDerivedFieldData" in kvargs and kvargs["qDerivedFieldData"] is not None:
            if (
                type(kvargs["qDerivedFieldData"]).__name__
                == NxFieldDescription.__annotations__["qDerivedFieldData"]
            ):
                self_.qDerivedFieldData = kvargs["qDerivedFieldData"]
            else:
                self_.qDerivedFieldData = NxDerivedFieldDescriptionList(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qDerivedFieldData"],
                )
        if "qIsDefinitionOnly" in kvargs and kvargs["qIsDefinitionOnly"] is not None:
            self_.qIsDefinitionOnly = kvargs["qIsDefinitionOnly"]
        if "qIsDetail" in kvargs and kvargs["qIsDetail"] is not None:
            self_.qIsDetail = kvargs["qIsDetail"]
        if "qIsHidden" in kvargs and kvargs["qIsHidden"] is not None:
            self_.qIsHidden = kvargs["qIsHidden"]
        if "qIsImplicit" in kvargs and kvargs["qIsImplicit"] is not None:
            self_.qIsImplicit = kvargs["qIsImplicit"]
        if "qIsSemantic" in kvargs and kvargs["qIsSemantic"] is not None:
            self_.qIsSemantic = kvargs["qIsSemantic"]
        if "qIsSystem" in kvargs and kvargs["qIsSystem"] is not None:
            self_.qIsSystem = kvargs["qIsSystem"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qReadableName" in kvargs and kvargs["qReadableName"] is not None:
            self_.qReadableName = kvargs["qReadableName"]
        if "qTags" in kvargs and kvargs["qTags"] is not None:
            self_.qTags = kvargs["qTags"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxFieldProperties:
    """

    Attributes
    ----------
    qOneAndOnlyOne: bool
      This parameter is set to true, if the field has one and only one selection (not 0 and not more than 1).
      If this property is set to true, the field cannot be cleared anymore and no more selections can be performed in that field.
      The property OneAndOnlyOne can be set to true if one and only value has been selected in the field prior to setting the property.
    """

    qOneAndOnlyOne: bool = None

    def __init__(self_, **kvargs):
        if "qOneAndOnlyOne" in kvargs and kvargs["qOneAndOnlyOne"] is not None:
            self_.qOneAndOnlyOne = kvargs["qOneAndOnlyOne"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxFieldResourceId:
    """

    Attributes
    ----------
    qName: str
      Name of the field to get the resource id for.
    qResourceIds: list[NxFieldTableResourceId]
      Field level resource Id per table that the field is part of
    """

    qName: str = None
    qResourceIds: list[NxFieldTableResourceId] = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qResourceIds" in kvargs and kvargs["qResourceIds"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxFieldResourceId.__annotations__["qResourceIds"]
                for e in kvargs["qResourceIds"]
            ):
                self_.qResourceIds = kvargs["qResourceIds"]
            else:
                self_.qResourceIds = [
                    NxFieldTableResourceId(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qResourceIds"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxFieldSelectionInfo:
    """

    Attributes
    ----------
    qFieldSelectionMode: Literal["SELECTION_MODE_NORMAL", "SELECTION_MODE_AND", "SELECTION_MODE_NOT"]
      Selection mode.
       Properties:
      One of:

      • NORMAL for a selection in normal mode.

      • AND for a selection in AND mode.

      • NOT for a selection NOT in AND mode.
      One of:

      • NORMAL or SELECTION_MODE_NORMAL

      • AND or SELECTION_MODE_AND

      • NOT or SELECTION_MODE_NOT
    qName: str
      Name of the field.
    """

    qFieldSelectionMode: Literal[
        "SELECTION_MODE_NORMAL", "SELECTION_MODE_AND", "SELECTION_MODE_NOT"
    ] = None
    qName: str = None

    def __init__(self_, **kvargs):
        if (
            "qFieldSelectionMode" in kvargs
            and kvargs["qFieldSelectionMode"] is not None
        ):
            self_.qFieldSelectionMode = kvargs["qFieldSelectionMode"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxFieldSelectionMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxFieldTableResourceId:
    """

    Attributes
    ----------
    qResourceId: str
      Resource identifier for the field
    qTable: str
      Name of the table that the field belongs to get the resource id for
    """

    qResourceId: str = None
    qTable: str = None

    def __init__(self_, **kvargs):
        if "qResourceId" in kvargs and kvargs["qResourceId"] is not None:
            self_.qResourceId = kvargs["qResourceId"]
        if "qTable" in kvargs and kvargs["qTable"] is not None:
            self_.qTable = kvargs["qTable"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxFrequencyMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxGetBookmarkOptions:
    """

    Attributes
    ----------
    qData: JsonObject
      Set of data.
    qIncludePatches: bool
      Include the bookmark patches. Patches can be very large and may make the list result unmanageable.
    qTypes: list[str]
      List of object types.
    """

    qData: JsonObject = None
    qIncludePatches: bool = None
    qTypes: list[str] = None

    def __init__(self_, **kvargs):
        if "qData" in kvargs and kvargs["qData"] is not None:
            if (
                type(kvargs["qData"]).__name__
                == NxGetBookmarkOptions.__annotations__["qData"]
            ):
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qData"],
                )
        if "qIncludePatches" in kvargs and kvargs["qIncludePatches"] is not None:
            self_.qIncludePatches = kvargs["qIncludePatches"]
        if "qTypes" in kvargs and kvargs["qTypes"] is not None:
            self_.qTypes = kvargs["qTypes"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxGetObjectOptions:
    """

    Attributes
    ----------
    qData: JsonObject
      Set of data.
    qIncludeSessionObjects: bool
      Set to true to include session objects.
      The default value is false.
    qTypes: list[str]
      List of object types.
    """

    qData: JsonObject = None
    qIncludeSessionObjects: bool = None
    qTypes: list[str] = None

    def __init__(self_, **kvargs):
        if "qData" in kvargs and kvargs["qData"] is not None:
            if (
                type(kvargs["qData"]).__name__
                == NxGetObjectOptions.__annotations__["qData"]
            ):
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qData"],
                )
        if (
            "qIncludeSessionObjects" in kvargs
            and kvargs["qIncludeSessionObjects"] is not None
        ):
            self_.qIncludeSessionObjects = kvargs["qIncludeSessionObjects"]
        if "qTypes" in kvargs and kvargs["qTypes"] is not None:
            self_.qTypes = kvargs["qTypes"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxGroupTail:
    """

    Attributes
    ----------
    qDown: int
      Number of elements that are part of the next tail.
      This number depends on the paging, more particularly it depends on the values defined in qTop and qHeight
      Is not shown if the value is 0.
      This parameter is optional.
    qUp: int
      Number of elements that are part of the previous tail.
      This number depends on the paging, more particularly it depends on the values defined in qTop and qHeight .
      Is not shown if the value is 0.
      This parameter is optional.
    """

    qDown: int = None
    qUp: int = None

    def __init__(self_, **kvargs):
        if "qDown" in kvargs and kvargs["qDown"] is not None:
            self_.qDown = kvargs["qDown"]
        if "qUp" in kvargs and kvargs["qUp"] is not None:
            self_.qUp = kvargs["qUp"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxGrpType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxHighlightRanges:
    """

    Attributes
    ----------
    qRanges: list[CharRange]
      Ranges of highlighted values.
    """

    qRanges: list[CharRange] = None

    def __init__(self_, **kvargs):
        if "qRanges" in kvargs and kvargs["qRanges"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxHighlightRanges.__annotations__["qRanges"]
                for e in kvargs["qRanges"]
            ):
                self_.qRanges = kvargs["qRanges"]
            else:
                self_.qRanges = [
                    CharRange(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qRanges"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxHypercubeMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxInfo:
    """

    Attributes
    ----------
    qId: str
      Identifier of the object.
      If the chosen identifier is already in use, the engine automatically sets another one.
      If an identifier is not set, the engine automatically sets one.
      This parameter is optional.
    qType: str
      Type of the object.
      This parameter is mandatory.
    """

    qId: str = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qId" in kvargs and kvargs["qId"] is not None:
            self_.qId = kvargs["qId"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxInlineDimensionDef:
    """

    Attributes
    ----------
    qActiveField: int
      Index of the active field in a cyclic dimension.
      This parameter is optional. The default value is 0.
      This parameter is used in case of cyclic dimensions ( qGrouping is C).
    qFieldDefs: list[str]
      Array of field names.
      When creating a grouped dimension, more than one field name is defined.
      This parameter is optional.
    qFieldLabels: list[str]
      Array of field labels.
      This parameter is optional.
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"]
      Used to define a cyclic group or drill-down group.
      Default value is no grouping.
      This parameter is optional.

      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qLabelExpression: str
      Label expression.
      This parameter is optional.
    qNumberPresentations: list[FieldAttributes]
      Defines the format of the value.
      This parameter is optional.
    qReverseSort: bool
      If set to true, it inverts the sort criteria in the field.
    qSortCriterias: list[SortCriteria]
      Defines the sorting criteria in the field.
      Default is to sort by alphabetical order, ascending.
      This parameter is optional.
    """

    qActiveField: int = None
    qFieldDefs: list[str] = None
    qFieldLabels: list[str] = None
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"] = None
    qLabelExpression: str = None
    qNumberPresentations: list[FieldAttributes] = None
    qReverseSort: bool = None
    qSortCriterias: list[SortCriteria] = None

    def __init__(self_, **kvargs):
        if "qActiveField" in kvargs and kvargs["qActiveField"] is not None:
            self_.qActiveField = kvargs["qActiveField"]
        if "qFieldDefs" in kvargs and kvargs["qFieldDefs"] is not None:
            self_.qFieldDefs = kvargs["qFieldDefs"]
        if "qFieldLabels" in kvargs and kvargs["qFieldLabels"] is not None:
            self_.qFieldLabels = kvargs["qFieldLabels"]
        if "qGrouping" in kvargs and kvargs["qGrouping"] is not None:
            self_.qGrouping = kvargs["qGrouping"]
        if "qLabelExpression" in kvargs and kvargs["qLabelExpression"] is not None:
            self_.qLabelExpression = kvargs["qLabelExpression"]
        if (
            "qNumberPresentations" in kvargs
            and kvargs["qNumberPresentations"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == NxInlineDimensionDef.__annotations__["qNumberPresentations"]
                for e in kvargs["qNumberPresentations"]
            ):
                self_.qNumberPresentations = kvargs["qNumberPresentations"]
            else:
                self_.qNumberPresentations = [
                    FieldAttributes(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qNumberPresentations"]
                ]
        if "qReverseSort" in kvargs and kvargs["qReverseSort"] is not None:
            self_.qReverseSort = kvargs["qReverseSort"]
        if "qSortCriterias" in kvargs and kvargs["qSortCriterias"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxInlineDimensionDef.__annotations__["qSortCriterias"]
                for e in kvargs["qSortCriterias"]
            ):
                self_.qSortCriterias = kvargs["qSortCriterias"]
            else:
                self_.qSortCriterias = [
                    SortCriteria(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qSortCriterias"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxInlineMeasureDef:
    """

    Attributes
    ----------
    qAccumulate: int
      * 0 means no accumulation
                                  * 1 means full accumulation (each y-value accumulates all previous y-values of the expression)
                                  * ≥ 2 means accumulate as many steps as the qAccumulate value
      Default value is 0.
      This parameter is optional.
    qActiveExpression: int
      Index of the active expression in a cyclic measure. The indexing starts from 0.
      The default value is 0.
      This parameter is optional.
    qAggrFunc: str
      Aggregate function.
      For more information on the aggregate function syntax, see the section Working with Qlik Sense on the online help portal.
      The default value is 0 (Sum of rows)
      This parameter is optional.
    qBrutalSum: bool
      If set to true, the sum of rows total should be used rather than real expression total.
      This parameter is optional and applies to straight tables.
      Default value is false.
      If using the Qlik Sense interface, it means that the total mode is set to Expression Total .
    qDef: str
      Definition of the expression in the measure.
      Example: Sum (OrderTotal)
      This parameter is mandatory.
    qDescription: str
      Description of the measure.
      An empty string is returned as a default value.
      This parameter is optional.
    qExpressions: list[str]
      Array of expressions. This parameter is used in case of cyclic measures ( qGrouping is C). List of the expressions in the cyclic group.
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"]
      Default value is no grouping.
      This parameter is optional.

      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qLabel: str
      Name of the measure.
      An empty string is returned as a default value.
      This parameter is optional.
    qLabelExpression: str
      Label expression.
      This parameter is optional.
    qNumFormat: FieldAttributes
      Format of the field.
      This parameter is optional.
    qRelative: bool
      If set to true, percentage values are returned instead of absolute numbers.
      Default value is false.
      This parameter is optional.
    qReverseSort: bool
      If set to true, it inverts the sort criteria in the field.
    qTags: list[str]
      Name connected to the measure that is used for search purposes.
      A measure can have several tags.
      This parameter is optional.
    """

    qAccumulate: int = None
    qActiveExpression: int = None
    qAggrFunc: str = None
    qBrutalSum: bool = None
    qDef: str = None
    qDescription: str = None
    qExpressions: list[str] = None
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"] = None
    qLabel: str = None
    qLabelExpression: str = None
    qNumFormat: FieldAttributes = None
    qRelative: bool = None
    qReverseSort: bool = None
    qTags: list[str] = None

    def __init__(self_, **kvargs):
        if "qAccumulate" in kvargs and kvargs["qAccumulate"] is not None:
            self_.qAccumulate = kvargs["qAccumulate"]
        if "qActiveExpression" in kvargs and kvargs["qActiveExpression"] is not None:
            self_.qActiveExpression = kvargs["qActiveExpression"]
        if "qAggrFunc" in kvargs and kvargs["qAggrFunc"] is not None:
            self_.qAggrFunc = kvargs["qAggrFunc"]
        if "qBrutalSum" in kvargs and kvargs["qBrutalSum"] is not None:
            self_.qBrutalSum = kvargs["qBrutalSum"]
        if "qDef" in kvargs and kvargs["qDef"] is not None:
            self_.qDef = kvargs["qDef"]
        if "qDescription" in kvargs and kvargs["qDescription"] is not None:
            self_.qDescription = kvargs["qDescription"]
        if "qExpressions" in kvargs and kvargs["qExpressions"] is not None:
            self_.qExpressions = kvargs["qExpressions"]
        if "qGrouping" in kvargs and kvargs["qGrouping"] is not None:
            self_.qGrouping = kvargs["qGrouping"]
        if "qLabel" in kvargs and kvargs["qLabel"] is not None:
            self_.qLabel = kvargs["qLabel"]
        if "qLabelExpression" in kvargs and kvargs["qLabelExpression"] is not None:
            self_.qLabelExpression = kvargs["qLabelExpression"]
        if "qNumFormat" in kvargs and kvargs["qNumFormat"] is not None:
            if (
                type(kvargs["qNumFormat"]).__name__
                == NxInlineMeasureDef.__annotations__["qNumFormat"]
            ):
                self_.qNumFormat = kvargs["qNumFormat"]
            else:
                self_.qNumFormat = FieldAttributes(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qNumFormat"],
                )
        if "qRelative" in kvargs and kvargs["qRelative"] is not None:
            self_.qRelative = kvargs["qRelative"]
        if "qReverseSort" in kvargs and kvargs["qReverseSort"] is not None:
            self_.qReverseSort = kvargs["qReverseSort"]
        if "qTags" in kvargs and kvargs["qTags"] is not None:
            self_.qTags = kvargs["qTags"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLTrendlineType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLayoutErrors:
    """

    Attributes
    ----------
    qErrorCode: int
      Error code.
    """

    qErrorCode: int = None

    def __init__(self_, **kvargs):
        if "qErrorCode" in kvargs and kvargs["qErrorCode"] is not None:
            self_.qErrorCode = kvargs["qErrorCode"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLibraryDimension:
    """

    Attributes
    ----------
    qFieldDefs: list[str]
      Array of dimension names.
    qFieldLabels: list[str]
      Array of dimension labels.
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"]
      Information about the grouping.

      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qLabelExpression: str
    """

    qFieldDefs: list[str] = None
    qFieldLabels: list[str] = None
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"] = None
    qLabelExpression: str = None

    def __init__(self_, **kvargs):
        if "qFieldDefs" in kvargs and kvargs["qFieldDefs"] is not None:
            self_.qFieldDefs = kvargs["qFieldDefs"]
        if "qFieldLabels" in kvargs and kvargs["qFieldLabels"] is not None:
            self_.qFieldLabels = kvargs["qFieldLabels"]
        if "qGrouping" in kvargs and kvargs["qGrouping"] is not None:
            self_.qGrouping = kvargs["qGrouping"]
        if "qLabelExpression" in kvargs and kvargs["qLabelExpression"] is not None:
            self_.qLabelExpression = kvargs["qLabelExpression"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLibraryDimensionDef:
    """

    Attributes
    ----------
    qFieldDefs: list[str]
      Array of dimension names.
    qFieldLabels: list[str]
      Array of dimension labels.
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"]
      Information about the grouping.

      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qLabelExpression: str
    """

    qFieldDefs: list[str] = None
    qFieldLabels: list[str] = None
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"] = None
    qLabelExpression: str = None

    def __init__(self_, **kvargs):
        if "qFieldDefs" in kvargs and kvargs["qFieldDefs"] is not None:
            self_.qFieldDefs = kvargs["qFieldDefs"]
        if "qFieldLabels" in kvargs and kvargs["qFieldLabels"] is not None:
            self_.qFieldLabels = kvargs["qFieldLabels"]
        if "qGrouping" in kvargs and kvargs["qGrouping"] is not None:
            self_.qGrouping = kvargs["qGrouping"]
        if "qLabelExpression" in kvargs and kvargs["qLabelExpression"] is not None:
            self_.qLabelExpression = kvargs["qLabelExpression"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLibraryMeasure:
    """
    Information about the library measure. Is the layout for NxLibraryMeasureDef.

    Attributes
    ----------
    qActiveExpression: int
    qDef: str
    qExpressions: list[str]
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"]

      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qLabel: str
    qLabelExpression: str
    qNumFormat: FieldAttributes
      Format of the field.
      This parameter is optional.
    """

    qActiveExpression: int = None
    qDef: str = None
    qExpressions: list[str] = None
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"] = None
    qLabel: str = None
    qLabelExpression: str = None
    qNumFormat: FieldAttributes = None

    def __init__(self_, **kvargs):
        if "qActiveExpression" in kvargs and kvargs["qActiveExpression"] is not None:
            self_.qActiveExpression = kvargs["qActiveExpression"]
        if "qDef" in kvargs and kvargs["qDef"] is not None:
            self_.qDef = kvargs["qDef"]
        if "qExpressions" in kvargs and kvargs["qExpressions"] is not None:
            self_.qExpressions = kvargs["qExpressions"]
        if "qGrouping" in kvargs and kvargs["qGrouping"] is not None:
            self_.qGrouping = kvargs["qGrouping"]
        if "qLabel" in kvargs and kvargs["qLabel"] is not None:
            self_.qLabel = kvargs["qLabel"]
        if "qLabelExpression" in kvargs and kvargs["qLabelExpression"] is not None:
            self_.qLabelExpression = kvargs["qLabelExpression"]
        if "qNumFormat" in kvargs and kvargs["qNumFormat"] is not None:
            if (
                type(kvargs["qNumFormat"]).__name__
                == NxLibraryMeasure.__annotations__["qNumFormat"]
            ):
                self_.qNumFormat = kvargs["qNumFormat"]
            else:
                self_.qNumFormat = FieldAttributes(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qNumFormat"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLibraryMeasureDef:
    """

    Attributes
    ----------
    qActiveExpression: int
      Index to the active expression in a measure.
    qDef: str
      Definition of the measure.
    qExpressions: list[str]
      Array of expressions.
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"]
      Used to define a cyclic group or drill-down group.
      Default value is no grouping.
      This parameter is optional.

      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qLabel: str
      Label of the measure.
    qLabelExpression: str
      Optional expression used for dynamic label.
    qNumFormat: FieldAttributes
      Format of the field.
      This parameter is optional.
    """

    qActiveExpression: int = None
    qDef: str = None
    qExpressions: list[str] = None
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"] = None
    qLabel: str = None
    qLabelExpression: str = None
    qNumFormat: FieldAttributes = None

    def __init__(self_, **kvargs):
        if "qActiveExpression" in kvargs and kvargs["qActiveExpression"] is not None:
            self_.qActiveExpression = kvargs["qActiveExpression"]
        if "qDef" in kvargs and kvargs["qDef"] is not None:
            self_.qDef = kvargs["qDef"]
        if "qExpressions" in kvargs and kvargs["qExpressions"] is not None:
            self_.qExpressions = kvargs["qExpressions"]
        if "qGrouping" in kvargs and kvargs["qGrouping"] is not None:
            self_.qGrouping = kvargs["qGrouping"]
        if "qLabel" in kvargs and kvargs["qLabel"] is not None:
            self_.qLabel = kvargs["qLabel"]
        if "qLabelExpression" in kvargs and kvargs["qLabelExpression"] is not None:
            self_.qLabelExpression = kvargs["qLabelExpression"]
        if "qNumFormat" in kvargs and kvargs["qNumFormat"] is not None:
            if (
                type(kvargs["qNumFormat"]).__name__
                == NxLibraryMeasureDef.__annotations__["qNumFormat"]
            ):
                self_.qNumFormat = kvargs["qNumFormat"]
            else:
                self_.qNumFormat = FieldAttributes(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qNumFormat"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLinkedObjectInfo:
    """

    Attributes
    ----------
    qInfo: NxInfo
      Information about the linked object.
    qRootId: str
      Identifier of the root object.
      If the linked object is a child, the root identifier is the identifier of the parent.
      If the linked object is an app object, the root identifier is the same than the identifier of the linked object since the linked object is a root object.
    """

    qInfo: NxInfo = None
    qRootId: str = None

    def __init__(self_, **kvargs):
        if "qInfo" in kvargs and kvargs["qInfo"] is not None:
            if (
                type(kvargs["qInfo"]).__name__
                == NxLinkedObjectInfo.__annotations__["qInfo"]
            ):
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qInfo"],
                )
        if "qRootId" in kvargs and kvargs["qRootId"] is not None:
            self_.qRootId = kvargs["qRootId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxListObjectExpression:
    """

    Attributes
    ----------
    qError: NxLayoutErrors
      Gives information on the error.
      This parameter is optional.
    qExpr: str
      Value of the expression.
    """

    qError: NxLayoutErrors = None
    qExpr: str = None

    def __init__(self_, **kvargs):
        if "qError" in kvargs and kvargs["qError"] is not None:
            if (
                type(kvargs["qError"]).__name__
                == NxListObjectExpression.__annotations__["qError"]
            ):
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxLayoutErrors(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qError"],
                )
        if "qExpr" in kvargs and kvargs["qExpr"] is not None:
            self_.qExpr = kvargs["qExpr"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxListObjectExpressionDef:
    """

    Attributes
    ----------
    qExpr: str
      Value of the expression.
    qLibraryId: str
      Refers to an expression stored in the library.
    """

    qExpr: str = None
    qLibraryId: str = None

    def __init__(self_, **kvargs):
        if "qExpr" in kvargs and kvargs["qExpr"] is not None:
            self_.qExpr = kvargs["qExpr"]
        if "qLibraryId" in kvargs and kvargs["qLibraryId"] is not None:
            self_.qLibraryId = kvargs["qLibraryId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLocalizedErrorCode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxLocalizedWarningCode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMatchingFieldInfo:
    """

    Attributes
    ----------
    qName: str
      Name of the field.
    qTags: list[str]
      List of tags.
    """

    qName: str = None
    qTags: list[str] = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qTags" in kvargs and kvargs["qTags"] is not None:
            self_.qTags = kvargs["qTags"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMatchingFieldMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMeasure:
    """
    Either qDef or qLibraryId must be set, but not both.  If the measure is set in the hypercube and not in the library, this measure cannot be shared with other objects. A measure that is set in the library can be used by many objects.
    expressions are complementary expressions associated to a measure. For example, you can decide to change the background color of a visualization depending on the values of the measure.
    Attribute expressions do not affect the layout of an object. The sorting order is unchanged.


    Attributes
    ----------
    qAttributeDimensions: list[NxAttrDimDef]
      List of attribute dimensions.
    qAttributeExpressions: list[NxAttrExprDef]
      List of attribute expressions.
    qCalcCond: ValueExpr
      Specifies a calculation condition, which must be fulfilled for the measure to be calculated.
      If the calculation condition is not met, the measure is excluded from the calculation.
      By default, there is no calculation condition.
      This property is optional.
    qCalcCondition: NxCalcCond
      Specifies a calculation condition object.
      If CalcCondition.Cond is not fulfilled, the measure is excluded from the calculation and CalcCondition.Msg is evaluated.
      By default, there is no calculation condition.
      This property is optional.
    qDef: NxInlineMeasureDef
      Refers to a measure stored in the hypercube.
    qLibraryId: str
      Refers to a measure stored in the library.
    qMiniChartDef: NxMiniChartDef
    qSortBy: SortCriteria
      Defines the sort criteria.
      The default value is sort by ascending alphabetic order.
      This property is optional.
    qTrendLines: list[NxTrendlineDef]
      Specifies trendlines for this measure.
    """

    qAttributeDimensions: list[NxAttrDimDef] = None
    qAttributeExpressions: list[NxAttrExprDef] = None
    qCalcCond: ValueExpr = None
    qCalcCondition: NxCalcCond = None
    qDef: NxInlineMeasureDef = None
    qLibraryId: str = None
    qMiniChartDef: NxMiniChartDef = None
    qSortBy: SortCriteria = None
    qTrendLines: list[NxTrendlineDef] = None

    def __init__(self_, **kvargs):
        if (
            "qAttributeDimensions" in kvargs
            and kvargs["qAttributeDimensions"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == NxMeasure.__annotations__["qAttributeDimensions"]
                for e in kvargs["qAttributeDimensions"]
            ):
                self_.qAttributeDimensions = kvargs["qAttributeDimensions"]
            else:
                self_.qAttributeDimensions = [
                    NxAttrDimDef(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qAttributeDimensions"]
                ]
        if (
            "qAttributeExpressions" in kvargs
            and kvargs["qAttributeExpressions"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == NxMeasure.__annotations__["qAttributeExpressions"]
                for e in kvargs["qAttributeExpressions"]
            ):
                self_.qAttributeExpressions = kvargs["qAttributeExpressions"]
            else:
                self_.qAttributeExpressions = [
                    NxAttrExprDef(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qAttributeExpressions"]
                ]
        if "qCalcCond" in kvargs and kvargs["qCalcCond"] is not None:
            if (
                type(kvargs["qCalcCond"]).__name__
                == NxMeasure.__annotations__["qCalcCond"]
            ):
                self_.qCalcCond = kvargs["qCalcCond"]
            else:
                self_.qCalcCond = ValueExpr(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qCalcCond"],
                )
        if "qCalcCondition" in kvargs and kvargs["qCalcCondition"] is not None:
            if (
                type(kvargs["qCalcCondition"]).__name__
                == NxMeasure.__annotations__["qCalcCondition"]
            ):
                self_.qCalcCondition = kvargs["qCalcCondition"]
            else:
                self_.qCalcCondition = NxCalcCond(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qCalcCondition"],
                )
        if "qDef" in kvargs and kvargs["qDef"] is not None:
            if type(kvargs["qDef"]).__name__ == NxMeasure.__annotations__["qDef"]:
                self_.qDef = kvargs["qDef"]
            else:
                self_.qDef = NxInlineMeasureDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qDef"],
                )
        if "qLibraryId" in kvargs and kvargs["qLibraryId"] is not None:
            self_.qLibraryId = kvargs["qLibraryId"]
        if "qMiniChartDef" in kvargs and kvargs["qMiniChartDef"] is not None:
            if (
                type(kvargs["qMiniChartDef"]).__name__
                == NxMeasure.__annotations__["qMiniChartDef"]
            ):
                self_.qMiniChartDef = kvargs["qMiniChartDef"]
            else:
                self_.qMiniChartDef = NxMiniChartDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMiniChartDef"],
                )
        if "qSortBy" in kvargs and kvargs["qSortBy"] is not None:
            if type(kvargs["qSortBy"]).__name__ == NxMeasure.__annotations__["qSortBy"]:
                self_.qSortBy = kvargs["qSortBy"]
            else:
                self_.qSortBy = SortCriteria(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qSortBy"],
                )
        if "qTrendLines" in kvargs and kvargs["qTrendLines"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NxMeasure.__annotations__["qTrendLines"]
                for e in kvargs["qTrendLines"]
            ):
                self_.qTrendLines = kvargs["qTrendLines"]
            else:
                self_.qTrendLines = [
                    NxTrendlineDef(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qTrendLines"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMeasureInfo:
    """
    Layout for NxInlineMeasureDef.

    Attributes
    ----------
    qApprMaxGlyphCount: int
      Length of the longest value in the field.
    qAttrDimInfo: list[NxAttrDimInfo]
      List of attribute dimensions.
    qAttrExprInfo: list[NxAttrExprInfo]
      List of attribute expressions.
    qCalcCondMsg: str
      The message displayed if calculation condition is not fulfilled.
    qCardinal: int
      Number of distinct field values.
    qError: NxValidationError
      This parameter is optional.
      Gives information on the error.
    qFallbackTitle: str
      Corresponds to the label of the measure.
      If the label is not defined then the measure name is used.
    qIsAutoFormat: bool
      This parameter is set to true if qNumFormat is set to U (unknown). The engine guesses the type of the field based on the field's expression.
    qLibraryId: str
      Refers to a dimension stored in the library.
    qMax: float
      Highest value in the range.
    qMin: float
      Lowest value in the range.
    qMiniChart: NxMiniChart
    qNumFormat: FieldAttributes
      Format of the field.
      This parameter is optional.
    qReverseSort: bool
      If set to true, it inverts the sort criteria in the field.
    qSortIndicator: Literal["NX_SORT_INDICATE_NONE", "NX_SORT_INDICATE_ASC", "NX_SORT_INDICATE_DESC"]
      Sort indicator.
      The default value is no sorting.
      This parameter is optional.

      One of:

      • N or NX_SORT_INDICATE_NONE

      • A or NX_SORT_INDICATE_ASC

      • D or NX_SORT_INDICATE_DESC
    qTrendLines: list[NxTrendline]
      Calculated trendlines
    """

    qApprMaxGlyphCount: int = None
    qAttrDimInfo: list[NxAttrDimInfo] = None
    qAttrExprInfo: list[NxAttrExprInfo] = None
    qCalcCondMsg: str = None
    qCardinal: int = None
    qError: NxValidationError = None
    qFallbackTitle: str = None
    qIsAutoFormat: bool = None
    qLibraryId: str = None
    qMax: float = None
    qMin: float = None
    qMiniChart: NxMiniChart = None
    qNumFormat: FieldAttributes = None
    qReverseSort: bool = None
    qSortIndicator: Literal[
        "NX_SORT_INDICATE_NONE", "NX_SORT_INDICATE_ASC", "NX_SORT_INDICATE_DESC"
    ] = None
    qTrendLines: list[NxTrendline] = None

    def __init__(self_, **kvargs):
        if "qApprMaxGlyphCount" in kvargs and kvargs["qApprMaxGlyphCount"] is not None:
            self_.qApprMaxGlyphCount = kvargs["qApprMaxGlyphCount"]
        if "qAttrDimInfo" in kvargs and kvargs["qAttrDimInfo"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxMeasureInfo.__annotations__["qAttrDimInfo"]
                for e in kvargs["qAttrDimInfo"]
            ):
                self_.qAttrDimInfo = kvargs["qAttrDimInfo"]
            else:
                self_.qAttrDimInfo = [
                    NxAttrDimInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qAttrDimInfo"]
                ]
        if "qAttrExprInfo" in kvargs and kvargs["qAttrExprInfo"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxMeasureInfo.__annotations__["qAttrExprInfo"]
                for e in kvargs["qAttrExprInfo"]
            ):
                self_.qAttrExprInfo = kvargs["qAttrExprInfo"]
            else:
                self_.qAttrExprInfo = [
                    NxAttrExprInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qAttrExprInfo"]
                ]
        if "qCalcCondMsg" in kvargs and kvargs["qCalcCondMsg"] is not None:
            self_.qCalcCondMsg = kvargs["qCalcCondMsg"]
        if "qCardinal" in kvargs and kvargs["qCardinal"] is not None:
            self_.qCardinal = kvargs["qCardinal"]
        if "qError" in kvargs and kvargs["qError"] is not None:
            if (
                type(kvargs["qError"]).__name__
                == NxMeasureInfo.__annotations__["qError"]
            ):
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qError"],
                )
        if "qFallbackTitle" in kvargs and kvargs["qFallbackTitle"] is not None:
            self_.qFallbackTitle = kvargs["qFallbackTitle"]
        if "qIsAutoFormat" in kvargs and kvargs["qIsAutoFormat"] is not None:
            self_.qIsAutoFormat = kvargs["qIsAutoFormat"]
        if "qLibraryId" in kvargs and kvargs["qLibraryId"] is not None:
            self_.qLibraryId = kvargs["qLibraryId"]
        if "qMax" in kvargs and kvargs["qMax"] is not None:
            self_.qMax = kvargs["qMax"]
        if "qMin" in kvargs and kvargs["qMin"] is not None:
            self_.qMin = kvargs["qMin"]
        if "qMiniChart" in kvargs and kvargs["qMiniChart"] is not None:
            if (
                type(kvargs["qMiniChart"]).__name__
                == NxMeasureInfo.__annotations__["qMiniChart"]
            ):
                self_.qMiniChart = kvargs["qMiniChart"]
            else:
                self_.qMiniChart = NxMiniChart(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMiniChart"],
                )
        if "qNumFormat" in kvargs and kvargs["qNumFormat"] is not None:
            if (
                type(kvargs["qNumFormat"]).__name__
                == NxMeasureInfo.__annotations__["qNumFormat"]
            ):
                self_.qNumFormat = kvargs["qNumFormat"]
            else:
                self_.qNumFormat = FieldAttributes(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qNumFormat"],
                )
        if "qReverseSort" in kvargs and kvargs["qReverseSort"] is not None:
            self_.qReverseSort = kvargs["qReverseSort"]
        if "qSortIndicator" in kvargs and kvargs["qSortIndicator"] is not None:
            self_.qSortIndicator = kvargs["qSortIndicator"]
        if "qTrendLines" in kvargs and kvargs["qTrendLines"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxMeasureInfo.__annotations__["qTrendLines"]
                for e in kvargs["qTrendLines"]
            ):
                self_.qTrendLines = kvargs["qTrendLines"]
            else:
                self_.qTrendLines = [
                    NxTrendline(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qTrendLines"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMeta:
    """
    Layout for NxMetaDef.

    Attributes
    ----------
    qName: str
      Name.
      This property is optional.
    """

    qName: str = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMetaDef:
    """
    Used to collect meta data.

     Properties:
    Semantic type with an empty structure.

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMiniChart:
    """

    Attributes
    ----------
    qAttrExprInfo: list[NxAttrExprInfo]
      List of attribute expressions.
    qError: NxValidationError
      This parameter is optional and is displayed in case of error.
    qXMax: float
    qXMin: float
    qYMax: float
    qYMin: float
    """

    qAttrExprInfo: list[NxAttrExprInfo] = None
    qError: NxValidationError = None
    qXMax: float = None
    qXMin: float = None
    qYMax: float = None
    qYMin: float = None

    def __init__(self_, **kvargs):
        if "qAttrExprInfo" in kvargs and kvargs["qAttrExprInfo"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxMiniChart.__annotations__["qAttrExprInfo"]
                for e in kvargs["qAttrExprInfo"]
            ):
                self_.qAttrExprInfo = kvargs["qAttrExprInfo"]
            else:
                self_.qAttrExprInfo = [
                    NxAttrExprInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qAttrExprInfo"]
                ]
        if "qError" in kvargs and kvargs["qError"] is not None:
            if type(kvargs["qError"]).__name__ == NxMiniChart.__annotations__["qError"]:
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qError"],
                )
        if "qXMax" in kvargs and kvargs["qXMax"] is not None:
            self_.qXMax = kvargs["qXMax"]
        if "qXMin" in kvargs and kvargs["qXMin"] is not None:
            self_.qXMin = kvargs["qXMin"]
        if "qYMax" in kvargs and kvargs["qYMax"] is not None:
            self_.qYMax = kvargs["qYMax"]
        if "qYMin" in kvargs and kvargs["qYMin"] is not None:
            self_.qYMin = kvargs["qYMin"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMiniChartCell:
    """

    Attributes
    ----------
    qAttrExps: NxAttributeExpressionValues
      Attribute expressions values.
    qElemNumber: int
      Rank number of the value, starting from 0.
      If the element number is a negative number, it means that the returned value is not an element number.
      You can get the following negative values:

      • -1: the cell is a Total cell. It shows a total.

      • -2: the cell is a Null cell.

      • -3: the cell belongs to the group Others .

      • -4: the cell is empty. Applies to pivot tables.
    qNum: float
      A value.
      This parameter is optional.
    qText: str
      Some text.
    """

    qAttrExps: NxAttributeExpressionValues = None
    qElemNumber: int = None
    qNum: float = None
    qText: str = None

    def __init__(self_, **kvargs):
        if "qAttrExps" in kvargs and kvargs["qAttrExps"] is not None:
            if (
                type(kvargs["qAttrExps"]).__name__
                == NxMiniChartCell.__annotations__["qAttrExps"]
            ):
                self_.qAttrExps = kvargs["qAttrExps"]
            else:
                self_.qAttrExps = NxAttributeExpressionValues(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qAttrExps"],
                )
        if "qElemNumber" in kvargs and kvargs["qElemNumber"] is not None:
            self_.qElemNumber = kvargs["qElemNumber"]
        if "qNum" in kvargs and kvargs["qNum"] is not None:
            self_.qNum = kvargs["qNum"]
        if "qText" in kvargs and kvargs["qText"] is not None:
            self_.qText = kvargs["qText"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMiniChartData:
    """

    Attributes
    ----------
    qError: NxValidationError
      This parameter is optional and is displayed in case of error.
    qMatrix: list[NxMiniChartRows]
      Array of data.
    qMax: float
    qMin: float
    """

    qError: NxValidationError = None
    qMatrix: list[NxMiniChartRows] = None
    qMax: float = None
    qMin: float = None

    def __init__(self_, **kvargs):
        if "qError" in kvargs and kvargs["qError"] is not None:
            if (
                type(kvargs["qError"]).__name__
                == NxMiniChartData.__annotations__["qError"]
            ):
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qError"],
                )
        if "qMatrix" in kvargs and kvargs["qMatrix"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxMiniChartData.__annotations__["qMatrix"]
                for e in kvargs["qMatrix"]
            ):
                self_.qMatrix = kvargs["qMatrix"]
            else:
                self_.qMatrix = [NxMiniChartRows(e) for e in kvargs["qMatrix"]]
        if "qMax" in kvargs and kvargs["qMax"] is not None:
            self_.qMax = kvargs["qMax"]
        if "qMin" in kvargs and kvargs["qMin"] is not None:
            self_.qMin = kvargs["qMin"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMiniChartDef:
    """

    Attributes
    ----------
    qAttributeExpressions: list[NxAttrExprDef]
      List of attribute expressions.
    qDef: str
      Expression or field name.
    qLibraryId: str
      LibraryId for dimension.
    qMaxNumberPoints: int
    qNullSuppression: bool
      If set to true, no null values are returned.
    qOtherTotalSpec: OtherTotalSpecProp
    qSortBy: SortCriteria
      Sorting.
    """

    qAttributeExpressions: list[NxAttrExprDef] = None
    qDef: str = None
    qLibraryId: str = None
    qMaxNumberPoints: int = -1
    qNullSuppression: bool = None
    qOtherTotalSpec: OtherTotalSpecProp = None
    qSortBy: SortCriteria = None

    def __init__(self_, **kvargs):
        if (
            "qAttributeExpressions" in kvargs
            and kvargs["qAttributeExpressions"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == NxMiniChartDef.__annotations__["qAttributeExpressions"]
                for e in kvargs["qAttributeExpressions"]
            ):
                self_.qAttributeExpressions = kvargs["qAttributeExpressions"]
            else:
                self_.qAttributeExpressions = [
                    NxAttrExprDef(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qAttributeExpressions"]
                ]
        if "qDef" in kvargs and kvargs["qDef"] is not None:
            self_.qDef = kvargs["qDef"]
        if "qLibraryId" in kvargs and kvargs["qLibraryId"] is not None:
            self_.qLibraryId = kvargs["qLibraryId"]
        if "qMaxNumberPoints" in kvargs and kvargs["qMaxNumberPoints"] is not None:
            self_.qMaxNumberPoints = kvargs["qMaxNumberPoints"]
        if "qNullSuppression" in kvargs and kvargs["qNullSuppression"] is not None:
            self_.qNullSuppression = kvargs["qNullSuppression"]
        if "qOtherTotalSpec" in kvargs and kvargs["qOtherTotalSpec"] is not None:
            if (
                type(kvargs["qOtherTotalSpec"]).__name__
                == NxMiniChartDef.__annotations__["qOtherTotalSpec"]
            ):
                self_.qOtherTotalSpec = kvargs["qOtherTotalSpec"]
            else:
                self_.qOtherTotalSpec = OtherTotalSpecProp(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qOtherTotalSpec"],
                )
        if "qSortBy" in kvargs and kvargs["qSortBy"] is not None:
            if (
                type(kvargs["qSortBy"]).__name__
                == NxMiniChartDef.__annotations__["qSortBy"]
            ):
                self_.qSortBy = kvargs["qSortBy"]
            else:
                self_.qSortBy = SortCriteria(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qSortBy"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxMiniChartRows(List["NxMiniChartCell"]):
    """

    Attributes
    ----------
    """

    def __init__(self_, elements):
        for e in elements:
            self_.append(NxMiniChartCell(**e))


@dataclass
class NxMultiRangeSelectInfo:
    """

    Attributes
    ----------
    qColumnsToSelect: list[int]
    qRanges: list[NxRangeSelectInfo]
    """

    qColumnsToSelect: list[int] = None
    qRanges: list[NxRangeSelectInfo] = None

    def __init__(self_, **kvargs):
        if "qColumnsToSelect" in kvargs and kvargs["qColumnsToSelect"] is not None:
            self_.qColumnsToSelect = kvargs["qColumnsToSelect"]
        if "qRanges" in kvargs and kvargs["qRanges"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxMultiRangeSelectInfo.__annotations__["qRanges"]
                for e in kvargs["qRanges"]
            ):
                self_.qRanges = kvargs["qRanges"]
            else:
                self_.qRanges = [
                    NxRangeSelectInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qRanges"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPage:
    """

    Attributes
    ----------
    qHeight: int
      Number of rows or elements in the page. The indexing of the rows may vary depending on whether the cells are expanded or not (parameter qAlwaysFullyExpanded in HyperCubeDef ).
    qLeft: int
      Position from the left.
      Corresponds to the first column.
    qTop: int
      Position from the top.
      Corresponds to the first row.
    qWidth: int
      Number of columns in the page. The indexing of the columns may vary depending on whether the cells are expanded or not (parameter qAlwaysFullyExpanded in HyperCubeDef ).
    """

    qHeight: int = None
    qLeft: int = None
    qTop: int = None
    qWidth: int = None

    def __init__(self_, **kvargs):
        if "qHeight" in kvargs and kvargs["qHeight"] is not None:
            self_.qHeight = kvargs["qHeight"]
        if "qLeft" in kvargs and kvargs["qLeft"] is not None:
            self_.qLeft = kvargs["qLeft"]
        if "qTop" in kvargs and kvargs["qTop"] is not None:
            self_.qTop = kvargs["qTop"]
        if "qWidth" in kvargs and kvargs["qWidth"] is not None:
            self_.qWidth = kvargs["qWidth"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPageTreeLevel:
    """

    Attributes
    ----------
    qDepth: int
      Number of dimensions to include in the tree.
    qLeft: int
      The first dimension that is to be part of the tree, counted from the left. For example, if qLeft is equal to 1, omit nodes from the first dimension in the current sort order.
    """

    qDepth: int = -1
    qLeft: int = None

    def __init__(self_, **kvargs):
        if "qDepth" in kvargs and kvargs["qDepth"] is not None:
            self_.qDepth = kvargs["qDepth"]
        if "qLeft" in kvargs and kvargs["qLeft"] is not None:
            self_.qLeft = kvargs["qLeft"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPageTreeNode:
    """
    Defines an area of the tree to be fetched.

    Attributes
    ----------
    qAllValues: bool
      When set to true, generated nodes (based on current selection) will be inserted into the returned tree even when there is no actual value. For example, suppose you are looking for hybrid car sales at all car dealerships. Normally, only dealerships where hybrid cars are sold would be part of the returned tree but with qAllValues set to true, all available dealerships will be included regardless if they sold any hybrid cars or not.
    qArea: Rect
      The area of the tree to be fetched. If no area is defined on a dimension, all existing nodes are included.
    """

    qAllValues: bool = None
    qArea: Rect = None

    def __init__(self_, **kvargs):
        if "qAllValues" in kvargs and kvargs["qAllValues"] is not None:
            self_.qAllValues = kvargs["qAllValues"]
        if "qArea" in kvargs and kvargs["qArea"] is not None:
            if (
                type(kvargs["qArea"]).__name__
                == NxPageTreeNode.__annotations__["qArea"]
            ):
                self_.qArea = kvargs["qArea"]
            else:
                self_.qArea = Rect(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qArea"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPatch:
    """

    Attributes
    ----------
    qOp: Literal["Add", "Remove", "Replace"]
      Operation to perform.

      One of:

      • add or Add

      • remove or Remove

      • replace or Replace
    qPath: str
      Path to the property to add, remove or replace.
    qValue: str
      This parameter is not used in a remove operation.
      Corresponds to the value of the property to add or to the new value of the property to update.
      Examples:
      "false", "2", "\"New title\""
    """

    qOp: Literal["Add", "Remove", "Replace"] = None
    qPath: str = None
    qValue: str = None

    def __init__(self_, **kvargs):
        if "qOp" in kvargs and kvargs["qOp"] is not None:
            self_.qOp = kvargs["qOp"]
        if "qPath" in kvargs and kvargs["qPath"] is not None:
            self_.qPath = kvargs["qPath"]
        if "qValue" in kvargs and kvargs["qValue"] is not None:
            self_.qValue = kvargs["qValue"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPatchOperationType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPatches:
    """

    Attributes
    ----------
    qChildren: list[NxPatches]
      Array with child objects and their patches.
    qInfo: NxInfo
      Identifier and type of the object.
    qPatches: list[NxPatch]
      Array with patches.
    """

    qChildren: list[NxPatches] = None
    qInfo: NxInfo = None
    qPatches: list[NxPatch] = None

    def __init__(self_, **kvargs):
        if "qChildren" in kvargs and kvargs["qChildren"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NxPatches.__annotations__["qChildren"]
                for e in kvargs["qChildren"]
            ):
                self_.qChildren = kvargs["qChildren"]
            else:
                self_.qChildren = [
                    NxPatches(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qChildren"]
                ]
        if "qInfo" in kvargs and kvargs["qInfo"] is not None:
            if type(kvargs["qInfo"]).__name__ == NxPatches.__annotations__["qInfo"]:
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qInfo"],
                )
        if "qPatches" in kvargs and kvargs["qPatches"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NxPatches.__annotations__["qPatches"]
                for e in kvargs["qPatches"]
            ):
                self_.qPatches = kvargs["qPatches"]
            else:
                self_.qPatches = [
                    NxPatch(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qPatches"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPivotDimensionCell:
    """

    Attributes
    ----------
    qAttrDims: NxAttributeDimValues
      Information about attribute dimensions.
    qAttrExps: NxAttributeExpressionValues
      Information about attribute expressions.
      The array is empty [ ] when there is no attribute expressions.
    qCanCollapse: bool
      If set to true, it means that the cell can be collapsed.
      This parameter is not returned if it is set to false.
    qCanExpand: bool
      If set to true, it means that the cell can be expanded.
      This parameter is not returned if it is set to false.
    qDown: int
      Number of elements that are part of the next tail.
      This number depends on the paging, more particularly it depends on the values defined in qTop and qHeight .
    qElemNo: int
      Rank number of the value.
      If set to -1, it means that the value is not an element number.
    qSubNodes: list[NxPivotDimensionCell]
      Information about sub nodes (or sub cells).
      The array is empty [ ] when there is no sub nodes.
    qText: str
      Some text.
    qType: Literal["NX_DIM_CELL_VALUE", "NX_DIM_CELL_EMPTY", "NX_DIM_CELL_NORMAL", "NX_DIM_CELL_TOTAL", "NX_DIM_CELL_OTHER", "NX_DIM_CELL_AGGR", "NX_DIM_CELL_PSEUDO", "NX_DIM_CELL_ROOT", "NX_DIM_CELL_NULL", "NX_DIM_CELL_GENERATED"]
      Type of the cell.

      One of:

      • V or NX_DIM_CELL_VALUE

      • E or NX_DIM_CELL_EMPTY

      • N or NX_DIM_CELL_NORMAL

      • T or NX_DIM_CELL_TOTAL

      • O or NX_DIM_CELL_OTHER

      • A or NX_DIM_CELL_AGGR

      • P or NX_DIM_CELL_PSEUDO

      • R or NX_DIM_CELL_ROOT

      • U or NX_DIM_CELL_NULL

      • G or NX_DIM_CELL_GENERATED
    qUp: int
      Number of elements that are part of the previous tail.
      This number depends on the paging, more particularly it depends on the values defined in qTop and qHeight .
    qValue: float
      Value of the cell.
      Is set to NaN , if the value is not a number.
    """

    qAttrDims: NxAttributeDimValues = None
    qAttrExps: NxAttributeExpressionValues = None
    qCanCollapse: bool = None
    qCanExpand: bool = None
    qDown: int = None
    qElemNo: int = None
    qSubNodes: list[NxPivotDimensionCell] = None
    qText: str = None
    qType: Literal[
        "NX_DIM_CELL_VALUE",
        "NX_DIM_CELL_EMPTY",
        "NX_DIM_CELL_NORMAL",
        "NX_DIM_CELL_TOTAL",
        "NX_DIM_CELL_OTHER",
        "NX_DIM_CELL_AGGR",
        "NX_DIM_CELL_PSEUDO",
        "NX_DIM_CELL_ROOT",
        "NX_DIM_CELL_NULL",
        "NX_DIM_CELL_GENERATED",
    ] = None
    qUp: int = None
    qValue: float = None

    def __init__(self_, **kvargs):
        if "qAttrDims" in kvargs and kvargs["qAttrDims"] is not None:
            if (
                type(kvargs["qAttrDims"]).__name__
                == NxPivotDimensionCell.__annotations__["qAttrDims"]
            ):
                self_.qAttrDims = kvargs["qAttrDims"]
            else:
                self_.qAttrDims = NxAttributeDimValues(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qAttrDims"],
                )
        if "qAttrExps" in kvargs and kvargs["qAttrExps"] is not None:
            if (
                type(kvargs["qAttrExps"]).__name__
                == NxPivotDimensionCell.__annotations__["qAttrExps"]
            ):
                self_.qAttrExps = kvargs["qAttrExps"]
            else:
                self_.qAttrExps = NxAttributeExpressionValues(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qAttrExps"],
                )
        if "qCanCollapse" in kvargs and kvargs["qCanCollapse"] is not None:
            self_.qCanCollapse = kvargs["qCanCollapse"]
        if "qCanExpand" in kvargs and kvargs["qCanExpand"] is not None:
            self_.qCanExpand = kvargs["qCanExpand"]
        if "qDown" in kvargs and kvargs["qDown"] is not None:
            self_.qDown = kvargs["qDown"]
        if "qElemNo" in kvargs and kvargs["qElemNo"] is not None:
            self_.qElemNo = kvargs["qElemNo"]
        if "qSubNodes" in kvargs and kvargs["qSubNodes"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxPivotDimensionCell.__annotations__["qSubNodes"]
                for e in kvargs["qSubNodes"]
            ):
                self_.qSubNodes = kvargs["qSubNodes"]
            else:
                self_.qSubNodes = [
                    NxPivotDimensionCell(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qSubNodes"]
                ]
        if "qText" in kvargs and kvargs["qText"] is not None:
            self_.qText = kvargs["qText"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        if "qUp" in kvargs and kvargs["qUp"] is not None:
            self_.qUp = kvargs["qUp"]
        if "qValue" in kvargs and kvargs["qValue"] is not None:
            self_.qValue = kvargs["qValue"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPivotPage:
    """

    Attributes
    ----------
    qArea: Rect
      Size and offset of the data in the matrix.
    qData: list[ArrayOfNxValuePoint]
      Array of data.
    qLeft: list[NxPivotDimensionCell]
      Information about the left dimension values of a pivot table.
    qTop: list[NxPivotDimensionCell]
      Information about the top dimension values of a pivot table. If there is no top dimension in the pivot table, information about the measures are given.
    """

    qArea: Rect = None
    qData: list[ArrayOfNxValuePoint] = None
    qLeft: list[NxPivotDimensionCell] = None
    qTop: list[NxPivotDimensionCell] = None

    def __init__(self_, **kvargs):
        if "qArea" in kvargs and kvargs["qArea"] is not None:
            if type(kvargs["qArea"]).__name__ == NxPivotPage.__annotations__["qArea"]:
                self_.qArea = kvargs["qArea"]
            else:
                self_.qArea = Rect(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qArea"],
                )
        if "qData" in kvargs and kvargs["qData"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NxPivotPage.__annotations__["qData"]
                for e in kvargs["qData"]
            ):
                self_.qData = kvargs["qData"]
            else:
                self_.qData = [ArrayOfNxValuePoint(e) for e in kvargs["qData"]]
        if "qLeft" in kvargs and kvargs["qLeft"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NxPivotPage.__annotations__["qLeft"]
                for e in kvargs["qLeft"]
            ):
                self_.qLeft = kvargs["qLeft"]
            else:
                self_.qLeft = [
                    NxPivotDimensionCell(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qLeft"]
                ]
        if "qTop" in kvargs and kvargs["qTop"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NxPivotPage.__annotations__["qTop"]
                for e in kvargs["qTop"]
            ):
                self_.qTop = kvargs["qTop"]
            else:
                self_.qTop = [
                    NxPivotDimensionCell(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qTop"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxPivotValuePoint:
    """

    Attributes
    ----------
    qAttrDims: NxAttributeDimValues
    qAttrExps: NxAttributeExpressionValues
      Attribute expressions values.
    qLabel: str
      Label of the cell.
      This parameter is optional.
    qNum: float
      Value of the cell.
    qText: str
      Some text related to the cell.
    qType: Literal["NX_DIM_CELL_VALUE", "NX_DIM_CELL_EMPTY", "NX_DIM_CELL_NORMAL", "NX_DIM_CELL_TOTAL", "NX_DIM_CELL_OTHER", "NX_DIM_CELL_AGGR", "NX_DIM_CELL_PSEUDO", "NX_DIM_CELL_ROOT", "NX_DIM_CELL_NULL", "NX_DIM_CELL_GENERATED"]
      Type of the cell.

      One of:

      • V or NX_DIM_CELL_VALUE

      • E or NX_DIM_CELL_EMPTY

      • N or NX_DIM_CELL_NORMAL

      • T or NX_DIM_CELL_TOTAL

      • O or NX_DIM_CELL_OTHER

      • A or NX_DIM_CELL_AGGR

      • P or NX_DIM_CELL_PSEUDO

      • R or NX_DIM_CELL_ROOT

      • U or NX_DIM_CELL_NULL

      • G or NX_DIM_CELL_GENERATED
    """

    qAttrDims: NxAttributeDimValues = None
    qAttrExps: NxAttributeExpressionValues = None
    qLabel: str = None
    qNum: float = None
    qText: str = None
    qType: Literal[
        "NX_DIM_CELL_VALUE",
        "NX_DIM_CELL_EMPTY",
        "NX_DIM_CELL_NORMAL",
        "NX_DIM_CELL_TOTAL",
        "NX_DIM_CELL_OTHER",
        "NX_DIM_CELL_AGGR",
        "NX_DIM_CELL_PSEUDO",
        "NX_DIM_CELL_ROOT",
        "NX_DIM_CELL_NULL",
        "NX_DIM_CELL_GENERATED",
    ] = None

    def __init__(self_, **kvargs):
        if "qAttrDims" in kvargs and kvargs["qAttrDims"] is not None:
            if (
                type(kvargs["qAttrDims"]).__name__
                == NxPivotValuePoint.__annotations__["qAttrDims"]
            ):
                self_.qAttrDims = kvargs["qAttrDims"]
            else:
                self_.qAttrDims = NxAttributeDimValues(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qAttrDims"],
                )
        if "qAttrExps" in kvargs and kvargs["qAttrExps"] is not None:
            if (
                type(kvargs["qAttrExps"]).__name__
                == NxPivotValuePoint.__annotations__["qAttrExps"]
            ):
                self_.qAttrExps = kvargs["qAttrExps"]
            else:
                self_.qAttrExps = NxAttributeExpressionValues(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qAttrExps"],
                )
        if "qLabel" in kvargs and kvargs["qLabel"] is not None:
            self_.qLabel = kvargs["qLabel"]
        if "qNum" in kvargs and kvargs["qNum"] is not None:
            self_.qNum = kvargs["qNum"]
        if "qText" in kvargs and kvargs["qText"] is not None:
            self_.qText = kvargs["qText"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxRange:
    """

    Attributes
    ----------
    qCount: int
      Number of characters in the field name.
    qFrom: int
      Position in the expression of the first character of the field name.
    """

    qCount: int = None
    qFrom: int = None

    def __init__(self_, **kvargs):
        if "qCount" in kvargs and kvargs["qCount"] is not None:
            self_.qCount = kvargs["qCount"]
        if "qFrom" in kvargs and kvargs["qFrom"] is not None:
            self_.qFrom = kvargs["qFrom"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxRangeSelectInfo:
    """

    Attributes
    ----------
    qMeasureIx: int
      Number of the measure to select.
      Numbering starts from 0.
    qRange: Range
      Range of values.
    """

    qMeasureIx: int = None
    qRange: Range = None

    def __init__(self_, **kvargs):
        if "qMeasureIx" in kvargs and kvargs["qMeasureIx"] is not None:
            self_.qMeasureIx = kvargs["qMeasureIx"]
        if "qRange" in kvargs and kvargs["qRange"] is not None:
            if (
                type(kvargs["qRange"]).__name__
                == NxRangeSelectInfo.__annotations__["qRange"]
            ):
                self_.qRange = kvargs["qRange"]
            else:
                self_.qRange = Range(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qRange"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxSelectionCell:
    """

    Attributes
    ----------
    qCol: int
      Column index to select.
      Indexing starts from 0.
      If the cell's type is:

      • D, the index is based on the data matrix.

      • T, the index is based on the data matrix.

      • L, the index is based on the left dimensions indexes.
    qRow: int
      Row index to select.
      Indexing starts from 0.
      If the cell's type is:

      • D, the index is based on the data matrix.

      • T, the index is based on the top dimensions indexes.

      • L, the index is based on the data matrix.
    qType: Literal["NX_CELL_DATA", "NX_CELL_TOP", "NX_CELL_LEFT"]
      Type of cells to select.

      One of:

      • D or NX_CELL_DATA

      • T or NX_CELL_TOP

      • L or NX_CELL_LEFT
    """

    qCol: int = None
    qRow: int = None
    qType: Literal["NX_CELL_DATA", "NX_CELL_TOP", "NX_CELL_LEFT"] = None

    def __init__(self_, **kvargs):
        if "qCol" in kvargs and kvargs["qCol"] is not None:
            self_.qCol = kvargs["qCol"]
        if "qRow" in kvargs and kvargs["qRow"] is not None:
            self_.qRow = kvargs["qRow"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxSelectionCellType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxSelectionInfo:
    """

    Attributes
    ----------
    qInSelections: bool
      Is set to true if the visualization is in selection mode.
      For more information about the selection mode, see BeginSelections Method.
    qMadeSelections: bool
      Is set to true if the visualization is in selection mode and if some selections have been made while in selection mode.
      For more information about the selection mode, see BeginSelections Method.
    """

    qInSelections: bool = None
    qMadeSelections: bool = None

    def __init__(self_, **kvargs):
        if "qInSelections" in kvargs and kvargs["qInSelections"] is not None:
            self_.qInSelections = kvargs["qInSelections"]
        if "qMadeSelections" in kvargs and kvargs["qMadeSelections"] is not None:
            self_.qMadeSelections = kvargs["qMadeSelections"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxSimpleDimValue:
    """

    Attributes
    ----------
    qElemNo: int
      Element number.
    qText: str
      Text related to the attribute expression value.
      This property is optional. No text is returned if the attribute expression value is a numeric.
    """

    qElemNo: int = None
    qText: str = None

    def __init__(self_, **kvargs):
        if "qElemNo" in kvargs and kvargs["qElemNo"] is not None:
            self_.qElemNo = kvargs["qElemNo"]
        if "qText" in kvargs and kvargs["qText"] is not None:
            self_.qText = kvargs["qText"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxSimpleValue:
    """

    Attributes
    ----------
    qNum: float
      Numeric value of the attribute expression.
      Set to NaN (Not a Number) if the attribute expression value is not numeric.
    qText: str
      Text related to the attribute expression value.
    """

    qNum: float = None
    qText: str = None

    def __init__(self_, **kvargs):
        if "qNum" in kvargs and kvargs["qNum"] is not None:
            self_.qNum = kvargs["qNum"]
        if "qText" in kvargs and kvargs["qText"] is not None:
            self_.qText = kvargs["qText"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxSortIndicatorType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxStackPage:
    """

    Attributes
    ----------
    qArea: Rect
      Size and offset of the data in the matrix.
    qData: list[NxStackedPivotCell]
      Array of data.
    """

    qArea: Rect = None
    qData: list[NxStackedPivotCell] = None

    def __init__(self_, **kvargs):
        if "qArea" in kvargs and kvargs["qArea"] is not None:
            if type(kvargs["qArea"]).__name__ == NxStackPage.__annotations__["qArea"]:
                self_.qArea = kvargs["qArea"]
            else:
                self_.qArea = Rect(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qArea"],
                )
        if "qData" in kvargs and kvargs["qData"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NxStackPage.__annotations__["qData"]
                for e in kvargs["qData"]
            ):
                self_.qData = kvargs["qData"]
            else:
                self_.qData = [
                    NxStackedPivotCell(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qData"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxStackedPivotCell:
    """

    Attributes
    ----------
    qAttrDims: NxAttributeDimValues
      Attribute dimensions values.
    qAttrExps: NxAttributeExpressionValues
      Attribute expressions values.
    qCanCollapse: bool
      If set to true, it means that the cell can be collapsed.
      This parameter is not returned if it is set to false.
    qCanExpand: bool
      If set to true, it means that the cell can be expanded.
      This parameter is not returned if it is set to false.
    qDown: int
      Number of elements that are part of the next tail.
    qElemNo: int
      Rank number of the value.
      If set to -1, it means that the value is not an element number.
    qMaxPos: float
      Total of the positive values in the current group of cells.
    qMinNeg: float
      Total of the negative values in the current group of cells.
    qRow: int
      Row index in the data matrix.
      The indexing starts from 0.
    qSubNodes: list[NxStackedPivotCell]
      Information about sub nodes (or sub cells).
      The array is empty [ ] when there are no sub nodes.
    qText: str
      Some text.
    qType: Literal["NX_DIM_CELL_VALUE", "NX_DIM_CELL_EMPTY", "NX_DIM_CELL_NORMAL", "NX_DIM_CELL_TOTAL", "NX_DIM_CELL_OTHER", "NX_DIM_CELL_AGGR", "NX_DIM_CELL_PSEUDO", "NX_DIM_CELL_ROOT", "NX_DIM_CELL_NULL", "NX_DIM_CELL_GENERATED"]
      Type of the cell.

      One of:

      • V or NX_DIM_CELL_VALUE

      • E or NX_DIM_CELL_EMPTY

      • N or NX_DIM_CELL_NORMAL

      • T or NX_DIM_CELL_TOTAL

      • O or NX_DIM_CELL_OTHER

      • A or NX_DIM_CELL_AGGR

      • P or NX_DIM_CELL_PSEUDO

      • R or NX_DIM_CELL_ROOT

      • U or NX_DIM_CELL_NULL

      • G or NX_DIM_CELL_GENERATED
    qUp: int
      Number of elements that are part of the previous tail.
    qValue: float
      Value of the cell.
      Is set to NaN , if the value is not a number.
    """

    qAttrDims: NxAttributeDimValues = None
    qAttrExps: NxAttributeExpressionValues = None
    qCanCollapse: bool = None
    qCanExpand: bool = None
    qDown: int = None
    qElemNo: int = None
    qMaxPos: float = None
    qMinNeg: float = None
    qRow: int = None
    qSubNodes: list[NxStackedPivotCell] = None
    qText: str = None
    qType: Literal[
        "NX_DIM_CELL_VALUE",
        "NX_DIM_CELL_EMPTY",
        "NX_DIM_CELL_NORMAL",
        "NX_DIM_CELL_TOTAL",
        "NX_DIM_CELL_OTHER",
        "NX_DIM_CELL_AGGR",
        "NX_DIM_CELL_PSEUDO",
        "NX_DIM_CELL_ROOT",
        "NX_DIM_CELL_NULL",
        "NX_DIM_CELL_GENERATED",
    ] = None
    qUp: int = None
    qValue: float = None

    def __init__(self_, **kvargs):
        if "qAttrDims" in kvargs and kvargs["qAttrDims"] is not None:
            if (
                type(kvargs["qAttrDims"]).__name__
                == NxStackedPivotCell.__annotations__["qAttrDims"]
            ):
                self_.qAttrDims = kvargs["qAttrDims"]
            else:
                self_.qAttrDims = NxAttributeDimValues(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qAttrDims"],
                )
        if "qAttrExps" in kvargs and kvargs["qAttrExps"] is not None:
            if (
                type(kvargs["qAttrExps"]).__name__
                == NxStackedPivotCell.__annotations__["qAttrExps"]
            ):
                self_.qAttrExps = kvargs["qAttrExps"]
            else:
                self_.qAttrExps = NxAttributeExpressionValues(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qAttrExps"],
                )
        if "qCanCollapse" in kvargs and kvargs["qCanCollapse"] is not None:
            self_.qCanCollapse = kvargs["qCanCollapse"]
        if "qCanExpand" in kvargs and kvargs["qCanExpand"] is not None:
            self_.qCanExpand = kvargs["qCanExpand"]
        if "qDown" in kvargs and kvargs["qDown"] is not None:
            self_.qDown = kvargs["qDown"]
        if "qElemNo" in kvargs and kvargs["qElemNo"] is not None:
            self_.qElemNo = kvargs["qElemNo"]
        if "qMaxPos" in kvargs and kvargs["qMaxPos"] is not None:
            self_.qMaxPos = kvargs["qMaxPos"]
        if "qMinNeg" in kvargs and kvargs["qMinNeg"] is not None:
            self_.qMinNeg = kvargs["qMinNeg"]
        if "qRow" in kvargs and kvargs["qRow"] is not None:
            self_.qRow = kvargs["qRow"]
        if "qSubNodes" in kvargs and kvargs["qSubNodes"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxStackedPivotCell.__annotations__["qSubNodes"]
                for e in kvargs["qSubNodes"]
            ):
                self_.qSubNodes = kvargs["qSubNodes"]
            else:
                self_.qSubNodes = [
                    NxStackedPivotCell(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qSubNodes"]
                ]
        if "qText" in kvargs and kvargs["qText"] is not None:
            self_.qText = kvargs["qText"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        if "qUp" in kvargs and kvargs["qUp"] is not None:
            self_.qUp = kvargs["qUp"]
        if "qValue" in kvargs and kvargs["qValue"] is not None:
            self_.qValue = kvargs["qValue"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxStateCounts:
    """

    Attributes
    ----------
    qAlternative: int
      Number of values in alternative state.
    qDeselected: int
      Number of values in deselected state.
    qExcluded: int
      Number of values in excluded state.
    qLocked: int
      Number of values in locked state.
    qLockedExcluded: int
      Number of values in locked excluded state.
    qOption: int
      Number of values in optional state.
    qSelected: int
      Number of values in selected state.
    qSelectedExcluded: int
      Number of values in selected excluded state.
    """

    qAlternative: int = None
    qDeselected: int = None
    qExcluded: int = None
    qLocked: int = None
    qLockedExcluded: int = None
    qOption: int = None
    qSelected: int = None
    qSelectedExcluded: int = None

    def __init__(self_, **kvargs):
        if "qAlternative" in kvargs and kvargs["qAlternative"] is not None:
            self_.qAlternative = kvargs["qAlternative"]
        if "qDeselected" in kvargs and kvargs["qDeselected"] is not None:
            self_.qDeselected = kvargs["qDeselected"]
        if "qExcluded" in kvargs and kvargs["qExcluded"] is not None:
            self_.qExcluded = kvargs["qExcluded"]
        if "qLocked" in kvargs and kvargs["qLocked"] is not None:
            self_.qLocked = kvargs["qLocked"]
        if "qLockedExcluded" in kvargs and kvargs["qLockedExcluded"] is not None:
            self_.qLockedExcluded = kvargs["qLockedExcluded"]
        if "qOption" in kvargs and kvargs["qOption"] is not None:
            self_.qOption = kvargs["qOption"]
        if "qSelected" in kvargs and kvargs["qSelected"] is not None:
            self_.qSelected = kvargs["qSelected"]
        if "qSelectedExcluded" in kvargs and kvargs["qSelectedExcluded"] is not None:
            self_.qSelectedExcluded = kvargs["qSelectedExcluded"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxStreamListEntry:
    """
    This struct is deprecated (not recommended to use).

    Attributes
    ----------
    qId: str
      Identifier of the stream.
    qName: str
      Name of the stream.
    """

    qId: str = None
    qName: str = None

    def __init__(self_, **kvargs):
        if "qId" in kvargs and kvargs["qId"] is not None:
            self_.qId = kvargs["qId"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTempBookmarkOptions:
    """

    Attributes
    ----------
    qIncludeAllPatches: bool
      IncludeAllPatches If true all patches will be stored in the temporary bookmark, if false ObjectIdsToPatch will determine what patches to include
    qIncludeVariables: bool
      IncludeVariables If true all variables will be stored in the temporary bookmark
    """

    qIncludeAllPatches: bool = None
    qIncludeVariables: bool = None

    def __init__(self_, **kvargs):
        if "qIncludeAllPatches" in kvargs and kvargs["qIncludeAllPatches"] is not None:
            self_.qIncludeAllPatches = kvargs["qIncludeAllPatches"]
        if "qIncludeVariables" in kvargs and kvargs["qIncludeVariables"] is not None:
            self_.qIncludeVariables = kvargs["qIncludeVariables"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTickCell:
    """

    Attributes
    ----------
    qEnd: float
      End value.
    qStart: float
      Start value.
    qText: str
      Tick's label.
    """

    qEnd: float = None
    qStart: float = None
    qText: str = None

    def __init__(self_, **kvargs):
        if "qEnd" in kvargs and kvargs["qEnd"] is not None:
            self_.qEnd = kvargs["qEnd"]
        if "qStart" in kvargs and kvargs["qStart"] is not None:
            self_.qStart = kvargs["qStart"]
        if "qText" in kvargs and kvargs["qText"] is not None:
            self_.qText = kvargs["qText"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTreeDataOption:
    """
    Specifies all the paging filters needed to define the tree to be fetched.

    Attributes
    ----------
    qMaxNbrOfNodes: int
      Maximum number of nodes in the tree. If this limit is exceeded, no nodes are returned. All nodes are counted.
    qTreeLevels: NxPageTreeLevel
      Filters out complete dimensions from the fetched tree.
    qTreeNodes: list[NxPageTreeNode]
      Defines areas of the tree to be fetched. Areas must be defined left to right.
    """

    qMaxNbrOfNodes: int = None
    qTreeLevels: NxPageTreeLevel = None
    qTreeNodes: list[NxPageTreeNode] = None

    def __init__(self_, **kvargs):
        if "qMaxNbrOfNodes" in kvargs and kvargs["qMaxNbrOfNodes"] is not None:
            self_.qMaxNbrOfNodes = kvargs["qMaxNbrOfNodes"]
        if "qTreeLevels" in kvargs and kvargs["qTreeLevels"] is not None:
            if (
                type(kvargs["qTreeLevels"]).__name__
                == NxTreeDataOption.__annotations__["qTreeLevels"]
            ):
                self_.qTreeLevels = kvargs["qTreeLevels"]
            else:
                self_.qTreeLevels = NxPageTreeLevel(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qTreeLevels"],
                )
        if "qTreeNodes" in kvargs and kvargs["qTreeNodes"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxTreeDataOption.__annotations__["qTreeNodes"]
                for e in kvargs["qTreeNodes"]
            ):
                self_.qTreeNodes = kvargs["qTreeNodes"]
            else:
                self_.qTreeNodes = [
                    NxPageTreeNode(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qTreeNodes"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTreeDimensionDef:
    """

    Attributes
    ----------
    qAttributeDimensions: list[NxAttrDimDef]
      List of attribute dimensions.
    qAttributeExpressions: list[NxAttrExprDef]
      List of attribute expressions.
    qCalcCondition: NxCalcCond
      Specifies a calculation condition object.
      If CalcCondition.Cond is not fulfilled, the dimension is excluded from the calculation and CalcCondition.Msg is evaluated.
      By default, there is no calculation condition.
      This property is optional.
    qDef: NxInlineDimensionDef
      Refers to a dimension.
    qLibraryId: str
      Refers to a dimension stored in the library.
    qNullSuppression: bool
      If set to true, no null values are returned.
    qOtherLabel: StringExpr
      This property is used when some dimension limits are set.
      Label of the Others group. The default label is Others .
      Example:
      "qOtherLabel":"= <label>"
      or
      "qOtherLabel":{"qExpr":"= <label>"}
      Where:

      • < label > is the label of the Others group.
    qOtherTotalSpec: OtherTotalSpecProp
      Sets the dimension limits. Each dimension of a hypercube is configured separately.
      Defines if some values (grouped as Others ) should be grouped together in the visualization.
      For example in a pie chart all values lower than 200 could be grouped together.
    qShowAll: bool
      If set to true, all dimension values are shown.
    qTotalLabel: StringExpr
      If this property is set, the total of the calculated values is returned.
      The default label is Total .
      Example:
      "qTotalLabel":"= <label>"
      or
      "qTotalLabel":{"qExpr":"= <label>"}
      Where:

      • < label > is the label of the Total group.
    qValueExprs: list[NxMeasure]
      List of measures.
    """

    qAttributeDimensions: list[NxAttrDimDef] = None
    qAttributeExpressions: list[NxAttrExprDef] = None
    qCalcCondition: NxCalcCond = None
    qDef: NxInlineDimensionDef = None
    qLibraryId: str = None
    qNullSuppression: bool = None
    qOtherLabel: StringExpr = None
    qOtherTotalSpec: OtherTotalSpecProp = None
    qShowAll: bool = None
    qTotalLabel: StringExpr = None
    qValueExprs: list[NxMeasure] = None

    def __init__(self_, **kvargs):
        if (
            "qAttributeDimensions" in kvargs
            and kvargs["qAttributeDimensions"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == NxTreeDimensionDef.__annotations__["qAttributeDimensions"]
                for e in kvargs["qAttributeDimensions"]
            ):
                self_.qAttributeDimensions = kvargs["qAttributeDimensions"]
            else:
                self_.qAttributeDimensions = [
                    NxAttrDimDef(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qAttributeDimensions"]
                ]
        if (
            "qAttributeExpressions" in kvargs
            and kvargs["qAttributeExpressions"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == NxTreeDimensionDef.__annotations__["qAttributeExpressions"]
                for e in kvargs["qAttributeExpressions"]
            ):
                self_.qAttributeExpressions = kvargs["qAttributeExpressions"]
            else:
                self_.qAttributeExpressions = [
                    NxAttrExprDef(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qAttributeExpressions"]
                ]
        if "qCalcCondition" in kvargs and kvargs["qCalcCondition"] is not None:
            if (
                type(kvargs["qCalcCondition"]).__name__
                == NxTreeDimensionDef.__annotations__["qCalcCondition"]
            ):
                self_.qCalcCondition = kvargs["qCalcCondition"]
            else:
                self_.qCalcCondition = NxCalcCond(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qCalcCondition"],
                )
        if "qDef" in kvargs and kvargs["qDef"] is not None:
            if (
                type(kvargs["qDef"]).__name__
                == NxTreeDimensionDef.__annotations__["qDef"]
            ):
                self_.qDef = kvargs["qDef"]
            else:
                self_.qDef = NxInlineDimensionDef(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qDef"],
                )
        if "qLibraryId" in kvargs and kvargs["qLibraryId"] is not None:
            self_.qLibraryId = kvargs["qLibraryId"]
        if "qNullSuppression" in kvargs and kvargs["qNullSuppression"] is not None:
            self_.qNullSuppression = kvargs["qNullSuppression"]
        if "qOtherLabel" in kvargs and kvargs["qOtherLabel"] is not None:
            if (
                type(kvargs["qOtherLabel"]).__name__
                == NxTreeDimensionDef.__annotations__["qOtherLabel"]
            ):
                self_.qOtherLabel = kvargs["qOtherLabel"]
            else:
                self_.qOtherLabel = StringExpr(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qOtherLabel"],
                )
        if "qOtherTotalSpec" in kvargs and kvargs["qOtherTotalSpec"] is not None:
            if (
                type(kvargs["qOtherTotalSpec"]).__name__
                == NxTreeDimensionDef.__annotations__["qOtherTotalSpec"]
            ):
                self_.qOtherTotalSpec = kvargs["qOtherTotalSpec"]
            else:
                self_.qOtherTotalSpec = OtherTotalSpecProp(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qOtherTotalSpec"],
                )
        if "qShowAll" in kvargs and kvargs["qShowAll"] is not None:
            self_.qShowAll = kvargs["qShowAll"]
        if "qTotalLabel" in kvargs and kvargs["qTotalLabel"] is not None:
            if (
                type(kvargs["qTotalLabel"]).__name__
                == NxTreeDimensionDef.__annotations__["qTotalLabel"]
            ):
                self_.qTotalLabel = kvargs["qTotalLabel"]
            else:
                self_.qTotalLabel = StringExpr(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qTotalLabel"],
                )
        if "qValueExprs" in kvargs and kvargs["qValueExprs"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxTreeDimensionDef.__annotations__["qValueExprs"]
                for e in kvargs["qValueExprs"]
            ):
                self_.qValueExprs = kvargs["qValueExprs"]
            else:
                self_.qValueExprs = [
                    NxMeasure(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qValueExprs"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTreeDimensionInfo:
    """

    Attributes
    ----------
    qApprMaxGlyphCount: int
      Length of the longest value in the field.
    qAttrDimInfo: list[NxAttrDimInfo]
      List of attribute dimensions.
    qAttrExprInfo: list[NxAttrExprInfo]
      List of attribute expressions.
    qCalcCondMsg: str
      The message displayed if calculation condition is not fulfilled.
    qCardinal: int
      Number of distinct field values.
    qCardinalities: NxCardinalities
      Dimension Cardinalities
    qContinuousAxes: bool
      Is continuous axis used.
    qDerivedField: bool
      Is derived field is used as a dimension.
    qDimensionType: Literal["NX_DIMENSION_TYPE_DISCRETE", "NX_DIMENSION_TYPE_NUMERIC", "NX_DIMENSION_TYPE_TIME"]
      Binary format of the field.

      One of:

      • D or NX_DIMENSION_TYPE_DISCRETE

      • N or NX_DIMENSION_TYPE_NUMERIC

      • T or NX_DIMENSION_TYPE_TIME
    qError: NxValidationError
      This parameter is optional.
      Gives information on the error.
    qFallbackTitle: str
      Corresponds to the label of the dimension that is selected.
      If the label is not defined then the field name is used.
    qGroupFallbackTitles: list[str]
      Array of dimension labels.
      Contains the labels of all dimensions in a hierarchy group (for example the labels of all dimensions in a drill down group).
    qGroupFieldDefs: list[str]
      Array of field names.
    qGroupPos: int
      Index of the dimension that is currently in use.
      qGroupPos is set to 0 if there are no hierarchical groups (drill-down groups) or cycle groups.
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"]
      Defines the grouping.

      One of:

      • N or GRP_NX_NONE

      • H or GRP_NX_HIEARCHY

      • C or GRP_NX_COLLECTION
    qIsAutoFormat: bool
      This parameter is set to true if qNumFormat is set to U (unknown). The engine guesses the type of the field based on the field's definition.
    qIsCalculated: bool
      True if this is a calculated dimension.
    qIsCyclic: bool
      Is a cyclic dimension used.
    qIsOneAndOnlyOne: bool
      If set to true, it means that the field always has one and only one selected value.
    qIsSemantic: bool
      If set to true, it means that the field is a semantic.
    qLibraryId: str
      Refers to a dimension stored in the library.
    qLocked: bool
      Is set to true if the field is locked.
    qMax: float
      Maximum value.
    qMeasureInfo: list[NxMeasureInfo]
      A List of measures to be calculated on this TreeDimension.
    qMin: float
      Minimum value.
    qNumFormat: FieldAttributes
      Format of the field.
      This parameter is optional.
    qReverseSort: bool
      If set to true, it inverts the sort criteria in the field.
    qSortIndicator: Literal["NX_SORT_INDICATE_NONE", "NX_SORT_INDICATE_ASC", "NX_SORT_INDICATE_DESC"]
      Sort indicator.
      The default value is no sorting.
      This parameter is optional.

      One of:

      • N or NX_SORT_INDICATE_NONE

      • A or NX_SORT_INDICATE_ASC

      • D or NX_SORT_INDICATE_DESC
    qStateCounts: NxStateCounts
      Number of values in a particular state.
    qTags: list[str]
      Gives information on a field. For example, it can return the type of the field.
      Examples: key, text, ASCII
    """

    qApprMaxGlyphCount: int = None
    qAttrDimInfo: list[NxAttrDimInfo] = None
    qAttrExprInfo: list[NxAttrExprInfo] = None
    qCalcCondMsg: str = None
    qCardinal: int = None
    qCardinalities: NxCardinalities = None
    qContinuousAxes: bool = None
    qDerivedField: bool = None
    qDimensionType: Literal[
        "NX_DIMENSION_TYPE_DISCRETE",
        "NX_DIMENSION_TYPE_NUMERIC",
        "NX_DIMENSION_TYPE_TIME",
    ] = None
    qError: NxValidationError = None
    qFallbackTitle: str = None
    qGroupFallbackTitles: list[str] = None
    qGroupFieldDefs: list[str] = None
    qGroupPos: int = None
    qGrouping: Literal["GRP_NX_NONE", "GRP_NX_HIEARCHY", "GRP_NX_COLLECTION"] = None
    qIsAutoFormat: bool = None
    qIsCalculated: bool = None
    qIsCyclic: bool = None
    qIsOneAndOnlyOne: bool = None
    qIsSemantic: bool = None
    qLibraryId: str = None
    qLocked: bool = None
    qMax: float = None
    qMeasureInfo: list[NxMeasureInfo] = None
    qMin: float = None
    qNumFormat: FieldAttributes = None
    qReverseSort: bool = None
    qSortIndicator: Literal[
        "NX_SORT_INDICATE_NONE", "NX_SORT_INDICATE_ASC", "NX_SORT_INDICATE_DESC"
    ] = None
    qStateCounts: NxStateCounts = None
    qTags: list[str] = None

    def __init__(self_, **kvargs):
        if "qApprMaxGlyphCount" in kvargs and kvargs["qApprMaxGlyphCount"] is not None:
            self_.qApprMaxGlyphCount = kvargs["qApprMaxGlyphCount"]
        if "qAttrDimInfo" in kvargs and kvargs["qAttrDimInfo"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxTreeDimensionInfo.__annotations__["qAttrDimInfo"]
                for e in kvargs["qAttrDimInfo"]
            ):
                self_.qAttrDimInfo = kvargs["qAttrDimInfo"]
            else:
                self_.qAttrDimInfo = [
                    NxAttrDimInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qAttrDimInfo"]
                ]
        if "qAttrExprInfo" in kvargs and kvargs["qAttrExprInfo"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxTreeDimensionInfo.__annotations__["qAttrExprInfo"]
                for e in kvargs["qAttrExprInfo"]
            ):
                self_.qAttrExprInfo = kvargs["qAttrExprInfo"]
            else:
                self_.qAttrExprInfo = [
                    NxAttrExprInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qAttrExprInfo"]
                ]
        if "qCalcCondMsg" in kvargs and kvargs["qCalcCondMsg"] is not None:
            self_.qCalcCondMsg = kvargs["qCalcCondMsg"]
        if "qCardinal" in kvargs and kvargs["qCardinal"] is not None:
            self_.qCardinal = kvargs["qCardinal"]
        if "qCardinalities" in kvargs and kvargs["qCardinalities"] is not None:
            if (
                type(kvargs["qCardinalities"]).__name__
                == NxTreeDimensionInfo.__annotations__["qCardinalities"]
            ):
                self_.qCardinalities = kvargs["qCardinalities"]
            else:
                self_.qCardinalities = NxCardinalities(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qCardinalities"],
                )
        if "qContinuousAxes" in kvargs and kvargs["qContinuousAxes"] is not None:
            self_.qContinuousAxes = kvargs["qContinuousAxes"]
        if "qDerivedField" in kvargs and kvargs["qDerivedField"] is not None:
            self_.qDerivedField = kvargs["qDerivedField"]
        if "qDimensionType" in kvargs and kvargs["qDimensionType"] is not None:
            self_.qDimensionType = kvargs["qDimensionType"]
        if "qError" in kvargs and kvargs["qError"] is not None:
            if (
                type(kvargs["qError"]).__name__
                == NxTreeDimensionInfo.__annotations__["qError"]
            ):
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qError"],
                )
        if "qFallbackTitle" in kvargs and kvargs["qFallbackTitle"] is not None:
            self_.qFallbackTitle = kvargs["qFallbackTitle"]
        if (
            "qGroupFallbackTitles" in kvargs
            and kvargs["qGroupFallbackTitles"] is not None
        ):
            self_.qGroupFallbackTitles = kvargs["qGroupFallbackTitles"]
        if "qGroupFieldDefs" in kvargs and kvargs["qGroupFieldDefs"] is not None:
            self_.qGroupFieldDefs = kvargs["qGroupFieldDefs"]
        if "qGroupPos" in kvargs and kvargs["qGroupPos"] is not None:
            self_.qGroupPos = kvargs["qGroupPos"]
        if "qGrouping" in kvargs and kvargs["qGrouping"] is not None:
            self_.qGrouping = kvargs["qGrouping"]
        if "qIsAutoFormat" in kvargs and kvargs["qIsAutoFormat"] is not None:
            self_.qIsAutoFormat = kvargs["qIsAutoFormat"]
        if "qIsCalculated" in kvargs and kvargs["qIsCalculated"] is not None:
            self_.qIsCalculated = kvargs["qIsCalculated"]
        if "qIsCyclic" in kvargs and kvargs["qIsCyclic"] is not None:
            self_.qIsCyclic = kvargs["qIsCyclic"]
        if "qIsOneAndOnlyOne" in kvargs and kvargs["qIsOneAndOnlyOne"] is not None:
            self_.qIsOneAndOnlyOne = kvargs["qIsOneAndOnlyOne"]
        if "qIsSemantic" in kvargs and kvargs["qIsSemantic"] is not None:
            self_.qIsSemantic = kvargs["qIsSemantic"]
        if "qLibraryId" in kvargs and kvargs["qLibraryId"] is not None:
            self_.qLibraryId = kvargs["qLibraryId"]
        if "qLocked" in kvargs and kvargs["qLocked"] is not None:
            self_.qLocked = kvargs["qLocked"]
        if "qMax" in kvargs and kvargs["qMax"] is not None:
            self_.qMax = kvargs["qMax"]
        if "qMeasureInfo" in kvargs and kvargs["qMeasureInfo"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxTreeDimensionInfo.__annotations__["qMeasureInfo"]
                for e in kvargs["qMeasureInfo"]
            ):
                self_.qMeasureInfo = kvargs["qMeasureInfo"]
            else:
                self_.qMeasureInfo = [
                    NxMeasureInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qMeasureInfo"]
                ]
        if "qMin" in kvargs and kvargs["qMin"] is not None:
            self_.qMin = kvargs["qMin"]
        if "qNumFormat" in kvargs and kvargs["qNumFormat"] is not None:
            if (
                type(kvargs["qNumFormat"]).__name__
                == NxTreeDimensionInfo.__annotations__["qNumFormat"]
            ):
                self_.qNumFormat = kvargs["qNumFormat"]
            else:
                self_.qNumFormat = FieldAttributes(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qNumFormat"],
                )
        if "qReverseSort" in kvargs and kvargs["qReverseSort"] is not None:
            self_.qReverseSort = kvargs["qReverseSort"]
        if "qSortIndicator" in kvargs and kvargs["qSortIndicator"] is not None:
            self_.qSortIndicator = kvargs["qSortIndicator"]
        if "qStateCounts" in kvargs and kvargs["qStateCounts"] is not None:
            if (
                type(kvargs["qStateCounts"]).__name__
                == NxTreeDimensionInfo.__annotations__["qStateCounts"]
            ):
                self_.qStateCounts = kvargs["qStateCounts"]
            else:
                self_.qStateCounts = NxStateCounts(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qStateCounts"],
                )
        if "qTags" in kvargs and kvargs["qTags"] is not None:
            self_.qTags = kvargs["qTags"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTreeMultiRangeSelectInfo:
    """

    Attributes
    ----------
    qRanges: list[NxTreeRangeSelectInfo]
      An array of Ranges.
    """

    qRanges: list[NxTreeRangeSelectInfo] = None

    def __init__(self_, **kvargs):
        if "qRanges" in kvargs and kvargs["qRanges"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == NxTreeMultiRangeSelectInfo.__annotations__["qRanges"]
                for e in kvargs["qRanges"]
            ):
                self_.qRanges = kvargs["qRanges"]
            else:
                self_.qRanges = [
                    NxTreeRangeSelectInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qRanges"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTreeNode:
    """
    Represents a dimension in the tree.

    Attributes
    ----------
    qAttrDims: NxAttributeDimValues
      Attribute dimension values.
    qAttrExps: NxAttributeExpressionValues
      Attribute expression values.
    qCanCollapse: bool
      If set to true, it means that the cell can be collapsed.
      This parameter is not returned if it is set to false.
    qCanExpand: bool
      If set to true, it means that the cell can be expanded.
      This parameter is not returned if it is set to false.
    qElemNo: int
      Element number.
    qGroupPos: int
      The position of this node inside it's group in the complete tree, i.e. Not dependant om what part is fetched.
    qGroupSize: int
      Nbr of nodes connected to this node on the next level of the tree. Not dependant on what part is fetched.
    qMaxPos: list[float]
      Total of the positive values in the current group of cells.
    qMinNeg: list[float]
      Total of the negative values in the current group of cells.
    qNodes: list[NxTreeNode]
      The children of this node in the fetched tree structure.
    qRow: int
      Row index in the data matrix.
      The indexing starts from 0.
    qState: Literal["LOCKED", "SELECTED", "OPTION", "DESELECTED", "ALTERNATIVE", "EXCLUDED", "EXCL_SELECTED", "EXCL_LOCKED", "NSTATES"]
      Selection State of the value.
      The default state for a measure is L(Locked).

      One of:

      • L or LOCKED

      • S or SELECTED

      • O or OPTION

      • D or DESELECTED

      • A or ALTERNATIVE

      • X or EXCLUDED

      • XS or EXCL_SELECTED

      • XL or EXCL_LOCKED

      • NSTATES
    qText: str
      The text version of the value, if available.
    qTreePath: list[int]
      The GroupPos of all prior nodes connected to this one, one position for each level of the tree.
      If this node is attached directly to the root, this array is empty.
    qType: Literal["NX_DIM_CELL_VALUE", "NX_DIM_CELL_EMPTY", "NX_DIM_CELL_NORMAL", "NX_DIM_CELL_TOTAL", "NX_DIM_CELL_OTHER", "NX_DIM_CELL_AGGR", "NX_DIM_CELL_PSEUDO", "NX_DIM_CELL_ROOT", "NX_DIM_CELL_NULL", "NX_DIM_CELL_GENERATED"]
      Type of the cell.

      One of:

      • V or NX_DIM_CELL_VALUE

      • E or NX_DIM_CELL_EMPTY

      • N or NX_DIM_CELL_NORMAL

      • T or NX_DIM_CELL_TOTAL

      • O or NX_DIM_CELL_OTHER

      • A or NX_DIM_CELL_AGGR

      • P or NX_DIM_CELL_PSEUDO

      • R or NX_DIM_CELL_ROOT

      • U or NX_DIM_CELL_NULL

      • G or NX_DIM_CELL_GENERATED
    qValue: float
      Value of the cell.
      Is set to NaN , if the value is not a number.
    qValues: list[NxTreeValue]
      The measures for this node.
    """

    qAttrDims: NxAttributeDimValues = None
    qAttrExps: NxAttributeExpressionValues = None
    qCanCollapse: bool = None
    qCanExpand: bool = None
    qElemNo: int = None
    qGroupPos: int = None
    qGroupSize: int = None
    qMaxPos: list[float] = None
    qMinNeg: list[float] = None
    qNodes: list[NxTreeNode] = None
    qRow: int = None
    qState: Literal[
        "LOCKED",
        "SELECTED",
        "OPTION",
        "DESELECTED",
        "ALTERNATIVE",
        "EXCLUDED",
        "EXCL_SELECTED",
        "EXCL_LOCKED",
        "NSTATES",
    ] = None
    qText: str = None
    qTreePath: list[int] = None
    qType: Literal[
        "NX_DIM_CELL_VALUE",
        "NX_DIM_CELL_EMPTY",
        "NX_DIM_CELL_NORMAL",
        "NX_DIM_CELL_TOTAL",
        "NX_DIM_CELL_OTHER",
        "NX_DIM_CELL_AGGR",
        "NX_DIM_CELL_PSEUDO",
        "NX_DIM_CELL_ROOT",
        "NX_DIM_CELL_NULL",
        "NX_DIM_CELL_GENERATED",
    ] = None
    qValue: float = None
    qValues: list[NxTreeValue] = None

    def __init__(self_, **kvargs):
        if "qAttrDims" in kvargs and kvargs["qAttrDims"] is not None:
            if (
                type(kvargs["qAttrDims"]).__name__
                == NxTreeNode.__annotations__["qAttrDims"]
            ):
                self_.qAttrDims = kvargs["qAttrDims"]
            else:
                self_.qAttrDims = NxAttributeDimValues(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qAttrDims"],
                )
        if "qAttrExps" in kvargs and kvargs["qAttrExps"] is not None:
            if (
                type(kvargs["qAttrExps"]).__name__
                == NxTreeNode.__annotations__["qAttrExps"]
            ):
                self_.qAttrExps = kvargs["qAttrExps"]
            else:
                self_.qAttrExps = NxAttributeExpressionValues(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qAttrExps"],
                )
        if "qCanCollapse" in kvargs and kvargs["qCanCollapse"] is not None:
            self_.qCanCollapse = kvargs["qCanCollapse"]
        if "qCanExpand" in kvargs and kvargs["qCanExpand"] is not None:
            self_.qCanExpand = kvargs["qCanExpand"]
        if "qElemNo" in kvargs and kvargs["qElemNo"] is not None:
            self_.qElemNo = kvargs["qElemNo"]
        if "qGroupPos" in kvargs and kvargs["qGroupPos"] is not None:
            self_.qGroupPos = kvargs["qGroupPos"]
        if "qGroupSize" in kvargs and kvargs["qGroupSize"] is not None:
            self_.qGroupSize = kvargs["qGroupSize"]
        if "qMaxPos" in kvargs and kvargs["qMaxPos"] is not None:
            self_.qMaxPos = kvargs["qMaxPos"]
        if "qMinNeg" in kvargs and kvargs["qMinNeg"] is not None:
            self_.qMinNeg = kvargs["qMinNeg"]
        if "qNodes" in kvargs and kvargs["qNodes"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NxTreeNode.__annotations__["qNodes"]
                for e in kvargs["qNodes"]
            ):
                self_.qNodes = kvargs["qNodes"]
            else:
                self_.qNodes = [
                    NxTreeNode(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qNodes"]
                ]
        if "qRow" in kvargs and kvargs["qRow"] is not None:
            self_.qRow = kvargs["qRow"]
        if "qState" in kvargs and kvargs["qState"] is not None:
            self_.qState = kvargs["qState"]
        if "qText" in kvargs and kvargs["qText"] is not None:
            self_.qText = kvargs["qText"]
        if "qTreePath" in kvargs and kvargs["qTreePath"] is not None:
            self_.qTreePath = kvargs["qTreePath"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        if "qValue" in kvargs and kvargs["qValue"] is not None:
            self_.qValue = kvargs["qValue"]
        if "qValues" in kvargs and kvargs["qValues"] is not None:
            if all(
                f"list[{type(e).__name__}]" == NxTreeNode.__annotations__["qValues"]
                for e in kvargs["qValues"]
            ):
                self_.qValues = kvargs["qValues"]
            else:
                self_.qValues = [
                    NxTreeValue(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qValues"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTreeRangeSelectInfo:
    """

    Attributes
    ----------
    qDimensionIx: int
      Number of the dimension to select
      measure from.  Numbering starts from 0.
    qMeasureIx: int
      Number of the measure to select.
      Numbering starts from 0.
    qRange: Range
      Range of values.
    """

    qDimensionIx: int = None
    qMeasureIx: int = None
    qRange: Range = None

    def __init__(self_, **kvargs):
        if "qDimensionIx" in kvargs and kvargs["qDimensionIx"] is not None:
            self_.qDimensionIx = kvargs["qDimensionIx"]
        if "qMeasureIx" in kvargs and kvargs["qMeasureIx"] is not None:
            self_.qMeasureIx = kvargs["qMeasureIx"]
        if "qRange" in kvargs and kvargs["qRange"] is not None:
            if (
                type(kvargs["qRange"]).__name__
                == NxTreeRangeSelectInfo.__annotations__["qRange"]
            ):
                self_.qRange = kvargs["qRange"]
            else:
                self_.qRange = Range(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qRange"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTreeValue:
    """
    Represents a measure.

    Attributes
    ----------
    qAttrDims: NxAttributeDimValues
      Attribute dimension values.
    qAttrExps: NxAttributeExpressionValues
      Attribute expression values.
    qText: str
      The text version of the value, if available.
    qValue: float
      Value of the cell.
      Is set to NaN , if the value is not a number.
    """

    qAttrDims: NxAttributeDimValues = None
    qAttrExps: NxAttributeExpressionValues = None
    qText: str = None
    qValue: float = None

    def __init__(self_, **kvargs):
        if "qAttrDims" in kvargs and kvargs["qAttrDims"] is not None:
            if (
                type(kvargs["qAttrDims"]).__name__
                == NxTreeValue.__annotations__["qAttrDims"]
            ):
                self_.qAttrDims = kvargs["qAttrDims"]
            else:
                self_.qAttrDims = NxAttributeDimValues(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qAttrDims"],
                )
        if "qAttrExps" in kvargs and kvargs["qAttrExps"] is not None:
            if (
                type(kvargs["qAttrExps"]).__name__
                == NxTreeValue.__annotations__["qAttrExps"]
            ):
                self_.qAttrExps = kvargs["qAttrExps"]
            else:
                self_.qAttrExps = NxAttributeExpressionValues(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qAttrExps"],
                )
        if "qText" in kvargs and kvargs["qText"] is not None:
            self_.qText = kvargs["qText"]
        if "qValue" in kvargs and kvargs["qValue"] is not None:
            self_.qValue = kvargs["qValue"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTrendline:
    """
    Information about the calculated trendline.

    Attributes
    ----------
    qCoeff: list[float]
      Coefficent c0..cN depending on the trendline type.
    qElemNo: int
      Inner Dim elem no
    qError: NxValidationError
      This parameter is optional and is displayed in case of error.
    qExpression: str
      Trendline expression
    qR2: float
      R2 score. Value between 0..1 that shows the correlation between the trendline and the data. Higher value means higher correlation.
    qType: Literal["Average", "Linear", "Polynomial2", "Polynomial3", "Polynomial4", "Exponential", "Power", "Logarithmic"]
      Type of trendline

      One of:

      • AVERAGE or Average

      • LINEAR or Linear

      • POLYNOMIAL2 or Polynomial2

      • POLYNOMIAL3 or Polynomial3

      • POLYNOMIAL4 or Polynomial4

      • EXPONENTIAL or Exponential

      • POWER or Power

      • LOG or Logarithmic
    """

    qCoeff: list[float] = None
    qElemNo: int = None
    qError: NxValidationError = None
    qExpression: str = None
    qR2: float = None
    qType: Literal[
        "Average",
        "Linear",
        "Polynomial2",
        "Polynomial3",
        "Polynomial4",
        "Exponential",
        "Power",
        "Logarithmic",
    ] = None

    def __init__(self_, **kvargs):
        if "qCoeff" in kvargs and kvargs["qCoeff"] is not None:
            self_.qCoeff = kvargs["qCoeff"]
        if "qElemNo" in kvargs and kvargs["qElemNo"] is not None:
            self_.qElemNo = kvargs["qElemNo"]
        if "qError" in kvargs and kvargs["qError"] is not None:
            if type(kvargs["qError"]).__name__ == NxTrendline.__annotations__["qError"]:
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qError"],
                )
        if "qExpression" in kvargs and kvargs["qExpression"] is not None:
            self_.qExpression = kvargs["qExpression"]
        if "qR2" in kvargs and kvargs["qR2"] is not None:
            self_.qR2 = kvargs["qR2"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTrendlineDef:
    """
    Trendline input definition

    Attributes
    ----------
    qCalcR2: bool
      Set to true to calulatate the R2 score
    qContinuousXAxis: Literal["CONTINUOUS_NEVER", "CONTINUOUS_IF_POSSIBLE", "CONTINUOUS_IF_TIME"]
      Set if the numerical value of x axis dimension should be used

      One of:

      • Never or CONTINUOUS_NEVER

      • Possible or CONTINUOUS_IF_POSSIBLE

      • Time or CONTINUOUS_IF_TIME
    qMultiDimMode: Literal["TRENDLINE_MULTILINE", "TRENDLINE_SUM"]
      If you have a hypercube with two dimensions and qXColIx refers to a dimension
      This determines if you get one trendline of each value in the other dimension or
      Or trendline based on the sum of the value in the other dimension
      The sum variant is only supported when qXColIx is 0 and qMode (on the hypercube) is K or T

      One of:

      • Multi or TRENDLINE_MULTILINE

      • Sum or TRENDLINE_SUM
    qType: Literal["Average", "Linear", "Polynomial2", "Polynomial3", "Polynomial4", "Exponential", "Power", "Logarithmic"]
      The type of trendline to calculate

      One of:

      • AVERAGE or Average

      • LINEAR or Linear

      • POLYNOMIAL2 or Polynomial2

      • POLYNOMIAL3 or Polynomial3

      • POLYNOMIAL4 or Polynomial4

      • EXPONENTIAL or Exponential

      • POWER or Power

      • LOG or Logarithmic
    qXColIx: int
      The column in the hypercube to be used as x axis. Can point to either a dimension (numeric or text) or a measure
    """

    qCalcR2: bool = None
    qContinuousXAxis: Literal[
        "CONTINUOUS_NEVER", "CONTINUOUS_IF_POSSIBLE", "CONTINUOUS_IF_TIME"
    ] = "CONTINUOUS_NEVER"
    qMultiDimMode: Literal[
        "TRENDLINE_MULTILINE", "TRENDLINE_SUM"
    ] = "TRENDLINE_MULTILINE"
    qType: Literal[
        "Average",
        "Linear",
        "Polynomial2",
        "Polynomial3",
        "Polynomial4",
        "Exponential",
        "Power",
        "Logarithmic",
    ] = None
    qXColIx: int = -1

    def __init__(self_, **kvargs):
        if "qCalcR2" in kvargs and kvargs["qCalcR2"] is not None:
            self_.qCalcR2 = kvargs["qCalcR2"]
        if "qContinuousXAxis" in kvargs and kvargs["qContinuousXAxis"] is not None:
            self_.qContinuousXAxis = kvargs["qContinuousXAxis"]
        if "qMultiDimMode" in kvargs and kvargs["qMultiDimMode"] is not None:
            self_.qMultiDimMode = kvargs["qMultiDimMode"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        if "qXColIx" in kvargs and kvargs["qXColIx"] is not None:
            self_.qXColIx = kvargs["qXColIx"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxTrendlineMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxValidationError:
    """

    Attributes
    ----------
    qContext: str
      Context related to the error, from the user app domain.
      It can be the identifier of an object, a field name, a table name.
      This parameter is optional.
    qErrorCode: int
      Error code.
      This parameter is always displayed in case of error.
    qExtendedMessage: str
      Internal information from the server.
      This parameter is optional.
    """

    qContext: str = None
    qErrorCode: int = None
    qExtendedMessage: str = None

    def __init__(self_, **kvargs):
        if "qContext" in kvargs and kvargs["qContext"] is not None:
            self_.qContext = kvargs["qContext"]
        if "qErrorCode" in kvargs and kvargs["qErrorCode"] is not None:
            self_.qErrorCode = kvargs["qErrorCode"]
        if "qExtendedMessage" in kvargs and kvargs["qExtendedMessage"] is not None:
            self_.qExtendedMessage = kvargs["qExtendedMessage"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxVariableListItem:
    """

    Attributes
    ----------
    qData: JsonObject
      Data.
    qDefinition: str
      Definition of the variable. It can be a value or an expression.
    qDescription: str
      Description of the variable.
    qInfo: NxInfo
      Identifier and type of the object.
      This parameter is mandatory.
    qIsConfig: bool
      If set to true, it means that the variable is a system variable.
      A system variable provides information about the system and is set by the engine. The content cannot be changed by the user.
      This parameter is optional.
      The default value is false.
    qIsReserved: bool
      If set to true, it means that the variable is reserved.
      The default value is false.
      This parameter is optional.
      Examples:

      • ScriptError is a reserved variable, set by the engine.

      • DayNames is a reserved variable, set by the user.
    qIsScriptCreated: bool
      If set to true, it means that the variable was defined via script.
    qMeta: NxMeta
      Information about publishing and permissions.
      This parameter is optional.
    qName: str
      Name of the variable.
    """

    qData: JsonObject = None
    qDefinition: str = None
    qDescription: str = None
    qInfo: NxInfo = None
    qIsConfig: bool = None
    qIsReserved: bool = None
    qIsScriptCreated: bool = None
    qMeta: NxMeta = None
    qName: str = None

    def __init__(self_, **kvargs):
        if "qData" in kvargs and kvargs["qData"] is not None:
            if (
                type(kvargs["qData"]).__name__
                == NxVariableListItem.__annotations__["qData"]
            ):
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qData"],
                )
        if "qDefinition" in kvargs and kvargs["qDefinition"] is not None:
            self_.qDefinition = kvargs["qDefinition"]
        if "qDescription" in kvargs and kvargs["qDescription"] is not None:
            self_.qDescription = kvargs["qDescription"]
        if "qInfo" in kvargs and kvargs["qInfo"] is not None:
            if (
                type(kvargs["qInfo"]).__name__
                == NxVariableListItem.__annotations__["qInfo"]
            ):
                self_.qInfo = kvargs["qInfo"]
            else:
                self_.qInfo = NxInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qInfo"],
                )
        if "qIsConfig" in kvargs and kvargs["qIsConfig"] is not None:
            self_.qIsConfig = kvargs["qIsConfig"]
        if "qIsReserved" in kvargs and kvargs["qIsReserved"] is not None:
            self_.qIsReserved = kvargs["qIsReserved"]
        if "qIsScriptCreated" in kvargs and kvargs["qIsScriptCreated"] is not None:
            self_.qIsScriptCreated = kvargs["qIsScriptCreated"]
        if "qMeta" in kvargs and kvargs["qMeta"] is not None:
            if (
                type(kvargs["qMeta"]).__name__
                == NxVariableListItem.__annotations__["qMeta"]
            ):
                self_.qMeta = kvargs["qMeta"]
            else:
                self_.qMeta = NxMeta(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qMeta"],
                )
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxVariableProperties:
    """

    Attributes
    ----------
    qIncludeInBookmark: bool
      Set this property to true to update the variable when applying a bookmark.
      The value of a variable can affect the state of the selections.
      The default value is false.
    qName: str
      Name of the variable.
    qNumberPresentation: FieldAttributes
      Defines the format of the value of a variable.
    qPreDefinedList: list[str]
      List of enumerations.
      This property is used if qUsePredefListedValues is set to true.
    qUsePredefListedValues: bool
      The value of a variable can be an enumeration.
      Set this property to true to reflect the predefined values in an enumeration.
    """

    qIncludeInBookmark: bool = None
    qName: str = None
    qNumberPresentation: FieldAttributes = None
    qPreDefinedList: list[str] = None
    qUsePredefListedValues: bool = None

    def __init__(self_, **kvargs):
        if "qIncludeInBookmark" in kvargs and kvargs["qIncludeInBookmark"] is not None:
            self_.qIncludeInBookmark = kvargs["qIncludeInBookmark"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if (
            "qNumberPresentation" in kvargs
            and kvargs["qNumberPresentation"] is not None
        ):
            if (
                type(kvargs["qNumberPresentation"]).__name__
                == NxVariableProperties.__annotations__["qNumberPresentation"]
            ):
                self_.qNumberPresentation = kvargs["qNumberPresentation"]
            else:
                self_.qNumberPresentation = FieldAttributes(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qNumberPresentation"],
                )
        if "qPreDefinedList" in kvargs and kvargs["qPreDefinedList"] is not None:
            self_.qPreDefinedList = kvargs["qPreDefinedList"]
        if (
            "qUsePredefListedValues" in kvargs
            and kvargs["qUsePredefListedValues"] is not None
        ):
            self_.qUsePredefListedValues = kvargs["qUsePredefListedValues"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class NxViewPort:
    """

    Attributes
    ----------
    qHeight: int
      Height of the canvas in pixels.
    qWidth: int
      Width of the canvas in pixels.
    qZoomLevel: int
      Zoom level.
    """

    qHeight: int = None
    qWidth: int = None
    qZoomLevel: int = None

    def __init__(self_, **kvargs):
        if "qHeight" in kvargs and kvargs["qHeight"] is not None:
            self_.qHeight = kvargs["qHeight"]
        if "qWidth" in kvargs and kvargs["qWidth"] is not None:
            self_.qWidth = kvargs["qWidth"]
        if "qZoomLevel" in kvargs and kvargs["qZoomLevel"] is not None:
            self_.qZoomLevel = kvargs["qZoomLevel"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ObjectInterface:
    """

    Attributes
    ----------
    qGenericId: str
      Object ID.
    qGenericType: str
      The type of the object.
    qHandle: int
      The handle used to connect to object.
    qType: str
      The native type of the object.
    """

    qGenericId: str = None
    qGenericType: str = None
    qHandle: int = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qGenericId" in kvargs and kvargs["qGenericId"] is not None:
            self_.qGenericId = kvargs["qGenericId"]
        if "qGenericType" in kvargs and kvargs["qGenericType"] is not None:
            self_.qGenericType = kvargs["qGenericType"]
        if "qHandle" in kvargs and kvargs["qHandle"] is not None:
            self_.qHandle = kvargs["qHandle"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def on(self, event_name, listener):
        self._session.on_handle(self.qHandle, event_name, listener)


@dataclass
class OdbcDsn:
    """

    Attributes
    ----------
    qBit32: bool
      Is set to true if the version of ODBC is 32-bit.
      This parameter is optional. Default is false.
    qDescription: str
      Description of the ODBC connection.
    qName: str
      Name of the ODBC connection.
    qUserOnly: bool
      Is set to true if the connection is User DSN. The connection works only for a specific user.
      Default is false.
      This parameter is optional.
    """

    qBit32: bool = None
    qDescription: str = None
    qName: str = None
    qUserOnly: bool = None

    def __init__(self_, **kvargs):
        if "qBit32" in kvargs and kvargs["qBit32"] is not None:
            self_.qBit32 = kvargs["qBit32"]
        if "qDescription" in kvargs and kvargs["qDescription"] is not None:
            self_.qDescription = kvargs["qDescription"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qUserOnly" in kvargs and kvargs["qUserOnly"] is not None:
            self_.qUserOnly = kvargs["qUserOnly"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class OleDbProvider:
    """

    Attributes
    ----------
    qBit32: bool
      Is set to true if the version of the OLEDB provider is 32-bit.
      Default is false.
      This parameter is optional.
    qDescription: str
      Description of the OLEDB provider.
    qName: str
      Name of the OLEDB provider.
    """

    qBit32: bool = None
    qDescription: str = None
    qName: str = None

    def __init__(self_, **kvargs):
        if "qBit32" in kvargs and kvargs["qBit32"] is not None:
            self_.qBit32 = kvargs["qBit32"]
        if "qDescription" in kvargs and kvargs["qDescription"] is not None:
            self_.qDescription = kvargs["qDescription"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class OtherLimitMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class OtherMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class OtherSortMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class OtherTotalSpecProp:
    """

    Attributes
    ----------
    qApplyEvenWhenPossiblyWrongResult: bool
      Set this parameter to true to allow the calculation of Others even if the engine detects some potential mistakes.
      For example the country Russia is part of the continent Europe and Asia. If you have an hypercube with two dimensions Country and Continent and one measure Population, the engine can detect that the population of Russia is included in both the continent Asia and Europe.
      The default value is true.
    qForceBadValueKeeping: bool
      This parameter is used when qOtherMode is set to:

      • OTHER_ABS_LIMITED

      • OTHER_REL_LIMITED

      • OTHER_ABS_ACC_TARGET
      OTHER_REL_ACC_TARGET

      and when the dimension values include not numeric values.
      Set this parameter to true to include text values in the returned values.
      The default value is true.
    qGlobalOtherGrouping: bool
      This parameter applies to inner dimensions.
      If this parameter is set to true, the restrictions are calculated on the selected dimension only. All previous dimensions are ignored.
      The default value is false.
    qOtherCollapseInnerDimensions: bool
      If set to true, it collapses the inner dimensions (if any) in the group Others .
      The default value is false.
    qOtherCounted: ValueExpr
      Number of values to display. The number of values can be entered as a calculated formula.
      This parameter is used when qOtherMode is set to OTHER_COUNTED .
    qOtherLimit: ValueExpr
      Value used to limit the dimension values. The limit can be entered as a calculated formula.
      This parameter is used when qOtherMode is set to:

      • OTHER_ABS_LIMITED

      • OTHER_REL_LIMITED

      • OTHER_ABS_ACC_TARGET
      OTHER_REL_ACC_TARGET
    qOtherLimitMode: Literal["OTHER_GE_LIMIT", "OTHER_LE_LIMIT", "OTHER_GT_LIMIT", "OTHER_LT_LIMIT"]
      Sets the limit for the Others mode.
      This parameter is used when qOtherMode is set to:

      • OTHER_ABS_LIMITED

      • OTHER_REL_LIMITED

      • OTHER_ABS_ACC_TARGET
      OTHER_REL_ACC_TARGET

      One of:

      • OTHER_GE_LIMIT

      • OTHER_LE_LIMIT

      • OTHER_GT_LIMIT

      • OTHER_LT_LIMIT
    qOtherMode: Literal["OTHER_OFF", "OTHER_COUNTED", "OTHER_ABS_LIMITED", "OTHER_ABS_ACC_TARGET", "OTHER_REL_LIMITED", "OTHER_REL_ACC_TARGET"]
      Determines how many dimension values are displayed.
      The default value is OTHER_OFF .

      One of:

      • OTHER_OFF

      • OTHER_COUNTED

      • OTHER_ABS_LIMITED

      • OTHER_ABS_ACC_TARGET

      • OTHER_REL_LIMITED

      • OTHER_REL_ACC_TARGET
    qOtherSortMode: Literal["OTHER_SORT_DEFAULT", "OTHER_SORT_DESCENDING", "OTHER_SORT_ASCENDING"]
      Defines the sort order of the dimension values.
      The default value is OTHER_SORT_DESCENDING .

      One of:

      • OTHER_SORT_DEFAULT

      • OTHER_SORT_DESCENDING

      • OTHER_SORT_ASCENDING
    qReferencedExpression: StringExpr
      This parameter applies when there are several measures.
      Name of the measure to use for the calculation of Others for a specific dimension.
    qSuppressOther: bool
      If set to true, the group Others is not displayed as a dimension value.
      The default value is false.
    qTotalMode: Literal["TOTAL_OFF", "TOTAL_EXPR"]
      If set to TOTAL_EXPR , the total of the dimension values is returned.
      The default value is TOTAL_OFF .

      One of:

      • TOTAL_OFF

      • TOTAL_EXPR
    """

    qApplyEvenWhenPossiblyWrongResult: bool = True
    qForceBadValueKeeping: bool = True
    qGlobalOtherGrouping: bool = None
    qOtherCollapseInnerDimensions: bool = None
    qOtherCounted: ValueExpr = None
    qOtherLimit: ValueExpr = None
    qOtherLimitMode: Literal[
        "OTHER_GE_LIMIT", "OTHER_LE_LIMIT", "OTHER_GT_LIMIT", "OTHER_LT_LIMIT"
    ] = "OTHER_GT_LIMIT"
    qOtherMode: Literal[
        "OTHER_OFF",
        "OTHER_COUNTED",
        "OTHER_ABS_LIMITED",
        "OTHER_ABS_ACC_TARGET",
        "OTHER_REL_LIMITED",
        "OTHER_REL_ACC_TARGET",
    ] = "OTHER_OFF"
    qOtherSortMode: Literal[
        "OTHER_SORT_DEFAULT", "OTHER_SORT_DESCENDING", "OTHER_SORT_ASCENDING"
    ] = "OTHER_SORT_DESCENDING"
    qReferencedExpression: StringExpr = None
    qSuppressOther: bool = None
    qTotalMode: Literal["TOTAL_OFF", "TOTAL_EXPR"] = "TOTAL_OFF"

    def __init__(self_, **kvargs):
        if (
            "qApplyEvenWhenPossiblyWrongResult" in kvargs
            and kvargs["qApplyEvenWhenPossiblyWrongResult"] is not None
        ):
            self_.qApplyEvenWhenPossiblyWrongResult = kvargs[
                "qApplyEvenWhenPossiblyWrongResult"
            ]
        if (
            "qForceBadValueKeeping" in kvargs
            and kvargs["qForceBadValueKeeping"] is not None
        ):
            self_.qForceBadValueKeeping = kvargs["qForceBadValueKeeping"]
        if (
            "qGlobalOtherGrouping" in kvargs
            and kvargs["qGlobalOtherGrouping"] is not None
        ):
            self_.qGlobalOtherGrouping = kvargs["qGlobalOtherGrouping"]
        if (
            "qOtherCollapseInnerDimensions" in kvargs
            and kvargs["qOtherCollapseInnerDimensions"] is not None
        ):
            self_.qOtherCollapseInnerDimensions = kvargs[
                "qOtherCollapseInnerDimensions"
            ]
        if "qOtherCounted" in kvargs and kvargs["qOtherCounted"] is not None:
            if (
                type(kvargs["qOtherCounted"]).__name__
                == OtherTotalSpecProp.__annotations__["qOtherCounted"]
            ):
                self_.qOtherCounted = kvargs["qOtherCounted"]
            else:
                self_.qOtherCounted = ValueExpr(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qOtherCounted"],
                )
        if "qOtherLimit" in kvargs and kvargs["qOtherLimit"] is not None:
            if (
                type(kvargs["qOtherLimit"]).__name__
                == OtherTotalSpecProp.__annotations__["qOtherLimit"]
            ):
                self_.qOtherLimit = kvargs["qOtherLimit"]
            else:
                self_.qOtherLimit = ValueExpr(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qOtherLimit"],
                )
        if "qOtherLimitMode" in kvargs and kvargs["qOtherLimitMode"] is not None:
            self_.qOtherLimitMode = kvargs["qOtherLimitMode"]
        if "qOtherMode" in kvargs and kvargs["qOtherMode"] is not None:
            self_.qOtherMode = kvargs["qOtherMode"]
        if "qOtherSortMode" in kvargs and kvargs["qOtherSortMode"] is not None:
            self_.qOtherSortMode = kvargs["qOtherSortMode"]
        if (
            "qReferencedExpression" in kvargs
            and kvargs["qReferencedExpression"] is not None
        ):
            if (
                type(kvargs["qReferencedExpression"]).__name__
                == OtherTotalSpecProp.__annotations__["qReferencedExpression"]
            ):
                self_.qReferencedExpression = kvargs["qReferencedExpression"]
            else:
                self_.qReferencedExpression = StringExpr(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qReferencedExpression"],
                )
        if "qSuppressOther" in kvargs and kvargs["qSuppressOther"] is not None:
            self_.qSuppressOther = kvargs["qSuppressOther"]
        if "qTotalMode" in kvargs and kvargs["qTotalMode"] is not None:
            self_.qTotalMode = kvargs["qTotalMode"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Point:
    """

    Attributes
    ----------
    qx: int
      x-coordinate in pixels.
      The origin is the top left of the screen.
    qy: int
      y-coordinate in pixels.
      The origin is the top left of the screen.
    """

    qx: int = None
    qy: int = None

    def __init__(self_, **kvargs):
        if "qx" in kvargs and kvargs["qx"] is not None:
            self_.qx = kvargs["qx"]
        if "qy" in kvargs and kvargs["qy"] is not None:
            self_.qy = kvargs["qy"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class PositionMark:
    """

    Attributes
    ----------
    qDimName: str
    qElemNo: list[int]
    qElemValues: list[Blob]
    """

    qDimName: str = None
    qElemNo: list[int] = None
    qElemValues: list[Blob] = None

    def __init__(self_, **kvargs):
        if "qDimName" in kvargs and kvargs["qDimName"] is not None:
            self_.qDimName = kvargs["qDimName"]
        if "qElemNo" in kvargs and kvargs["qElemNo"] is not None:
            self_.qElemNo = kvargs["qElemNo"]
        if "qElemValues" in kvargs and kvargs["qElemValues"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == PositionMark.__annotations__["qElemValues"]
                for e in kvargs["qElemValues"]
            ):
                self_.qElemValues = kvargs["qElemValues"]
            else:
                self_.qElemValues = [
                    Blob(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qElemValues"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ProgressData:
    """

    Attributes
    ----------
    qCompleted: int
      This property is not used.
    qErrorData: list[ErrorData]
      Information about the error messages that occur during the script execution.
    qFinished: bool
      True if the request is finished.
    qKB: int
      This property is not used.
    qMillisecs: int
      Request duration in milliseconds.
    qPersistentProgress: str
      A progress message is persistent when it informs about the start or end of a statement. For example, it can inform about the total number of lines fetched from a data source or tell that the app was saved. All persistent progress messages between two *GetProgress* calls are summarized in this string. Contrarily to *qPersistentProgressMessages*, the content of the localized message string is displayed (not its message code).
    qPersistentProgressMessages: list[ProgressMessage]
      List of persistent progress messages.
    qStarted: bool
      True if the request is started.
    qTotal: int
      This property is not used.
    qTransientProgress: str
      A progress message is transient when it informs about the progress of an ongoing statement. For example, it can tell how many lines are currently fetched from a data source. All transient progress messages between two *GetProgress* calls are summarized in this string. Contrarily to *qTransientProgressMessage*, the content of the localized message string is displayed (not its message code).
    qTransientProgressMessage: ProgressMessage
      Transient progress message.
    qUserInteractionWanted: bool
      True when the engine pauses the script execution and waits for a user interaction.
    """

    qCompleted: int = None
    qErrorData: list[ErrorData] = None
    qFinished: bool = None
    qKB: int = None
    qMillisecs: int = None
    qPersistentProgress: str = None
    qPersistentProgressMessages: list[ProgressMessage] = None
    qStarted: bool = None
    qTotal: int = None
    qTransientProgress: str = None
    qTransientProgressMessage: ProgressMessage = None
    qUserInteractionWanted: bool = None

    def __init__(self_, **kvargs):
        if "qCompleted" in kvargs and kvargs["qCompleted"] is not None:
            self_.qCompleted = kvargs["qCompleted"]
        if "qErrorData" in kvargs and kvargs["qErrorData"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == ProgressData.__annotations__["qErrorData"]
                for e in kvargs["qErrorData"]
            ):
                self_.qErrorData = kvargs["qErrorData"]
            else:
                self_.qErrorData = [
                    ErrorData(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qErrorData"]
                ]
        if "qFinished" in kvargs and kvargs["qFinished"] is not None:
            self_.qFinished = kvargs["qFinished"]
        if "qKB" in kvargs and kvargs["qKB"] is not None:
            self_.qKB = kvargs["qKB"]
        if "qMillisecs" in kvargs and kvargs["qMillisecs"] is not None:
            self_.qMillisecs = kvargs["qMillisecs"]
        if (
            "qPersistentProgress" in kvargs
            and kvargs["qPersistentProgress"] is not None
        ):
            self_.qPersistentProgress = kvargs["qPersistentProgress"]
        if (
            "qPersistentProgressMessages" in kvargs
            and kvargs["qPersistentProgressMessages"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == ProgressData.__annotations__["qPersistentProgressMessages"]
                for e in kvargs["qPersistentProgressMessages"]
            ):
                self_.qPersistentProgressMessages = kvargs[
                    "qPersistentProgressMessages"
                ]
            else:
                self_.qPersistentProgressMessages = [
                    ProgressMessage(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qPersistentProgressMessages"]
                ]
        if "qStarted" in kvargs and kvargs["qStarted"] is not None:
            self_.qStarted = kvargs["qStarted"]
        if "qTotal" in kvargs and kvargs["qTotal"] is not None:
            self_.qTotal = kvargs["qTotal"]
        if "qTransientProgress" in kvargs and kvargs["qTransientProgress"] is not None:
            self_.qTransientProgress = kvargs["qTransientProgress"]
        if (
            "qTransientProgressMessage" in kvargs
            and kvargs["qTransientProgressMessage"] is not None
        ):
            if (
                type(kvargs["qTransientProgressMessage"]).__name__
                == ProgressData.__annotations__["qTransientProgressMessage"]
            ):
                self_.qTransientProgressMessage = kvargs["qTransientProgressMessage"]
            else:
                self_.qTransientProgressMessage = ProgressMessage(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qTransientProgressMessage"],
                )
        if (
            "qUserInteractionWanted" in kvargs
            and kvargs["qUserInteractionWanted"] is not None
        ):
            self_.qUserInteractionWanted = kvargs["qUserInteractionWanted"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ProgressMessage:
    """

    Attributes
    ----------
    qMessageCode: int
      Code number to the corresponding localized message string.
    qMessageParameters: list[str]
      Parameters to be inserted in the localized message string.
    """

    qMessageCode: int = None
    qMessageParameters: list[str] = None

    def __init__(self_, **kvargs):
        if "qMessageCode" in kvargs and kvargs["qMessageCode"] is not None:
            self_.qMessageCode = kvargs["qMessageCode"]
        if "qMessageParameters" in kvargs and kvargs["qMessageParameters"] is not None:
            self_.qMessageParameters = kvargs["qMessageParameters"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Range:
    """

    Attributes
    ----------
    qMax: float
      Highest value in the range
    qMaxInclEq: bool
      If set to true, the range includes the highest value in the range of selections (Equals to ). [bn(50500)]
      Example:
      The range is [1,10]. If qMinInclEq is set to true it means that 10 is included in the range of selections.
    qMin: float
      Lowest value in the range
    qMinInclEq: bool
      If set to true, the range includes the lowest value in the range of selections (Equals to ). [bn(50500)]
      Example:
      The range is [1,10]. If qMinInclEq is set to true it means that 1 is included in the range of selections.
    """

    qMax: float = None
    qMaxInclEq: bool = None
    qMin: float = None
    qMinInclEq: bool = None

    def __init__(self_, **kvargs):
        if "qMax" in kvargs and kvargs["qMax"] is not None:
            self_.qMax = kvargs["qMax"]
        if "qMaxInclEq" in kvargs and kvargs["qMaxInclEq"] is not None:
            self_.qMaxInclEq = kvargs["qMaxInclEq"]
        if "qMin" in kvargs and kvargs["qMin"] is not None:
            self_.qMin = kvargs["qMin"]
        if "qMinInclEq" in kvargs and kvargs["qMinInclEq"] is not None:
            self_.qMinInclEq = kvargs["qMinInclEq"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class RangeSelectInfo:
    """

    Attributes
    ----------
    qMeasure: str
      Label of the measure.
    qRangeHi: float
      Highest value in the range.
    qRangeLo: float
      Lowest value in the range.
    """

    qMeasure: str = None
    qRangeHi: float = -1e300
    qRangeLo: float = -1e300

    def __init__(self_, **kvargs):
        if "qMeasure" in kvargs and kvargs["qMeasure"] is not None:
            self_.qMeasure = kvargs["qMeasure"]
        if "qRangeHi" in kvargs and kvargs["qRangeHi"] is not None:
            self_.qRangeHi = kvargs["qRangeHi"]
        if "qRangeLo" in kvargs and kvargs["qRangeLo"] is not None:
            self_.qRangeLo = kvargs["qRangeLo"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Rect:
    """

    Attributes
    ----------
    qHeight: int
      Number of rows or elements in the page. The indexing of the rows may vary depending on whether the cells are expanded or not (parameter qAlwaysFullyExpanded in HyperCubeDef ).
    qLeft: int
      Position from the left.
      Corresponds to the first column.
    qTop: int
      Position from the top.
      Corresponds to the first row.
    qWidth: int
      Number of columns in the page. The indexing of the columns may vary depending on whether the cells are expanded or not (parameter qAlwaysFullyExpanded in HyperCubeDef ).
    """

    qHeight: int = None
    qLeft: int = None
    qTop: int = None
    qWidth: int = None

    def __init__(self_, **kvargs):
        if "qHeight" in kvargs and kvargs["qHeight"] is not None:
            self_.qHeight = kvargs["qHeight"]
        if "qLeft" in kvargs and kvargs["qLeft"] is not None:
            self_.qLeft = kvargs["qLeft"]
        if "qTop" in kvargs and kvargs["qTop"] is not None:
            self_.qTop = kvargs["qTop"]
        if "qWidth" in kvargs and kvargs["qWidth"] is not None:
            self_.qWidth = kvargs["qWidth"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SampleResult:
    """

    Attributes
    ----------
    qFieldOrColumn: FieldOrColumn
      Name of field or column.
    qValues: list[FieldValue]
      Matched values part of the sample.
    """

    qFieldOrColumn: FieldOrColumn = None
    qValues: list[FieldValue] = None

    def __init__(self_, **kvargs):
        if "qFieldOrColumn" in kvargs and kvargs["qFieldOrColumn"] is not None:
            if (
                type(kvargs["qFieldOrColumn"]).__name__
                == SampleResult.__annotations__["qFieldOrColumn"]
            ):
                self_.qFieldOrColumn = kvargs["qFieldOrColumn"]
            else:
                self_.qFieldOrColumn = FieldOrColumn(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qFieldOrColumn"],
                )
        if "qValues" in kvargs and kvargs["qValues"] is not None:
            if all(
                f"list[{type(e).__name__}]" == SampleResult.__annotations__["qValues"]
                for e in kvargs["qValues"]
            ):
                self_.qValues = kvargs["qValues"]
            else:
                self_.qValues = [
                    FieldValue(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qValues"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ScriptSyntaxError:
    """

    Attributes
    ----------
    qColInLine: int
      Position of the erroneous text from the beginning of the line.
    qErrLen: int
      Length of the word where the error is located.
    qLineInTab: int
      Line number in the section where the error is located.
    qSecondaryFailure: bool
      The default value is false.
    qTabIx: int
      Number of the faulty section.
    qTextPos: int
      Position of the erroneous text from the beginning of the script.
    """

    qColInLine: int = None
    qErrLen: int = None
    qLineInTab: int = None
    qSecondaryFailure: bool = None
    qTabIx: int = None
    qTextPos: int = None

    def __init__(self_, **kvargs):
        if "qColInLine" in kvargs and kvargs["qColInLine"] is not None:
            self_.qColInLine = kvargs["qColInLine"]
        if "qErrLen" in kvargs and kvargs["qErrLen"] is not None:
            self_.qErrLen = kvargs["qErrLen"]
        if "qLineInTab" in kvargs and kvargs["qLineInTab"] is not None:
            self_.qLineInTab = kvargs["qLineInTab"]
        if "qSecondaryFailure" in kvargs and kvargs["qSecondaryFailure"] is not None:
            self_.qSecondaryFailure = kvargs["qSecondaryFailure"]
        if "qTabIx" in kvargs and kvargs["qTabIx"] is not None:
            self_.qTabIx = kvargs["qTabIx"]
        if "qTextPos" in kvargs and kvargs["qTextPos"] is not None:
            self_.qTextPos = kvargs["qTextPos"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ScrollPosition:
    """

    Attributes
    ----------
    qPos: Point
    qUsePosition: bool
    """

    qPos: Point = None
    qUsePosition: bool = None

    def __init__(self_, **kvargs):
        if "qPos" in kvargs and kvargs["qPos"] is not None:
            if type(kvargs["qPos"]).__name__ == ScrollPosition.__annotations__["qPos"]:
                self_.qPos = kvargs["qPos"]
            else:
                self_.qPos = Point(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qPos"],
                )
        if "qUsePosition" in kvargs and kvargs["qUsePosition"] is not None:
            self_.qUsePosition = kvargs["qUsePosition"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchAssociationResult:
    """

    Attributes
    ----------
    qFieldDictionaries: list[SearchFieldDictionary]
      Information about the fields containing search hits.
    qFieldNames: list[str]
      List of the fields that contains search associations.
    qSearchTerms: list[str]
      List of the search terms.
    qSearchTermsMatched: list[SearchMatchCombinations]
      List of search results.
      The maximum number of search results in this list is set by qPage/qCount .
    qTotalSearchResults: int
      Total number of search results.
      This number is not limited by qPage/qCount .
    """

    qFieldDictionaries: list[SearchFieldDictionary] = None
    qFieldNames: list[str] = None
    qSearchTerms: list[str] = None
    qSearchTermsMatched: list[SearchMatchCombinations] = None
    qTotalSearchResults: int = None

    def __init__(self_, **kvargs):
        if "qFieldDictionaries" in kvargs and kvargs["qFieldDictionaries"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == SearchAssociationResult.__annotations__["qFieldDictionaries"]
                for e in kvargs["qFieldDictionaries"]
            ):
                self_.qFieldDictionaries = kvargs["qFieldDictionaries"]
            else:
                self_.qFieldDictionaries = [
                    SearchFieldDictionary(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qFieldDictionaries"]
                ]
        if "qFieldNames" in kvargs and kvargs["qFieldNames"] is not None:
            self_.qFieldNames = kvargs["qFieldNames"]
        if "qSearchTerms" in kvargs and kvargs["qSearchTerms"] is not None:
            self_.qSearchTerms = kvargs["qSearchTerms"]
        if (
            "qSearchTermsMatched" in kvargs
            and kvargs["qSearchTermsMatched"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == SearchAssociationResult.__annotations__["qSearchTermsMatched"]
                for e in kvargs["qSearchTermsMatched"]
            ):
                self_.qSearchTermsMatched = kvargs["qSearchTermsMatched"]
            else:
                self_.qSearchTermsMatched = [
                    SearchMatchCombinations(e) for e in kvargs["qSearchTermsMatched"]
                ]
        if (
            "qTotalSearchResults" in kvargs
            and kvargs["qTotalSearchResults"] is not None
        ):
            self_.qTotalSearchResults = kvargs["qTotalSearchResults"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchAttribute:
    """

    Attributes
    ----------
    qKey: str
      String corresponding to SearchObjectOptions.qAttributes. It will be qProperty for SearchObjectOptions.
    qValue: str
      String corresponding to qKey for the current SearchGroupItemMatch. For example, if the match is Make by Price found in the title of a generic object, qValue will be qMetaDef/title.
    """

    qKey: str = None
    qValue: str = None

    def __init__(self_, **kvargs):
        if "qKey" in kvargs and kvargs["qKey"] is not None:
            self_.qKey = kvargs["qKey"]
        if "qValue" in kvargs and kvargs["qValue"] is not None:
            self_.qValue = kvargs["qValue"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchCharRange:
    """

    Attributes
    ----------
    qCharCount: int
      Length of the match in the search result.
    qCharPos: int
      Starting position of the match in the search result, starting from 0.
    qTerm: int
      Position of the term in the list of search terms, starting from 0.
    """

    qCharCount: int = None
    qCharPos: int = None
    qTerm: int = None

    def __init__(self_, **kvargs):
        if "qCharCount" in kvargs and kvargs["qCharCount"] is not None:
            self_.qCharCount = kvargs["qCharCount"]
        if "qCharPos" in kvargs and kvargs["qCharPos"] is not None:
            self_.qCharPos = kvargs["qCharPos"]
        if "qTerm" in kvargs and kvargs["qTerm"] is not None:
            self_.qTerm = kvargs["qTerm"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchCombinationOptions:
    """

    Attributes
    ----------
    qAttributes: list[str]
      Optional.

      • For SearchSuggest method, this array is empty.

      • For SearchObjects method, this array is empty or contain qProperty .

      • For SearchResults method, this array is empty, or contains qNum and/or qElemNum . It allows the user to request details in the outputted SearchGroupItemMatch . For more information, see SearchGroupItemMatch.
    qCharEncoding: Literal["CHAR_ENCODING_UTF8", "CHAR_ENCODING_UTF16"]
      Encoding used to compute qRanges of type SearchCharRange.
      Only affects the computation of the ranges. It does not impact the encoding of the text.

      One of:

      • Utf8 or CHAR_ENCODING_UTF8

      • Utf16 or CHAR_ENCODING_UTF16
    qContext: Literal["CONTEXT_CLEARED", "CONTEXT_LOCKED_FIELDS_ONLY", "CONTEXT_CURRENT_SELECTIONS"]
      Search context.
      The default value is LockedFieldsOnly .

      One of:

      • Cleared or CONTEXT_CLEARED

      • LockedFieldsOnly or CONTEXT_LOCKED_FIELDS_ONLY

      • CurrentSelections or CONTEXT_CURRENT_SELECTIONS
    qSearchFields: list[str]
      List of the search fields.
      If empty, the search is performed in all fields of the app.
    """

    qAttributes: list[str] = None
    qCharEncoding: Literal[
        "CHAR_ENCODING_UTF8", "CHAR_ENCODING_UTF16"
    ] = "CHAR_ENCODING_UTF8"
    qContext: Literal[
        "CONTEXT_CLEARED", "CONTEXT_LOCKED_FIELDS_ONLY", "CONTEXT_CURRENT_SELECTIONS"
    ] = "CONTEXT_LOCKED_FIELDS_ONLY"
    qSearchFields: list[str] = None

    def __init__(self_, **kvargs):
        if "qAttributes" in kvargs and kvargs["qAttributes"] is not None:
            self_.qAttributes = kvargs["qAttributes"]
        if "qCharEncoding" in kvargs and kvargs["qCharEncoding"] is not None:
            self_.qCharEncoding = kvargs["qCharEncoding"]
        if "qContext" in kvargs and kvargs["qContext"] is not None:
            self_.qContext = kvargs["qContext"]
        if "qSearchFields" in kvargs and kvargs["qSearchFields"] is not None:
            self_.qSearchFields = kvargs["qSearchFields"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchContextType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchFieldDictionary:
    """

    Attributes
    ----------
    qField: int
      Position of the field in the list of fields, starting from 0.
      The list of fields is defined in qResults/qFieldNames and contains the search associations.
    qResult: list[SearchTermResult]
      List of the matching values.
      The maximum number of values in this list is set by qMaxNbrFieldMatches .
    """

    qField: int = None
    qResult: list[SearchTermResult] = None

    def __init__(self_, **kvargs):
        if "qField" in kvargs and kvargs["qField"] is not None:
            self_.qField = kvargs["qField"]
        if "qResult" in kvargs and kvargs["qResult"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == SearchFieldDictionary.__annotations__["qResult"]
                for e in kvargs["qResult"]
            ):
                self_.qResult = kvargs["qResult"]
            else:
                self_.qResult = [
                    SearchTermResult(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qResult"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchFieldMatch:
    """

    Attributes
    ----------
    qField: int
      Position of the field in the list of fields, starting from 0.
      The list of fields is defined in qResults/qFieldNames and contains the search associations.
    qNoOfMatches: int
      Number of search hits in the field.
      The number of values in qValues and the value of qNoOfMatches are equal if qMaxNbrFieldMatches is -1.
    qTerms: list[int]
      Positions of the search terms, starting from 0.
    qValues: list[int]
      Positions of the matching values in the search results.
      The maximum number of values in this list is defined by qMaxNbrFieldMatches .
    """

    qField: int = None
    qNoOfMatches: int = None
    qTerms: list[int] = None
    qValues: list[int] = None

    def __init__(self_, **kvargs):
        if "qField" in kvargs and kvargs["qField"] is not None:
            self_.qField = kvargs["qField"]
        if "qNoOfMatches" in kvargs and kvargs["qNoOfMatches"] is not None:
            self_.qNoOfMatches = kvargs["qNoOfMatches"]
        if "qTerms" in kvargs and kvargs["qTerms"] is not None:
            self_.qTerms = kvargs["qTerms"]
        if "qValues" in kvargs and kvargs["qValues"] is not None:
            self_.qValues = kvargs["qValues"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchFieldMatchType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchFieldMatchesItem:
    """

    Attributes
    ----------
    qElemNo: int
    qSearchTermsMatched: list[int]
    qText: str
    """

    qElemNo: int = None
    qSearchTermsMatched: list[int] = None
    qText: str = None

    def __init__(self_, **kvargs):
        if "qElemNo" in kvargs and kvargs["qElemNo"] is not None:
            self_.qElemNo = kvargs["qElemNo"]
        if (
            "qSearchTermsMatched" in kvargs
            and kvargs["qSearchTermsMatched"] is not None
        ):
            self_.qSearchTermsMatched = kvargs["qSearchTermsMatched"]
        if "qText" in kvargs and kvargs["qText"] is not None:
            self_.qText = kvargs["qText"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchFieldSelectionMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchFieldValueItem:
    """

    Attributes
    ----------
    qFieldName: str
      Field name of matches.
    qValues: list[SearchFieldMatchesItem]
      List of search matches.
    """

    qFieldName: str = None
    qValues: list[SearchFieldMatchesItem] = None

    def __init__(self_, **kvargs):
        if "qFieldName" in kvargs and kvargs["qFieldName"] is not None:
            self_.qFieldName = kvargs["qFieldName"]
        if "qValues" in kvargs and kvargs["qValues"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == SearchFieldValueItem.__annotations__["qValues"]
                for e in kvargs["qValues"]
            ):
                self_.qValues = kvargs["qValues"]
            else:
                self_.qValues = [
                    SearchFieldMatchesItem(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qValues"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchGroup:
    """

    Attributes
    ----------
    qGroupType: Literal["DATASET_GROUP", "GENERIC_OBJECTS_GROUP"]
      Type of the search group.

      One of:

      • DatasetType or DATASET_GROUP

      • GenericObjectsType or GENERIC_OBJECTS_GROUP
    qId: int
      Identifier of the search group.
    qItems: list[SearchGroupItem]
      List of items in the search group.
      The group items are numbered from the value of SearchGroupOptions.qOffset to the value of SearchGroupOptions.qOffset \+ SearchGroupOptions.qCount
    qSearchTermsMatched: list[int]
      Indexes of the search terms that are included in the group. These search terms are related to the list of terms defined in SearchResult.qSearchTerms .
    qTotalNumberOfItems: int
      Total number of distinct items in the search group.
    """

    qGroupType: Literal["DATASET_GROUP", "GENERIC_OBJECTS_GROUP"] = None
    qId: int = None
    qItems: list[SearchGroupItem] = None
    qSearchTermsMatched: list[int] = None
    qTotalNumberOfItems: int = None

    def __init__(self_, **kvargs):
        if "qGroupType" in kvargs and kvargs["qGroupType"] is not None:
            self_.qGroupType = kvargs["qGroupType"]
        if "qId" in kvargs and kvargs["qId"] is not None:
            self_.qId = kvargs["qId"]
        if "qItems" in kvargs and kvargs["qItems"] is not None:
            if all(
                f"list[{type(e).__name__}]" == SearchGroup.__annotations__["qItems"]
                for e in kvargs["qItems"]
            ):
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [
                    SearchGroupItem(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qItems"]
                ]
        if (
            "qSearchTermsMatched" in kvargs
            and kvargs["qSearchTermsMatched"] is not None
        ):
            self_.qSearchTermsMatched = kvargs["qSearchTermsMatched"]
        if (
            "qTotalNumberOfItems" in kvargs
            and kvargs["qTotalNumberOfItems"] is not None
        ):
            self_.qTotalNumberOfItems = kvargs["qTotalNumberOfItems"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchGroupItem:
    """

    Attributes
    ----------
    qIdentifier: str
      Identifier of the item.
      It corresponds to:

      • The name of the field, if the type of the search group is data set.

      • The id of the generic object if the type of the search group is generic object.
    qItemMatches: list[SearchGroupItemMatch]
      List of matches in the search group item.
      The group item matches are numbered from the value of SearchGroupItemOptions.qOffset to the value of SearchGroupItemOptions.qOffset \+ SearchGroupItemOptions.qCount .
    qItemType: Literal["FIELD", "GENERIC_OBJECT"]
      Type of the group item.

      One of:

      • Field or FIELD

      • GenericObject or GENERIC_OBJECT
    qMatchType: Literal["FM_NONE", "FM_SUBSTRING", "FM_WORD", "FM_EXACT", "FM_LAST"]
      Match type applied in this result group.

      One of:

      • FieldMatchNone or FM_NONE

      • FieldMatchSubString or FM_SUBSTRING

      • FieldMatchWord or FM_WORD

      • FieldMatchExact or FM_EXACT

      • FieldMatchLast or FM_LAST
    qSearchTermsMatched: list[int]
      Indexes of the search terms that are included in the group item. These search terms are related to the list of terms defined in SearchResult.qSearchTerms .
    qTotalNumberOfMatches: int
      Total number of distinct matches in the search group item.
    """

    qIdentifier: str = None
    qItemMatches: list[SearchGroupItemMatch] = None
    qItemType: Literal["FIELD", "GENERIC_OBJECT"] = None
    qMatchType: Literal[
        "FM_NONE", "FM_SUBSTRING", "FM_WORD", "FM_EXACT", "FM_LAST"
    ] = None
    qSearchTermsMatched: list[int] = None
    qTotalNumberOfMatches: int = None

    def __init__(self_, **kvargs):
        if "qIdentifier" in kvargs and kvargs["qIdentifier"] is not None:
            self_.qIdentifier = kvargs["qIdentifier"]
        if "qItemMatches" in kvargs and kvargs["qItemMatches"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == SearchGroupItem.__annotations__["qItemMatches"]
                for e in kvargs["qItemMatches"]
            ):
                self_.qItemMatches = kvargs["qItemMatches"]
            else:
                self_.qItemMatches = [
                    SearchGroupItemMatch(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qItemMatches"]
                ]
        if "qItemType" in kvargs and kvargs["qItemType"] is not None:
            self_.qItemType = kvargs["qItemType"]
        if "qMatchType" in kvargs and kvargs["qMatchType"] is not None:
            self_.qMatchType = kvargs["qMatchType"]
        if (
            "qSearchTermsMatched" in kvargs
            and kvargs["qSearchTermsMatched"] is not None
        ):
            self_.qSearchTermsMatched = kvargs["qSearchTermsMatched"]
        if (
            "qTotalNumberOfMatches" in kvargs
            and kvargs["qTotalNumberOfMatches"] is not None
        ):
            self_.qTotalNumberOfMatches = kvargs["qTotalNumberOfMatches"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchGroupItemMatch:
    """

    Attributes
    ----------
    qAttributes: list[SearchAttribute]
      Provides detail of the match as requested by the user in SearchObjectsOptions.qAttributes or SearchCombinationOptions.qAttributes
      If the user requests SearchObjects or SearchResults with an empty qAttributes option, the outputted qAttributes is returned empty.
      For SearchObjects requested with qProperty , the SearchGroupItemMatch.qAttributes return value contains [“qProperty”, "qMetaDef/title”] if the match has been found in the title of the item. For dimension values, the returned qProperty will be “*” .
      For SearchResults requested with qNum , the SearchGroupItemMatch.qAttributes return value contains ["qNum", N] where N is the numeric value of the element or NaN if the value is not numeric.
      For SearchResults requested with qElemNum , the SearchGroupItemMatch.qAttributes return value contains ["qElemNum", N] where N is the value index of the element.
    qFieldSelectionMode: Literal["ONE_AND_ONLY_ONE"]
      Selection mode of a field.
      Suppressed by default. One and always one field value is selected when set to OneAndOnlyOne.
    qRanges: list[SearchCharRange]
      List of ranges.
      For example, if the search terms are Price and Make, and the search group item value is Make by Price vs Mileage, then there are two ranges: one for Price and one for Make.
    qText: str
      Search match value.
      Value of the search group item.
      If the match is found in a field, it corresponds to the value of the field.
      If the match is found in a generic object property, it corresponds to the property value.
    """

    qAttributes: list[SearchAttribute] = None
    qFieldSelectionMode: Literal["ONE_AND_ONLY_ONE"] = None
    qRanges: list[SearchCharRange] = None
    qText: str = None

    def __init__(self_, **kvargs):
        if "qAttributes" in kvargs and kvargs["qAttributes"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == SearchGroupItemMatch.__annotations__["qAttributes"]
                for e in kvargs["qAttributes"]
            ):
                self_.qAttributes = kvargs["qAttributes"]
            else:
                self_.qAttributes = [
                    SearchAttribute(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qAttributes"]
                ]
        if (
            "qFieldSelectionMode" in kvargs
            and kvargs["qFieldSelectionMode"] is not None
        ):
            self_.qFieldSelectionMode = kvargs["qFieldSelectionMode"]
        if "qRanges" in kvargs and kvargs["qRanges"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == SearchGroupItemMatch.__annotations__["qRanges"]
                for e in kvargs["qRanges"]
            ):
                self_.qRanges = kvargs["qRanges"]
            else:
                self_.qRanges = [
                    SearchCharRange(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qRanges"]
                ]
        if "qText" in kvargs and kvargs["qText"] is not None:
            self_.qText = kvargs["qText"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchGroupItemOptions:
    """

    Attributes
    ----------
    qCount: int
      Maximum number of matches per item (in qItemMatches[ ] ).
      The default value is -1: all values are returned.
    qGroupItemType: Literal["FIELD", "GENERIC_OBJECT"]
      Type of the group item. Can be:

      • GenericObject: the type of the search group item is a generic object. Group items have this type when you are calling SearchObjects .

      • Field: the type of the search group item is a field. Group items have this type when you are calling SearchResults .

      One of:

      • Field or FIELD

      • GenericObject or GENERIC_OBJECT
    qOffset: int
      Position starting from 0.
      The default value is 0.
    """

    qCount: int = -1
    qGroupItemType: Literal["FIELD", "GENERIC_OBJECT"] = None
    qOffset: int = None

    def __init__(self_, **kvargs):
        if "qCount" in kvargs and kvargs["qCount"] is not None:
            self_.qCount = kvargs["qCount"]
        if "qGroupItemType" in kvargs and kvargs["qGroupItemType"] is not None:
            self_.qGroupItemType = kvargs["qGroupItemType"]
        if "qOffset" in kvargs and kvargs["qOffset"] is not None:
            self_.qOffset = kvargs["qOffset"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchGroupItemType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchGroupOptions:
    """

    Attributes
    ----------
    qCount: int
      Maximum number of items per group (in qItems[ ] ).
      The default value is -1; all values are returned.
    qGroupType: Literal["DATASET_GROUP", "GENERIC_OBJECTS_GROUP"]
      Type of the group. Can be:

      • GenericObjectType: the type of the search group item is a generic object. Groups have this type when you are calling SearchObjects .

      • DatasetType: type of the search group item is a dataset association. Groups have this type when you are calling SearchResults .

      One of:

      • DatasetType or DATASET_GROUP

      • GenericObjectsType or GENERIC_OBJECTS_GROUP
    qOffset: int
      Position starting from 0.
      The default value is 0.
    """

    qCount: int = -1
    qGroupType: Literal["DATASET_GROUP", "GENERIC_OBJECTS_GROUP"] = None
    qOffset: int = None

    def __init__(self_, **kvargs):
        if "qCount" in kvargs and kvargs["qCount"] is not None:
            self_.qCount = kvargs["qCount"]
        if "qGroupType" in kvargs and kvargs["qGroupType"] is not None:
            self_.qGroupType = kvargs["qGroupType"]
        if "qOffset" in kvargs and kvargs["qOffset"] is not None:
            self_.qOffset = kvargs["qOffset"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchGroupType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchMatchCombination:
    """

    Attributes
    ----------
    qFieldMatches: list[SearchFieldMatch]
      Information about the search matches.
    qId: int
      Index of the search result, starting from 0.
    """

    qFieldMatches: list[SearchFieldMatch] = None
    qId: int = None

    def __init__(self_, **kvargs):
        if "qFieldMatches" in kvargs and kvargs["qFieldMatches"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == SearchMatchCombination.__annotations__["qFieldMatches"]
                for e in kvargs["qFieldMatches"]
            ):
                self_.qFieldMatches = kvargs["qFieldMatches"]
            else:
                self_.qFieldMatches = [
                    SearchFieldMatch(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qFieldMatches"]
                ]
        if "qId" in kvargs and kvargs["qId"] is not None:
            self_.qId = kvargs["qId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchMatchCombinations(List["SearchMatchCombination"]):
    """

    Attributes
    ----------
    """

    def __init__(self_, elements):
        for e in elements:
            self_.append(SearchMatchCombination(**e))


@dataclass
class SearchObjectOptions:
    """

    Attributes
    ----------
    qAttributes: list[str]
      This array is either empty or contains qProperty .
    qCharEncoding: Literal["CHAR_ENCODING_UTF8", "CHAR_ENCODING_UTF16"]
      Encoding used to compute qRanges of type SearchCharRange.
      Only affects the computation of the ranges. It does not impact the encoding of the text.

      One of:

      • Utf8 or CHAR_ENCODING_UTF8

      • Utf16 or CHAR_ENCODING_UTF16
    """

    qAttributes: list[str] = None
    qCharEncoding: Literal[
        "CHAR_ENCODING_UTF8", "CHAR_ENCODING_UTF16"
    ] = "CHAR_ENCODING_UTF8"

    def __init__(self_, **kvargs):
        if "qAttributes" in kvargs and kvargs["qAttributes"] is not None:
            self_.qAttributes = kvargs["qAttributes"]
        if "qCharEncoding" in kvargs and kvargs["qCharEncoding"] is not None:
            self_.qCharEncoding = kvargs["qCharEncoding"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchPage:
    """

    Attributes
    ----------
    qCount: int
      Number of search groups to return (in qSearchGroupArray ).
    qGroupItemOptions: list[SearchGroupItemOptions]
      Options of the search group items.
      If this property is not set, all values are returned.
      This property is to be used with the SearchResults method or the SearchObjects method.
    qGroupOptions: list[SearchGroupOptions]
      Options of the search groups.
      If this property is not set, all values are returned.
      This property is to be used with the SearchResults method or the SearchObjects method.
    qMaxNbrFieldMatches: int
      Maximum number of matching values to return per search result.
      The default value is -1; all values are returned.
      This property is to be used with the SearchAssociations method.
    qOffset: int
      Position from the top, starting from 0.
      If the offset is set to 0, the first search result to be returned is at position 0.
    """

    qCount: int = None
    qGroupItemOptions: list[SearchGroupItemOptions] = None
    qGroupOptions: list[SearchGroupOptions] = None
    qMaxNbrFieldMatches: int = -1
    qOffset: int = None

    def __init__(self_, **kvargs):
        if "qCount" in kvargs and kvargs["qCount"] is not None:
            self_.qCount = kvargs["qCount"]
        if "qGroupItemOptions" in kvargs and kvargs["qGroupItemOptions"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == SearchPage.__annotations__["qGroupItemOptions"]
                for e in kvargs["qGroupItemOptions"]
            ):
                self_.qGroupItemOptions = kvargs["qGroupItemOptions"]
            else:
                self_.qGroupItemOptions = [
                    SearchGroupItemOptions(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qGroupItemOptions"]
                ]
        if "qGroupOptions" in kvargs and kvargs["qGroupOptions"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == SearchPage.__annotations__["qGroupOptions"]
                for e in kvargs["qGroupOptions"]
            ):
                self_.qGroupOptions = kvargs["qGroupOptions"]
            else:
                self_.qGroupOptions = [
                    SearchGroupOptions(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qGroupOptions"]
                ]
        if (
            "qMaxNbrFieldMatches" in kvargs
            and kvargs["qMaxNbrFieldMatches"] is not None
        ):
            self_.qMaxNbrFieldMatches = kvargs["qMaxNbrFieldMatches"]
        if "qOffset" in kvargs and kvargs["qOffset"] is not None:
            self_.qOffset = kvargs["qOffset"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchResult:
    """

    Attributes
    ----------
    qSearchGroupArray: list[SearchGroup]
      List of search groups.
      The groups are numbered from the value of SearchPage.qOffset to the value of SearchPage.qOffset + SearchPage.qCount .
    qSearchTerms: list[str]
      List of the search terms.
    qTotalNumberOfGroups: int
      Total number of groups.
    """

    qSearchGroupArray: list[SearchGroup] = None
    qSearchTerms: list[str] = None
    qTotalNumberOfGroups: int = None

    def __init__(self_, **kvargs):
        if "qSearchGroupArray" in kvargs and kvargs["qSearchGroupArray"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == SearchResult.__annotations__["qSearchGroupArray"]
                for e in kvargs["qSearchGroupArray"]
            ):
                self_.qSearchGroupArray = kvargs["qSearchGroupArray"]
            else:
                self_.qSearchGroupArray = [
                    SearchGroup(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qSearchGroupArray"]
                ]
        if "qSearchTerms" in kvargs and kvargs["qSearchTerms"] is not None:
            self_.qSearchTerms = kvargs["qSearchTerms"]
        if (
            "qTotalNumberOfGroups" in kvargs
            and kvargs["qTotalNumberOfGroups"] is not None
        ):
            self_.qTotalNumberOfGroups = kvargs["qTotalNumberOfGroups"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchSuggestItem:
    """

    Attributes
    ----------
    qTerm: int
      Index of the suggestion value.
      The indexing starts from 0 and from the left.
    qValue: str
      Value of the suggestion.
    """

    qTerm: int = None
    qValue: str = None

    def __init__(self_, **kvargs):
        if "qTerm" in kvargs and kvargs["qTerm"] is not None:
            self_.qTerm = kvargs["qTerm"]
        if "qValue" in kvargs and kvargs["qValue"] is not None:
            self_.qValue = kvargs["qValue"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchSuggestionResult:
    """

    Attributes
    ----------
    qFieldNames: list[str]
      List of field names that contain search hits.
    qSuggestions: list[SearchSuggestItem]
      List of suggestions.
    """

    qFieldNames: list[str] = None
    qSuggestions: list[SearchSuggestItem] = None

    def __init__(self_, **kvargs):
        if "qFieldNames" in kvargs and kvargs["qFieldNames"] is not None:
            self_.qFieldNames = kvargs["qFieldNames"]
        if "qSuggestions" in kvargs and kvargs["qSuggestions"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == SearchSuggestionResult.__annotations__["qSuggestions"]
                for e in kvargs["qSuggestions"]
            ):
                self_.qSuggestions = kvargs["qSuggestions"]
            else:
                self_.qSuggestions = [
                    SearchSuggestItem(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qSuggestions"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchTermResult:
    """

    Attributes
    ----------
    qElemNumber: int
      Element number of the associated value.
    qRanges: list[SearchCharRange]
      List of ranges.
      For example, if the user searches the term read and the associative value is Reading , then the corresponding range would be Read in Reading .
    qText: str
      Text of the associated value.
    """

    qElemNumber: int = None
    qRanges: list[SearchCharRange] = None
    qText: str = None

    def __init__(self_, **kvargs):
        if "qElemNumber" in kvargs and kvargs["qElemNumber"] is not None:
            self_.qElemNumber = kvargs["qElemNumber"]
        if "qRanges" in kvargs and kvargs["qRanges"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == SearchTermResult.__annotations__["qRanges"]
                for e in kvargs["qRanges"]
            ):
                self_.qRanges = kvargs["qRanges"]
            else:
                self_.qRanges = [
                    SearchCharRange(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qRanges"]
                ]
        if "qText" in kvargs and kvargs["qText"] is not None:
            self_.qText = kvargs["qText"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchValueOptions:
    """

    Attributes
    ----------
    qSearchFields: list[str]
      List of the search fields.
      If empty, the search is performed in all fields of the app.
    """

    qSearchFields: list[str] = None

    def __init__(self_, **kvargs):
        if "qSearchFields" in kvargs and kvargs["qSearchFields"] is not None:
            self_.qSearchFields = kvargs["qSearchFields"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchValuePage:
    """

    Attributes
    ----------
    qCount: int
      Number of search fields to return
    qMaxNbrFieldMatches: int
      Maximum number of matching values to return per search result.
    qOffset: int
      Position from the top, starting from 0.
      If the offset is set to 0, the first search result to be returned is at position 0.
    """

    qCount: int = None
    qMaxNbrFieldMatches: int = -1
    qOffset: int = None

    def __init__(self_, **kvargs):
        if "qCount" in kvargs and kvargs["qCount"] is not None:
            self_.qCount = kvargs["qCount"]
        if (
            "qMaxNbrFieldMatches" in kvargs
            and kvargs["qMaxNbrFieldMatches"] is not None
        ):
            self_.qMaxNbrFieldMatches = kvargs["qMaxNbrFieldMatches"]
        if "qOffset" in kvargs and kvargs["qOffset"] is not None:
            self_.qOffset = kvargs["qOffset"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SearchValueResult:
    """

    Attributes
    ----------
    qFieldMatches: list[SearchFieldValueItem]
      List of search groups.
      The groups are numbered from the value of SearchPage.qOffset to the value of SearchPage.qOffset + SearchPage.qCount .
    qSearchTerms: list[str]
      List of the search terms.
    """

    qFieldMatches: list[SearchFieldValueItem] = None
    qSearchTerms: list[str] = None

    def __init__(self_, **kvargs):
        if "qFieldMatches" in kvargs and kvargs["qFieldMatches"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == SearchValueResult.__annotations__["qFieldMatches"]
                for e in kvargs["qFieldMatches"]
            ):
                self_.qFieldMatches = kvargs["qFieldMatches"]
            else:
                self_.qFieldMatches = [
                    SearchFieldValueItem(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qFieldMatches"]
                ]
        if "qSearchTerms" in kvargs and kvargs["qSearchTerms"] is not None:
            self_.qSearchTerms = kvargs["qSearchTerms"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SelectInfo:
    """

    Attributes
    ----------
    qContinuousRangeInfo: list[Range]
      List of information about ranges for selections.
    qNumberFormat: FieldAttributes
      Gives information about the formatting of the range.
      This parameter is used when performing range selections or text searches in dimensions.
    qRangeHi: float
      Highest value of the search range.
      This parameter is used when performing range selections or text searches in dimensions.
      Default is Null.
    qRangeInfo: list[RangeSelectInfo]
      This parameter is used when performing range selections or text searches in measures.
      Gives information about the range of selections.
    qRangeLo: float
      Lower value of the search range.
      This parameter is used when performing range selections or text searches in dimensions.
      Default is Null.
    qSelectFieldSearch: bool
      This parameter is true if the TextSearch is a result of a Select Field operation.
    qSoftLock: bool
      Set to true to ignore locks; in that case, locked fields can be selected.
      The default value is false.
    qTextSearch: str
      Text search string.
      Everything that matches the text is selected.
      This parameter is optional.
    """

    qContinuousRangeInfo: list[Range] = None
    qNumberFormat: FieldAttributes = None
    qRangeHi: float = -1e300
    qRangeInfo: list[RangeSelectInfo] = None
    qRangeLo: float = -1e300
    qSelectFieldSearch: bool = None
    qSoftLock: bool = None
    qTextSearch: str = None

    def __init__(self_, **kvargs):
        if (
            "qContinuousRangeInfo" in kvargs
            and kvargs["qContinuousRangeInfo"] is not None
        ):
            if all(
                f"list[{type(e).__name__}]"
                == SelectInfo.__annotations__["qContinuousRangeInfo"]
                for e in kvargs["qContinuousRangeInfo"]
            ):
                self_.qContinuousRangeInfo = kvargs["qContinuousRangeInfo"]
            else:
                self_.qContinuousRangeInfo = [
                    Range(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qContinuousRangeInfo"]
                ]
        if "qNumberFormat" in kvargs and kvargs["qNumberFormat"] is not None:
            if (
                type(kvargs["qNumberFormat"]).__name__
                == SelectInfo.__annotations__["qNumberFormat"]
            ):
                self_.qNumberFormat = kvargs["qNumberFormat"]
            else:
                self_.qNumberFormat = FieldAttributes(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qNumberFormat"],
                )
        if "qRangeHi" in kvargs and kvargs["qRangeHi"] is not None:
            self_.qRangeHi = kvargs["qRangeHi"]
        if "qRangeInfo" in kvargs and kvargs["qRangeInfo"] is not None:
            if all(
                f"list[{type(e).__name__}]" == SelectInfo.__annotations__["qRangeInfo"]
                for e in kvargs["qRangeInfo"]
            ):
                self_.qRangeInfo = kvargs["qRangeInfo"]
            else:
                self_.qRangeInfo = [
                    RangeSelectInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qRangeInfo"]
                ]
        if "qRangeLo" in kvargs and kvargs["qRangeLo"] is not None:
            self_.qRangeLo = kvargs["qRangeLo"]
        if "qSelectFieldSearch" in kvargs and kvargs["qSelectFieldSearch"] is not None:
            self_.qSelectFieldSearch = kvargs["qSelectFieldSearch"]
        if "qSoftLock" in kvargs and kvargs["qSoftLock"] is not None:
            self_.qSoftLock = kvargs["qSoftLock"]
        if "qTextSearch" in kvargs and kvargs["qTextSearch"] is not None:
            self_.qTextSearch = kvargs["qTextSearch"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SelectionObject:
    """
    Indicates which selections are currently applied. It gives the current selections. Is the layout for SelectionObjectDef.

    Attributes
    ----------
    qBackCount: int
      Number of steps back.
    qForwardCount: int
      Number of steps forward.
    qSelections: list[NxCurrentSelectionItem]
      Lists the fields that are selected.
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    """

    qBackCount: int = None
    qForwardCount: int = None
    qSelections: list[NxCurrentSelectionItem] = None
    qStateName: str = None

    def __init__(self_, **kvargs):
        if "qBackCount" in kvargs and kvargs["qBackCount"] is not None:
            self_.qBackCount = kvargs["qBackCount"]
        if "qForwardCount" in kvargs and kvargs["qForwardCount"] is not None:
            self_.qForwardCount = kvargs["qForwardCount"]
        if "qSelections" in kvargs and kvargs["qSelections"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == SelectionObject.__annotations__["qSelections"]
                for e in kvargs["qSelections"]
            ):
                self_.qSelections = kvargs["qSelections"]
            else:
                self_.qSelections = [
                    NxCurrentSelectionItem(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qSelections"]
                ]
        if "qStateName" in kvargs and kvargs["qStateName"] is not None:
            self_.qStateName = kvargs["qStateName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SelectionObjectDef:
    """
    To display the current selections.
    Can be added to any generic object but is particularly meaningful when using session objects to monitor an app.

     Properties:
    "qSelectionObjectDef": {}

    Attributes
    ----------
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    """

    qStateName: str = None

    def __init__(self_, **kvargs):
        if "qStateName" in kvargs and kvargs["qStateName"] is not None:
            self_.qStateName = kvargs["qStateName"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Size:
    """

    Attributes
    ----------
    qcx: int
      Number of pixels on the x axis.
    qcy: int
      Number of pixels on the y axis.
    """

    qcx: int = None
    qcy: int = None

    def __init__(self_, **kvargs):
        if "qcx" in kvargs and kvargs["qcx"] is not None:
            self_.qcx = kvargs["qcx"]
        if "qcy" in kvargs and kvargs["qcy"] is not None:
            self_.qcy = kvargs["qcy"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SortCriteria:
    """

    Attributes
    ----------
    qExpression: ValueExpr
      Sort by expression.
    qSortByAscii: int
      Sorts the field by alphabetical order.
    qSortByExpression: int
      Sorts the field by expression.
    qSortByFrequency: int
      Sorts the field values by frequency (number of occurrences in the field).
    qSortByGreyness: int
    qSortByLoadOrder: int
      Sorts the field values by the initial load order.
    qSortByNumeric: int
      Sorts the field values by numeric value.
    qSortByState: int
      Sorts the field values according to their logical state (selected, optional, alternative or excluded).
    """

    qExpression: ValueExpr = None
    qSortByAscii: int = None
    qSortByExpression: int = None
    qSortByFrequency: int = None
    qSortByGreyness: int = None
    qSortByLoadOrder: int = None
    qSortByNumeric: int = None
    qSortByState: int = None

    def __init__(self_, **kvargs):
        if "qExpression" in kvargs and kvargs["qExpression"] is not None:
            if (
                type(kvargs["qExpression"]).__name__
                == SortCriteria.__annotations__["qExpression"]
            ):
                self_.qExpression = kvargs["qExpression"]
            else:
                self_.qExpression = ValueExpr(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qExpression"],
                )
        if "qSortByAscii" in kvargs and kvargs["qSortByAscii"] is not None:
            self_.qSortByAscii = kvargs["qSortByAscii"]
        if "qSortByExpression" in kvargs and kvargs["qSortByExpression"] is not None:
            self_.qSortByExpression = kvargs["qSortByExpression"]
        if "qSortByFrequency" in kvargs and kvargs["qSortByFrequency"] is not None:
            self_.qSortByFrequency = kvargs["qSortByFrequency"]
        if "qSortByGreyness" in kvargs and kvargs["qSortByGreyness"] is not None:
            self_.qSortByGreyness = kvargs["qSortByGreyness"]
        if "qSortByLoadOrder" in kvargs and kvargs["qSortByLoadOrder"] is not None:
            self_.qSortByLoadOrder = kvargs["qSortByLoadOrder"]
        if "qSortByNumeric" in kvargs and kvargs["qSortByNumeric"] is not None:
            self_.qSortByNumeric = kvargs["qSortByNumeric"]
        if "qSortByState" in kvargs and kvargs["qSortByState"] is not None:
            self_.qSortByState = kvargs["qSortByState"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SourceKeyRecord:
    """

    Attributes
    ----------
    qKeyFields: list[str]
      Name of the key field.
    qTables: list[str]
      Table the key belongs to.
    """

    qKeyFields: list[str] = None
    qTables: list[str] = None

    def __init__(self_, **kvargs):
        if "qKeyFields" in kvargs and kvargs["qKeyFields"] is not None:
            self_.qKeyFields = kvargs["qKeyFields"]
        if "qTables" in kvargs and kvargs["qTables"] is not None:
            self_.qTables = kvargs["qTables"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class StateEnumType:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class StaticContentList:
    """

    Attributes
    ----------
    qItems: list[StaticContentListItem]
      Information about the list of content files.
    """

    qItems: list[StaticContentListItem] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs and kvargs["qItems"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == StaticContentList.__annotations__["qItems"]
                for e in kvargs["qItems"]
            ):
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [
                    StaticContentListItem(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qItems"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class StaticContentListItem:
    """
    In addition, this structure can return dynamic properties.

    Attributes
    ----------
    qUrl: str
      Relative path to the content file. The URL is static.
      In Qlik Sense Enterprise, content files located:

      • In the /content/ <content library name>/ folder are part of a global content library.

      • In the /appcontent/ folder are part of the app specific library.
      The content files are never embedded in the qvf file.
      In Qlik Sense Desktop, content files located:

      • In the /content/default/ folder are outside the qvf file.

      • In the /media/ folder are embedded in the qvf file.
    qUrlDef: str
      Relative path to the content file. The URL is static.
      In Qlik Sense Enterprise, content files located:

      • In the /content/ <content library name>/ folder are part of a global content library.

      • In the /appcontent/ folder are part of the app specific library.
      The content files are never embedded in the qvf file.
      In Qlik Sense Desktop, content files located:

      • In the /content/default/ folder are outside the qvf file.

      • In the /media/ folder are embedded in the qvf file.
    """

    qUrl: str = None
    qUrlDef: str = None

    def __init__(self_, **kvargs):
        if "qUrl" in kvargs and kvargs["qUrl"] is not None:
            self_.qUrl = kvargs["qUrl"]
        if "qUrlDef" in kvargs and kvargs["qUrlDef"] is not None:
            self_.qUrlDef = kvargs["qUrlDef"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class StaticContentUrl:
    """
    In addition, this structure can return dynamic properties.

    Attributes
    ----------
    qUrl: str
      Relative path of the thumbnail.
    """

    qUrl: str = None

    def __init__(self_, **kvargs):
        if "qUrl" in kvargs and kvargs["qUrl"] is not None:
            self_.qUrl = kvargs["qUrl"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class StaticContentUrlDef:
    """
    In addition, this structure can contain dynamic properties.

    Attributes
    ----------
    qUrl: str
      Relative path of the thumbnail.
    """

    qUrl: str = None

    def __init__(self_, **kvargs):
        if "qUrl" in kvargs and kvargs["qUrl"] is not None:
            self_.qUrl = kvargs["qUrl"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class StoreTempSelectionStateReturn:
    """

    Attributes
    ----------
    qId: str
    qReturn: bool
    """

    qId: str = None
    qReturn: bool = None

    def __init__(self_, **kvargs):
        if "qId" in kvargs and kvargs["qId"] is not None:
            self_.qId = kvargs["qId"]
        if "qReturn" in kvargs and kvargs["qReturn"] is not None:
            self_.qReturn = kvargs["qReturn"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class StringExpr:
    """

    Attributes
    ----------
    qv: str
      Expression evaluated to string.
    """

    qv: str = None

    def __init__(self_, **kvargs):
        if "qv" in kvargs and kvargs["qv"] is not None:
            self_.qv = kvargs["qv"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class StringExpression:
    """
     Properties:
    Abbreviated syntax:
    "qStringExpression":"=<expression>"
    Extended object syntax:
    "qStringExpression":{"qExpr":"=<expression>"}
    Where:

    • < expression > is a string

    The "=" sign in the string expression is not mandatory. Even if the "=" sign is not given, the expression is evaluated. A string expression is not evaluated, if the expression is surrounded by simple quotes.
    The result of the evaluation of the expression can be of any type, as it is returned as a JSON (quoted) string.

    Attributes
    ----------
    qExpr: str
    """

    qExpr: str = None

    def __init__(self_, **kvargs):
        if "qExpr" in kvargs and kvargs["qExpr"] is not None:
            self_.qExpr = kvargs["qExpr"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SymbolFrequency:
    """

    Attributes
    ----------
    qFrequency: int
      Frequency of the above symbol in the field
    qSymbol: SymbolValue
      Symbol. Either string and NaN or number alone
    """

    qFrequency: int = None
    qSymbol: SymbolValue = None

    def __init__(self_, **kvargs):
        if "qFrequency" in kvargs and kvargs["qFrequency"] is not None:
            self_.qFrequency = kvargs["qFrequency"]
        if "qSymbol" in kvargs and kvargs["qSymbol"] is not None:
            if (
                type(kvargs["qSymbol"]).__name__
                == SymbolFrequency.__annotations__["qSymbol"]
            ):
                self_.qSymbol = kvargs["qSymbol"]
            else:
                self_.qSymbol = SymbolValue(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qSymbol"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SymbolValue:
    """

    Attributes
    ----------
    qNumber: float
      Numeric value of the symbol. NaN otherwise.
    qText: str
      String value of the symbol. This parameter is optional and present only if Symbol is a string.
    """

    qNumber: float = None
    qText: str = None

    def __init__(self_, **kvargs):
        if "qNumber" in kvargs and kvargs["qNumber"] is not None:
            self_.qNumber = kvargs["qNumber"]
        if "qText" in kvargs and kvargs["qText"] is not None:
            self_.qText = kvargs["qText"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableProfilingData:
    """

    Attributes
    ----------
    qFieldProfiling: list[FieldInTableProfilingData]
      Field values profiling info
    qNoOfRows: int
      Number of rows in the table.
    """

    qFieldProfiling: list[FieldInTableProfilingData] = None
    qNoOfRows: int = None

    def __init__(self_, **kvargs):
        if "qFieldProfiling" in kvargs and kvargs["qFieldProfiling"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == TableProfilingData.__annotations__["qFieldProfiling"]
                for e in kvargs["qFieldProfiling"]
            ):
                self_.qFieldProfiling = kvargs["qFieldProfiling"]
            else:
                self_.qFieldProfiling = [
                    FieldInTableProfilingData(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qFieldProfiling"]
                ]
        if "qNoOfRows" in kvargs and kvargs["qNoOfRows"] is not None:
            self_.qNoOfRows = kvargs["qNoOfRows"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableRecord:
    """

    Attributes
    ----------
    qComment: str
      Comment related to the table.
    qFields: list[FieldInTableData]
      Information about the fields in the table.
    qIsDirectDiscovery: bool
      If set to true, Direct Discovery is used.
      Direct Discovery fields are not loaded into memory and remain in the external database.
    qIsSynthetic: bool
      This property is set to true if the table contains a synthetic key.
    qLoose: bool
      This property is set to true if the table is loose.
    qName: str
      Name of the table.
    qNoOfRows: int
      Number of rows in the table.
    qPos: Point
      Information about the position of the table.
    qProfilingData: TableProfilingData
      Profiling information of the table.
    qTableTags: list[str]
      List of tags related to the table.
    """

    qComment: str = None
    qFields: list[FieldInTableData] = None
    qIsDirectDiscovery: bool = None
    qIsSynthetic: bool = None
    qLoose: bool = None
    qName: str = None
    qNoOfRows: int = None
    qPos: Point = None
    qProfilingData: TableProfilingData = None
    qTableTags: list[str] = None

    def __init__(self_, **kvargs):
        if "qComment" in kvargs and kvargs["qComment"] is not None:
            self_.qComment = kvargs["qComment"]
        if "qFields" in kvargs and kvargs["qFields"] is not None:
            if all(
                f"list[{type(e).__name__}]" == TableRecord.__annotations__["qFields"]
                for e in kvargs["qFields"]
            ):
                self_.qFields = kvargs["qFields"]
            else:
                self_.qFields = [
                    FieldInTableData(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qFields"]
                ]
        if "qIsDirectDiscovery" in kvargs and kvargs["qIsDirectDiscovery"] is not None:
            self_.qIsDirectDiscovery = kvargs["qIsDirectDiscovery"]
        if "qIsSynthetic" in kvargs and kvargs["qIsSynthetic"] is not None:
            self_.qIsSynthetic = kvargs["qIsSynthetic"]
        if "qLoose" in kvargs and kvargs["qLoose"] is not None:
            self_.qLoose = kvargs["qLoose"]
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if "qNoOfRows" in kvargs and kvargs["qNoOfRows"] is not None:
            self_.qNoOfRows = kvargs["qNoOfRows"]
        if "qPos" in kvargs and kvargs["qPos"] is not None:
            if type(kvargs["qPos"]).__name__ == TableRecord.__annotations__["qPos"]:
                self_.qPos = kvargs["qPos"]
            else:
                self_.qPos = Point(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qPos"],
                )
        if "qProfilingData" in kvargs and kvargs["qProfilingData"] is not None:
            if (
                type(kvargs["qProfilingData"]).__name__
                == TableRecord.__annotations__["qProfilingData"]
            ):
                self_.qProfilingData = kvargs["qProfilingData"]
            else:
                self_.qProfilingData = TableProfilingData(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qProfilingData"],
                )
        if "qTableTags" in kvargs and kvargs["qTableTags"] is not None:
            self_.qTableTags = kvargs["qTableTags"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableRow:
    """

    Attributes
    ----------
    qValue: list[FieldValue]
      Array of field values.
    """

    qValue: list[FieldValue] = None

    def __init__(self_, **kvargs):
        if "qValue" in kvargs and kvargs["qValue"] is not None:
            if all(
                f"list[{type(e).__name__}]" == TableRow.__annotations__["qValue"]
                for e in kvargs["qValue"]
            ):
                self_.qValue = kvargs["qValue"]
            else:
                self_.qValue = [
                    FieldValue(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qValue"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableViewBroomPointSaveInfo:
    """

    Attributes
    ----------
    qFields: list[str]
      List of fields in the table.
    qPos: Point
      Information about the position of the broom point.
    qTable: str
      Name of the table.
    """

    qFields: list[str] = None
    qPos: Point = None
    qTable: str = None

    def __init__(self_, **kvargs):
        if "qFields" in kvargs and kvargs["qFields"] is not None:
            self_.qFields = kvargs["qFields"]
        if "qPos" in kvargs and kvargs["qPos"] is not None:
            if (
                type(kvargs["qPos"]).__name__
                == TableViewBroomPointSaveInfo.__annotations__["qPos"]
            ):
                self_.qPos = kvargs["qPos"]
            else:
                self_.qPos = Point(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qPos"],
                )
        if "qTable" in kvargs and kvargs["qTable"] is not None:
            self_.qTable = kvargs["qTable"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableViewConnectionPointSaveInfo:
    """

    Attributes
    ----------
    qFields: list[str]
      List of the fields in the table.
    qPos: Point
      Information about the position of the connection point.
    """

    qFields: list[str] = None
    qPos: Point = None

    def __init__(self_, **kvargs):
        if "qFields" in kvargs and kvargs["qFields"] is not None:
            self_.qFields = kvargs["qFields"]
        if "qPos" in kvargs and kvargs["qPos"] is not None:
            if (
                type(kvargs["qPos"]).__name__
                == TableViewConnectionPointSaveInfo.__annotations__["qPos"]
            ):
                self_.qPos = kvargs["qPos"]
            else:
                self_.qPos = Point(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qPos"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableViewCtlSaveInfo:
    """

    Attributes
    ----------
    qInternalView: TableViewSaveInfo
      Internal view mode.
    qSourceView: TableViewSaveInfo
      Source view mode.
    """

    qInternalView: TableViewSaveInfo = None
    qSourceView: TableViewSaveInfo = None

    def __init__(self_, **kvargs):
        if "qInternalView" in kvargs and kvargs["qInternalView"] is not None:
            if (
                type(kvargs["qInternalView"]).__name__
                == TableViewCtlSaveInfo.__annotations__["qInternalView"]
            ):
                self_.qInternalView = kvargs["qInternalView"]
            else:
                self_.qInternalView = TableViewSaveInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qInternalView"],
                )
        if "qSourceView" in kvargs and kvargs["qSourceView"] is not None:
            if (
                type(kvargs["qSourceView"]).__name__
                == TableViewCtlSaveInfo.__annotations__["qSourceView"]
            ):
                self_.qSourceView = kvargs["qSourceView"]
            else:
                self_.qSourceView = TableViewSaveInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qSourceView"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableViewDlgSaveInfo:
    """

    Attributes
    ----------
    qCtlInfo: TableViewCtlSaveInfo
      Set of data for internal and source view modes.
    qMode: int
      View mode to display when opening Qlik Sense data model viewer.
      One of:

      • 0 for internal view mode.

      • 1 for source view mode.
    qPos: Rect
      Information about the position of the dialog window.
      Not used in Qlik Sense.
    """

    qCtlInfo: TableViewCtlSaveInfo = None
    qMode: int = None
    qPos: Rect = None

    def __init__(self_, **kvargs):
        if "qCtlInfo" in kvargs and kvargs["qCtlInfo"] is not None:
            if (
                type(kvargs["qCtlInfo"]).__name__
                == TableViewDlgSaveInfo.__annotations__["qCtlInfo"]
            ):
                self_.qCtlInfo = kvargs["qCtlInfo"]
            else:
                self_.qCtlInfo = TableViewCtlSaveInfo(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qCtlInfo"],
                )
        if "qMode" in kvargs and kvargs["qMode"] is not None:
            self_.qMode = kvargs["qMode"]
        if "qPos" in kvargs and kvargs["qPos"] is not None:
            if (
                type(kvargs["qPos"]).__name__
                == TableViewDlgSaveInfo.__annotations__["qPos"]
            ):
                self_.qPos = kvargs["qPos"]
            else:
                self_.qPos = Rect(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qPos"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableViewSaveInfo:
    """

    Attributes
    ----------
    qBroomPoints: list[TableViewBroomPointSaveInfo]
      List of the broom points in the database model viewer.
      Not used in Qlik Sense.
    qConnectionPoints: list[TableViewConnectionPointSaveInfo]
      List of connection points in the database model viewer.
      Not used in Qlik Sense.
    qTables: list[TableViewTableWinSaveInfo]
      List of the tables in the database model viewer.
    qZoomFactor: float
      Zoom factor in the database model viewer.
      The default value is 1.0.
    """

    qBroomPoints: list[TableViewBroomPointSaveInfo] = None
    qConnectionPoints: list[TableViewConnectionPointSaveInfo] = None
    qTables: list[TableViewTableWinSaveInfo] = None
    qZoomFactor: float = 1

    def __init__(self_, **kvargs):
        if "qBroomPoints" in kvargs and kvargs["qBroomPoints"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == TableViewSaveInfo.__annotations__["qBroomPoints"]
                for e in kvargs["qBroomPoints"]
            ):
                self_.qBroomPoints = kvargs["qBroomPoints"]
            else:
                self_.qBroomPoints = [
                    TableViewBroomPointSaveInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qBroomPoints"]
                ]
        if "qConnectionPoints" in kvargs and kvargs["qConnectionPoints"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == TableViewSaveInfo.__annotations__["qConnectionPoints"]
                for e in kvargs["qConnectionPoints"]
            ):
                self_.qConnectionPoints = kvargs["qConnectionPoints"]
            else:
                self_.qConnectionPoints = [
                    TableViewConnectionPointSaveInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qConnectionPoints"]
                ]
        if "qTables" in kvargs and kvargs["qTables"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == TableViewSaveInfo.__annotations__["qTables"]
                for e in kvargs["qTables"]
            ):
                self_.qTables = kvargs["qTables"]
            else:
                self_.qTables = [
                    TableViewTableWinSaveInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qTables"]
                ]
        if "qZoomFactor" in kvargs and kvargs["qZoomFactor"] is not None:
            self_.qZoomFactor = kvargs["qZoomFactor"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TableViewTableWinSaveInfo:
    """

    Attributes
    ----------
    qCaption: str
      Table name.
    qPos: Rect
      Information about the position of the table.
    """

    qCaption: str = None
    qPos: Rect = None

    def __init__(self_, **kvargs):
        if "qCaption" in kvargs and kvargs["qCaption"] is not None:
            self_.qCaption = kvargs["qCaption"]
        if "qPos" in kvargs and kvargs["qPos"] is not None:
            if (
                type(kvargs["qPos"]).__name__
                == TableViewTableWinSaveInfo.__annotations__["qPos"]
            ):
                self_.qPos = kvargs["qPos"]
            else:
                self_.qPos = Rect(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qPos"],
                )
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TextMacro:
    """

    Attributes
    ----------
    qDisplayString: str
      Variable value.
    qIsReserved: bool
      Is set to true if the variable is a reserved variable.
    qIsSystem: bool
      Is set to true if the variable is a system variable.
    qRefSeqNo: int
      Order in which the variable was referenced during the script execution.
      The same number sequence is used for both qRefSeqNo and qSetSeqNo .
    qSetSeqNo: int
      Order in which the variable was updated during the script execution.
      The same number sequence is used for both qRefSeqNo and qSetSeqNo .
    qTag: str
      Name of the variable.
    """

    qDisplayString: str = None
    qIsReserved: bool = None
    qIsSystem: bool = None
    qRefSeqNo: int = None
    qSetSeqNo: int = None
    qTag: str = None

    def __init__(self_, **kvargs):
        if "qDisplayString" in kvargs and kvargs["qDisplayString"] is not None:
            self_.qDisplayString = kvargs["qDisplayString"]
        if "qIsReserved" in kvargs and kvargs["qIsReserved"] is not None:
            self_.qIsReserved = kvargs["qIsReserved"]
        if "qIsSystem" in kvargs and kvargs["qIsSystem"] is not None:
            self_.qIsSystem = kvargs["qIsSystem"]
        if "qRefSeqNo" in kvargs and kvargs["qRefSeqNo"] is not None:
            self_.qRefSeqNo = kvargs["qRefSeqNo"]
        if "qSetSeqNo" in kvargs and kvargs["qSetSeqNo"] is not None:
            self_.qSetSeqNo = kvargs["qSetSeqNo"]
        if "qTag" in kvargs and kvargs["qTag"] is not None:
            self_.qTag = kvargs["qTag"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TotalMode:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TransformAppParameters:
    """

    Attributes
    ----------
    qName: str
      The name (title) of the application
    qScriptParameterPrefix: str
      Prefix to be used on inserted ScriptParameters, only applicable for template apps
    qSpaceId: str
      ID of the space where the app is to be created. Empty value implies Personal space
    """

    qName: str = None
    qScriptParameterPrefix: str = None
    qSpaceId: str = None

    def __init__(self_, **kvargs):
        if "qName" in kvargs and kvargs["qName"] is not None:
            self_.qName = kvargs["qName"]
        if (
            "qScriptParameterPrefix" in kvargs
            and kvargs["qScriptParameterPrefix"] is not None
        ):
            self_.qScriptParameterPrefix = kvargs["qScriptParameterPrefix"]
        if "qSpaceId" in kvargs and kvargs["qSpaceId"] is not None:
            self_.qSpaceId = kvargs["qSpaceId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TransformAppResult:
    """

    Attributes
    ----------
    qAppId: str
      ID of created App
    """

    qAppId: str = None

    def __init__(self_, **kvargs):
        if "qAppId" in kvargs and kvargs["qAppId"] is not None:
            self_.qAppId = kvargs["qAppId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TreeData:
    """
    Renders the properties of a TreeData object. Is the layout for TreeDataDef.
    For more information about the definition of TreeData, see Generic object.
    To retrieve data from the TreeData object, use the method called GetHyperCubeTreeData.

    Attributes
    ----------
    qCalcCondMsg: str
      The message displayed if calculation condition is not fulfilled.
    qDimensionInfo: list[NxTreeDimensionInfo]
      Information on the dimension.
    qEffectiveInterColumnSortOrder: list[int]
      Defines the order of the dimenion levels/columns in the TreeData object.
      Column numbers are separated by a comma.
      Example: [1,0,2] means that the first level in the tree structure is dimension 1, followed by dimension 0 and dimension 2.
    qError: NxValidationError
      This parameter is optional and is displayed in case of error.
    qHasOtherValues: bool
      True if other row exists.
    qLastExpandedPos: NxCellPosition
      Position of the last expended cell.
      This property is optional.
    qMeasureInfo: list[NxMeasureInfo]
      Information on the measures calculated on the whole tree.
    qNodesOnDim: list[int]
      The total number of nodes on each dimension.
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    qTitle: str
      Title of the TreeData object, for example the title of a chart.
    qTreeDataPages: list[NxTreeNode]
      Set of data.
      Is empty if nothing has been defined in qInitialDataFetch in TreeDataDef.
    """

    qCalcCondMsg: str = None
    qDimensionInfo: list[NxTreeDimensionInfo] = None
    qEffectiveInterColumnSortOrder: list[int] = None
    qError: NxValidationError = None
    qHasOtherValues: bool = None
    qLastExpandedPos: NxCellPosition = None
    qMeasureInfo: list[NxMeasureInfo] = None
    qNodesOnDim: list[int] = None
    qStateName: str = None
    qTitle: str = None
    qTreeDataPages: list[NxTreeNode] = None

    def __init__(self_, **kvargs):
        if "qCalcCondMsg" in kvargs and kvargs["qCalcCondMsg"] is not None:
            self_.qCalcCondMsg = kvargs["qCalcCondMsg"]
        if "qDimensionInfo" in kvargs and kvargs["qDimensionInfo"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == TreeData.__annotations__["qDimensionInfo"]
                for e in kvargs["qDimensionInfo"]
            ):
                self_.qDimensionInfo = kvargs["qDimensionInfo"]
            else:
                self_.qDimensionInfo = [
                    NxTreeDimensionInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qDimensionInfo"]
                ]
        if (
            "qEffectiveInterColumnSortOrder" in kvargs
            and kvargs["qEffectiveInterColumnSortOrder"] is not None
        ):
            self_.qEffectiveInterColumnSortOrder = kvargs[
                "qEffectiveInterColumnSortOrder"
            ]
        if "qError" in kvargs and kvargs["qError"] is not None:
            if type(kvargs["qError"]).__name__ == TreeData.__annotations__["qError"]:
                self_.qError = kvargs["qError"]
            else:
                self_.qError = NxValidationError(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qError"],
                )
        if "qHasOtherValues" in kvargs and kvargs["qHasOtherValues"] is not None:
            self_.qHasOtherValues = kvargs["qHasOtherValues"]
        if "qLastExpandedPos" in kvargs and kvargs["qLastExpandedPos"] is not None:
            if (
                type(kvargs["qLastExpandedPos"]).__name__
                == TreeData.__annotations__["qLastExpandedPos"]
            ):
                self_.qLastExpandedPos = kvargs["qLastExpandedPos"]
            else:
                self_.qLastExpandedPos = NxCellPosition(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qLastExpandedPos"],
                )
        if "qMeasureInfo" in kvargs and kvargs["qMeasureInfo"] is not None:
            if all(
                f"list[{type(e).__name__}]" == TreeData.__annotations__["qMeasureInfo"]
                for e in kvargs["qMeasureInfo"]
            ):
                self_.qMeasureInfo = kvargs["qMeasureInfo"]
            else:
                self_.qMeasureInfo = [
                    NxMeasureInfo(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qMeasureInfo"]
                ]
        if "qNodesOnDim" in kvargs and kvargs["qNodesOnDim"] is not None:
            self_.qNodesOnDim = kvargs["qNodesOnDim"]
        if "qStateName" in kvargs and kvargs["qStateName"] is not None:
            self_.qStateName = kvargs["qStateName"]
        if "qTitle" in kvargs and kvargs["qTitle"] is not None:
            self_.qTitle = kvargs["qTitle"]
        if "qTreeDataPages" in kvargs and kvargs["qTreeDataPages"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == TreeData.__annotations__["qTreeDataPages"]
                for e in kvargs["qTreeDataPages"]
            ):
                self_.qTreeDataPages = kvargs["qTreeDataPages"]
            else:
                self_.qTreeDataPages = [
                    NxTreeNode(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qTreeDataPages"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class TreeDataDef:
    """
    Defines the properties of a TreeData object.
    For more information about the definition of a TreeData object, see Generic object.

    Attributes
    ----------
    qCalcCondition: NxCalcCond
      Specifies a calculation condition object.
      If CalcCondition.Cond is not fulfilled, the TreeData is excluded from the calculation and CalcCondition.Msg is evaluated.
      By default, there is no calculation condition.
      This property is optional.
    qContextSetExpression: str
      Set Expression valid for the whole cube. Used to limit computations to the set specified.
    qDimensions: list[NxTreeDimensionDef]
      Array of dimensions.
    qExpansionState: list[ExpansionData]
      Expansion state per dimension.
    qInitialDataFetch: list[NxTreeDataOption]
      Initial data set.
      This property is optional.
    qInterColumnSortOrder: list[int]
      Defines the order of the dimension levels/columns in the TreeData object.
      Column numbers are separated by a comma.
      Example: [1,0,2] means that the first level in the tree structure is dimension 1, followed by dimension 0 and dimension 2.
      The default sort order is the order in which the dimensions and measures have been defined in the TreeDataDef.
    qOpenFullyExpanded: bool
      If this property is set to true, the cells are opened expanded. The default value is false.
    qPopulateMissing: bool
      If this property is set to true, the missing symbols (if any) are replaced by 0 if the value is a numeric and by an empty string if the value is a string.
      The default value is false.
    qStateName: str
      Name of the alternate state.
      Default is current selections $ .
    qSuppressMissing: bool
      Removes missing values.
    qSuppressZero: bool
      Removes zero values.
    qTitle: StringExpr
      Title of the TreeData object, for example the title of a chart.
    qValueExprs: list[NxMeasure]
      List of measures to calculate on the whole tree.
    """

    qCalcCondition: NxCalcCond = None
    qContextSetExpression: str = None
    qDimensions: list[NxTreeDimensionDef] = None
    qExpansionState: list[ExpansionData] = None
    qInitialDataFetch: list[NxTreeDataOption] = None
    qInterColumnSortOrder: list[int] = None
    qOpenFullyExpanded: bool = None
    qPopulateMissing: bool = None
    qStateName: str = None
    qSuppressMissing: bool = None
    qSuppressZero: bool = None
    qTitle: StringExpr = None
    qValueExprs: list[NxMeasure] = None

    def __init__(self_, **kvargs):
        if "qCalcCondition" in kvargs and kvargs["qCalcCondition"] is not None:
            if (
                type(kvargs["qCalcCondition"]).__name__
                == TreeDataDef.__annotations__["qCalcCondition"]
            ):
                self_.qCalcCondition = kvargs["qCalcCondition"]
            else:
                self_.qCalcCondition = NxCalcCond(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qCalcCondition"],
                )
        if (
            "qContextSetExpression" in kvargs
            and kvargs["qContextSetExpression"] is not None
        ):
            self_.qContextSetExpression = kvargs["qContextSetExpression"]
        if "qDimensions" in kvargs and kvargs["qDimensions"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == TreeDataDef.__annotations__["qDimensions"]
                for e in kvargs["qDimensions"]
            ):
                self_.qDimensions = kvargs["qDimensions"]
            else:
                self_.qDimensions = [
                    NxTreeDimensionDef(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qDimensions"]
                ]
        if "qExpansionState" in kvargs and kvargs["qExpansionState"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == TreeDataDef.__annotations__["qExpansionState"]
                for e in kvargs["qExpansionState"]
            ):
                self_.qExpansionState = kvargs["qExpansionState"]
            else:
                self_.qExpansionState = [
                    ExpansionData(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qExpansionState"]
                ]
        if "qInitialDataFetch" in kvargs and kvargs["qInitialDataFetch"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == TreeDataDef.__annotations__["qInitialDataFetch"]
                for e in kvargs["qInitialDataFetch"]
            ):
                self_.qInitialDataFetch = kvargs["qInitialDataFetch"]
            else:
                self_.qInitialDataFetch = [
                    NxTreeDataOption(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qInitialDataFetch"]
                ]
        if (
            "qInterColumnSortOrder" in kvargs
            and kvargs["qInterColumnSortOrder"] is not None
        ):
            self_.qInterColumnSortOrder = kvargs["qInterColumnSortOrder"]
        if "qOpenFullyExpanded" in kvargs and kvargs["qOpenFullyExpanded"] is not None:
            self_.qOpenFullyExpanded = kvargs["qOpenFullyExpanded"]
        if "qPopulateMissing" in kvargs and kvargs["qPopulateMissing"] is not None:
            self_.qPopulateMissing = kvargs["qPopulateMissing"]
        if "qStateName" in kvargs and kvargs["qStateName"] is not None:
            self_.qStateName = kvargs["qStateName"]
        if "qSuppressMissing" in kvargs and kvargs["qSuppressMissing"] is not None:
            self_.qSuppressMissing = kvargs["qSuppressMissing"]
        if "qSuppressZero" in kvargs and kvargs["qSuppressZero"] is not None:
            self_.qSuppressZero = kvargs["qSuppressZero"]
        if "qTitle" in kvargs and kvargs["qTitle"] is not None:
            if type(kvargs["qTitle"]).__name__ == TreeDataDef.__annotations__["qTitle"]:
                self_.qTitle = kvargs["qTitle"]
            else:
                self_.qTitle = StringExpr(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qTitle"],
                )
        if "qValueExprs" in kvargs and kvargs["qValueExprs"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == TreeDataDef.__annotations__["qValueExprs"]
                for e in kvargs["qValueExprs"]
            ):
                self_.qValueExprs = kvargs["qValueExprs"]
            else:
                self_.qValueExprs = [
                    NxMeasure(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qValueExprs"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UndoInfo:
    """
    Displays information about the number of possible undos and redos. Is the layout for UndoInfoDef.

    Attributes
    ----------
    qRedoCount: int
      Number of possible redos.
    qUndoCount: int
      Number of possible undos.
    """

    qRedoCount: int = None
    qUndoCount: int = None

    def __init__(self_, **kvargs):
        if "qRedoCount" in kvargs and kvargs["qRedoCount"] is not None:
            self_.qRedoCount = kvargs["qRedoCount"]
        if "qUndoCount" in kvargs and kvargs["qUndoCount"] is not None:
            self_.qUndoCount = kvargs["qUndoCount"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UndoInfoDef:
    """
    Defines if an object should contain information on the number of possible undo and redo.

     Properties:
    "qUndoInfoDef": {}
    The numbers of undos and redos are empty when an object is created. The number of possible undos is increased every time an action (for example, create a child, set some properties) on the object is performed. The number of possible redos is increased every time an undo action is performed.

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UsageEnum:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ValueExpr:
    """

    Attributes
    ----------
    qv: str
      Expression evaluated to dual.
    """

    qv: str = None

    def __init__(self_, **kvargs):
        if "qv" in kvargs and kvargs["qv"] is not None:
            self_.qv = kvargs["qv"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ValueExpression:
    """
     Properties:
    Abbreviated syntax:
    "qValueExpression":"=<expression>"
    Extended object syntax:
    "qValueExpression":{"qExpr":"=<expression>"}
    Where:

    • < expression > is a string.

    The "=" sign in the value expression is not mandatory. Even if the "=" sign is not given, the expression is evaluated.
    The expression is evaluated as a numeric.

    Attributes
    ----------
    qExpr: str
    """

    qExpr: str = None

    def __init__(self_, **kvargs):
        if "qExpr" in kvargs and kvargs["qExpr"] is not None:
            self_.qExpr = kvargs["qExpr"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Variable:
    """

    Attributes
    ----------
    qGenericId: str
      Object ID.
    qGenericType: str
      The type of the object.
    qHandle: int
      The handle used to connect to object.
    qType: str
      The native type of the object.
    """

    _session: RpcSession = None
    qGenericId: str = None
    qGenericType: str = None
    qHandle: int = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qGenericId" in kvargs and kvargs["qGenericId"] is not None:
            self_.qGenericId = kvargs["qGenericId"]
        if "qGenericType" in kvargs and kvargs["qGenericType"] is not None:
            self_.qGenericType = kvargs["qGenericType"]
        if "qHandle" in kvargs and kvargs["qHandle"] is not None:
            self_.qHandle = kvargs["qHandle"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}) or k == "_session":
                self_.__setattr__(k, v)

    def get_content(self) -> AlfaNumString:
        """
        Returns the calculated value of a variable.

        Parameters
        ----------
        """
        warnings.warn("GetContent is deprecated", DeprecationWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetContent", handle)["qContent"]
        obj = AlfaNumString(**response)
        return obj

    def get_raw_content(self) -> str:
        """
        Returns the raw value of a variable.

        Parameters
        ----------
        """
        warnings.warn("GetRawContent is deprecated", DeprecationWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetRawContent", handle)["qReturn"]
        return response

    def set_content(self, qContent: str, qUpdateMRU: bool) -> bool:
        """
        Sets a value to a variable.

        Parameters
        ----------
        qContent: str
          Value of the variable.
        qUpdateMRU: bool
          If set to true, the value is added to the Most Recently Used (MRU) list.
        """
        warnings.warn("SetContent is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qContent"] = qContent
        params["qUpdateMRU"] = qUpdateMRU
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetContent", handle, **params)["qReturn"]
        return response

    def force_content(self, qs: str, qd: float) -> object:
        """
        Sets the value of a dual variable overriding any input constraints.

        Parameters
        ----------
        qs: str
          String representation of a dual value.
          Set this parameter to "", if the string representation is to be Null.
        qd: float
          Numeric representation of a dual value.
        """
        warnings.warn("ForceContent is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qs"] = qs
        params["qd"] = qd
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("ForceContent", handle, **params)
        return response

    def get_nx_properties(self) -> NxVariableProperties:
        """
        Gets the properties of a variable.

        Parameters
        ----------
        """
        warnings.warn("GetNxProperties is deprecated", DeprecationWarning, stacklevel=2)
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("GetNxProperties", handle)["qProperties"]
        obj = NxVariableProperties(**response)
        return obj

    def set_nx_properties(self, qProperties: NxVariableProperties) -> object:
        """
        Sets some properties to a variable.

        Parameters
        ----------
        qProperties: NxVariableProperties
          Information about the properties of the variable
        """
        warnings.warn("SetNxProperties is deprecated", DeprecationWarning, stacklevel=2)
        params = {}
        params["qProperties"] = qProperties
        handle = -1 if not hasattr(self, "qHandle") else self.qHandle
        response = self._session.send("SetNxProperties", handle, **params)
        return response

    def on(self, event_name, listener):
        self._session.on_handle(self.qHandle, event_name, listener)


@dataclass
class VariableList:
    """
    Lists the variables in an app. Is the layout for VariableListDef.

    Attributes
    ----------
    qItems: list[NxVariableListItem]
      List of the variables.
    """

    qItems: list[NxVariableListItem] = None

    def __init__(self_, **kvargs):
        if "qItems" in kvargs and kvargs["qItems"] is not None:
            if all(
                f"list[{type(e).__name__}]" == VariableList.__annotations__["qItems"]
                for e in kvargs["qItems"]
            ):
                self_.qItems = kvargs["qItems"]
            else:
                self_.qItems = [
                    NxVariableListItem(
                        _session=kvargs["_session"] if "_session" in kvargs else None,
                        **e,
                    )
                    for e in kvargs["qItems"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class VariableListDef:
    """
    Defines the list of variables in an app.

    Attributes
    ----------
    qData: JsonObject
      Data
    qShowConfig: bool
      Shows the system variables if set to true.
    qShowReserved: bool
      Shows the reserved variables if set to true.
    qShowSession: bool
      Shows the session variables if set to true.
    qType: str
      Type of variables to include in the list.
    """

    qData: JsonObject = None
    qShowConfig: bool = None
    qShowReserved: bool = None
    qShowSession: bool = None
    qType: str = None

    def __init__(self_, **kvargs):
        if "qData" in kvargs and kvargs["qData"] is not None:
            if (
                type(kvargs["qData"]).__name__
                == VariableListDef.__annotations__["qData"]
            ):
                self_.qData = kvargs["qData"]
            else:
                self_.qData = JsonObject(
                    _session=kvargs["_session"] if "_session" in kvargs else None,
                    **kvargs["qData"],
                )
        if "qShowConfig" in kvargs and kvargs["qShowConfig"] is not None:
            self_.qShowConfig = kvargs["qShowConfig"]
        if "qShowReserved" in kvargs and kvargs["qShowReserved"] is not None:
            self_.qShowReserved = kvargs["qShowReserved"]
        if "qShowSession" in kvargs and kvargs["qShowSession"] is not None:
            self_.qShowSession = kvargs["qShowSession"]
        if "qType" in kvargs and kvargs["qType"] is not None:
            self_.qType = kvargs["qType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)
