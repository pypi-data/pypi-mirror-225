from __future__ import annotations

__all__ = [
    "Random",
]

import typing as t

from wild_devs_api.restclient import RESTClient
from wild_devs_api.models.response import APIResponse


class Random:
    """
    The endpoint class for random related endpoints.
    Contains sync and async variants of the endpoint methods.
    """

    _rest: RESTClient

    def __init__(self, rest: RESTClient) -> None:
        self._rest = rest

    @property
    def rest(self) -> RESTClient:
        return self._rest

    # Synchronous Methods

    def affirmation(
        self,
        *,
        tag: str,
        limit: int = 1,
        offset: int = 1,
        random: bool = True,
        return_headers: bool = False,
        xml: bool = False
                    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/affirmation.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        query_string = f"?limit={limit}&offset={offset}"
        if random:
            query_string += "&random"
        if tag:
            query_string += "&tag"
        return self.rest.get(f"affirmation{query_string}", return_headers=return_headers, xml=xml)

    def poem(
        self,
        *,
        limit: int = 1,
        offset: int = 1,
        random: bool = True,
        return_headers: bool = False,
        xml: bool = False
                    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/poem.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        query_string = f"?limit={limit}&offset={offset}"
        if random:
            query_string += "&random"
        return self.rest.get(f"poem{query_string}", return_headers=return_headers, xml=xml)

    def quote(
        self,
        *,
        limit: int = 1,
        offset: int = 1,
        random: bool = True,
        return_headers: bool = False,
        xml: bool = False
                    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/quote.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        query_string = f"?limit={limit}&offset={offset}"
        if random:
            query_string += "&random"
        return self.rest.get(f"quote{query_string}", return_headers=return_headers, xml=xml)

    def string(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send a synchronous POST request to https://api.wild-devs.net/v1/string.

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
        return self.rest.post("string", payload, return_headers=return_headers, xml=xml)

    def number(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send a synchronous POST request to https://api.wild-devs.net/v1/number.

        Args:
            payload (Optional`dict`[`str`, `Any`]): The payload to send to the endpoint.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.
        **kwargs (`Any`): The additional kwargs that have to be passed if payload
        is `None`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if not payload:
            payload = self.rest.build_payload(kwargs)
        return self.rest.post("number", payload, return_headers=return_headers, xml=xml)

    def joke(self, *, return_headers: bool = False, xml: bool = False) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/joke.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self.rest.get("joke", return_headers=return_headers, xml=xml)

    # Asynchronous Methods

    async def async_affirmation(
            self,
            *,
            tag: str,
            limit: int = 1,
            offset: int = 1,
            random: bool = True,
            return_headers: bool = False,
            xml: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/affirmation.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        query_string = f"?limit={limit}&offset={offset}"
        if random:
            query_string += "&random"
        if tag:
            query_string += "&tag"
        return await self.rest.async_get(f"affirmation{query_string}", return_headers=return_headers, xml=xml)

    async def async_poem(
            self,
            *,
            limit: int = 1,
            offset: int = 1,
            random: bool = True,
            return_headers: bool = False,
            xml: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/poem.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        query_string = f"?limit={limit}&offset={offset}"
        if random:
            query_string += "&random"
        return await self.rest.async_get(f"poem{query_string}", return_headers=return_headers, xml=xml)

    async def async_quote(
            self,
            *,
            limit: int = 1,
            offset: int = 1,
            random: bool = True,
            return_headers: bool = False,
            xml: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/quote.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        query_string = f"?limit={limit}&offset={offset}"
        if random:
            query_string += "&random"
        return await self.rest.async_get(f"quote{query_string}", return_headers=return_headers, xml=xml)

    async def async_string(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send an asynchronous POST request to https://api.wild-devs.net/v1/string.

        Args:
            payload (Optional`dict`[`str`, `Any`]): The payload to send to the endpoint.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.
        **kwargs (`Any`): The additional kwargs that have to be passed if payload
        is `None`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if not payload:
            payload = self.rest.build_payload(kwargs)
        return await self.rest.async_post(
            "string", payload, return_headers=return_headers, xml=xml
        )

    async def async_number(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send an asynchronous POST request to https://api.wild-devs.net/v1/number.

        Args:
            payload (Optional`dict`[`str`, `Any`]): The payload to send to the endpoint.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.
        **kwargs (`Any`): The additional kwargs that have to be passed if payload
        is `None`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if not payload:
            payload = self.rest.build_payload(kwargs)
        return await self.rest.async_post(
            "number", payload, return_headers=return_headers, xml=xml
        )

    async def async_joke(self, *, return_headers: bool = False, xml: bool = False) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/joke.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return await self.rest.async_get("joke", return_headers=return_headers, xml=xml)
