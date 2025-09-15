
import messages.problemInBot

async def handler(query):
    await query.message.reply_text(messages.problemInBot.problem_in_bot_message())