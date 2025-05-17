# bank.py
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from utils import load_data, save_data

# /bankayaekle: Kullanıcının cüzdanından bankaya coin aktarır.
def bankayaekle(update, context):
    user_id = update.message.chat_id
    args = context.args
    if not args:
        update.message.reply_text("⚠️ Kullanım: /bankayaekle miktar")
        return
    try:
        miktar = int(args[0])
    except ValueError:
        update.message.reply_text("⚠️ Lütfen geçerli bir miktar giriniz!")
        return
    data = load_data()
    if str(user_id) not in data["users"]:
        update.message.reply_text("Kullanıcı bulunamadı. Önce /start kullanın!")
        return
    if data["users"][str(user_id)]["coin"] < miktar:
        update.message.reply_text("⚠️ Yeterli coin bakiyeniz yok!")
        return
    data["users"][str(user_id)]["coin"] -= miktar
    data["users"][str(user_id)]["bank"] = data["users"][str(user_id)].get("bank", 0) + miktar
    save_data(data)
    update.message.reply_text(f"🏦 {miktar} coin bankaya eklendi!")

# /bankadanal: Bankadaki coinleri cüzdana aktarır.
def bankadanal(update, context):
    user_id = update.message.chat_id
    args = context.args
    if not args:
        update.message.reply_text("⚠️ Kullanım: /bankadanal miktar")
        return
    try:
        miktar = int(args[0])
    except ValueError:
        update.message.reply_text("⚠️ Lütfen geçerli bir miktar giriniz!")
        return
    data = load_data()
    if str(user_id) not in data["users"]:
        update.message.reply_text("Kullanıcı bulunamadı. Önce /start kullanın!")
        return
    if data["users"][str(user_id)].get("bank", 0) < miktar:
        update.message.reply_text("⚠️ Yeterli banka bakiyeniz yok!")
        return
    data["users"][str(user_id)]["bank"] -= miktar
    data["users"][str(user_id)]["coin"] += miktar
    save_data(data)
    update.message.reply_text(f"🏦 {miktar} coin bankadan çekildi!")

# /banka: Cüzdan ve banka bakiyelerini gösterir.
def banka(update, context):
    user_id = update.message.chat_id
    data = load_data()
    if str(user_id) not in data["users"]:
        update.message.reply_text("Kullanıcı bulunamadı. Önce /start kullanın!")
        return
    coin = data["users"][str(user_id)]["coin"]
    bank = data["users"][str(user_id)].get("bank", 0)
    update.message.reply_text(f"💰 Cüzdan: {coin} coin\n🏦 Banka: {bank} coin", parse_mode=ParseMode.MARKDOWN)

# /döviz: Döviz fiyatlarını basit örnek olarak gösterir, ayrıca inline satın alma butonu ekler.
def doviz(update, context):
    doviz_fiyatlari = {
        "USD": 1.0,
        "EUR": 0.93,
        "TRY": 18.0  # Dummy nilai
    }
    text = "💱 **Döviz Fiyatları:**\n"
    for currency, price in doviz_fiyatlari.items():
        text += f"- {currency}: {price}\n"
    
    keyboard = [[InlineKeyboardButton("Satın Al", callback_data="satinal_doviz")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
