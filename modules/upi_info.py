from pyrogram.types import Message
from database.users import get_user, is_premium
from datetime import datetime

async def upi_info_lookup(client, message: Message):
    user_id = message.from_user.id
    db = client.db

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("❌ Send UPI like: `/upi username@bank`", parse_mode="Markdown")

    upi = args[1].strip().lower()

    # ⚠️ Basic validation
    if not await is_premium(user_data):
    if user_data["credits"] < 5:
        from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        return await message.reply(
            "🚫 Not enough credits. UPI search costs 5 credits.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💵 Buy Credits", callback_data="buy_credits")]
            ]),
            parse_mode="Markdown"
        )

    user_data = await get_user(db, user_id)

    if not await is_premium(user_data):
        if user_data["credits"] < 5:
            return await message.reply("🚫 Not enough credits. UPI search needs 5 credits.", parse_mode="Markdown")
        await db.users.update_one({"_id": user_id}, {"$inc": {"credits": -5}})

    # 🔍 MOCK result (replace with real API logic later)
    result = f"""✅ *UPI Details Found:*

💳 *VPA:* `{upi}`
👤 *Name:* Sakhawat Hossain Biswas
📜 *IFSC Code:* NESF0000333

🏦 *Bank:* North East Small Finance Bank  
🏢 *Branch:* KORAMANGALA BRANCH  
📍 *Address:* 3rd Floor, Indiqube, Koramangala, Bengaluru  
🌍 *State:* Karnataka  
📞 *Contact:* +910000000000  
💳 *RTGS:* Yes  
💳 *NEFT:* Yes  
💳 *IMPS:* Yes  
💳 *UPI:* Yes
"""

    from utils.logger import log_user_action

await log_user_action(
    db=db,
    user_id=user_id,
    username=message.from_user.username or "N/A",
    feature="upi",
    query=upi,
    result_text=result
)