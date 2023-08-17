# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import List, Literal

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class ItemResultResponseBody:
    """
    An item.

    Attributes
    ----------
    actions: list[str]
      The actions that the user can perform on the item.
    collectionIds: list[str]
      The ID of the collections that the item has been added to.
    createdAt: str
      The RFC3339 datetime when the item was created.
    creatorId: str
      The ID of the user who created the item. This is only populated if the JWT contains a userId.
    description: str
    id: str
      The item's unique identifier.
    isFavorited: bool
      The flag that indicates if item is in the user's favorites collection.
    itemViews: ItemViewsResponseBody
    links: ItemLinksResponseBody
    meta: ItemMetaResponseBody
      Item metadata and computed fields.
    name: str
    ownerId: str
      The ID of the user who owns the item.
    resourceAttributes: object
    resourceCreatedAt: str
      The RFC3339 datetime when the resource that the item references was created.
    resourceCustomAttributes: object
    resourceId: str
      The case-sensitive string used to search for an item by resourceId. If resourceId is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceLink: str
      The case-sensitive string used to search for an item by resourceLink. If resourceLink is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceReloadEndTime: str
      The RFC3339 datetime when the resource last reload ended.
    resourceReloadStatus: str
      If the resource last reload was successful or not.
    resourceSize: ItemsResourceSizeResponseBody
    resourceSubType: str
      Optional field defining the item's subtype, if any.
    resourceType: Literal["app", "collection", "qlikview", "insight", "qvapp", "genericlink", "sharingservicetask", "note", "dataasset", "dataset", "automation", "automl-experiment", "automl-deployment"]
      The case-sensitive string defining the item's type.
    resourceUpdatedAt: str
      The RFC3339 datetime when the resource that the item references was last updated.
    spaceId: str
      The space's unique identifier.
    tenantId: str
      The ID of the tenant that owns the item. This is populated using the JWT.
    thumbnailId: str
      The item thumbnail's unique identifier. This is optional for internal resources.
    updatedAt: str
      The RFC3339 datetime when the item was last updated.
    updaterId: str
      ID of the user who last updated the item. This is only populated if the JWT contains a userId.
    """

    actions: list[str] = None
    collectionIds: list[str] = None
    createdAt: str = None
    creatorId: str = None
    description: str = None
    id: str = None
    isFavorited: bool = None
    itemViews: ItemViewsResponseBody = None
    links: ItemLinksResponseBody = None
    meta: ItemMetaResponseBody = None
    name: str = None
    ownerId: str = None
    resourceAttributes: object = None
    resourceCreatedAt: str = None
    resourceCustomAttributes: object = None
    resourceId: str = None
    resourceLink: str = None
    resourceReloadEndTime: str = None
    resourceReloadStatus: str = None
    resourceSize: ItemsResourceSizeResponseBody = None
    resourceSubType: str = None
    resourceType: Literal[
        "app",
        "collection",
        "qlikview",
        "insight",
        "qvapp",
        "genericlink",
        "sharingservicetask",
        "note",
        "dataasset",
        "dataset",
        "automation",
        "automl-experiment",
        "automl-deployment",
    ] = None
    resourceUpdatedAt: str = None
    spaceId: str = None
    tenantId: str = None
    thumbnailId: str = None
    updatedAt: str = None
    updaterId: str = None

    def __init__(self_, **kvargs):
        if "actions" in kvargs and kvargs["actions"] is not None:
            self_.actions = kvargs["actions"]
        if "collectionIds" in kvargs and kvargs["collectionIds"] is not None:
            self_.collectionIds = kvargs["collectionIds"]
        if "createdAt" in kvargs and kvargs["createdAt"] is not None:
            self_.createdAt = kvargs["createdAt"]
        if "creatorId" in kvargs and kvargs["creatorId"] is not None:
            self_.creatorId = kvargs["creatorId"]
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "isFavorited" in kvargs and kvargs["isFavorited"] is not None:
            self_.isFavorited = kvargs["isFavorited"]
        if "itemViews" in kvargs and kvargs["itemViews"] is not None:
            if (
                type(kvargs["itemViews"]).__name__
                == ItemResultResponseBody.__annotations__["itemViews"]
            ):
                self_.itemViews = kvargs["itemViews"]
            else:
                self_.itemViews = ItemViewsResponseBody(**kvargs["itemViews"])
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == ItemResultResponseBody.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = ItemLinksResponseBody(**kvargs["links"])
        if "meta" in kvargs and kvargs["meta"] is not None:
            if (
                type(kvargs["meta"]).__name__
                == ItemResultResponseBody.__annotations__["meta"]
            ):
                self_.meta = kvargs["meta"]
            else:
                self_.meta = ItemMetaResponseBody(**kvargs["meta"])
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "ownerId" in kvargs and kvargs["ownerId"] is not None:
            self_.ownerId = kvargs["ownerId"]
        if "resourceAttributes" in kvargs and kvargs["resourceAttributes"] is not None:
            self_.resourceAttributes = kvargs["resourceAttributes"]
        if "resourceCreatedAt" in kvargs and kvargs["resourceCreatedAt"] is not None:
            self_.resourceCreatedAt = kvargs["resourceCreatedAt"]
        if (
            "resourceCustomAttributes" in kvargs
            and kvargs["resourceCustomAttributes"] is not None
        ):
            self_.resourceCustomAttributes = kvargs["resourceCustomAttributes"]
        if "resourceId" in kvargs and kvargs["resourceId"] is not None:
            self_.resourceId = kvargs["resourceId"]
        if "resourceLink" in kvargs and kvargs["resourceLink"] is not None:
            self_.resourceLink = kvargs["resourceLink"]
        if (
            "resourceReloadEndTime" in kvargs
            and kvargs["resourceReloadEndTime"] is not None
        ):
            self_.resourceReloadEndTime = kvargs["resourceReloadEndTime"]
        if (
            "resourceReloadStatus" in kvargs
            and kvargs["resourceReloadStatus"] is not None
        ):
            self_.resourceReloadStatus = kvargs["resourceReloadStatus"]
        if "resourceSize" in kvargs and kvargs["resourceSize"] is not None:
            if (
                type(kvargs["resourceSize"]).__name__
                == ItemResultResponseBody.__annotations__["resourceSize"]
            ):
                self_.resourceSize = kvargs["resourceSize"]
            else:
                self_.resourceSize = ItemsResourceSizeResponseBody(
                    **kvargs["resourceSize"]
                )
        if "resourceSubType" in kvargs and kvargs["resourceSubType"] is not None:
            self_.resourceSubType = kvargs["resourceSubType"]
        if "resourceType" in kvargs and kvargs["resourceType"] is not None:
            self_.resourceType = kvargs["resourceType"]
        if "resourceUpdatedAt" in kvargs and kvargs["resourceUpdatedAt"] is not None:
            self_.resourceUpdatedAt = kvargs["resourceUpdatedAt"]
        if "spaceId" in kvargs and kvargs["spaceId"] is not None:
            self_.spaceId = kvargs["spaceId"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            self_.tenantId = kvargs["tenantId"]
        if "thumbnailId" in kvargs and kvargs["thumbnailId"] is not None:
            self_.thumbnailId = kvargs["thumbnailId"]
        if "updatedAt" in kvargs and kvargs["updatedAt"] is not None:
            self_.updatedAt = kvargs["updatedAt"]
        if "updaterId" in kvargs and kvargs["updaterId"] is not None:
            self_.updaterId = kvargs["updaterId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def get_collections(
        self,
        limit: int = None,
        name: str = None,
        next: str = None,
        prev: str = None,
        query: str = None,
        sort: Literal[
            "+createdAt", "-createdAt", "+name", "-name", "+updatedAt", "-updatedAt"
        ] = None,
        type: Literal["private", "public", "publicgoverned"] = None,
    ) -> ListableResource[CollectionResultResponseBody]:
        """
        Returns the collections of an item.
        Finds and returns the collections of an item. This endpoint does not return the user's favorites collection.

        Parameters
        ----------
        limit: int = None
          The maximum number of resources to return for a request. The limit must be an integer between 1 and 100 (inclusive).
        name: str = None
          The case-sensitive string used to search for a collection by name.
        next: str = None
          The cursor to the next page of resources. Provide either the next or prev cursor, but not both.
        prev: str = None
          The cursor to the previous page of resources. Provide either the next or prev cursor, but not both.
        query: str = None
          The case-insensitive string used to search for a resource by name or description.
        sort: Literal["+createdAt", "-createdAt", "+name", "-name", "+updatedAt", "-updatedAt"] = None
          The property of a resource to sort on (default sort is +createdAt). The supported properties are createdAt, updatedAt, and name. A property must be prefixed by + or   - to indicate ascending or descending sort order respectively.
        type: Literal["private", "public", "publicgoverned"] = None
          The case-sensitive string used to search for a collection by type.
        """
        query_params = {}
        if limit is not None:
            query_params["limit"] = limit
        if name is not None:
            query_params["name"] = name
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if query is not None:
            query_params["query"] = query
        if sort is not None:
            query_params["sort"] = sort
        if type is not None:
            query_params["type"] = type
        response = self.auth.rest(
            path="/items/{itemId}/collections".replace("{itemId}", self.id),
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=CollectionResultResponseBody,
            auth=self.auth,
            path="/items/{itemId}/collections".replace("{itemId}", self.id),
            query_params=query_params,
        )

    def get_publisheditems(
        self,
        limit: int = None,
        next: str = None,
        prev: str = None,
        resourceType: Literal[
            "app",
            "collection",
            "qlikview",
            "insight",
            "qvapp",
            "genericlink",
            "sharingservicetask",
            "note",
            "dataasset",
            "dataset",
            "automation",
            "automl-experiment",
            "automl-deployment",
        ] = None,
        sort: Literal[
            "+createdAt", "-createdAt", "+name", "-name", "+updatedAt", "-updatedAt"
        ] = None,
    ) -> ListableResource[CollectionResultResponseBody]:
        """
        Returns published items for a given item.
        Finds and returns the published items for a given item.

        Parameters
        ----------
        limit: int = None
          The maximum number of resources to return for a request. The limit must be an integer between 1 and 100 (inclusive).
        next: str = None
          The cursor to the next page of resources. Provide either the next or prev cursor, but not both.
        prev: str = None
          The cursor to the previous page of resources. Provide either the next or prev cursor, but not both.
        resourceType: Literal["app", "collection", "qlikview", "insight", "qvapp", "genericlink", "sharingservicetask", "note", "dataasset", "dataset", "automation", "automl-experiment", "automl-deployment"] = None
          The case-sensitive string used to search for an item by resourceType.
        sort: Literal["+createdAt", "-createdAt", "+name", "-name", "+updatedAt", "-updatedAt"] = None
          The property of a resource to sort on (default sort is +createdAt). The supported properties are createdAt, updatedAt, and name. A property must be prefixed by + or   - to indicate ascending or descending sort order respectively.
        """
        query_params = {}
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if resourceType is not None:
            query_params["resourceType"] = resourceType
        if sort is not None:
            query_params["sort"] = sort
        response = self.auth.rest(
            path="/items/{itemId}/publisheditems".replace("{itemId}", self.id),
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=CollectionResultResponseBody,
            auth=self.auth,
            path="/items/{itemId}/publisheditems".replace("{itemId}", self.id),
            query_params=query_params,
        )

    def delete(self) -> None:
        """
        Deletes an item.
        Deletes an item and removes the item from all collections.

        Parameters
        ----------
        """
        self.auth.rest(
            path="/items/{itemId}".replace("{itemId}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def set(self, data: ItemsUpdateItemRequestBody) -> ItemResultResponseBody:
        """
        Updates an item.
        Updates an item. Omitted and unsupported fields are ignored. To unset a field, provide the field's zero value.

        Parameters
        ----------
        data: ItemsUpdateItemRequestBody
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/items/{itemId}".replace("{itemId}", self.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self


@dataclass
class ItemsListItemCollectionsResponseBody:
    """
    ListItemCollectionsResponseBody result type

    Attributes
    ----------
    data: list[CollectionResultResponseBody]
    links: CollectionsLinksResponseBody
    """

    data: list[CollectionResultResponseBody] = None
    links: CollectionsLinksResponseBody = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == ItemsListItemCollectionsResponseBody.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [CollectionResultResponseBody(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == ItemsListItemCollectionsResponseBody.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = CollectionsLinksResponseBody(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsListItemsResponseBody:
    """
    ListItemsResponseBody result type

    Attributes
    ----------
    data: list[ItemResultResponseBody]
    links: ItemsLinksResponseBody
    """

    data: list[ItemResultResponseBody] = None
    links: ItemsLinksResponseBody = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == ItemsListItemsResponseBody.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [ItemResultResponseBody(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == ItemsListItemsResponseBody.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = ItemsLinksResponseBody(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsSettingsPatch(List["ItemsSettingsPatchElement"]):
    """

    Attributes
    ----------
    """

    def __init__(self_, elements):
        for e in elements:
            self_.append(ItemsSettingsPatchElement(**e))


@dataclass
class ItemsSettingsPatchElement:
    """
    A JSONPatch document as defined by RFC 6902.

    Attributes
    ----------
    op: Literal["replace"]
      The operation to be performed. Only "replace" is supported.
    path: Literal["/usageMetricsEnabled"]
      Field of Settings to be patched (updated).
    value: bool
      The value to be used within the operations.

    """

    op: Literal["replace"] = None
    path: Literal["/usageMetricsEnabled"] = None
    value: bool = None

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
class ItemsSettingsResponseBody:
    """

    Attributes
    ----------
    usageMetricsEnabled: bool
      Decides if the usage metrics will be shown in the hub UI.
    """

    usageMetricsEnabled: bool = True

    def __init__(self_, **kvargs):
        if (
            "usageMetricsEnabled" in kvargs
            and kvargs["usageMetricsEnabled"] is not None
        ):
            self_.usageMetricsEnabled = kvargs["usageMetricsEnabled"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsUpdateItemRequestBody:
    """

    Attributes
    ----------
    description: str
    name: str
    resourceAttributes: object
    resourceCustomAttributes: object
    resourceId: str
      The case-sensitive string used to search for an item by resourceId. If resourceId is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceLink: str
      The case-sensitive string used to search for an item by resourceLink. If resourceLink is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceSubType: str
      Optional field defining the item's subtype, if any.
    resourceType: Literal["app", "collection", "qlikview", "insight", "qvapp", "genericlink", "sharingservicetask", "note", "dataasset", "dataset", "automation", "automl-experiment", "automl-deployment"]
      The case-sensitive string defining the item's type.
    resourceUpdatedAt: str
      The RFC3339 datetime when the resource that the item references was last updated.
    spaceId: str
      The space's unique identifier.
    thumbnailId: str
      The item thumbnail's unique identifier. This is optional for internal resources.
    """

    description: str = None
    name: str = None
    resourceAttributes: object = None
    resourceCustomAttributes: object = None
    resourceId: str = None
    resourceLink: str = None
    resourceSubType: str = None
    resourceType: Literal[
        "app",
        "collection",
        "qlikview",
        "insight",
        "qvapp",
        "genericlink",
        "sharingservicetask",
        "note",
        "dataasset",
        "dataset",
        "automation",
        "automl-experiment",
        "automl-deployment",
    ] = None
    resourceUpdatedAt: str = None
    spaceId: str = None
    thumbnailId: str = None

    def __init__(self_, **kvargs):
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "resourceAttributes" in kvargs and kvargs["resourceAttributes"] is not None:
            self_.resourceAttributes = kvargs["resourceAttributes"]
        if (
            "resourceCustomAttributes" in kvargs
            and kvargs["resourceCustomAttributes"] is not None
        ):
            self_.resourceCustomAttributes = kvargs["resourceCustomAttributes"]
        if "resourceId" in kvargs and kvargs["resourceId"] is not None:
            self_.resourceId = kvargs["resourceId"]
        if "resourceLink" in kvargs and kvargs["resourceLink"] is not None:
            self_.resourceLink = kvargs["resourceLink"]
        if "resourceSubType" in kvargs and kvargs["resourceSubType"] is not None:
            self_.resourceSubType = kvargs["resourceSubType"]
        if "resourceType" in kvargs and kvargs["resourceType"] is not None:
            self_.resourceType = kvargs["resourceType"]
        if "resourceUpdatedAt" in kvargs and kvargs["resourceUpdatedAt"] is not None:
            self_.resourceUpdatedAt = kvargs["resourceUpdatedAt"]
        if "spaceId" in kvargs and kvargs["spaceId"] is not None:
            self_.spaceId = kvargs["spaceId"]
        if "thumbnailId" in kvargs and kvargs["thumbnailId"] is not None:
            self_.thumbnailId = kvargs["thumbnailId"]
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
class CollectionLinksResponseBody:
    """

    Attributes
    ----------
    items: Link
    self: Link
    """

    items: Link = None
    self: Link = None

    def __init__(self_, **kvargs):
        if "items" in kvargs and kvargs["items"] is not None:
            if (
                type(kvargs["items"]).__name__
                == CollectionLinksResponseBody.__annotations__["items"]
            ):
                self_.items = kvargs["items"]
            else:
                self_.items = Link(**kvargs["items"])
        if "self" in kvargs and kvargs["self"] is not None:
            if (
                type(kvargs["self"]).__name__
                == CollectionLinksResponseBody.__annotations__["self"]
            ):
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CollectionMetaResponseBody:
    """
    Collection metadata and computed fields.

    Attributes
    ----------
    items: ItemsResultResponseBody
      Multiple items.
    """

    items: ItemsResultResponseBody = None

    def __init__(self_, **kvargs):
        if "items" in kvargs and kvargs["items"] is not None:
            if (
                type(kvargs["items"]).__name__
                == CollectionMetaResponseBody.__annotations__["items"]
            ):
                self_.items = kvargs["items"]
            else:
                self_.items = ItemsResultResponseBody(**kvargs["items"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CollectionResultResponseBody:
    """
    A collection.

    Attributes
    ----------
    createdAt: str
      The RFC3339 datetime when the collection was created.
    creatorId: str
      The ID of the user who created the collection. This property is only populated if the JWT contains a userId.
    description: str
    full: bool
      States if a collection has reached its items limit or not
    id: str
      The collection's unique identifier.
    itemCount: int
      The number of items that have been added to the collection that the user has access to.
    links: CollectionLinksResponseBody
    meta: CollectionMetaResponseBody
      Collection metadata and computed fields.
    name: str
    tenantId: str
      The ID of the tenant that owns the collection. This property is populated by using JWT.
    type: Literal["private", "public", "favorite", "publicgoverned"]
    updatedAt: str
      The RFC3339 datetime when the collection was last updated.
    updaterId: str
      The ID of the user who last updated the collection. This property is only populated if the JWT contains a userId.
    """

    createdAt: str = None
    creatorId: str = None
    description: str = None
    full: bool = None
    id: str = None
    itemCount: int = None
    links: CollectionLinksResponseBody = None
    meta: CollectionMetaResponseBody = None
    name: str = None
    tenantId: str = None
    type: Literal["private", "public", "favorite", "publicgoverned"] = None
    updatedAt: str = None
    updaterId: str = None

    def __init__(self_, **kvargs):
        if "createdAt" in kvargs and kvargs["createdAt"] is not None:
            self_.createdAt = kvargs["createdAt"]
        if "creatorId" in kvargs and kvargs["creatorId"] is not None:
            self_.creatorId = kvargs["creatorId"]
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "full" in kvargs and kvargs["full"] is not None:
            self_.full = kvargs["full"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "itemCount" in kvargs and kvargs["itemCount"] is not None:
            self_.itemCount = kvargs["itemCount"]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == CollectionResultResponseBody.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = CollectionLinksResponseBody(**kvargs["links"])
        if "meta" in kvargs and kvargs["meta"] is not None:
            if (
                type(kvargs["meta"]).__name__
                == CollectionResultResponseBody.__annotations__["meta"]
            ):
                self_.meta = kvargs["meta"]
            else:
                self_.meta = CollectionMetaResponseBody(**kvargs["meta"])
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            self_.tenantId = kvargs["tenantId"]
        if "type" in kvargs and kvargs["type"] is not None:
            self_.type = kvargs["type"]
        if "updatedAt" in kvargs and kvargs["updatedAt"] is not None:
            self_.updatedAt = kvargs["updatedAt"]
        if "updaterId" in kvargs and kvargs["updaterId"] is not None:
            self_.updaterId = kvargs["updaterId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CollectionsLinksResponseBody:
    """

    Attributes
    ----------
    item: Link
    next: Link
    prev: Link
    self: Link
    """

    item: Link = None
    next: Link = None
    prev: Link = None
    self: Link = None

    def __init__(self_, **kvargs):
        if "item" in kvargs and kvargs["item"] is not None:
            if (
                type(kvargs["item"]).__name__
                == CollectionsLinksResponseBody.__annotations__["item"]
            ):
                self_.item = kvargs["item"]
            else:
                self_.item = Link(**kvargs["item"])
        if "next" in kvargs and kvargs["next"] is not None:
            if (
                type(kvargs["next"]).__name__
                == CollectionsLinksResponseBody.__annotations__["next"]
            ):
                self_.next = kvargs["next"]
            else:
                self_.next = Link(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if (
                type(kvargs["prev"]).__name__
                == CollectionsLinksResponseBody.__annotations__["prev"]
            ):
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Link(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if (
                type(kvargs["self"]).__name__
                == CollectionsLinksResponseBody.__annotations__["self"]
            ):
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemLinksResponseBody:
    """

    Attributes
    ----------
    collections: Link
    open: Link
    self: Link
    thumbnail: Link
    """

    collections: Link = None
    open: Link = None
    self: Link = None
    thumbnail: Link = None

    def __init__(self_, **kvargs):
        if "collections" in kvargs and kvargs["collections"] is not None:
            if (
                type(kvargs["collections"]).__name__
                == ItemLinksResponseBody.__annotations__["collections"]
            ):
                self_.collections = kvargs["collections"]
            else:
                self_.collections = Link(**kvargs["collections"])
        if "open" in kvargs and kvargs["open"] is not None:
            if (
                type(kvargs["open"]).__name__
                == ItemLinksResponseBody.__annotations__["open"]
            ):
                self_.open = kvargs["open"]
            else:
                self_.open = Link(**kvargs["open"])
        if "self" in kvargs and kvargs["self"] is not None:
            if (
                type(kvargs["self"]).__name__
                == ItemLinksResponseBody.__annotations__["self"]
            ):
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        if "thumbnail" in kvargs and kvargs["thumbnail"] is not None:
            if (
                type(kvargs["thumbnail"]).__name__
                == ItemLinksResponseBody.__annotations__["thumbnail"]
            ):
                self_.thumbnail = kvargs["thumbnail"]
            else:
                self_.thumbnail = Link(**kvargs["thumbnail"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemMetaResponseBody:
    """
    Item metadata and computed fields.

    Attributes
    ----------
    actions: list[str]
      The actions that the user can perform on the item.
    collections: list[ItemTagResponseBody]
      An array of collections that the item is part of.
    isFavorited: bool
      The flag that indicates if item is in the user's favorites collection.
    tags: list[ItemTagResponseBody]
      An array of tags that the item is part of.
    """

    actions: list[str] = None
    collections: list[ItemTagResponseBody] = None
    isFavorited: bool = None
    tags: list[ItemTagResponseBody] = None

    def __init__(self_, **kvargs):
        if "actions" in kvargs and kvargs["actions"] is not None:
            self_.actions = kvargs["actions"]
        if "collections" in kvargs and kvargs["collections"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == ItemMetaResponseBody.__annotations__["collections"]
                for e in kvargs["collections"]
            ):
                self_.collections = kvargs["collections"]
            else:
                self_.collections = [
                    ItemTagResponseBody(**e) for e in kvargs["collections"]
                ]
        if "isFavorited" in kvargs and kvargs["isFavorited"] is not None:
            self_.isFavorited = kvargs["isFavorited"]
        if "tags" in kvargs and kvargs["tags"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == ItemMetaResponseBody.__annotations__["tags"]
                for e in kvargs["tags"]
            ):
                self_.tags = kvargs["tags"]
            else:
                self_.tags = [ItemTagResponseBody(**e) for e in kvargs["tags"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemTagResponseBody:
    """
    Holds basic information about a tag or collection.

    Attributes
    ----------
    id: str
      The ID of the tag/collection.
    name: str
      The name of the tag/collection.
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
class ItemViewsResponseBody:
    """

    Attributes
    ----------
    total: int
      Total number of views the resource got during the last 28 days.
    trend: float
      Trend in views over the last 4 weeks.
    unique: int
      Number of unique users who viewed the resource during the last 28 days.
    usedBy: int
      Number of apps this dataset is used in (datasets only).
    week: list[ItemViewsWeeksResponseBody]
    """

    total: int = None
    trend: float = None
    unique: int = None
    usedBy: int = None
    week: list[ItemViewsWeeksResponseBody] = None

    def __init__(self_, **kvargs):
        if "total" in kvargs and kvargs["total"] is not None:
            self_.total = kvargs["total"]
        if "trend" in kvargs and kvargs["trend"] is not None:
            self_.trend = kvargs["trend"]
        if "unique" in kvargs and kvargs["unique"] is not None:
            self_.unique = kvargs["unique"]
        if "usedBy" in kvargs and kvargs["usedBy"] is not None:
            self_.usedBy = kvargs["usedBy"]
        if "week" in kvargs and kvargs["week"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == ItemViewsResponseBody.__annotations__["week"]
                for e in kvargs["week"]
            ):
                self_.week = kvargs["week"]
            else:
                self_.week = [ItemViewsWeeksResponseBody(**e) for e in kvargs["week"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemViewsWeeksResponseBody:
    """

    Attributes
    ----------
    start: str
      The RFC3339 datetime representing the start of the referenced week.
    total: int
      Total number of views the resource got during the referenced week.
    unique: int
      Number of unique users who viewed the resource during the referenced week.
    """

    start: str = None
    total: int = None
    unique: int = None

    def __init__(self_, **kvargs):
        if "start" in kvargs and kvargs["start"] is not None:
            self_.start = kvargs["start"]
        if "total" in kvargs and kvargs["total"] is not None:
            self_.total = kvargs["total"]
        if "unique" in kvargs and kvargs["unique"] is not None:
            self_.unique = kvargs["unique"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsLinksResponseBody:
    """

    Attributes
    ----------
    collection: Link
    next: Link
    prev: Link
    self: Link
    """

    collection: Link = None
    next: Link = None
    prev: Link = None
    self: Link = None

    def __init__(self_, **kvargs):
        if "collection" in kvargs and kvargs["collection"] is not None:
            if (
                type(kvargs["collection"]).__name__
                == ItemsLinksResponseBody.__annotations__["collection"]
            ):
                self_.collection = kvargs["collection"]
            else:
                self_.collection = Link(**kvargs["collection"])
        if "next" in kvargs and kvargs["next"] is not None:
            if (
                type(kvargs["next"]).__name__
                == ItemsLinksResponseBody.__annotations__["next"]
            ):
                self_.next = kvargs["next"]
            else:
                self_.next = Link(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if (
                type(kvargs["prev"]).__name__
                == ItemsLinksResponseBody.__annotations__["prev"]
            ):
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Link(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if (
                type(kvargs["self"]).__name__
                == ItemsLinksResponseBody.__annotations__["self"]
            ):
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsResourceSizeResponseBody:
    """

    Attributes
    ----------
    appFile: float
      Size of the app on disk in bytes.
    appMemory: float
      Size of the app in memory in bytes.
    """

    appFile: float = None
    appMemory: float = None

    def __init__(self_, **kvargs):
        if "appFile" in kvargs and kvargs["appFile"] is not None:
            self_.appFile = kvargs["appFile"]
        if "appMemory" in kvargs and kvargs["appMemory"] is not None:
            self_.appMemory = kvargs["appMemory"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsResultResponseBody:
    """
    Multiple items.

    Attributes
    ----------
    data: list[ItemResultResponseBody]
    links: ItemsLinksResponseBody
    """

    data: list[ItemResultResponseBody] = None
    links: ItemsLinksResponseBody = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]"
                == ItemsResultResponseBody.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [ItemResultResponseBody(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == ItemsResultResponseBody.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = ItemsLinksResponseBody(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Items:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_settings(self) -> ItemsSettingsResponseBody:
        """
        Returns tenant specific settings.
        Finds and returns the settings for the current tenant.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/items/settings",
            method="GET",
            params={},
            data=None,
        )
        obj = ItemsSettingsResponseBody(**response.json())
        obj.auth = self.auth
        return obj

    def patch_settings(self, data: ItemsSettingsPatch) -> ItemsSettingsResponseBody:
        """
        Patches tenant specific settings.
        Updates the settings provided in the patch body.

        Parameters
        ----------
        data: ItemsSettingsPatch
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/items/settings",
            method="PATCH",
            params={},
            data=data,
        )
        obj = ItemsSettingsResponseBody(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, itemId: str) -> ItemResultResponseBody:
        """
        Returns an item.
        Finds and returns an item.

        Parameters
        ----------
        itemId: str
          The item's unique identifier
        """
        response = self.auth.rest(
            path="/items/{itemId}".replace("{itemId}", itemId),
            method="GET",
            params={},
            data=None,
        )
        obj = ItemResultResponseBody(**response.json())
        obj.auth = self.auth
        return obj

    def get_items(
        self,
        collectionId: str = None,
        createdByUserId: str = None,
        id: str = None,
        limit: int = None,
        name: str = None,
        next: str = None,
        notCreatedByUserId: str = None,
        notOwnerId: str = None,
        ownerId: str = None,
        prev: str = None,
        query: str = None,
        resourceId: str = None,
        resourceIds: str = None,
        resourceLink: str = None,
        resourceSubType: str = None,
        resourceType: Literal[
            "app",
            "collection",
            "qlikview",
            "insight",
            "qvapp",
            "genericlink",
            "sharingservicetask",
            "note",
            "dataasset",
            "dataset",
            "automation",
            "automl-experiment",
            "automl-deployment",
        ] = None,
        shared: bool = None,
        sort: Literal[
            "+createdAt", "-createdAt", "+name", "-name", "+updatedAt", "-updatedAt"
        ] = None,
        spaceId: str = None,
        noActions: bool = False,
    ) -> ListableResource[ItemResultResponseBody]:
        """
        Retrieves items that the user has access to.
        Finds and returns items that the user has access to.

        Parameters
        ----------
        collectionId: str = None
          The collection's unique identifier.
        createdByUserId: str = None
          User's unique identifier.
        id: str = None
          The item's unique identifier.
        limit: int = None
          The maximum number of resources to return for a request. The limit must be an integer between 1 and 100 (inclusive).
        name: str = None
          The case-insensitive string used to search for a resource by name.
        next: str = None
          The cursor to the next page of resources. Provide either the next or prev cursor, but not both.
        notCreatedByUserId: str = None
          User's unique identifier.
        notOwnerId: str = None
          Owner identifier.
        ownerId: str = None
          Owner identifier.
        prev: str = None
          The cursor to the previous page of resources. Provide either the next or prev cursor, but not both.
        query: str = None
          The case-insensitive string used to search for a resource by name or description.
        resourceId: str = None
          The case-sensitive string used to search for an item by resourceId. If resourceId is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
        resourceIds: str = None
          The case-sensitive strings used to search for an item by resourceIds. The maximum number of resourceIds it supports is 100. If resourceIds is provided, then resourceType must be provided. For example '?resourceIds=appId1,appId2'
        resourceLink: str = None
          The case-sensitive string used to search for an item by resourceLink. If resourceLink is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
        resourceSubType: str = None
          the case-sensitive string used to filter items by resourceSubType(s). For example '?resourceSubType=chart-monitoring,qix-df,qvd'
        resourceType: Literal["app", "collection", "qlikview", "insight", "qvapp", "genericlink", "sharingservicetask", "note", "dataasset", "dataset", "automation", "automl-experiment", "automl-deployment"] = None
          The case-sensitive string used to filter items by resourceType(s). For example '?resourceType=app,qvapp'
        shared: bool = None
          Whether or not to return items in a shared space.
        sort: Literal["+createdAt", "-createdAt", "+name", "-name", "+updatedAt", "-updatedAt"] = None
          The property of a resource to sort on (default sort is +createdAt). The supported properties are createdAt, updatedAt, and name. A property must be prefixed by + or   - to indicate ascending or descending sort order respectively.
        spaceId: str = None
          The space's unique identifier (supports \'personal\' as spaceId).
        noActions: bool = False
          If set to true, the user's available actions for each item will not be evaluated meaning the actions-array will be omitted from the response (reduces response time).
        """
        query_params = {}
        if collectionId is not None:
            query_params["collectionId"] = collectionId
        if createdByUserId is not None:
            query_params["createdByUserId"] = createdByUserId
        if id is not None:
            query_params["id"] = id
        if limit is not None:
            query_params["limit"] = limit
        if name is not None:
            query_params["name"] = name
        if next is not None:
            query_params["next"] = next
        if notCreatedByUserId is not None:
            query_params["notCreatedByUserId"] = notCreatedByUserId
        if notOwnerId is not None:
            query_params["notOwnerId"] = notOwnerId
        if ownerId is not None:
            query_params["ownerId"] = ownerId
        if prev is not None:
            query_params["prev"] = prev
        if query is not None:
            query_params["query"] = query
        if resourceId is not None:
            query_params["resourceId"] = resourceId
        if resourceIds is not None:
            query_params["resourceIds"] = resourceIds
        if resourceLink is not None:
            query_params["resourceLink"] = resourceLink
        if resourceSubType is not None:
            query_params["resourceSubType"] = resourceSubType
        if resourceType is not None:
            query_params["resourceType"] = resourceType
        if shared is not None:
            query_params["shared"] = shared
        if sort is not None:
            query_params["sort"] = sort
        if spaceId is not None:
            query_params["spaceId"] = spaceId
        if noActions is not None:
            query_params["noActions"] = noActions
        response = self.auth.rest(
            path="/items",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=ItemResultResponseBody,
            auth=self.auth,
            path="/items",
            query_params=query_params,
        )
