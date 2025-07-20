from pyrogram.types import Message
from config import OWNER_ID

async def admin_add_credits(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("🚫 You're not authorized.")

    args = message.text.split()
    if len(args) != 3:
        return await message.reply("❌ Usage:\n`/addcredits <user_id> <amount>`", parse_mode="Markdown")

    try:
        user_id = int(args[1])
        amount = int(args[2])
    except:
        return await message.reply("⚠️ Invalid user ID or amount.")

    db = client.db
    user = await db.users.find_one({"_id": user_id})
    if not user:
        return await message.reply("🚫 User not found.")

    await db.users.update_one({"_id": user_id}, {"$inc": {"credits": amount}})

    await message.reply(f"✅ Added `{amount}` credits to user `{user_id}`.", parse_mode="Markdown")

    # Optional: Notify user
    try:
        await client.send_message(user_id, f"💳 *{amount} credits* added to your account by admin!", parse_mode="Markdown")
    except:
        pass