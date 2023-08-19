from __future__ import annotations

__all__ = [
    "AI",
]

import typing as t

from wild_devs_api.restclient import RESTClient
from wild_devs_api.models.response import APIResponse


class AI:
    """
    The endpoint class for AI related endpoints.
    Contains sync and async variants of the endpoint methods.
    """

    _rest: RESTClient

    def __init__(self, rest: RESTClient) -> None:
        self._rest = rest

    @property
    def rest(self) -> RESTClient:
        return self._rest

    # Synchronous Methods

    def dictionary(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send a synchronous POST request to https://api.wild-devs.net/v1/dictionary.

        Args:
            payload (Optional`dict`[`str`, `Any`]): The payload to send to the endpoint.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`. **kwargs (`Any`): The additional kwargs that have to be passed if payload
        is `None`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if not payload:
            payload = self.rest.build_payload(kwargs)
        return self.rest.post(
            f"dictionary", payload, return_headers=return_headers, xml=xml
        )

    def synonyms(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send a synchronous POST request to https://api.wild-devs.net/v1/synonyms.

        Args:
            payload (Optional`dict`[`str`, `Any`]): The payload to send to the endpoint.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`. **kwargs (`Any`): The additional kwargs that have to be passed if payload
        is `None`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if not payload:
            payload = self.rest.build_payload(kwargs)
        return self.rest.post(
            "synonyms", payload, return_headers=return_headers, xml=xml
        )

    # Asynchronous Methods

    async def async_dictionary(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send an asynchronous POST request to https://api.wild-devs.net/v1/dictionary.

        Args:
            payload (Optional`dict`[`str`, `Any`]): The payload to send to the endpoint.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`. **kwargs (`Any`): The additional kwargs that have to be passed if payload
        is `None`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if not payload:
            payload = self.rest.build_payload(kwargs)
        return await self.rest.async_post(
            "dictionary", payload, return_headers=return_headers, xml=xml
        )

    async def async_synonyms(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send an asynchronous POST request to https://api.wild-devs.net/v1/synonyms.

        Args:
            payload (Optional`dict`[`str`, `Any`]): The payload to send to the endpoint.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`. **kwargs (`Any`): The additional kwargs that have to be passed if payload
        is `None`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if not payload:
            payload = self.rest.build_payload(kwargs)
        return await self.rest.async_post(
            "synonyms", payload, return_headers=return_headers, xml=xml
        )
