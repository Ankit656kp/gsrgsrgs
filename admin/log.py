from pyrogram.types import Message
from config import OWNER_ID
from fpdf import FPDF
from io import BytesIO

async def admin_export_logs(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("🚫 You're not authorized.")

    logs = await client.db.logs.find().to_list(length=5000)
    if not logs:
        return await message.reply("❌ No logs found.")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="📕 Devil OSINT Bot - User Logs", ln=True, align='C')
    pdf.ln(5)

    for log in logs:
        line = f"👤 {log.get('username', '-') or '-'} | 🆔 {log['user_id']} | 🔎 {log['feature']} | 📄 {log['query']} | ⏰ {log['timestamp'].strftime('%d-%b-%Y %H:%M')}"
        pdf.multi_cell(0, 7, txt=line)
        pdf.ln(1)

    output = BytesIO()
    pdf.output(output)
    output.seek(0)

    await client.send_document(
        chat_id=message.chat.id,
        document=output,
        file_name="DevilOSINT_Logs.pdf",
        caption="📕 User activity logs exported!"
    )