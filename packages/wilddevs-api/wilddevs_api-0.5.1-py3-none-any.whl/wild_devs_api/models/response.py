from __future__ import annotations

__all__ = [
    "APIResponse",
]

import typing as t
from dataclasses import dataclass

from wild_devs_api.errors.errors import send_error_response
from wild_devs_api.models.response_headers import ResponseHeaders


@dataclass
class APIResponse:
    """
    Class representation of the API response.
    """

    _status: str
    _code: int
    _message: str
    _data: t.Any
    _headers: ResponseHeaders
    _as_dict: t.Union[dict[str, str], dict[dict[str, t.Any], dict[str, str]]]
    _xml: str

    def __init__(
        self,
        data: dict[str, t.Any],
        *,
        headers: t.Optional[
            t.Union[t.MutableMapping[str, t.Any], t.Mapping[str, t.Any]]
        ] = None,
        xml: str,
    ) -> None:
        if data["code"] >= 400:
            raise send_error_response(data)
        self.status = data["status"]
        self.code = data["code"]
        self.message = data["message"]
        self.data = data["data"]
        self.xml = xml
        if headers:
            self.as_dict = {"Response": data, "Headers": headers}
            self.headers = ResponseHeaders(headers)
        else:
            self.as_dict = data

    def __str__(self) -> str:
        return f"{self.as_dict}"

    @property
    def status(self):
        """The status of the response."""
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = value

    @property
    def code(self):
        """The status code of the response."""
        return self._code

    @code.setter
    def code(self, value: int):
        self._code = value

    @property
    def message(self):
        """The message of the response"""
        return self._message

    @message.setter
    def message(self, value: str):
        self._message = value

    @property
    def data(self):
        """The content of the response."""
        return self._data

    @data.setter
    def data(self, value: dict[str, t.Any]):
        self._data = value

    @property
    def headers(self):
        """The `ResponseHeaders` of the response. Will only be present if `return_headers=True` in the request method."""
        return self._headers

    @headers.setter
    def headers(self, value: ResponseHeaders):
        self._headers = value

    @property
    def as_dict(self):
        """Dictionary representation of the response data. Will be a dictionary of dictionaries if `return_headers=True` in the request method."""
        return self._as_dict

    @as_dict.setter
    def as_dict(
        self, value: t.Union[dict[str, t.Any], dict[dict[str, t.Any], dict[str, str]]]
    ):
        self._as_dict = value

    @property
    def xml(self) -> str:
        """The xml representation, if `xml=True` in the request method."""
        return self._xml

    @xml.setter
    def xml(self, value: str) -> None:
        self._xml = value
