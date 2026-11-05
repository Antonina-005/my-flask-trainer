from flask import Flask, abort, render_template, request

app = Flask(__name__)

# Полная база знаний с новыми темами
PYTHON_DATA = {
    'venv': {
        'title': 'Виртуальное окружение (venv) на Mac',
        'desc': 'Нужно, чтобы библиотеки одного проекта не конфликтовали с другими.',
        'cheat_sheet': [
            'python3 -m venv venv — создать окружение (делается 1 раз)',
            'source venv/bin/activate — АКТИВИРОВАТЬ окружение (каждый раз в терминале)',
            'deactivate — выйти из окружения'
        ],
        'example': '(venv) user@MacBook my_flask_app % \n# Перед строкой ввода ОБЯЗАТЕЛЬНО должно быть (venv)!'
    },
    'pytest': {
        'title': 'Тестирование с PyTest',
        'desc': 'Библиотека для автоматической проверки твоего кода на ошибки.',
        'cheat_sheet': [
            'pip install pytest — установка тестировщика',
            'pytest -v — запустить тесты с подробным отчетом',
            'Имена файлов тестов ОБЯЗАТЕЛЬНО должны начинаться с "test_"'
        ],
        'example': 'def test_add():\n    assert 2 + 2 == 4  # Если условие верно, тест пройден'
    },
    'github': {
        'title': 'Как пушить проект на GitHub',
        'desc': 'Пошаговый алгоритм, как сохранить свой код в облако.',
        'cheat_sheet': [
            'git init — инициализировать Git в папке',
            'git add . — добавить все файлы проекта в индекс',
            'git commit -m "Сообщение" — сохранить изменения локально',
            'git push — отправить код на GitHub 🚀'
        ],
        'example': 'git add .\ngit commit -m "fix style"\ngit push'
    },
    'decorators': {
        'title': 'Декораторы (Decorators)',
        'desc': 'Функции, расширяющие поведение другого кода без его изменения.',
        'cheat_sheet': [
            '@my_decorator — синтаксический сахар для применения',
            'from functools import wraps — импорт обязательного помощника',
            '@wraps(func) — сохраняет имя и docstring исходной функции'
        ],
        'example': 'def my_decor(func):\n    @wraps(func)\n    def wrapper(*args, **kwargs):\n        return func(*args, **kwargs)\n    return wrapper'
    },
    'flask-pro': {
        'title': 'Продвинутый Flask (Формы)',
        'desc': 'Работа с запросами пользователя и передача данных.',
        'cheat_sheet': [
            'request.form.get("input_name") — достать данные из POST-формы',
            'render_template("page.html", key=value) — передать переменную в HTML',
            'methods=["GET", "POST"] — разрешить обработку формы в роуте'
        ],
        'example': '@app.route("/quiz", methods=["POST"])\ndef quiz():\n    answer = request.form.get("quiz_input")'
    },
    'indentation': {
        'title': 'Отступы в Python и HTML (PEP 8)',
        'desc': 'Главное правило Python: один уровень вложенности = 4 пробела. Никаких табов!',
        'cheat_sheet': [
            'IndentationError — ошибка, если отступы разъехались',
            'TabError — смертный грех Python (смешивание Табов и Пробелов)',
            'В HTML (Jinja) отступы не ломают код, но нужны для читаемости блоков {% if %} и {% for %}'
        ],
        'example': 'def hello():\n    if True:\n        print("Здесь ровно 8 пробелов от края!")'
    }
}


@app.route('/')
def index():
    return render_template('index.html', topics=PYTHON_DATA)


@app.route('/topic/<topic_id>', methods=['GET', 'POST'])
def topic(topic_id):
    if topic_id not in PYTHON_DATA:
        abort(404)

    data = PYTHON_DATA[topic_id]
    result_message = None
    user_answer = ""

    if request.method == 'POST':
        user_answer = request.form.get('quiz_input', '').strip()

        if topic_id == 'venv':
            correct = "source venv/bin/activate"
            if user_answer == correct:
                result_message = "🎉 Абсолютно верно! Окружение активировано."
            else:
                result_message = f"❌ Не совсем так. Правильный ответ: {correct}"

        elif topic_id == 'github':
            correct = "git push"
            if user_answer == correct:
                result_message = "🚀 Супер! Код улетел в облако."
            else:
                result_message = f"❌ Ошибка в синтаксисе. Попробуй: {correct}"

        elif topic_id == 'pytest':
            correct = "pytest -v"
            if user_answer in ["pytest", "pytest -v"]:
                result_message = "✅ Отлично! Тесты запущены."
            else:
                result_message = f"❌ Попробуй еще раз. Ответ: {correct}"

        elif topic_id == 'decorators':
            correct = "@wraps(func)"
            if user_answer == correct or "wraps" in user_answer.lower():
                result_message = "🎯 Верно! @wraps сохраняет метаданные функции."
            else:
                result_message = f"❌ Используй встроенный декоратор: {correct}"

        elif topic_id == 'flask-pro':
            correct = "request.form.get"
            if "form.get" in user_answer or "request.form" in user_answer:
                result_message = "🍦 Отлично! Забираем данные через request.form."
            else:
                result_message = f"❌ Используй объект request: {correct}('поле')"

        elif topic_id == 'indentation':
            correct = "4"
            if user_answer == correct:
                result_message = "📐 Идеально! 4 пробела — золотой стандарт PEP 8."
            else:
                result_message = "❌ Нет, стандарт PEP 8 требует ровно 4 пробела!"

    return render_template(
        'topic.html',
        topic_id=topic_id,
        data=data,
        result_message=result_message,
        user_answer=user_answer
    )


if __name__ == '__main__':
    app.run(debug=True, port=8080)