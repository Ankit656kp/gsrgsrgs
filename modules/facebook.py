from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.users import get_user, is_premium
from utils.logger import log_user_action
from config import LOG_CHANNEL
from datetime import datetime
import re

CREDIT_COST = 10

async def number_to_facebook_lookup(client, message: Message):
    user_id = message.from_user.id
    db = client.db

    # 📥 Input validation
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("❌ Usage:\n`/numberfb 9876543210`", parse_mode="Markdown")

    number = re.sub(r'\D', '', args[1])
    if len(number) != 10:
        return await message.reply("❌ Invalid number. Please enter a 10-digit mobile number.", parse_mode="Markdown")

    # 🔐 User info
    user = await get_user(db, user_id)

    # 💳 Credit check
    if not await is_premium(user):
        if user.get("credits", 0) < CREDIT_COST:
            return await message.reply(
                "🚫 You don't have enough credits.\n🔎 *Facebook Lookup* needs 10 credits.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💰 Buy Credits", callback_data="buy_credits")]
                ]),
                parse_mode="Markdown"
            )
        await db.users.update_one({"_id": user_id}, {"$inc": {"credits": -CREDIT_COST}})

    # 🔍 MOCK RESULT
    result = f"""✅ *Facebook Profile Found:*

📱 Mobile: `{number}`
👤 Name: Ramesh Kumar
📸 Profile: [Click Here](https://facebook.com/ramesh.kumar.fake)
🗓️ Last Active: 2 days ago
🌐 Friends Count: 248
📝 Bio: "Engineer | Traveler | Dreamer"

(_Note: This is a demo output. Real dataset/API logic will be integrated._)
"""

    await message.reply(result, parse_mode="Markdown", disable_web_page_preview=True)

    # 📝 Log the search
    await log_user_action(
        db=db,
        user_id=user_id,
        username=message.from_user.username or "N/A",
        feature="facebook",
        query=number,
        result_text=result
    )

    # 🔐 Log group notification
    try:
        uname = f"@{message.from_user.username}" if message.from_user.username else "N/A"
        await client.send_message(LOG_CHANNEL,
            f"🔍 *Facebook Lookup*\n👤 User: `{user_id}` ({uname})\n📱 Number: `{number}`",
            parse_mode="Markdown"
        )
    except:
        pass