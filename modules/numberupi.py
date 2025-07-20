from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.users import get_user, is_premium
from utils.logger import log_user_action
from config import LOG_CHANNEL
from datetime import datetime
import re

CREDIT_COST = 1

async def number_to_upi_lookup(client, message: Message):
    user_id = message.from_user.id
    db = client.db

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("❌ Usage:\n`/numberupi 9876543210`", parse_mode="Markdown")

    number = re.sub(r'\D', '', args[1])
    if len(number) != 10:
        return await message.reply("❌ Invalid mobile number. Must be 10 digits.", parse_mode="Markdown")

    user = await get_user(db, user_id)

    if not await is_premium(user):
        if user.get("credits", 0) < CREDIT_COST:
            return await message.reply(
                "🚫 Not enough credits. This feature costs 1 credit.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💰 Buy Credits", callback_data="buy_credits")]
                ]),
                parse_mode="Markdown"
            )
        await db.users.update_one({"_id": user_id}, {"$inc": {"credits": -CREDIT_COST}})

    # 🔎 MOCK OUTPUT
    result = f"""✅ *UPI ID Found:*

📱 Mobile: `{number}`
💳 UPI ID: `{number}@upi`
👤 Name: Rahul Verma
🏛️ Bank: SBI Bank
📍 Location: New Delhi

(_This is a sample. Real logic will match with APIs/datasets._)
"""

    await message.reply(result, parse_mode="Markdown")

    # 🔍 Logging
    await log_user_action(
        db=db,
        user_id=user_id,
        username=message.from_user.username or "N/A",
        feature="number_to_upi",
        query=number,
        result_text=result
    )

    try:
        uname = f"@{message.from_user.username}" if message.from_user.username else "N/A"
        await client.send_message(LOG_CHANNEL,
            f"🔍 *Number → UPI Lookup*\nUser: `{user_id}` ({uname})\nNumber: `{number}`",
            parse_mode="Markdown"
        )
    except:
        pass