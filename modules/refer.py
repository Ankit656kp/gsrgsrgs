from pyrogram.types import Message
from database.users import get_user

async def show_referral_info(client, message: Message):
    user_id = message.from_user.id
    user = await get_user(client.db, user_id)

    referral_link = f"https://t.me/{client.me.username}?start={user_id}"
    ref_count = user.get("ref_count", 0)
    credits = user.get("credits", 0)

    text = f"""🧑‍🤝‍🧑 *Referral Program* 🎁

🎯 *Your Credits:* `{credits}`
👥 *Referrals:* `{ref_count}`

📲 *Your Referral Link:*
`{referral_link}`

🔹 Share this link with friends
🔹 You get 1 credit when they join!
🔹 They get 2 free trial credits

⚠️ Fake/duplicate referrals won't count.
"""

    await message.reply(text, parse_mode="Markdown")