from __future__ import annotations

__all__ = [
    "MovieFinder",
]

import typing as t

from wild_devs_api.restclient import RESTClient
from wild_devs_api.models.response import APIResponse


class MovieFinder:
    """
    The endpoint class for moviefinder related endpoints.
    Contains sync and async variants of the endpoint methods.
    """

    _rest: RESTClient

    def __init__(self, rest: RESTClient) -> None:
        self._rest = rest

    @property
    def rest(self) -> RESTClient:
        return self._rest

    # Synchronous Methods

    def moviefinder(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send a synchronous POST request to https://api.wild-devs.net/v1/moviefinder.

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
            "moviefinder", payload, return_headers=return_headers, xml=xml
        )

    def moviefinder_locales(
        self,
        *,
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/moviefinder/locales.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the

        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self.rest.get(
            "moviefinder/locales", return_headers=return_headers, xml=xml
        )

    def moviefinder_providers(
        self,
        *,
        locale: str = "",
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/moviefinder/providers.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if locale:
            locale = f"locale={locale}"
        return self.rest.get(
            f"moviefinder/providers?{locale}", return_headers=return_headers, xml=xml
        )

    # Asynchronous Methods

    async def async_moviefinder(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send an asynchronous POST request to https://api.wild-devs.net/v1/moviefinder.

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
            "moviefinder", payload, return_headers=return_headers, xml=xml
        )

    async def async_moviefinder_locales(
        self,
        *,
        return_headers: bool = False,
        xml: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/moviefinder/locales.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return await self.rest.async_get(
            "moviefinder/locales", return_headers=return_headers, xml=xml
        )

    async def async_moviefinder_providers(
        self,
        *,
        locale: str = "",
        return_headers: bool = False,
        xml: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/moviefinder/providers.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if locale:
            locale = f"locale={locale}"
        return await self.rest.async_get(
            f"moviefinder/providers?{locale}", return_headers=return_headers, xml=xml
        )
