from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import os

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.api_key = os.getenv("API_KEY")
    
    async def dispatch(self, request: Request, call_next):
        # Пропускаем документацию и health checks
        if request.url.path in ["/docs", "/redoc", "/openapi.json", "/health"]:
            return await call_next(request)
        
        # Проверяем API ключ
        api_key = request.headers.get("X-API-Key")
        if not api_key or api_key != self.api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid API key"}
            )
        
        return await call_next(request)