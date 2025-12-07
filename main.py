import os
import sys
import logging

# ========== НАСТРОЙКА ЛОГИРОВАНИЯ ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout  # Важно: выводим в stdout
)
logger = logging.getLogger(__name__)

# ========== ОТЛАДКА ПЕРЕМЕННЫХ ==========
logger.info("=" * 60)
logger.info("🔍 DEBUG START")

# Проверяем все переменные
env_vars = dict(os.environ)
logger.info(f"📊 Total environment variables: {len(env_vars)}")

# Проверяем конкретно BOT_TOKEN
BOT_TOKEN = os.getenv("BOT_TOKEN")
logger.info(f"🎯 BOT_TOKEN found: {bool(BOT_TOKEN)}")
if BOT_TOKEN:
    logger.info(f"✅ Token starts with: {BOT_TOKEN[:20]}...")
else:
    logger.error("❌ ERROR: BOT_TOKEN is missing!")
    logger.error("Please add BOT_TOKEN to Render Environment Variables")
    sys.exit(1)

logger.info("🔍 DEBUG END")
logger.info("=" * 60)

# ========== ОСНОВНОЙ КОД ==========
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Инициализируем бота с логами
logger.info("🤖 Initializing bot...")
try:
    bot = Bot(token=BOT_TOKEN)
    logger.info("✅ Bot initialized successfully")
except Exception as e:
    logger.error(f"❌ Bot initialization failed: {e}")
    sys.exit(1)

dp = Dispatcher()
logger.info("✅ Dispatcher created")

# Храним выбор пользователя
user_choice = {}

# Ответы для персонажей
RESPONSES = {
    "Emily": [
        "Hi! I'm Emily from California! 😊",
        "I love surfing at the beach! 🌊",
        "What's your favorite music?",
        "Nice weather today! ☀️",
        "Do you have any pets?",
        "How's school going?",
        "Let's practice English together!",
        "I like drawing and listening to pop music! 🎵",
        "What do you do for fun?",
        "Have an awesome day! 😄"
    ],
    "John": [
        "Hello! I'm John from London! ⚽",
        "Football is my favorite sport!",
        "It's raining here today! ☔",
        "Do you play video games? 🎮",
        "Cheers mate! How are you?",
        "I support Chelsea FC!",
        "What's your hobby?",
        "Learning English is cool, right?",
        "Do you like pizza? 🍕",
        "Talk to you later! 😊"
    ]
}

@dp.message(Command("start"))
async def start_command(message: types.Message):
    logger.info(f"User {message.from_user.id} sent /start")
    await message.answer(
        "🇺🇸🇬🇧 **English Practice Bot**\n\n"
        "Practice English by chatting with:\n\n"
        "👧 /emily - American girl, 13 years old\n"
        "👦 /john - British boy, 12 years old\n\n"
        "Choose a friend and start chatting in English!"
    )

@dp.message(Command("emily"))
async def emily_command(message: types.Message):
    logger.info(f"User {message.from_user.id} chose Emily")
    user_choice[message.from_user.id] = "Emily"
    await message.answer(
        "Hey there! 😊 I'm Emily!\n"
        "I'm 13 years old and I live in San Diego, California.\n"
        "I love surfing, drawing, and listening to music!\n\n"
        "What's your name?"
    )

@dp.message(Command("john"))
async def john_command(message: types.Message):
    logger.info(f"User {message.from_user.id} chose John")
    user_choice[message.from_user.id] = "John"
    await message.answer(
        "Hello! ⚽ I'm John!\n"
        "I'm 12 years old and I'm from London, England.\n"
        "I play football, chess, and love video games!\n\n"
        "How's your day going?"
    )

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    
    # Пропускаем команды
    if message.text.startswith('/'):
        return
    
    logger.info(f"User {user_id} sent: {message.text[:50]}...")
    
    # Проверяем, выбрал ли пользователь персонажа
    if user_id not in user_choice:
        await message.answer(
            "Please choose who you want to chat with:\n"
            "/emily - American girl\n"
            "/john - British boy"
        )
        return
    
    character = user_choice[user_id]
    
    # Выбираем случайный ответ
    reply = random.choice(RESPONSES[character])
    
    # Отправляем ответ
    logger.info(f"Bot ({character}) replied: {reply[:50]}...")
    await message.answer(reply)

async def main():
    logger.info("🚀 Starting Telegram bot polling...")
    logger.info("📱 Bot is ready! Find it in Telegram.")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Polling error: {e}")
    finally:
        logger.info("🛑 Bot stopped")

if __name__ == "__main__":
    # Явно запускаем asyncio с логированием
    logger.info("🎬 Starting application...")
    asyncio.run(main())
