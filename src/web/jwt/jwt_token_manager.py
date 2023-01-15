import os
from datetime import datetime

import jwt
from dotenv import load_dotenv

from src.interfaces.token_manager import ITokenManager

load_dotenv()
    
jwt_secret = os.environ["JWT_SECRET_KEY"]

class JwtTokenManager(ITokenManager):

    def encode_token(self, payload: dict, exp: datetime = None, iat: datetime = None) -> str:
        try:
            if exp is not None:
                payload["exp"] = exp
            
            if iat is not None:
                payload["iat"] = iat

            return jwt.encode(payload, jwt_secret, algorithm="HS256")
        except Exception as e:
            error_msg = "Exception when calling JwtTokenManager.encode_token: %s\n" % e
            raise Exception(error_msg)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, jwt_secret, algorithms=["HS256"])
        except Exception as e:
            error_msg = "Exception when calling JwtTokenManager.decode_token: %s\n" % e
            raise Exception(error_msg)