import datetime

async def add_user(db, user_id: int, name: str, username: str, referrer_id: int = None):
    user = await db.users.find_one({"_id": user_id})
    if user:
        return

    data = {
        "_id": user_id,
        "name": name,
        "username": username,
        "credits": 2,  # Trial credits
        "referred_by": referrer_id,
        "referrals": 0,
        "joined_at": datetime.datetime.utcnow()
    }

    await db.users.insert_one(data)

    # Give referrer bonus if valid
    if referrer_id:
        await db.users.update_one(
            {"_id": referrer_id},
            {"$inc": {"credits": 2, "referrals": 1}}
        )

async def get_user(db, user_id: int):
    return await db.users.find_one({"_id": user_id})

async def update_credits(db, user_id: int, amount: int):
    await db.users.update_one({"_id": user_id}, {"$inc": {"credits": amount}})

async def get_all_users(db):
    users = db.users.find({})
    return [u async for u in users]

async def get_user_profile(db, user_id: int):
    user = await db.users.find_one({"_id": user_id})
    if not user:
        return None
    return {
        "name": user.get("name"),
        "username": user.get("username"),
        "credits": user.get("credits", 0),
        "referrals": user.get("referrals", 0),
        "referred_by": user.get("referred_by")
    }