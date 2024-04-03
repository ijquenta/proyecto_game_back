from datetime import datetime, timedelta
import os
import jwt

class TokenGenerator:
    @staticmethod
    def encode_token(user_id, user_rol):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1,minutes=0,seconds=0),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'rol': user_rol 
        }
        token = jwt.encode(payload, os.environ.get("APP_SECRET_KEY"), algorithm='HS256')
        return token.decode('utf-8')

    @staticmethod
    def decode_token(token):
        """_summary_

        Args:
            token (_type_): _description_
            It takes a token, decodes it, and returns the decoded token
            :param token: The token to decode
        """
        return jwt.decode(
            token,
            os.environ.get("APP_SECRET_KEY"),
            algorithms="HS256",
            options={"required_exp": True}
        )
    
    @staticmethod
    def check_token(token):
        """
        It takes a token, and returns True if the token is valid, and False if it's not
        
        :param token: The token to be decoded
        :return: A boolean value.
        """
        try:
            jwt.decode(
                token,
                os.environ.get("APP_SECRET_KEY"),
                algorithms="HS256",
                options={"require_exp": True},
            )
            return True
        except:
            return False 
        
token_generetor = TokenGenerator()