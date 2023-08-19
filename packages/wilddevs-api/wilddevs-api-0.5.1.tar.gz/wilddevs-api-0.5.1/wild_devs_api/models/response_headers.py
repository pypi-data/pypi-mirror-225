from __future__ import annotations

__all__ = [
    "ResponseHeaders",
]

from datetime import datetime
import typing as t


class ResponseHeaders:
    """
    Class representation of the response headers of a `APIResponse`.
    """

    _server: str
    _date: datetime
    _content_type: str
    _content_length: int
    _connection: str
    _x_powered_by: str
    _access_control_allow_origin: str
    _access_control_allow_headers: str
    _x_ratelimit_retry_after: float
    _x_ratelimit_limit: int
    _x_ratelimit_remaining: int
    _x_ratelimit_reset: datetime
    _etag: str
    _vary: str
    _strict_transport_security: str
    _referrer_policy: str
    _x_content_type_options: str
    _x_download_options: str
    _x_frame_options: str
    _x_permitted_cross_domain_policies: str
    _x_robots_tag: str
    _x_xss_protection: str
    _as_dict: t.Union[t.MutableMapping[str, t.Any], t.Mapping[str, t.Any]]

    def __init__(
        self, headers: t.Union[t.MutableMapping[str, t.Any], t.Mapping[str, t.Any]]
    ) -> None:
        self._server = headers["Server"]
        self._date = datetime.strptime(headers["Date"], "%a, %d %b %Y %H:%M:%S %Z")
        self._content_type = headers["Content-Type"]
        self._content_length = int(headers["Content-Length"])
        self._connection = headers["Connection"]
        self._x_powered_by = headers["X-Powered-By"]
        self._access_control_allow_origin = headers["Access-Control-Allow-Origin"]
        self._access_control_allow_headers = headers["Access-Control-Allow-Headers"]
        self._x_ratelimit_retry_after = float(headers["x-ratelimit-retry-after"])
        self._x_ratelimit_limit = int(headers["x-ratelimit-limit"])
        self._x_ratelimit_remaining = int(headers["x-ratelimit-remaining"])
        self._x_ratelimit_reset = datetime.strptime(
            headers["x-ratelimit-reset"], "%a %b %d %Y %H:%M:%S %Z%z"
        )
        self._etag = headers["ETag"]
        self._vary = headers["Vary"]
        self._strict_transport_security = headers["Strict-Transport-Security"]
        self._referrer_policy = headers["Referrer-Policy"]
        self._x_content_type_options = headers["X-Content-Type-Options"]
        self._x_download_options = headers["X-Download-Options"]
        self._x_frame_options = headers["X-Frame-Options"]
        self._x_permitted_cross_domain_policies = headers[
            "X-Permitted-Cross-Domain-Policies"
        ]
        self._x_robots_tag = headers["X-Robots-Tag"]
        self._x_xss_protection = headers["X-XSS-Protection"]
        self._as_dict = headers

    def __str__(self) -> str:
        return f"{self.as_dict}"

    @property
    def server(self):
        """The type of server, that the API uses."""
        return self._server

    @property
    def date(self):
        """The timestamp of the response."""
        return self._date

    @property
    def content_type(self):
        """The content type of the response."""
        return self._content_type

    @property
    def content_length(self):
        """The length of the response content."""
        return self._content_length

    @property
    def connection(self):
        """The type of connection for requests to the API server."""
        return self._connection

    @property
    def x_powered_by(self):
        """The name of the API server."""
        return self._x_powered_by

    @property
    def access_control_allow_origin(self):
        """The origins allowed to make requests from."""
        return self._access_control_allow_origin

    @property
    def access_control_allow_headers(self):
        """The headers that can be sent to the API."""
        return self._access_control_allow_headers

    @property
    def x_ratelimit_retry_after(self):
        """The time in seconds until the next reset."""
        return self._x_ratelimit_retry_after

    @property
    def x_ratelimit_limit(self):
        """The daily ratelimit."""
        return self._x_ratelimit_limit

    @property
    def x_ratelimit_remaining(self):
        """The remaining amount of requests before reset."""
        return self._x_ratelimit_remaining

    @property
    def x_ratelimit_reset(self):
        """The date, when the ratelimit gets reset."""
        return self._x_ratelimit_reset

    @property
    def etag(self):
        """The resource identifier for the request."""
        return self._etag

    @property
    def vary(self):
        """The parts of the request message aside from the method and URL."""
        return self._vary

    @property
    def strict_transport_security(self):
        """The information sent to browsers, that sites should only be accessed using HTTPS."""
        return self._strict_transport_security

    @property
    def referrer_policy(self):
        """The amount of referrer information, that should be included with requests."""
        return self._referrer_policy

    @property
    def x_content_type_options(self):
        """The indication if MIME types in the `content_type` header should be followed."""
        return self._x_content_type_options

    @property
    def x_download_options(self):
        """The instruction to the browser, that downloads shouldn't directly be started."""
        return self._x_download_options

    @property
    def x_frame_options(self):
        """The indication if a browser should be allowed to render a page."""
        return self._x_frame_options

    @property
    def x_permitted_cross_domain_policies(self):
        """The allowance of a cross-domain policy file."""
        return self._x_permitted_cross_domain_policies

    @property
    def x_robots_tag(self):
        """The indication how a web page is to be indexed within public search engine results."""
        return self._x_robots_tag

    @property
    def x_xss_protection(self):
        """The filtering used when cross-site scripting attacks get detected."""
        return self._x_xss_protection

    @property
    def as_dict(self):
        """The dictionary representation of the `ResponseHeaders`."""
        return self._as_dict
