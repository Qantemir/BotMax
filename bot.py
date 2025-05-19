import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramAPIError, TelegramNetworkError
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties

import config
from database.mongodb import db
from handlers import user_handlers, admin_handlers  # Предполагается, что это модули с Router

def setup_logging():
    """Configure logging for the bot"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('bot.log', encoding='utf-8')
        ]
    )
    return logging.getLogger(__name__)

async def set_commands(bot: Bot):
    """Set bot commands in Telegram menu"""
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь по использованию"),
        BotCommand(command="catalog", description="Каталог товаров"),
        BotCommand(command="cart", description="Корзина"),
        BotCommand(command="orders", description="Мои заказы")
    ]
    await bot.set_my_commands(commands)

async def on_startup(bot: Bot, logger):
    """Perform startup actions"""
    try:
        # Connect to MongoDB
        await db.connect()
        logger.info("Connected to MongoDB successfully")
        
        # Set bot commands
        await set_commands(bot)
        logger.info("Bot commands set successfully")
        
        # Send startup notification to admin
        await bot.send_message(
            chat_id=config.ADMIN_ID,
            text="🟢 Бот запущен и готов к работе!\n"
                 f"Версия: 1.0.0\n"
                 f"Режим: {'Production' if config.PRODUCTION else 'Development'}"
        )
        logger.info("Startup notification sent to admin")
    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)
        raise

async def on_shutdown(bot: Bot, logger):
    """Perform cleanup actions"""
    try:
        # Close MongoDB connection
        await db.close()
        logger.info("MongoDB connection closed")
        
        # Send shutdown notification to admin
        try:
            await bot.send_message(
                chat_id=config.ADMIN_ID,
                text="🔴 Бот остановлен!"
            )
        except (TelegramAPIError, TelegramNetworkError) as e:
            logger.warning(f"Could not send shutdown notification: {e}")
            
        # Close bot session
        await bot.session.close()
        logger.info("Bot session closed")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}", exc_info=True)

async def main():
    # Setup logging
    logger = setup_logging()
    
    try:
        # Initialize bot and dispatcher
        bot = Bot(
            token=config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode="HTML")
        )
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        
        # Register handlers
        dp.include_router(user_handlers.router)
        dp.include_router(admin_handlers.router)
        
        # Register startup and shutdown handlers
        dp.startup.register(lambda: on_startup(bot, logger))
        dp.shutdown.register(lambda: on_shutdown(bot, logger))
        
        # Start polling
        logger.info("Starting bot...")
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logger.critical(f"Critical error while running bot: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped gracefully")
    except Exception as e:
        logging.critical(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
