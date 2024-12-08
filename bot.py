import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.exceptions import TelegramAPIError
from config import TELEGRAM_BOT_TOKEN
from database import get_db
from handlers import BotHandlers
from gpt_service import GPTService

# Enhanced logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Add handler to also log errors specifically
error_handler = logging.StreamHandler()
error_handler.setLevel(logging.ERROR)
logger.addHandler(error_handler)

async def handle_errors(event: types.Update, exception: Exception):
    """Handle errors that occur during update processing."""
    logger.error(f"Update processing error: {exception}", exc_info=True)
    try:
        if isinstance(event, types.Message):
            await event.answer(
                "An error occurred while processing your message. Please try again later."
            )
    except Exception as e:
        logger.error(f"Error while handling error: {e}")

async def main():
    # Bot instance
    bot = None
    dp = None
    
    try:
        logger.info("Starting bot initialization...")
        
        # Initialize dispatcher first
        dp = Dispatcher()
        
        # Verify token and initialize bot
        if not TELEGRAM_BOT_TOKEN:
            raise ValueError("Telegram bot token is not set!")
            
        logger.info("Initializing bot with token...")
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        # Test bot connection
        try:
            logger.info("Testing bot connection...")
            bot_info = await bot.get_me()
            logger.info(f"Bot connected successfully: @{bot_info.username}")
        except TelegramAPIError as e:
            logger.error(f"Failed to connect to Telegram: {e}")
            raise
        
        # Initialize services
        try:
            logger.info("Initializing database connection...")
            db = next(get_db())
            logger.info("Database connection successful")
            
            logger.info("Initializing GPT service...")
            gpt_service = GPTService()
            logger.info("Initializing GPT service...")
            gpt_service = GPTService()
            logger.info("GPT service initialized successfully with model: gpt-4o")
            
            # Initialize handlers with dependency injection
            logger.info("Initializing bot handlers...")
            handlers = BotHandlers(db, gpt_service)
            logger.info("Bot handlers initialized successfully")
            
        except Exception as e:
            logger.error(f"Service initialization failed: {e}")
            raise
        
        # Register error handler
        logger.info("Registering error handler...")
        dp.errors.register(handle_errors)
        
        # Register message handlers
        logger.info("Registering message handlers...")
        dp.message.register(handlers.start_command, Command("start"))
        dp.message.register(
            handlers.handle_places_button,
            F.text == "📍 Choose Places"
        )
        dp.callback_query.register(
            handlers.handle_place_selection,
            F.data.startswith('place_')
        )
        dp.message.register(
            handlers.handle_location_button,
            F.text == "📌 Location"
        )
        dp.message.register(
            handlers.handle_user_question,
            (F.text != "📍 Choose Places") & 
            (F.text != "📌 Location") & 
            ~F.text.startswith('/')
        )

        # Start polling
        logger.info("Starting bot polling...")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}", exc_info=True)
        raise
    finally:
        if bot:
            await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
