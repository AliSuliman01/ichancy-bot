# Quick Deployment Guide

This is a quick reference guide for deploying the iChancy Bot on a Debian server.

## Prerequisites Checklist

- [ ] Debian/Ubuntu server with sudo access
- [ ] MySQL/MariaDB installed (or will be installed by script)
- [ ] Git installed (or will be installed by script)
- [ ] Telegram Bot Token from @BotFather
- [ ] iChancy Cookie and Parent ID

## Step-by-Step Deployment

### 1. Clone and Prepare

```bash
# Clone repository
sudo mkdir -p /opt
sudo git clone <your-repo-url> /opt/ichancy-bot
sudo chown -R $USER:$USER /opt/ichancy-bot
cd /opt/ichancy-bot
```

### 2. Configure Environment

```bash
# Copy example file
cp .env.example .env

# Edit with your values
nano .env
```

**Required minimum configuration:**
```env
DB_PASSWORD=your_mysql_password
DJANGO_SECRET_KEY=<generate-random-key>
TELEGRAM_BOT_TOKEN=your_bot_token
ADMIN_TELEGRAM_ID=your_telegram_id
ICHANCY_COOKIE=your_cookie
PARENT_ID=your_parent_id
```

**Generate Django secret key:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Run Deployment

```bash
chmod +x deploy.sh
./deploy.sh
```

The script will:
- Install all dependencies
- Set up MySQL database
- Create virtual environment
- Install Python packages
- Run migrations
- Create superuser
- Initialize settings
- Set up services

### 4. Configure Bot Settings

After deployment, access Django admin:
```
http://your-server-ip/admin
```

Login and configure Settings model with:
- Telegram Bot Token
- Admin Telegram ID
- iChancy Cookie
- Parent ID
- Other required settings

### 5. Start the Bot

```bash
# Using systemd (recommended)
sudo systemctl start ichancy-bot
sudo systemctl enable ichancy-bot
sudo systemctl status ichancy-bot

# OR using Supervisor
sudo supervisorctl start ichancy-bot
sudo supervisorctl status ichancy-bot
```

### 6. Verify

```bash
# Check logs
tail -f /opt/ichancy-bot/mm/logs/bot.log

# Check service status
sudo systemctl status ichancy-bot
```

## Post-Deployment Checklist

- [ ] Bot is running (check logs)
- [ ] Django admin accessible
- [ ] Settings configured in database
- [ ] Bot responds to Telegram messages
- [ ] Changed default superuser password
- [ ] Firewall configured (if needed)
- [ ] SSL/HTTPS configured (for production)

## Common Issues

### Bot won't start
- Check `.env` file exists and has correct values
- Verify database connection: `mysql -u $DB_USERNAME -p$DB_PASSWORD $DB_NAME`
- Check logs: `tail -f /opt/ichancy-bot/mm/logs/bot.log`

### Database connection error
- Ensure MySQL is running: `sudo systemctl status mysql`
- Verify credentials in `.env`
- Check database exists: `mysql -u root -e "SHOW DATABASES;"`

### Permission denied
```bash
sudo chown -R $USER:$USER /opt/ichancy-bot
chmod 600 /opt/ichancy-bot/.env
```

## Updating the Bot

```bash
cd /opt/ichancy-bot
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
cd mm
python manage.py migrate
sudo systemctl restart ichancy-bot
```

## Useful Commands

```bash
# View logs
tail -f /opt/ichancy-bot/mm/logs/bot.log

# Restart bot
sudo systemctl restart ichancy-bot

# Stop bot
sudo systemctl stop ichancy-bot

# Check status
sudo systemctl status ichancy-bot

# Django shell
cd /opt/ichancy-bot/mm
source ../venv/bin/activate
python manage.py shell
```

## Support

For detailed information, see [README.md](README.md)
