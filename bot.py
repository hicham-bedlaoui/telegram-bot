from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8436906818:AAFkT5jlzmsDf3p-5DBh2wViYw0PyrkUbUA"

# 🔗 روابط القنوات
CHANNELS = {
    "amazon": {
        "url": "https://t.me/kanzamazon",
        "username": "@kanzamazon"
    },
    "aliexpress": {
        "url": "https://t.me/kanzaliexpress",
        "username": "@kanzaliexpress"
    },
    "temu": {
        "url": "https://t.me/kanztemu1",
        "username": "@kanztemu1"
    }
}

# ===== القائمة الرئيسية =====
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛍 Amazon", callback_data="amazon")],
        [InlineKeyboardButton("🛒 AliExpress", callback_data="aliexpress")],
        [InlineKeyboardButton("🏷 Temu", callback_data="temu")]
    ])

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 اختر المتجر 👇",
        reply_markup=main_menu()
    )

# ===== تحقق من الاشتراك =====
async def is_subscribed(user_id, bot, channel_username):
    try:
        member = await bot.get_chat_member(channel_username, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print("ERROR:", e)
        return False

# ===== HANDLE =====
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id

    await query.answer()

    # ===== اختيار متجر =====
    if data in CHANNELS:
        channel = CHANNELS[data]
        subscribed = await is_subscribed(user_id, context.bot, channel["username"])

        if not subscribed:
            keyboard = [
                [InlineKeyboardButton("📢 اشترك أولاً", url=channel["url"])],
                [InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data=f"check_{data}")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="back")]
            ]

            await query.edit_message_text(
                "🚫 يجب الاشتراك في القناة أولاً\n\n👇 اشترك ثم اضغط تحقق",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            keyboard = [
                [InlineKeyboardButton("📢 دخول القناة", url=channel["url"])],
                [InlineKeyboardButton("🔙 رجوع", callback_data="back")]
            ]

            await query.edit_message_text(
                "✅ أنت مشترك بالفعل!\n\n👇 ادخل القناة:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    # ===== زر التحقق =====
    elif data.startswith("check_"):
        market = data.split("_")[1]
        channel = CHANNELS[market]

        subscribed = await is_subscribed(user_id, context.bot, channel["username"])

        if subscribed:
            keyboard = [
                [InlineKeyboardButton("📢 دخول القناة", url=channel["url"])],
                [InlineKeyboardButton("🔙 رجوع", callback_data="back")]
            ]

            await query.edit_message_text(
                "✅ تم التحقق بنجاح!\n\n👇 ادخل القناة:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await query.answer("❌ لم تشترك بعد!", show_alert=True)

    # ===== رجوع =====
    elif data == "back":
        await query.edit_message_text(
            "🔥 اختر المتجر 👇",
            reply_markup=main_menu()
        )

# ===== تشغيل =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()