├── README.md
├── app.py
├── models.py
├── requirements.txt
├── static
│   └── style.css
├── templates
│   ├── base.html
│   └── index.html
├── docs
│   └── conf.py (placeholder for Sphinx)
└── diagram.png (placeholder for UML)

# README.md
"""
# To-Do List Web App

Prosta aplikacja internetowa do zarządzania zadaniami zbudowana za pomocą Flaska i SQLite.

## Funkcje
- Dodawanie zadań
- Oznaczanie zadań jako wykonane
- Usuwanie zadań
- Prosty interfejs przeglądarkowy (GUI)

## Typ interakcji
- GUI (HTML/CSS za pomocą szablonów Flask)

## Stos technologiczny
- Python
- Flask
- SQLite (ORM SQLAlchemy)
- HTML/CSS

## Struktura projektu
```
app.py           # Główna aplikacja Flaska
models.py        # Modele bazy danych
templates/       # Szablony HTML
static/          # Pliki CSS
requirements.txt # Wymagane biblioteki
docs/            # Folder dokumentacji (gotowy pod Sphinx)
```

## Instalacja
```bash
pip install -r requirements.txt
python app.py
```

## Opcjonalnie (budowanie za pomocą PyInstaller)
```bash
pyinstaller --onefile app.py
```

## Dokumentacja
Użyj `sphinx-quickstart` w katalogu `docs/`, aby zainicjować dokumentację.

## Status
Wszystkie podstawowe funkcje zostały zaimplementowane.
"""

# requirements.txt
flask
sqlalchemy

# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unikalne ID zadania
    title = db.Column(db.String(100), nullable=False)  # Tytuł zadania
    done = db.Column(db.Boolean, default=False)  # Status wykonania

# app.py
from flask import Flask, render_template, request, redirect
from models import db, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # Ścieżka do bazy danych SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Wyłączenie ostrzeżeń

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()  # Tworzenie tabel przy pierwszym uruchomieniu

@app.route('/')
def index():
    tasks = Task.query.all()  # Pobieranie wszystkich zadań
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')  # Pobieranie tytułu z formularza
    if title:
        db.session.add(Task(title=title))  # Dodawanie nowego zadania
        db.session.commit()
    return redirect('/')

@app.route('/done/<int:task_id>')
def done(task_id):
    task = Task.query.get(task_id)  # Pobieranie zadania po ID
    if task:
        task.done = not task.done  # Przełączanie statusu wykonania
        db.session.commit()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)  # Pobieranie zadania po ID
    if task:
        db.session.delete(task)  # Usuwanie zadania
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)  # Uruchomienie aplikacji w trybie debugowania

# templates/base.html
<!DOCTYPE html>
<html>
<head>
    <title>To-Do List</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>

# templates/index.html
{% extends 'base.html' %}

{% block content %}
<h1>To-Do List</h1>
<form action="/add" method="post">
    <input type="text" name="title" placeholder="Wpisz zadanie">
    <button type="submit">Dodaj</button>
</form>
<ul>
    {% for task in tasks %}
    <li class="{% if task.done %}done{% endif %}">
        {{ task.title }}
        <a href="/done/{{ task.id }}">[Wykonane]</a>
        <a href="/delete/{{ task.id }}">[Usuń]</a>
    </li>
    {% endfor %}
</ul>
{% endblock %}

# static/style.css
body {
    font-family: Arial, sans-serif;
    background: #f9f9f9;
    padding: 20px;
}
.container {
    max-width: 600px;
    margin: 0 auto;
    background: white;
    padding: 20px;
    border-radius: 8px;
}
.done {
    text-decoration: line-through;
    color: gray;
}
