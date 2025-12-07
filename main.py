import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Получаем ключи
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранение выбора персонажа
users = {}

# Промпты для персонажей
PROMPTS = {
    "Emily": """Ты Emily, 13 лет из Сан-Диего. Говори как американская школьница.
    Твои интересы: сёрфинг, рисование, TikTok, музыка.
    Говори просто, коротко, дружелюбно. Только на английском!
    Пример: "Hey! How's your day going?" или "I love surfing in California!" """,
    
    "John": """Ты John, 12 лет из Лондона. Говори как британский школьник.
    Твои интересы: футбол, видеоигры, шахматы, мемы.
    Говори просто, коротко, дружелюбно. Только на английском!
    Пример: "Hello! What's up?" или "I support Chelsea FC!" """
}

# Старт
@dp.message(Command("start"))
async def start(message: types.Message):
    text = """👋 Hi! I'm your English practice bot!
    
Choose who you want to talk to:
/emily - Emily from USA 🇺🇸
/john - John from UK 🇬🇧

Just start chatting in English!"""
    await message.answer(text)

# Выбор Эмили
@dp.message(Command("emily"))
async def choose_emily(message: types.Message):
    users[message.from_user.id] = "Emily"
    await message.answer("Hi! I'm Emily from California! 🌊😊\nWhat would you like to talk about?")

# Выбор Джона
@dp.message(Command("john"))
async def choose_john(message: types.Message):
    users[message.from_user.id] = "John"
    await message.answer("Hello! I'm John from London! ⚽😄\nHow's it going?")

# Общение с AI
@dp.message()
async def chat(message: types.Message):
    user_id = message.from_user.id
    
    # Если пользователь не выбрал персонажа
    if user_id not in users:
        await message.answer("Please choose who to talk with first:\n/emily or /john")
        return
    
    # Показать "печатает..."
    await bot.send_chat_action(message.chat.id, "typing")
    
    character = users[user_id]
    prompt = PROMPTS[character]
    
    try:
        # Запрос к DeepSeek
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {DEEPSEEK_KEY}"},
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": message.text}
                    ],
                    "max_tokens": 100
                }
            )
            
            if response.status == 200:
                data = await response.json()
                reply = data["choices"][0]["message"]["content"]
                await message.answer(reply)
            else:
                await message.answer(f"Sorry, {character} is busy now. Try again!")
                
    except Exception as e:
        # Простой fallback
        if character == "Emily":
            await message.answer("Cool! Tell me more! 😊")
        else:
            await message.answer("Interesting! What else? ⚽")

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
