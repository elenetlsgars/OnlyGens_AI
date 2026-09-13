import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import TelegramError

# ⚙️ НАСТРОЙКИ
BOT_TOKEN = os.environ
CHANNEL_ID = os.environ
CHANNEL_LINK = "https://t.me/onlygens_ai"
SOURCE_PHOTO = "AgACAgIAAxkBAAMFaqXUlWZGUNa2bop9nzarjtms7TsAAkIfaxtGOTFJX6ZV4iIlGK0BAAMCAAN3AAM9BA"

YOUR_PROMPT = """Гиперреалистичная профессиональная бьюти-фотография, реклама премиального ухода за кожей. Целостная, единая сцена: блондинка с гладко зачесанными назад волосами и сияющей, чистой кожей. Она наклоняется вперед, руки лежат на белом столе. Ее руки мягко обрамляют и держат цилиндрическую янтарную пластиковую бутылку с черной крышкой. Бутылка стоит прямо перед ее подбородком. Она смотрит в сторону, влево, с мягким, безмятежным выражением. Угол камеры низкий, съемка снизу от уровня ее глаз. На бутылке полностью читаемая белая этикетка с бледно-мятными полосами сверху и снизу, и текстом: «BIOBALANCE» вверху, «Super Toner» крупным жирным шрифтом с засечками в центре, и «PORE TIGHT» под ним. Бутылка и ее лицо освещены абсолютно одинаковым мягким, естественным студийным светом, с реалистичными тенями и отражениями, связывающими их воедино. Фон — чистый, яркий белый. Сверхдетализированное, разрешение 8k, резкий фокус на лице и бутылке, единое освещение."""

logging.basicConfig(level=logging.INFO)

async def is_subscribed(user_id: int, bot) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except TelegramError:
        return False

def subscribe_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Подписаться", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ Я подписался", callback_data="check_sub")],
    ])

async def send_prompt(message, context) -> None:
    await message.reply_photo(
        photo=SOURCE_PHOTO,
        caption="🎨 Исходник для промпта ☝️",
    )
    text = (
        f"Вставь этот промпт в Nano Banana и получи крутой результат:\n\n"
        f"{YOUR_PROMPT}\n\n"
        f"🔥 Понравилось? В @OnlyGens_AI постоянно появляются новые промпты "
        f"для фото и видео генераций — заглядывай, чтобы не пропустить."
    )
    await message.reply_text(text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if await is_subscribed(user_id, context.bot):
        await send_prompt(update.message, context)
    else:
        await update.message.reply_text(
            "🔒 Чтобы получить промпт, подпишитесь на канал:",
            reply_markup=subscribe_keyboard(),
        )

async def check_sub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if await is_subscribed(query.from_user.id, context.bot):
        await query.message.edit_text("✅ Подписка подтверждена! Отправляю промпт...")
        await send_prompt(query.message, context)
    else:
        await query.answer("❌ Подписка не найдена. Попробуйте ещё раз.", show_alert=True)

def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_sub, pattern="check_sub"))
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()