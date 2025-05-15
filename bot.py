import json, random, time
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

DATA_FILE = "users.json"
ADMINS = [8121637254]  # Kendi Telegram ID'ni buraya ekle

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def get_user(user_id):
    data = load_data()
    if str(user_id) not in data:
        data[str(user_id)] = {"jeton": 500, "admin": False, "bonus": 0, "faiz": 0, "görev": 0}
        save_data(data)
    return data

def update_user(user_id, field, value):
    data = load_data()
    data[str(user_id)][field] = value
    save_data(data)

def change_jeton(user_id, amount):
    data = load_data()
    data[str(user_id)]["jeton"] += amount
    save_data(data)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    get_user(update.effective_user.id)
    keyboard = [["/bakiye", "/bonus", "/faiz"], ["/görev", "/slot", "/hırsızlık"],
                ["/bahis", "/çekiliş", "/kazıkazan"], ["/gönder", "/top", "/yapımcı"]]
    await update.message.reply_text("Hoş geldin! Kumar Botuna başladın.", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

async def bakiye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_user(update.effective_user.id)
    await update.message.reply_text(f"Jeton bakiyen: {data[str(update.effective_user.id)]['jeton']}")

async def bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    data = get_user(uid)
    if time.time() - data[uid]["bonus"] < 3600:
        await update.message.reply_text("Bonus almak için 1 saat beklemelisin.")
        return
    bonus = random.randint(50, 150)
    change_jeton(uid, bonus)
    update_user(uid, "bonus", time.time())
    await update.message.reply_text(f"{bonus} jeton bonus kazandın!")

async def faiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    data = get_user(uid)
    if time.time() - data[uid]["faiz"] < 3600:
        await update.message.reply_text("Faiz için 1 saat beklemelisin.")
        return
    faiz = int(data[uid]["jeton"] * 0.1)
    change_jeton(uid, faiz)
    update_user(uid, "faiz", time.time())
    await update.message.reply_text(f"{faiz} jeton faiz kazandın!")

async def görev(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    data = get_user(uid)
    if time.time() - data[uid]["görev"] < 86400:
        await update.message.reply_text("Yeni görev için 24 saat beklemelisin.")
        return
    ödül = random.randint(100, 300)
    change_jeton(uid, ödül)
    update_user(uid, "görev", time.time())
    await update.message.reply_text(f"Görev tamamlandı! {ödül} jeton kazandın.")

async def slot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    emojis = ["🍒", "🍋", "🍉"]
    result = [random.choice(emojis) for _ in range(3)]
    kazan = result[0] == result[1] == result[2]
    if kazan:
        change_jeton(uid, 100)
        await update.message.reply_text(f"{' | '.join(result)}\nKazandın! +100 jeton")
    else:
        change_jeton(uid, -50)
        await update.message.reply_text(f"{' | '.join(result)}\nKaybettin! -50 jeton")

async def hırsızlık(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    data = get_user(uid)
    hedef = random.choice([u for u in data if u != uid])
    miktar = random.randint(50, 200)
    success = random.random() < 0.5
    if success and data[hedef]["jeton"] >= miktar:
        change_jeton(hedef, -miktar)
        change_jeton(uid, miktar)
        await update.message.reply_text(f"{miktar} jeton çaldın!")
    else:
        await update.message.reply_text("Hırsızlık başarısız oldu!")

async def bahis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    try:
        miktar = int(context.args[0])
    except:
        await update.message.reply_text("Kullanım: /bahis <miktar>")
        return
    if miktar <= 0:
        return
    data = get_user(uid)
    if data[uid]["jeton"] < miktar:
        await update.message.reply_text("Yetersiz bakiye.")
        return
    kazan = random.random() < 0.5
    change_jeton(uid, miktar if kazan else -miktar)
    msg = f"Bahis kazandın! +{miktar}" if kazan else f"Bahis kaybettin! -{miktar}"
    await update.message.reply_text(msg)

async def çekiliş(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    winner = random.choice(list(data.keys()))
    ödül = 300
    change_jeton(winner, ödül)
    await update.message.reply_text(f"Çekilişi kazanan: {winner} (+{ödül} jeton)")

async def kazıkazan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    change_jeton(uid, -50)
    kazan = random.random() < 0.3
    if kazan:
        ödül = random.randint(100, 500)
        change_jeton(uid, ödül)
        await update.message.reply_text(f"Kazandın! +{ödül} jeton")
    else:
        await update.message.reply_text("Kaybettin! Daha şanslı olabilirsin.")

async def gönder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        hedef = context.args[0]
        miktar = int(context.args[1])
    except:
        await update.message.reply_text("Kullanım: /gönder <id> <miktar>")
        return
    uid = str(update.effective_user.id)
    data = get_user(uid)
    if data[uid]["jeton"] < miktar:
        await update.message.reply_text("Yetersiz bakiye.")
        return
    get_user(hedef)
    change_jeton(uid, -miktar)
    change_jeton(hedef, miktar)
    await update.message.reply_text(f"{miktar} jeton gönderildi.")

async def id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"ID: {update.effective_user.id}")

async def yapımcı(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot yapımcısı: @reallykrak")

async def para(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    if uid not in ADMINS:
        await update.message.reply_text("Yetkin yok.")
        return
    try:
        miktar = int(context.args[0])
        change_jeton(uid, miktar)
        await update.message.reply_text(f"{miktar} jeton eklendi.")
    except:
        await update.message.reply_text("Kullanım: /para <miktar>")

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    if uid not in ADMINS:
        await update.message.reply_text("Yetkin yok.")
        return
    try:
        hedef = context.args[0]
        data = get_user(hedef)
        data[hedef]["admin"] = True
        save_data(data)
        await update.message.reply_text(f"{hedef} artık admin.")
    except:
        await update.message.reply_text("Kullanım: /admin <id>")

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    sıralı = sorted(data.items(), key=lambda x: x[1]["jeton"], reverse=True)[:10]
    mesaj = "\n".join([f"{i+1}. {k} - {v['jeton']} jeton" for i, (k, v) in enumerate(sıralı)])
    await update.message.reply_text("En Zenginler:\n" + mesaj)

# BOTU BAŞLAT
app = ApplicationBuilder().token("7763395301:AAF3thVNH883Rzmz0RTpsx3wuiCG_VLpa-g").build()
komutlar = [
    ("start", start), ("bakiye", bakiye), ("bonus", bonus), ("faiz", faiz), ("görev", görev),
    ("slot", slot), ("hırsızlık", hırsızlık), ("bahis", bahis), ("çekiliş", çekiliş),
    ("kazıkazan", kazıkazan), ("gönder", gönder), ("id", id), ("yapımcı", yapımcı),
    ("para", para), ("admin", admin), ("top", top)
]
for ad, fonk in komutlar:
    app.add_handler(CommandHandler(ad, fonk))
app.run_polling()
