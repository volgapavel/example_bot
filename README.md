# Place Information Telegram Bot

A Telegram bot that provides detailed information about interesting places using ChatGPT integration. The bot allows users to explore various locations, ask questions, and receive AI-powered responses about the places' history, features, and interesting facts.

## Features

- 🤖 Interactive Telegram bot interface
- 📍 Browse and select from various places of interest
- 💬 AI-powered responses using GPT-4 for detailed place information
- 📊 PostgreSQL database for storing place data and user interactions
- 📱 User-friendly keyboard interface for easy navigation

## Prerequisites

- Python 3.11+
- PostgreSQL database
- Telegram Bot Token
- OpenAI API Key

## Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
PGHOST=your_db_host
PGPORT=your_db_port
PGUSER=your_db_user
PGPASSWORD=your_db_password
PGDATABASE=your_db_name

# API Keys
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database:
   ```bash
   python create_tables.py
   ```

## Usage

1. Start the bot:
   ```bash
   python bot.py
   ```

2. In Telegram:
   - Start a chat with the bot using `/start`
   - Use the "📍 Choose Places" button to browse available locations
   - Select a place to learn more about it
   - Ask questions about the selected place
   - Use the "📌 Location" button (coming soon) for location-based features

## Key Components

- `bot.py`: Main bot application with event handlers
- `handlers.py`: Message and callback query handlers
- `gpt_service.py`: OpenAI GPT integration for AI-powered responses
- `models.py`: Database models for places and user dialogs
- `keyboards.py`: Custom keyboard layouts for user interaction

## Database Schema

### Places Table
- `id`: Primary key
- `name`: Place name
- `description`: Brief description
- `chatgpt_prompt`: Detailed information for GPT context
- `picture_links`: Array of image URLs
- `location`: Geographic coordinates
- `created_at`: Timestamp

### User Dialogs Table
- `id`: Primary key
- `user_id`: Telegram user ID
- `message_text`: User's message
- `response_text`: Bot's response
- `place_id`: Reference to place
- `timestamp`: Interaction timestamp

## Features in Development

- 📍 Location-based place recommendations
- 🖼️ Image support for places
- 📊 User interaction analytics
- 🗺️ Interactive maps integration

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
