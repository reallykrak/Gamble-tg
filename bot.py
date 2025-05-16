import telebot
from telebot import types
import json
import os
import random
from datetime import datetime, timedelta

BOT_TOKEN = "7763395301:AAF3thVNH883Rzmz0RTpsx3wuiCG_VLpa-g"
bot = telebot.TeleBot(BOT_TOKEN)

DATA_FILE = "veri.json"

def veri_yukle():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def veri_kaydet(veri):
    with open(DATA_FILE, "w") as f:
        json.dump(veri, f, indent=4)

def kullanici_kontrol_et(user_id):
    veri = veri_yukle()
    if str(user_id) not in veri:
        veri[str(user_id)] = {
            "bakiye": 1000,
            "banka": 0,
            "admin": False,
            "giris": str(datetime.now()),
            "bonus": "",
            "görev": ""
        }
        veri_kaydet(veri)

@bot.message_handler(commands=["start"])
def start(m):
    kullanici_kontrol_et(m.from_user.id)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🎰 Slot", "🎁 Bonus", "💸 Para Gönder")
    kb.row("🏦 Banka", "🎯 Bahis", "🎫 Kazı Kazan")
    bot.reply_to(m, f"Merhaba {m.from_user.first_name}! Kumar Botuna hoş geldin!", reply_markup=kb)

@bot.message_handler(commands=["bakiye"])
def bakiye(m):
    veri = veri_yukle()
    user = veri[str(m.from_user.id)]
    bot.reply_to(m, f"💰 Bakiye: {user['bakiye']} TL\n🏦 Banka: {user['banka']} TL")

@bot.message_handler(commands=["bonus"])
def bonus(m):
    veri = veri_yukle()
    user = veri[str(m.from_user.id)]
    bugun = datetime.now().date()
    if user["bonus"] == str(bugun):
        bot.reply_to(m, "❌ Bugün zaten bonus aldın!")
        return
    bonus_miktar = random.randint(250, 1000)
    user["bakiye"] += bonus_miktar
    user["bonus"] = str(bugun)
    veri_kaydet(veri)
    bot.reply_to(m, f"🎁 Günlük bonus: {bonus_miktar} TL eklendi!")

@bot.message_handler(commands=["slot"])
def slot(m):
    veri = veri_yukle()
    user = veri[str(m.from_user.id)]
    if user["bakiye"] < 100:
        bot.reply_to(m, "❌ Slot oynamak için en az 100 TL gerekir!")
        return
    user["bakiye"] -= 100
    slotlar = ["🍒", "🍋", "🔔", "💎", "7️⃣"]
    sonuc = [random.choice(slotlar) for _ in range(3)]
    mesaj = "🎰 | " + " | ".join(sonuc) + " |\n"
    if sonuc[0] == sonuc[1] == sonuc[2]:
        kazan = 1000
        user["bakiye"] += kazan
        mesaj += f"✨ Tebrikler! {kazan} TL kazandın!"
    else:
        mesaj += "😢 Üzgünüm, kazanamadın."
    veri_kaydet(veri)
    bot.reply_to(m, mesaj)

@bot.message_handler(commands=["para"])
def para_gonder(m):
    try:
        veri = veri_yukle()
        user = veri[str(m.from_user.id)]
        args = m.text.split()
        hedef = int(args[1])
        miktar = int(args[2])
        if user["bakiye"] < miktar:
            return bot.reply_to(m, "❌ Yetersiz bakiye!")
        kullanici_kontrol_et(hedef)
        user["bakiye"] -= miktar
        veri[str(hedef)]["bakiye"] += miktar
        veri_kaydet(veri)
        bot.reply_to(m, f"✅ {hedef} ID'li kullanıcıya {miktar} TL gönderildi.")
    except:
        bot.reply_to(m, "❗ Kullanım: /para kullanıcı_id miktar")

@bot.message_handler(commands=["paraekle"])
def admin_para(m):
    veri = veri_yukle()
    user = veri[str(m.from_user.id)]
    if not user["admin"]:
        return bot.reply_to(m, "❌ Yetkin yok.")
    try:
        _, hedef, miktar = m.text.split()
        hedef = int(hedef)
        miktar = int(miktar)
        kullanici_kontrol_et(hedef)
        veri[str(hedef)]["bakiye"] += miktar
        veri_kaydet(veri)
        bot.reply_to(m, f"✅ {hedef} kullanıcısına {miktar} TL eklendi.")
    except:
        bot.reply_to(m, "❗ Kullanım: /paraekle kullanıcı_id miktar")

@bot.message_handler(commands=["admin"])
def admin_ekle(m):
    veri = veri_yukle()
    user = veri[str(m.from_user.id)]
    if not user["admin"]:
        return bot.reply_to(m, "❌ Yetkin yok.")
    try:
        _, hedef = m.text.split()
        veri[str(int(hedef))]["admin"] = True
        veri_kaydet(veri)
        bot.reply_to(m, f"✅ {hedef} artık admin.")
    except:
        bot.reply_to(m, "❗ Kullanım: /admin kullanıcı_id")

@bot.message_handler(commands=["liderlik"])
def liderlik(m):
    veri = veri_yukle()
    sirali = sorted(veri.items(), key=lambda x: x[1]["bakiye"] + x[1]["banka"], reverse=True)
    mesaj = "🏆 En Zenginler:\n"
    for i, (uid, data) in enumerate(sirali[:10], 1):
        mesaj += f"{i}. ID {uid} — {data['bakiye']} + {data['banka']} TL\n"
    bot.reply_to(m, mesaj)

@bot.message_handler(func=lambda m: True)
def cevapla(m):
    if m.text == "🎰 Slot":
        slot(m)
    elif m.text == "🎁 Bonus":
        bonus(m)
    elif m.text == "💸 Para Gönder":
        bot.reply_to(m, "Kullanım: /para kullanıcı_id miktar")
    elif m.text == "🏦 Banka":
        bot.reply_to(m, "Kullanım: /faiz | /banka yatır/çek miktar")
    elif m.text == "🎯 Bahis":
        bot.reply_to(m, "Komut: /bahis <1-6>")
    elif m.text == "🎫 Kazı Kazan":
        bot.reply_to(m, "Komut: /kazikazan")

print("Bot aktif.")
bot.infinity_polling()
