
import messages.problemInWebsite

async def handler(query):
    await query.message.reply_text(messages.problemInWebsite.problem_in_website_message())