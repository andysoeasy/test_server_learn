import os
from dotenv import load_dotenv

from sqlalchemy import String, ForeignKey, BigInteger, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator
import re

load_dotenv()

engine = create_async_engine(url=os.getenv('POSTGRES_URL'))
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


# ---------------------- DATABASE ORM MODELS -----------------------


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = 'items'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    weight: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(300))
    cost: Mapped[int] = mapped_column()
    category: Mapped[int] = mapped_column()
    image_name: Mapped[str] = mapped_column(String(100))
    

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(50))


class Order(Base):
    __tablename__ = 'orders'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    tg_id = mapped_column(BigInteger)
    items: Mapped[str] = mapped_column(String(500))
    total_cost: Mapped[int] = mapped_column()
    date_create_order: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    type_of_delivery: Mapped[str] = mapped_column(String(30))
    type_of_pay: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(300))
    address: Mapped[Optional[str]] = mapped_column(String(200))


# --------------------------- PYDENTIC SHEMAS -------------------------------
class ItemSchema(BaseModel):
    id: int = Field(default=1, description='Уникальный идентификатор позиции в меню', title='Уникальный идентификатор')
    weight: int = Field(default=1, gt=0, description='Вес позиции в граммах, не может быть равен 0 или быть меньше этого значения', title='Вес позиции')
    name: str = Field(default=..., min_length=2, max_length=100, description='Наименовании позиции, длина не может быть меньше 2 и больше 100 символов', title='Наименование')
    description: str = Field(default=..., min_length=1, max_length=300, description='Описание характеристик позиции меню, от 1 до 300', title='Описание позиции')
    cost: int = Field(default=100, gt=0, description='Стоимость позиции в меню, не может быть меньше 0 или равняться этому значению', title='Стоимость')
    category: int = Field(default=1, le=6, ge=1, description='Описание категории позиции в меню', title='Категория товара')
    image_name: str = Field(default=..., min_length=1, max_length=100, description='Описание пути, где хранится изображение, от 1 до 100 символов', title='Путь до изображения позиции')
    
    model_config = ConfigDict(from_attributes=True)
    

class OrderSchema(BaseModel):
    id: int = Field(default=1, description='Уникальный идентификатор заказа', title='Идентификатор заказа')
    user: int = Field(default=1, description='Уникальный идентификатор пользователя, который сделал заказ', title='Идентификатор пользователя')
    tg_id: int = Field(default=1, description='Уникальный идентификатор пользователя telegram, который сделал заказ', title='Telegram ID пользователя')
    items: str = Field(default=..., min_length=1, max_length=500, description='Позиции заказа, от 1 до 500 символов')
    total_cost: int = Field(default=..., gt=0, description='Общая стоимость заказа, должна быть больше нуля', title='Стоимость заказа')
    date_create_order: Optional[date] = Field(default=str(datetime.now()), description='Дата оформления заказа', title='Дата оформления заказа')
    type_of_pay: str = Field(default='Наличными при получении', min_length=15, max_length=50, description='Способ оплаты заказа: наличными при получении, картой при получении, картой на сайте. От 15 до 50 символов', title='Способ оплаты заказа')
    type_of_delivery: str = Field(default='Самовывоз', min_length=9, max_length=30, description='Способ доставки: самовывоз или доставка курьером. От 9 до 30 символов', title='Способ доставки')
    address: Optional[str] = Field(default='пгт Гвардейское, ул. Острякова, 27/1', min_length=10, max_length='200', description='Адрес доставки заказа. Заполняется только при выборе доставки курьером. От 10 до 200 символов', title='Адрес доставки')
    description: Optional[str] = Field(default='Описание заказа', min_length=0, max_length=300, description='Описание деталей заказа/пожеланий клиента. От 0 до 300 символов', title='Комментарий к заказу')
    
    @field_validator('date_create_order', mode='before')
    @classmethod
    def convert_datetime_to_data(cls, value):
        if isinstance(value, datetime):
            return value.date()
        return value
    
    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    tg_id: Optional[int] = Field(default=..., description='Telegram ID ползователя, данные которого нужно обновить', title='Telegram ID')
    name: Optional[str] = Field(default='Андрей', min_length=1, max_length=100, description='Новое имя пользователя', title='Имя пользователя')
    phone: Optional[str] = Field(default='+71234567890', min_length=12, max_length=12, description='Новый номер телефона полььзователя', title='Номер телефона')
    email: Optional[str] = Field(default='andrew@example.ru', min_length=1, max_length=50, description='Новая электронная почта пользователя', title='Электронная почта')

    @field_validator('phone')
    @classmethod
    def validate_phone_number(cls, value: str):
        if not re.match(r'^\+\d{11}', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать 11 цифр')
        return value
    
    @field_validator('email')
    @classmethod
    def validate_email_address(cls, value: str):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', value):
            raise ValueError('Адрес электронной почты должен быть в формате "email@example.com"')
        return value
    
    
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)