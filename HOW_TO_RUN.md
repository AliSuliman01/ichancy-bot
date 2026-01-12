# How to Run the Bot and Dashboard

This guide explains how to run both the Telegram bot and the Django admin dashboard.

## Prerequisites

1. **Python 3.8+** installed
2. **MySQL database** running and accessible
3. **Virtual environment** activated (recommended)
4. **Environment variables** configured (`.env` file)
5. **Database settings** configured in MySQL `settings` table

## Initial Setup

### 1. Install Dependencies

```bash
# Activate virtual environment (if using one)
# Windows:
ichancy-env\Scripts\activate

# Linux/Mac:
source ichancy-env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root (`ichancy-bot/`) with:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=root
DB_PASSWORD=your_password
DB_NAME=cicp_bot
```

### 3. Configure Database Settings

The bot reads configuration from the MySQL `settings` table. You need to:

1. Ensure the `settings` table exists in your MySQL database
2. Insert a settings record with required values:
   - `telegram_bot_token`: Your Telegram bot token
   - `admin_telegram_id`: Admin Telegram user ID
   - `admin_chat_id`: Admin chat ID (optional)
   - `ichancy_cookie`: iChancy platform session cookie
   - `parent_id`: iChancy parent/affiliate ID
   - And other settings as needed

### 4. Initialize Django Admin Database

```bash
cd mm
python manage.py migrate
python manage.py createsuperuser
```

This creates the SQLite database for Django admin and creates a superuser account.

## Running the Application

### Option 1: Run Both Separately (Recommended for Development)

#### Terminal 1: Django Admin Dashboard

```bash
cd mm
python manage.py runserver
```

The dashboard will be available at: **http://127.0.0.1:8000/admin/**

Login with the superuser credentials you created.

#### Terminal 2: Telegram Bot

**Method A: Using Django Management Command (Recommended)**

```bash
cd mm
python manage.py run_telegram_bot
```

**Method B: Run Bot Directly**

```bash
cd mm/myapp/ichancyBot
python bot.py
```

### Option 2: Run Bot Only (No Dashboard)

If you only need the bot:

```bash
cd mm
python manage.py run_telegram_bot
```

Or:

```bash
cd mm/myapp/ichancyBot
python bot.py
```

## Running in Production

### Using Supervisor (Linux)

Create `/etc/supervisor/conf.d/ichancy_bot.conf`:

```ini
[program:ichancy_bot]
command=/path/to/venv/bin/python /path/to/mm/manage.py run_telegram_bot
directory=/path/to/mm
user=your_user
autostart=true
autorestart=true
stderr_logfile=/var/log/ichancy_bot.err.log
stdout_logfile=/var/log/ichancy_bot.out.log
environment=PATH="/path/to/venv/bin:%(ENV_PATH)s"
```

Then:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start ichancy_bot
```

### Using systemd (Linux)

Create `/etc/systemd/system/ichancy-bot.service`:

```ini
[Unit]
Description=iChancy Telegram Bot
After=network.target mysql.service

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/mm
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python manage.py run_telegram_bot
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ichancy-bot
sudo systemctl start ichancy-bot
sudo systemctl status ichancy-bot
```

### Using PM2 (Cross-platform)

```bash
pm2 start "python manage.py run_telegram_bot" --name ichancy-bot --cwd /path/to/mm
pm2 save
pm2 startup
```

### Windows Task Scheduler

1. Create a batch file `start_bot.bat`:
```batch
@echo off
cd C:\path\to\mm
C:\path\to\venv\Scripts\python.exe manage.py run_telegram_bot
```

2. Schedule it to run at startup or as a service.

## Verification

### Check Bot is Running

- Look for log messages indicating the bot started
- Send a message to your bot on Telegram
- Check that background threads are running (referral, crypto prices, cookie refresh)

### Check Dashboard is Running

- Open http://127.0.0.1:8000/admin/
- Login with superuser credentials
- Verify you can see Users, Transactions, Settings, etc.

## Troubleshooting

### Bot Won't Start

1. **Check environment variables**:
   ```bash
   # Verify .env file exists and has correct values
   cat .env
   ```

2. **Check database connection**:
   ```bash
   cd mm
   python manage.py dbshell
   ```

3. **Check settings table**:
   ```sql
   SELECT * FROM settings LIMIT 1;
   ```

4. **Check bot token**:
   - Verify `telegram_bot_token` is set in settings table
   - Token should start with a number and colon (e.g., `123456789:ABCdef...`)

5. **Check Python path**:
   - If using direct method, ensure you're in the correct directory
   - If using management command, it should handle paths automatically

### Dashboard Won't Start

1. **Check migrations**:
   ```bash
   cd mm
   python manage.py migrate
   ```

2. **Check database connection**:
   - Verify MySQL is running
   - Check `.env` file has correct credentials

3. **Check admin user**:
   ```bash
   python manage.py createsuperuser
   ```

### Import Errors

If you see import errors:

1. **Activate virtual environment**:
   ```bash
   # Windows
   ichancy-env\Scripts\activate
   
   # Linux/Mac
   source ichancy-env/bin/activate
   ```

2. **Reinstall dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Check Python path** (for direct bot run):
   ```bash
   # Make sure you're in the ichancyBot directory
   cd mm/myapp/ichancyBot
   python bot.py
   ```

### Database Connection Errors

1. **Verify MySQL is running**:
   ```bash
   # Linux/Mac
   sudo systemctl status mysql
   
   # Windows - check Services
   ```

2. **Test connection**:
   ```bash
   mysql -h localhost -u root -p
   ```

3. **Check Django can connect**:
   ```bash
   cd mm
   python manage.py dbshell
   ```

## Stopping the Services

### Bot
- Press `Ctrl+C` in the terminal running the bot
- Or use process manager commands:
  ```bash
  # Supervisor
  sudo supervisorctl stop ichancy_bot
  
  # systemd
  sudo systemctl stop ichancy-bot
  
  # PM2
  pm2 stop ichancy-bot
  ```

### Dashboard
- Press `Ctrl+C` in the terminal running Django
- Or stop the web server process

## Quick Start Summary

```bash
# 1. Activate virtual environment
ichancy-env\Scripts\activate  # Windows
# or
source ichancy-env/bin/activate  # Linux/Mac

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Setup Django admin (first time only)
cd mm
python manage.py migrate
python manage.py createsuperuser

# 4. Run Django dashboard (Terminal 1)
python manage.py runserver

# 5. Run Telegram bot (Terminal 2)
python manage.py run_telegram_bot
```

## Notes

- The bot is a **long-running process** - it needs to stay running to receive Telegram updates
- The dashboard can be started/stopped independently
- Both services can run simultaneously without conflicts
- Settings changes in Django admin automatically sync to the bot (via signals)
- The bot reads configuration from the database, not environment variables (except DB connection)


