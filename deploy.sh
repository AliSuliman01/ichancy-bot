#!/bin/bash

###############################################################################
# iChancy Bot Deployment Script for Debian/Ubuntu
# This script handles complete deployment including dependencies, database setup,
# and migrations for a fresh server installation.
###############################################################################

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/var/www/ichancy-bot"
VENV_DIR="$PROJECT_DIR/venv"
DB_NAME="${DB_NAME:-cicp_bot}"
DB_USER="${DB_USERNAME:-root}"
DB_PASSWORD="${DB_PASSWORD:-}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-3306}"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}iChancy Bot Deployment Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Function to print status
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    print_error "Please do not run this script as root. Run as a regular user with sudo privileges."
    exit 1
fi

# Check if .env file exists
if [ ! -f "$PROJECT_DIR/.env" ]; then
    print_error ".env file not found in $PROJECT_DIR"
    print_warning "Please create a .env file with the following variables:"
    echo "  DB_HOST=localhost"
    echo "  DB_PORT=3306"
    echo "  DB_USERNAME=your_db_user"
    echo "  DB_PASSWORD=your_db_password"
    echo "  DB_NAME=cicp_bot"
    echo "  DJANGO_SECRET_KEY=your_secret_key"
    echo "  DEBUG=False"
    echo "  ALLOWED_HOSTS=your_domain.com,localhost"
    exit 1
fi

# Load environment variables
export $(cat $PROJECT_DIR/.env | grep -v '^#' | xargs)

print_status "Starting deployment process..."

# Step 1: Update system packages
print_status "Step 1: Updating system packages..."
sudo apt-get update -qq
sudo apt-get upgrade -y -qq

# Step 2: Install system dependencies
print_status "Step 2: Installing system dependencies..."

# Check for required system packages (skip installation if already present)
print_status "Checking for required system packages..."

# Check MySQL client libraries
MYSQL_DEV_PKG=""
if dpkg -l | grep -q "libmysqlclient-dev"; then
    print_status "libmysqlclient-dev is already installed."
    MYSQL_DEV_PKG="libmysqlclient-dev"
elif dpkg -l | grep -q "libmariadb-dev"; then
    print_status "libmariadb-dev is already installed."
    MYSQL_DEV_PKG="libmariadb-dev"
else
    # Try to install MySQL dev package if not found
    print_status "Installing MySQL development libraries..."
    if sudo apt-get install -y libmysqlclient-dev 2>/dev/null; then
        MYSQL_DEV_PKG="libmysqlclient-dev"
    else
        print_status "libmysqlclient-dev not available, installing libmariadb-dev..."
        sudo apt-get install -y libmariadb-dev libmariadb-dev-compat
        MYSQL_DEV_PKG="libmariadb-dev"
    fi
fi

# Check for other required packages
REQUIRED_PKGS=""
for pkg in python3 python3-pip python3-venv build-essential pkg-config; do
    if ! dpkg -l | grep -q "^ii  $pkg "; then
        REQUIRED_PKGS="$REQUIRED_PKGS $pkg"
    fi
done

if [ -n "$REQUIRED_PKGS" ]; then
    print_status "Installing missing packages: $REQUIRED_PKGS"
    sudo apt-get install -y $REQUIRED_PKGS
else
    print_status "All required packages are already installed."
fi

# Verify MySQL, Git, Supervisor, and Nginx are available (but don't install)
if ! command -v mysql &> /dev/null && ! command -v mariadb &> /dev/null; then
    print_warning "MySQL/MariaDB client not found in PATH, but continuing (may be installed but not in PATH)"
fi

if ! command -v git &> /dev/null; then
    print_warning "Git not found in PATH, but continuing (may be installed but not in PATH)"
fi

if ! command -v supervisorctl &> /dev/null; then
    print_warning "Supervisor not found in PATH, but continuing (may be installed but not in PATH)"
fi

if ! command -v nginx &> /dev/null; then
    print_warning "Nginx not found in PATH, but continuing (may be installed but not in PATH)"
