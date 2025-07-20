from pyrogram.types import Message
from database.users import get_user
from datetime import datetime

async def show_user_stats(client, message: Message):
    user_id = message.from_user.id
    user = await get_user(client.db, user_id)

    credits = user.get("credits", 0)
    ref_count = user.get("ref_count", 0)
    plan_expiry = user.get("plan_expiry")
    is_premium = user.get("is_premium", False)

    if is_premium and plan_expiry:
        expiry_str = plan_expiry.strftime("%d %b %Y")
        plan = f"🟢 Premium (valid till {expiry_str})"
    else:
        plan = "🔴 Free Plan"

    referral_link = f"https://t.me/{client.me.username}?start={user_id}"

    text = f"""📊 *Your Account Stats*

👤 *User ID:* `{user_id}`
💳 *Credits:* `{credits}`
🛡️ *Plan:* {plan}
👥 *Referrals:* `{ref_count}`

🔗 *Referral Link:*
`{referral_link}`

💡 Share this to earn credits!
"""

    await message.reply(text, parse_mode="Markdown")