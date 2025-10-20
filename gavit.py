from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- TOKEN BOT ---
TOKEN = "8260825711:AAGWvHR9B1z_c7GP2vSHvE21gNEwlLItqG4"

# --- LỆNH /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Xin Chào! Mình Là Hứa Thịnh, mình có thể giúp gì cho bạn"
    )

# --- LỆNH /vit ---
async def vit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Dưới đây là mức giá của các loại vịt mà mình có bán:\n"
        "Vịt Ta: 90.000vnđ/kg\n"
        "Vịt Xiêm: 100.000vnđ/kg\n"
        "Vịt Huế: chưa xác định"
    )
    await update.message.reply_text(text)

# --- LỆNH /ga ---
async def ga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Đây là giá tiền các loại gà mình có bán:\n"
        "Gà Ta, Tre: 130.000/kg\n"
        "Gà Trống (Cựa): chưa xác định"
    )
    await update.message.reply_text(text)

# --- LỆNH /thongtin ---
async def thongtin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Thông Tin Giao Dịch:\n"
        "Địa Điểm: Chợ P2 (Chợ Nhật Lệ Cũ), Tỉnh Sóc Trăng, TP Cần Thơ\n"
        "Thời Gian: 6h30 Sáng - 9h Sáng Hàng Ngày\n"
        "Số Điện Thoại:\n"
        "  0329726487 (Chú Đẹp)\n"
        "  0363135487 (Hứa Thịnh)\n"
        "*Lưu Ý:\n"
        "   - Chỉ Nhận Đặt Trước Từ 11h Trưa - 22h Hàng Ngày\n"
        "   - Khi Đến Chợ P2 Muốn Tìm Chú Đẹp Chỉ Cần Hỏi Chỗ Bán Của Chú Đẹp Bán Vịt\n"
        "Xin Cảm Ơn!"
    )
    await update.message.reply_text(text)

# --- CHẠY BOT ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Gán lệnh
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vit", vit))
    app.add_handler(CommandHandler("ga", ga))
    app.add_handler(CommandHandler("thongtin", thongtin))

    print("✅ Bot đang chạy... Nhấn Ctrl + C để dừng.")
    app.run_polling()

if __name__ == "__main__":
    main()
