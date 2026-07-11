import json

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

# Docs routes serve their own raw JSON/HTML (e.g. the OpenAPI schema) - wrapping
# them would break Swagger UI, which expects the schema as-is.
_EXCLUDED_PATHS = {"/openapi.json", "/docs", "/redoc"}

# Recomputed by JSONResponse for the new (re-wrapped) body, so the old values
# from the inner response would be stale/wrong if we let them through.
_STALE_HEADERS = {"content-length", "content-type"}


class StructuredResponseMiddleware(BaseHTTPMiddleware):
    """Wraps every JSON API response in a `{success, status_code, data, error}` envelope."""

    async def dispatch(self, request: Request, call_next):
        if request.url.path in _EXCLUDED_PATHS:
            return await call_next(request)

        try:
            response = await call_next(request)
        except Exception as exc:
            # Only reached for errors with no exception handler registered (e.g. a bug
            # deep in a route) - FastAPI's own handlers already turn HTTPException etc.
            # into a normal response before we get here.
            return self._error_response(500, str(exc) or "Internal Server Error")

        content_type = response.headers.get("content-type", "").split(";")[0]
        if content_type != "application/json":
            return response

        # call_next() returns a streaming wrapper, not a plain Response, so the body
        # has to be read off its async iterator rather than a `.body` attribute.
        body = b""
        async for chunk in response.body_iterator:  # type: ignore[attr-defined]
            body += chunk

        payload = json.loads(body) if body else None
        headers = {k: v for k, v in response.headers.items() if k.lower() not in _STALE_HEADERS}

        if response.status_code < 400:
            return self._success_response(response.status_code, payload, headers)
        return self._error_response(response.status_code, payload, headers)

    @staticmethod
    def _success_response(status_code, data, headers=None) -> JSONResponse:
        content = {"success": True, "status_code": status_code, "data": data, "error": None}
        return JSONResponse(status_code=status_code, content=content, headers=headers)

    @staticmethod
    def _error_response(status_code, error, headers=None) -> JSONResponse:
        content = {"success": False, "status_code": status_code, "data": None, "error": error}
        return JSONResponse(status_code=status_code, content=content, headers=headers)
