
import messages.contactUs


async def handler(query):
    text , reply_markup = messages.contactUs.contact_us_message()
    await query.edit_message_text(text , reply_markup = reply_markup )