import os
import asyncio
from aioalice import Dispatcher, get_new_configured_app
from aioalice.types import Message
from google import genai

# Инициализация клиента Gemini
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
dp = Dispatcher()

@dp.message()
async def handle_message(message: Message):
    # Быстрый ответ, если пользователь просто запустил навык
    if not message.text:
        return message.response("Привет! Я готов к общению.")

    try:
        # Запускаем запрос к Gemini с таймаутом
        response = await asyncio.wait_for(
            client.aio.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=message.text,
                config={"max_output_tokens": 150}
            ),
            timeout=4.0  # Ждем не дольше 4 секунд
        )
        answer = response.text
    except asyncio.TimeoutError:
        answer = "Извините, я задумался. Попробуйте спросить еще раз."
    except Exception as e:
        print("ОШИБКА GEMINI:", e)
        answer = "Произошла ошибка. Попробуйте позже."

    return message.response(answer)

# Создаем приложение FastAPI
app = get_new_configured_app(dispatcher=dp, path="/")
