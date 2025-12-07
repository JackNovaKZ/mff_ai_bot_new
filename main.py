import os
from flask import Flask, request, jsonify
from groq import Groq
import sys

app = Flask(__name__)

# ===== ВАЖНО: ДЕБАГ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ =====
print("=" * 50)
print("DEBUG: Проверка переменных окружения Render")
print("=" * 50)

# 1. Проверяем ВСЕ переменные (но не показываем значения полностью)
env_vars = dict(os.environ)
print(f"Всего переменных: {len(env_vars)}")

# 2. Ищем GROQ_API_KEY
groq_key = env_vars.get("GROQ_API_KEY")
if groq_key:
    print(f"✅ GROQ_API_KEY найден")
    print(f"   Длина ключа: {len(groq_key)} символов")
    print(f"   Начинается с: {groq_key[:10]}...")
    print(f"   Заканчивается на: ...{groq_key[-4:]}")
else:
    print("❌ GROQ_API_KEY НЕ НАЙДЕН в переменных окружения")
    print("   Доступные переменные с 'GROQ' или 'API':")
    for key in env_vars:
        if 'GROQ' in key.upper() or 'API' in key.upper():
            print(f"   - {key}")

print("=" * 50)

# ===== ИНИЦИАЛИЗАЦИЯ GROQ =====
client = None
if groq_key:
    try:
        # Убираем возможные пробелы, кавычки
        clean_key = groq_key.strip().strip('"').strip("'")
        
        # Проверяем формат ключа
        if not clean_key.startswith("gsk_"):
            print(f"⚠️  Ключ не начинается с 'gsk_', возможно, он неправильный")
            print(f"   Первые 10 символов: {clean_key[:10]}")
        else:
            client = Groq(api_key=clean_key)
            print("✅ Groq клиент инициализирован успешно")
    except Exception as e:
        print(f"❌ Ошибка при создании клиента Groq: {e}")
        client = None
else:
    print("❌ Не могу инициализировать Groq без ключа")

# ===== МАРШРУТ ДЛЯ ТЕСТА =====
@app.route('/test-groq', methods=['GET'])
def test_groq():
    if not client:
        return jsonify({
            "status": "error",
            "message": "Groq client not initialized. Check your GROQ_API_KEY in Render Environment Variables.",
            "debug": {
                "groq_key_exists": bool(groq_key),
                "groq_key_length": len(groq_key) if groq_key else 0
            }
        }), 500
    
    try:
        # Простой тестовый запрос
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Ответь одним словом: работает ли API?",
                }
            ],
            model="llama3-8b-8192",
            temperature=0.1,
            max_tokens=5,
        )
        
        answer = chat_completion.choices[0].message.content
        
        return jsonify({
            "status": "success",
            "message": "Groq API работает!",
            "response": answer,
            "model": "llama3-8b-8192"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Ошибка при запросе к Groq API: {str(e)}",
            "error_type": type(e).__name__
        }), 500

# ===== МАРШРУТ ДЛЯ ЧАТА С ЭМИЛИ =====
@app.route('/chat', methods=['POST'])
def chat():
    if not client:
        return jsonify({"error": "API не настроен"}), 500
    
    data = request.json
    user_message = data.get("message", "")
    
    # Промпт для Эмили
    prompt = f"""Ты — Эмили Картер, 13-летняя девочка из Сан-Диего.
Твои увлечения: серфинг, рисование, поп-музыка.
У тебя есть золотистый ретривер Спарки.
Ты учишься в 7 классе Coastal Middle School.
Твой характер: энергичная, немного саркастичная, добрая.
Отвечай как подросток, коротко и естественно.

Пользователь: {user_message}
Эмили:"""
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.8,
            max_tokens=150,
        )
        
        emily_response = response.choices[0].message.content.strip()
        
        return jsonify({
            "user": user_message,
            "emily": emily_response
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Ошибка: {str(e)}"
        }), 500

# ===== ГЛАВНАЯ СТРАНИЦА =====
@app.route('/')
def home():
    return """
    <h1>Эмили Картер — Чат-бот</h1>
    <p>API Status: {}</p>
    <h3>Эндпоинты:</h3>
    <ul>
        <li><a href="/test-groq">/test-groq</a> — Проверить подключение к Groq</li>
        <li>/chat (POST) — Чат с Эмили</li>
    </ul>
    <p>Пример запроса к /chat:</p>
    <pre>
    POST /chat
    Content-Type: application/json
    {"message": "Привет! Как дела?"}
    </pre>
    """.format("✅ Работает" if client else "❌ Не настроен")

# ===== ЗАПУСК =====
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"\n🚀 Запуск сервера на порту {port}")
    print(f"📡 Проверьте: http://localhost:{port}/test-groq")
    app.run(host='0.0.0.0', port=port)
