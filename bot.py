import asyncio
import json
import random
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

TOKEN = "7763395301:AAF3thVNH883Rzmz0RTpsx3wuiCG_VLpa-g"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Veri dosyası
DATA_FILE = "data.json"

# Sabit admin ID'leri
SABIT_ADMINLER = [8121637254, 987654321]  # Buraya sabit admin ID'lerini ekle

# Başlangıç TL, bonus ve diğer sabitler
BAŞLANGIÇ_TL = 10000
BONUS_TL = 50000
BONUS_SÜRE = 86400  # 24 saat

# Alt menü
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("/start"), KeyboardButton("/bonus"))
main_menu.add(KeyboardButton("/bakiye"), KeyboardButton("/kazikazan 100"))
main_menu.add(KeyboardButton("/slot 100"), KeyboardButton("/risk 100"))

# Veri yükle
def veri_yükle():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# Veri kaydet
def veri_kaydet(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Kullanıcı başlatma
def kullanıcı_kontrol(user_id):
    data = veri_yükle()
    if str(user_id) not in data:
        data[str(user_id)] = {
            "tl": BAŞLANGIÇ_TL,
            "last_bonus": "1970-01-01 00:00:00",
            "admin": False
        }
        veri_kaydet(data)

# Admin kontrol
def admin_mi(user_id):
    return user_id in SABIT_ADMINLER or veri_yükle().get(str(user_id), {}).get("admin", False)

# TL güncelleme
def tl_güncelle(user_id, miktar):
    data = veri_yükle()
    data[str(user_id)]["tl"] += miktar
    veri_kaydet(data)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kullanıcı_kontrol(message.from_user.id)
    await message.answer(f"Hoş geldin {message.from_user.first_name}!\nHesabına {BAŞLANGIÇ_TL} TL yüklendi! 💸", reply_markup=main_menu)

@dp.message_handler(commands=["bakiye"])
async def bakiye(message: types.Message):
    kullanıcı_kontrol(message.from_user.id)
    data = veri_yükle()
    bakiye = data[str(message.from_user.id)]["tl"]
    await message.answer(f"Bakiyen: {bakiye:,} TL 💰")

@dp.message_handler(commands=["bonus"])
async def bonus(message: types.Message):
    kullanıcı_kontrol(message.from_user.id)
    data = veri_yükle()
    user = data[str(message.from_user.id)]
    son = datetime.strptime(user["last_bonus"], "%Y-%m-%d %H:%M:%S")
    if datetime.now() - son >= timedelta(seconds=BONUS_SÜRE):
        user["last_bonus"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user["tl"] += BONUS_TL
        veri_kaydet(data)
        await message.answer(f"Günlük bonus alındı! +{BONUS_TL:,} TL 🎁")
    else:
        kalan = timedelta(seconds=BONUS_SÜRE) - (datetime.now() - son)
        await message.answer(f"Bonus zaten alındı! ⏳\nYeniden almak için bekle: {str(kalan).split('.')[0]}")

@dp.message_handler(commands=["kazikazan"])
async def kazikazan(message: types.Message):
    kullanıcı_kontrol(message.from_user.id)
    try:
        miktar = int(message.text.split()[1])
    except:
        return await message.reply("Kullanım: /kazikazan [miktar]")

    data = veri_yükle()
    user = data[str(message.from_user.id)]

    if user["tl"] < miktar:
        return await message.reply("Yetersiz bakiye! ❌")

    user["tl"] -= miktar
    if random.randint(1, 100) <= 30:
        kazanç = miktar * 3
        user["tl"] += kazanç
        await message.answer(f"Tebrikler! Kazı Kazan'dan {kazanç:,} TL kazandın! 🎉")
    else:
        await message.answer("Üzgünüm, bu sefer olmadı... ☹️")
    veri_kaydet(data)

@dp.message_handler(commands=["risk"])
async def risk(message: types.Message):
    kullanıcı_kontrol(message.from_user.id)
    try:
        miktar = int(message.text.split()[1])
    except:
        return await message.reply("Kullanım: /risk [miktar]")

    data = veri_yükle()
    user = data[str(message.from_user.id)]

    if user["tl"] < miktar:
        return await message.reply("TL yetersiz! ❌")

    user["tl"] -= miktar
    if random.randint(1, 100) <= 40:
        kazanç = miktar * 2
        user["tl"] += kazanç
        await message.answer(f"Şanslısın! {kazanç:,} TL kazandın! 🍀")
    else:
        await message.answer("Kaybettin... Riskin sonucu bu! 💀")
    veri_kaydet(data)

@dp.message_handler(commands=["slot"])
async def slot(message: types.Message):
    kullanıcı_kontrol(message.from_user.id)
    try:
        miktar = int(message.text.split()[1])
    except:
        return await message.reply("Kullanım: /slot [miktar]")

    data = veri_yükle()
    user = data[str(message.from_user.id)]

    if user["tl"] < miktar:
        return await message.reply("TL yetersiz! ❌")

    user["tl"] -= miktar
    if random.randint(1, 100) <= 30:
        kazanç = miktar * 4
        user["tl"] += kazanç
        await message.answer(f"JACKPOT! Slotta {kazanç:,} TL kazandın! 🎰")
    else:
        await message.answer("Slot kaybettin... Tekrar dene! 🎲")
    veri_kaydet(data)

@dp.message_handler(commands=["admin"])
async def admin_ekle(message: types.Message):
    kullanıcı_kontrol(message.from_user.id)
    if not admin_mi(message.from_user.id):
        return await message.reply("Bu komutu sadece adminler kullanabilir! 🚫")

    try:
        hedef_id = int(message.text.split()[1])
    except:
        return await message.reply("Kullanım: /admin [id]")

    data = veri_yükle()
    kullanıcı_kontrol(hedef_id)
    data[str(hedef_id)]["admin"] = True
    veri_kaydet(data)
    await message.answer(f"{hedef_id} artık admin! 👑")

@dp.message_handler(commands=["parabasma"])
async def parabasma(message: types.Message):
    if not admin_mi(message.from_user.id):
        return await message.reply("Sadece adminler para basabilir! 💼")

    try:
        _, hedef_id, miktar = message.text.split()
        hedef_id = int(hedef_id)
        miktar = int(miktar)
    except:
        return await message.reply("Kullanım: /parabasma [id] [miktar]")

    kullanıcı_kontrol(hedef_id)
    tl_güncelle(hedef_id, miktar)
    await message.answer(f"{hedef_id} kişisine {miktar:,} TL basıldı! 🤑")

@dp.message_handler(commands=["paragönder"])
async def paragönder(message: types.Message):
    kullanıcı_kontrol(message.from_user.id)
    try:
        _, hedef_id, miktar = message.text.split()
        hedef_id = int(hedef_id)
        miktar = int(miktar)
    except:
        return await message.reply("Kullanım: /paragönder [id] [miktar]")

    data = veri_yükle()
    kullanıcı_kontrol(hedef_id)

    if data[str(message.from_user.id)]["tl"] < miktar:
        return await message.reply("Yetersiz bakiye! 💸")

    data[str(message.from_user.id)]["tl"] -= miktar
    data[str(hedef_id)]["tl"] += miktar
    veri_kaydet(data)
    await message.answer(f"{miktar:,} TL başarıyla gönderildi! ✉️")

@dp.message_handler(commands=["id"])
async def idbilgi(message: types.Message):
    kullanıcı_kontrol(message.from_user.id)
    if not message.reply_to_message:
        return await message.reply("Kullanmak için bir mesaja yanıt ver: /id")

    hedef = message.reply_to_message.from_user
    kullanıcı_kontrol(hedef.id)
    data = veri_yükle()
    tl = data[str(hedef.id)]["tl"]
    await message.answer(f"{hedef.first_name} adlı kullanıcının bakiyesi: {tl:,} TL 💼")

@dp.message_handler(commands=["top"])
async def toplist(message: types.Message):
    data = veri_yükle()
    sıralama = sorted(data.items(), key=lambda x: x[1]["tl"], reverse=True)[:10]
    liste = "\n".join([f"{i+1}. {uid} - {veri['tl']:,} TL" for i, (uid, veri) in enumerate(sıralama)])
    await message.answer(f"🏆 En Zenginler:\n{liste}")

# Botu çalıştır
if __name__ == "__main__":
    print("Bot çalışıyor...")
    executor.start_polling(dp, skip_updates=True)7763395301:AAF3thVNH883Rzmz0RTpsx3wuiCG_VLpa-g
