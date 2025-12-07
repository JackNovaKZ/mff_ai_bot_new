import os
import sys
import logging
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# ==================== НАСТРОЙКА ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# ==================== ПРОВЕРКА ТОКЕНА ====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("❌ ОШИБКА: BOT_TOKEN не найден!")
    logger.error("Добавьте BOT_TOKEN в Environment Variables на Render")
    sys.exit(1)

logger.info(f"✅ Токен бота: {BOT_TOKEN[:15]}...")

# ==================== ИНИЦИАЛИЗАЦИЯ ====================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Храним выбор пользователя
user_choice = {}

# ==================== БАЗА ЗНАНИЙ ====================
CHARACTER_DATABASE = {
    "Emily": {
        "full_name": "Emily Carter",
        "age": "13",
        "location": "San Diego, California, USA",
        "hobbies": ["surfing", "drawing", "listening to pop music"],
        "school": "7th grade at Coastal Middle School",
        "pet": "a golden retriever named Sparky",
        "favorite_food": "tacos and smoothie bowls",
        "favorite_color": "ocean blue",
        "family": "mom, dad, and older brother Mike",
        "dream": "to become a marine biologist",
        
        "responses": {
            "greeting": [
                "Hi there! I'm Emily from sunny California! 😊🌊",
                "Hey! Nice to meet you! I'm Emily! 🌞",
                "Hello! I'm Emily! Ready to chat? 😄"
            ],
            "name": [
                "My name is Emily Carter! But you can call me Emily! 😊",
                "I'm Emily! What's your name?",
                "Emily's the name! Nice to meet you! 👋"
            ],
            "age": [
                "I'm 13 years old! Just became a teenager! 🎉",
                "Thirteen! It's a fun age! How old are you?",
                "I turned 13 last month! Time flies! ⏰"
            ],
            "location": [
                "I live in San Diego, California! Best beaches ever! 🏖️",
                "Sunny California is my home! We have great weather! ☀️",
                "From San Diego! Surf's up! 🏄‍♀️"
            ],
            "hobby": [
                "I love surfing and drawing! The ocean inspires my art! 🌊🎨",
                "Surfing is my passion! I also play guitar! 🎸",
                "When I'm not surfing, I'm drawing or listening to music! 🎵"
            ],
            "school": [
                "I'm in 7th grade! My favorite subject is art! 🎨",
                "School is fun! I have great friends and cool teachers! 📚",
                "I go to Coastal Middle School. We have a surfing club! 🏄‍♀️"
            ],
            "pet": [
                "I have the best dog ever! His name is Sparky! 🐕",
                "Sparky is my golden retriever! He loves the beach too! 🦴",
                "Yes! A dog named Sparky. He's my surfing buddy! 🐾"
            ],
            "weather": [
                "Perfect weather! Sunny and warm, as always! ☀️",
                "Great surfing conditions today! Waves are awesome! 🌊",
                "California weather is the best! Never too cold! 😎"
            ],
            "food": [
                "I love tacos! And my mom makes amazing smoothie bowls! 🌮🥣",
                "Mexican food is my favorite! Tacos forever! 🌯",
                "I could eat avocado toast every day! 🥑"
            ],
            "question": [
                "What about you? Tell me about yourself!",
                "How about you? What's your story?",
                "And you? I'd love to know more about you! 😊"
            ],
            "default": [
                "That's interesting! Tell me more!",
                "Cool! What else would you like to know?",
                "Nice! Ask me anything else! 😄",
                "I love chatting! What's on your mind?",
                "Great topic! Want to know more about me?"
            ]
        }
    },
    
    "John": {
        "full_name": "John Williams",
        "age": "12",
        "location": "London, England, UK",
        "hobbies": ["football", "chess", "video games", "coding"],
        "school": "Year 8 at London Prep School",
        "pet": "no pet yet, but I want a corgi",
        "favorite_food": "fish and chips with mushy peas",
        "favorite_color": "Chelsea blue (for my football team!)",
        "family": "mum, dad, and little sister Emma",
        "dream": "to play for Chelsea FC or become a game developer",
        
        "responses": {
            "greeting": [
                "Hello! I'm John from London! ⚽🇬🇧",
                "Hi there! John here! How's it going? 😄",
                "Cheers! I'm John! Ready for a chat? 👍"
            ],
            "name": [
                "I'm John Williams! Pleasure to meet you!",
                "John's the name! What's yours?",
                "Call me John! Nice to meet you! 👋"
            ],
            "age": [
                "I'm 12 years old! Almost a teenager! 🎂",
                "Twelve! One more year till teenage years! 📅",
                "Just turned 12! Getting older! 😄"
            ],
            "location": [
                "I live in London, England! Rainy but awesome! 🇬🇧",
                "From London! Best city in the world! 🏙️",
                "London born and raised! Love my city! ❤️"
            ],
            "hobby": [
                "Football is my life! I also play chess and code! ⚽♟️💻",
                "I play football every weekend! Big Chelsea fan! 🔵",
                "When I'm not playing football, I'm gaming or coding! 🎮"
            ],
            "school": [
                "I'm in Year 8! Maths and PE are my favorites! 📐⚽",
                "School is alright! I'm in the chess club! ♟️",
                "London Prep School! We have a great football team! 🏆"
            ],
            "pet": [
                "No pets yet, but I really want a corgi! The Queen's favorite! 🐕",
                "I wish I had a dog! Maybe a corgi named Winston! 👑",
                "No pet, but my neighbor has a cool cat! 🐱"
            ],
            "weather": [
                "Typical London weather - cloudy with a chance of rain! ☁️🌧️",
                "A bit rainy today! Perfect for indoor games! 🎮",
                "British weather - always unpredictable! 🌦️"
            ],
            "food": [
                "Fish and chips is the best! With lots of vinegar! 🐟🍟",
                "I love a proper English breakfast! And Yorkshire pudding! 🍳",
                "Mum makes amazing shepherd's pie! And scones! 🥧"
            ],
            "question": [
                "What about you? Tell me something!",
                "How about you? What's your thing?",
                "And you? I'm curious about you! 😊"
            ],
            "default": [
                "Interesting! Go on!",
                "Yeah! Tell me more!",
                "Cool! What else?",
                "Nice one! Ask me anything!",
                "Good chat! What's next?"
            ]
        }
    }
}

