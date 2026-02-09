# Deploy on BotHost

## Prerequisites
- Python 3.11+
- Virtualenv (recommended)
- Telegram bot token (set as `BOT_TOKEN`)

## Setup
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Export the token:
   ```bash
   export BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
   ```
3. Start the bot:
   ```bash
   python main.py
   ```

## Notes
- The bot reads the token from the `BOT_TOKEN` environment variable.
- Keep the process running with a process manager (e.g., systemd, supervisord, or tmux).
