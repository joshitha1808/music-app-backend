from fastapi import HTTPException, Header
import jwt


def auth_middleware(x_auth_token=Header()):
    try:
        # 1. Check for token 
        if not x_auth_token:
            raise HTTPException(401, 'No auth token, access denied!')
        # 2. Decode the token (Logic must be inside 'try')
        verified_token = jwt.decode(x_auth_token, 'password_key', ['HS256'])

        if not verified_token:
            raise HTTPException(401, 'Token verification failed, authorization')

        # 3. Get the id from the token
        uid = verified_token.get('id')
        return {'uid':uid,'token':x_auth_token}
    
    #postgress database get the user info 
    except jwt.PyJWTError:
        # This catches errors like expired or fake tokens
        raise HTTPException(401, 'Token is not valid, authorization failed')