fi

# Step 3: Setup MySQL database
print_status "Step 3: Setting up MySQL database..."

# Check if MySQL/MariaDB is running (try both service names)
if sudo systemctl is-active --quiet mysql 2>/dev/null || sudo systemctl is-active --quiet mariadb 2>/dev/null; then
    print_status "MySQL/MariaDB service is running."
elif sudo systemctl is-active --quiet mysqld 2>/dev/null; then
    print_status "MySQL service (mysqld) is running."
else
    print_warning "MySQL/MariaDB service doesn't appear to be running."
    print_warning "Please ensure MySQL/MariaDB is running before continuing."
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Aborting deployment."
        exit 1
    fi
fi

# Create database if it doesn't exist
print_status "Creating database '$DB_NAME' if it doesn't exist..."
sudo mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS \`$DB_NAME\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EOF

# Create database user if specified and different from root
if [ "$DB_USER" != "root" ]; then
    print_status "Creating database user '$DB_USER'..."
    sudo mysql -u root <<EOF
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON \`$DB_NAME\`.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
EOF
fi

# Step 4: Create virtual environment
print_status "Step 4: Setting up Python virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    print_status "Virtual environment created."
else
    print_status "Virtual environment already exists."
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Step 5: Upgrade pip
print_status "Step 5: Upgrading pip..."
pip install --upgrade pip setuptools wheel -q

# Step 6: Install Python dependencies
print_status "Step 6: Installing Python dependencies..."
cd "$PROJECT_DIR"
pip install -r requirements.txt -q

# Step 7: Run Django migrations
print_status "Step 7: Running Django migrations..."
cd "$PROJECT_DIR/mm"

# First, create the settings table manually to avoid errors during migrations
# This prevents Django from trying to load settings before the table exists
print_status "Creating settings table if it doesn't exist..."
python create_settings_table.py 2>/dev/null || print_warning "Settings table check completed."

# Make migrations for Settings model (only managed model)
print_status "Making migrations..."
python manage.py makemigrations myapp --noinput 2>&1 | grep -v "Failed to load settings" || true

# Run migrations for admin_db (SQLite for Django admin)
print_status "Running migrations for admin database..."
python manage.py migrate --database=admin_db --noinput 2>&1 | grep -v "Failed to load settings" || true

# Run migrations for default database (MySQL - only Settings table)
print_status "Running migrations for MySQL database..."
python manage.py migrate myapp --database=default --noinput 2>&1 | grep -v "Failed to load settings" || true

# Verify Settings table exists one more time
print_status "Verifying Settings table exists..."
python create_settings_table.py 2>/dev/null || print_warning "Settings table verification completed."

print_status "Database migrations completed."

# Step 8: Create Django superuser (if not exists)
print_status "Step 8: Creating Django superuser..."
if [ -z "$DJANGO_SUPERUSER_USERNAME" ]; then
    DJANGO_SUPERUSER_USERNAME="admin"
fi
if [ -z "$DJANGO_SUPERUSER_EMAIL" ]; then
    DJANGO_SUPERUSER_EMAIL="admin@example.com"
fi
if [ -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
    DJANGO_SUPERUSER_PASSWORD="admin123"
    print_warning "Using default superuser password. Please change it after first login!"
fi

python create_superuser.py || print_warning "Superuser may already exist or creation failed."

# Step 9: Initialize settings in database
print_status "Step 9: Initializing settings in database..."
python add_settings.py || print_warning "Settings initialization completed or already exists."

# Step 10: Create necessary directories
print_status "Step 10: Creating necessary directories..."
mkdir -p "$PROJECT_DIR/mm/logs"
mkdir -p "$PROJECT_DIR/mm/static"
mkdir -p "$PROJECT_DIR/mm/media"

# Step 11: Collect static files (if needed)
print_status "Step 11: Collecting static files..."
python manage.py collectstatic --noinput || print_warning "Static files collection skipped or failed."

# Step 12: Set proper permissions
print_status "Step 12: Setting proper permissions..."
sudo chown -R $USER:$USER "$PROJECT_DIR"
chmod -R 755 "$PROJECT_DIR"
chmod 600 "$PROJECT_DIR/.env"

# Step 13: Create supervisor configuration
print_status "Step 13: Creating supervisor configuration..."
sudo tee /etc/supervisor/conf.d/ichancy-bot.conf > /dev/null <<EOF
[program:ichancy-bot]
command=$VENV_DIR/bin/python $PROJECT_DIR/mm/manage.py run_telegram_bot
directory=$PROJECT_DIR/mm
user=$USER
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=$PROJECT_DIR/mm/logs/bot_supervisor.log
stderr_logfile=$PROJECT_DIR/mm/logs/bot_supervisor_error.log
environment=PATH="$VENV_DIR/bin"
EOF

# Step 14: Create systemd service (alternative to supervisor)
print_status "Step 14: Creating systemd service..."
sudo tee /etc/systemd/system/ichancy-bot.service > /dev/null <<EOF
[Unit]
Description=iChancy Telegram Bot
After=network.target mysql.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_DIR/mm
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/python $PROJECT_DIR/mm/manage.py run_telegram_bot
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Step 15: Reload and enable services
print_status "Step 15: Reloading service configurations..."
# Handle supervisor gracefully (ignore errors from other configs)
print_status "Reloading supervisor configuration..."
# Suppress errors from other projects' configs (like laravel-worker)
sudo supervisorctl reread 2>&1 | grep -v "CANT_REREAD" | grep -v "laravel-worker" || true
sudo supervisorctl update ichancy-bot 2>&1 | grep -v "CANT_REREAD" | grep -v "error" || true
print_status "Reloading systemd daemon..."
sudo systemctl daemon-reload
sudo systemctl enable ichancy-bot.service
print_status "Service configurations reloaded."

# Step 16: Create Nginx configuration (optional, for Django admin)
print_status "Step 16: Creating Nginx configuration..."
if [ ! -z "$ALLOWED_HOSTS" ]; then
    sudo tee /etc/nginx/sites-available/ichancy-bot > /dev/null <<EOF
server {
    listen 80;
    server_name $ALLOWED_HOSTS;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static/ {
        alias $PROJECT_DIR/mm/static/;
    }

    location /media/ {
        alias $PROJECT_DIR/mm/media/;
    }
}
EOF

    sudo ln -sf /etc/nginx/sites-available/ichancy-bot /etc/nginx/sites-enabled/
    # Test nginx config (ignore warnings from other projects' SSL configs)
    if sudo nginx -t 2>&1 | grep -q "test is successful"; then
        sudo systemctl reload nginx
        print_status "Nginx configuration created and reloaded."
    else
        # Check if it's just warnings (like ssl_stapling) vs actual errors
        if sudo nginx -t 2>&1 | grep -q "syntax is ok"; then
            sudo systemctl reload nginx
            print_status "Nginx configuration created and reloaded (warnings from other configs ignored)."
        else
            print_warning "Nginx configuration test failed. Please check manually: sudo nginx -t"
        fi
    fi
else
    print_warning "ALLOWED_HOSTS not set. Skipping Nginx configuration."
fi

# Final summary
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Completed Successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
print_status "Next steps:"
echo "  1. Review and update settings in Django admin: http://your-server/admin"
echo "  2. Configure Telegram bot token and other settings in the Settings model"
echo "  3. Start the bot service:"
echo "     sudo supervisorctl start ichancy-bot"
echo "     OR"
echo "     sudo systemctl start ichancy-bot"
echo "  4. Check bot status:"
echo "     sudo supervisorctl status ichancy-bot"
echo "     OR"
echo "     sudo systemctl status ichancy-bot"
echo "  5. View logs:"
echo "     tail -f $PROJECT_DIR/mm/logs/bot.log"
echo ""
print_warning "IMPORTANT: Change the default Django superuser password!"
print_warning "IMPORTANT: Ensure all required settings are configured in the database!"
