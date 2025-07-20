from pyrogram.types import Message
from database.users import get_user, is_premium
from utils.logger import log_user_action
from config import LOG_CHANNEL
from datetime import datetime
import re

CREDIT_COST = 1

async def vehicle_info_lookup(client, message: Message):
    user_id = message.from_user.id
    db = client.db

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("❌ Usage:\n`/vehicle BR01AB1234`", parse_mode="Markdown")

    reg_num = re.sub(r'\s+', '', args[1].upper())

    if not re.match(r'^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$', reg_num):
        return await message.reply("❌ Invalid vehicle number format.\nUse format like `BR01AB1234`", parse_mode="Markdown")

    user = await get_user(db, user_id)

    if not await is_premium(user):
        if user.get("credits", 0) < CREDIT_COST:
            from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            return await message.reply(
                "🚫 Not enough credits. Vehicle info costs 1 credit.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💵 Buy Credits", callback_data="buy_credits")]
                ]),
                parse_mode="Markdown"
            )
        await db.users.update_one({"_id": user_id}, {"$inc": {"credits": -CREDIT_COST}})

    # 🔍 MOCK RESULT
    result = f"""✅ *Vehicle Info Found*

🚘 Reg. No: `{reg_num}`
👤 Owner: Rishabh Kumar
🏠 Address: Patna, Bihar
🏍️ Vehicle: Hero Splendor Plus  
📅 Registration Date: 2020-05-13  
🛣️ RTO: Patna  
🆔 Chassis: MBLAHE205J2XXXXXX  
🔢 Engine: HE05J2XXXXX  
📄 Insurance: Active till 2025-04-30

(_Mock result. Real API or DB logic will be integrated later._)
"""

    await message.reply(result, parse_mode="Markdown")

    await log_user_action(
        db=db,
        user_id=user_id,
        username=message.from_user.username or "N/A",
        feature="vehicle",
        query=reg_num,
        result_text=result
    )

    try:
        uname = f"@{message.from_user.username}" if message.from_user.username else "N/A"
        await client.send_message(LOG_CHANNEL,
            f"🚗 *Vehicle Search*\n👤 User: `{user_id}` ({uname})\n🔎 Vehicle: `{reg_num}`",
            parse_mode="Markdown")
    except:
        pass