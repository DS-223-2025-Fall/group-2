import os
from dotenv import load_dotenv

# Load .env if it exists
load_dotenv()

# Get variables from environment (OS env first, .env fallback)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")