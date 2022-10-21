from sqlite3 import connect
from key import *
from databas import *
from aiogram import *
from aiogram.types import *
import asyncio
import aiohttp

class functions:
    @staticmethod
    async def check_on_start(user_id):
        rows = sql.execute("SELECT id FROM channels").fetchall()
        error_code = 0
        for row in rows:
            r = await dp.bot.get_chat_member(chat_id=row[0], user_id=user_id)
            if r.status in ['member', 'creator', 'admin']:
                pass
            else:
                error_code = 1
        if error_code == 0:
            return True
        else:
            return False

class panel_func:
    @staticmethod
    async def channel_add(id):
        sql.execute("""CREATE TABLE IF NOT EXISTS channels(id)""")
        db.commit()
        sql.execute("INSERT INTO channels VALUES(?);", id)
        db.commit()


    @staticmethod
    async def channel_delete(id):
        sql.execute(f'DELETE FROM channels WHERE id = "{id}"')
        db.commit()

    @staticmethod
    async def channel_list():
        sql.execute("SELECT id from channels")
        str = ''
        for row in sql.fetchall():
            id = row[0]
            try:
                all_details = await dp.bot.get_chat(chat_id=id)
                title = all_details["title"]
                channel_id = all_details["id"]
                info = all_details["description"]
                str+= f"------------------------------------------------\nKanal useri: > {id}\nKamal nomi: > {title}\nKanal id si: > {channel_id}\nKanal haqida: > {info}\n"
            except:
                str+= "Kanalni admin qiling"
        return str

async def forward_send_msg(chat_id: int, from_chat_id: int, message_id: int) -> bool:
    try:
        await dp.bot.forward_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)
    except exceptions.BotBlocked:
        sql.execute(f"DELETE FROM users WHERE user_id ='{chat_id}'")
        db.commit()
    except exceptions.ChatNotFound:
        sql.execute(f"DELETE FROM users WHERE user_id ='{chat_id}'")
        db.commit()
    except exceptions.UserDeactivated:
        sql.execute(f"DELETE FROM users WHERE user_id ='{chat_id}'")
        db.commit()
    except exceptions.TelegramAPIError:
        sql.execute(f"DELETE FROM users WHERE user_id ='{chat_id}'")
        db.commit()
    else:
        return True
    return False

async def send_message_chats(chat_id: int, from_chat_id: int, message_id: int) -> bool:
    try:
        await dp.bot.copy_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)
    except exceptions.BotBlocked:
        sql.execute(f"DELETE FROM users WHERE user_id ='{chat_id}'")
        db.commit()
    except exceptions.ChatNotFound:
        sql.execute(f"DELETE FROM users WHERE user_id ='{chat_id}'")
        db.commit()
    except exceptions.UserDeactivated:
        sql.execute(f"DELETE FROM users WHERE user_id ='{chat_id}'")
        db.commit()
    except exceptions.TelegramAPIError:
        sql.execute(f"DELETE FROM users WHERE user_id ='{chat_id}'")
        db.commit()
    else:
        return True
    return False


async def get_site_content(URL):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            text = await resp.json()
    return text


