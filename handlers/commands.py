@app.on_message(filters.command("upi") & filters.private)
async def upi_search(client, message):
    from modules.upi_info import upi_info_lookup
    await upi_info_lookup(client, message)
@app.on_message(filters.command("number") & filters.private)
async def number_search(client, message):
    from modules.number_info import number_info_lookup
    await number_info_lookup(client, message)
@app.on_message(filters.command("redeem") & filters.private)
async def redeem_handler(client, message):
    from modules.redeem import redeem_code
    await redeem_code(client, message)
@app.on_message(filters.command("refer") & filters.private)
async def refer_handler(client, message):
    from modules.refer import show_referral_info
    await show_referral_info(client, message)
@app.on_message(filters.command("buycredits") & filters.private)
async def buycredits_handler(client, message):
    from modules.buycredits import show_credit_plans
    await show_credit_plans(client, message)
@app.on_message(filters.command("stats") & filters.private)
async def stats_handler(client, message):
    from modules.stats import show_user_stats
    await show_user_stats(client, message)
@app.on_message(filters.command("addcredits") & filters.private)
async def handle_addcredits(client, message):
    from admin.addcredits import admin_add_credits
    await admin_add_credits(client, message)
@app.on_message(filters.command("number") & filters.private)
async def handle_number(client, message):
    from modules.number_info import number_info_lookup
    await number_info_lookup(client, message)
@app.on_message(filters.command("aadhaar") & filters.private)
async def handle_aadhaar(client, message):
    from modules.aadhaar_info import aadhaar_info_lookup
    await aadhaar_info_lookup(client, message)
@app.on_message(filters.command("fampay") & filters.private)
async def handle_fampay(client, message):
    from modules.fampay_info import fampay_lookup
    await fampay_lookup(client, message)
@app.on_message(filters.command("vehicle") & filters.private)
async def handle_vehicle(client, message):
    from modules.vehicle_info import vehicle_info_lookup
    await vehicle_info_lookup(client, message)
@app.on_message(filters.command("numberfb") & filters.private)
async def handle_numberfb(client, message):
    from modules.facebook import number_to_facebook_lookup
    await number_to_facebook_lookup(client, message)
@app.on_message(filters.command("pan") & filters.private)
async def handle_pan(client, message):
    from modules.pan import pan_info_lookup
    await pan_info_lookup(client, message)
@app.on_message(filters.command("numberupi") & filters.private)
async def handle_numberupi(client, message):
    from modules.numberupi import number_to_upi_lookup
    await number_to_upi_lookup(client, message)
@app.on_message(filters.command("ration") & filters.private)
async def handle_ration(client, message):
    from modules.ration_info import ration_card_lookup
    await ration_card_lookup(client, message)