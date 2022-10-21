from handlaers.startFor import *
from handlaers.admin_panel import *


@dp.message_handler(text="💼Ish qidirish")
async def search(message: types.Message):
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
        try:
            user_id = message.from_user.id
            checker = sql.execute(f"""SELECT specs FROM users WHERE user_id = {user_id} """).fetchone()[0]
            if checker == None:
                await message.answer("Botdan foydalanish uchun avval filtrlarni sozlab oling. Kerakli bo‘limni tanglang!", reply_markup=await special_btn(user_id))
            else:
                send = await  message.answer("⏳Iltimos biroz kuting,🔎 ish qidirilmoqda...")
                # region = sql.execute(f"""SELECT reg_ids FROM locations WHERE region = {reg0}""").fetchone()[0]
                texts = await search_vakant(user_id, 1)
                try:
                    await message.answer(text=f"{texts[2]}\n{texts[0]}", reply_markup=await vacancie_btn(texts[1], texts[2], texts[3]))
                except:
                    await message.answer(texts[0])
                try:
                    await send.delete()
                except:
                    pass
        except:
            await message.answer("Ma'lumot topilmadi. Filtrlarni o'zgartirib ko'ring")
    else:
        await message.answer("Botimizdan foydalanish uchun kanalimizga azo bo'ling", reply_markup=join_inline)



######################         ALL FILTERS

@dp.message_handler(text="🛠Filtrni boshqarish")
async def helper(message: types.Message):
    await message.answer("Kerakli sohani tanlang", reply_markup=await special_btn(message.from_user.id))


