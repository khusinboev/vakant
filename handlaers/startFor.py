import datetime
from function.functions import *
from databas import *
from key import *
from buttons.mButtons import *
import pytz



@dp.message_handler(commands='start')
async def welcome(message: types.Message):
    user_id = message.chat.id
    sql.execute("""CREATE TABLE IF NOT EXISTS users ("user_id"  INTEGER,"date"  INTEGER, "lang" INTEGER, "region" INTEGER, "district" INTEGER, "money" INTEGER, "level" INTEGER);""")
    db.commit()
    sql.execute("""CREATE TABLE IF NOT EXISTS channels ("id"  INTEGER);""")
    db.commit()
    sql.execute("""CREATE TABLE IF NOT EXISTS locations ("regions"  INTEGER, "reg_ids"  INTEGER, "districts"  INTEGER, "dist_ids"  INTEGER, "addition"  INTEGER);""")
    db.commit()
    check = sql.execute(f"""SELECT user_id FROM users WHERE user_id = {user_id}""").fetchone()


    if check == None:
        sana = datetime.datetime.now(pytz.timezone('Asia/Tashkent')).strftime('%d-%m-%Y %H:%M')
        sql.execute(f"""INSERT INTO users (user_id, date, lang) VALUES ('{user_id}', '{sana}', '{message.from_user.language_code}')""")
        db.commit()

    sql.execute("SELECT id FROM channels")
    rows = sql.fetchall()
    join_inline = types.InlineKeyboardMarkup(row_width=1)
    title = 1
    for row in rows:
        all_details = await dp.bot.get_chat(chat_id=row[0])
        url = all_details['invite_link']
        join_inline.insert(InlineKeyboardButton(f"{title} - kanal", url=url))
        title += 1
    join_inline.add(InlineKeyboardButton("✅Obuna bo'ldim", callback_data="check"))
    if await functions.check_on_start(message.from_user.id):
        await message.answer(f"""Assalomu alaykum. Botimizga hush kelibsiz. Kerakli bo‘limni tanlang!""", reply_markup=MM_btn)
    else:
        await message.answer("Botimizdan foydalanish uchun kanalimizga azo bo'ling", reply_markup=join_inline)

@dp.callback_query_handler(text="check")
async def check(call: CallbackQuery):
    user_id = call.from_user.id
    if await functions.check_on_start(user_id):
        await call.answer()
        await call.message.delete()
        await call.message.answer("Assalomu alaykum. Botimizga xush kelibsiz.\n\nO'zingizga kerakli viloyatni tanlang va davom eting", reply_markup=await special_btn(user_id))
    else:
        await call.answer(show_alert=True, text="Botimizdan foydalanish uchun kanalimizga azo bo'ling")
