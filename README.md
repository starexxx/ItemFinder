
# ItemFinder Bot

ItemFinder is a Telegram bot designed to retrieve and display item information from a JSON data source. This bot allows users to search for items by their ID or description and provides item previews with details and icons.

## Features

- **Search by ID or Description**: Quickly retrieve items using their ID or description.
- **Inline Queries**: Use the bot in inline mode to search for items without starting a chat.
- **Preview Items**: Displays a preview of the item with its details and an icon.
- **Interactive Buttons**: Use buttons to perform additional actions, like showing an item's preview.
- **Dynamic Data**: Fetches data from a remote JSON URL to keep information updated.

## Project Structure

```
.
├── LICENSE
├── README.md
├── main.py
├── project-banner.png
└── requirements.txt
```

### Files:
- **`main.py`**: Contains the bot's source code.
- **`project-banner.png`**: The banner image for the project.
- **`requirements.txt`**: Python dependencies for the project.
- **`README.md`**: Documentation for the project.
- **`LICENSE`**: License information for the project.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/starexxx/ItemFinder.git
   cd ItemFinder
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Update the `BOT_TOKEN` and `JSON_URL` variables in `main.py`:
   - **`BOT_TOKEN`**: Your Telegram bot token.
   - **`JSON_URL`**: Use `itemData.json` for `JSON_URL`, available at:
     [https://github.com/jinix6/ItemID/tree/main/assets](https://github.com/jinix6/ItemID/tree/main/assets)
   - **`ICON_URL_BASE`**: Use:
     `https://raw.githubusercontent.com/starexxx/ff-resources/main/pngs/300x300/`

## Image Quality Options

The icon URLs support the following resolutions:
- `300x300`
- `200x200`
- `100x100`

Choose the resolution that best suits your requirements.

## Usage

1. Run the bot:
   ```bash
   python main.py
   ```

2. Start the bot on Telegram:
   - Send `/start` to begin interacting with the bot.
   - Send an item ID or description to search for an item.
   - Use inline queries by typing `@YourBotUsername <query>` in any Telegram chat.

## Dependencies

The project requires the following Python packages:

- `python-telegram-bot`
- `requests`

Install them via `requirements.txt` or manually using pip.

## Example

**Inline Query Example:**

- Type `@YourBotUsername <item ID or description>` in any Telegram chat to search for an item.

**Search Example:**

- Send `12345` to retrieve the item with ID `12345`.
- Send `Sword` to retrieve an item named "Sword."

## Contribution

Contributions are welcome! Feel free to fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Credits

- **Created by Starexx**.
- Icon resources are hosted at: `https://raw.githubusercontent.com/starexxx/ff-resources/main/`.

---
