from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
storage = MemoryStorage()


TOKEN = "7855267108:AAFpBSZIlR8z9WY7bcZ33kUq3RPTa4Smm6s"

bot = Bot(token=TOKEN, parse_mode='html')
dp = Dispatcher(bot=bot, storage=storage)
