import config
import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

log = logging.getLogger(__name__)
log.setLevel(os.environ.get('LOGGING_LEVEL', 'INFO').upper())

bot = Bot(os.environ.get("BOT_TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())

