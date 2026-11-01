import os
import asyncio
from fastapi import FastAPI, Request
from google import genai

app = FastAPI()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.get("/")
@app.head("/")
async def health_check():
    return {"status": "ok"}

@app.post("/")
async def main(request: Request):
    body = await request.json()
    user_text = body["request"]["original_utterance"]
    
    if not user_text:
        user_text = "Привет! Я готов к общению."

    try:
        response = await asyncio.wait_for(
            client.aio.models.generate_content(
                model="gemini-3.8-flash",  # Вернули актуальную модель
                contents=user_text,
                config={"max_output_tokens": 50} # Жестко ограничили ответ (около 2-3 предложений)
            ),
            timeout=4.4  # Даем максимально возможное время
        )
        answer = response.text
    except asyncio.TimeoutError:
        # Если Gemini не успел, отдаём быструю заглушку
        print("ТАЙМАУТ GEMINI")
        answer = "Извините, я задумался. Попробуйте спросить еще раз."
    except Exception as e:
        print("ОШИБКА GEMINI:", e)
        answer = "Произошла ошибка. Попробуйте позже."

    return {
        "version": body["version"],
        "session": body["session"],
        "response": {
            "end_session": False,
            "text": answer
        }
    }
