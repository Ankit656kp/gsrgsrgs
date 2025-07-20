from pyrogram.types import Message
from database.users import get_user, is_premium
from utils.logger import log_user_action
from config import LOG_CHANNEL
from datetime import datetime
import re

CREDIT_COST = 1

async def number_info_lookup(client, message: Message):
    user_id = message.from_user.id
    db = client.db

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("❌ Please use:\n`/number 9876543210`", parse_mode="Markdown")

    number = re.sub(r'\D', '', args[1])
    if len(number) != 10:
        return await message.reply("❌ Invalid mobile number format.")

    user_data = await get_user(db, user_id)

    if not await is_premium(user_data):
        if user_data.get("credits", 0) < CREDIT_COST:
            return await message.reply("🚫 Not enough credits. Please recharge.", parse_mode="Markdown")
        await db.users.update_one({"_id": user_id}, {"$inc": {"credits": -CREDIT_COST}})

    # Demo result (no Aadhaar masking)
    result = f"""✅ *Result for* `{number}`:

👤 *Name:* Kundan Kumar
👴 *Father:* Shushankar Prasad
🏠 *Address:* Madhuban, East Champaran, Bihar
🔴 *Circle:* JIO BIHAR
🆔 *Aadhaar:* 774168242565
📲 *Alternate:* 7632010342

(_This is a demo result. Real API/dataset will be added here._)
"""

    await message.reply(result, parse_mode="Markdown")

    await log_user_action(
        db=db,
        user_id=user_id,
        username=message.from_user.username or "N/A",
        feature="number",
        query=number,
        result_text=result
    )

    try:
        uname = f"@{message.from_user.username}" if message.from_user.username else "N/A"
        log_msg = (
            f"🔍 *Number Lookup*\n"
            f"👤 User: `{user_id}` ({uname})\n"
            f"📲 Number: `{number}`\n"
            f"🕒 {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        await client.send_message(LOG_CHANNEL, log_msg, parse_mode="Markdown")
    except:
        pass