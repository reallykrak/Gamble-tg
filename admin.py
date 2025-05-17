# admin.py
from utils import load_data, save_data
import config

# /admin: Admin panelini gösterir
def admin_panel(update, context):
    user_id = update.message.chat_id
    if user_id not in config.ADMIN_IDS:
        update.message.reply_text("⛔ Admin değilsiniz!")
        return
    update.message.reply_text("👑 Admin Paneline Hoş Geldiniz!\nKullanılabilir admin komutları: /coinver, /coinals, /ban, /unban, /kullanici")

# /coinver: Belirtilen kullanıcıya coin ekler
def coinver(update, context):
    user_id = update.message.chat_id
    if user_id not in config.ADMIN_IDS:
        update.message.reply_text("⛔ Admin değilsiniz!")
        return

    args = context.args
    if len(args) < 2:
        update.message.reply_text("⚠️ Kullanım: /coinver @kullanici miktar")
        return

    target = args[0].strip("@")
    try:
        amount = int(args[1])
    except ValueError:
        update.message.reply_text("⚠️ Lütfen geçerli bir miktar giriniz!")
        return

    data = load_data()
    if target not in data["users"]:
        update.message.reply_text("⚠️ Hedef kullanıcı bulunamadı!")
        return

    data["users"][target]["coin"] += amount
    save_data(data)
    update.message.reply_text(f"✅ {target} kullanıcısına {amount} coin eklendi!")

# /coinals: Belirtilen kullanıcıdan coin çeker
def coinals(update, context):
    user_id = update.message.chat_id
    if user_id not in config.ADMIN_IDS:
        update.message.reply_text("⛔ Admin değilsiniz!")
        return

    args = context.args
    if len(args) < 2:
        update.message.reply_text("⚠️ Kullanım: /coinals @kullanici miktar")
        return

    target = args[0].strip("@")
    try:
        amount = int(args[1])
    except ValueError:
        update.message.reply_text("⚠️ Lütfen geçerli bir miktar giriniz!")
        return

    data = load_data()
    if target not in data["users"]:
        update.message.reply_text("⚠️ Hedef kullanıcı bulunamadı!")
        return

    data["users"][target]["coin"] -= amount
    save_data(data)
    update.message.reply_text(f"🚫 {target} kullanıcısından {amount} coin silindi!")

# /ban: Kullanıcıyı yasaklar
def ban(update, context):
    user_id = update.message.chat_id
    if user_id not in config.ADMIN_IDS:
        update.message.reply_text("⛔ Admin değilsiniz!")
        return

    args = context.args
    if not args:
        update.message.reply_text("⚠️ Kullanım: /ban @kullanici")
        return

    target = args[0].strip("@")
    data = load_data()
    if target not in data["users"]:
        update.message.reply_text("⚠️ Hedef kullanıcı bulunamadı!")
        return

    data["users"][target]["banned"] = True
    save_data(data)
    update.message.reply_text(f"🚫 {target} kullanıcısı yasaklandı!")

# /unban: Kullanıcının yasağını kaldırır
def unban(update, context):
    user_id = update.message.chat_id
    if user_id not in config.ADMIN_IDS:
        update.message.reply_text("⛔ Admin değilsiniz!")
        return

    args = context.args
    if not args:
        update.message.reply_text("⚠️ Kullanım: /unban @kullanici")
        return

    target = args[0].strip("@")
    data = load_data()
    if target not in data["users"]:
        update.message.reply_text("⚠️ Hedef kullanıcı bulunamadı!")
        return

    data["users"][target]["banned"] = False
    save_data(data)
    update.message.reply_text(f"✅ {target} kullanıcısının yasağı kaldırıldı!")

# /kullanici: Kullanıcı bilgilerini görüntüler
def kullanici(update, context):
    user_id = update.message.chat_id

    args = context.args
    if not args:
        update.message.reply_text("⚠️ Kullanım: /kullanici @kullanici")
        return

    target = args[0].strip("@")
    data = load_data()
    if target not in data["users"]:
        update.message.reply_text("⚠️ Hedef kullanıcı bulunamadı!")
        return

    user_info = data["users"][target]
    mesaj = f"🔍 **{target} Kullanıcı Bilgileri**\n\n💰 Coin: {user_info['coin']}\n🏦 Banka: {user_info.get('bank', 0)}\n🚫 Yasaklı mı?: {'Evet' if user_info.get('banned', False) else 'Hayır'}"
    update.message.reply_text(mesaj)
