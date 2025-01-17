import asyncio
import logging
import config

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import common, registration


# Запуск процесса поллинга новых апдейтов
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )
    
    bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
        # ParseMode.MARKDOWN_V2
            )
        )
    
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(common.router)
    dp.include_router(registration.router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
