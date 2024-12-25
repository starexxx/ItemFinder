import json
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, InputMediaPhoto, InputMedia
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, filters, ContextTypes
from uuid import uuid4

BOT_TOKEN = 'BOT_TOKEN'
JSON_URL = 'https://raw.githubusercontent.com/starexxx/ItemID/refs/heads/main/itemData.json'
ICON_URL_BASE = 'https://raw.githubusercontent.com/jinix6/ff-resources/main/pngs/300x300/'

data = []
previous_message_id_user = None
previous_message_id_bot = None

def fetch_data():
    global data
    response = requests.get(JSON_URL)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Failed to fetch data, status code {response.status_code}")

def escape_markdown(text):
    escape_chars = r"\_*[]()~`>#+-=|{}.!"
    return "".join(f"\\{char}" if char in escape_chars else char for char in text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Starexx! Send any message"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global previous_message_id_user, previous_message_id_bot  # Access the global previous message IDs

    # Delete previous user message if it exists
    if previous_message_id_user:
        try:
            await update.message.chat.delete_message(previous_message_id_user)
        except:
            pass

    # Delete previous bot message if it exists
    if previous_message_id_bot:
        try:
            await update.message.chat.delete_message(previous_message_id_bot)
        except:
            pass

    # Send the new message and store the message ID
    message_text = update.message.text
    escaped_text = escape_markdown(message_text)

    if message_text.isdigit():  # Check if the message is a number
        result_item = next((item for item in data if item['itemID'] == message_text), None)
        result = result_item
    else:
        result_name = next((item for item in data if item['description'].lower() == message_text.lower()), None)
        result = result_name

    if result:
        # Generate the icon image URL
        icon_url = f"{ICON_URL_BASE}{result['icon']}.png"

        # Send preview button with "Show Preview"
        response = (
            f"*Name* `{escape_markdown(result['description'])}`\n"
            f"*Item ID* `{escape_markdown(result['itemID'])}`\n"
            f"*Icon Name* `{escape_markdown(result['icon'])}`"
        )

        new_message = await update.message.reply_text(
            response,
            parse_mode='MarkdownV2',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Show Preview", callback_data=f"show_preview:{result['itemID']}:{result['icon']}")]
            ])
        )
        
        previous_message_id_user = update.message.message_id
        previous_message_id_bot = new_message.message_id
    else:
        await update.message.reply_text(f"Item not found!")

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    query_data = query.data.split(':')
    action = query_data[0]
    item_id = query_data[1]
    icon_name = query_data[2]

    if action == 'show_preview':
        result = next((item for item in data if item['itemID'] == item_id), None)
        if result:
            icon_url = f"{ICON_URL_BASE}{icon_name}.png"
            response = requests.get(icon_url)
            if response.status_code == 200:
                media = InputMediaPhoto(icon_url, caption=f"*Name* `{escape_markdown(result['description'])}`\n*Item ID* `{escape_markdown(result['itemID'])}`\n*Icon Name* `{escape_markdown(result['icon'])}`", parse_mode="MarkdownV2")
            else:
                media = InputMedia(media_type="photo", media="https://via.placeholder.com/2048?text=STAREXX", caption=f"*Name* `{escape_markdown(result['description'])}`\n*Item ID* `{escape_markdown(result['itemID'])}`\n*Icon Name* `{escape_markdown(result['icon'])}`", parse_mode="MarkdownV2")

            await query.edit_message_media(media=media)
            # Remove the "Show Preview" button after showing the image
            await query.edit_message_reply_markup(reply_markup=None)
        else:
            await query.edit_message_text("Item not found.")
    else:
        await query.edit_message_text("Invalid action.")

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return

    results = []

    if query.isdigit():
        result_item = next((item for item in data if item['itemID'] == query), None)
        if result_item:
            results.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=f"Finding {result_item['itemID']}s",
                    input_message_content=InputTextMessageContent(
                        message_text=f"*Name* `{escape_markdown(result_item['description'])}`\n"
                                     f"*Item ID* `{escape_markdown(result_item['itemID'])}`\n"
                                     f"*Icon Name* `{escape_markdown(result_item['icon'])}`",
                        parse_mode='MarkdownV2'
                    ),
                    description=f"This bot created by Starexx"
                )
            )
    else:
        result_name = next((item for item in data if item['description'].lower() == query.lower()), None)
        if result_name:
            results.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=f"Finding {result_name['description']}!",
                    input_message_content=InputTextMessageContent(
                        message_text=f"*Name* `{escape_markdown(result_name['description'])}`\n"
                                     f"*Item ID* `{escape_markdown(result_name['itemID'])}`\n"
                                     f"*Icon Name* `{escape_markdown(result_name['icon'])}`",
                        parse_mode='MarkdownV2'
                    ),
                    description=f"This bot created by Starexx"
                )
            )

    await update.inline_query.answer(results)

def main():
    fetch_data()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(InlineQueryHandler(inline_query))

    app.run_polling()

if __name__ == '__main__':
    main()