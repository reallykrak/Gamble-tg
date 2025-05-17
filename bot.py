import json, os, time, random
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

DATA_FILE = "veri.json"
admins = [8121637254]  # Kendi Telegram ID'ni buraya ekle

# Veri işlemleri
def veri_yukle():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def veri_kaydet(veri):
    with open(DATA_FILE, "w") as f:
        json.dump(veri, f)

def para_al(uid):
    veri = veri_yukle()
    return veri.get(str(uid), {}).get("para", 0)

def para_ekle(uid, miktar):
    veri = veri_yukle()
    uid = str(uid)
    if uid not in veri:
        veri[uid] = {"para": 0}
    veri[uid]["para"] += miktar
    veri_kaydet(veri)

def admin_kontrol(uid):
    return uid in admins

# Komutlar
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    para_ekle(uid, 10000)
    butonlar = [
        [KeyboardButton("/bakiye"), KeyboardButton("/bonus")],
        [KeyboardButton("/kazikazan"), KeyboardButton("/risk")],
        [KeyboardButton("/slot")]
    ]
    await update.message.reply_text("Hoş geldin! 10.000 coin verildi.", reply_markup=ReplyKeyboardMarkup(butonlar, resize_keyboard=True))

async def bakiye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    await update.message.reply_text(f"Bakiye: {para_al(uid)} coin")

async def bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    veri = veri_yukle()
    user = veri.get(uid, {"para": 0})
    now = time.time()
    last = user.get("bonus", 0)
    if now - last >= 86400:
        user["bonus"] = now
        user["para"] += 50000
        veri[uid] = user
        veri_kaydet(veri)
        await update.message.reply_text("Tebrikler! 50.000 coin bonus aldın.")
    else:
        kalan = int(86400 - (now - last))
        saat = kalan // 3600
        dakika = (kalan % 3600) // 60
        await update.message.reply_text(f"Bonus için bekle: {saat} saat {dakika} dakika")

async def kazikazan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if para_al(uid) < 100:
        await update.message.reply_text("Yetersiz coin!")
        return
    para_ekle(uid, -100)
    if random.random() < 0.3:
        kazanc = 400
        para_ekle(uid, kazanc)
        await update.message.reply_text(f"Kazandın! +{kazanc} coin")
    else:
        await update.message.reply_text("Kaybettin!")

async def risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text("Kullanım: /risk <miktar>")
        return
    miktar = int(context.args[0])
    if para_al(uid) < miktar:
        await update.message.reply_text("Yetersiz coin!")
        return
    para_ekle(uid, -miktar)
    if random.random() < 0.4:
        kazanc = miktar * 2
        para_ekle(uid, kazanc)
        await update.message.reply_text(f"Şanslısın! +{kazanc} coin kazandın.")
    else:
        await update.message.reply_text("Kaybettin!")

async def slot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if para_al(uid) < 100:
        await update.message.reply_text("Yetersiz coin!")
        return
    para_ekle(uid, -100)
    if random.random() < 0.3:
        kazanc = 400
        para_ekle(uid, kazanc)
        await update.message.reply_text(f"Kazandın! +{kazanc} coin")
    else:
        await update.message.reply_text("Kaybettin!")

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not admin_kontrol(uid):
        await update.message.reply_text("Yetkin yok.")
        return
    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text("Kullanım: /admin <kullanıcı_id>")
        return
    yeni = int(context.args[0])
    admins.append(yeni)
    await update.message.reply_text(f"{yeni} artık admin!")

async def parabasma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not admin_kontrol(uid):
        await update.message.reply_text("Yetkin yok.")
        return
    if len(context.args) != 2 or not context.args[0].isdigit() or not context.args[1].isdigit():
        await update.message.reply_text("Kullanım: /parabasma <kullanıcı_id> <miktar>")
        return
    hedef = int(context.args[0])
    miktar = int(context.args[1])
    para_ekle(hedef, miktar)
    await update.message.reply_text(f"{hedef} ID'li kişiye {miktar} coin verildi.")

async def paragönder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if len(context.args) != 2 or not context.args[0].isdigit() or not context.args[1].isdigit():
        await update.message.reply_text("Kullanım: /paragönder <kullanıcı_id> <miktar>")
        return
    hedef = int(context.args[0])
    miktar = int(context.args[1])
    if para_al(uid) < miktar:
        await update.message.reply_text("Yetersiz coin!")
        return
    para_ekle(uid, -miktar)
    para_ekle(hedef, miktar)
    await update.message.reply_text(f"{miktar} coin gönderildi.")

async def id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hedef = update.message.reply_to_message.from_user if update.message.reply_to_message else update.effective_user
    uid = hedef.id
    await update.message.reply_text(f"Kullanıcı: {hedef.full_name}\nID: {uid}\nBakiye: {para_al(uid)} coin")

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    veri = veri_yukle()
    sıralama = sorted(veri.items(), key=lambda x: x[1].get("para", 0), reverse=True)[:10]
    mesaj = "En Zenginler:\n\n"
    for i, (uid, user) in enumerate(sıralama, 1):
        mesaj += f"{i}. {uid} - {user.get('para', 0)} coin\n"
    await update.message.reply_text(mesaj)

# Bot başlat
app = ApplicationBuilder().token("7763395301:AAF3thVNH883Rzmz0RTpsx3wuiCG_VLpa-g").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("bakiye", bakiye))
app.add_handler(CommandHandler("bonus", bonus))
app.add_handler(CommandHandler("kazikazan", kazikazan))
app.add_handler(CommandHandler("risk", risk))
app.add_handler(CommandHandler("slot", slot))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CommandHandler("parabasma", parabasma))
app.add_handler(CommandHandler("paragonder", paragönder))
app.add_handler(CommandHandler("id", id))
app.add_handler(CommandHandler("top", top))

app.run_polling()
