# iChancy Telegram Bot

A comprehensive Telegram bot for managing iChancy platform accounts, transactions, deposits, withdrawals, and user interactions.

## Features

- **User Management**: Registration, authentication, and account management
- **Transaction Processing**: Multiple payment methods (Crypto, Bemo, Syriatel, ShamCash, Money Orders)
- **Deposit & Withdrawal**: Automated flows for deposits and withdrawals with admin approval
- **Gift System**: Send and receive gifts between users
- **Referral System**: User referral tracking and rewards
- **Admin Dashboard**: Django admin interface for managing settings and viewing data
- **Real-time Updates**: Background threads for cookie refresh, referral processing, and more

## Architecture

### Components

1. **Django Backend** (`mm/`): Admin interface and database models
2. **Telegram Bot** (`mm/myapp/ichancyBot/`): Main bot implementation
3. **Database**: MySQL for business data, SQLite for Django admin

### Technology Stack

- Python 3.8+
- Django 4.1.13
- python-telegram-bot 22.5
- MySQL/MariaDB
- Supervisor/systemd (for process management)

## Prerequisites

- Debian/Ubuntu server (or compatible Linux distribution)
- Python 3.8 or higher
- MySQL/MariaDB server
- Git
- sudo/root access for installation

## Quick Start

### 1. Clone the Repository

```bash
sudo mkdir -p /opt
sudo git clone <repository-url> /opt/ichancy-bot
sudo chown -R $USER:$USER /opt/ichancy-bot
cd /opt/ichancy-bot
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
nano .env
```

Edit the `.env` file with your configuration:

```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=cicp_bot

# Django
DJANGO_SECRET_KEY=generate-a-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost

# Telegram Bot (can also be set via Django admin)
TELEGRAM_BOT_TOKEN=your_bot_token
ADMIN_TELEGRAM_ID=your_admin_id
ICHANCY_COOKIE=your_cookie
PARENT_ID=your_parent_id
```

**Generate a secure Django secret key:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Run Deployment Script

Make the script executable and run it:

```bash
chmod +x deploy.sh
./deploy.sh
```

The deployment script will:
- Install all system dependencies
- Set up MySQL database
- Create Python virtual environment
- Install Python packages
- Run database migrations
- Create Django superuser
- Initialize settings
- Configure supervisor/systemd service
- Set up Nginx (if ALLOWED_HOSTS is configured)

### 4. Configure Settings

After deployment, configure the bot settings:

**Option A: Via Django Admin (Recommended)**
1. Access Django admin: `http://your-server/admin`
2. Login with superuser credentials
3. Go to "Settings" and configure:
   - Telegram Bot Token
   - Admin Telegram ID
   - iChancy Cookie
   - Parent ID
   - Other settings as needed

**Option B: Via Environment Variables**
- Set variables in `.env` file
- Run: `cd mm && python add_settings.py`

### 5. Start the Bot

**Using Supervisor:**
```bash
sudo supervisorctl start ichancy-bot
sudo supervisorctl status ichancy-bot
```

**Using systemd:**
```bash
sudo systemctl start ichancy-bot
sudo systemctl status ichancy-bot
sudo systemctl enable ichancy-bot  # Enable auto-start on boot
```

### 6. Verify Installation

Check the logs to ensure the bot is running:

```bash
tail -f /opt/ichancy-bot/mm/logs/bot.log
```

## Manual Installation (Alternative)

If you prefer manual installation:

### 1. Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv mysql-server mysql-client libmysqlclient-dev build-essential pkg-config
```

### 2. Set Up MySQL Database

```bash
sudo mysql -u root
```

```sql
CREATE DATABASE cicp_bot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bot_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON cicp_bot.* TO 'bot_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Create Virtual Environment

