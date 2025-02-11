from fastapi import HTTPException, Request
from sqlmodel import Session
from starlette.middleware.base import BaseHTTPMiddleware

from app.config.database import get_session
from app.services.auth import is_token_revoked, verify_access_token


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        session: Session = next(get_session())

        # 🔥 Lista de rotas públicas (sem necessidade de autenticação)
        public_routes = ["/", "/auth/login", "/auth/refresh", "/docs", "/openapi.json"]

        # Se a rota for pública, passa direto
        if any(request.url.path.startswith(route) for route in public_routes):
            return await call_next(request)

        # 🔒 Obtém o token do cabeçalho Authorization
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token não encontrado")

        token = auth_header.split(" ")[1]  # Extrai o token após "Bearer"

        # 🔒 Verifica se o token é válido
        payload = verify_access_token(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")

        # 🔒 Verifica se o token foi revogado (Logout)
        if is_token_revoked(token, session):
            raise HTTPException(status_code=401, detail="Token revogado")

        # ✅ Se tudo estiver OK, continua o processamento
        response = await call_next(request)
        return response
