from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID

async def admin_help_panel(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("🚫 You're not authorized.")

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Broadcast", switch_inline_query_current_chat="/broadcast ")],
        [InlineKeyboardButton("💳 Add Credits", switch_inline_query_current_chat="/addcredits ")],
        [InlineKeyboardButton("🛡️ Make Premium", switch_inline_query_current_chat="/makepremium ")],
        [InlineKeyboardButton("🎁 Generate Code", switch_inline_query_current_chat="/gencode ")],
        [InlineKeyboardButton("📤 Upload Dataset", switch_inline_query_current_chat="/upload")],
        [InlineKeyboardButton("📕 View Logs", switch_inline_query_current_chat="/log")],
        [InlineKeyboardButton("👥 View Users", switch_inline_query_current_chat="/users")],
        [InlineKeyboardButton("🆓 Free Access", switch_inline_query_current_chat="/free ")]
    ])

    await message.reply(
        "📋 **Devil OSINT Admin Panel**\n\nChoose any admin command below:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )