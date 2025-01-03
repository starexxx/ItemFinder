import os
import json
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, filters, ContextTypes
from uuid import uuid4
from typing import List, Optional

# Load the bot token from the environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
JSON_URL = 'https://raw.githubusercontent.com/starexxx/ItemID/refs/heads/main/itemData.json'
ICON_URL_BASE = 'https://raw.githubusercontent.com/starexxx/ff-resources/main/pngs/300x300/'

# Global variable to store the item data
data: List[dict] = []

def fetch_data() -> None:
    """Fetches the item data from the JSON URL and stores it in the global `data` list."""
    global data
    try:
        response = requests.get(JSON_URL)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

def escape_markdown(text: str) -> str:
    """Escapes special Markdown characters in the text."""
    escape_chars = r"\_*[]()~`>#+-=|{}.!"
    return "".join(f"\\{char}" if char in escape_chars else char for char in text)

def search_items(keyword: str) -> List[dict]:
    """Search for items that match the given keyword in description, itemID, or icon."""
    # Check if the keyword is numeric (itemID)
    if keyword.isdigit():
        return [item for item in data if item['itemID'] == keyword]
    else:
        # Search for items with matching description or icon
        return [item for item in data if keyword.lower() in item['description'].lower() or keyword.lower() in item.get('icon', '').lower()]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command and welcomes the user."""
    await update.message.reply_text(
        "Send any message to search for items."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles user messages, searches for items based on the input keyword, and sends the first matching result."""
    # Extract the search keyword from the user's message
    keyword = update.message.text.strip()
    escaped_text = escape_markdown(keyword)

    # Search for items matching the keyword
    results = search_items(keyword)

    if results:
        # Get the first matching result
        result = results[0]
        icon_url = f"{ICON_URL_BASE}{result['icon']}.png"
        
        # Safely access 'description2' using get()
        description2 = result.get('description2', 'No additional description available.')
        
        response_text = (
            f"*Name*: `{escape_markdown(result['description'])}`\n"
            f"*Item ID*: `{escape_markdown(result['itemID'])}`\n"
            f"*Description*: `{escape_markdown(description2)}`\n"
            f"*Icon Name*: `{escape_markdown(result['icon'])}`"
        )

        # Send the result to the user with an inline button for preview
        new_message = await update.message.reply_text(
            response_text,
            parse_mode='MarkdownV2',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Show Preview", callback_data=f"show_preview:{result['itemID']}:{result['icon']}")]
            ])
        )
    else:
        # If no result is found, notify the user
        await update.message.reply_text("No items found matching your search keyword.")

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles button presses for the "Show Preview" button."""
    query = update.callback_query
    await query.answer()

    # Parse the callback data
    action, item_id, icon_name = query.data.split(':')

    if action == 'show_preview':
        result = next((item for item in data if item['itemID'] == item_id), None)
        if result:
            icon_url = f"{ICON_URL_BASE}{icon_name}.png"
            response = requests.get(icon_url)
            if response.status_code == 200:
                media = InputMediaPhoto(icon_url, caption=f"*Name* `{escape_markdown(result['description'])}`\n*Item ID* `{escape_markdown(result['itemID'])}`\n*Icon Name* `{escape_markdown(result['icon'])}`", parse_mode="MarkdownV2")
            else:
                media = InputMediaPhoto(media="https://via.placeholder.com/2048?text=STAREXX+7", caption=f"*Name* `{escape_markdown(result['description'])}`\n*Item ID* `{escape_markdown(result['itemID'])}`\n*Icon Name* `{escape_markdown(result['icon'])}`", parse_mode="MarkdownV2")
            await query.edit_message_media(media=media)
            await query.edit_message_reply_markup(reply_markup=None)
        else:
            await query.edit_message_text("Item not found.")
    else:
        await query.edit_message_text("Invalid action.")

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles inline queries."""
    query = update.inline_query.query
    if not query:
        return

    results = []

    # Search for items based on query
    items = search_items(query)
    for item in items:
        results.append(
            InlineQueryResultArticle(
                id=uuid4(),
                title=f"Finding {item['description']}",
                input_message_content=InputTextMessageContent(
                    message_text=f"*Name* `{escape_markdown(item['description'])}`\n"
                                 f"*Item ID* `{escape_markdown(item['itemID'])}`\n"
                                 f"*Icon Name* `{escape_markdown(item['icon'])}`",
                    parse_mode='MarkdownV2'
                ),
                description=f"Search result for {item['description']}"
            )
        )

    await update.inline_query.answer(results)

def main() -> None:
    """Sets up the bot and starts the polling loop."""
    fetch_data()

    # Initialize the bot application
    app = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(InlineQueryHandler(inline_query))

    # Start polling
    app.run_polling()

if __name__ == '__main__':
    main()