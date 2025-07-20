from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.users import get_user, is_premium
from utils.logger import log_user_action
from config import LOG_CHANNEL
from datetime import datetime
import re

CREDIT_COST = 10

async def pan_info_lookup(client, message: Message):
    user_id = message.from_user.id
    db = client.db

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("❌ Usage:\n`/pan ABCDE1234F`", parse_mode="Markdown")

    pan = args[1].strip().upper()

    # 🔒 Validate PAN format
    if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan):
        return await message.reply("❌ Invalid PAN format.\nCorrect format: `ABCDE1234F`", parse_mode="Markdown")

    user = await get_user(db, user_id)

    if not await is_premium(user):
        if user.get("credits", 0) < CREDIT_COST:
            return await message.reply(
                "🚫 Not enough credits. PAN Lookup costs 10 credits.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💳 Buy Credits", callback_data="buy_credits")]
                ]),
                parse_mode="Markdown"
            )
        await db.users.update_one({"_id": user_id}, {"$inc": {"credits": -CREDIT_COST}})

    # 🧪 MOCK PAN RESULT
    result = f"""✅ *PAN Card Info:*

🆔 PAN: `{pan}`
👤 Name: Rajesh Kumar
📆 DOB: 15/07/1988
🧑‍💼 Status: Active
🏢 Linked Bank: HDFC Bank
📍 City: Patna
📞 Linked Mobile: 9876543210

(_Note: This is a placeholder. API or dataset logic will be added here._)
"""

    await message.reply(result, parse_mode="Markdown")

    await log_user_action(
        db=db,
        user_id=user_id,
        username=message.from_user.username or "N/A",
        feature="pan",
        query=pan,
        result_text=result
    )

    try:
        uname = f"@{message.from_user.username}" if message.from_user.username else "N/A"
        await client.send_message(LOG_CHANNEL,
            f"🔍 *PAN Lookup*\nUser: `{user_id}` ({uname})\nPAN: `{pan}`",
            parse_mode="Markdown"
        )
    except:
        pass