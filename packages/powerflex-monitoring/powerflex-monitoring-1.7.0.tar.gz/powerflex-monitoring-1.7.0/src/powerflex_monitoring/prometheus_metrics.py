from typing import Callable, Optional

from prometheus_client import generate_latest
from starlette.types import Receive, Scope, Send

PROMETHEUS_CONTENT_TYPE_LATEST = "text/plain; version=0.0.4; charset=utf-8"


async def prometheus_asgi_app(scope: Scope, receive: Receive, send: Send) -> None:
    """ASGI app which returns the prometheus metrics as plain text via HTTP."""
    assert scope.get("type") == "http"

    headers = ("Content-Type", PROMETHEUS_CONTENT_TYPE_LATEST)

    output = generate_latest()

    payload = await receive()
    if payload.get("type") == "http.request":
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [tuple(header.encode("utf8") for header in headers)],
            }
        )
        await send({"type": "http.response.body", "body": output})


class PrometheusASGIAppWithCallback:
    def __init__(
        self, after_metrics_scraped: Optional[Callable[[], None]] = None
    ) -> None:
        self.after_metrics_scraped = after_metrics_scraped

    def set_after_metrics_scraped(
        self, after_metrics_scraped: Callable[[], None]
    ) -> None:
        self.after_metrics_scraped = after_metrics_scraped

    async def asgi_app(self, scope: Scope, receive: Receive, send: Send) -> None:
        """ASGI app which returns the prometheus metrics as plain text."""
        await prometheus_asgi_app(scope, receive, send)

        if self.after_metrics_scraped is not None:
            self.after_metrics_scraped()