async def search_vakant(user_id, page):
        reg0 = sql.execute(f"""SELECT region FROM users WHERE user_id = {user_id}""").fetchone()[0]
        reg1 = sql.execute(f"""SELECT district FROM users WHERE user_id = {user_id} """).fetchone()[0]
        specs = sql.execute(f"""SELECT specs FROM users WHERE user_id = {user_id} """).fetchone()[0]
        if specs==None:
            spec = "&"
        else:
            spec = f"&nskz={specs}&"
        if reg1 == 0:
            if reg0 == "Barchasi":
                reg2=0
            else:
                reg2 = sql.execute(f"""SELECT reg_ids FROM locations WHERE regions = "{reg0}" """).fetchone()[0]
        elif reg1 == None:
            if reg0 == None:
                reg2=0
            else:
                reg2 = sql.execute(f"""SELECT reg_ids FROM locations WHERE regions = "{reg0}" """).fetchone()[0]
        else:
            reg2 = sql.execute(f"""SELECT dist_ids FROM locations WHERE districts = "{reg1}" """).fetchone()[0]
        salary = sql.execute(f"""SELECT money FROM users WHERE user_id = {user_id}""").fetchone()[0]
        level = sql.execute(f"""SELECT level FROM users WHERE user_id = {user_id}""").fetchone()[0]
        ##
        dict2 = {'⭕️Ahamiyatsiz️':0, '1 mln ➕':1000000, '3 mln ➕':3000000}
        dict3 = {'️⭕️Ahamiyatsiz':0, "👨‍💼O'rta maxsus":'ССПО', '👨‍🎓Oliy':"В%2FО"}
        if level == None:
            levelim = '&'
        elif dict3[level] == 0:
            levelim = '&'
        else:
            levelim = f"&min_education={dict3[level]}&"
        if salary == None:
            salarym = '&'
        elif dict2[salary] == 0:
            salarym = '&'
        else:
            salarym = f"salary={dict2[salary]}&"
        if levelim=='&' and salarym=='&':
            optimal = '&'
        else:
            optimal = levelim + salarym
        URL = f"https://ishapi.mehnat.uz/api/v1/vacancies?per_page=5{optimal}company_soato_code={reg2}{spec}page={page}"
        soup = await get_site_content(URL)

        try:
            text = soup['data']['data']

            num = soup['data']['from']
            texts = ''
            ids = []
            for i in text:

                id = i['id']
                company_name = i['company_name']
                position_salary = i['position_salary']
                if position_salary == None:
                    position_salary = "Mavjud emas"
                location = i['region']['name_uz_ln'] + ' ' + i['district']['name_uz_ln']
                texts += f"""<b>👨‍💻{num}- Vakansiya\n\n🆔ID raqami: </b>{id}\n<b>🏢Ish beruvchi nomi: </b>{company_name}\n<b>💰Taxminiy maoshi: </b>{position_salary} so'm\n<b>📍Joylashuvi: </b>{location}\n\n➖➖➖➖➖➖➖➖➖➖\n\n"""
                num += 1
                ids.append(id)
            all = soup['data']['total']
            dan = soup['data']['from']
            ga = soup['data']['to']
            joriy = soup['data']['current_page']
            end = soup['data']['last_page']
            texts = f"<b>NATIJALAR</b>: {all} ta bo'sh ish o'rnlari topildi | {dan}-{ga}\n\n\n" + texts
            if dan == None:
                texts = "Sizning belgilagan filterlaringiz bo'yicha ma'lumot topilmadi, Filtrlarni o'zgartirib ko'ring"
        except:
            texts="Xato yuz berdi"
            ids = 1
            joriy = 0
            dan = 0
            end = 0
        return texts, ids, joriy, dan, end

async def vacancie_btn(ids, joriy, ga):

    region_choos = types.InlineKeyboardMarkup(row_width=5)
    for name, id in zip(range(ga, ga+10), ids):
        region_choos.insert(InlineKeyboardButton(name, callback_data=id))

    region_choos.add(InlineKeyboardButton("⬅", callback_data=f"⬅{joriy}"))
    region_choos.insert(InlineKeyboardButton("❌", callback_data="❌"))
    region_choos.insert(InlineKeyboardButton("➡", callback_data=f"➡{joriy}"))
    return region_choos



########################                main
async def region_btn(user_id):
    rows = ['Barchasi', 'Andijon viloyati', 'Buxoro viloyati', 'Jizzax viloyati', 'Qashqadaryo viloyati',
            'Navoiy viloyati', 'Namangan viloyati', 'Samarqand viloyati', 'Surxondaryo viloyati',
            'Sirdaryo viloyati', 'Toshkent shahri', 'Toshkent viloyati', "Farg'ona viloyati", 'Xorazm viloyati',
            "Qoraqalpog'iston Respublikasi"]
    region_choos = types.InlineKeyboardMarkup(row_width=2)
    title = 1
    for row in rows:
        reg = sql.execute(f"""SELECT region FROM users WHERE user_id = {user_id}""").fetchone()
        if row == reg[0]:
            region_choos.insert(InlineKeyboardButton(text=f"🟢{row}", callback_data=row))
        else:
            region_choos.insert(InlineKeyboardButton(row, callback_data=row))
        title += 1
    region_choos.add(InlineKeyboardButton("✅️Tanladim✅", callback_data="✅️Tanladim✅"))
    return region_choos


async def district_btn(user_id):
    regs = sql.execute(f"""SELECT region FROM users WHERE user_id = {user_id}""").fetchone()[0]

    districts = sql.execute(f"""SELECT districts FROM locations WHERE regions = "{regs}" """).fetchall()

    region_choos = types.InlineKeyboardMarkup(row_width=2)
    title = 1
    for row in districts:
        row = row[0]
        reg = sql.execute(f"""SELECT district FROM users WHERE user_id = {user_id}""").fetchone()
        if row == reg[0]:
            region_choos.insert(InlineKeyboardButton(text=f"🟢{row}", callback_data=row))
        else:
            region_choos.insert(InlineKeyboardButton(row, callback_data=row))
        title += 1
    region_choos.add(InlineKeyboardButton("✅Tanladim✅", callback_data="✅Tanladim✅"))
    return region_choos


