import re
import unicodedata
from telegram import (
    Update,
    BotCommand,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

TOKEN = "8260825711:AAGWvHR9B1z_c7GP2vSHvE21gNEwlLItqG4"

LOAI_GA_VIT = ["gà ta", "gà tre", "gà trống", "vịt ta", "vịt xiêm", "vịt huế"]

# Hàm loại bỏ dấu tiếng Việt và chuẩn hóa text
def remove_vietnamese_diacritics(text):
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    return str(text).lower()

# --- /START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.set_my_commands([
        BotCommand("start", "Bắt đầu và xem hướng dẫn"),
        BotCommand("dathang", "Đặt hàng theo cú pháp"),
        BotCommand("cs", "Chỉnh sửa lại đơn hàng"),
        BotCommand("xacnhan", "Xác nhận đơn hàng"),
        BotCommand("thongtin", "Thông tin giao dịch"),
    ])

    keyboard = [
        [KeyboardButton("Đặt Hàng")],
        [KeyboardButton("Hướng Dẫn")],
        [KeyboardButton("Liên Hệ")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    message = (
        "👋 Xin chào! Mình là **Hứa Thịnh**, rất vui được hỗ trợ bạn!\n\n"
        "📋 Các lệnh có sẵn:\n"
        "/vit — Xem giá vịt\n"
        "/ga — Xem giá gà\n"
        "/thongtin — Thông tin giao dịch\n"
        "/dathang — Đặt hàng nhanh\n"
        "/cs — Chỉnh sửa lại đơn hàng\n"
        "/xacnhan — Xác nhận đơn hàng\n\n"
        "📦 Hướng dẫn đặt hàng:\n"
        "/dathang <số lượng> <loại> <cân nặng> <số điện thoại> <tên>\n"
        "🧾 Ví dụ: `/dathang 2 vịt xiêm 5kg 0363135487 Nguyễn Văn A`\n\n"
        "💬 Hoặc bạn chỉ cần nhắn ví dụ như:\n"
        "`2 gà ta 3kg 0912345678 Nguyễn Văn A`\n"
        "Bot sẽ tự hiểu và tạo đơn hàng giúp bạn!"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup, parse_mode="Markdown")

# --- /VIT ---
async def vit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🦆 Giá vịt hiện có:\n"
        "- Vịt Ta: 90.000đ/kg\n"
        "- Vịt Xiêm: 100.000đ/kg\n"
        "- Vịt Huế: chưa xác định"
    )

# --- /GA ---
async def ga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🐔 Giá gà hiện có:\n"
        "- Gà Ta, Tre: 130.000đ/kg\n"
        "- Gà Trống (Cựa): chưa xác định"
    )

# --- /THONGTIN ---
async def thongtin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📍 **Thông Tin Giao Dịch**\n"
        "Địa điểm: Chợ P2 (Chợ Nhật Lệ Cũ), Sóc Trăng - TP Cần Thơ\n"
        "⏰ Thời gian: 6h30 sáng - 9h sáng hàng ngày\n\n"
        "📞 Liên hệ:\n"
        "  0329726487 (Chú Đẹp)\n"
        "  0363135487 (Hứa Thịnh)\n\n"
        "⚠️ *Chỉ nhận đặt trước từ 11h trưa - 22h hàng ngày*\n"
        "_Khi đến chợ, muốn tìm Chú Đẹp, hãy hỏi 'Chỗ Chú Đẹp bán vịt'_",
        parse_mode="Markdown"
    )

# --- /DATHANG ---
async def dathang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 5:
        await update.message.reply_text(
            "⚠️ Cú pháp chưa đúng!\n"
            "Hãy dùng: /dathang <số lượng> <loại> <cân nặng> <số điện thoại> <tên người đặt>"
        )
        return

    so_luong = args[0]
    loai = args[1]
    if args[1] + " " + args[2] in LOAI_GA_VIT:
        loai = args[1] + " " + args[2]
        args.pop(2)

    can_nang = args[-3]
    sdt = args[-2]
    ten = " ".join(args[-1:])

    msg = (
        f"🧾 **Xác nhận đơn hàng:**\n\n"
        f"Số lượng: {so_luong}\n"
        f"Loại: {loai}\n"
        f"Cân nặng: {can_nang}\n"
        f"Số điện thoại: {sdt}\n"
        f"Tên người đặt: {ten}\n\n"
        "✅ Nếu thông tin đúng, trả lời /xacnhan\n"
        "❌ Nếu sai, trả lời /cs để nhập lại."
    )

    context.user_data["xacnhan_msg"] = msg
    await update.message.reply_text(msg, parse_mode="Markdown")

# --- /CS ---
async def cs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Hãy nhập lại đơn hàng theo cú pháp /dathang ...")

# --- /XACNHAN ---
async def xacnhan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = context.user_data.get("xacnhan_msg", None)
    if not msg:
        await update.message.reply_text("⚠️ Không có đơn hàng nào để xác nhận.")
        return

    await update.message.reply_text("✅ Đơn hàng đã được xác nhận và gửi đến quản lý!")
    await context.bot.send_message("@huathinh", f"📩 Đơn hàng mới:\n{msg}")

# --- XỬ LÝ TIN NHẮN TỰ NHIÊN ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    normalized = remove_vietnamese_diacritics(text)

    # Nhận diện từ menu
    if normalized == "dat hang":
        await update.message.reply_text("💬 Hãy nhập cú pháp: /dathang <số lượng> <loại> <cân nặng> <số điện thoại> <tên>")
        return
    elif normalized == "huong dan":
        await update.message.reply_text("📦 Dùng /dathang để đặt hàng nhanh hoặc nhắn tự nhiên như: '1 vịt xiêm 2kg 0393135487 Thịnh'")
        return
    elif normalized == "lien he":
        await thongtin(update, context)
        return

    # Regex nhận diện đơn hàng
    pattern = r"(\d+)\s+(ga|vit)(?:\s+(ta|tre|trong|xiem|hue))?\s+(\d+(?:kg)?)\s+(\d{9,11})\s+([\w\sÀ-ỹ]+)"
    match = re.search(pattern, normalized)
    if match:
        so_luong = match.group(1)
        loai = match.group(2)
        phu_loai = match.group(3) if match.group(3) else ""
        can_nang = match.group(4)
        sdt = match.group(5)
        ten = match.group(6).title()

        full_loai = (loai + " " + phu_loai).strip()

        msg = (
            f"🧾 **Xác nhận đơn hàng:**\n\n"
            f"Số lượng: {so_luong}\n"
            f"Loại: {full_loai}\n"
            f"Cân nặng: {can_nang}\n"
            f"Số điện thoại: {sdt}\n"
            f"Tên người đặt: {ten}\n\n"
            "✅ Nếu đúng, trả lời /xacnhan\n"
            "❌ Nếu sai, trả lời /cs để nhập lại."
        )

        context.user_data["xacnhan_msg"] = msg
        await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        await update.message.reply_text("❓ Mình chưa hiểu ý bạn, hãy gõ /start để xem hướng dẫn hoặc chọn trong menu nhé.")

# --- MAIN ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("vit", vit))
app.add_handler(CommandHandler("ga", ga))
app.add_handler(CommandHandler("thongtin", thongtin))
app.add_handler(CommandHandler("dathang", dathang))
app.add_handler(CommandHandler("cs", cs))
app.add_handler(CommandHandler("xacnhan", xacnhan))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()