```bash
cd /opt/ichancy-bot
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Run Migrations

```bash
cd mm
python manage.py makemigrations myapp
python manage.py migrate --database=admin_db
python manage.py migrate --database=default
```

### 6. Create Superuser

```bash
python create_superuser.py
# Or interactively:
python manage.py createsuperuser
```

### 7. Initialize Settings

```bash
python add_settings.py
```

## Configuration

### Database Settings

The bot uses a dual-database setup:
- **MySQL (`default`)**: Business data (users, transactions, settings)
- **SQLite (`admin_db`)**: Django admin, authentication, sessions

### Bot Settings

Most bot configuration is stored in the MySQL `settings` table and can be managed via Django admin. The bot automatically reloads settings when they're updated.

### Environment Variables

Key environment variables (see `.env.example` for full list):

- `DB_*`: Database connection settings
- `DJANGO_SECRET_KEY`: Django secret key (required for production)
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `ADMIN_TELEGRAM_ID`: Admin Telegram user ID

## Running the Bot

### Development Mode

```bash
cd /opt/ichancy-bot/mm
source ../venv/bin/activate
python manage.py run_telegram_bot
```

### Production Mode (with Supervisor)

```bash
sudo supervisorctl start ichancy-bot
sudo supervisorctl stop ichancy-bot
sudo supervisorctl restart ichancy-bot
sudo supervisorctl status ichancy-bot
```

### Production Mode (with systemd)

```bash
sudo systemctl start ichancy-bot
sudo systemctl stop ichancy-bot
sudo systemctl restart ichancy-bot
sudo systemctl status ichancy-bot
```

## Monitoring and Logs

### View Logs

```bash
# Bot logs
tail -f /opt/ichancy-bot/mm/logs/bot.log

# Django logs
tail -f /opt/ichancy-bot/mm/django.log

# Supervisor logs
tail -f /opt/ichancy-bot/mm/logs/bot_supervisor.log

# Systemd logs
sudo journalctl -u ichancy-bot -f
```

### Check Bot Status

```bash
# Supervisor
sudo supervisorctl status ichancy-bot

# systemd
sudo systemctl status ichancy-bot
```

## Updating the Bot

1. **Pull latest changes:**
   ```bash
   cd /opt/ichancy-bot
   git pull
   ```

2. **Update dependencies:**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt --upgrade
   ```

3. **Run migrations:**
   ```bash
   cd mm
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Restart the bot:**
   ```bash
   sudo supervisorctl restart ichancy-bot
   # OR
   sudo systemctl restart ichancy-bot
   ```

## Troubleshooting

### Bot Not Starting

1. Check logs: `tail -f /opt/ichancy-bot/mm/logs/bot.log`
2. Verify database connection in `.env`
3. Check if settings are configured in database
4. Verify Telegram bot token is correct

### Database Connection Issues

1. Verify MySQL is running: `sudo systemctl status mysql`
2. Check database credentials in `.env`
3. Test connection: `mysql -u $DB_USERNAME -p$DB_PASSWORD -h $DB_HOST $DB_NAME`

### Permission Issues

```bash
sudo chown -R $USER:$USER /opt/ichancy-bot
chmod 600 /opt/ichancy-bot/.env
```

### Missing Dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Security Considerations

1. **Change Default Passwords**: Update Django superuser password and database passwords
2. **Secure Secret Key**: Use a strong, random `DJANGO_SECRET_KEY`
3. **Environment Variables**: Never commit `.env` file to version control
4. **Firewall**: Configure firewall to allow only necessary ports
5. **SSL/TLS**: Use HTTPS for Django admin in production
6. **File Permissions**: Ensure `.env` has restricted permissions (600)

## Project Structure

```
ichancy-bot/
├── deploy.sh              # Deployment script
├── .env.example           # Environment variables template
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── mm/                    # Django project
    ├── manage.py
    ├── mm/                # Django settings
    │   ├── settings.py
    │   └── ...
    └── myapp/             # Main application
        ├── models.py      # Database models
        ├── admin.py       # Django admin configuration
        └── ichancyBot/    # Telegram bot
            ├── bot.py     # Bot entry point
            ├── config/    # Configuration modules
            ├── flows/     # Conversation handlers
            └── ...
```

## Support

For issues, questions, or contributions, please contact the development team or open an issue in the repository.

## License

[Your License Here]
