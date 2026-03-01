from fastapi import Depends, HTTPException, Header
from src.db.supabase_client import supabase

def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        user = supabase.auth.get_user(token)
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")