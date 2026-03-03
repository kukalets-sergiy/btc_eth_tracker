from app.api import AuthAPI
from app.schemas import Token, LoginSchema

from fastapi import APIRouter

auth_router = APIRouter()


@auth_router.post("/login", response_model=Token)
async def login(data: LoginSchema):
    return await AuthAPI.login(data)
