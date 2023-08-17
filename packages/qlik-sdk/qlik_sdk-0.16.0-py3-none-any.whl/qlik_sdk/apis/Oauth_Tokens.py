# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class Link:
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
class OauthToken:
    """

    Attributes
    ----------
    description: str
      The description of the token.
    deviceType: str
      The type of the user device the authorization token is generated for (Tablet, Phone etc.).
    id: str
      The token ID.
    lastUsed: str
      The last time the token was used.
    tenantId: str
      The ID of the owning tenant.
    userId: str
      The ID of the owning user.
    """

    description: str = None
    deviceType: str = None
    id: str = None
    lastUsed: str = None
    tenantId: str = None
    userId: str = None

    def __init__(self_, **kvargs):
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "deviceType" in kvargs and kvargs["deviceType"] is not None:
            self_.deviceType = kvargs["deviceType"]
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "lastUsed" in kvargs and kvargs["lastUsed"] is not None:
            self_.lastUsed = kvargs["lastUsed"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            self_.tenantId = kvargs["tenantId"]
        if "userId" in kvargs and kvargs["userId"] is not None:
            self_.userId = kvargs["userId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class OauthTokenPage:
    """

    Attributes
    ----------
    data: list[OauthToken]
    links: OauthTokenPageLinks
    """

    data: list[OauthToken] = None
    links: OauthTokenPageLinks = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]" == OauthTokenPage.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [OauthToken(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == OauthTokenPage.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = OauthTokenPageLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class OauthTokenPageLinks:
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
            if (
                type(kvargs["next"]).__name__
                == OauthTokenPageLinks.__annotations__["next"]
            ):
                self_.next = kvargs["next"]
            else:
                self_.next = Link(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if (
                type(kvargs["prev"]).__name__
                == OauthTokenPageLinks.__annotations__["prev"]
            ):
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Link(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if (
                type(kvargs["self"]).__name__
                == OauthTokenPageLinks.__annotations__["self"]
            ):
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class OauthTokens:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def delete(self, tokenId: str) -> None:
        """
        Revoke an OAuth token by ID

        Parameters
        ----------
        tokenId: str
          The ID of the token to revoke.
        """
        self.auth.rest(
            path="/oauth-tokens/{tokenId}".replace("{tokenId}", tokenId),
            method="DELETE",
            params={},
            data=None,
        )

    def get_oauth_tokens(
        self,
        limit: float = None,
        page: str = None,
        sort: Literal["userId"] = "userId",
        userId: str = None,
    ) -> ListableResource[OauthToken]:
        """
        List OAuth tokens

        Parameters
        ----------
        limit: float = None
          The maximum number of tokens to return.
        page: str = None
          The target page.
        sort: Literal["userId"] = "userId"
          The field to sort by.
        userId: str = None
          The ID of the user to limit results to.
        """
        query_params = {}
        if limit is not None:
            query_params["limit"] = limit
        if page is not None:
            query_params["page"] = page
        if sort is not None:
            query_params["sort"] = sort
        if userId is not None:
            query_params["userId"] = userId
        response = self.auth.rest(
            path="/oauth-tokens",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=OauthToken,
            auth=self.auth,
            path="/oauth-tokens",
            query_params=query_params,
        )
