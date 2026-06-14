from src.application.value_objects.auth.session_id import Id as SessionId

class Session():
    def __init__(
        self,
        session_id: SessionId,
        user_id: str,
        access_token: str,
        refresh_token: str,
        access_token_expiry: int,
        refresh_token_expiry: int,
    ) -> None:
        self.session_id = session_id
        self.user_id = user_id
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.access_token_expiry = access_token_expiry
        self.refresh_token_expiry = refresh_token_expiry

    def json(self) -> dict:
        return {
            "session_id": self.session_id.value,
            "user_id": self.user_id,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "access_token_expiry": self.access_token_expiry,
            "refresh_token_expiry": self.refresh_token_expiry
        }