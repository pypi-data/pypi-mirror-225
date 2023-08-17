# This is spectacularly generated code by spectacular based on
# Qlik Cloud Services APIs

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class CSPEntry:
    """

    Attributes
    ----------
    id: str
      The CSP entry's unique identifier.
    childSrc: bool
      Defines the valid sources for loading web workers and nested browsing contexts using elements such as frame and iFrame.
    connectSrc: bool
      Restricts the URLs that can be loaded using script interfaces.
    connectSrcWSS: bool
      Restricts the URLs that can be connected to websockets (all sources will be prefixed with 'wss://').
    createdDate: str
      The UTC timestamp when the CSP entry was created.
    description: str
      The reason for adding this origin to the Content Security Policy.
    fontSrc: bool
      Specifies valid sources for loading fonts.
    formAction: bool
      Allow forms to be submitted to the origin.
    frameAncestors: bool
      Specifies valid sources for embedding the resource using frame, iFrame, object, embed and applet.
    frameSrc: bool
      Specifies valid sources for loading nested browsing contexts using elements such as frame and iFrame.
    imgSrc: bool
      Specifies valid sources of images and favicons.
    mediaSrc: bool
      Specifies valid sources for loading media using the audio and video elements.
    modifiedDate: str
      The UTC timestamp when the CSP entry was last modified.
    name: str
      The name for this entry.
    objectSrc: bool
      Specifies valid sources for the object, embed, and applet elements.
    origin: str
      The origin that the CSP directives should be applied to.
    scriptSrc: bool
      Specifies valid sources for JavaScript.
    styleSrc: bool
      Specifies valid sources for stylesheets.
    workerSrc: bool
      Specifies valid sources for Worker, SharedWorker, or ServiceWorker scripts.
    """

    id: str = None
    childSrc: bool = None
    connectSrc: bool = None
    connectSrcWSS: bool = None
    createdDate: str = None
    description: str = None
    fontSrc: bool = None
    formAction: bool = None
    frameAncestors: bool = None
    frameSrc: bool = None
    imgSrc: bool = None
    mediaSrc: bool = None
    modifiedDate: str = None
    name: str = None
    objectSrc: bool = None
    origin: str = None
    scriptSrc: bool = None
    styleSrc: bool = None
    workerSrc: bool = None

    def __init__(self_, **kvargs):
        if "id" in kvargs and kvargs["id"] is not None:
            self_.id = kvargs["id"]
        if "childSrc" in kvargs and kvargs["childSrc"] is not None:
            self_.childSrc = kvargs["childSrc"]
        if "connectSrc" in kvargs and kvargs["connectSrc"] is not None:
            self_.connectSrc = kvargs["connectSrc"]
        if "connectSrcWSS" in kvargs and kvargs["connectSrcWSS"] is not None:
            self_.connectSrcWSS = kvargs["connectSrcWSS"]
        if "createdDate" in kvargs and kvargs["createdDate"] is not None:
            self_.createdDate = kvargs["createdDate"]
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "fontSrc" in kvargs and kvargs["fontSrc"] is not None:
            self_.fontSrc = kvargs["fontSrc"]
        if "formAction" in kvargs and kvargs["formAction"] is not None:
            self_.formAction = kvargs["formAction"]
        if "frameAncestors" in kvargs and kvargs["frameAncestors"] is not None:
            self_.frameAncestors = kvargs["frameAncestors"]
        if "frameSrc" in kvargs and kvargs["frameSrc"] is not None:
            self_.frameSrc = kvargs["frameSrc"]
        if "imgSrc" in kvargs and kvargs["imgSrc"] is not None:
            self_.imgSrc = kvargs["imgSrc"]
        if "mediaSrc" in kvargs and kvargs["mediaSrc"] is not None:
            self_.mediaSrc = kvargs["mediaSrc"]
        if "modifiedDate" in kvargs and kvargs["modifiedDate"] is not None:
            self_.modifiedDate = kvargs["modifiedDate"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "objectSrc" in kvargs and kvargs["objectSrc"] is not None:
            self_.objectSrc = kvargs["objectSrc"]
        if "origin" in kvargs and kvargs["origin"] is not None:
            self_.origin = kvargs["origin"]
        if "scriptSrc" in kvargs and kvargs["scriptSrc"] is not None:
            self_.scriptSrc = kvargs["scriptSrc"]
        if "styleSrc" in kvargs and kvargs["styleSrc"] is not None:
            self_.styleSrc = kvargs["styleSrc"]
        if "workerSrc" in kvargs and kvargs["workerSrc"] is not None:
            self_.workerSrc = kvargs["workerSrc"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def delete(self) -> None:
        """
        Deletes a specific CSP entry

        Parameters
        ----------
        """
        self.auth.rest(
            path="/csp-origins/{id}".replace("{id}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def set(self, data: CSPEntryContent) -> CSPEntry:
        """
        Updates a CSP entry

        Parameters
        ----------
        data: CSPEntryContent
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/csp-origins/{id}".replace("{id}", self.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self


@dataclass
class CSPEntryContent:
    """

    Attributes
    ----------
    childSrc: bool
      Defines the valid sources for loading web workers and nested browsing contexts using elements such as frame and iFrame.
    connectSrc: bool
      Restricts the URLs that can be loaded using script interfaces.
    connectSrcWSS: bool
      Restricts the URLs that can be connected to websockets (all sources will be prefixed with 'wss://').
    createdDate: str
      The UTC timestamp when the CSP entry was created.
    description: str
      The reason for adding this origin to the Content Security Policy.
    fontSrc: bool
      Specifies valid sources for loading fonts.
    formAction: bool
      Allow forms to be submitted to the origin.
    frameAncestors: bool
      Specifies valid sources for embedding the resource using frame, iFrame, object, embed and applet.
    frameSrc: bool
      Specifies valid sources for loading nested browsing contexts using elements such as frame and iFrame.
    imgSrc: bool
      Specifies valid sources of images and favicons.
    mediaSrc: bool
      Specifies valid sources for loading media using the audio and video elements.
    modifiedDate: str
      The UTC timestamp when the CSP entry was last modified.
    name: str
      The name for this entry.
    objectSrc: bool
      Specifies valid sources for the object, embed, and applet elements.
    origin: str
      The origin that the CSP directives should be applied to.
    scriptSrc: bool
      Specifies valid sources for JavaScript.
    styleSrc: bool
      Specifies valid sources for stylesheets.
    workerSrc: bool
      Specifies valid sources for Worker, SharedWorker, or ServiceWorker scripts.
    """

    childSrc: bool = None
    connectSrc: bool = None
    connectSrcWSS: bool = None
    createdDate: str = None
    description: str = None
    fontSrc: bool = None
    formAction: bool = None
    frameAncestors: bool = None
    frameSrc: bool = None
    imgSrc: bool = None
    mediaSrc: bool = None
    modifiedDate: str = None
    name: str = None
    objectSrc: bool = None
    origin: str = None
    scriptSrc: bool = None
    styleSrc: bool = None
    workerSrc: bool = None

    def __init__(self_, **kvargs):
        if "childSrc" in kvargs and kvargs["childSrc"] is not None:
            self_.childSrc = kvargs["childSrc"]
        if "connectSrc" in kvargs and kvargs["connectSrc"] is not None:
            self_.connectSrc = kvargs["connectSrc"]
        if "connectSrcWSS" in kvargs and kvargs["connectSrcWSS"] is not None:
            self_.connectSrcWSS = kvargs["connectSrcWSS"]
        if "createdDate" in kvargs and kvargs["createdDate"] is not None:
            self_.createdDate = kvargs["createdDate"]
        if "description" in kvargs and kvargs["description"] is not None:
            self_.description = kvargs["description"]
        if "fontSrc" in kvargs and kvargs["fontSrc"] is not None:
            self_.fontSrc = kvargs["fontSrc"]
        if "formAction" in kvargs and kvargs["formAction"] is not None:
            self_.formAction = kvargs["formAction"]
        if "frameAncestors" in kvargs and kvargs["frameAncestors"] is not None:
            self_.frameAncestors = kvargs["frameAncestors"]
        if "frameSrc" in kvargs and kvargs["frameSrc"] is not None:
            self_.frameSrc = kvargs["frameSrc"]
        if "imgSrc" in kvargs and kvargs["imgSrc"] is not None:
            self_.imgSrc = kvargs["imgSrc"]
        if "mediaSrc" in kvargs and kvargs["mediaSrc"] is not None:
            self_.mediaSrc = kvargs["mediaSrc"]
        if "modifiedDate" in kvargs and kvargs["modifiedDate"] is not None:
            self_.modifiedDate = kvargs["modifiedDate"]
        if "name" in kvargs and kvargs["name"] is not None:
            self_.name = kvargs["name"]
        if "objectSrc" in kvargs and kvargs["objectSrc"] is not None:
            self_.objectSrc = kvargs["objectSrc"]
        if "origin" in kvargs and kvargs["origin"] is not None:
            self_.origin = kvargs["origin"]
        if "scriptSrc" in kvargs and kvargs["scriptSrc"] is not None:
            self_.scriptSrc = kvargs["scriptSrc"]
        if "styleSrc" in kvargs and kvargs["styleSrc"] is not None:
            self_.styleSrc = kvargs["styleSrc"]
        if "workerSrc" in kvargs and kvargs["workerSrc"] is not None:
            self_.workerSrc = kvargs["workerSrc"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CSPEntryList:
    """

    Attributes
    ----------
    data: list[CSPEntry]
    links: CSPEntryListLinks
    """

    data: list[CSPEntry] = None
    links: CSPEntryListLinks = None

    def __init__(self_, **kvargs):
        if "data" in kvargs and kvargs["data"] is not None:
            if all(
                f"list[{type(e).__name__}]" == CSPEntryList.__annotations__["data"]
                for e in kvargs["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [CSPEntry(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == CSPEntryList.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = CSPEntryListLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CSPEntryListLinks:
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
                == CSPEntryListLinks.__annotations__["next"]
            ):
                self_.next = kvargs["next"]
            else:
                self_.next = Link(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if (
                type(kvargs["prev"]).__name__
                == CSPEntryListLinks.__annotations__["prev"]
            ):
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Link(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if (
                type(kvargs["self"]).__name__
                == CSPEntryListLinks.__annotations__["self"]
            ):
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CSPHeader:
    """

    Attributes
    ----------
    Content_Security_Policy: str
      The compiled CSP header.
    """

    Content_Security_Policy: str = None

    def __init__(self_, **kvargs):
        if (
            "Content-Security-Policy" in kvargs
            and kvargs["Content-Security-Policy"] is not None
        ):
            self_.Content_Security_Policy = kvargs["Content-Security-Policy"]
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
      URL to a resource request.
    """

    href: str = None

    def __init__(self_, **kvargs):
        if "href" in kvargs and kvargs["href"] is not None:
            self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class CspOrigins:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def generate_header(self) -> CSPHeader:
        """
        Retrieves the CSP header for a tenant

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/csp-origins/actions/generate-header",
            method="GET",
            params={},
            data=None,
        )
        obj = CSPHeader(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, id: str) -> CSPEntry:
        """
        Returns details for a specific CSP entry

        Parameters
        ----------
        id: str
          The CSP entry's unique identifier.
        """
        response = self.auth.rest(
            path="/csp-origins/{id}".replace("{id}", id),
            method="GET",
            params={},
            data=None,
        )
        obj = CSPEntry(**response.json())
        obj.auth = self.auth
        return obj

    def get_csp_origins(
        self,
        childSrc: bool = None,
        connectSrc: bool = None,
        connectSrcWSS: bool = None,
        fontSrc: bool = None,
        formAction: bool = None,
        frameAncestors: bool = None,
        frameSrc: bool = None,
        imgSrc: bool = None,
        limit: float = 20,
        mediaSrc: bool = None,
        name: str = None,
        next: str = None,
        objectSrc: bool = None,
        origin: str = None,
        prev: str = None,
        scriptSrc: bool = None,
        sort: Literal[
            "name",
            "-name",
            "origin",
            "-origin",
            "createdDate",
            "-createdDate",
            "modifiedDate",
            "-modifiedDate",
        ] = None,
        styleSrc: bool = None,
        workerSrc: bool = None,
    ) -> ListableResource[CSPEntry]:
        """
        Retrieves all CSP entries for a tenant

        Parameters
        ----------
        childSrc: bool = None
          Filter resources by directive 'childSrc', true/false.
        connectSrc: bool = None
          Filter resources by directive 'connectSrc', true/false.
        connectSrcWSS: bool = None
          Filter resources by directive 'connectSrcWSS', true/false.
        fontSrc: bool = None
          Filter resources by directive 'fontSrc', true/false.
        formAction: bool = None
          Filter resources by directive 'formAction', true/false.
        frameAncestors: bool = None
          Filter resources by directive 'frameAncestors', true/false.
        frameSrc: bool = None
          Filter resources by directive 'frameSrc', true/false.
        imgSrc: bool = None
          Filter resources by directive 'imgSrc', true/false.
        limit: float = 20
          Maximum number of CSP-Origins to retrieve.
        mediaSrc: bool = None
          Filter resources by directive 'mediaSrc', true/false.
        name: str = None
          Filter resources by name (wildcard and case insensitive).
        next: str = None
          Cursor to the next page.
        objectSrc: bool = None
          Filter resources by directive 'objectSrc', true/false.
        origin: str = None
          Filter resources by origin (wildcard and case insensitive).
        prev: str = None
          Cursor to previous next page.
        scriptSrc: bool = None
          Filter resources by directive 'scriptSrc', true/false.
        sort: Literal["name", "-name", "origin", "-origin", "createdDate", "-createdDate", "modifiedDate", "-modifiedDate"] = None
          Field to sort by, prefix with -/+ to indicate order.
        styleSrc: bool = None
          Filter resources by directive 'styleSrc', true/false.
        workerSrc: bool = None
          Filter resources by directive 'workerSrc', true/false.
        """
        query_params = {}
        if childSrc is not None:
            query_params["childSrc"] = childSrc
        if connectSrc is not None:
            query_params["connectSrc"] = connectSrc
        if connectSrcWSS is not None:
            query_params["connectSrcWSS"] = connectSrcWSS
        if fontSrc is not None:
            query_params["fontSrc"] = fontSrc
        if formAction is not None:
            query_params["formAction"] = formAction
        if frameAncestors is not None:
            query_params["frameAncestors"] = frameAncestors
        if frameSrc is not None:
            query_params["frameSrc"] = frameSrc
        if imgSrc is not None:
            query_params["imgSrc"] = imgSrc
        if limit is not None:
            query_params["limit"] = limit
        if mediaSrc is not None:
            query_params["mediaSrc"] = mediaSrc
        if name is not None:
            query_params["name"] = name
        if next is not None:
            query_params["next"] = next
        if objectSrc is not None:
            query_params["objectSrc"] = objectSrc
        if origin is not None:
            query_params["origin"] = origin
        if prev is not None:
            query_params["prev"] = prev
        if scriptSrc is not None:
            query_params["scriptSrc"] = scriptSrc
        if sort is not None:
            query_params["sort"] = sort
        if styleSrc is not None:
            query_params["styleSrc"] = styleSrc
        if workerSrc is not None:
            query_params["workerSrc"] = workerSrc
        response = self.auth.rest(
            path="/csp-origins",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=CSPEntry,
            auth=self.auth,
            path="/csp-origins",
            query_params=query_params,
        )

    def create(self, data: CSPEntryContent) -> CSPEntry:
        """
        Creates a new CSP entry

        Parameters
        ----------
        data: CSPEntryContent
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/csp-origins",
            method="POST",
            params={},
            data=data,
        )
        obj = CSPEntry(**response.json())
        obj.auth = self.auth
        return obj
