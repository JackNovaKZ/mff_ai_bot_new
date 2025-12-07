import os
import sys

# === ОТЛАДКА ===
print("=" * 50)
print("🔍 DEBUG: Checking environment variables")

# Получаем все переменные
all_vars = dict(os.environ)
print(f"Total env vars: {len(all_vars)}")

# Ищем BOT_TOKEN
bot_token = os.getenv("BOT_TOKEN")
print(f"BOT_TOKEN exists: {bool(bot_token)}")
if bot_token:
    print(f"BOT_TOKEN first 20 chars: {bot_token[:20]}...")

# Если нет токена - выходим
if not bot_token:
    print("❌ ERROR: BOT_TOKEN not found!")
    print("Please add BOT_TOKEN to Render Environment Variables")
    sys.exit(1)

print("✅ BOT_TOKEN found!")
print("=" * 50)

# === ОСНОВНОЙ КОД ===
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

bot = Bot(token=bot_token)
dp = Dispatcher()

users = {}

RESPONSES = {
    "Emily": [
        "Hi! I'm Emily from California! 😊",
        "I love surfing! 🌊 Want to try?",
        "Nice weather today! ☀️",
        "What's your favorite subject?",
        "Do you have pets? I have a dog! 🐶"
    ],
    "John": [
        "Hello! I'm John from London! ⚽",
        "Football is the best sport!",
        "Rainy day here in UK! ☔",
        "Do you play video games? 🎮",
        "Cheers mate! How are you?"
    ]
}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🇺🇸🇬🇧 **English Practice Bot**\n\n"
        "Chat with:\n"
        "/emily - American girl (13)\n"
        "/john - British boy (12)\n\n"
        "Just type in English!"
    )

@dp.message(Command("emily"))
async def emily(message: types.Message):
    users[message.from_user.id] = "Emily"
    await message.answer("Hey there! I'm Emily! 😊\nWhat's your name?")

@dp.message(Command("john"))
async def john(message: types.Message):
    users[message.from_user.id] = "John"
    await message.answer("Hello! I'm John! ⚽\nHow's your day?")

@dp.message()
async def chat(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in users:
        await message.answer("Please choose /emily or /john")
        return
    
    char = users[user_id]
    reply = random.choice(RESPONSES[char])
    await message.answer(reply)

async def main():
    print("🤖 Bot starting polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
