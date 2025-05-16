import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

api_id = 25404254  # Buraya kendi api_id'nizi yazın
api_hash = "a0159a4e4d780841ac88f0c002d0231a"
bot_token = "7763395301:AAF3thVNH883Rzmz0RTpsx3wuiCG_VLpa-g"

app = Client("kumar_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

users = {}  # {user_id: {"coin": 50000, "bank": 0, "borsa": {"altin": 0, "elmas": 0, "dolar": 0, "euro": 0}}}

borsa_fiyat = {
    "altin": 1000,
    "elmas": 2000,
    "dolar": 10,
    "euro": 12
}

# --- Yardımcı Fonksiyonlar --- #
def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 Günlük Bonus", callback_data="bonus")],
        [InlineKeyboardButton("🎰 Slot", callback_data="slot"),
         InlineKeyboardButton("🎯 Kazı Kazan", callback_data="kazi")],
        [InlineKeyboardButton("🏦 Banka & Faiz", callback_data="banka")],
        [InlineKeyboardButton("📉 Borsa", callback_data="borsa")],
    ])

def init_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "coin": 50000,
            "bank": 0,
            "borsa": {"altin": 0, "elmas": 0, "dolar": 0, "euro": 0}
        }

# --- Başlangıç --- #
@app.on_message(filters.command("start") & filters.group)
async def start(_, message: Message):
    init_user(message.from_user.id)
    await message.reply(f"Merhaba {message.from_user.first_name}! Kumar botuna hoş geldin.\nAşağıdaki menüden işlemlerini seçebilirsin.", reply_markup=menu())

# --- Callback Handler --- #
@app.on_callback_query()
async def callback_handler(client, callback_query):
    user_id = callback_query.from_user.id
    init_user(user_id)
    data = callback_query.data

    if data == "bonus":
        users[user_id]["coin"] += 50000
        await callback_query.message.edit_text("🎁 Günlük bonus alındı! +50,000 coin", reply_markup=menu())

    elif data == "slot":
        await callback_query.message.edit_text("🎰 Ne kadar coin ile slot oynamak istersin? (örn: /slot 5000)")

    elif data == "kazi":
        await callback_query.message.edit_text("🎯 Ne kadar coin ile kazı kazan oynamak istersin? (örn: /kazi 1000)")

    elif data == "banka":
        bank = users[user_id]["bank"]
        coin = users[user_id]["coin"]
        await callback_query.message.edit_text(f"🏦 Bankadaki coin: {bank}\nCüzdan: {coin}\n\nPara çekme: /cek 1000\nPara yatırma: /yatir 1000\nFaiz alma: /faiz", reply_markup=menu())

    elif data == "borsa":
        b = borsa_fiyat
        p = users[user_id]["borsa"]
        msg = f"📉 Güncel Borsa Fiyatları:\nAltın: {b['altin']} | Senin: {p['altin']}\nElmas: {b['elmas']} | Senin: {p['elmas']}\nDolar: {b['dolar']} | Senin: {p['dolar']}\nEuro: {b['euro']} | Senin: {p['euro']}\n\nSatın Al: /al altin 1\nSat: /sat altin 1"
        await callback_query.message.edit_text(msg, reply_markup=menu())

# --- Slot --- #
@app.on_message(filters.command("slot") & filters.group)
async def slot(_, message: Message):
    try:
        miktar = int(message.text.split()[1])
        uid = message.from_user.id
        init_user(uid)
        if users[uid]["coin"] < miktar:
            return await message.reply("Yetersiz coin!")
        kazandin = random.randint(1, 100) <= 40
        if kazandin:
            kazanc = miktar * 2
            users[uid]["coin"] += kazanc
            await message.reply(f"🎰 Kazandın! +{kazanc} coin")
        else:
            users[uid]["coin"] -= miktar
            await message.reply(f"🎰 Kaybettin! -{miktar} coin")
    except:
        await message.reply("Kullanım: /slot <miktar>")

