import os
import sys

# ========== ОТЛАДКА ПЕРЕМЕННЫХ ==========
print("=" * 60)
print("🔍 DEBUG START")

# Проверяем все переменные
env_vars = dict(os.environ)
print(f"📊 Total environment variables: {len(env_vars)}")

# Выводим все переменные (скрываем значения)
for key, value in env_vars.items():
    if 'KEY' in key or 'TOKEN' in key or 'SECRET' in key:
        print(f"  🔑 {key}: {'*' * 10}{value[-5:] if value else 'EMPTY'}")
    else:
        print(f"  📝 {key}: {value[:30] if value else 'EMPTY'}...")

# Проверяем конкретно BOT_TOKEN
BOT_TOKEN = os.getenv("BOT_TOKEN")
print(f"\n🎯 BOT_TOKEN found: {bool(BOT_TOKEN)}")
if BOT_TOKEN:
    print(f"✅ Token starts with: {BOT_TOKEN[:20]}...")
else:
    print("❌ ERROR: BOT_TOKEN is missing!")
    print("Please add BOT_TOKEN to Render Environment Variables")
    sys.exit(1)

print("🔍 DEBUG END")
print("=" * 60)

# ========== ОСНОВНОЙ КОД ==========
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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
    await message.answer(
        "🇺🇸🇬🇧 **English Practice Bot**\n\n"
        "Practice English by chatting with:\n\n"
        "👧 /emily - American girl, 13 years old\n"
        "👦 /john - British boy, 12 years old\n\n"
        "Choose a friend and start chatting in English!"
    )

@dp.message(Command("emily"))
async def emily_command(message: types.Message):
    user_choice[message.from_user.id] = "Emily"
    await message.answer(
        "Hey there! 😊 I'm Emily!\n"
        "I'm 13 years old and I live in San Diego, California.\n"
        "I love surfing, drawing, and listening to music!\n\n"
        "What's your name?"
    )

@dp.message(Command("john"))
async def john_command(message: types.Message):
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
    await message.answer(reply)

async def main():
    print("🤖 Telegram bot is starting...")
    print("📱 Bot is ready! Find it in Telegram.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
