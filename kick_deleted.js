const fs = require('fs')
const Telegram = require('node-telegram-bot-api')
const bot = new Telegram(process.env.TG_CRON_BOT_TOKEN)

const sleep = (ms) => {
    return new Promise(resolve => setTimeout(resolve, ms))
}

const main = async () => {
    const strDeleted = fs.readFileSync('data/deleted.json', 'utf-8')
    const deleted = JSON.parse(strDeleted.toString())

    for (let i = 0; i < deleted.length; i++) {
        const chatId = deleted[i].id
        const userIds = deleted[i].user_ids
        console.log(chatId, userIds.length)

        if (userIds.length) {
            for (let j = 0; j < userIds.length; j++) {
                console.log('kick:', userIds[j])
                await bot.kickChatMember(chatId, userIds[j])
                await sleep(150)
            }

            const message = '*kick deleted accounts*\n\n' +
                '`' + userIds.length + ' invalid users (Deleted Account) REMOVED`'
            console.log(message)
            await bot.sendMessage(chatId, message, {parse_mode : "MARKDOWN"})
        }
    }
}

main()
