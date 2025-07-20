import datetime

async def create_redeem_code(db, code: str, credits: int, created_by: int):
    await db.redeem.insert_one({
        "_id": code,
        "credits": credits,
        "used_by": None,
        "created_by": created_by,
        "created_at": datetime.datetime.utcnow()
    })

async def redeem_code(db, code: str, user_id: int):
    redeem = await db.redeem.find_one({"_id": code})
    if not redeem or redeem.get("used_by"):
        return False, "Invalid or already used code"

    # Mark as used
    await db.redeem.update_one(
        {"_id": code},
        {"$set": {"used_by": user_id}}
    )

    # Add credits
    await db.users.update_one(
        {"_id": user_id},
        {"$inc": {"credits": redeem["credits"]}}
    )
    return True, redeem["credits"]

async def get_all_redeem_codes(db):
    codes = db.redeem.find({})
    return [code async for code in codes]