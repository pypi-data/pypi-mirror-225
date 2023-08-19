from __future__ import annotations

__all__ = [
    "Utility",
]

import typing as t
import base64

from wild_devs_api.restclient import RESTClient
from wild_devs_api.models.response import APIResponse


class Utility:
    """
    The endpoint class for utility related endpoints.
    Contains sync and async variants of the endpoint methods.
    """

    _rest: RESTClient

    def __init__(self, rest: RESTClient) -> None:
        self._rest = rest

    @property
    def rest(self) -> RESTClient:
        return self._rest

    # Synchronous Methods

    def plagiarism(
            self,
            payload: t.Optional[dict[str, t.Any]] = None,
            *,
            return_headers: bool = False,
            xml: bool = False,
            **kwargs: t.Any
            ) -> APIResponse:
        """
        Method to send a synchronous POST request to https://api.wild-dev.net/v1/plagiarism.

        Args:
            payload (`Optional`[`dict`[`str`, `Any`]]): The payload to send to the endpoint.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`. **kwargs (`Any`): The additional kwargs that have to be passed if payload
        is `None`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if not payload:
            payload = self.rest.build_payload(kwargs)
        return self.rest.post(
            "plagiarism", payload, return_headers=return_headers, xml=xml
        )

    def captcha(
        self,
        *,
        length: int = 6,
        height: int = 100,
        width: int = 200,
        charset: str = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        create_img: bool = False,
        file_path: str = "./",
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/captcha.

        Keyword Args: create_img (`bool`): Decides if a .png will be created from the generated QR-code. Default is
        `False`. file_path (`str`): The filepath where the .png will be created. Default is the current directory.
        return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the `APIResponse`. Default is
        `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if not create_img:
            return self.rest.get(
                f"captcha?length={length}&height={height}&width={width}&charset={charset}",
                return_headers=return_headers,
                xml=xml,
            )
        else:
            data = self.rest.get(
                f"captcha?length={length}&height={height}&width={width}&charset={charset}",
                return_headers=return_headers,
                xml=xml,
            )
            code = data.data["image"][22:]
            captcha = base64.b64decode(code)
            with open(f"{file_path}captcha.jpeg", "wb") as f:
                f.write(captcha)
            return data

    def compile(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send a synchronous POST request to https://api.wild-devs.net/v1/compile.

        Args:
            payload (`Optional`[`dict`[`str`, `Any`]]): The payload to send to the endpoint.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`. **kwargs (`Any`): The additional kwargs that have to be passed if payload
        is `None`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if not payload:
            payload = self.rest.build_payload(kwargs)
        return self.rest.post(
            "compile", payload, return_headers=return_headers, xml=xml
        )

    def decode(
        self,
        payload: dict[str, t.Any],
        *,
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Method to send a synchronous POST request to https://api.wild-devs.net/v1/decode.
        This endpoint doesn't support the usage of `**kwargs`.

        Args:
            payload (`dict`[`str`, `Any`]): The payload to send to the endpoint.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self.rest.post("decode", payload, return_headers=return_headers, xml=xml)

    def encode(
        self,
        payload: dict[str, t.Any],
        *,
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Method to send a synchronous POST request to https://api.wild-devs.net/v1/encode.
        This endpoint doesn't support the usage of `**kwargs`.

        Args:
            payload (`dict`[`str`, `Any`]): The payload to send to the endpoint.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self.rest.post("encode", payload, return_headers=return_headers, xml=xml)

    def hash(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send a synchronous POST request to https://api.wild-devs.net/v1/hash.

        Args:
            payload (`Optional`[`dict`[`str`, `Any`]]): The payload to send to the endpoint.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`. **kwargs (`Any`): The additional kwargs that have to be passed if payload
        is `None`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if not payload:
            payload = self.rest.build_payload(kwargs)
        return self.rest.post("hash", payload, return_headers=return_headers, xml=xml)

    def qrcode(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        create_img: bool = False,
        file_path: str = "./",
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send a synchronous POST request to https://api.wild-devs.net/v1/qrcode.

        Args:
            payload (Optional`dict`[`str`, `Any`]): The payload to send to the endpoint.

        Keyword Args: create_img (`bool`): Decides if a .png will be created from the generated QR-code. Default is
        `False`. file_path (`str`): The filepath where the .png will be created. Default is the current directory.
        return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the `APIResponse`. Default is
        `False`. **kwargs (`Any`): The additional kwargs that have to be passed if payload is `None`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if not payload:
            payload = self.rest.build_payload(kwargs)
        if not create_img:
            return self.rest.post(
                "qrcode", payload, return_headers=return_headers, xml=xml
            )
        else:
            data = self.rest.post(
                "qrcode", payload, return_headers=return_headers, xml=xml
            )
            code = data.data[21:]
            qr = base64.b64decode(code)
            with open(f"{file_path}qrcode.png", "wb") as f:
                f.write(qr)
            return data

    def nsfw(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send a synchronous POST request to https://api.wild-devs.net/v1/nsfw.

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
        return self.rest.post("nsfw", payload, return_headers=return_headers, xml=xml)

    def tts(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send a synchronous POST request to https://api.wild-devs.net/v1/tts.

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
        return self.rest.post("tts", payload, return_headers=return_headers, xml=xml)

    def tts_voices(
        self,
        *,
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/tts/voices.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """

        return self.rest.get("tts/voices", return_headers=return_headers, xml=xml)

    # Asynchronous Methods

    async def async_plagiarism(
            self,
            payload: t.Optional[dict[str, t.Any]] = None,
            *,
            return_headers: bool = False,
            xml: bool = False,
            **kwargs: t.Any
            ) -> APIResponse:
        """
        Method to send an asynchronous POST request to https://api.wild-dev.net/v1/plagiarism.

        Args:
            payload (`Optional`[`dict`[`str`, `Any`]]): The payload to send to the endpoint.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`. **kwargs (`Any`): The additional kwargs that have to be passed if payload
        is `None`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if not payload:
            payload = self.rest.build_payload(kwargs)
        return await self.rest.async_post(
            "plagiarism", payload, return_headers=return_headers, xml=xml
        )

    async def async_captcha(
        self,
        *,
        length: int = 6,
        height: int = 100,
        width: int = 200,
        charset: str = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        create_img: bool = False,
        file_path: str = "./",
        return_headers: bool = False,
        xml: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/captcha.

        Keyword Args: create_img (`bool`): Decides if a .png will be created from the generated QR-code. Default is
        `False`. file_path (`str`): The filepath where the .png will be created. Default is the current directory.
        return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the `APIResponse`. Default is
        `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if not create_img:
            return await self.rest.async_get(
                f"captcha?length={length}&height={height}&width={width}&charset={charset}",
                return_headers=return_headers, xml=xml
            )
        else:
            data = await self.rest.async_get(
                f"captcha?length={length}&height={height}&width={width}&charset={charset}",
                return_headers=return_headers, xml=xml
            )
            code = data.data["image"][22:]
            captcha = base64.b64decode(code)
            with open(f"{file_path}captcha.jpeg", "wb") as f:
                f.write(captcha)
            return data

    async def async_compile(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send an asynchronous POST request to https://api.wild-devs.net/v1/compile.

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
            "compile", payload, return_headers=return_headers
        )

    async def async_decode(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send an asynchronous POST request to https://api.wild-devs.net/v1/decode.

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
            "decode", payload, return_headers=return_headers, xml=xml
        )

    async def async_encode(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send an asynchronous POST request to https://api.wild-devs.net/v1/encode.

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
            "encode", payload, return_headers=return_headers, xml=xml
        )

    async def async_hash(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send an asynchronous POST request to https://api.wild-devs.net/v1/hash.

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
            "hash", payload, return_headers=return_headers
        )

    async def async_qrcode(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        create_img: bool = False,
        file_path: str = "./",
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send an asynchronous POST request to https://api.wild-devs.net/v1/qrcode.

        Args:
            payload (Optional`dict`[`str`, `Any`]): The payload to send to the endpoint.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`. create_img (`bool`): Decides if a .png will be created from the generated
        QR-code. Default is `False`. file_path (`str`): The filepath where the .png will be created. Default is the
        current directory. **kwargs (`Any`): The additional kwargs that have to be passed if payload is `None`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if not payload:
            payload = self.rest.build_payload(kwargs)
        if not create_img:
            return await self.rest.async_post(
                "qrcode", payload, return_headers=return_headers, xml=xml
            )
        else:
            data = await self.rest.async_post(
                "qrcode", payload, return_headers=return_headers, xml=xml
            )
            code = data.data[21:]
            qr = base64.b64decode(code)
            async with open(f"{file_path}qrcode.png", "wb") as f:
                f.write(qr)
            return data

    async def async_nsfw(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send an asynchronous POST request to https://api.wild-devs.net/v1/nsfw.

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
            "nsfw", payload, return_headers=return_headers, xml=xml
        )

    async def async_tts(
        self,
        payload: t.Optional[dict[str, t.Any]] = None,
        *,
        return_headers: bool = False,
        xml: bool = False,
        **kwargs: t.Any,
    ) -> APIResponse:
        """
        Method to send an asynchronous POST request to https://api.wild-devs.net/v1/tts.

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
        return await self.rest.async_post("tts", payload, return_headers=return_headers, xml=xml)

    async def async_tts_voices(
        self,
        *,
        return_headers: bool = False,
        xml: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/tts/voices.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """

        return await self.rest.async_get("tts/voices", return_headers=return_headers, xml=xml)
