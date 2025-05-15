const { Telegraf, Markup } = require("telegraf");

const bot = new Telegraf("7763395301:AAF3thVNH883Rzmz0RTpsx3wuiCG_VLpa-g");

// Veriler bellekte tutuluyor, restartta sıfırlanır!
const users = {};
const admins = new Set();

// Başlangıç admini buraya koy:
// Botu kullanan ilk kişi veya kendi ID'niz
admins.add(8121637254); // <-- kendi Telegram ID'nizi buraya yazın

// Yardımcı fonksiyonlar
function ensureUser(id) {
  if (!users[id]) {
    users[id] = {
      balance: 0,
      bank: 0,
      lastBonus: 0,
    };
  }
}

function formatMoney(num) {
  return num.toLocaleString() + "₺";
}

function formatBalance(user) {
  return `💰 Cüzdan: ${formatMoney(user.balance)}\n🏦 Banka: ${formatMoney(user.bank)}`;
}

function isAdmin(id) {
  return admins.has(id);
}

function canTakeBonus(user) {
  return Date.now() - user.lastBonus > 24 * 60 * 60 * 1000;
}

// Ana menü butonları
function mainMenu() {
  return Markup.inlineKeyboard([
    [Markup.button.callback("💰 Bakiye", "bakiye"), Markup.button.callback("🎁 Bonus Al", "bonus")],
    [Markup.button.callback("🎟️ Kazı Kazan", "kazi"), Markup.button.callback("🏦 Faiz Al", "faiz")],
    [Markup.button.callback("🕵️‍♂️ Hırsızlık", "hirsizlik"), Markup.button.callback("🎲 Bahis Oyna", "bahis")],
    [Markup.button.callback("🎰 Slot Oyna", "slot"), Markup.button.callback("💳 Banka İşlemleri", "banka")],
    [Markup.button.callback("🏆 Liderlik", "liderlik"), Markup.button.callback("🆔 ID Göster", "id")],
    [Markup.button.callback("💸 Para Gönder", "paragonder"), Markup.button.callback("🛠️ Admin Paneli", "adminpanel")]
  ]);
}

// Başlat
bot.start((ctx) => {
  const id = ctx.from.id;
  ensureUser(id);
  ctx.reply(
    `👋 Merhaba ${ctx.from.first_name}!\n\n` +
    "🎰 Kumar botuna hoşgeldin.\nAşağıdaki menüden işlemlerini seçebilirsin.",
    mainMenu()
  );
});

// Butonlar
bot.action("bakiye", (ctx) => {
  const id = ctx.from.id;
  ensureUser(id);
  ctx.answerCbQuery();
  ctx.editMessageText(`💰 Bakiyen:\n${formatBalance(users[id])}`, mainMenu());
});

bot.action("bonus", (ctx) => {
  const id = ctx.from.id;
  ensureUser(id);
  ctx.answerCbQuery();
  const user = users[id];
  if (canTakeBonus(user)) {
    user.balance += 50000;
    user.lastBonus = Date.now();
    ctx.editMessageText("🎉 50.000₺ bonus hesabına eklendi!", mainMenu());
  } else {
    const wait = 24 * 60 * 60 * 1000 - (Date.now() - user.lastBonus);
    const saat = Math.floor(wait / 3600000);
    const dakika = Math.floor((wait % 3600000) / 60000);
    ctx.editMessageText(`⏳ Bonus sadece 24 saatte bir alınabilir.\nLütfen ${saat} saat ${dakika} dakika bekle.`, mainMenu());
  }
});

