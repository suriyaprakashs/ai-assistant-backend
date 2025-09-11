import os, jwt, logging
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

log = logging.getLogger("uvicorn")
security = HTTPBearer(auto_error=True)

SECRET = os.getenv("SUPABASE_JWT_SECRET")
AUDIENCE = os.getenv("SUPABASE_JWT_AUDIENCE", "authenticated")  # Supabase default

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if not SECRET:
        log.error("SUPABASE_JWT_SECRET is not set")
        raise HTTPException(500, "Auth misconfigured")
    try:
        decoded = jwt.decode(
            token,
            SECRET,
            algorithms=["HS256"],
            audience=AUDIENCE,  # ✅ expect aud to be "authenticated"
        )
        return decoded.get("sub")
    except jwt.ExpiredSignatureError:
        log.warning("JWT expired")
        raise HTTPException(401, "Token expired")
    except Exception as e:
        log.error(f"JWT verify failed: {e}")
        raise HTTPException(401, "Invalid token")
