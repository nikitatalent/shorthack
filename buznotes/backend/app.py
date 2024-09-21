from flask import Flask, render_template, request, redirect, session, flash, jsonify
from werkzeug.urls import url_quote
from .models import db, User, Note
from .translate_service import translate_text
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

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

from starlette.responses import FileResponse 

@app.get("/editor")
async def read_index():
    return FileResponse('../frontend/templates/editor.html')