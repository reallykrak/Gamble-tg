# commands.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from utils import load_data, save_data, register_user

# /start: Botu başlatır, kullanıcı kayıt edilir ve katılım mesajı gönderilir
def start(update, context):
    user_id = update.message.chat_id
    register_user(user_id)

    # Inline katılım butonu
    keyboard = [[InlineKeyboardButton("🟢 Katıldım", callback_data="katildim")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    mesaj = """⛔ **Bu Botu Kullanabilmek İçin Aşağıdaki Kanala Katılmanız GereKIyor**

🔗 [Kanalımıza Katıl]("https://t.me/addlist/h49pICAbWT81OGI0")

✅ Katıldıktan Sonra '🟢 Katıldım' Butonuna Tıklayın!"""
    update.message.reply_text(mesaj, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

# Katılım onayına ait callback; inline butona basıldığında çağrılır
def katildim_callback(update, context):
    query = update.callback_query
    user_id = query.message.chat_id
    data = load_data()
    if str(user_id) in data["users"]:
        data["users"][str(user_id)]["joined"] = True
        save_data(data)
    query.answer()
    query.edit_message_text("✅ Katılım Onaylandı! Artık komutları kullanabilirsin. /yardım komutunu deneyebilirsin.")

# /yardım: Komut listesini gösterir
def yardim(update, context):
    mesaj = """🤖 **Komut Listesi**

💥 Genel Komutlar:
• /start – Botu başlatır, kanal kontrolü yapar
• /yardım – Komutları gösterir
• /bonus – Günlük bonus verir
• /bakiye – Coin ve döviz bakiyenizi gösterir
• /istatistikler – Kişisel oyun istatistiklerini gösterir
• /top – En zengin kullanıcıları listeler
• /id – Kullanıcı ID ve bilgilerini gösterir
• /gönder – Coin transferi

🎰 Oyun Komutları:
• /slot – Slot makinesi oynar
• /bahis – Futbol bahis oyunu
• /zar – Zar tahmini (1-6)
• /yazitura – Yazı tura oyunu
• /hayvan – Hayvan tahmini
• /renk – Renk tepkisi oyunu
• /hedef – Hedef vuruşu

🏦 Banka/Döviz Komutları:
• /bankayaekle – Bankaya coin yatırır
• /bankadanal – Bankadan coin çeker
• /banka – Banka bakiyenizi gösterir
• /döviz – Döviz fiyatlarını gösterir

👑 Yönetici Komutları:
• /admin – Admin paneli
• /coinver – Kullanıcıya coin ekle
• /coinals – Kullanıcıdan coin sil
• /ban – Kullanıcıyı engelle
• /unban – Engeli kaldır
• /kullanici – Kullanıcı bilgilerini görüntüler

🎲 İyi eğlenceler!"""
    update.message.reply_text(mesaj, parse_mode=ParseMode.MARKDOWN)

# /bonus: Günlük bonus verir (basit örnek, zaman kontrolü eklenebilir)
def bonus(update, context):
    user_id = update.message.chat_id
    data = load_data()
    if str(user_id) in data["users"]:
        bonus_amount = 500  # Bonus miktarı
        data["users"][str(user_id)]["coin"] += bonus_amount
        save_data(data)
        update.message.reply_text(f"🎉 Günlük bonus: {bonus_amount} coin hesabınıza eklendi!")
    else:
        update.message.reply_text("Kayıt bulunamadı. Lütfen /start komutunu kullanın.")

# /bakiye: Mevcut coin bakiyesini gösterir
def bakiye(update, context):
    user_id = update.message.chat_id
    data = load_data()
    if str(user_id) in data["users"]:
        coin = data["users"][str(user_id)]["coin"]
        update.message.reply_text(f"💰 Mevcut bakiyeniz: {coin} coin")
    else:
        update.message.reply_text("Kullanıcı bulunamadı. Lütfen /start komutunu kullanın.")

# /istatistikler: Oyun istatistiklerini gösterir
def istatistikler(update, context):
    user_id = update.message.chat_id
    data = load_data()
    if str(user_id) in data["users"]:
        stats = data["users"][str(user_id)].get("stats", {"wins": 0, "losses": 0})
        update.message.reply_text(f"📊 İstatistikleriniz:\n🏆 Kazanma: {stats.get('wins', 0)}\n❌ Kaybetme: {stats.get('losses', 0)}")
    else:
        update.message.reply_text("Kayıt bulunamadı. Lütfen /start komutunu kullanın.")

# /top: En zengin kullanıcıları listeler
def top(update, context):
    data = load_data()
    users = data.get("users", {})
    sorted_users = sorted(users.items(), key=lambda x: x[1].get("coin", 0), reverse=True)
    mesaj = "🏅 En Zengin Kullanıcılar:\n"
    for i, (user_id, info) in enumerate(sorted_users[:10], 1):
        mesaj += f"{i}. Kullanıcı {user_id}: {info.get('coin', 0)} coin\n"
    update.message.reply_text(mesaj)

# /id: Kullanıcı ID bilgisini gösterir
def user_id(update, context):
    if context.args:
        update.message.reply_text(f"Kullanıcı bilgisi: {' '.join(context.args)}")
    else:
        update.message.reply_text(f"🔍 Sizin ID'niz: {update.message.chat_id}")

# /gönder: Coin transferi yapar (hem gönderici hem alıcı verisi data.json üzerinden işlenir)
def gonder(update, context):
    data = load_data()
    message = update.message.text.split()
    if len(message) < 3:
        update.message.reply_text("⚠️ Kullanım: /gönder @kullanici miktar")
        return

    target = message[1]
    try:
        amount = int(message[2])
    except ValueError:
        update.message.reply_text("⚠️ Lütfen geçerli bir miktar giriniz!")
        return

    sender_id = str(update.message.chat_id)
    if sender_id not in data["users"]:
        update.message.reply_text("Kayıt bulunamadı. Lütfen /start komutunu kullanın.")
        return

    if data["users"][sender_id]["coin"] < amount:
        update.message.reply_text("⚠️ Yeterli coin bakiyeniz yok!")
        return

    # Bu örnekte, alıcı kullanıcı ID’sini direkt string olarak kullanıyoruz.
    receiver_id = target.strip("@")
    if receiver_id not in data["users"]:
        # Alıcı kayıtlı değilse otomatik kayıt ekleniyor.
        data["users"][receiver_id] = {"coin": 1000, "bank": 0, "joined": False, "stats": {"wins": 0, "losses": 0}}

    data["users"][sender_id]["coin"] -= amount
    data["users"][receiver_id]["coin"] += amount
    save_data(data)
    update.message.reply_text(f"✅ {amount} coin {target}'a gönderildi!")
