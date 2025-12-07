import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")  # Новый ключ

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

users = {}

# Fallback ответы (уже есть)
FALLBACK = {
    "Emily": ["Hi! I'm from California! 😊", "Nice weather! ☀️", "Love surfing! 🌊"],
    "John": ["Hello from London! ⚽", "Rainy day! ☔", "Football is life!"]
}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🇺🇸🇬🇧 Chat with:\n/emily (USA)\n/john (UK)\n\nJust type English!"
    )

@dp.message(Command("emily"))
async def emily_cmd(message: types.Message):
    users[message.from_user.id] = "Emily"
    await message.answer("Hey! I'm Emily! 😊")

@dp.message(Command("john"))
async def john_cmd(message: types.Message):
    users[message.from_user.id] = "John"
    await message.answer("Hi! I'm John! ⚽")

@dp.message()
async def chat(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in users:
        await message.answer("Choose /emily or /john")
        return
    
    char = users[user_id]
    reply = random.choice(FALLBACK[char])
    await message.answer(reply)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
