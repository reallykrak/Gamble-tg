# games.py
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

# /slot: Rastgele slot sonucu üretir.
def slot(update, context):
    symbols = ["🍒", "🍋", "🍊", "🍉", "⭐"]
    result = random.choices(symbols, k=3)
    update.message.reply_text(f"🎰 Slot Sonucu: {' '.join(result)}")

# /zar: Kullanıcının tahminini alır, 1-6 arasında rastgele zar atar.
def zar(update, context):
    args = context.args
    if not args:
        update.message.reply_text("⚠️ Kullanım: /zar sayı (1-6)")
        return
    try:
        tahmin = int(args[0])
    except ValueError:
        update.message.reply_text("⚠️ Lütfen 1 ile 6 arasında bir sayı girin!")
        return
    if tahmin < 1 or tahmin > 6:
        update.message.reply_text("⚠️ Lütfen 1 ile 6 arasında bir sayı seçin!")
        return
    sonuc = random.randint(1,6)
    if tahmin == sonuc:
        update.message.reply_text(f"🎲 Tebrikler! Zar: {sonuc} - Doğru tahmin! 🎉")
    else:
        update.message.reply_text(f"🎲 Maalesef yanlış! Zar: {sonuc} - Tekrar deneyin.")

# /yazitura: Yazı-tura oyunu, kullanıcının seçimine göre sonucu belirler.
def yazitura(update, context):
    args = context.args
    if len(args) < 2:
        update.message.reply_text("⚠️ Kullanım: /yazitura yazı/tura miktar")
        return
    secim = args[0].lower()
    try:
        miktar = int(args[1])
    except ValueError:
        update.message.reply_text("⚠️ Lütfen geçerli bir miktar girin!")
        return
    if secim not in ["yazı", "tura"]:
        update.message.reply_text("⚠️ Lütfen 'yazı' veya 'tura' seçin!")
        return
    sonuc = random.choice(["yazı", "tura"])
    if secim == sonuc:
        update.message.reply_text(f"✅ {sonuc.capitalize()} çıktı! {miktar} coin kazandınız!")
    else:
        update.message.reply_text(f"❌ {sonuc.capitalize()} çıktı! {miktar} coin kaybettiniz.")

# /hayvan: Hayvan tahmin oyunu; kullanıcının seçtiğiyle rastgele çıkan hayvan karşılaştırılır.
def hayvan(update, context):
    args = context.args
    if not args:
        update.message.reply_text("⚠️ Lütfen bir hayvan seçin (örneğin: fil, kaplan)")
        return
    tahmin = args[0].lower()
    animals = ["fil", "kaplan", "aslan", "kedi", "köpek", "kuş"]
    sonuc = random.choice(animals)
    if tahmin == sonuc:
        update.message.reply_text(f"🐾 Tebrikler, doğru tahmin! Seçilen: {sonuc}")
    else:
        update.message.reply_text(f"🐾 Yanlış tahmin! Gerçek hayvan: {sonuc}")

# /renk: Renk tahmin oyunu; verilen tahmin ile rastgele çıkan renk karşılaştırılır.
def renk(update, context):
    args = context.args
    if not args:
        update.message.reply_text("⚠️ Lütfen bir renk seçin (örneğin: kırmızı, mavi)")
        return
    tahmin = args[0].lower()
    colors = ["kırmızı", "mavi", "yeşil", "sarı"]
    sonuc = random.choice(colors)
    if tahmin == sonuc:
        update.message.reply_text(f"✅ Doğru! Çıkan renk: {sonuc}")
    else:
        update.message.reply_text(f"❌ Yanlış! Çıkan renk: {sonuc}")

# /hedef: Hedef vuruşu oyunu; 3 seçenekli inline butonlarla oynanır.
def hedef(update, context):
    keyboard = [
        [InlineKeyboardButton("🎯 Hedef 1", callback_data="hedef_1")],
        [InlineKeyboardButton("🎯 Hedef 2", callback_data="hedef_2")],
        [InlineKeyboardButton("🎯 Hedef 3", callback_data="hedef_3")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("🎯 Hedef vuruşu yapmak için 3 hedeften birini seçin:", reply_markup=reply_markup)

# Hedef seçimine ait callback fonksiyonu
def hedef_callback(update, context):
    query = update.callback_query
    target = query.data  # örneğin: "hedef_1"
    sonuc = "🔥 Vuruldunuz! Tebrikler!" if random.choice([True, False]) else "💥 Iskaladınız! Şansınızı tekrar deneyin."
    query.answer()
    query.edit_message_text(f"{target.replace('hedef_', 'Hedef ')} seçildi. {sonuc}")
