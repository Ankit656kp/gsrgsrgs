async def get_credits(db, user_id):
    user = await db.users.find_one({"_id": user_id})
    if user:
        return user.get("credits", 0)
    return 0

async def add_credits(db, user_id, amount):
    await db.users.update_one(
        {"_id": user_id},
        {"$inc": {"credits": amount}}
    )

async def deduct_credits(db, user_id, amount):
    user = await db.users.find_one({"_id": user_id})
    if user and user.get("credits", 0) >= amount:
        await db.users.update_one(
            {"_id": user_id},
            {"$inc": {"credits": -amount}}
        )
        return True
    return False

async def set_credits(db, user_id, amount):
    await db.users.update_one(
        {"_id": user_id},
        {"$set": {"credits": amount}}
    )