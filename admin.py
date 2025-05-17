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
