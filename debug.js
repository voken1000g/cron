require('dotenv').config()
const fetch = require('node-fetch')
const Telegram = require('node-telegram-bot-api')

const TG_BOT_TOKEN = process.env.TG_BOT_TOKEN
const TG_CHAT_ID = process.env.TG_CHAT_ID
const bot = new Telegram(TG_BOT_TOKEN)

const getIpData = async () => {
  const resp = await fetch('https://api.myip.com/')
  return await resp.json()
}

const main = async () => {
  const ipData = await getIpData()

  const message = '*GitHub Actions*\n\n`From ' + ipData.ip + ' ' + ipData.country + '`'

  await bot.sendMessage(TG_CHAT_ID, message)
}

main()
