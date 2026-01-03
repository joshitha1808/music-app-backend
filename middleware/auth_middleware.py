from fastapi import Header, HTTPException
import jwt

def auth_middleware(x_auth_token: str = Header(...)):
    try:
        # 1. Check for token
        if not x_auth_token:
            raise HTTPException(
                status_code=401,
                detail="No auth token, access denied!"
            )

        # 2. Decode token
        verified_token = jwt.decode(
            x_auth_token,
            "password_key",
            algorithms=["HS256"]
        )

        # 3. Get user id
        uid = verified_token.get("id")
        if not uid:
            raise HTTPException(
                status_code=401,
                detail="Token verification failed"
            )

        return {
            "uid": uid,
            "token": x_auth_token
        }

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Token is not valid, authorization failed"
        )
