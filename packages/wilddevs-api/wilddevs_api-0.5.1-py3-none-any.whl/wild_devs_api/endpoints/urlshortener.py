from __future__ import annotations

__all__ = [
    "UrlShortener",
]

import typing as t

from wild_devs_api.restclient import RESTClient
from wild_devs_api.models.response import APIResponse


class UrlShortener:
    """
    The endpoint class for urlshortener related endpoints.
    Contains sync and async variants of the endpoint methods.
    """

    _rest: RESTClient

    def __init__(self, rest: RESTClient) -> None:
        self._rest = rest

    @property
    def rest(self) -> RESTClient:
        return self._rest

    # Synchronous Methods

    def url_shortener(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send a synchronous POST request to https://api.wild-devs.net/v1/urlshortener.

        Args: payload (`Optional`[`dict`[`str`, `Any`]]): The payload to send to the endpoint. Keyword Args:
        return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the `APIResponse`. Default is
        `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if not payload:
            payload = self.rest.build_payload(kwargs)
        return self.rest.post(
            "urlshortener", payload, return_headers=return_headers, xml=xml
        )

    def url_shorteners(
        self, *, return_headers: bool = False, xml: bool = False
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/urlshorteners.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self.rest.get("urlshorteners", return_headers=return_headers, xml=xml)

    def delete_url_shortener(
        self, url: str, *, return_headers: bool = False
    ) -> APIResponse:
        """
        Method to send a synchronous DELETE request to https://api.wild-devs.net/v1/urlshortener{id}.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self.rest.delete(f"urlshortener/{url}", return_headers=return_headers)

    # Asynchronous Methods

    async def async_url_shortener(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send an asynchronous POST request to https://api.wild-devs.net/v1/urlshortener.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if not payload:
            payload = self.rest.build_payload(kwargs)
        return await self.rest.async_post(
            "urlshortener",
            payload,
            return_headers=return_headers, xml=xml
        )

    async def async_url_shorteners(
        self, *, return_headers: bool = False, xml: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/urlshorteners.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return await self.rest.async_get("urlshorteners", return_headers=return_headers, xml=xml)

    async def async_delete_url_shortener(
        self, url: str, *, return_headers: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous DELETE request to https://api.wild-devs.net/v1/urlshortener{id}.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return await self.rest.async_delete(
            f"urlshortener/{url}", return_headers=return_headers
        )
