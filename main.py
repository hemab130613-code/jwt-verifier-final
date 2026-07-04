from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import jwt

app = FastAPI()

PUBLIC_KEY = """
PASTE THE PUBLIC KEY HERE EXACTLY AS GIVEN
"""

ISSUER = "https://idp.exam.local"
AUDIENCE = "tds-o5hh1tel.apps.exam.local"

class TokenRequest(BaseModel):
    token: str

@app.post("/verify")
def verify_token(req: TokenRequest):
    try:
        payload = jwt.decode(
            req.token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=ISSUER,
        )

        return {
            "valid": True,
            "email": payload.get("email"),
            "sub": payload.get("sub"),
            "aud": payload.get("aud"),
        }

    except Exception:
        return JSONResponse(
            status_code=401,
            content={"valid": False}
        )