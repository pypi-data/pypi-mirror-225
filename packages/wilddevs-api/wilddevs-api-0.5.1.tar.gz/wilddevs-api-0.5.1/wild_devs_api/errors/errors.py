from __future__ import annotations

__all__ = [
    "WildDevsError",
    "BadRequestError",
    "send_error_response",
    "UnauthorizedError",
    "ForbiddenError",
    "NotFoundError",
    "InternalServerError",
    "BadGatewayError",
    "ServiceUnavailableError",
    "GatewayTimeoutError",
]

import typing as t


class WildDevsError(Exception):
    """
    Base error class of the WildDevsAPI Wrapper. All errors raised by the WildDevsAPI module will be a subclass of this exception.
    """

    pass


class BadRequestError(WildDevsError):
    """
    Error raised when an API request returns code 400.
    """

    def __init__(
        self,
        error: str,
        *,
        not_allowed_fields: str | None = "",
        missing_fields: str | None = "",
    ) -> None:
        super().__init__(f"{error} {not_allowed_fields}{missing_fields}")


class UnauthorizedError(WildDevsError):
    """
    Error raised when an API request returns code 401.
    """

    def __init__(self, error: str) -> None:
        super().__init__(error)


class ForbiddenError(WildDevsError):
    """
    Error raised when an API request returns code 403.
    """

    def __init__(self, error: str) -> None:
        super().__init__(error)


class NotFoundError(WildDevsError):
    """
    Error raised when an API request returns code 404.
    """

    def __init__(self, error: str) -> None:
        super().__init__(error)


class InternalServerError(WildDevsError):
    """
    Error raised when an API request returns code 500.
    """

    def __init__(self, error: str) -> None:
        super().__init__(error)


class BadGatewayError(WildDevsError):
    """
    Error raised when an API request returns code 502.
    """

    def __init__(self, error: str) -> None:
        super().__init__(error)


class ServiceUnavailableError(WildDevsError):
    """
    Error raised when an API request returns code 503.
    """

    def __init__(self, error: str) -> None:
        super().__init__(error)


class GatewayTimeoutError(WildDevsError):
    """
    Error raised when an API request returns code 504.
    """

    def __init__(self, error: str) -> None:
        super().__init__(error)


class TooManyRequestsError(WildDevsError):
    """
    Error raised when an API request returns code 429.
    """

    def __init__(self, error: str) -> None:
        super().__init__(error)


def send_error_response(data: dict[str, t.Any]) -> WildDevsError:
    code = data["code"]
    error = data["note"]
    if code == 400:
        if not_allowed_fields := data.get("notAllowedFields"):
            return BadRequestError(error, not_allowed_fields=not_allowed_fields)
        if missing_fields := data.get("missingFields"):
            return BadRequestError(error, missing_fields=missing_fields)
        return BadRequestError(error)
    return _error_dict[code](error)


_error_dict: dict[int, type[WildDevsError]] = {
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    429: TooManyRequestsError,
    500: InternalServerError,
    502: BadGatewayError,
    503: ServiceUnavailableError,
    504: GatewayTimeoutError,
}
