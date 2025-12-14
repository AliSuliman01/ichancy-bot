# Telegram Bot Integration Guide

This document explains how the Telegram bot has been integrated into the Django project.

## Overview

The Telegram bot is now integrated into the Django project as a **Django management command**. This allows you to run the bot as a long-running process alongside your Django web server.

## Important Note

**The bot is NOT a cron job** - it's a long-running process that needs to stay alive to continuously receive updates from Telegram. Cron jobs are for periodic tasks that run and exit, but the Telegram bot uses `run_polling()` which blocks and continuously polls for updates.

## Running the Bot

### Option 1: Django Management Command (Recommended)

Run the bot using Django's management command:

```bash
cd mm
python manage.py run_telegram_bot
```

This will:
- Start the bot and all its background threads
- Keep running until you press Ctrl+C
- Log all activity through the bot's logger

### Option 2: Run as a Separate Process

You can run the bot in a separate terminal/process while Django runs in another:

**Terminal 1 (Django):**
```bash
cd mm
python manage.py runserver
```

**Terminal 2 (Telegram Bot):**
```bash
cd mm
python manage.py run_telegram_bot
```

### Option 3: Using a Process Manager (Production)

For production, use a process manager like:
- **supervisor** (Linux)
- **systemd** (Linux)
- **PM2** (Node.js-based, works on all platforms)
- **Windows Task Scheduler** (Windows)

Example supervisor configuration (`/etc/supervisor/conf.d/telegram_bot.conf`):

```ini
[program:telegram_bot]
command=/path/to/venv/bin/python /path/to/mm/manage.py run_telegram_bot
directory=/path/to/mm
user=your_user
autostart=true
autorestart=true
stderr_logfile=/var/log/telegram_bot.err.log
stdout_logfile=/var/log/telegram_bot.out.log
```

## Project Structure

The integration maintains the existing structure:
- `telegramBot/ichancyBot/` - Original bot code (unchanged)
- `mm/myapp/management/commands/run_telegram_bot.py` - Django command to run the bot

## How It Works

1. The Django management command adds the `telegramBot/ichancyBot` directory to Python's `sys.path`
2. It imports the bot module and all its dependencies
3. It initializes background threads (referral handler, crypto prices, cookie refresh)
4. It starts the bot's polling loop using `application.run_polling()`

## Benefits of This Approach

1. **Unified Project**: Both Django and Telegram bot are in one codebase
2. **Shared Configuration**: Can use Django settings for configuration
3. **Shared Database**: Both can use the same database connection
4. **Easy Deployment**: Deploy both together
5. **Management**: Use Django's management infrastructure

## Configuration

The bot still uses its original configuration from:
- `telegramBot/ichancyBot/config/telegram.py`
- Environment variables (via `.env` file)

Make sure your `.env` file is in the project root or in the `telegramBot/ichancyBot/` directory.

## Troubleshooting

### Import Errors

If you get import errors, make sure:
1. All dependencies are installed: `pip install -r requirements.txt`
2. The `telegramBot/ichancyBot` directory exists
3. Python can find the bot modules (the command adds them to sys.path automatically)

### Bot Not Starting

Check:
1. Environment variables are set correctly (TELEGRAM_BOT_TOKEN, etc.)
2. Database connection is working
3. All required files exist (sessions, config files, etc.)

### Running Both Django and Bot

You can run both simultaneously:
- They are independent processes
- They can share the same database
- They don't interfere with each other

## Next Steps

1. Test the bot: `python manage.py run_telegram_bot`
2. Set up a process manager for production
3. Consider integrating shared models/database access between Django and the bot
4. Add Django admin interface for bot management (optional)

