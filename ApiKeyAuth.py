import os
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

class ApiKeyAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware that checks for a custom 'x-api-key' header and compares it 
    to an environment variable called 'API_KEY'.
    """

    def __init__(self, app: FastAPI, api_key_header: str = "x-api-key"):
        super().__init__(app)
        self.app = app
        self.api_key_header = api_key_header
        self.expected_api_key = os.getenv("API_KEY")

        if not self.expected_api_key:
            raise ValueError(
                "API_KEY environment variable not set. Please set it before running the application."
            )

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Extract the API key from the incoming request's headers
        incoming_api_key = request.headers.get(self.api_key_header)

        if not incoming_api_key or incoming_api_key != self.expected_api_key:
            raise HTTPException(status_code=403, detail="Invalid or missing API Key")

        # If valid, process the request
        response = await call_next(request)
        return response
