from logging import getLogger

from pydantic import EmailStr

from app.models import User
from app.schemas import LoginSchema
from configurations.exceptions import (
    InvalidCredentialsException,
    InvalidEmailOrPasswordException,
)
from configurations.jwt import create_access_token_response
from configurations.password import verify_password

logger = getLogger(__name__)


class AuthAPI:
    @classmethod
    async def login(cls, data: LoginSchema) -> dict[str, str]:
        if not data.email or not data.password:
            raise InvalidCredentialsException()

        user = await cls()._authenticate_user(
            email=data.email,
            password=data.password,
        )

        return create_access_token_response({"sub": str(user.uuid)})

    async def _authenticate_user(self, email: EmailStr, password: str) -> User:
        user = await User.objects.filter(email=email).afirst()
        if not user:
            raise InvalidEmailOrPasswordException()

        if not verify_password(password, user.password) or not user.is_active:
            raise InvalidEmailOrPasswordException()

        return user
