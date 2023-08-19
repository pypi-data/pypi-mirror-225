from __future__ import annotations

__all__ = [
    "WildDevsAPI",
]

import base64
import typing as t

import aiohttp

from wild_devs_api.restclient import RESTClient
from wild_devs_api.endpoints.conversion import Conversion
from wild_devs_api.endpoints.games import Games
from wild_devs_api.endpoints.mockup import Mockup
from wild_devs_api.endpoints.random import Random
from wild_devs_api.endpoints.urlshortener import UrlShortener
from wild_devs_api.endpoints.utility import Utility
from wild_devs_api.endpoints.validation import Validation
from wild_devs_api.endpoints.ai import AI
from wild_devs_api.endpoints.nettools import NetTools
from wild_devs_api.endpoints.moviefinder import MovieFinder
from wild_devs_api.endpoints.opendata import OpenData
from wild_devs_api.__version__ import __version__


class WildDevsAPI:
    """
    Base class of the WildDevsAPI wrapper.
    Includes a `RESTClient` and `AsyncRESTClient` with all endpoint methods.
    """

    _x_api_key: str
    _headers: dict[str, t.Any]
    _rest: RESTClient
    _conversion: Conversion
    _games: Games
    _mockup: Mockup
    _random: Random
    _urlshortener: UrlShortener
    _utility: Utility
    _validation: Validation
    _ai: AI
    _nettools: NetTools
    _moviefinder: MovieFinder
    _opendata: OpenData

    def __init__(
        self,
        *,
        base_url: str = "https://api.wild-devs.net/v1/",
        timeout: int = 30,
    ) -> None:
        self._headers = {
            "User-Agent": f"Wild Devs API v{__version__} Python SDK",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self._rest = RESTClient(base_url, timeout, self._headers)
        self._conversion = Conversion(self._rest)
        self._games = Games(self._rest)
        self._mockup = Mockup(self._rest)
        self._random = Random(self._rest)
        self._urlshortener = UrlShortener(self._rest)
        self._utility = Utility(self._rest)
        self._validation = Validation(self._rest)
        self._ai = AI(self._rest)
        self._nettools = NetTools(self._rest)
        self._moviefinder = MovieFinder(self._rest)
        self._opendata = OpenData(self._rest)

    def __str__(self) -> str:
        return f"X-Api-Key: {self.x_api_key}\nHeaders: {self.headers}\nRESTClient: {self.rest}\nVersion: {__version__}"

    @property
    def x_api_key(self) -> str:
        """The api-key used for member/subscriber endpoint requests."""
        return self._x_api_key

    @property
    def headers(self) -> dict[str, t.Any]:
        """The request headers of the API. More headers can be added manually."""
        return self._headers

    @property
    def rest(self) -> RESTClient:
        """The `RESTClient` of the API. Contains raw HTTP requests."""
        return self._rest

    @property
    def conversion(self) -> Conversion:
        """The class containing conversion related endpoint methods."""
        return self._conversion

    @property
    def games(self) -> Games:
        """The class containing game related endpoint methods."""
        return self._games

    @property
    def mockup(self) -> Mockup:
        """The class containing mockup related endpoint methods."""
        return self._mockup

    @property
    def random(self) -> Random:
        """The class containing random related endpoint methods."""
        return self._random

    @property
    def utility(self) -> Utility:
        """The class containing utility related endpoint methods."""
        return self._utility

    @property
    def urlshortener(self) -> UrlShortener:
        """The class containing urlshortener related endpoint methods."""
        return self._urlshortener

    @property
    def validation(self) -> Validation:
        """The class containing validation related endpoint methods."""
        return self._validation

    @property
    def ai(self) -> AI:
        """The class containing AI related endpoint methods."""
        return self._ai

    @property
    def nettools(self) -> NetTools:
        """The class containing net tools related endpoint methods."""
        return self._nettools

    @property
    def moviefinder(self) -> MovieFinder:
        """The class containing moviefinder related endpoint methods."""
        return self._moviefinder

    @property
    def opendata(self) -> OpenData:
        """The class containing open data related endpoint methods."""
        return self._opendata

    def encode_api_key(self, key: str, secret: str) -> None:
        """
        Method to turn the api-key and secret into base64 and add it to the headers. This is required to be able to use the member/subscriber endpoints.

        Args:
            key (`str`): The API key generated on https://wild-devs.net/account/keys. Always starts with `WD-`.
            secret (`str`): The secret generated besides the API key.
        """
        self._x_api_key = base64.b64encode(f"{key}:{secret}".encode("utf-8")).decode(
            "utf-8"
        )
        self._headers["x-api-key"] = self.x_api_key
        self._rest.headers = self.headers
        self._conversion = Conversion(self._rest)
        self._games = Games(self._rest)
        self._mockup = Mockup(self._rest)
        self._random = Random(self._rest)
        self._urlshortener = UrlShortener(self._rest)
        self._utility = Utility(self._rest)
        self._validation = Validation(self._rest)
        self._ai = AI(self._rest)
        self._nettools = NetTools(self._rest)
        self._moviefinder = MovieFinder(self._rest)
        self._opendata = OpenData(self._rest)