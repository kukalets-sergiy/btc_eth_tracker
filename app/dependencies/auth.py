from app.models import User
from configurations.exceptions import InvalidTokenException
from configurations.jwt import jwt_decode_handler
from jose import JWTError

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials


from fastapi.security import HTTPBearer

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> User:
    token = credentials.credentials

    try:
        payload = jwt_decode_handler(token)
    except JWTError:
        raise InvalidTokenException()

    user = await User.objects.filter(uuid=payload.get("sub")).afirst()
    if not user:
        raise InvalidTokenException()

    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
