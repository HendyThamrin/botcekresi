const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');

// Ganti dengan token bot kamu
const TELEGRAM_TOKEN = '7866835274:AAFHFO7pBZHRFlIA47cdsISvS8PhZA_JLqQ';
// Ganti dengan API key BinderByte kamu
const BINDERBYTE_KEY = '071ef170e025fe2ca816ed5aecb5413e2356fbb0c9f701a01a581870527581ec';

const bot = new TelegramBot(TELEGRAM_TOKEN, { polling: true });

bot.on('message', async (msg) => {
  const chatId = msg.chat.id;
  const awb = msg.text.trim();
  if (!awb) return;

  bot.sendMessage(chatId, `📡 Mengecek resi: ${awb}...`);

  try {
    const url = `https://api.binderbyte.com/v1/track?api_key=${BINDERBYTE_KEY}&courier=jnt&awb=${awb}`;
    const res = await axios.get(url);
    const data = res.data;

    if (data.status !== 200 || !data.data || !data.data.manifest?.length) {
      return bot.sendMessage(chatId, '❌ Resi belum tersedia atau salah nomor.');
    }

    const result = data.data;
    const receiverName = result.receiver_name || '-';
    const receiverAddress = result.receiver_address || '-';
    const latestManifest = result.manifest[result.manifest.length -1];
    const statusText = latestManifest.manifest_description || '-';
    const dateText = `${latestManifest.manifest_date || '-'} ${latestManifest.manifest_time || '-'}`;

    // COD otomatis Ya/Tidak dan tampil harga jika ada
    let codText = 'Tidak';
    if(result.cod_status && result.cod_amount){
        codText = `Ya (Rp ${result.cod_amount})`;
    } else if(result.cod_status){
        codText = 'Ya';
    }

    let reply = `📦 EKSPEDISI JNT\n└ J&T Express\n\n`;
    reply += `📩 Resi\n└ No Resi : ${awb}\n\n`;
    reply += `📮 Status\n├ ${statusText}\n└ ${dateText}\n\n`;
    reply += `🚩 Penerima\n├ ${receiverName}\n└ ${receiverAddress}\n\n`;
    reply += `💰 COD: ${codText}\n\n`;
    reply += `⏩ POD Detail\nsilahkan cek dengan kode berikut:\n!JNT ${awb}`;

    bot.sendMessage(chatId, reply);

  } catch (err) {
    bot.sendMessage(chatId, `❌ Terjadi error: ${err.message}`);
  }
});
