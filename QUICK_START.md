# Quick Start Guide

## ✅ Setup Complete

The virtual environment has been activated and dependencies have been installed.

## 📋 Prerequisites Checklist

Before running the project, ensure you have:

- [x] Virtual environment activated
- [x] Dependencies installed
- [x] `.env` file created (✅ Done - update `DB_PASSWORD` with your MySQL password)
- [ ] MySQL database running and accessible
- [ ] Database `cicp_bot` created (or update `DB_NAME` in `.env`)
- [ ] MySQL `settings` table configured with required values

## 🚀 Running the Project

### Step 1: Update Environment Variables

Edit the `.env` file and update the database password:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=root
DB_PASSWORD=your_actual_mysql_password  # ← Update this!
DB_NAME=cicp_bot
```

### Step 2: Setup MySQL Database Settings

The bot requires configuration in the MySQL `settings` table. Connect to your MySQL database and ensure the `settings` table exists with at least these fields:

- `telegram_bot_token`: Your Telegram bot token (from @BotFather)
- `admin_telegram_id`: Your Telegram user ID
- `admin_chat_id`: Admin chat ID (optional)
- `ichancy_cookie`: iChancy platform session cookie
- `parent_id`: iChancy parent/affiliate ID

### Step 3: Initialize Django Admin (First Time Only)

Open a terminal and run:

```bash
# Activate virtual environment
source ichancy-env/Scripts/activate  # Git Bash
# OR
ichancy-env\Scripts\activate  # Command Prompt

# Navigate to Django project
cd mm

# Run migrations
python manage.py migrate

# Create superuser (for admin dashboard)
# Note: Must specify admin_db database due to dual database setup
python manage.py createsuperuser --database=admin_db
# OR use the helper script:
python create_superuser.py
```

### Step 4: Run the Application

You have two options:

#### Option A: Run Both Bot and Dashboard (Recommended)

**Terminal 1 - Django Admin Dashboard:**
```bash
# Activate venv (if not already activated)
source ichancy-env/Scripts/activate
cd mm
python manage.py runserver
```

Access the dashboard at: **http://127.0.0.1:8000/admin/**

**Terminal 2 - Telegram Bot:**
```bash
# Activate venv (if not already activated)
source ichancy-env/Scripts/activate
cd mm
python manage.py run_telegram_bot
```

#### Option B: Run Bot Only

```bash
# Activate venv
source ichancy-env/Scripts/activate
cd mm
python manage.py run_telegram_bot
```

Or run directly:
```bash
source ichancy-env/Scripts/activate
cd mm/myapp/ichancyBot
python bot.py
```

## 🔍 Verification

### Check Bot is Running
- Look for log messages indicating the bot started
- Send a message to your bot on Telegram
- Check that background threads are running

### Check Dashboard is Running
- Open http://127.0.0.1:8000/admin/
- Login with superuser credentials
- Verify you can see Users, Transactions, Settings, etc.

## ⚠️ Troubleshooting

### Database Connection Issues
1. Verify MySQL is running:
   ```bash
   # Test connection
   mysql -h localhost -u root -p
   ```

2. Check `.env` file has correct credentials

3. Test Django connection:
   ```bash
   cd mm
   python manage.py dbshell
   ```

### Bot Won't Start
1. Check environment variables are loaded
2. Verify `telegram_bot_token` is set in MySQL `settings` table
3. Check database connection settings

### Import Errors
1. Ensure virtual environment is activated
2. Reinstall dependencies: `pip install -r requirements.txt`

## 📝 Notes

- The bot is a **long-running process** - keep it running to receive Telegram updates
- The dashboard can be started/stopped independently
- Both services can run simultaneously
- Settings changes in Django admin automatically sync to the bot

## 🛑 Stopping Services

- **Bot**: Press `Ctrl+C` in the terminal
- **Dashboard**: Press `Ctrl+C` in the terminal

---

For more detailed information, see `HOW_TO_RUN.md`
