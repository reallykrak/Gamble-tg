# betting.py - Futbol Bahis Oyunu
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils import load_data, save_data

# Rastgele futbol maçları oluşturma
def generate_matches():
    takımlar = ["Barcelona", "Real Madrid", "Liverpool", "Manchester City", "Bayern Munich", "PSG", "Juventus", "Chelsea"]
    matches = []
    for _ in range(4):  # 4 farklı maç seçiyoruz
        ev_sahibi = random.choice(takımlar)
        misafir = random.choice(takımlar)
        while misafir == ev_sahibi:  # Aynı takımı iki kez seçmemek için
            misafir = random.choice(takımlar)
        matches.append(f"{ev_sahibi} vs {misafir}")
    return matches

# Bahis oyununu başlatan komut
def bahis(update, context):
    matches = generate_matches()

    keyboard = [[InlineKeyboardButton(match, callback_data=f"bahis_{i}")] for i, match in enumerate(matches)]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("⚽ Bahis zamanı! Aşağıdaki maçlardan birini seç:", reply_markup=reply_markup)

# Bahis callback fonksiyonu (seçilen bahsi işler)
def bahis_callback(update, context):
    query = update.callback_query
    match_id = query.data.replace("bahis_", "")

    # Kullanıcının seçtiği bahis sonucunu rastgele belirle
    kazandı_mı = random.choice([True, False])
    mesaj = "🔥 Tebrikler, bahsin kazandı!" if kazandı_mı else "💥 Maalesef, bahsin kaybetti!"

    query.answer()
    query.edit_message_text(mesaj)
