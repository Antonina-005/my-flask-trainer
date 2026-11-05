import pytest  # type: ignore

from app import PYTHON_DATA, app


@pytest.fixture
def client():
    """Создает тестовый клиент для нашего Flask-приложения"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Проверяем, что главная страница открывается и содержит нужный текст"""
    response = client.get('/')
    assert response.status_code == 200
    # Декодируем байты ответа в обычный текст и проверяем наличие русской строки
    assert "🐍 Мой интерактивный тренажер Python" in response.data.decode('utf-8')

def test_topic_page_success(client):
    """Проверяем динамические страницы (например, тему venv)"""
    response = client.get('/topic/venv')
    assert response.status_code == 200
    # Декодируем ответ сервера в текст и проверяем наличие заголовка
    assert f"<h1>{PYTHON_DATA['venv']['title']}" in response.data.decode('utf-8')

def test_topic_page_404(client):
    """Проверяем, что несуществующая тема выдает ошибку 404"""
    response = client.get('/topic/unknown-topic-name')
    assert response.status_code == 404
