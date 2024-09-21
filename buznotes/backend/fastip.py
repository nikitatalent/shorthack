from fastapi import FastAPI

# FastAPI для обработки API-запросов
fastapi_app = FastAPI()

# API роуты FastAPI

@fastapi_app.post("/translate")
async def translate(data: dict):
    user_id = data.get('user_id')
    text = data.get('text')
    user = User.query.get(user_id)
    translated_text = translate_text(text, user.language)
    return {"translated_text": translated_text}

@fastapi_app.post("/save_note")
async def save_note(data: dict):
    user_id = data.get('user_id')
    text = data.get('text')
    new_note = Note(user_id=user_id, text=text)
    db.session.add(new_note)
    db.session.commit()
    return {"status": "success"}