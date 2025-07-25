import logging
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI, MONGO_DB_NAME
from pyrogram.types import Message
import os

# Logging setup
logging.basicConfig(leveimport logging
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI, MONGO_DB_NAME

import os
import asyncio

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot initialization
app = Client(
    "DevilOSINTBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# MongoDB initialization
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client[MONGO_DB_NAME]

# Attach DB to client for global use
app.db = db

# START command (basic response)
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message: Message):
    user = message.from_user
    await message.reply_text(f"👋 Hello {user.first_name}!\nWelcome to Devil OSINT Bot.")
    
    # Log to group if LOG_CHANNEL is set
    try:
        from config import LOG_CHANNEL
        await client.send_message(
            LOG_CHANNEL,
            f"📥 New /start by [{user.first_name}](tg://user?id={user.id}) (`{user.id}`)"
        )
    except Exception as e:
        logger.warning(f"Log send failed: {e}")

# IMPORT ALL HANDLERS
def import_handlers():
    try:
        import handlers.start
        import handlers.commands
        import handlers.admin
        import handlers.forcejoin
        import handlers.admin_commands
        logger.info("✅ All handlers imported successfully.")
    except Exception as e:
        logger.error(f"❌ Handler import failed: {e}")

if __name__ == "__main__":
    logger.info("🚀 Starting Devil OSINT Bot...")
    import_handlers()
    app.run()l=logging.INFO)
logger = logging.getLogger(__name__)

# Bot initialization
app = Client(
    "DevilOSINTBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# MongoDB initialization
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client[MONGO_DB_NAME]

# Attach DB to client for global use
app.db = db

# Startup log
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message: Message):
    user = message.from_user
    await message.reply_text(f"👋 Hello {user.first_name}!\nWelcome to Devil OSINT Bot.")
    
    # Log to group if LOG_CHANNEL is set
    try:
        from config import LOG_CHANNEL
        await client.send_message(
    app.run()
