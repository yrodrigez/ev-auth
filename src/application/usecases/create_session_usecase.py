# src/application/usecases/create_session_usecase.py

import secrets
import time
from dataclasses import dataclass

from src.application.entities.auth.session import Session
from src.application.value_objects.auth.session_id import Id as SessionId
from src.application.ports.session_repository_port import SessionRepositoryPort


@dataclass(frozen=True)
class CreateSessionResult:
    session_id: SessionId
    max_age: int


class CreateSessionUseCase:
    def __init__(self, session_repository: SessionRepositoryPort) -> None:
        self.session_repository = session_repository

    def execute(
        self,
        user_id: str,
        access_token: str,
        refresh_token: str,
        access_token_expiry: int,
        refresh_token_expiry: int
    ) -> CreateSessionResult:

        max_age = refresh_token_expiry - int(time.time())

        if max_age <= 0:
            raise ValueError("refresh_token_expiry must be in the future")
        
        session = Session(
            session_id=SessionId(),
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expiry=access_token_expiry,
            refresh_token_expiry=refresh_token_expiry
        )

        self.session_repository.create_session(
            session=session,
        )

        return CreateSessionResult(
            session_id=session.session_id,
            max_age=max_age
        )