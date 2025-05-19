import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN: str = os.getenv("BOT_TOKEN")
ADMIN_ID: int = int(os.getenv("ADMIN_ID"))
ADMIN_CARD: str = os.getenv("ADMIN_CARD", "")  # Card number for payments

# MongoDB Configuration
MONGODB_URI: str = os.getenv("MONGODB_URI")
DB_NAME: str = os.getenv("DB_NAME", "maxshop_db")

# Shop Configuration
SHOP_NAME: str = os.getenv("MAXSHOP",)
CURRENCY: str = os.getenv("CURRENCY", "TNG")

# Product Categories
CATEGORIES = [
    "Тестовая категория",
    "Тестовая категория 2",
    "тестовая категория 3",
    "Тестовая категория 4",
]

# Order Statuses
ORDER_STATUSES = {
    "pending": "🕒 Ожидает подтверждения",
    "confirmed": "✅ Подтвержден",
    "cancelled": "❌ Отменен",
    "completed": "🎉 Выполнен"
}
