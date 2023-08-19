from __future__ import annotations

__all__ = [
    "Games",
]

from wild_devs_api.restclient import RESTClient
from wild_devs_api.models.response import APIResponse


class Games:
    """
    The endpoint class for game related endpoints.
    Contains sync and async variants of the endpoint methods.
    """

    _rest: RESTClient

    def __init__(self, rest: RESTClient) -> None:
        self._rest = rest

    @property
    def rest(self) -> RESTClient:
        return self._rest

    # Synchronous Methods

    def free_epicgames(
        self,
        *,
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/epicgames/free.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`. **kwargs (`Any`): The additional kwargs that have to be passed if payload
        is `None`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self.rest.get("epicgames/free", return_headers=return_headers, xml=xml)

    # Asynchronous Methods

    async def async_free_epicgames(
        self, *, return_headers: bool = False, xml: bool = False,
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/epicgames/free.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`. **kwargs (`Any`): The additional kwargs that have to be passed if payload
        is `None`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return await self.rest.async_get(
            "epicgames/free", return_headers=return_headers, xml=xml
        )
