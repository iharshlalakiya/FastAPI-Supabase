from fastapi import HTTPException, Header
from supabase import create_client
from src.core.config import settings
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials   
# from src.db.supabase_client import supabase
# from typing import Annotated

def get_current_user(authorization: str = Header(None, alias="Authorization")):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    user_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    user_client.postgrest.auth(token)

    try:
        user_response = user_client.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = getattr(user_response, "user", None)
    user_id = getattr(user, "id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user_client, user_id


# security = HTTPBearer()


# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security)
# ):
#     try:
#         token = credentials.credentials

#         user_response = supabase.auth.get_user(token)

#         if not user_response.user:
#             raise HTTPException(status_code=401, detail="Invalid token")

#         return user_response.user

#     except Exception as e:
#         print("AUTH ERROR:", str(e))
#         raise HTTPException(status_code=401, detail="Unauthorized")