
from pytest import Session

from src.application.ports.session_repository_port import SessionRepositoryPort


class GetSessionUseCase:
    def __init__(self, session_repository: SessionRepositoryPort):
        self.session_repository = session_repository

    def execute(self, session_id: str) -> Session:
        session = self.session_repository.get_session(session_id)
        if not session:
            raise ValueError("Session not found")
        return session