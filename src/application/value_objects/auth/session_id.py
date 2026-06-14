import secrets

class Id():
    def __init__(self, value: str = secrets.token_urlsafe(32)):
        self.value = value
        if not self.is_valid():
            raise ValueError("Invalid Id")
    
    def is_valid(self) -> bool:
        return isinstance(self.value, str) and len(self.value) > 0