bot.action("kazi", (ctx) => {
  const id = ctx.from.id;
  ensureUser(id);
  ctx.answerCbQuery();
  const user = users[id];

  if (user.balance < 1000) return ctx.answerCbQuery("❌ Kazı kazan için en az 1.000₺ bakiyen olmalı.", true);

  user.balance -= 1000;

  if (Math.random() < 0.3) {
    const kazanc = 3000 + Math.floor(Math.random() * 3000);
    user.balance += kazanc;
    ctx.editMessageText(`🎉 Kazı Kazan: Kazandın! +${formatMoney(kazanc)}`, mainMenu());
  } else {
    ctx.editMessageText("😞 Kazı Kazan: Kaybettin.", mainMenu());
  }
});

bot.action("faiz", (ctx) => {
  const id = ctx.from.id;
  ensureUser(id);
  ctx.answerCbQuery();
  const user = users[id];
  if (user.bank <= 0) return ctx.answerCbQuery("❌ Bankanda para yok.", true);

  const faizOrani = 0.02;
  const faiz = Math.floor(user.bank * faizOrani);
  user.bank += faiz;

  ctx.editMessageText(`🏦 Banka faizinden %2 kazandın: +${formatMoney(faiz)}`, mainMenu());
});

bot.action("hirsizlik", (ctx) => {
  const id = ctx.from.id;
  ensureUser(id);
  ctx.answerCbQuery();

  ctx.reply("🔍 Para çalmak istediğin kişinin Telegram ID'sini yaz. İptal için /iptal");

  bot.once("text", (ctx2) => {
    const hedefId = Number(ctx2.message.text);
    if (!hedefId || hedefId === id) return ctx2.reply("❌ Geçersiz kullanıcı ID.");
    ensureUser(hedefId);

    const hedef = users[hedefId];
    const user = users[id];

    if (hedef.balance < 1000) return ctx2.reply("❌ Hedef kişinin yeterli parası yok.");

    const cekilen = Math.min(5000, Math.floor(hedef.balance * 0.3));

    if (Math.random() < 0.5) {
      hedef.balance -= cekilen;
      user.balance += cekilen;
      ctx2.reply(`🎉 Başarılı hırsızlık! ${formatMoney(cekilen)} çaldın.`);
    } else {
      ctx2.reply("❌ Hırsızlık başarısız oldu, dikkatli ol!");
    }
  });
});

bot.action("bahis", (ctx) => {
  const id = ctx.from.id;
  ensureUser(id);
  ctx.answerCbQuery();

  ctx.reply("🎲 Bahis için miktar yaz:");

  bot.once("text", (ctx2) => {
    const miktar = Number(ctx2.message.text);
    if (!miktar || miktar <= 0) return ctx2.reply("❌ Geçersiz miktar.");
    const user = users[id];
    if (user.balance < miktar) return ctx2.reply("❌ Yeterli bakiyen yok.");

    user.balance -= miktar;

    if (Math.random() < 0.5) {
      const kazanclik = miktar * 2;
      user.balance += kazanclik;
      ctx2.reply(`🎉 Bahisi kazandın! +${formatMoney(kazanclik)}`);
    } else {
      ctx2.reply("😞 Bahisi kaybettin.");
    }
  });
});

bot.action("slot", (ctx) => {
  const id = ctx.from.id;
  ensureUser(id);
  ctx.answerCbQuery();

  const user = users[id];
  if (user.balance < 1000) return ctx.answerCbQuery("❌ Slot oynamak için en az 1.000₺ olmalı.", true);

  user.balance -= 1000;

  const semboller = ["🍒", "🍋", "🍉", "🔔", "⭐"];
  const secilen = [];
  for (let i = 0; i < 3; i++) {
    secilen.push(semboller[Math.floor(Math.random() * semboller.length)]);
  }

  let mesaj = `🎰 Slot sonuçları:\n${secilen.join(" | ")}\n`;

  if (secilen[0] === secilen[1] && secilen[1] === secilen[2]) {
    const kazanc = 10000;
    user.balance += kazanc;
    mesaj += `🎉 Tebrikler! Jackpot! +${formatMoney(kazanc)}`;
  } else if (secilen[0] === secilen[1] || secilen[1] === secilen[2] ||
