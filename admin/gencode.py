from pyrogram.types import Message
from config import OWNER_ID
import random
import string

def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

async def admin_generate_code(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("🚫 You're not authorized.")

    args = message.text.split()
    if len(args) != 3:
        return await message.reply("❌ Usage:\n`/gencode <credits> <days>`", parse_mode="Markdown")

    try:
        credits = int(args[1])
        days = int(args[2])
    except:
        return await message.reply("⚠️ Invalid values. Use numbers only.")

    if credits <= 0 and days <= 0:
        return await message.reply("⚠️ Either credits or days must be > 0.")

    code = generate_code()

    data = {"code": code}
    if credits > 0:
        data["credits"] = credits
    if days > 0:
        data["days"] = days

    await client.db.redeem_codes.insert_one(data)

    reply = f"✅ *New Redeem Code Generated*\n\n🎁 Code: `{code}`"
    if credits > 0:
        reply += f"\n💳 Credits: `{credits}`"
    if days > 0:
        reply += f"\n🛡️ Premium: `{days}` days"

    await message.reply(reply, parse_mode="Markdown")