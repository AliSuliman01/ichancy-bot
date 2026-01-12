# How to Update Settings Record

A settings record has been created in the database with default values. You need to update it with your actual configuration.

## Method 1: Using Environment Variables (Recommended for Scripts)

```bash
# Set environment variables
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export ADMIN_TELEGRAM_ID="your_telegram_user_id"
export ICHANCY_COOKIE="your_ichancy_cookie"
export PARENT_ID="your_parent_id"
export ADMIN_CHAT_ID="your_admin_chat_id"  # Optional
export EXCHANGE_RATE="1.00"  # Optional, defaults to 1.00

# Run the script
source ichancy-env/Scripts/activate
cd mm
python add_settings.py
```

## Method 2: Using Django Admin (Recommended for Manual Updates)

1. Start Django server:
   ```bash
   source ichancy-env/Scripts/activate
   cd mm
   python manage.py runserver
   ```

2. Go to http://127.0.0.1:8000/admin/
3. Login with your superuser credentials
4. Navigate to **Myapp** > **Settings**
5. Click on the settings record (ID: 1)
6. Update the fields:
   - **Telegram Bot Token**: Your bot token from @BotFather
   - **Admin Telegram ID**: Your Telegram user ID
   - **iChancy Cookie**: Your iChancy platform session cookie
   - **Parent ID**: Your iChancy parent/affiliate ID
   - **Admin Chat ID**: (Optional) Admin chat ID
   - **Exchange Rate**: (Optional) Currency exchange rate
   - Other fields as needed

7. Click **Save**

## Method 3: Using Django Shell

```bash
source ichancy-env/Scripts/activate
cd mm
python manage.py shell
```

Then in the shell:
```python
from myapp.models import Settings

settings = Settings.objects.first()
settings.telegram_bot_token = "your_bot_token"
settings.admin_telegram_id = "your_telegram_id"
settings.ichancy_cookie = "your_cookie"
settings.parent_id = "your_parent_id"
settings.save()
```

## Required Fields

The following fields are **required** for the bot to function:

- `telegram_bot_token`: Your Telegram bot token (from @BotFather)
- `admin_telegram_id`: Your Telegram user ID
- `ichancy_cookie`: iChancy platform session cookie
- `parent_id`: iChancy parent/affiliate ID

## Optional Fields

- `admin_chat_id`: Admin chat ID
- `exchange_rate`: Currency exchange rate (default: 1.00)
- `bot_name`: Bot name
- `telegram_channels`: Comma-separated channel IDs
- `telegram_groups`: Comma-separated group IDs
- `transactions_telegram_bot_token`: Secondary bot token for transactions
- `cookie_from_group_id`: Group ID for cookie refresh
- Payment method group IDs (crypto, bemo, syriatel, shamcash deposit/withdraw groups)
- `user_agent`: User agent string for API requests

## Verify Settings

After updating, verify the settings:

```bash
source ichancy-env/Scripts/activate
cd mm
python add_settings.py
```

This will show the current settings and warn about any missing required fields.
