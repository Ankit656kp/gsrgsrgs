from datetime import datetime

async def log_action(db, user_id, action, details=None):
    log_entry = {
        "user_id": user_id,
        "action": action,
        "details": details,
        "timestamp": datetime.utcnow()
    }
    await db.logs.insert_one(log_entry)

async def get_user_logs(db, user_id, limit=20):
    return db.logs.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)

async def get_all_logs(db, limit=100):
    return db.logs.find().sort("timestamp", -1).limit(limit)