
import messages.problemInWebsite

async def handler(query):
    text , reply_markup  = messages.problemInWebsite.problem_in_website_message()
    await query.message.reply_text(text , reply_markup = reply_markup)