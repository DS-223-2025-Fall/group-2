from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from core.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, API_SECRET_KEY
from datetime import datetime, timedelta, timezone
from jose import jwt
from sqlalchemy.orm import Session
from db.postgres import get_db
from db.models import AppUser
from urllib.parse import quote
from core.config import CALLBACK_URL

router = APIRouter(prefix="/auth", tags=["Auth"])

# Initialize OAuth client for Google
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
async def login_via_google(request: Request) -> RedirectResponse:
    """
    Start Google OAuth login flow.

    This endpoint redirects the user to Google's authorization page.
    After successful login, Google redirects the user back to the
    `/google/callback` endpoint.

    Args:
        request (Request): Incoming HTTP request containing session info.

    Returns:
        RedirectResponse: Redirects the user to Google OAuth consent screen.
    """
    redirect_uri = request.url_for("auth_google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def auth_google_callback(request: Request, db: Session = Depends(get_db)) -> RedirectResponse:
    """
    Handle Google OAuth callback, authenticate the user, and return a JWT token.

    This endpoint:
    1. Exchanges the authorization code for an access token.
    2. Fetches the user's Google profile (email + name).
    3. Creates a database user if one does not already exist.
    4. Generates a JWT token valid for 24 hours.
    5. Redirects the user to the frontend callback URL with token and user details.

    Args:
        request (Request): Incoming request containing OAuth authorization response.
        db (Session): Database session dependency.

    Returns:
        RedirectResponse: Redirect to frontend with JWT, email, and name in query params.
    """
    # Retrieve access token from Google
    token = await oauth.google.authorize_access_token(request)

    # Fetch Google user info
    user_info = await oauth.google.get("userinfo", token=token)
    user = user_info.json()
    email = user["email"]
    name = user.get("name", "")

    # -------------------------
    # Create user in DB if not present
    # -------------------------
    db_user = db.query(AppUser).filter(AppUser.email == email).first()
    if not db_user:
        db_user = AppUser(email=email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    # -------------------------
    # Create JWT token
    # -------------------------
    payload = {
        "sub": email,
        "name": name,
        "exp": datetime.now(timezone.utc) + timedelta(days=1),
    }
    jwt_token = jwt.encode(payload, API_SECRET_KEY, algorithm="HS256")

    # Redirect to frontend callback URL with encoded details
    return RedirectResponse(
        url=f"{CALLBACK_URL}?token={jwt_token}&email={quote(email)}&name={quote(name)}"
    )
