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
        "example": "if True:\n    print('4 spaces')",
    },
    "sql": {
        "title": "Базы данных и основы SQL (Спринт 5)",
        "desc": "Язык запросов к базам данных. Базовый инструмент для Django.",
        "cheat_sheet": [
            "SELECT * FROM table; — выбрать все данные",
            "WHERE condition — фильтрация по условию",
            "INSERT INTO table VALUES — добавить запись",
        ],
        "example": "SELECT name FROM users WHERE age >= 18;",
    },
    "cs": {
        "title": "Computer Science: Алгоритмы",
        "desc": "Оценка эффективности кода и скорость его работы.",
        "cheat_sheet": [
            "O(1) — константное время (поиск в dict)",
            "O(n) — линейное время (поиск в list)",
            "Стек (Stack) — принцип LIFO (последний пришел)",
        ],
        "example": 'user = {"id": 42}\nprint(user["id"])  # Работает за O(1)',
    },
    "type_hinting": {
        "title": "Аннотация типов (Type Hinting)",
        "desc": "Подсказки для разработчика и линтеров, какие типы данных ожидает и возвращает функция.",
        "cheat_sheet": [
            "def calc(a: int, b: int) -> int: — синтаксический сахар для типов",
            "Помогает VS Code мгновенно подсвечивать ошибки до запуска кода",
            "В Django аннотации типов сильно упрощают работу с большими проектами",
        ],
        "example": 'def greet(name: str) -> str:\n    return "Привет, " + name',
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
    correct_answer = ""

    if topic_id == "venv":
        correct_answer = "source venv/bin/activate"
    elif topic_id == "github":
        correct_answer = "git push"
    elif topic_id == "pytest":
        correct_answer = "pytest -v"
    elif topic_id == "decorators":
        correct_answer = "@wraps(func)"
    elif topic_id == "flask-pro":
        correct_answer = "request.form.get"
    elif topic_id == "oop":
        correct_answer = "self"
    elif topic_id == "indentation":
        correct_answer = "4"
    elif topic_id == "sql":
        correct_answer = "SELECT"
    elif topic_id == "cs":
        correct_answer = "O(1)"
    elif topic_id == "type_hinting":
        correct_answer = "->"

    if request.method == "POST":
        user_answer = request.form.get("quiz_input", "").strip()

        if topic_id == "venv" and user_answer == correct_answer:
            result_message = "🎉 Верно! Окружение активно."
        elif topic_id == "github" and user_answer == correct_answer:
            result_message = "🚀 Супер! Код улетел в облако."
        elif topic_id == "pytest" and user_answer in ["pytest", "pytest -v"]:
            result_message = "✅ Отлично! Тесты запущены."
        elif topic_id == "decorators" and (
            "wraps" in user_answer.lower() or user_answer == correct_answer
        ):
            result_message = "🎯 Верно! Метаданные сохранены."
        elif topic_id == "flask-pro" and (
            "form.get" in user_answer or "request.form" in user_answer
        ):
            result_message = "🍦 Отлично! Забираем данные формы."
        elif topic_id == "oop" and user_answer.lower() == correct_answer:
            result_message = "🦾 Пять баллов! self привязывает метод к объекту."
        elif topic_id == "indentation" and user_answer == correct_answer:
            result_message = "📐 Идеально! 4 пробела по PEP 8."
        elif topic_id == "sql" and user_answer.upper() == correct_answer:
            result_message = "🗄 Правильно! SELECT запрашивает данные из БД."
        elif topic_id == "cs" and ("1" in user_answer or "o(1)" in user_answer.lower()):
            result_message = "⚡️ Супер! Поиск в словаре — это мгновенный O(1)."
        elif topic_id == "type_hinting":
            correct = "->"
            if correct in user_answer:
                result_message = (
                    "⚡️ Точно! Стрелочка указывает тип возвращаемого значения функции."
                )
            else:
                result_message = f"❌ Попробуй еще раз. Каким символом (стрелочкой) обозначается возвращаемый тип функции? Ответ: {correct}"
        else:
            result_message = "❌ Попробуй еще раз, загляни в подсказку ниже!"

    return render_template(
        "topic.html",
        topic_id=topic_id,
        data=data,
        result_message=result_message,
        user_answer=user_answer,
        correct_answer=correct_answer,
    )


if __name__ == "__main__":
    app.run(debug=True, port=8080)
