from sqlite3 import connect
from key import *
from databas import *
from aiogram import Bot, exceptions, types
import asyncio
import aiohttp

bot = Bot(token=BOT_TOKEN)

class functions:
    @staticmethod
    async def check_on_start(user_id):
        rows = sql.execute("SELECT id FROM channels").fetchall()
        for row in rows:
            try:
                r = await bot.get_chat_member(chat_id=row[0], user_id=user_id)
                if r.status not in ['member', 'creator', 'administrator']:
                    return False
            except exceptions.TelegramAPIError:
                return False
        return True

class panel_func:
    @staticmethod
    async def channel_add(id):
        sql.execute("""CREATE TABLE IF NOT EXISTS channels(id INTEGER PRIMARY KEY)""")
        db.commit()
        sql.execute("INSERT OR IGNORE INTO channels VALUES(?)", (id,))
        db.commit()

    @staticmethod
    async def channel_delete(id):
        sql.execute("DELETE FROM channels WHERE id = ?", (id,))
        db.commit()

    @staticmethod
    async def channel_list():
        rows = sql.execute("SELECT id FROM channels").fetchall()
        result = ""
        for row in rows:
            id = row[0]
            try:
                all_details = await bot.get_chat(chat_id=id)
                result += (
                    f"------------------------------------------------\n"
                    f"Kanal useri: > {id}\n"
                    f"Kanal nomi: > {all_details.title}\n"
                    f"Kanal ID: > {all_details.id}\n"
                    f"Kanal haqida: > {all_details.description or 'Mavjud emas'}\n"
                )
            except exceptions.TelegramAPIError:
                result += f"Kanalni admin qiling: {id}\n"
        return result or "Hech qanday kanal mavjud emas."

async def forward_send_msg(chat_id: int, from_chat_id: int, message_id: int) -> bool:
    try:
        await bot.forward_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)
        return True
    except (exceptions.BotBlocked, exceptions.ChatNotFound, exceptions.UserDeactivated, exceptions.TelegramAPIError):
        sql.execute("DELETE FROM users WHERE user_id = ?", (chat_id,))
        db.commit()
        return False

async def send_message_chats(chat_id: int, from_chat_id: int, message_id: int) -> bool:
    try:
        await bot.copy_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)
        return True
    except (exceptions.BotBlocked, exceptions.ChatNotFound, exceptions.UserDeactivated, exceptions.TelegramAPIError):
        sql.execute("DELETE FROM users WHERE user_id = ?", (chat_id,))
        db.commit()
        return False

async def get_site_content(URL):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            return await resp.json()

async def search_vakant(user_id, page):
    user_data = sql.execute("SELECT region, district, specs, money, level FROM users WHERE user_id = ?", (user_id,)).fetchone()
    if not user_data:
        return "Foydalanuvchi topilmadi", [], 0, 0, 0

    reg0, reg1, specs, salary, level = user_data
    spec = f"&nskz={specs}&" if specs else "&"
    
    if reg1 and reg1 != 0:
        reg2 = sql.execute("SELECT dist_ids FROM locations WHERE districts = ?", (reg1,)).fetchone()
    else:
        reg2 = sql.execute("SELECT reg_ids FROM locations WHERE regions = ?", (reg0,)).fetchone()
    
    reg2 = reg2[0] if reg2 else 0

    salary_dict = {'⭕️Ahamiyatsiz️': 0, '1 mln ➕': 1000000, '3 mln ➕': 3000000}
    level_dict = {'⭕️Ahamiyatsiz': 0, "👨‍💼O'rta maxsus": 'ССПО', '👨‍🎓Oliy': "В%2FО"}

    salary_param = f"salary={salary_dict.get(salary, 0)}&" if salary and salary != '⭕️Ahamiyatsiz️' else '&'
    level_param = f"&min_education={level_dict.get(level, 0)}&" if level and level != '⭕️Ahamiyatsiz' else '&'

    URL = f"https://ishapi.mehnat.uz/api/v1/vacancies?per_page=5{level_param}{salary_param}company_soato_code={reg2}{spec}page={page}"
    soup = await get_site_content(URL)

    try:
        text_data = soup['data']['data']
        texts, ids = "", []
        for num, i in enumerate(text_data, start=soup['data']['from']):
            ids.append(i['id'])
            texts += (
                f"<b>👨‍💻{num}- Vakansiya</b>\n"
                f"🆔 ID: {i['id']}\n"
                f"🏢 Ish beruvchi: {i['company_name']}\n"
                f"💰 Maoshi: {i.get('position_salary', 'Mavjud emas')} so'm\n"
                f"📍 Joylashuvi: {i['region']['name_uz_ln']} {i['district']['name_uz_ln']}\n"
                f"➖➖➖➖➖➖➖➖➖➖\n\n"
            )
        return texts, ids, soup['data']['current_page'], soup['data']['from'], soup['data']['last_page']
    except:
        return "Xato yuz berdi", [], 0, 0, 0

async def vacancie_btn(ids, joriy, ga):
    region_choos = types.InlineKeyboardMarkup(row_width=5)
    for name, id in zip(range(ga, ga+10), ids):
        region_choos.insert(types.InlineKeyboardButton(str(name), callback_data=str(id)))
    region_choos.add(types.InlineKeyboardButton("⬅", callback_data=f"⬅{joriy}"))
    region_choos.insert(types.InlineKeyboardButton("❌", callback_data="❌"))
    region_choos.insert(types.InlineKeyboardButton("➡", callback_data=f"➡{joriy}"))
    return region_choos

async def saves_info(data):
    soup = await get_site_content(f'https://ishapi.mehnat.uz/api/v1/vacancies/{data}')
    soup1 = soup['data']
    status = "Aktiv" if soup1["active"] else "Band"

    return (
        f"<b>🏢 Kompaniya:</b> {soup1['company_name']}\n"
        f"<b>🧑‍🏭 Ish nomi:</b> {soup1['position_name']}\n"
        f"<b>ℹ️ Ish haqida:</b> {soup1['position_conditions']}\n"
        f"<b>📌 Majburiyatlari:</b> {soup1['position_duties']}\n"
        f"<b>📎 Talab:</b> {soup1['position_requirements']}\n"
        f"<b>💸 Maoshi:</b> {soup1.get('position_salary', 'Mavjud emas')} so'm\n"
        f"<b>📣 Holati:</b> {status}\n"
        f"<b>🗺 Manzil:</b> {soup1['region']['name_uz_ln']}, {soup1['district']['name_uz_ln']}\n"
        f"<b>📞 Telefon:</b> +{soup1['phones'][0]}"
    )

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

