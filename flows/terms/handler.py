import messages.term
async def handler(query):
    await query.edit_message_text(messages.term.term_message())