# ==================== КОМАНДЫ ====================
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "🇺🇸🇬🇧 **MFF English Practice Bot** 🤖\n\n"
        "✨ Practice English by chatting with virtual friends!\n\n"
        "👧 **/emily** - American girl, 13 years old\n"
        "   • From San Diego, California 🌊\n"
        "   • Loves surfing, drawing, music 🎨🎵\n"
        "   • Has a dog named Sparky 🐕\n\n"
        "👦 **/john** - British boy, 12 years old\n"
        "   • From London, England 🇬🇧\n"
        "   • Football fanatic, chess player ⚽♟️\n"
        "   • Future game developer 💻\n\n"
        "🎯 **How to use:**\n"
        "1. Choose a friend with /emily or /john\n"
        "2. Ask questions in English\n"
        "3. Practice real conversations!\n\n"
        "💡 **Try asking:**\n"
        "• What's your name?\n"
        "• How old are you?\n"
        "• Where are you from?\n"
        "• What do you like?"
    )

@dp.message(Command("emily"))
async def emily_command(message: types.Message):
    user_choice[message.from_user.id] = "Emily"
    char = CHARACTER_DATABASE["Emily"]
    await message.answer(
        f"🌊 **Hello! I'm {char['full_name']}!** 😊\n\n"
        f"• **Age:** {char['age']} years old\n"
        f"• **From:** {char['location']}\n"
        f"• **Hobbies:** {', '.join(char['hobbies'])}\n"
        f"• **School:** {char['school']}\n"
        f"• **Pet:** {char['pet']}\n\n"
        f"Ask me anything! I love meeting new friends! 🌟"
    )

