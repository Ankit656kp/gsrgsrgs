from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import FORCE_JOIN
import asyncio

async def is_user_joined(client: Client, user_id: int) -> bool:
    try:
        member = await client.get_chat_member(FORCE_JOIN, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def force_join_prompt(client: Client, message):
    join_button = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("📢 Join Channel", url=FORCE_JOIN),
            InlineKeyboardButton("✅ Joined", callback_data="refresh_join")
        ]]
    )
    await message.reply_text(
        "**🔒 You must join our channel to use this bot.**",
        reply_markup=join_button,
        disable_web_page_preview=True
    )
    return