from abc import ABC, abstractmethod

from src.application.entities.auth.session import Session

class SessionRepositoryPort(ABC):
    @abstractmethod
    def create_session(
        self,
        session: Session
    ) -> None:
        pass

    @abstractmethod
    def get_session(self, session_id: str) -> Session | None:
        pass

    @abstractmethod
    def delete_session(self, session_id: str) -> None:
        pass