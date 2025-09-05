# services/supabase_auth.py
import os, jwt, logging
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

log = logging.getLogger("uvicorn")
security = HTTPBearer(auto_error=True)
SECRET = os.getenv("SUPABASE_JWT_SECRET")

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if not SECRET:
        log.error("SUPABASE_JWT_SECRET missing")
        raise HTTPException(500, "Auth misconfigured")
    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        return decoded.get("sub")
    except jwt.ExpiredSignatureError:
        log.warning("JWT expired")
        raise HTTPException(401, "Token expired")
    except Exception as e:
        log.error(f"JWT verify failed: {e}")
        raise HTTPException(401, "Invalid token")
