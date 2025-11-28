import os
from dotenv import load_dotenv

# Load .env if it exists
load_dotenv()

# Get variables from environment (OS env first, .env fallback)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")

# DS Service URL - defaults to docker service name, can be overridden
DS_SERVICE_URL = os.getenv("DS_SERVICE_URL", "http://ds_service:8001")
CALLBACK_URL = os.getenv("CALLBACK_URL")