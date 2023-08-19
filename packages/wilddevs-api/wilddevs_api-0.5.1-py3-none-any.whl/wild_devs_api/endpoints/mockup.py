from __future__ import annotations

__all__ = [
    "Mockup",
]

from wild_devs_api.restclient import RESTClient
from wild_devs_api.models.response import APIResponse


class Mockup:
    """
    The endpoint class for mockup related endpoints.
    Contains sync and async variants of the endpoint methods.
    """

    _rest: RESTClient

    def __init__(self, rest: RESTClient) -> None:
        self._rest = rest

    @property
    def rest(self) -> RESTClient:
        return self._rest

    # Synchronous Methods

    def address(
        self,
        *,
        locale: str = "en",
        count: int = 1,
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/address.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self.rest.get(
            f"address?locale={locale}&count={count}",
            return_headers=return_headers,
            xml=xml,
        )

    def company(
        self, *, count: int = 1, return_headers: bool = False, xml: bool = False
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/company.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self.rest.get(
            f"company?count={count}", return_headers=return_headers, xml=xml
        )

    def finance(
        self, *, count: int = 1, return_headers: bool = False, xml: bool = False
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/finance.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self.rest.get(
            f"finance?count={count}", return_headers=return_headers, xml=xml
        )

    def git(
        self, *, count: int = 1, return_headers: bool = False, xml: bool = False
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/git.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self.rest.get(
            f"git?count={count}", return_headers=return_headers, xml=xml
        )

    def internet(
        self, *, count: int = 1, return_headers: bool = False, xml: bool = False
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/internet.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self.rest.get(
            f"internet?count={count}", return_headers=return_headers, xml=xml
        )

    def product(
        self, *, count: int = 1, return_headers: bool = False, xml: bool = False
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/product.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self.rest.get(
            f"product?count={count}", return_headers=return_headers, xml=xml
        )

    def user(
        self,
        *,
        locale: str = "en",
        count: int = 1,
        sex: str = "",
        address: bool = False,
        finance: bool = False,
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/user.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        query_string = ""
        if sex in ["male", "female"]:
            query_string += f"&sex={sex}"
        if address:
            query_string += "&address"
        if finance:
            query_string += "&finance"
        return self.rest.get(
            f"user?locale={locale}&count={count}{query_string}",
            return_headers=return_headers,
            xml=xml,
        )

    def vehicle(
        self, *, count: int = 1, return_headers: bool = False, xml: bool = False
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/vehicle.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self.rest.get(
            f"vehicle?count={count}", return_headers=return_headers, xml=xml
        )

    # Asynchronous Methods

    async def async_address(
        self, *, locale: str = "en", count: int = 1, return_headers: bool = False, xml: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/address.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return await self.rest.async_get(
            f"address?locale={locale}&count={count}", return_headers=return_headers, xml=xml
        )

    async def async_company(
        self, *, count: int = 1, return_headers: bool = False, xml: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/company.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return await self.rest.async_get(
            f"company?count={count}", return_headers=return_headers, xml=xml
        )

    async def async_finance(
        self, *, count: int = 1, return_headers: bool = False, xml: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/finance.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return await self.rest.async_get(
            f"finance?count={count}", return_headers=return_headers, xml=xml
        )

    async def async_git(
        self, *, count: int = 1, return_headers: bool = False, xml: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/git.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return await self.rest.async_get(
            f"git?count={count}", return_headers=return_headers, xml=xml
        )

    async def async_internet(
        self, *, count: int = 1, return_headers: bool = False, xml: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/internet.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return await self.rest.async_get(
            f"internet?count={count}", return_headers=return_headers, xml=xml
        )

    async def async_product(
        self, *, count: int = 1, return_headers: bool = False, xml: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/product.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return await self.rest.async_get(
            f"product?count={count}", return_headers=return_headers, xml=xml
        )

    async def async_user(
        self,
        *,
        locale: str = "en",
        sex: str = "",
        count: int = 1,
        address: bool = False,
        finance: bool = False,
        return_headers: bool = False,
        xml: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/user.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        query_string = ""
        if sex in ["male", "female"]:
            query_string += f"&sex={sex}"
        if address:
            query_string += "&address"
        if finance:
            query_string += "&finance"
        return await self.rest.async_get(
            f"user?locale={locale}&count={count}{query_string}",
            return_headers=return_headers, xml=xml
        )

    async def async_vehicle(
        self, *, count: int = 1, return_headers: bool = False, xml: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/vehicle.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return await self.rest.async_get(
            f"vehicle?count={count}", return_headers=return_headers, xml=xml
        )
