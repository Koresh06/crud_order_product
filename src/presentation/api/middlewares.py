from datetime import datetime, timedelta

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from src.utils.exceptions import RateLimitExceededException


class RateLimitingMiddleware(BaseHTTPMiddleware):
    rate_limit_duration = timedelta(minutes=1)
    rate_limit_requests = 100

    def __init__(self, app, **kwargs):
        super().__init__(app)
        self.request_counts: dict[str, tuple[int, datetime]] = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host

        request_count, last_request = self.request_counts.get(
            client_ip, (0, datetime.min)
        )
        elapsed_time = datetime.now() - last_request

        if elapsed_time > self.rate_limit_duration:
            request_count = 1
        else:
            if request_count >= self.rate_limit_requests:
                return RateLimitExceededException.get_response()
            request_count += 1

        self.request_counts[client_ip] = (request_count, datetime.now())

        response = await call_next(request)
        return response
