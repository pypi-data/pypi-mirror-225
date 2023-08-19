from __future__ import annotations

__all__ = [
    "RESTClient",
]

import typing as t

import requests
import aiohttp

from wild_devs_api.models.response import APIResponse
from wild_devs_api.errors.errors import send_error_response


class RESTClient:
    """
    The synchronous RestClient containing basic HTTP request methods.
    Implements sync and async variants of the requests.
    """

    _base_url: str
    _timeout: int
    _headers: dict[str, t.Any]
    _session: aiohttp.ClientSession

    def __init__(self, base_url: str, timeout: int, headers: dict[str, t.Any]) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.headers = headers

    def __str__(self) -> str:
        return f"BaseURL: {self.base_url}\nTimeout: {self.timeout}"

    @property
    def base_url(self):
        """The baseURL for all requests. Default is https://api.wild-devs.net/v1/."""
        return self._base_url

    @base_url.setter
    def base_url(self, value: str):
        if not value.startswith("https://"):
            print("Value is not a URL.")
            return
        else:
            self._base_url = value

    @property
    def timeout(self):
        """The amount of time to wait for a response, when a request has been made.
        Default is 30 seconds.
        Can be set between 5 seconds and 30 seconds."""
        return self._timeout

    @timeout.setter
    def timeout(self, value: int):
        if value > 30 or value < 5:
            print("Timeout must be a value between 5 and 30!")
            self._timeout = 30
        else:
            self._timeout = value

    @property
    def headers(self):
        """The request headers of the API. More headers can be added manually."""
        return self._headers

    @headers.setter
    def headers(self, value: dict[str, t.Any]):
        self._headers = value

    def build_payload(self, kwargs: dict[str, t.Any]) -> dict[str, t.Any]:
        """
        Helper method to create a payload from passed `**kwargs` if no payload has been supplied.

        Args:
            kwargs (`dict[str, t.Any]`): The `**kwargs` passed to an endpoint method.
        """
        payload: dict[str, t.Any] = {}
        for k in kwargs:
            payload[k] = kwargs[k]
        return payload

    def _request(
        self,
        method: str,
        endpoint: str,
        payload: t.Optional[dict[str, t.Any]] = None,
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        xml_string = ""
        r = requests.request(
            method, f"{self.base_url}{endpoint}", headers=self.headers, json=payload
        )
        if r.status_code == 404:
            resp = {"code": r.status_code, "note": f"{r.url} {r.reason}"}
            raise send_error_response(resp)
        if xml:
            if "?" in endpoint:
                xml_query_string = "&xml"
            else:
                xml_query_string = "?xml"
            xml_string = requests.request(
                method,
                f"{self.base_url + endpoint + xml_query_string}",
                headers=self.headers,
                json=payload,
            ).text
        if not return_headers:
            return APIResponse(r.json(), xml=xml_string)
        else:
            return APIResponse(r.json(), headers=r.headers, xml=xml_string)

    def get(self, endpoint: str, return_headers: bool = False, xml: bool = False) -> APIResponse:
        """
        Synchronous GET request.

        Args:
            endpoint (`str`): The endpoint to send the request to.
            return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self._request("GET", endpoint, return_headers=return_headers, xml=xml)

    def post(
        self,
        endpoint: str,
        payload: dict[str, t.Any],
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Synchronous POST request.

        Args:
            endpoint (`str`): The endpoint to send the request to.
            payload (`dict`[`str`, `Any`]): The payload to send to the endpoint.
            return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self._request(
            "POST", endpoint, payload, return_headers=return_headers, xml=xml
        )

    def put(
        self,
        endpoint: str,
        payload: dict[str, t.Any],
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Synchronous PUT request.

        Args:
            endpoint (`str`): The endpoint to send the request to.
            payload (`dict`[`str`, `Any`]): The payload to send to the endpoint.
            return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self._request(
            "PUT", endpoint, payload, return_headers=return_headers, xml=xml
        )

    def delete(self, endpoint: str, return_headers: bool = False, xml: bool = False) -> APIResponse:
        """
        Synchronous DELETE request.

        Args:
            endpoint (`str`): The endpoint to send the request to.
            return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self._request("DELETE", endpoint, return_headers=return_headers, xml=xml)

    async def _async_request(
        self,
        method: str,
        endpoint: str,
        payload: t.Optional[dict[str, t.Any]] = None,
        return_headers: bool = False,
        xml: bool = False
    ) -> APIResponse:
        xml_string = ""
        async with aiohttp.request(
            method, f"{self.base_url}{endpoint}", json=payload, headers=self.headers
        ) as r:
            if r.status == 404:
                resp = {"code": r.status, "note": f"{r.url} {r.reason}"}
                raise send_error_response(resp)
            if xml:
                if "?" in endpoint:
                    xml_query_string = "&xml"
                else:
                    xml_query_string = "?xml"
                xml_string = requests.request(
                    method,
                    f"{self.base_url + endpoint + xml_query_string}",
                    headers=self.headers,
                    json=payload,
                ).text
            if not return_headers:
                return APIResponse(await r.json(), xml=xml_string)
            else:
                return APIResponse(await r.json(), headers=r.headers, xml=xml_string)

    async def async_get(self, endpoint: str, *, return_headers: bool = False, xml: bool = False) -> APIResponse:
        """
        Asynchronous GET request.

        Args:
            endpoint (`str`): The endpoint to send the request to.
            return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return await self._async_request("GET", endpoint, return_headers=return_headers, xml=xml)

    async def async_post(
        self,
        endpoint: str,
        payload: dict[str, t.Any],
        return_headers: bool = False,
        xml: bool = False
    ) -> APIResponse:
        """
        Asynchronous POST request.

        Args:
            endpoint (`str`): The endpoint to send the request to.
            payload (`dict`[`str`, `Any`]): The payload to send to the endpoint.
            return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return await self._async_request(
            "POST", endpoint, payload, return_headers=return_headers, xml=xml
        )

    async def async_put(
        self,
        endpoint: str,
        payload: dict[str, t.Any],
        return_headers: bool = False,
        xml: bool = False
    ) -> APIResponse:
        """
        Asynchronous PUT request.

        Args:
            endpoint (`str`): The endpoint to send the request to.
            payload (`dict`[`str`, `Any`]): The payload to send to the endpoint.
            return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return await self._async_request(
            "PUT", endpoint, payload, return_headers=return_headers, xml=xml
        )

    async def async_delete(self, endpoint: str, return_headers: bool = False, xml: bool = False) -> APIResponse:
        """
        Asynchronous DELETE request.

        Args:
            endpoint (`str`): The endpoint to send the request to.
            return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return await self._async_request(
            "DELETE", endpoint, return_headers=return_headers, xml=xml
        )
