from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from handlers.forcejoin import is_user_joined, force_join_prompt
from database.users import add_or_update_user, get_user
from config import OWNER_ID, LOG_CHANNEL
from utils.credits import get_user, update_username
import asyncio

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    user = message.from_user
    user_id = user.id
    name = user.first_name or "NoName"
    username = user.username or "N/A"

    # 🔒 Force Join Check
    if not await is_user_joined(client, user_id):
        return await force_join_prompt(client, message)

    # 🔗 Referral ID (if passed in /start command)
    ref_id = None
    if len(message.command) > 1:
        ref_arg = message.command[1]
        if ref_arg.isdigit() and int(ref_arg) != user_id:
            ref_id = int(ref_arg)

    # ➕ Add user to DB (or update)
    await add_or_update_user(client.db, user_id, name, username, ref_id)

    # 🎯 Fetch user profile
    user_data = await get_user(client.db, user_id)
    credits = user_data.get("credits", 0)
    ref_count = user_data.get("ref_count", 0)

    # 📊 Profile Card
    text = f"""🟩 *BLACKHAT CYBER INFO* 🟩

👤 *User:* {name}
📛 *Username:* @{username}
🆔 *ID:* `{user_id}`
💳 *Credits:* `{credits}`
👥 *Referrals:* `{ref_count}`
✅ *Status:* {"PREMIUM ✅" if await is_premium(user_data) else "FREE 🔓"}

👨‍💻 *Bot Owner:* @your_owner_username
"""

    # 🔘 UI Buttons
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📱 NUMBER INFO", callback_data="number_info"),
         InlineKeyboardButton("🆔 Aadhaar Info", callback_data="aadhaar_info")],
        [InlineKeyboardButton("🚘 Car Info", callback_data="vehicle_info"),
         InlineKeyboardButton("🏦 UPI Info", callback_data="upi_info")],
        [InlineKeyboardButton("📜 Ration Info", callback_data="ration_info"),
         InlineKeyboardButton("🔗 UPI ↔ Number", callback_data="upi_link")],
        [InlineKeyboardButton("🧑‍🤝‍🧑 Refer & Earn", callback_data="refer"),
         InlineKeyboardButton("🎁 Redeem Code", callback_data="redeem")],
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/yourchannel")]
    ])

    await message.reply_text(text, reply_markup=buttons, disable_web_page_preview=True, parse_mode="Markdown")

    # 📝 Send log to log group
    try:
        await client.send_message(
            LOG_CHANNEL,
            f"👤 New user started:\n• Name: {name}\n• ID: `{user_id}`\n• Username: @{username}"
        )
    except Exception as e:
        print(f"[LogError] {e}")