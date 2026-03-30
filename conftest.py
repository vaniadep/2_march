import pytest
import requests
from schemas.user import UserSchema


@pytest.fixture(scope="session")
def base_url():
    """Фикстура возвращает базовый URL API."""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api_session(base_url):
    """Сессия requests для эффективного выполнения запросов."""
    session = requests.Session()
    session.base_url = base_url
    yield session
    session.close()


@pytest.fixture
def get_user(api_session):
    """Фабрика-фикстура для получения пользователя по ID."""
    def _get_user(user_id: int) -> UserSchema:
        response = api_session.get(f"{api_session.base_url}/users/{user_id}")
        response.raise_for_status()
        return UserSchema.model_validate(response.json())
    return _get_user