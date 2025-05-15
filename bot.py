import telebot
from telebot import types
import json
import os
import time
import random

TOKEN = "7763395301:AAF3thVNH883Rzmz0RTpsx3wuiCG_VLpa-g"
ADMINS = [8121637254]  # Buraya kendi Telegram ID'nizi yazın

DATA_FILE = "users.json"
bot = telebot.TeleBot(TOKEN)

# Kullanıcı verilerini yükle veya oluştur
def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def check_user(uid):
    data = load_data()
    uid = str(uid)
    if uid not in data:
        data[uid] = {
            "balance": 50000,
            "last_bonus": 0,
            "last_mission": 0,
            "bank": 0,
            "last_faiz": 0,
            "cekilis_hakki": 1
        }
        save_data(data)
    return data

def is_admin(uid):
    return uid in ADMINS

def get_balance(uid):
    data = check_user(uid)
    return data[str(uid)]["balance"]

def add_balance(uid, amount):
    data = check_user(uid)
    uid = str(uid)
    data[uid]["balance"] += amount
    save_data(data)

def subtract_balance(uid, amount):
    data = check_user(uid)
    uid = str(uid)
    if data[uid]["balance"] >= amount:
        data[uid]["balance"] -= amount
        save_data(data)
        return True
    else:
        return False

@bot.message_handler(commands=["start"])
def cmd_start(m):
    check_user(m.from_user.id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("Bakiye", callback_data="bakiye"),
        types.InlineKeyboardButton("Bonus", callback_data="bonus"),
        types.InlineKeyboardButton("Kazı Kazan", callback_data="kazikazan"),
        types.InlineKeyboardButton("Günlük Görev", callback_data="gorev"),
        types.InlineKeyboardButton("Slot", callback_data="slot"),
        types.InlineKeyboardButton("Hırsızlık", callback_data="hirsizlik"),
        types.InlineKeyboardButton("Bahis", callback_data="bahis"),
        types.InlineKeyboardButton("Çekiliş", callback_data="cekilis"),
        types.InlineKeyboardButton("Faiz", callback_data="faiz"),
        types.InlineKeyboardButton("Lider", callback_data="lider"),
    ]
    markup.add(*buttons)

    reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
    reply.row("/bakiye", "/id", "/bonus", "/kazikazan")
    reply.row("/görev", "/slot", "/hırsızlık", "/bahis")
    reply.row("/çekiliş", "/faiz", "/lider")
    reply.row("/paragonder", "/parabas", "/adminekle")

    bot.send_message(m.chat.id, "Kumar Botuna Hoş Geldin! Aşağıdaki menüden işlem seçebilirsin.", reply_markup=reply)
    bot.send_message(m.chat.id, "İşlem menüsü:", reply_markup=markup)

@bot.message_handler(commands=["id"])
def cmd_id(m):
    bot.reply_to(m, f"ID'niz: {m.from_user.id}")

@bot.message_handler(commands=["bakiye"])
def cmd_bakiye(m):
    bal = get_balance(m.from_user.id)
    bot.reply_to(m, f"Bakiyeniz: {bal} TL")

@bot.callback_query_handler(func=lambda c: True)
def callback_handler(c):
    uid = c.from_user.id
    data = check_user(uid)

    if c.data == "bakiye":
        bot.answer_callback_query(c.id, f"Bakiyeniz: {data[str(uid)]['balance']} TL", show_alert=True)

    elif c.data == "bonus":
        now = time.time()
        last = data[str(uid)]["last_bonus"]
        if now - last >= 24*3600:
            bonus_amt = 50000
            data[str(uid)]["balance"] += bonus_amt
            data[str(uid)]["last_bonus"] = now
            save_data(data)
            bot.answer_callback_query(c.id, f"Bonus olarak {bonus_amt} TL kazandınız!", show_alert=True)
        else:
            kalan = int(24*3600 - (now - last))
            bot.answer_callback_query(c.id, f"Bonus 24 saatte bir alınır. Kalan süre: {kalan//3600} saat {(kalan%3600)//60} dakika", show_alert=True)

    elif c.data == "kazikazan":
        kazikazan_game(c.message)

    elif c.data == "gorev":
        gorev_system(c.message)

    elif c.data == "slot":
        slot_game(c.message)

    elif c.data == "hirsizlik":
        bot.send_message(c.message.chat.id, "Hırsızlık yapmak için komut: /hirsiz <hedef_id>")

    elif c.data == "bahis":
        bot.send_message(c.message.chat.id, "Bahis yapmak için komut: /bahis <miktar>")

    elif c.data == "cekilis":
        cekilis_game(c.message)

    elif c.data == "faiz":
        faiz_system(c.message)

    elif c.data == "lider":
        lider_tablosu(c.message)

# Bonus komutu (komut olarak)
@bot.message_handler(commands=["bonus"])
def cmd_bonus(m):
    uid = m.from_user.id
    data = check_user(uid)
    now = time.time()
    last = data[str(uid)]["last_bonus"]
    if now - last >= 24*3600:
        bonus_amt = 50000
        data[str(uid)]["balance"] += bonus_amt
        data[str(uid)]["last_bonus"] = now
        save_data(data)
        bot.reply_to(m, f"Bonus olarak {bonus_amt} TL kazandınız!")
    else:
        kalan = int(24*3600 - (now - last))
        bot.reply_to(m, f"Bonus 24 saatte bir alınır. Kalan süre: {kalan//3600} saat {(kalan%3600)//60} dakika")

