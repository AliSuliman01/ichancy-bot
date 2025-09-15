
import messages.problemInBot

async def handler(query):
    text , reply_markup = messages.problemInBot.problem_in_bot_message()
    await query.message.reply_text(text , reply_markup = reply_markup)