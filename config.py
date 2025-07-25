import os
from dotenv import load_dotenv

load_dotenv()  # Only used in local environment (Heroku sets env automatically)

API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

OWNER_ID = int(os.getenv("OWNER_ID", "123456789"))
FORCE_JOIN = os.getenv("FORCE_JOIN", "")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1001234567890"))

MONGO_URI = os.getenv("MONGO_URI", "")
MONGO_DB_NAME = "devil_osint"
