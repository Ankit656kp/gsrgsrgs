@app.on_message(filters.command("makepremium") & filters.private)
async def handle_makepremium(client, message):
    from admin.makepremium import admin_make_premium
    await admin_make_premium(client, message)
@app.on_message(filters.command("gencode") & filters.private)
async def handle_gencode(client, message):
    from admin.gencode import admin_generate_code
    await admin_generate_code(client, message)
@app.on_message(filters.command("upload") & filters.private & filters.document)
async def handle_upload(client, message):
    from admin.upload import admin_upload_dataset
    await admin_upload_dataset(client, message)
@app.on_message(filters.command("broadcast") & filters.private)
async def handle_broadcast(client, message):
    from admin.broadcast import admin_broadcast
    await admin_broadcast(client, message)
@app.on_message(filters.command("log") & filters.private)
async def handle_log(client, message):
    from admin.log import admin_export_logs
    await admin_export_logs(client, message)
@app.on_message(filters.command("users") & filters.private)
async def handle_users(client, message):
    from admin.users import admin_list_users
    await admin_list_users(client, message)
@app.on_message(filters.command("free") & filters.private)
async def handle_free(client, message):
    from admin.free import admin_free_access
    await admin_free_access(client, message)
@app.on_message(filters.command("ahelp") & filters.private)
async def handle_ahelp(client, message):
    from admin.ahelp import admin_help_panel
    await admin_help_panel(client, message)