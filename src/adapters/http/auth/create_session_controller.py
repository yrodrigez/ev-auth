from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel

from src.infrastructure.redis.redis_client import get_redis_client
from src.infrastructure.redis.redis_session_repository import RedisSessionRepository
from src.application.usecases.create_session_usecase import CreateSessionUseCase

router = APIRouter()

def build_create_session_usecase() -> CreateSessionUseCase:
    redis_client = get_redis_client()
    session_repository = RedisSessionRepository(client=redis_client)

    return CreateSessionUseCase(
        session_repository=session_repository
    )

class CreateSessionRequest(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    access_token_expiry: int
    refresh_token_expiry: int


@router.post("/sessions")
def create_session(
    request: CreateSessionRequest,
    response: Response,
    usecase: CreateSessionUseCase = Depends(build_create_session_usecase)
):
    result = usecase.execute(
        user_id=request.user_id,
        access_token=request.access_token,
        refresh_token=request.refresh_token,
        access_token_expiry=request.access_token_expiry,
        refresh_token_expiry=request.refresh_token_expiry
    )

    response.set_cookie(
        key="ev_auth_session_id",
        value=result.session_id.value,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=result.max_age,
        path="/"
    )

    return {
        "success": True
    }