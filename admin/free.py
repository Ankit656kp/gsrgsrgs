from pyrogram.types import Message
from config import OWNER_ID
from datetime import datetime, timedelta

async def admin_free_access(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("🚫 You're not authorized.")

    args = message.text.split()
    if len(args) != 2:
        return await message.reply("❌ Usage:\n`/free <days>`", parse_mode="Markdown")

    try:
        days = int(args[1])
    except:
        return await message.reply("⚠️ Invalid number of days.")

    expiry = datetime.utcnow() + timedelta(days=days)

    await client.db.users.update_many(
        {},
        {"$set": {
            "is_premium": True,
            "plan_expiry": expiry
        }}
    )

    await message.reply(f"✅ All users granted free premium for `{days}` days!", parse_mode="Markdown")