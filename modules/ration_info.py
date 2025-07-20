from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.users import get_user, is_premium
from utils.logger import log_user_action
from config import LOG_CHANNEL
from datetime import datetime

CREDIT_COST = 1

async def ration_card_lookup(client, message: Message):
    user_id = message.from_user.id
    db = client.db

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("❌ Usage:\n`/ration CARD123456789`", parse_mode="Markdown")

    card_number = args[1].strip().upper()
    if len(card_number) < 5:
        return await message.reply("❌ Invalid Ration Card format.", parse_mode="Markdown")

    user = await get_user(db, user_id)

    if not await is_premium(user):
        if user.get("credits", 0) < CREDIT_COST:
            return await message.reply(
                "🚫 Not enough credits. Ration card lookup needs 1 credit.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💳 Buy Credits", callback_data="buy_credits")]
                ]),
                parse_mode="Markdown"
            )
        await db.users.update_one({"_id": user_id}, {"$inc": {"credits": -CREDIT_COST}})

    result = f"""✅ *Ration Card Info:*

🪪 Card Number: `{card_number}`
👨‍👩‍👧 Head: Shyam Lal
🏠 Address: Ward 12, Siwan, Bihar
🍚 Members: 5
📜 Type: BPL
🗓️ Issued: 2015

(_Note: This is a demo. Real API or dataset logic will be integrated._)
"""

    await message.reply(result, parse_mode="Markdown")

    await log_user_action(
        db=db,
        user_id=user_id,
        username=message.from_user.username or "N/A",
        feature="ration",
        query=card_number,
        result_text=result
    )

    try:
        uname = f"@{message.from_user.username}" if message.from_user.username else "N/A"
        await client.send_message(LOG_CHANNEL,
            f"📜 *Ration Card Lookup*\n👤 User: `{user_id}` ({uname})\n📄 Card: `{card_number}`",
            parse_mode="Markdown"
        )
    except:
        pass