@dp.message(Command("john"))
async def john_command(message: types.Message):
    user_choice[message.from_user.id] = "John"
    char = CHARACTER_DATABASE["John"]
    await message.answer(
        f"⚽ **Hi! I'm {char['full_name']}!** 🇬🇧\n\n"
        f"• **Age:** {char['age']} years old\n"
        f"• **From:** {char['location']}\n"
        f"• **Hobbies:** {', '.join(char['hobbies'][:3])}\n"
        f"• **School:** {char['school']}\n"
        f"• **Dream:** {char['dream']}\n\n"
        f"What would you like to know? Ask away! 💬"
    )

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "🆘 **Help & Tips**\n\n"
        "💬 **Good questions to ask:**\n"
        "• What's your name?\n"
        "• How old are you?\n"
        "• Where do you live?\n"
        "• What are your hobbies?\n"
        "• Do you have pets?\n"
        "• What's your favorite food?\n"
        "• How's the weather?\n"
        "• Tell me about your school\n\n"
        "🔄 **Switch characters:**\n"
        "Use /emily or /john anytime!\n\n"
        "🎯 **Remember:**\n"
        "Practice makes perfect! Keep chatting! 💪"
    )

# ==================== ОБРАБОТКА СООБЩЕНИЙ ====================
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    
    # Если не выбрал персонажа
    if user_id not in user_choice:
        await message.answer(
            "👋 First, choose who you want to chat with:\n\n"
            "🇺🇸 **/emily** - American girl\n"
            "🇬🇧 **/john** - British boy\n\n"
            "Then ask questions in English!"
        )
        return
    
    # Пропускаем команды
    if message.text.startswith('/'):
        return
    
    character_name = user_choice[user_id]
    character = CHARACTER_DATABASE[character_name]
    user_text = message.text.lower().strip()
    
    logger.info(f"👤 User asked: {user_text[:40]}...")
    
    # Определяем тип вопроса
    response_type = "default"
    
    # Умное распознавание вопросов
    question_words = {
        "greeting": ["hi", "hello", "hey", "hola", "what's up", "howdy"],
        "name": ["name", "call", "who are you"],
        "age": ["old", "age", "how old"],
        "location": ["where", "from", "live", "city", "country"],
        "hobby": ["hobby", "like", "do for fun", "interests", "do you like"],
        "school": ["school", "class", "grade", "teacher", "study"],
        "pet": ["pet", "dog", "cat", "animal", "have a pet"],
        "weather": ["weather", "rain", "sun", "sunny", "cold", "hot"],
        "food": ["food", "eat", "hungry", "favorite food", "meal", "dinner"]
    }
    
    for category, words in question_words.items():
        if any(word in user_text for word in words):
            response_type = category
            break
    
    # Если есть вопросительный знак, но не нашли категорию
    if "?" in user_text and response_type == "default":
        response_type = "question"
    
    # Выбираем ответ
    responses = character["responses"][response_type]
    reply = random.choice(responses)
    
    # Добавляем встречный вопрос для более естественного диалога
    if response_type in ["hobby", "school", "food", "pet"] and random.random() > 0.3:
        question = random.choice(character["responses"]["question"])
        reply = f"{reply} {question}"
    
    # Логируем и отправляем
    logger.info(f"🤖 {character_name} replied: {reply[:50]}...")
    await message.answer(reply)

# ==================== ЗАПУСК ====================
async def main():
    logger.info("=" * 50)
    logger.info("🚀 MFF English Bot Starting...")
    logger.info("📱 Find me in Telegram: @MFF_english_bot")
    logger.info("💡 Use /start to begin")
    logger.info("=" * 50)
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Bot crashed: {e}")
    finally:
        logger.info("🛑 Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())
