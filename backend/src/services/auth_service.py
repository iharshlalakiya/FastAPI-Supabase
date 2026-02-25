from fastapi import HTTPException
from src.db.supabase_client import supabase

def signup_user(data):
    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    # create user in supabase auth
    auth_response = supabase.auth.sign_up(
        {
            "email": data.email,
            "password": data.password,
        }
    )

    if not auth_response.user:
        raise HTTPException(status_code=400, details="Signup failed")
    
    user_id = auth_response.user.id

    # insert into users table
    supabase.table("users").insert(
        {
            "id": user_id,
            "name": data.name,
            "email": data.email,
            "phone": data.phone
        }
    ).execute()

    return{
        "message": "user registered successfully",
        "access_token": auth_response.session.access_token
    }


def login_user(data):
    auth_response = supabase.auth.sign_in_with_password(
        {
            "email": data.email,
            "password": data.password
        }
    )

    if not auth_response.user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    user_id = auth_response.user_id

    db_user = supabase.table("users").select("").eq("id", user_id).execute()

    if not db_user.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    return{
        "message": "Login successful",
        "access_token": auth_response.session.access_token,
        "user": db_user.data[0]
    }