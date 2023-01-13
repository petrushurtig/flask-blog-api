from datetime import datetime

class ITokenManager:
    def encode_token(self, payload: dict, exp: datetime = None, iat: datetime = None) -> str:
        raise NotImplementedError

    def decode_token(self, token: str) -> dict:
        raise NotImplementedError