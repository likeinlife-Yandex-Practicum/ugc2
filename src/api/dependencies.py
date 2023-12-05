import jwt
from fastapi import Depends, HTTPException, Request, status

from src.services import InvalidJWTScopeError, JWTService, get_jwt_service


class NoAccessError(Exception):
    ...


def get_user_id(
    request: Request,
    jwt_service: JWTService = Depends(get_jwt_service),
):
    try:
        access_token = request.cookies.get("access_token")
        if not access_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        user_id = jwt_service.get_user_id(access_token)
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except InvalidJWTScopeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
