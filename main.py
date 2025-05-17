# main.py
import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import config
from commands import start, katildim_callback, yardim, bonus, bakiye, istatistikler, top, user_id, gonder
from bank import bankayaekle, bankadanal, banka, doviz
from games import slot, zar, yazitura, hayvan, renk, hedef, hedef_callback
from admin import admin_panel, coinver, coinals, ban, unban, kullanici
from betting import bahis, bahis_callback

# Log yapılandırması 😊
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

from telegram.ext import ApplicationBuilder

app = ApplicationBuilder().token(config.TOKEN).build()
dispatcher = updater.dispatcher

# Genel komutlar
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(katildim_callback, pattern="katildim"))
dispatcher.add_handler(CommandHandler("yardım", yardim))
dispatcher.add_handler(CommandHandler("bonus", bonus))
dispatcher.add_handler(CommandHandler("bakiye", bakiye))
dispatcher.add_handler(CommandHandler("istatistikler", istatistikler))
dispatcher.add_handler(CommandHandler("top", top))
dispatcher.add_handler(CommandHandler("id", user_id))
dispatcher.add_handler(CommandHandler("gönder", gonder))

# Banka / Döviz komutları
dispatcher.add_handler(CommandHandler("bankayaekle", bankayaekle))
dispatcher.add_handler(CommandHandler("bankadanal", bankadanal))
dispatcher.add_handler(CommandHandler("banka", banka))
dispatcher.add_handler(CommandHandler("döviz", doviz))

# Oyun komutları
dispatcher.add_handler(CommandHandler("slot", slot))
dispatcher.add_handler(CommandHandler("zar", zar))
dispatcher.add_handler(CommandHandler("yazitura", yazitura))
dispatcher.add_handler(CommandHandler("hayvan", hayvan))
dispatcher.add_handler(CommandHandler("renk", renk))
dispatcher.add_handler(CommandHandler("hedef", hedef))
dispatcher.add_handler(CallbackQueryHandler(hedef_callback, pattern="hedef_"))

# Futbol bahis komutu
dispatcher.add_handler(CommandHandler("bahis", bahis))
dispatcher.add_handler(CallbackQueryHandler(bahis_callback, pattern="^bahis_"))

# Admin komutları
dispatcher.add_handler(CommandHandler("admin", admin_panel))
dispatcher.add_handler(CommandHandler("coinver", coinver))
dispatcher.add_handler(CommandHandler("coinals", coinals))
dispatcher.add_handler(CommandHandler("ban", ban))
dispatcher.add_handler(CommandHandler("unban", unban))
dispatcher.add_handler(CommandHandler("kullanici", kullanici))

# Botu çalıştırıyoruz...
updater.start_polling()
updater.idle()
