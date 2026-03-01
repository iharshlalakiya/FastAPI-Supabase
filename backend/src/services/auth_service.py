from fastapi import HTTPException
from src.db.supabase_client import supabase

def signup_user(data):
    try:
        if data.password != data.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        # Create auth user
        auth_response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password,
        })

        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Signup failed")

        user_id = auth_response.user.id

        # Insert into users table
        db_response = supabase.table("users").insert({
            "id": user_id,
            "name": data.name,
            "email": data.email,
            "phone": data.phone
        }).execute()

        print("DB RESPONSE:", db_response)

        # If insert fails, Supabase throws exception automatically
        if not db_response.data:
            raise HTTPException(status_code=400, detail="Insert failed")

        access_token = None
        if auth_response.session:
            access_token = auth_response.session.access_token

        return {
            "message": "User registered successfully",
            "access_token": access_token,
            "user": db_response.data[0]
        }

    except Exception as e:
        print("EXCEPTION:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


def login_user(data):
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })

        if not auth_response.user or not auth_response.session:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        user_token = auth_response.session.access_token

        supabase.postgrest.auth(user_token)

        db_user = supabase.table("users") \
            .select("*") \
            .eq("id", auth_response.user.id) \
            .execute()

        if not db_user.data:
            raise HTTPException(status_code=404, detail="User profile not found")

        return {
            "message": "Login successful",
            "access_token": user_token,
            "user": db_user.data[0]
        }

    except Exception as e:
        print("LOGIN ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))