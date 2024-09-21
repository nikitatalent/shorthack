from flask import render_template, request, redirect, url_for, session, flash
from .models import db, User, Note
from werkzeug.security import generate_password_hash, check_password_hash
import requests

def init_routes(app):
    
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            login = request.form['login']
            password = request.form['password']
            user = User.query.filter_by(login=login).first()
            
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect(url_for('editor'))
            else:
                flash('Неверный логин или пароль')
                return render_template('login.html')

        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            login = request.form['login']
            password = request.form['password']
            language = request.form['language']

            hashed_password = generate_password_hash(password)
            new_user = User(login=login, password=hashed_password, language=language)
            db.session.add(new_user)
            db.session.commit()
            
            session['user_id'] = new_user.id
            return redirect(url_for('editor'))

        return render_template('register.html')

    @app.route('/editor', methods=['GET', 'POST'])
    def editor():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            text = request.form['text']
            user = User.query.get(session['user_id'])
            
            # Пример использования внешнего API для перевода (вместо реального API используем заглушку)
            translated_text = f"Переведенный текст: {text}"

            new_note = Note(content=translated_text, user_id=user.id)
            db.session.add(new_note)
            db.session.commit()

            return render_template('editor.html', translation=translated_text)
        
        return render_template('editor.html')

    @app.route('/notes')
    def notes():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        user_notes = user.notes
        return render_template('notes.html', notes=user_notes)
    
    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('index'))
