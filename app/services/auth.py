from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.models.revoked_token import RevokedToken

# Configurações do Token
SECRET_KEY = "mysecretkey"  # 🔥 Substitua por uma chave segura
REFRESH_SECRET_KEY = "myrefreshsecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Configuração de Hash de Senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para criar um hash seguro da senha
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Função para verificar senha
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Função para gerar um token JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Criar Refresh Token (expira mais tarde)
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)


# Função para validar e decodificar um token JWT
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Retorna os dados do usuário no token
    except JWTError:
        return None

# Verificar Refresh Token
def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Revogar Token (Logout)
def revoke_token(token: str, session: Session):
    revoked = RevokedToken(token=token)
    session.add(revoked)
    session.commit()

# Verificar se um token foi revogado
def is_token_revoked(token: str, session: Session):
    return session.exec(select(RevokedToken).where(RevokedToken.token == token)).first() is not None
