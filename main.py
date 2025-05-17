import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
import config
from commands import start, katildim_callback, yardim, bonus, bakiye, istatistikler, top, user_id, gonder
from bank import bankayaekle, bankadanal, banka, doviz
from games import slot, zar, yazitura, hayvan, renk, hedef, hedef_callback
from admin import admin_panel, coinver, coinals, ban, unban, kullanici
from betting import bahis, bahis_callback

# Log yapılandırması 😊
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# ✅ Yeni sürüm ile ApplicationBuilder kullanılıyor!
app = ApplicationBuilder().token(config.TOKEN).build()

# Genel komutlar
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(katildim_callback, pattern="katildim"))
app.add_handler(CommandHandler("yardım", yardim))
app.add_handler(CommandHandler("bonus", bonus))
app.add_handler(CommandHandler("bakiye", bakiye))
app.add_handler(CommandHandler("istatistikler", istatistikler))
app.add_handler(CommandHandler("top", top))
app.add_handler(CommandHandler("id", user_id))
app.add_handler(CommandHandler("gönder", gonder))

# Banka / Döviz komutları
app.add_handler(CommandHandler("bankayaekle", bankayaekle))
app.add_handler(CommandHandler("bankadanal", bankadanal))
app.add_handler(CommandHandler("banka", banka))
app.add_handler(CommandHandler("döviz", doviz))

# Oyun komutları
app.add_handler(CommandHandler("slot", slot))
app.add_handler(CommandHandler("zar", zar))
app.add_handler(CommandHandler("yazitura", yazitura))
app.add_handler(CommandHandler("hayvan", hayvan))
app.add_handler(CommandHandler("renk", renk))
app.add_handler(CommandHandler("hedef", hedef))
app.add_handler(CallbackQueryHandler(hedef_callback, pattern="hedef_"))

# Futbol bahis komutu
app.add_handler(CommandHandler("bahis", bahis))
app.add_handler(CallbackQueryHandler(bahis_callback, pattern="^bahis_"))

# Admin komutları
app.add_handler(CommandHandler("admin", admin_panel))
app.add_handler(CommandHandler("coinver", coinver))
app.add_handler(CommandHandler("coinals", coinals))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("unban", unban))
app.add_handler(CommandHandler("kullanici", kullanici))

# ✅ Yeni başlatma yöntemi!
app.run_polling()
