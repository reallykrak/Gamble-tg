import json
import random
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7763395301:AAF3thVNH883Rzmz0RTpsx3wuiCG_VLpa-g"
DATA_FILE = "data.json"
SABIT_ADMINLER = [8121637254, 987654321]
BAŞLANGIÇ_TL = 10000
BONUS_TL = 50000
BONUS_SÜRE = 86400  # 24 saat

# Ana menü (bol emojili)
main_menu = ReplyKeyboardMarkup([
    ["🚀start", "🎁bonus"],
    ["💰bakiye", "🎯kazikazan 100"],
    ["🎰slot 100", "⚠️risk 100"]
], resize_keyboard=True)

# Veri yönetimi
def veri_yükle():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def veri_kaydet(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def kullanıcı_kontrol(user_id):
    data = veri_yükle()
    if str(user_id) not in data:
        data[str(user_id)] = {
            "tl": 0,
            "last_bonus": "1970-01-01 00:00:00",
            "admin": False,
            "ilk_giris": True
        }
        veri_kaydet(data)

def admin_mi(user_id):
    data = veri_yükle()
    return user_id in SABIT_ADMINLER or data.get(str(user_id), {}).get("admin", False)

def tl_güncelle(user_id, miktar):
    data = veri_yükle()
    data[str(user_id)]["tl"] += miktar
    veri_kaydet(data)

# Komutlar
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    kullanıcı_kontrol(user_id)
    data = veri_yükle()
    user = data[str(user_id)]

    if user["ilk_giris"]:
        user["tl"] += BAŞLANGIÇ_TL
        user["ilk_giris"] = False
        msg = f"👋 Hoş geldin {update.effective_user.first_name}!\nHesabına başlangıç olarak 💸 {BAŞLANGIÇ_TL:,} TL yüklendi!"
    else:
        msg = f"👋 Tekrar hoş geldin {update.effective_user.first_name}!"
    
    veri_kaydet(data)
    await update.message.reply_text(msg, reply_markup=main_menu)

async def bakiye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    kullanıcı_kontrol(user_id)
    data = veri_yükle()
    await update.message.reply_text(f"💼 Bakiyen: {data[str(user_id)]['tl']:,} TL")

async def bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    kullanıcı_kontrol(user_id)
    data = veri_yükle()
    user = data[str(user_id)]
    son = datetime.strptime(user["last_bonus"], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()

    if now - son >= timedelta(seconds=BONUS_SÜRE):
        user["last_bonus"] = now.strftime("%Y-%m-%d %H:%M:%S")
        user["tl"] += BONUS_TL
        msg = f"🎁 Günlük bonus alındı! +{BONUS_TL:,} TL"
    else:
        kalan = timedelta(seconds=BONUS_SÜRE) - (now - son)
        msg = f"⏳ Bonus zaten alındı!\nYeniden almak için bekle: {str(kalan).split('.')[0]}"

    veri_kaydet(data)
    await update.message.reply_text(msg)

async def kazikazan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    kullanıcı_kontrol(user_id)

    try:
        miktar = int(context.args[0])
    except:
        return await update.message.reply_text("❗ Kullanım: /kazikazan [miktar]")

    data = veri_yükle()
    user = data[str(user_id)]

    if user["tl"] < miktar:
        return await update.message.reply_text("💀 Yetersiz bakiye!")

    user["tl"] -= miktar
    if random.randint(1, 100) <= 30:
        kazanç = miktar * 3
        user["tl"] += kazanç
        msg = f"🎯 Tebrikler! Kazı Kazan'dan {kazanç:,} TL kazandın!"
    else:
        msg = "💀 Üzgünüm, bu sefer olmadı..."
    
    veri_kaydet(data)
    await update.message.reply_text(msg)

async def risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    kullanıcı_kontrol(user_id)

    try:
        miktar = int(context.args[0])
    except:
        return await update.message.reply_text("❗ Kullanım: /risk [miktar]")

    data = veri_yükle()
    user = data[str(user_id)]

    if user["tl"] < miktar:
        return await update.message.reply_text("💀 Yetersiz bakiye!")

    user["tl"] -= miktar
    if random.randint(1, 100) <= 40:
        kazanç = miktar * 2
        user["tl"] += kazanç
        msg = f"⚡ Şanslısın! {kazanç:,} TL kazandın!"
    else:
        msg = "💣 Kaybettin..."

    veri_kaydet(data)
    await update.message.reply_text(msg)

async def slot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    kullanıcı_kontrol(user_id)

    try:
        miktar = int(context.args[0])
    except:
        return await update.message.reply_text("❗ Kullanım: /slot [miktar]")

    data = veri_yükle()
    user = data[str(user_id)]

    if user["tl"] < miktar:
        return await update.message.reply_text("💀 Yetersiz bakiye!")

    user["tl"] -= miktar

    semboller = ["🍇", "🍍", "🍒", "🏆", "🏆"]
    sonuç = [random.choice(semboller) for _ in range(3)]

    if sonuç[0] == sonuç[1] == sonuç[2]:
        kazanç = miktar * 4
        user["tl"] += kazanç
        durum = "🎉 JACKPOT!"
        detay = f"{kazanç:,} coin kazandın!"
    else:
        durum = "💀 Kaybettin..."
        detay = ""

    veri_kaydet(data)
    mesaj = f"{' | '.join(sonuç)}\n\n{durum} {detay}"
    await update.message.reply_text(mesaj)

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not admin_mi(user_id):
        return await update.message.reply_text("🚫 Yetkisiz erişim.")

    try:
        hedef_id = int(context.args[0])
    except:
        return await update.message.reply_text("Kullanım: /admin [id]")

    data = veri_yükle()
    kullanıcı_kontrol(hedef_id)
    data[str(hedef_id)]["admin"] = True
    veri_kaydet(data)
    await update.message.reply_text(f"✅ {hedef_id} artık admin!")

async def parabasma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not admin_mi(user_id):
        return await update.message.reply_text("🚫 Sadece adminler para basabilir!")

    try:
        hedef_id = int(context.args[0])
        miktar = int(context.args[1])
    except:
        return await update.message.reply_text("Kullanım: /parabasma [id] [miktar]")

    kullanıcı_kontrol(hedef_id)
    tl_güncelle(hedef_id, miktar)
    await update.message.reply_text(f"💸 {hedef_id} kişisine {miktar:,} TL basıldı!")

async def paragönder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    try:
        hedef_id = int(context.args[0])
        miktar = int(context.args[1])
    except:
        return await update.message.reply_text("Kullanım: /paragönder [id] [miktar]")

    data = veri_yükle()
    kullanıcı_kontrol(hedef_id)

    if data[str(user_id)]["tl"] < miktar:
        return await update.message.reply_text("💀 Yetersiz bakiye!")

    data[str(user_id)]["tl"] -= miktar
    data[str(hedef_id)]["tl"] += miktar
    veri_kaydet(data)
    await update.message.reply_text(f"📤 {miktar:,} TL gönderildi!")

async def id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("Lütfen bir mesaja yanıt ver.")
    hedef = update.message.reply_to_message.from_user
    kullanıcı_kontrol(hedef.id)
    data = veri_yükle()
    await update.message.reply_text(f"👤 {hedef.first_name} bakiyesi: {data[str(hedef.id)]['tl']:,} coin")

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = veri_yükle()
    sıralama = sorted(data.items(), key=lambda x: x[1]["tl"], reverse=True)[:10]
    metin = "\n".join([f"{i+1}. 🪪 {uid} - 💰 {veri['tl']:,} coin" for i, (uid, veri) in enumerate(sıralama)])
    await update.message.reply_text(f"🏆 En Zenginler:\n\n{metin}")

# Bot başlatma
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
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

    print("Bot çalışıyor...")
    app.run_polling()
