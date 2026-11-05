from flask import Flask, abort, render_template, request

app = Flask(__name__)

PYTHON_DATA = {
    "venv": {
        "title": "Виртуальное окружение (venv) на Mac",
        "desc": "библиотеки проектов не конфликтуют.",
        "cheat_sheet": [
            "python3 -m venv venv - создать",
            "source venv/bin/activate - запустить",
            "deactivate - выйти",
        ],
        "example": "# Должно быть написано (venv)!",
    },
    "pytest": {
        "title": "Тестирование с PyTest",
        "desc": "Автоматическая проверка кода на ошибки.",
        "cheat_sheet": [
            "pip install pytest - поставить",
            "pytest -v - запустить тесты",
            "Имена файлов должны начинаться с test_",
        ],
        "example": "def test_add(): assert 2 + 2 == 4",
    },
    "github": {
        "title": "Как пушить проект на GitHub",
        "desc": "Сохранение кода в облако.",
        "cheat_sheet": [
            "git init - создать репозиторий",
            "git add . - добавить файлы",
            "git commit -m - сохранить локально",
            "git push - отправить 🚀",
        ],
        "example": "git add .\ngit commit\ngit push",
    },
    "decorators": {
        "title": "Декораторы (Decorators)",
        "desc": "Изменение логики функций.",
        "cheat_sheet": [
            "@my_decorator — запуск",
            "from functools import wraps — импорт",
            "@wraps(func) — спасает имя функции",
        ],
        "example": "def decor(f):\n @wraps(f)\n def w(): return f()\n return w",
    },
    "flask-pro": {
        "title": "Продвинутый Flask (Формы)",
        "desc": "Сбор информации из форм.",
        "cheat_sheet": [
            "request.form.get — чтение POST",
            "render_template — показ HTML",
            "methods=[GET, POST] — включить формы",
        ],
        "example": 'answer = request.form.get("quiz_input")',
    },
    "oop": {
        "title": "Основы ООП (Подготовка к Django)",
        "desc": "В Джанго все пишется на классах.",
        "cheat_sheet": [
            "class MyClass: — новый класс",
            "def __init__(self): — конструктор",
            "self — ссылка на текущий объект",
            "super().__init__() — вызов родителя",
        ],
        "example": "class Pet:\n def __init__(self, name):\n  self.name = name",
    },
    "indentation": {
        "title": "Отступы в Python (PEP 8)",
        "desc": "Один уровень равен 4 пробелам.",
        "cheat_sheet": [
            "IndentationError — уехали строки",
            "TabError — смесь табов и пробелов",
            "В HTML отступы нужны для красоты",
        ],
        "example": 'if True:\n    print("4 spaces")',
    },
}


@app.route("/")
def index():
    return render_template("index.html", topics=PYTHON_DATA)


@app.route("/topic/<topic_id>", methods=["GET", "POST"])
def topic(topic_id):
    if topic_id not in PYTHON_DATA:
        abort(404)

    data = PYTHON_DATA[topic_id]
    result_message = None
    user_answer = ""

    if request.method == "POST":
        user_answer = request.form.get("quiz_input", "").strip()

        if topic_id == "venv" and user_answer == "source venv/bin/activate":
            result_message = "🎉 Верно! Окружение активно."
        elif topic_id == "github" and user_answer == "git push":
            result_message = "🚀 Супер! Код улетел в облако."
        elif topic_id == "pytest" and user_answer in ["pytest", "pytest -v"]:
            result_message = "✅ Отлично! Тесты запущены."
        elif topic_id == "decorators" and (
            "wraps" in user_answer.lower() or user_answer == "@wraps(func)"
        ):
            result_message = "🎯 Верно! Метаданные сохранены."
        elif topic_id == "flask-pro" and (
            "form.get" in user_answer or "request.form" in user_answer
        ):
            result_message = "🍦 Отлично! Забираем данные формы."
        elif topic_id == "oop" and user_answer.lower() == "self":
            result_message = "🦾 Пять баллов! self привязывает метод к объекту."
        elif topic_id == "indentation" and user_answer == "4":
            result_message = "📐 Идеально! 4 пробела по PEP 8."
        else:
            result_message = "❌ Попробуй еще раз, загляни в шпору выше!"

    return render_template(
        "topic.html",
        topic_id=topic_id,
        data=data,
        result_message=result_message,
        user_answer=user_answer,
    )


if __name__ == "__main__":
    app.run(debug=True, port=8080)
