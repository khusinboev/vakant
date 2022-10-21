from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from handlaers.startFor import *


main_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_btn.add("📊Statistika", "🔧Kanallar", "📤Reklama")

channel_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
channel_btn.add("➕Kanal qo'shish", "❌Kanalni olib tashlash")
channel_btn.add("📋 Kanallar ro'yxati", "🔙Orqaga qaytish")

reklama_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
reklama_btn.add("📨Forward xabar yuborish", "📬Oddiy xabar yuborish", "🔙Orqaga qaytish")



MM_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
MM_btn.add("💼Ish qidirish", "🛠Filtrni boshqarish", "🗂Saqlangan ishlar")
