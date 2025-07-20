from pyrogram.types import Message
from config import OWNER_ID

async def admin_list_users(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("🚫 You're not authorized.")

    users = await client.db.users.find().to_list(length=10000)
    if not users:
        return await message.reply("❌ No users found.")

    text = f"👥 *Total Users:* {len(users)}\n\n"
    for user in users:
        uid = user['_id']
        uname = f"@{user.get('username')}" if user.get('username') else "N/A"
        credits = user.get('credits', 0)
        premium = "✅" if user.get("is_premium") else "❌"
        text += f"🆔 `{uid}` | {uname} | 💳 `{credits}` | Premium: {premium}\n"

    if len(text) > 4096:
        # If too long, send as document
        from io import BytesIO
        bio = BytesIO()
        bio.write(text.encode('utf-8'))
        bio.name = "users.txt"
        bio.seek(0)
        await message.reply_document(document=bio, caption="📋 User List")
    else:
        await message.reply(text, parse_mode="Markdown")