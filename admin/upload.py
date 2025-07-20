from pyrogram.types import Message
from config import OWNER_ID
import os, csv, json
from io import BytesIO

async def admin_upload_dataset(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("🚫 You're not authorized.")

    if not message.document:
        return await message.reply("📎 Please upload a `.csv` or `.json` file with the command `/upload`.")

    file_name = message.document.file_name.lower()
    if not (file_name.endswith(".csv") or file_name.endswith(".json")):
        return await message.reply("❌ Only `.csv` or `.json` files supported.")

    file = await client.download_media(message.document)

    collection_name = file_name.split('.')[0]
    collection = client.db[collection_name]
    inserted_count = 0

    if file_name.endswith(".csv"):
        with open(file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
            if data:
                await collection.insert_many(data)
                inserted_count = len(data)

    elif file_name.endswith(".json"):
        with open(file, encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                await collection.insert_many(data)
                inserted_count = len(data)
            elif isinstance(data, dict):
                await collection.insert_one(data)
                inserted_count = 1

    os.remove(file)
    await message.reply(f"✅ Uploaded `{file_name}`\n📁 Collection: `{collection_name}`\n🔢 Records Inserted: `{inserted_count}`", parse_mode="Markdown")