from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

async def show_credit_plans(client, message: Message):
    text = """💳 *Recharge & Access Plans*

🔍 1 Credit = 1 Search (Number, Aadhaar, Ration)
🔍 5 Credits = 1 UPI Search
🔍 10 Credits = Fampay, Facebook Search

⚡️ *Credit Packs:*
💰 ₹100 = 3 Credits  
💰 ₹200 = 6 Credits  
💰 ₹300 = 15 Credits  
💰 ₹500 = 25 Credits  
💰 ₹1000 = 80 Credits  

🔓 *Unlimited Plans:*
🗓 7 Days – ₹1500  
🗓 15 Days – ₹2000  
🗓 30 Days – ₹3000  
🗓 1 Year – ₹10,000  

💬 To Recharge: Contact @YourAdminUsername"""

    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 Contact Admin", url="https://t.me/YourAdminUsername")],
        [InlineKeyboardButton("🎁 Redeem Code", callback_data="redeem"),
         InlineKeyboardButton("📖 How to Use", callback_data="howtouse")]
    ])

    await message.reply(text, reply_markup=btn, parse_mode="Markdown")