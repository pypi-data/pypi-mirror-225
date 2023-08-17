from typing import Iterator, List, TypeVar
from urllib.parse import parse_qs, urlparse

from .auth import Auth

T = TypeVar("T")


def get_pagination_query_param(response: any):
    url_str: str = None
    try:
        url_str = response["links"]["next"]["href"]
    except:
        pass
    if not url_str:
        return False
    # should be "next" but for users it is "startingAfter"
    query_dict = parse_qs(urlparse(url_str).query)
    for k in ["next", "startingAfter"]:
        if k in query_dict:
            return k, query_dict[k][0]
    return False


class ListableResource(List[T]):
    pagination: Iterator[T]
    """
    Automatic paginating iterator for resources that supports it
    It handles fetching automatically the next set of data from the list

    Example:
    --------
    >>> items = Items(config).get_items()
    ... for item in items.pagination:
    ...     print_item(item)
    """

    def __init__(
        self,
        response,
        auth: Auth,
        cls=None,
        path="",
        method="GET",
        query_params={},
    ):
        has_data_response = isinstance(response, dict) and "data" in response
        is_paginated = has_data_response and "links" in response

        def create(objData: any):
            if cls is None:
                return objData
            obj = cls(**objData)
            obj.auth = auth
            return obj

        list.__init__(
            self,
            [
                create(elem)
                for elem in (response["data"] if has_data_response else response)
            ],
        )

        def gen():
            # Yield the elements from the first response
            for elem in self:
                yield elem

            # Make pagination requests if possible
            if is_paginated:
                pagination_params = query_params.copy()
                # use max limit to get the most elements per request
                pagination_params["limit"] = 100
                last_response = response
                done = False
                while not done:
                    pagination_query_param = get_pagination_query_param(
                        response=last_response
                    )
                    if pagination_query_param:
                        query_key, query_value = pagination_query_param
                        pagination_params[query_key] = query_value
                    else:
                        done = True
                    if not done:
                        raw_response = auth.rest(
                            method=method,
                            path=path,
                            data=None,
                            params=pagination_params,
                        )
                        last_response = raw_response.json()
                        for elem_data in last_response["data"]:
                            obj = create(elem_data)
                            # add the element to the list to make it accessible after the pagination too
                            self.append(obj)
                            yield obj

        self.pagination = gen()
