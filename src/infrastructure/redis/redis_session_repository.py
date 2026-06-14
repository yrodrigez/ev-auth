import json
import time

from redis import Redis

from src.application.entities.auth.session import Session
from src.application.value_objects.auth.session_id import Id as SessionId
from src.application.ports.session_repository_port import SessionRepositoryPort


class RedisSessionRepository(SessionRepositoryPort):
    def __init__(self, client: Redis) -> None:
        self.client = client

    def create_session(
        self,
        session: Session
    ) -> None:
        session_dict = {
            "session_id": session.session_id.value,
            "user_id": session.user_id,
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "access_token_expiry": session.access_token_expiry,
            "refresh_token_expiry": session.refresh_token_expiry
        }

        ttl = session.refresh_token_expiry - int(time.time())

        if ttl <= 0:
            raise ValueError("refresh_token_expiry must be in the future")

        self.client.set(
            name=self._get_session_key(session.session_id.value),
            ex=ttl,
            value=json.dumps(session_dict)
        )

    def get_session(self, session_id: str) -> Session | None:
        raw_session = self.client.get(
            self._get_session_key(session_id)
        )

        if raw_session is None:
            return None

        session_data = json.loads(raw_session)
        return Session(
            session_id=SessionId(session_data["session_id"]),
            user_id=session_data["user_id"],
            access_token=session_data["access_token"],
            refresh_token=session_data["refresh_token"],
            access_token_expiry=session_data["access_token_expiry"],
            refresh_token_expiry=session_data["refresh_token_expiry"]
        )

    def delete_session(self, session_id: str) -> None:
        self.client.delete(
            self._get_session_key(session_id)
        )

    def _get_session_key(self, session_id: str) -> str:
        return f"session:{session_id}"