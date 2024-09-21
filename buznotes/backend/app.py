from flask import Flask, render_template, request, redirect, session, flash, jsonify
from fastapi import FastAPI
from models import db, User, Note
from translate_service import translate_text
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# FastAPI для обработки API-запросов
fastapi_app = FastAPI()

# Flask роуты

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect('/editor')
        else:
            flash('Неверный ввод')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        language = request.form['language']
        new_user = User(username=username, password=password, language=language)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/editor')
    return render_template('register.html')

@app.route('/editor')
def editor():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('editor.html')

@app.route('/notes')
def notes():
    if 'user_id' not in session:
        return redirect('/login')
    user = User.query.get(session['user_id'])
    notes = Note.query.filter_by(user_id=user.id).all()
    return render_template('notes.html', notes=notes)

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