# --- Kazı Kazan --- #
@app.on_message(filters.command("kazi") & filters.group)
async def kazi(_, message: Message):
    try:
        miktar = int(message.text.split()[1])
        uid = message.from_user.id
        init_user(uid)
        if users[uid]["coin"] < miktar:
            return await message.reply("Yetersiz coin!")
        kazandin = random.randint(1, 100) <= 30
        if kazandin:
            kazanc = miktar * 2
            users[uid]["coin"] += kazanc
            await message.reply(f"🎯 Kazandın! +{kazanc} coin")
        else:
            users[uid]["coin"] -= miktar
            await message.reply(f"🎯 Kaybettin! -{miktar} coin")
    except:
        await message.reply("Kullanım: /kazi <miktar>")

# --- Banka --- #
@app.on_message(filters.command("yatir") & filters.group)
async def yatir(_, message: Message):
    try:
        miktar = int(message.text.split()[1])
        uid = message.from_user.id
        if users[uid]["coin"] < miktar:
            return await message.reply("Yetersiz coin!")
        users[uid]["coin"] -= miktar
        users[uid]["bank"] += miktar
        await message.reply(f"🏦 {miktar} coin bankaya yatırıldı.")
    except:
        await message.reply("Kullanım: /yatir <miktar>")

@app.on_message(filters.command("cek") & filters.group)
async def cek(_, message: Message):
    try:
        miktar = int(message.text.split()[1])
        uid = message.from_user.id
        if users[uid]["bank"] < miktar:
            return await message.reply("Bankada bu kadar yok!")
        users[uid]["bank"] -= miktar
        users[uid]["coin"] += miktar
        await message.reply(f"🏦 {miktar} coin cüzdana çekildi.")
    except:
        await message.reply("Kullanım: /cek <miktar>")

@app.on_message(filters.command("faiz") & filters.group)
async def faiz(_, message: Message):
    uid = message.from_user.id
    faiz = int(users[uid]["bank"] * 0.05)
    users[uid]["bank"] += faiz
    await message.reply(f"💰 Bankadan faiz aldın! +{faiz} coin")

# --- Borsa --- #
@app.on_message(filters.command("al") & filters.group)
async def al(_, message: Message):
    try:
        _, tur, adet = message.text.split()
        adet = int(adet)
        fiyat = borsa_fiyat[tur] * adet
        uid = message.from_user.id
        if users[uid]["coin"] < fiyat:
            return await message.reply("Yetersiz coin!")
        users[uid]["coin"] -= fiyat
        users[uid]["borsa"][tur] += adet
        await message.reply(f"✅ {adet} adet {tur} satın alındı.")
    except:
        await message.reply("Kullanım: /al <altin/elmas/dolar/euro> <adet>")

@app.on_message(filters.command("sat") & filters.group)
async def sat(_, message: Message):
    try:
        _, tur, adet = message.text.split()
        adet = int(adet)
        uid = message.from_user.id
        if users[uid]["borsa"][tur] < adet:
            return await message.reply("Bu kadar {tur} yok!")
        gelir = borsa_fiyat[tur] * adet
        users[uid]["borsa"][tur] -= adet
        users[uid]["coin"] += gelir
        await message.reply(f"💱 {adet} adet {tur} satıldı. +{gelir} coin")
    except:
        await message.reply("Kullanım: /sat <altin/elmas/dolar/euro> <adet>")

# --- Borsa Güncellemesi --- #
async def borsa_guncelle():
    while True:
        for item in borsa_fiyat:
            degisim = random.randint(-50, 50)
            borsa_fiyat[item] = max(1, borsa_fiyat[item] + degisim)
        await asyncio.sleep(60)

# --- Bot Başlat --- #
@app.on_message(filters.private)
async def private_block(_, message):
    await message.reply("Bu bot sadece gruplarda kullanılabilir.")

@app.on_message(filters.command("bakiye") & filters.group)
async def bakiye(_, message):
    uid = message.from_user.id
    c = users[uid]["coin"]
    await message.reply(f"Mevcut coin: {c}")

@app.on_message(filters.command("id") & filters.group)
async def id(_, message):
    await message.reply(f"Kullanıcı ID: {message.from_user.id}")

# --- Botu Başlat --- #
app.start()
asyncio.get_event_loop().create_task(borsa_guncelle())
print("Bot çalışıyor...")
app.idle()
