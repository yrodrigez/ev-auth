from time import time

from fastapi import APIRouter, Depends, Response
from fastapi.params import Cookie

from src.application.usecases.get_session_usecase import GetSessionUseCase
from src.infrastructure.redis.redis_client import get_redis_client
from src.infrastructure.redis.redis_session_repository import \
    RedisSessionRepository

router = APIRouter()

def build_get_session_usecase() -> GetSessionUseCase:
    redis_client = get_redis_client()
    session_repository = RedisSessionRepository(client=redis_client)

    return GetSessionUseCase(
        session_repository=session_repository
    )

@router.get("/sessions")
def get_session(
    session_id: str | None = Cookie(default=None, alias="ev_auth_session_id"),
    response: Response = None,
    usecase: GetSessionUseCase = Depends(build_get_session_usecase)
):
    if session_id is None:
        raise ValueError("Session ID cookie is missing")
    
    print(f"Session ID from cookie: {session_id}")
    result = usecase.execute(
        session_id=session_id
    )

    response.set_cookie(
        key="ev_auth_session_id",
        value=result.session_id.value,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=result.refresh_token_expiry - int(time()),
        path="/"
    )

    return result.json()