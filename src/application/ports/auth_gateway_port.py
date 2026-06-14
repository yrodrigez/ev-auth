from abc import ABC, abstractmethod
from typing_extensions import Literal
from typing import NotRequired, TypedDict


class RefreshAuthResponse(TypedDict):
    access_token: str
    refresh_token: str
    refresh_token_expiry: int
    access_token_expiry: int
    should_refresh_provider_token: bool
    provider: NotRequired[str | None]

class AuthGatewayPort(ABC):
    @abstractmethod 
    def refresh_token(self, refresh_token: str) -> RefreshAuthResponse:
        pass