@dp.callback_query_handler(text="🟢Tanladim🟢")
async def check(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete()
    except:
        pass
    await call.message.answer("Kerakli hududni tanlang!", reply_markup=await region_btn(call.from_user.id))


@dp.callback_query_handler(text="✅Tanladim✅")
async def check(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete()
    except:
        pass
    await call.message.answer("Kerakli maosh miqdorini tanlang", reply_markup=await money_btn(call.from_user.id))

@dp.callback_query_handler(text="✅️Tanladim✅")
async def check(call: CallbackQuery):
    user_id = call.from_user.id
    await call.answer()
    try:
        await call.message.delete()
    except:
        pass
    tes = sql.execute(f"""SELECT region FROM users WHERE user_id = {user_id} """).fetchone()[0]
    if tes =='Barchasi':
        await call.message.answer("Kerakli maosh miqdorini tanlang", reply_markup=await money_btn(user_id))
    elif tes == None:
        await call.message.answer("Kerakli maosh miqdorini tanlang", reply_markup=await money_btn(user_id))
    else:
        await call.message.answer("Kerakli hududni tanlang!", reply_markup=await district_btn(call.from_user.id))

@dp.callback_query_handler(text = ['22,322,323,324', '71', '91,522,523', '61', '214', '213,312', '23,33', '83'])
async def reg(call: CallbackQuery):

    user_id = call.from_user.id
    texts = call.data
    sql.execute(f"""UPDATE users SET specs="{texts}" WHERE user_id="{user_id}" """)
    db.commit()
    await call.answer("Saqlandi")
    try:
        await call.message.edit_reply_markup(reply_markup=await special_btn(user_id))
    except:
        pass


@dp.callback_query_handler(text = ['Barchasi', 'Andijon viloyati', 'Buxoro viloyati', 'Jizzax viloyati', 'Qashqadaryo viloyati',
			'Navoiy viloyati', 'Namangan viloyati', 'Samarqand viloyati', 'Surxondaryo viloyati',
			'Sirdaryo viloyati', 'Toshkent shahri', 'Toshkent viloyati', "Farg'ona viloyati", 'Xorazm viloyati',
			"Qoraqalpog'iston Respublikasi"])
async def reg(call: CallbackQuery):
    user_id = call.from_user.id
    texts = call.data
    sql.execute(f"""UPDATE users SET region="{texts}" WHERE user_id="{user_id}" """)
    db.commit()
    sql.execute(f"""UPDATE users SET district=0 WHERE user_id="{user_id}" """)
    db.commit()
    await call.answer("Saqlandi")
    try:
        await call.message.edit_reply_markup(reply_markup=await region_btn(user_id))
    except:
        pass

@dp.callback_query_handler(text = ["Oltinko'l tumani", 'Andijon tumani', 'Baliqchi tumani', "Bo'ston tumani",
                                   'Buloqboshi tumani', 'Jalaquduq tumani', 'Izboskan tumani', "Ulug'nor tumani",
                                   "Qo'rg'ontepa tumani", 'Asaka tumani', 'Marxamat tumani', 'Shaxrixon tumani',
                                   'Paxtaobod tumani', "Xo'jaobod tumani", 'Andijon', 'Xonobod', 'Konimex tumani',
                                   'Qiziltepa tumani', 'Navbahor tumani', 'Karmana tumani', 'Nurota tumani', 'Tomdi tumani', 'Uchquduq tumani', 'Xatirchi tumani', 'Navoiy', 'Zarafshon', "G'ozg'on", "Oqqo'rg'on tumani", 'Ohangaron tumani', 'Bekobod tumani', "Bo'stonliq tumani", "Bo'ka tumani", 'Quyichirchiq tumani', 'Zangiota tumani', 'Yuqorichirchiq tumani', 'Qibray tumani', 'Parkent tumani', 'Pskent tumani', "O'rtachirchiq tumani", 'Chinoz tumani', "Yangiyo'l tumani", 'Toshkent tumani', 'Nurafshon', 'Olmaliq', 'Angren', 'Bekobod', 'Ohangaron', 'Chirchiq', "Yangiyo'l", "Bog'ot tumani", 'Gurlan tumani', "Qo'shko'pir tumani", 'Urganch tumani', 'Xazorasp tumani', "Tuproqqal'a tumani", 'Xonqa tumani', 'Xiva tumani', 'Shovot tumani', 'Yangiariq tumani', 'Yangibozor tumani', 'Urganch', 'Xiva', 'Oltinsoy tumani', 'Angor tumani', 'Bandixon tumani', 'Boysun tumani', 'Muzrabot tumani', 'Denov tumani', "Jarqo'rg'on tumani", "Qumqo'rg'on tumani", 'Qiziriq tumani', 'Sariosiyo tumani', 'Termiz tumani', 'Uzun tumani', 'Sherobod tumani', "Sho'rchi tumani", 'Termiz', "G'uzor tumani", 'Dehqonobod tumani', 'Qamashi tumani', 'Qarshi tumani', 'Koson tumani', 'Kitob tumani', 'Mirishkor tumani', 'Muborak tumani', 'Nishon tumani', 'Kasbi tumani', 'Chiroqchi tumani', 'Shahrisabz tumani', "Yakkabog' tumani", 'Qarshi', 'Shahrisabz', 'Mingbuloq tumani', 'Kosonsoy tumani', 'Namangan tumani', 'Norin tumani', 'Pop tumani', "To'raqo'rg'on tumani", 'Uychi tumani', "Uchqo'rg'on tumani", 'Chortoq tumani', 'Chust tumani', "Yangiqo'rg'on tumani", 'Namangan', 'Oqdaryo tumani', "Bulung'ur tumani", 'Jomboy tumani', 'Ishtixon tumani', "Kattaqo'rg'on tumani", "Qo'shrabot tumani", 'Narpay tumani', 'Payariq tumani', "Pastdarg'om tumani", 'Paxtachi tumani', 'Samarqand tumani', 'Nurobod tumani', 'Urgut tumani', 'Tayloq tumani', 'Samarqand', "Kattaqo'rg'on", 'Oqoltin tumani', 'Boyovut tumani', 'Sayxunobod tumani', 'Guliston tumani', 'Sardoba tumani', 'Mirzaobod tumani', 'Sirdaryo tumani', 'Xovos tumani', 'Guliston', 'Shirin', 'Yangiyer', 'Uchtepa tumani', 'Bektemir tumani', 'Yunusobod tumani', "Mirzo Ulug'bek tumani", 'Mirobod tumani', 'Shayxontoxur tumani', 'Olmazor tumani', "Sirg'ali tumani", 'Yakkasaroy tumani', 'Yashnobod tumani', 'Yangihayot tumani', 'Chilonzor tumani', 'Oltiariq tumani', "Qo'shtepa tumani", "Bog'dod tumani", 'Buvayda tumani', 'Beshariq tumani', 'Quva tumani', "Uchko'prik tumani", 'Rishton tumani', "So'x tumani", 'Toshloq tumani', "O'zbekiston tumani", "Farg'ona tumani", "Dang'ara tumani", 'Furqat tumani', 'Yozyovon tumani', "Farg'ona", "Qo'qon", 'Quvasoy', "Marg'ilon", 'Amudaryo tumani', 'Beruniy tumani', "Bo'zatov tumani", "Qorao'zak tumani", 'Kegeyli tumani', "Qo'ng'irot tumani", "Qanliko'l tumani", "Mo'ynoq tumani", 'Nukus tumani', 'Taxiatosh tumani', "Taxtako'pir tumani", "To'rtko'l tumani", "Xo'jayli tumani", 'Chimboy tumani', 'Shumanay tumani', 'Ellikkala tumani', 'Nukus', 'Olot tumani', 'Buxoro tumani', 'Vobkent tumani', "G'ijduvon tumani", 'Kogon tumani', "Qorako'l tumani", 'Qorovulbozor tumani', 'Peshku tumani', 'Romitan tumani', 'Jondor tumani', 'Shofirkon tumani', 'Buxoro', 'Kogon'])
async def reg(call: CallbackQuery):
    user_id = call.from_user.id
    texts = call.data
    sql.execute(f"""UPDATE users SET district="{texts}" WHERE user_id="{user_id}" """)
    db.commit()
    await call.answer("Saqlandi")
    try:
        await call.message.edit_reply_markup(reply_markup=await district_btn(user_id))
    except:
        pass

#########################################                salary

@dp.callback_query_handler(text="✅ Tanladim ✅")
async def check(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete()
    except:
        pass
    await call.message.answer("Ta'lim darajangizni tanlang", reply_markup=await level_btn(call.from_user.id))

@dp.callback_query_handler(text = ['⭕️Ahamiyatsiz️', '1 mln ➕', '3 mln ➕'])
async def reg(call: CallbackQuery):
    user_id = call.from_user.id
    texts = call.data
    sql.execute(f"""UPDATE users SET money="{texts}" WHERE user_id="{user_id}" """)
    db.commit()
    await call.answer("Saqlandi")
    try:
        await call.message.edit_reply_markup(reply_markup=await money_btn(user_id))
    except:
        pass


#####################            LEVEL FILTERS

@dp.callback_query_handler(text=" ✅Tanladim✅")
async def check(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.delete()
    except:
        pass
    await call.message.answer("""Filtrlash yakunlandi, "ish qidirish" tugmasini bosing! """, reply_markup=MM_btn)

@dp.callback_query_handler(text = ['️⭕️Ahamiyatsiz', "👨‍💼O'rta maxsus", '👨‍🎓Oliy'])
async def reg(call: CallbackQuery):
    user_id = call.from_user.id
    texts = call.data
    sql.execute(f"""UPDATE users SET level="{texts}" WHERE user_id="{user_id}" """)
    db.commit()
    await call.answer("Saqlandi")
    try:
        await call.message.edit_reply_markup(reply_markup=await level_btn(user_id))
    except:
        pass

##############################################                                               Personal information

@dp.message_handler(text="🗂Saqlangan ishlar")
async def helper(message: types.Message):
    user_id = message.from_user.id

    delete = types.InlineKeyboardMarkup(row_width=1)
    delete.add(InlineKeyboardButton(text="🗑Saqlanganlarni o'chirish", callback_data="delete"))

    sql.execute("""CREATE TABLE IF NOT EXISTS saves ("user_id"  INTEGER, "save_id"  INTEGER, "fake"  INTEGER);""")
    db.commit()
    # try:
    saves = sql.execute(f"""SELECT save_id FROM saves WHERE user_id = {user_id}""").fetchall()
    if len(saves) == 0:
        await message.answer("Sizda saqlangan ishlar mavjud emas")
    else:
        for save in saves:
            save = save[0]
            if save == 0:
                pass
            else:
                text = await saves_info(save)
                await message.answer(text, reply_markup=delete)
    # except:
    #     await message.answer("Sizda saqlangan ishlar mavjud emas")


@dp.callback_query_handler(text="delete")
async def ss(call: CallbackQuery):
    try:
        sql.execute(f"DELETE from saves WHERE user_id='{call.from_user.id}'")
    except:
        pass
    await call.answer("Hammasi o'chirildi")


################        ##############################          $$$$$$$$$$$$$$$$$$$$$
@dp.callback_query_handler()
async def ss(call: CallbackQuery):
    # try:
        user_id = call.from_user.id
        data = call.data
        if data[0] == "⬅":
            if int(data[1:])-1 == 0:
                await call.answer(text="tamom")
            else:
                try:
                    await call.answer()
                    texts = await search_vakant(user_id, int(data[1:])-1)
                    await call.message.edit_text(text=f"""{int(call.message.text[0])-1}\n{texts[0]}""")
                    await call.message.edit_reply_markup(reply_markup=await vacancie_btn(texts[1], texts[2], texts[3]))
                except:
                    pass
        elif data == "❌":
            await call.answer("Raxmat")
            try:
                await call.message.delete()
            except:
                pass
        elif data[0] == "➡":
            ts = await search_vakant(user_id, data[1:])
            if int(data[1:]) + 1 > ts[4]:
                await call.answer(text="tamom")
            else:
                try:
                    texts = await search_vakant(user_id, int(data[1:]) + 1)
                    await call.message.edit_text(text=f"""{int(call.message.text[0])+1}\n{texts[0]}""")
                    await call.message.edit_reply_markup(reply_markup=await vacancie_btn(texts[1], texts[2], texts[3]))
                except:
                    pass

        elif data[0] == "🔙":
            try:
                await call.answer()
                texts = await search_vakant(user_id, data[1:])
                await call.message.edit_text(text=f"""{call.message.text[0]}\n{texts[0]}""")
                await call.message.edit_reply_markup(reply_markup=await vacancie_btn(texts[1], texts[2], texts[3]))
            except:
                pass

        elif data[0] == "🗂":
            checks = sql.execute(f"""SELECT save_id FROM saves WHERE user_id = {user_id}""").fetchall()
            che = []
            for c in checks:
                c=c[0]
                che.append(int(c))
            if int(data[1:]) in che:
                await call.answer("Bu avvaldan bor")
            else:
                sql.execute(
                    f"""INSERT INTO saves (user_id, save_id) VALUES ('{user_id}', '{data[1:]}')""")
                db.commit()
                await call.answer("Saqlandi")



        else:
            try:
                await call.message.delete()
            except:
                pass

            soup = await get_site_content(f'https://ishapi.mehnat.uz/api/v1/vacancies/{data}')
            soup1 = soup['data']
            status = soup1["active"]
            if status == True:
                status = "Aktiv"
            else:
                status = "Band"
            comp_name = soup1['company_name']
            work_title = soup1['position_name']
            salary = soup1['position_salary']
            commitment = soup1['position_duties']
            demand = soup1['position_requirements']
            condition = soup1['position_conditions']
            phones = soup1['phones']
            address = str(soup1['region']['name_uz_ln']) + ', ' + str(soup1['district']['name_uz_ln'])

            sav = types.InlineKeyboardMarkup(row_width=2)
            sav.add(InlineKeyboardButton(text="📌 Saqlash", callback_data=f"🗂{data}"))
            num = call.message.text[0]
            sav.insert(InlineKeyboardButton(text="⬅Orqaga", callback_data=f"🔙{num}"))

            await call.message.answer(text= f"{num}\n<b>🏢Komponiya nomi: </b>{comp_name}\n<b>🧑‍🏭Ish nomi: </b>{work_title}\n\n"
                                      f"<b>ℹ️Ish haqida: </b>{condition}\n\n<b>📌Majburiyatlari: </b>{commitment}\n\n"
                                      f"<b>📎Talab: </b>{demand}\n\n<b>💸Maoshi: </b>{salary}\n\n\n<b>📣Ishning holati: </b>{status}\n"
                                      f"<b>🗺Manzili: </b>{address}\n<b>📞Telefon raqami: </b>+{phones[0]}", reply_markup=sav)




# 908180189
if __name__ == "__main__":
    executor.start_polling(dp)
