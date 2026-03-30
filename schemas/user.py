from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class GeoSchema(BaseModel):
    """Схема географических координат."""
    lat: str = Field(
        ...,
        description="Широта в виде строки (диапазон: -90 до 90)",
        min_length=1,
        max_length=20,
        pattern=r'^-?\d+\.?\d*$'
    )
    lng: str = Field(
        ...,
        description="Долгота в виде строки (диапазон: -180 до 180)",
        min_length=1,
        max_length=20,
        pattern=r'^-?\d+\.?\d*$'
    )

    @field_validator("lat")
    @classmethod
    def validate_latitude(cls, v: str) -> str:
        """Валидация широты: диапазон от -90 до 90."""
        value = float(v)
        if not -90 <= value <= 90:
            raise ValueError(f"Широта должна быть в диапазоне [-90, 90], получено: {value}")
        return v

    @field_validator("lng")
    @classmethod
    def validate_longitude(cls, v: str) -> str:
        """Валидация долготы: диапазон от -180 до 180."""
        value = float(v)
        if not -180 <= value <= 180:
            raise ValueError(f"Долгота должна быть в диапазоне [-180, 180], получено: {value}")
        return v


class AddressSchema(BaseModel):
    """Схема адреса пользователя."""
    street: str = Field(
        ...,
        description="Название улицы",
        min_length=1,
        max_length=100
    )
    suite: str = Field(
        ...,
        description="Дополнительная информация об адресе (квартира, офис)",
        min_length=1,
        max_length=100
    )
    city: str = Field(
        ...,
        description="Город",
        min_length=1,
        max_length=100
    )
    zipcode: str = Field(
        ...,
        description="Почтовый индекс",
        min_length=1,
        max_length=20,
        pattern=r'^[\d\-]+$'
    )
    geo: GeoSchema = Field(
        ...,
        description="Географические координаты адреса"
    )


class CompanySchema(BaseModel):
    """Схема компании пользователя."""
    name: str = Field(
        ...,
        description="Название компании",
        min_length=1,
        max_length=100
    )
    catchPhrase: str = Field(
        ...,
        description="Корпоративный слоган компании",
        min_length=1,
        max_length=200
    )
    bs: str = Field(
        ...,
        description="Бизнес-направление компании (buzzwords)",
        min_length=1,
        max_length=200
    )


class UserSchema(BaseModel):
    """Основная схема пользователя."""
    id: int = Field(
        ...,
        description="Уникальный идентификатор пользователя",
        ge=1,
        le=1000
    )
    name: str = Field(
        ...,
        description="Полное имя пользователя",
        min_length=1,
        max_length=100
    )
    username: str = Field(
        ...,
        description="Уникальное имя пользователя для входа",
        min_length=1,
        max_length=50,
        pattern=r'^[a-zA-Z0-9_.\-]+$'
    )
    email: str = Field(
        ...,
        description="Электронная почта пользователя",
        min_length=5,
        max_length=100,
        pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    address: AddressSchema = Field(
        ...,
        description="Почтовый адрес пользователя"
    )
    phone: str = Field(
        ...,
        description="Номер телефона пользователя",
        min_length=1,
        max_length=50,
        pattern=r'^[\d\s\-\(\)x]+$'
    )
    website: str = Field(
        ...,
        description="Веб-сайт пользователя",
        min_length=1,
        max_length=100,
        pattern=r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    company: CompanySchema = Field(
        ...,
        description="Информация о компании, в которой работает пользователь"
    )