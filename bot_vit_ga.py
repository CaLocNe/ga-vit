import telebot
from telebot import types

API_TOKEN = "8260825711:AAGWvHR9B1z_c7GP2vSHvE21gNEwlLItqG4"
bot = telebot.TeleBot(API_TOKEN)

# Lưu tạm đơn hàng theo user_id
pending_orders = {}

# --- MENU COMMANDS ---
bot.set_my_commands([
    types.BotCommand("start", "Bắt đầu trò chuyện"),
    types.BotCommand("vit", "Xem giá vịt"),
    types.BotCommand("ga", "Xem giá gà"),
    types.BotCommand("thongtin", "Thông tin giao dịch"),
    types.BotCommand("dathang", "Đặt hàng: /dathang <số lượng> <loại> <cân nặng> <số điện thoại> <tên>"),
    types.BotCommand("cs", "Chỉnh sửa lại đơn hàng"),
    types.BotCommand("xacnhan", "Xác nhận đơn hàng")
])

# --- LỆNH /START ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
        "Xin Chào! Mình Là Hứa Thịnh, mình có thể giúp gì cho bạn 😊")

# --- LỆNH /VIT ---
@bot.message_handler(commands=['vit'])
def send_vit(message):
    text = (
        "Dưới đây là mức giá của các loại vịt mà mình có bán:\n"
        "🦆 Vịt Ta: 90.000vnđ/kg\n"
        "🦆 Vịt Xiêm: 100.000vnđ/kg\n"
        "🦆 Vịt Huế: chưa xác định"
    )
    bot.reply_to(message, text)

# --- LỆNH /GA ---
@bot.message_handler(commands=['ga'])
def send_ga(message):
    text = (
        "Đây là giá tiền các loại gà mình có bán:\n"
        "🐔 Gà Ta, Tre: 130.000/kg\n"
        "🐔 Gà Trống (Cựa): chưa xác định"
    )
    bot.reply_to(message, text)

# --- LỆNH /THONGTIN ---
@bot.message_handler(commands=['thongtin'])
def send_thongtin(message):
    text = (
        "📍 *Thông Tin Giao Dịch:*\n"
        "Địa Điểm: Chợ P2 (Chợ Nhật Lệ Cũ), Tỉnh Sóc Trăng, TP Cần Thơ\n"
        "Thời Gian: 6h30 Sáng - 9h Sáng Hàng Ngày\n"
        "Số Điện Thoại:\n"
        "  📞 0329726487 (Chú Đẹp)\n"
        "  📞 0363135487 (Hứa Thịnh)\n"
        "\n*Lưu Ý:*\n"
        "- Chỉ Nhận Đặt Trước Từ 11h Trưa - 22h Hàng Ngày\n"
        "- Khi Đến Chợ P2 Muốn Tìm Chú Đẹp Chỉ Cần Hỏi 'Chỗ Chú Đẹp Bán Vịt'\n"
        "\nXin Cảm Ơn! 🙏"
    )
    bot.reply_to(message, text, parse_mode="Markdown")

# --- LỆNH /DATHANG ---
@bot.message_handler(commands=['dathang'])
def dat_hang(message):
    try:
        parts = message.text.split(" ", 5)
        if len(parts) < 6:
            bot.reply_to(message,
                "❌ Sai cú pháp!\n\nĐúng định dạng là:\n"
                "`/dathang <số lượng> <loại> <cân nặng> <số điện thoại> <tên>`",
                parse_mode="Markdown")
            return

        soluong = parts[1]
        loai = parts[2].capitalize()
        cannang = parts[3]
        sdt = parts[4]
        ten = parts[5]

        # tạo nội dung xác nhận
        order_text = (
            f"🧾 *Đơn Hàng Mới:*\n"
            f"👤 Tên: {ten}\n"
            f"📞 SĐT: {sdt}\n"
            f"🐔 Loại: {loai}\n"
            f"⚖️ Cân Nặng: {cannang} kg\n"
            f"📦 Số Lượng: {soluong}\n"
            "\n✅ *Cảm ơn bạn đã đặt hàng!* Mình sẽ liên hệ xác nhận sớm nhất.\n\n"
            "Nếu thông tin đã chính xác vui lòng trả lời bằng /xacnhan\n"
            "Hoặc nếu chưa đúng hãy trả lời bằng /cs để nhập lại đơn hàng."
        )

        pending_orders[message.from_user.id] = order_text
        bot.reply_to(message, order_text, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Có lỗi xảy ra: {e}")

# --- LỆNH /CS ---
@bot.message_handler(commands=['cs'])
def chinh_sua(message):
    if message.from_user.id in pending_orders:
        del pending_orders[message.from_user.id]
    bot.reply_to(message,
        "🔄 Hãy nhập lại đơn hàng theo cú pháp:\n"
        "`/dathang <số lượng> <loại> <cân nặng> <số điện thoại> <tên>`",
        parse_mode="Markdown")

# --- LỆNH /XACNHAN ---
@bot.message_handler(commands=['xacnhan'])
def xac_nhan(message):
    if message.from_user.id not in pending_orders:
        bot.reply_to(message, "❗ Bạn chưa có đơn hàng nào cần xác nhận.")
        return

    order = pending_orders[message.from_user.id]

    try:
        # gửi tới tài khoản @huathinh (thay ID bằng username)
        # nếu biết user_id của @huathinh, bạn có thể thay trực tiếp ID vào đây
        bot.send_message("@huathinh", f"📩 *Đơn hàng mới được xác nhận:*\n\n{order}", parse_mode="Markdown")

        bot.reply_to(message, "✅ Đơn hàng của bạn đã được gửi đến Hứa Thịnh. Cảm ơn bạn rất nhiều! 🙏")
        del pending_orders[message.from_user.id]

    except Exception:
        bot.reply_to(message,
            "⚠️ Không thể gửi tin nhắn đến @huathinh.\n"
            "Vui lòng kiểm tra xem bot đã từng được @huathinh nhắn trước chưa (Telegram yêu cầu vậy).")

# --- CHẠY BOT ---
print("✅ Bot đang chạy...")
bot.infinity_polling()
