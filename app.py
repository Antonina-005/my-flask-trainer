from flask import Flask, abort, render_template, request  # type: ignore  # noqa: F401, RUF100

app = Flask(__name__)

# Наша интерактивная база знаний Python (фишки и шпаргалки)
PYTHON_DATA = {
    'venv': {
        'title': 'Виртуальное окружение (venv) на Mac',
        'desc': 'Нужно, чтобы библиотеки одного проекта не конфликтовали с другими.',
        'cheat_sheet': [
            'python3 -m venv venv — создать окружение (делается 1 раз)',
            'source venv/bin/activate — АКТИВИРОВАТЬ окружение (каждый раз при открытии терминала)',
            'deactivate — выйти из окружения',
            'pip install -r requirements.txt — установить все библиотеки проекта одной командой'
        ],
        'example': '# Как понять, что заработало?\n(venv) user@MacBook my_flask_app % \n# Перед строкой ввода ОБЯЗАТЕЛЬНО должно быть написано (venv)!'
    },
    'pytest': {
        'title': 'Тестирование с PyTest',
        'desc': 'Библиотека для автоматической проверки твоего кода на ошибки.',
        'cheat_sheet': [
            'pip install pytest — установка тестировщика',
            'pytest — запустить все тесты в папке',
            'pytest -v — запустить тесты с подробным отчетом',
            'Имена файлов тестов ОБЯЗАТЕЛЬНО должны начинаться с "test_"'
        ],
        'example': '# Файл test_logic.py\ndef test_add():\n    assert 2 + 2 == 4  # Если условие верно, тест пройден\n    assert len([1, 2]) == 2'
    },
    'github': {
        'title': 'Как пушить проект на GitHub',
        'desc': 'Пошаговый алгоритм, как сохранить свой код в облако и показать кураторам Яндекс Платформы.',
        'cheat_sheet': [
            'git init — инициализировать Git в папке (1 раз на проект)',
            'echo "venv/" > .gitignore — сказать Гиту НЕ сохранять виртуальное окружение',
            'git add . — добавить все файлы проекта в индекс для сохранения',
            'git commit -m "First commit" — сохранить изменения локально с комментарием',
            'git branch -M main — переименовать главную ветку в main',
            'git remote add origin ССЫЛКА_НА_РЕПОЗИТОРИЙ — связать с сайтом GitHub (1 раз)',
            'git push -u origin main — отправить код на GitHub 🚀'
        ],
        'example': '# Быстрый цикл обновлений кода (сделала изменения -> отправила):\ngit add .\ngit commit -m "fix style"\ngit push'
    },
    'lists': {
        'title': 'Срезы и методы списков',
        'desc': 'Списки — это изменяемые структуры данных. Самая мощная фишка — срезы!',
        'cheat_sheet': [
            'my_list[start:stop:step] — формула среза',
            'my_list[::-1] — быстрый разворот списка',
            '.append(x) — добавить элемент в конец'
        ],
        'example': 'numbers = [1, 2, 3, 4]\nprint(numbers[::-1])  # Выведет:'
    }
}

# 1. Главная страница со списком тем
@app.route('/')
def index():
    return render_template('index.html', topics=PYTHON_DATA)

# 2. Динамическая страница для каждой темы
@app.route('/topic/<topic_id>', methods=['GET', 'POST'])
def topic(topic_id):
    if topic_id not in PYTHON_DATA:
        abort(404)
    
    data = PYTHON_DATA[topic_id]
    result_message = None
    user_answer = ""
    
    # Сюда мы попадем, когда ты нажмешь кнопку "Проверить" на сайте
    if request.method == 'POST':
        user_answer = request.form.get('quiz_input', '').strip()
        
        # Простая логика проверки для каждой темы
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
                result_message = "❌ Линтер недоволен. Введи 'pytest' или 'pytest -v'"
                
        else:
            result_message = "👍 Спасибо за ответ! Тренажер для этой темы в разработке."

    return render_template(
        'topic.html', 
        topic_id=topic_id, 
        data=data, 
        result_message=result_message,
        user_answer=user_answer
    )

if __name__ == '__main__':
    # Теперь сайт будет жить на порту 8080
    app.run(debug=True, port=8080)
