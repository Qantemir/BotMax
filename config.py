import os
from dotenv import load_dotenv
from typing import Dict, List

# Load environment variables
load_dotenv()

# Environment
PRODUCTION: bool = os.getenv("ENVIRONMENT", "development").lower() == "production"

# Bot Configuration
BOT_TOKEN: str = os.getenv("BOT_TOKEN")
ADMIN_ID: int = int(os.getenv("ADMIN_ID", "0"))
ADMIN_CARD: str = os.getenv("ADMIN_CARD", "")

# MongoDB Configuration
MONGODB_URI: str = os.getenv("MONGODB_URI")
DB_NAME: str = os.getenv("DB_NAME", "maxshop_db")

# Shop Configuration
SHOP_NAME: str = os.getenv("SHOP_NAME", "MaxShop")
CURRENCY: str = os.getenv("CURRENCY", "TNG")
MIN_ORDER_AMOUNT: float = float(os.getenv("MIN_ORDER_AMOUNT", "100"))
MAX_ORDER_AMOUNT: float = float(os.getenv("MAX_ORDER_AMOUNT", "10000"))

# Product Categories
CATEGORIES: List[str] = [
    "Тестовая категория",
    "Тестовая категория 2",
    "Тестовая категория 3",
    "Тестовая категория 4",
]

# Order Statuses
ORDER_STATUSES: Dict[str, str] = {
    "pending": "🕒 Ожидает подтверждения",
    "confirmed": "✅ Подтвержден",
    "cancelled": "❌ Отменен",
    "completed": "🎉 Выполнен"
}

# Payment Settings
PAYMENT_TIMEOUT: int = int(os.getenv("PAYMENT_TIMEOUT", "3600"))  # 1 hour in seconds
PAYMENT_CHECK_INTERVAL: int = int(os.getenv("PAYMENT_CHECK_INTERVAL", "60"))  # 1 minute in seconds

# Bot Messages
MESSAGES = {
    "welcome": "👋 Добро пожаловать в {shop_name}!\n\n"
               "Здесь вы можете:\n"
               "• Просматривать каталог товаров\n"
               "• Добавлять товары в корзину\n"
               "• Оформлять заказы\n"
               "• Отслеживать статус заказов\n\n"
               "Используйте меню для навигации.",
    "help": "📚 Список доступных команд:\n\n"
            "/start - Запустить бота\n"
            "/help - Показать это сообщение\n"
            "/catalog - Просмотреть каталог товаров\n"
            "/cart - Просмотреть корзину\n"
            "/orders - Просмотреть ваши заказы",
    "error": "❌ Произошла ошибка. Пожалуйста, попробуйте позже или обратитесь к администратору.",
    "payment_success": "✅ Оплата успешно получена! Ваш заказ принят в обработку.",
    "payment_timeout": "⏰ Время на оплату истекло. Заказ отменен.",
}

# Validation
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not set in environment variables")
if ADMIN_ID == 0:
    raise ValueError("ADMIN_ID is not set in environment variables")
