from __future__ import annotations

__all__ = [
    "OpenData",
]

from wild_devs_api.restclient import RESTClient
from wild_devs_api.models.response import APIResponse


class OpenData:
    """
    The endpoint class for open data related endpoints.
    Contains sync and async variants of the endpoint methods.
    """

    _rest: RESTClient

    def __init__(self, rest: RESTClient) -> None:
        self._rest = rest

    @property
    def rest(self) -> RESTClient:
        return self._rest

    # Synchronous Methods

    def domains(
        self,
        *,
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/domains.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return self.rest.get("domains", return_headers=return_headers, xml=xml)

    def book(
        self,
        *,
        limit: int = 1,
        offset: int = 1,
        published_year: int = None,
        isbn13: int = None,
        isbn10: int = None,
        random: bool = True,
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/book.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        query_string = f"?limit={limit}&offset={offset}"
        if published_year:
            query_string += f"&published_year={published_year}"
        if isbn13:
            query_string += f"&isbn13={isbn13}"
        if isbn10:
            query_string += f"&isbn10={isbn10}"
        if random:
            query_string += "&random"
        return self.rest.get(f"book{query_string}", return_headers=return_headers, xml=xml)

    def exercise(
        self,
        *,
        limit: int = 1,
        offset: int = 1,
        difficulty: str = "Easy",
        random: bool = False,
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/exercise.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        if difficulty not in ["Easy", "Medium", "Hard"]:
            difficulty = "Easy"
        query_string = f"?limit={limit}&offset={offset}&difficulty={difficulty}"
        if random:
            query_string += "&random"
        return self.rest.get(f"exercise{query_string}", return_headers=return_headers, xml=xml)

    def chess_game(
        self,
        *,
        limit: int = 1,
        offset: int = 1,
        rated: bool = False,
        opening_code: str = "",
        victory_status: str = "",
        winner: str = "",
        random: bool = True,
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Method to send a synchronous GET request to https://api.wild-devs.net/v1/chess/game.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        query_string = f"?limit={limit}&offset={offset}"
        if rated:
            query_string += "&rated"
        if opening_code:
            query_string += f"&opening_code={opening_code}"
        if victory_status:
            query_string += f"&victory_status={victory_status}"
        if winner:
            query_string += f"&winner={winner}"
        if random:
            query_string += "&random"
        return self.rest.get(f"chess/game{query_string}", return_headers=return_headers, xml=xml)
    # Asynchronous Methods

    async def async_domains(
        self,
        *,
        return_headers: bool = False,
        xml: bool = False
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/domains.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        return await self.rest.async_get("domains", return_headers=return_headers, xml=xml)

    async def async_book(
        self,
        *,
        limit: int = 1,
        offset: int = 1,
        published_year: int = None,
        isbn13: int = None,
        isbn10: int = None,
        random: bool = True,
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/book.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        query_string = f"?limit={limit}&offset={offset}"
        if published_year:
            query_string += f"&published_year={published_year}"
        if isbn13:
            query_string += f"&isbn13={isbn13}"
        if isbn10:
            query_string += f"&isbn10={isbn10}"
        if random:
            query_string += "&random"
        return await self.rest.async_get(f"book{query_string}", return_headers=return_headers, xml=xml)

    async def async_exercise(
        self,
        *,
        limit: int = 1,
        offset: int = 1,
        difficulty: str = "Easy",
        random: bool = False,
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/exercise.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        query_string = f"?limit={limit}&offset={offset}&difficulty={difficulty}"
        if random:
            query_string += "&random"
        return await self.rest.async_get(f"exercise{query_string}", return_headers=return_headers, xml=xml)

    async def async_chess_game(
        self,
        *,
        limit: int = 1,
        offset: int = 1,
        rated: bool = False,
        opening_code: str = "",
        victory_status: str = "",
        winner: str = "",
        random: bool = True,
        return_headers: bool = False,
        xml: bool = False,
    ) -> APIResponse:
        """
        Method to send an asynchronous GET request to https://api.wild-devs.net/v1/chess/game.

        Keyword Args: return_headers (`bool`): Decides if the `ResponseHeaders` should be included in the
        `APIResponse`. Default is `False`.

        Returns:
            `APIResponse`: The object created from the response.
        """
        query_string = f"?limit={limit}&offset={offset}"
        if rated:
            query_string += "&rated"
        if opening_code:
            query_string += f"&opening_code={opening_code}"
        if victory_status:
            query_string += f"&victory_status={victory_status}"
        if winner:
            query_string += f"&winner={winner}"
        if random:
            query_string += "&random"
        return await self.rest.async_get(f"chess/game{query_string}", return_headers=return_headers, xml=xml)
    