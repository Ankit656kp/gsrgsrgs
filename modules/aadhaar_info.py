from pyrogram.types import Message
from database.users import get_user, is_premium
from utils.logger import log_user_action
from config import LOG_CHANNEL
from datetime import datetime
import re

CREDIT_COST = 1

async def aadhaar_info_lookup(client, message: Message):
    user_id = message.from_user.id
    db = client.db

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("❌ Usage:\n`/aadhaar 123412341234`", parse_mode="Markdown")

    aadhaar = re.sub(r'\D', '', args[1])
    if len(aadhaar) != 12:
        return await message.reply("❌ Invalid Aadhaar number. Must be 12 digits.")

    user = await get_user(db, user_id)

    if not await is_premium(user):
        if user.get("credits", 0) < CREDIT_COST:
            return await message.reply("🚫 Not enough credits. Please recharge.", parse_mode="Markdown")
        await db.users.update_one({"_id": user_id}, {"$inc": {"credits": -CREDIT_COST}})

    # 🔍 MOCK Aadhaar info
    result = f"""📋 *Aadhaar Info Result*

🆔 Aadhaar: {aadhaar}
👤 Name: Ramesh Kumar
👴 Father's Name: Suresh Kumar
🏠 Address: Patna, Bihar, India
📞 Linked Mobile: 9876543210
📧 Email: Not Available

(_Demo result. Real API or dataset will be linked later._)
"""

    await message.reply(result, parse_mode="Markdown")

    await log_user_action(
        db=db,
        user_id=user_id,
        username=message.from_user.username or "N/A",
        feature="aadhaar",
        query=aadhaar,
        result_text=result
    )

    try:
        uname = f"@{message.from_user.username}" if message.from_user.username else "N/A"
        log_msg = (
            f"🔍 *Aadhaar Lookup*\n"
            f"👤 User: `{user_id}` ({uname})\n"
            f"🆔 Aadhaar: `{aadhaar}`\n"
            f"🕒 {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        await client.send_message(LOG_CHANNEL, log_msg, parse_mode="Markdown")
    except:
        pass