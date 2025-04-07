import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

logging.basicConfig(level=logging.INFO)

# Шаги
MATERIAL, FROM, TO, VOLUME, DATE, TIME, PHONE = range(7)

materials = [["Песок", "Щебень"], ["Бой Асфальта", "Бой Бетона", "Бой Кирпича"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выберите материал:",
        reply_markup=ReplyKeyboardMarkup(materials, one_time_keyboard=True)
    )
    return MATERIAL

async def get_material(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["material"] = update.message.text
    await update.message.reply_text("Откуда везти?")
    return FROM

async def get_from(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["from"] = update.message.text
    await update.message.reply_text("Куда доставить?")
    return TO

async def get_to(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["to"] = update.message.text
    await update.message.reply_text("Сколько кубов?")
    return VOLUME

async def get_volume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["volume"] = update.message.text
    await update.message.reply_text("Когда нужно? (дата)")
    return DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["date"] = update.message.text
    await update.message.reply_text("В какое время?")
    return TIME

async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["time"] = update.message.text
    await update.message.reply_text("Контактный номер телефона?")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text

    # Сбор сообщения
    msg = (
        f"🚧 *Новая заявка!*\n"
        f"Материал: {context.user_data['material']}\n"
        f"Откуда: {context.user_data['from']}\n"
        f"Куда: {context.user_data['to']}\n"
        f"Объём: {context.user_data['volume']} м³\n"
        f"Когда: {context.user_data['date']} в {context.user_data['time']}\n"
        f"Контакт: {context.user_data['phone']}"
    )

    # Отправка тебе в канал
    channel_id = "t.me/Perevoz_spb" 
    await context.bot.send_message(chat_id=channel_id, text=msg, parse_mode='Markdown')

    await update.message.reply_text("Спасибо! Ваша заявка принята.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Заявка отменена.")
    return ConversationHandler.END

if __name__ == '__main__':
    import os
    token = os.getenv("TOKEN")  # <-- Не забудь создать переменную окружения

    app = ApplicationBuilder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MATERIAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_material)],
            FROM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_from)],
            TO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_to)],
            VOLUME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_volume)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()
