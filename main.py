import os
import sys
import logging
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# ========== НАСТРОЙКА ЛОГИРОВАНИЯ ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# ========== ПРОВЕРКА ТОКЕНА ==========
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("❌ ERROR: No BOT_TOKEN found!")
    logger.error("Please add BOT_TOKEN to Render Environment Variables")
    sys.exit(1)

logger.info(f"✅ Bot token: {BOT_TOKEN[:15]}...")

# ========== ИНИЦИАЛИЗАЦИЯ ==========
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Храним выбор пользователя
user_choice = {}

# ========== БАЗА ЗНАНИЙ ПЕРСОНАЖЕЙ ==========
CHARACTERS = {
    "Emily": {
        "name": "Emily Carter",
        "age": "13",
        "location": "San Diego, California, USA",
        "hobbies": ["surfing", "drawing", "listening to pop music"],
        "school": "7th grade",
        "pet": "a dog named Sparky",
        "favorite_food": "tacos",
        "favorite_color": "blue",
        
        "responses": {
            "greeting": ["Hi! I'm Emily from California! 😊", "Hey there! How's it going? 🌊"],
            "name": ["My name is Emily! 😊", "I'm Emily Carter!"],
            "age": ["I'm 13 years old!", "Just turned 13!"],
            "location": ["I live in San Diego, California!", "Sunny California! ☀️"],
            "hobby": ["I love surfing and drawing! 🏄‍♀️🎨", "My hobbies are surfing, drawing, and music!"],
            "school": ["I'm in 7th grade! I like art class.", "School is fun! I have cool friends."],
            "pet": ["I have a dog named Sparky! 🐕", "Yes, Sparky is my dog!"],
            "weather": ["The weather is awesome here! Always sunny!", "Perfect surfing weather! 🌊"],
            "food": ["I love tacos! 🌮", "Mexican food is my favorite!"],
            "question": ["What about you?", "How about you?", "What do you think?"],
            "default": ["That's cool! Tell me more! 😊", "Interesting! What else?", "Nice! 😊"]
        }
    },
    
    "John": {
        "name": "John Williams",
        "age": "12",
        "location": "London, England, UK",
        "hobbies": ["football", "chess", "video games"],
        "school": "Year 8",
        "pet": "no pets, but I want a dog",
        "favorite_food": "fish and chips",
        "favorite_color": "red",
        
        "responses": {
            "greeting": ["Hello! I'm John from London! ⚽", "Hi! What's up? 🇬🇧"],
            "name": ["I'm John Williams!", "My name is John!"],
            "age": ["I'm 12 years old!", "Just turned 12!"],
            "location": ["I'm from London, England!", "London, UK! 🏴󠁧󠁢󠁥󠁮󠁧󠁿"],
            "hobby": ["I play football and chess! ⚽♟️", "Football and video games are my thing!"],
            "school": ["I'm in Year 8!", "School is okay, PE is my favorite!"],
            "pet": ["No pets, but I really want a dog!", "I wish I had a dog!"],
            "weather": ["It rains a lot here! Typical UK weather ☔", "Rainy today!"],
            "food": ["Fish and chips is the best! 🐟🍟", "I love British food!"],
            "question": ["What about you?", "And you?", "How about you?"],
            "default": ["Interesting! Go on!", "Yeah! Tell me more!", "Cheers mate! 😄"]
        }
    }
}

# ========== КОМАНДЫ БОТА ==========
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "🇺🇸🇬🇧 **English Practice Bot**\n\n"
        "Practice English by chatting with:\n\n"
        "👧 /emily - American girl, 13 years old\n"
        "   From California, loves surfing & drawing\n\n"
        "👦 /john - British boy, 12 years old\n"
        "   From London, loves football & chess\n\n"
        "Choose a friend and start chatting in English!"
    )

@dp.message(Command("emily"))
async def emily_command(message: types.Message):
    user_choice[message.from_user.id] = "Emily"
    char = CHARACTERS["Emily"]
    await message.answer(
        f"👋 Hi! I'm {char['name']}! 😊\n"
        f"I'm {char['age']} and I live in {char['location']}.\n"
        f"I love {', '.join(char['hobbies'][:2])}!\n\n"
        f"Ask me anything!"
    )

@dp.message(Command("john"))
async def john_command(message: types.Message):
    user_choice[message.from_user.id] = "John"
    char = CHARACTERS["John"]
    await message.answer(
        f"👋 Hello! I'm {char['name']}! ⚽\n"
        f"I'm {char['age']} and I'm from {char['location']}.\n"
        f"I like {', '.join(char['hobbies'][:2])}!\n\n"
        f"What would you like to know?"
    )

# ========== ОБРАБОТКА СООБЩЕНИЙ ==========
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    
    # Если пользователь не выбрал персонажа
    if user_id not in user_choice:
        await message.answer("Please choose who to chat with:\n/emily or /john")
        return
    
    # Пропускаем команды
    if message.text.startswith('/'):
        return
    
    character_name = user_choice[user_id]
    character = CHARACTERS[character_name]
    user_text = message.text.lower().strip()
    
    logger.info(f"User {user_id}: {user_text[:50]}...")
    
    # Определяем тип вопроса
    response_type = "default"
    
    # Простая логика распознавания вопросов
    if any(word in user_text for word in ["hi", "hello", "hey"]):
        response_type = "greeting"
    elif any(word in user_text for word in ["name", "call"]):
        response_type = "name"
    elif any(word in user_text for word in ["old", "age"]):
        response_type = "age"
    elif any(word in user_text for word in ["where", "from", "live"]):
        response_type = "location"
    elif any(word in user_text for word in ["hobby", "like", "do for fun", "hobbies"]):
        response_type = "hobby"
    elif any(word in user_text for word in ["school", "class", "grade"]):
        response_type = "school"
    elif any(word in user_text for word in ["pet", "dog", "cat", "animal"]):
        response_type = "pet"
    elif any(word in user_text for word in ["weather", "rain", "sun", "sunny"]):
        response_type = "weather"
    elif any(word in user_text for word in ["food", "eat", "hungry", "taco", "pizza"]):
        response_type = "food"
    elif "?" in user_text:
        # Если это вопрос, но не поняли тему
        response_type = "question"
    
    # Выбираем ответ
    responses = character["responses"][response_type]
    reply = random.choice(responses)
    
    # Добавляем встречный вопрос, если это уместно
    if response_type in ["hobby", "school", "pet", "food"] and "?" not in reply:
        question = random.choice(character["responses"]["question"])
        reply = f"{reply} {question}"
    
    # Отправляем ответ
    await message.answer(reply)
    logger.info(f"Bot ({character_name}): {reply[:50]}...")

# ========== ЗАПУСК БОТА ==========
async def main():
    logger.info("🤖 Starting Telegram bot...")
    logger.info("📱 Bot is ready! Find @MFF_english_bot in Telegram")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
