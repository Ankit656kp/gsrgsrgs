from datetime import datetime

async def log_user_action(
    db,
    user_id: int,
    feature: str,
    query: str,
    username: str = "N/A",
    result_text: str = None
):
    log_entry = {
        "user_id": user_id,
        "username": username,
        "feature": feature,
        "query": query,
        "result": result_text or "✅ Searched",
        "timestamp": datetime.utcnow()
    }
    await db.logs.insert_one(log_entry)

    # Optional: Also store inside user's own log (inside users collection)
    await db.users.update_one(
        {"_id": user_id},
        {
            "$push": {
                "search_log": {
                    "type": feature,
                    "query": query,
                    "result": result_text or "✅ Searched",
                    "time": datetime.utcnow()
                }
            }
        }
    )