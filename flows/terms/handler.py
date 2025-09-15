import messages.term
async def handler(query):
    text , reply_markup = messages.term.term_message()
    await query.edit_message_text(text = text, reply_markup = reply_markup)