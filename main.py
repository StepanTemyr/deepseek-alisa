import os
from fastapi import FastAPI, Request
from google import genai

app = FastAPI()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.post("/")
async def main(request: Request):
    body = await request.json()
    user_text = body["request"]["original_utterance"]
    
    # Если пользователь просто запустил навык (пустой запрос)
    if not user_text:
        user_text = "Привет! Я готов к общению."

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text
        )
        answer = response.text
    except Exception as e:
        print("ОШИБКА GEMINI:", e)
        answer = "Произошла ошибка при обращении к Gemini."

    return {
        "version": body["version"],
        "session": body["session"],
        "response": {
            "end_session": False,
            "text": answer
        }
    }
