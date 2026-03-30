import pytest
from schemas.user import UserSchema


@pytest.mark.parametrize("user_id", range(1, 11))
def test_user_schema_validation(get_user, user_id):
    """
    Параметризованный тест валидации схемы пользователя для всех 10 пользователей.
    
    Проверяет:
    - Успешную валидацию ответа API через Pydantic-схему
    - Корректность типов данных
    - Применение кастомных валидаторов (lat/lng)
    """
    user: UserSchema = get_user(user_id)
    
    assert user.id == user_id
    assert user.name
    assert user.username
    assert user.email
    assert user.phone
    assert user.website
    
    assert user.address.street
    assert user.address.city
    assert user.address.zipcode
    assert user.address.geo.lat
    assert user.address.geo.lng
    
    assert user.company.name
    assert user.company.catchPhrase
    assert user.company.bs
    
    lat_value = float(user.address.geo.lat)
    lng_value = float(user.address.geo.lng)
    assert -90 <= lat_value <= 90, f"Широта {lat_value} вне диапазона"
    assert -180 <= lng_value <= 180, f"Долгота {lng_value} вне диапазона"


def test_user_schema_field_descriptions():
    """Тест проверяет наличие описаний у полей схемы (Field description)."""
    user_fields = UserSchema.model_fields
    
    assert user_fields['id'].description is not None
    assert user_fields['name'].description is not None
    assert user_fields['email'].description is not None
    assert user_fields['address'].description is not None
    assert user_fields['company'].description is not None
    
    geo_fields = user_fields['address'].annotation.model_fields
    assert geo_fields['lat'].description is not None
    assert geo_fields['lng'].description is not None


@pytest.mark.parametrize("invalid_lat", ["-95.0", "95.0", "abc"])
def test_geo_latitude_validation(invalid_lat):
    """Тест валидации некорректных значений широты."""
    from schemas.user import GeoSchema
    from pydantic import ValidationError
    
    with pytest.raises(ValidationError):
        GeoSchema(lat=invalid_lat, lng="0.0")


@pytest.mark.parametrize("invalid_lng", ["-185.0", "185.0", "xyz"])
def test_geo_longitude_validation(invalid_lng):
    """Тест валидации некорректных значений долготы."""
    from schemas.user import GeoSchema
    from pydantic import ValidationError
    
    with pytest.raises(ValidationError):
        GeoSchema(lat="0.0", lng=invalid_lng)