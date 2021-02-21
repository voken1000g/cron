const fetch = require('node-fetch')
const Telegram = require('node-telegram-bot-api')

const bot = new Telegram(process.env.TG_DEV_BOT_TOKEN)

const getIpData = async () => {
  const resp = await fetch('https://api.myip.com/')
  return await resp.json()
}

const main = async () => {
  const ipData = await getIpData()

  const message = '*GitHub Actions - debug.js*\n\n`From: ' + ipData.ip + ' (' + ipData.country + ')`'

  await bot.sendMessage(process.env.TG_DEV_CHAT_ID, message, {parse_mode : "MARKDOWN"})
}

main()
