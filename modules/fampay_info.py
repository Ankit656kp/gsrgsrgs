from pyrogram.types import Message
from database.users import get_user, is_premium
from utils.logger import log_user_action
from config import LOG_CHANNEL
from datetime import datetime

CREDIT_COST = 10

async def fampay_lookup(client, message: Message):
    user_id = message.from_user.id
    db = client.db

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("❌ Usage:\n`/fampay upiid@fampay`", parse_mode="Markdown")

    upi = args[1].strip().lower()
    if "@fampay" not in upi:
        return await message.reply("❌ Invalid Fampay UPI. Must end with `@fampay`.", parse_mode="Markdown")

    user = await get_user(db, user_id)

    # Check credits or premium
    if not await is_premium(user):
        if user.get("credits", 0) < CREDIT_COST:
            from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            return await message.reply(
                "🚫 Not enough credits. Fampay search costs 10 credits.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💵 Buy Credits", callback_data="buy_credits")]
                ]),
                parse_mode="Markdown"
            )
        await db.users.update_one({"_id": user_id}, {"$inc": {"credits": -CREDIT_COST}})

    # 🔍 Mock result
    result = f"""✅ *Fampay UPI → Mobile Number Result*

💳 UPI ID: `{upi}`
📱 Mobile Number: 7908940887
👤 Holder Name: Rishabh Singh
🏦 Bank: Fampay
🌍 Location: Bengaluru, Karnataka

(_Demo output shown. Actual API integration will go here._)
"""

    await message.reply(result, parse_mode="Markdown")

    await log_user_action(
        db=db,
        user_id=user_id,
        username=message.from_user.username or "N/A",
        feature="fampay",
        query=upi,
        result_text=result
    )

    try:
        uname = f"@{message.from_user.username}" if message.from_user.username else "N/A"
        await client.send_message(LOG_CHANNEL,
            f"🔍 *Fampay Lookup*\n👤 User: `{user_id}` ({uname})\n🔗 Query: `{upi}`",
            parse_mode="Markdown")
    except:
        pass