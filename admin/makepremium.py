from pyrogram.types import Message
from config import OWNER_ID
from datetime import datetime, timedelta

async def admin_make_premium(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("🚫 You're not authorized.")

    args = message.text.split()
    if len(args) != 3:
        return await message.reply("❌ Usage:\n`/makepremium <user_id> <days>`", parse_mode="Markdown")

    try:
        user_id = int(args[1])
        days = int(args[2])
    except:
        return await message.reply("⚠️ Invalid user ID or days.")

    db = client.db
    user = await db.users.find_one({"_id": user_id})
    if not user:
        return await message.reply("🚫 User not found.")

    expiry = datetime.utcnow() + timedelta(days=days)

    await db.users.update_one(
        {"_id": user_id},
        {
            "$set": {
                "is_premium": True,
                "plan_expiry": expiry
            }
        }
    )

    await message.reply(f"✅ Premium access given to `{user_id}` for `{days}` days.", parse_mode="Markdown")

    try:
        await client.send_message(user_id, f"🎉 You are now a *Premium User* for {days} days! 🔓", parse_mode="Markdown")
    except:
        pass