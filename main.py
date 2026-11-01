import os
from fastapi import FastAPI, Request
from google import genai

app = FastAPI()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Проверка для UptimeRobot, чтобы сервер не засыпал
@app.get("/")
@app.head("/")
async def health_check():
    return {"status": "ok"}

@app.post("/")
async def main(request: Request):
    body = await request.json()
    user_text = body["request"]["original_utterance"]
    
    # Если пользователь просто запустил навык (пустой запрос)
    if not user_text:
        user_text = "Привет! Я готов к общению."

    try:
        # Используем самую быструю модель Flash-Lite и ограничиваем длину ответа
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=user_text,
            config={"max_output_tokens": 150}
        )
        answer = response.text
    except Exception as e:
        print("ОШИБКА GEMINI:", e)
        answer = "Извините, не удалось получить ответ. Попробуйте спросить короче."

    return {
        "version": body["version"],
        "session": body["session"],
        "response": {
            "end_session": False,
            "text": answer
        }
    }
