from pyrogram.types import Message
from database.users import get_user
from datetime import datetime, timedelta

async def redeem_code(client, message: Message):
    user_id = message.from_user.id
    db = client.db

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("❌ Please enter a code like:\n`/redeem ABC123`", parse_mode="Markdown")

    code = args[1].strip().upper()

    # 🔎 Search in redeem_codes
    redeem_data = await db.redeem_codes.find_one({"code": code})
    if not redeem_data:
        return await message.reply("🚫 Invalid or already used code.")

    # ✅ Apply reward
    if redeem_data.get("credits"):
        await db.users.update_one(
            {"_id": user_id},
            {"$inc": {"credits": redeem_data["credits"]}}
        )
        result = f"✅ You got *{redeem_data['credits']} credits!* 🎉"
    
    elif redeem_data.get("days"):
        expiry = datetime.utcnow() + timedelta(days=redeem_data["days"])
        await db.users.update_one(
            {"_id": user_id},
            {"$set": {
                "is_premium": True,
                "plan_expiry": expiry
            }}
        )
        result = f"✅ You got *{redeem_data['days']} days premium access!* 🔓"

    else:
        return await message.reply("⚠️ Code format is broken. Contact admin.")

    # 🗑 Delete or mark code as used
    await db.redeem_codes.delete_one({"code": code})

    await message.reply(result, parse_mode="Markdown")

    # 📝 Log
    from config import LOG_CHANNEL
    try:
        await client.send_message(LOG_CHANNEL, f"🎁 *Code Redeemed*\nUser: `{user_id}`\nCode: `{code}`\n{result}", parse_mode="Markdown")
    except: pass