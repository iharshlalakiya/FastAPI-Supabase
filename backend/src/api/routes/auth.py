from fastapi import APIRouter, Depends
from src.schemas.auth import SignUpSchema, LoginSchema
from src.services.auth_service import signup_user, login_user
from src.core.security import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup")
def signup(data: SignUpSchema):
    return signup_user

@router.post("/login")
def login(data: LoginSchema):
    return login_user

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return current_user