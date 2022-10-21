from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
storage = MemoryStorage()


TOKEN = "5299322380:AAFDPqXWu2v-hR7jCsAArkIvvWyEdcp7xOA"

bot = Bot(token=TOKEN, parse_mode='html')
dp = Dispatcher(bot=bot, storage=storage)