# Kazı Kazan oyunu
def kazikazan_game(m):
    uid = m.from_user.id
    data = check_user(uid)
    chance = random.randint(1, 100)
    if chance <= 30:
        kazanilan = random.randint(10000, 70000)
        data[str(uid)]["balance"] += kazanilan
        save_data(data)
        bot.send_message(m.chat.id, f"Tebrikler! Kazı kazan oyununda {kazanilan} TL kazandınız.")
    else:
        kaybedilen = random.randint(1000, 10000)
        if data[str(uid)]["balance"] >= kaybedilen:
            data[str(uid)]["balance"] -= kaybedilen
            save_data(data)
            bot.send_message(m.chat.id, f"Üzgünüz, {kaybedilen} TL kaybettiniz.")
        else:
            bot.send_message(m.chat.id, "Yeterli bakiyeniz yok. Kaybetmediniz ama kazanamadınız da.")

# Günlük görev sistemi
@bot.message_handler(commands=["görev", "gorev"])
def gorev_system(m):
    uid = m.from_user.id
    data = check_user(uid)
    now = time.time()
    last = data[str(uid)]["last_mission"]
    if now - last >= 24*3600:
        odul = random.randint(10000, 50000)
        data[str(uid)]["balance"] += odul
        data[str(uid)]["last_mission"] = now
        save_data(data)
        bot.reply_to(m, f"Günlük görev başarıyla tamamlandı! {odul} TL kazandınız.")
    else:
        kalan = int(24*3600 - (now - last))
        bot.reply_to(m, f"Günlük görev zaten tamamlandı. Yeni görev için {kalan//3600} saat {(kalan%3600)//60} dakika bekleyin.")

# Slot oyunu
@bot.message_handler(commands=["slot"])
def slot_game(m):
    uid = m.from_user.id
    data = check_user(uid)

    semboller = ["🍒", "🍋", "🍉", "🔔", "⭐", "7️⃣"]
    slot1 = random.choice(semboller)
    slot2 = random.choice(semboller)
    slot3 = random.choice(semboller)

    sonuc = f"{slot1} | {slot2} | {slot3}"

    if slot1 == slot2 == slot3:
        odul = random.randint(50000, 150000)
        data[str(uid)]["balance"] += odul
        save_data(data)
        bot.reply_to(m, f"Slot sonucu: {sonuc}\nTEBRİKLER! {odul} TL kazandınız!")
    else:
        kayip = random.randint(10000, 50000)
        if data[str(uid)]["balance"] >= kayip:
            data[str(uid)]["balance"] -= kayip
            save_data(data)
            bot.reply_to(m, f"Slot sonucu: {sonuc}\nÜzgünüz, {kayip} TL kaybettiniz.")
        else:
            bot.reply_to(m, f"Slot sonucu: {sonuc}\nYeterli bakiyeniz yok, kaybetmediniz ama kazanamadınız da.")

# Hırsızlık komutu: /hirsiz <id>
@bot.message_handler(commands=["hirsiz", "hırsızlık"])
def hirsizlik(m):
    from_id = m.from_user.id
    data = check_user(from_id)
    args = m.text.split()
    if len(args) < 2:
        bot.reply_to(m, "Kullanım: /hirsiz <hedef_id>")
        return
    hedef_id = args[1]
    data = check_user(hedef_id)
    hedef_bal = data[str(hedef_id)]["balance"]
    if hedef_bal < 1000:
        bot.reply_to(m, "Hedefin yeterli bakiyesi yok.")
        return
    kazanma_sansi = random.randint(1, 100)
    if kazanma_sansi <= 40:
        miktar = random.randint(1000, min(hedef_bal, 20000))
        data[str(hedef_id)]["balance"] -= miktar
        data[str(from_id)]["balance"] += miktar
        save_data(data)
        bot.reply_to(m, f"Tebrikler! {miktar} TL çaldınız.")
    else:
        ceza = random.randint(1000, 5000)
        if data[str(from_id)]["balance"] >= ceza:
            data[str(from_id)]["balance"] -= ceza
            save_data(data)
            bot.reply_to(m, f"Yakalandınız! {ceza} TL ceza ödediniz.")
        else:
            bot.reply_to(m, "Yakalandınız ama ceza ödeyecek paranız yok.")

# Bahis oyunu: /bahis <miktar>
@bot.message_handler(commands=["bahis"])
def bahis(m):
    uid = m.from_user.id
    data = check_user(uid)
    args = m.text.split()
    if len(args) < 2:
        bot.reply_to(m, "Kullanım: /bahis <miktar>")
        return
    try:
        miktar = int(args[1])
    except:
        bot.reply_to(m, "Lütfen geçerli bir sayı girin.")
        return
    if miktar < 1000:
        bot.reply_to(m, "Minimum bahis 1000 TL'dir.")
        return
    if data[str(uid)]["balance"] < miktar:
        bot.reply_to(m, "Yeterli bakiyeniz yok.")
        return
    kazanma_sansi = random.randint(1, 100)
    if kazanma_sansi <= 50:
        kazanilan = miktar * 2
        data[str(uid)]["balance"] += kazanilan
        save_data(data)
        bot.reply_to(m, f"Tebrikler! Bahsi kazandınız ve {kazanilan} TL kazandınız.")
    else:
        data[str(uid)]["balance"] -= miktar
        save_data(data)
        bot.reply_to(m, f"Bahsi kaybettiniz ve {miktar} TL kaybettiniz.")

# Çekiliş oyunu
@bot.message_handler(commands=["çekiliş