async def money_btn(user_id):
    rows = ['⭕️Ahamiyatsiz️', '1 mln ➕', '3 mln ➕']
    region_choos = types.InlineKeyboardMarkup(row_width=2)
    title = 1
    for row in rows:
        reg = sql.execute(f"""SELECT money FROM users WHERE user_id = {user_id}""").fetchone()
        if row == reg[0]:
            region_choos.insert(InlineKeyboardButton(text=f"🟢{row}", callback_data=row))
        else:
            region_choos.insert(InlineKeyboardButton(row, callback_data=row))
        title += 1
    region_choos.add(InlineKeyboardButton("✅ Tanladim ✅", callback_data="✅ Tanladim ✅"))

    return region_choos


async def level_btn(user_id):
    rows = ['️⭕️Ahamiyatsiz', "👨‍💼O'rta maxsus", '👨‍🎓Oliy']
    region_choos = types.InlineKeyboardMarkup(row_width=2)
    title = 1
    for row in rows:
        reg = sql.execute(f"""SELECT level FROM users WHERE user_id = {user_id}""").fetchone()
        if row == reg[0]:
            region_choos.insert(InlineKeyboardButton(text=f"🟢{row}", callback_data=row))
        else:
            region_choos.insert(InlineKeyboardButton(row, callback_data=row))
        title += 1
    region_choos.add(InlineKeyboardButton(" ✅Tanladim✅", callback_data=" ✅Tanladim✅"))

    return region_choos


async def special_btn(user_id):

    specs = ["Sog'liqni saqlash", "Qurilish sohasi", "Savdo va xizmat ko'rsatish", "Qishloq xo'jaligi", "Arxitektura va Texnika", "IT sohasi", "Ta'lim sohasi", "Haydovchilik sohasi"]
    backs = ['22,322,323,324', '71', '91,522,523', '61', '214', '213,312', '23,33', '83']

    spec_choos = types.InlineKeyboardMarkup(row_width=2)
    for spec, back in zip(specs, backs):
        reg = sql.execute(f"""SELECT specs FROM users WHERE user_id = {user_id}""").fetchone()[0]
        sp = str(reg)
        if back == sp:
            spec_choos.insert(InlineKeyboardButton(text=f"🟢{spec}", callback_data=back))
        else:
            spec_choos.insert(InlineKeyboardButton(spec, callback_data=back))
    spec_choos.add(InlineKeyboardButton("✅Tanladim️✅️", callback_data="🟢Tanladim🟢"))
    return spec_choos


#######################

async def saves_info(data):
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
    text = f"<b>🏢Komponiya nomi: </b>{comp_name}\n<b>🧑‍🏭Ish nomi: </b>{work_title}\n\n<b>ℹ️Ish haqida: </b>{condition}\n\n<b>📌Majburiyatlari: </b>{commitment}\n\n<b>📎Talab: </b>{demand}\n\n<b>💸Maoshi: </b>{salary}\n\n\n<b>📣Ishning holati: </b>{status}\n<b>🗺Manzili: </b>{address}\n<b>📞Telefon raqami: </b>+{phones[0]}"
    return text


# async def vacancie_btn(ent_reg, raqam):
# 	text = ''
# 	lists = []
# 	for i in range(199, 250):
# 		try:
# 			URL = f"https://ishapi.mehnat.uz/api/v1/vacancies?per_page=5&company_soato_code={raqam}{i}"
# 			soup = await get_site_content(URL)
# 			p = json.loads(soup.text)['data']['data'][0]
# 			name = p['region']['name_uz_ln']
# 			id = p['district']['soato']
# 			if name == ent_reg:
# 				lists.append(p['district']['name_uz_ln'])
# 				sql.execute(
# 					f"""INSERT INTO locations (regions, reg_ids, districts, dist_ids) VALUES ("{ent_reg}", '{p['region']['soato']}', "{p['district']['name_uz_ln']}", "{id}")""")
# 				db.commit()
# 				text += f"{p['district']['name_uz_ln']} ----  {id}\n\n"
# 			else:
# 				pass
# 		except:
# 			pass
#
# 		if i == 249:
# 			for i in range(250, 450):
# 				try:
# 					URL = f"https://ishapi.mehnat.uz/api/v1/vacancies?per_page=5&company_soato_code={raqam}{i}"
# 					soup = await get_site_content(URL)
# 					p = json.loads(soup.text)['data']['data'][0]
# 					name = p['region']['name_uz_ln']
# 					id = p['district']['soato']
# 					if name == ent_reg:
# 						sql.execute(
# 							f"""INSERT INTO locations (regions, reg_ids, districts, dist_ids) VALUES ("{ent_reg}", '{p['region']['soato']}', "{p['district']['name_uz_ln']}", "{id}")""")
# 						db.commit()
# 						lists.append(p['district']['name_uz_ln'])
# 						text += f"{p['district']['name_uz_ln']} ----  {id}\n\n"
# 					else:
# 						pass
# 				except:
# 					pass
#
# 		else:
# 			pass
# 	return text

