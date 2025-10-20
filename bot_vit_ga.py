import telebot
from telebot import types

API_TOKEN = "8260825711:AAGWvHR9B1z_c7GP2vSHvE21gNEwlLItqG4"
bot = telebot.TeleBot(API_TOKEN)

# Lưu tạm đơn hàng theo user_id
pending_orders = {}

# Danh sách loại hàng hợp lệ
LOAI_HOP_LE = ["gà ta", "gà tre", "gà trống", "vịt ta", "vịt xiêm", "vịt huế"]

# --- MENU COMMANDS ---
bot.set_my_commands([
    types.BotCommand("start", "Bắt đầu trò chuyện"),
    types.BotCommand("vit", "Xem giá vịt"),
    types.BotCommand("ga", "Xem giá gà"),
    types.BotCommand("thongtin", "Thông tin giao dịch"),
    types.BotCommand("dathang", "Đặt hàng"),
    types.BotCommand("cs", "Chỉnh sửa đơn hàng"),
    types.BotCommand("xacnhan", "Xác nhận đơn hàng")
])

# --- LỆNH /START ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Tạo menu nút bấm
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🦆 Xem giá vịt")
    btn2 = types.KeyboardButton("🐔 Xem giá gà")
    btn3 = types.KeyboardButton("📍 Thông tin giao dịch")
    btn4 = types.KeyboardButton("🧾 Đặt hàng ngay")
    markup.add(btn1, btn2, btn3, btn4)

    text = (
        "👋 *Xin Chào!* Mình là *Hứa Thịnh* 🐔🦆\n"
        "Rất vui được hỗ trợ bạn!\n\n"
        "📋 *Các lệnh có sẵn:*\n"
        "/vit — Xem giá vịt\n"
        "/ga — Xem giá gà\n"
        "/thongtin — Thông tin giao dịch\n"
        "/dathang — Đặt hàng nhanh\n"
        "/cs — Chỉnh sửa lại đơn hàng\n"
        "/xacnhan — Xác nhận đơn hàng\n\n"
        "🧾 *Hướng dẫn đặt hàng:*\n"
        "`/dathang <số lượng> <loại> <cân nặng> <số điện thoại> <tên>`\n\n"
        "📦 *Ví dụ:* \n"
        "`/dathang 2 vịt huế 5 0363135487 Nguyễn Văn A`\n\n"
        "Hoặc chọn nhanh bằng nút bên dưới ⬇️"
    )

    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

# --- NÚT MENU XỬ LÝ ---
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    text = message.text.lower()

    if "xem giá vịt" in text:
        send_vit(message)
    elif "xem giá gà" in text:
        send_ga(message)
    elif "thông tin" in text:
        send_thongtin(message)
    elif "đặt hàng" in text:
        huong_dan_dathang(message)
    else:
        bot.reply_to(message, "❓ Mình chưa hiểu ý bạn, vui lòng chọn trong menu hoặc gõ /start để xem hướng dẫn.")

# --- LỆNH /VIT ---
def send_vit(message):
    text = (
        "Dưới đây là mức giá của các loại vịt mà mình có bán:\n"
        "🦆 Vịt Ta: 90.000vnđ/kg\n"
        "🦆 Vịt Xiêm: 100.000vnđ/kg\n"
        "🦆 Vịt Huế: chưa xác định"
    )
    bot.reply_to(message, text)

# --- LỆNH /GA ---
def send_ga(message):
    text = (
        "Đây là giá tiền các loại gà mình có bán:\n"
        "🐔 Gà Ta: 130.000/kg\n"
        "🐔 Gà Tre: 130.000/kg\n"
        "🐔 Gà Trống (Cựa): chưa xác định"
    )
    bot.reply_to(message, text)

# --- LỆNH /THONGTIN ---
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

# --- HƯỚNG DẪN ĐẶT HÀNG ---
def huong_dan_dathang(message):
    text = (
        "🧾 *Hướng dẫn đặt hàng:*\n"
        "Hãy nhập theo cú pháp sau:\n"
        "`/dathang <số lượng> <loại> <cân nặng> <số điện thoại> <tên>`\n\n"
        "📦 Ví dụ:\n"
        "`/dathang 2 vịt ta 5 0363135487 Nguyễn Văn A`"
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
        loai = parts[2].lower()
        cannang = parts[3]
        sdt = parts[4]
        ten = parts[5]

        # Kiểm tra loại hợp lệ
        if loai not in LOAI_HOP_LE:
            danh_sach = ", ".join(LOAI_HOP_LE)
            bot.reply_to(message,
                f"⚠️ Loại hàng bạn nhập không hợp lệ.\n"
                f"Vui lòng chọn 1 trong các loại sau:\n`{danh_sach}`",
                parse_mode="Markdown")
            return

        order_text = (
            f"🧾 *Đơn Hàng Mới:*\n"
            f"👤 Tên: {ten}\n"
            f"📞 SĐT: {sdt}\n"
            f"🐔 Loại: {loai.title()}\n"
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
        bot.send_message("@huathinh", f"📩 *Đơn hàng mới được xác nhận:*\n\n{order}", parse_mode="Markdown")
        bot.reply_to(message, "✅ Đơn hàng của bạn đã được gửi đến Hứa Thịnh. Cảm ơn bạn rất nhiều! 🙏")
        del pending_orders[message.from_user.id]
    except Exception:
        bot.reply_to(message,
            "⚠️ Không thể gửi tin nhắn đến @huathinh.\n"
            "Vui lòng kiểm tra xem tài khoản @huathinh đã từng nhắn tin với bot trước chưa (Telegram yêu cầu vậy).")

# --- CHẠY BOT ---
print("✅ Bot đang chạy...")
bot.infinity_polling()
