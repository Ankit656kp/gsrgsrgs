from pyrogram.types import Message
from config import OWNER_ID
from database.users import get_all_users
import asyncio

async def admin_broadcast(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("🚫 You're not authorized.")

    text = message.text.split(maxsplit=1)
    if len(text) != 2:
        return await message.reply("❌ Usage:\n`/broadcast Your message here...`", parse_mode="Markdown")

    broadcast_text = text[1]
    sent, failed = 0, 0

    async for user in get_all_users(client.db):
        try:
            await client.send_message(user["_id"], broadcast_text)
            sent += 1
        except:
            failed += 1
        await asyncio.sleep(0.1)

    await message.reply(f"📢 Broadcast Done\n✅ Sent: {sent}\n❌ Failed: {failed}")