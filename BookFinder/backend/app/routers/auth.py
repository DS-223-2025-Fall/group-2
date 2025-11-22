from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from core.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, API_SECRET_KEY
from datetime import datetime, timedelta, timezone
from jose import jwt

router = APIRouter(prefix="/auth", tags=["Auth"])

# Initialize OAuth
oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    api_base_url="https://www.googleapis.com/oauth2/v2/",
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/google")
async def login_via_google(request: Request):
    redirect_uri = request.url_for("auth_google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def auth_google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.get("userinfo", token=token)
    user = user_info.json()

    payload = {
        "sub": user["email"],
        "name": user.get("name"),
        "exp": datetime.now(timezone.utc) + timedelta(days=1),
    }
    jwt_token = jwt.encode(payload, API_SECRET_KEY, algorithm="HS256")

    frontend_url = "http://localhost:8501"  # or env var

    # Redirect to frontend with token, email, and name
    from urllib.parse import quote
    return RedirectResponse(
        url=f"{frontend_url}?token={jwt_token}&email={quote(user['email'])}&name={quote(user.get('name', ''))}"
    )
