# iChancy Bot Project Index

## Project Overview

This is a Django-based Telegram bot application for managing iChancy gaming platform accounts. The bot handles user registration, deposits, withdrawals, gift management, and various payment methods (crypto, mobile money, etc.).

## Project Structure

```
ichancy-bot/
├── mm/                          # Django project root
│   ├── manage.py                # Django management script
│   ├── mm/                      # Django project settings
│   │   ├── settings.py          # Django configuration
│   │   ├── urls.py              # URL routing
│   │   ├── wsgi.py              # WSGI config
│   │   └── asgi.py              # ASGI config
│   ├── myapp/                   # Main Django app
│   │   ├── models.py            # Django ORM models (read-only, mapped to MySQL)
│   │   ├── admin.py             # Django admin interface
│   │   ├── routers.py           # Database routing (SQLite for admin, MySQL for data)
│   │   ├── signals.py           # Django signals (syncs Settings to bot config)
│   │   ├── views.py             # Django views (currently empty)
│   │   └── ichancyBot/          # Telegram bot implementation
│   │       ├── bot.py           # Main bot entry point
│   │       ├── button.py        # Inline button handlers
│   │       ├── database.py      # MySQL database connection
│   │       ├── iChancyAPI.py    # iChancy platform API client
│   │       ├── Logger.py        # Logging configuration
│   │       ├── store.py         # State storage
│   │       ├── threadManager.py # Background thread management
│   │       ├── referalHandler.py # Referral system handler
│   │       ├── refreshingCookie.py # Cookie refresh thread
│   │       ├── refreshingCookieFromFile.py # Cookie refresh from file
│   │       ├── cryptoPrices.py  # Crypto price tracking
│   │       ├── config/          # Configuration modules
│   │       │   ├── telegram.py  # Telegram bot config (reads from DB)
│   │       │   ├── database.py  # Database config (from .env)
│   │       │   ├── settings.py  # Settings loader (reads from MySQL)
│   │       │   ├── ichancy.py   # iChancy API config
│   │       │   ├── device.py    # Device/user-agent config
│   │       │   ├── crypto.py    # Crypto payment config
│   │       │   ├── bemo.py      # Bemo payment config
│   │       │   ├── syriatel.py  # Syriatel payment config
│   │       │   ├── shamCash.py  # ShamCash payment config
│   │       │   └── orderMoney.py # Money order config
│   │       ├── models/          # Bot's internal models
│   │       │   ├── user.py
│   │       │   ├── transaction.py
│   │       │   ├── accountTransaction.py
│   │       │   ├── cryptoTransaction.py
│   │       │   ├── bemoTransaction.py
│   │       │   ├── syriatelTransaction.py
│   │       │   ├── shamCashTransaction.py
│   │       │   ├── orderMoney.py
│   │       │   ├── gift.py
│   │       │   └── messageToAdmin.py
│   │       ├── flows/           # Conversation flow handlers
│   │       │   ├── startFlow/   # Bot start/registration flow
│   │       │   ├── createAccount/ # Account creation
│   │       │   ├── depositAccount/ # Account deposit
│   │       │   ├── withdrawalAccount/ # Account withdrawal
│   │       │   ├── cryptoDeposit/ # Crypto deposit flow
│   │       │   ├── cryptoWithdraw/ # Crypto withdrawal flow
│   │       │   ├── bemoDepodit/ # Bemo deposit
│   │       │   ├── bemoWithdrawal/ # Bemo withdrawal
│   │       │   ├── syriatelCashDepodit/ # Syriatel deposit
│   │       │   ├── syriatelCashWithdrawal/ # Syriatel withdrawal
│   │       │   ├── shamCashDepodit/ # ShamCash deposit
│   │       │   ├── shamCashWithdrawal/ # ShamCash withdrawal
│   │       │   ├── moneyOrderWithdrawal/ # Money order withdrawal
│   │       │   ├── sendGifts/   # Send gift flow
│   │       │   ├── resieveGifts/ # Receive gift flow
│   │       │   ├── messageToAdmin/ # Contact admin flow
│   │       │   ├── balanceCommand/ # Balance check
│   │       │   ├── editDepositFromAdmin/ # Admin deposit editing
│   │       │   ├── editWithdrawFromAdmin/ # Admin withdrawal editing
│   │       │   ├── approveDepositFromAdmin/ # Admin deposit approval
│   │       │   ├── approveWithdrawFromAdmin/ # Admin withdrawal approval
│   │       │   ├── rejectDepositFromAdmin/ # Admin deposit rejection
│   │       │   ├── depositLog/ # Deposit history
│   │       │   ├── withdrawLog/ # Withdrawal history
│   │       │   ├── referal/     # Referral system
│   │       │   ├── referalDetails/ # Referral details
│   │       │   ├── guideHandlers/ # User guide flows
│   │       │   ├── terms/       # Terms and conditions
│   │       │   ├── contactUs/  # Contact information
│   │       │   ├── backToMenu/ # Navigation
│   │       │   └── error/      # Error handling
│   │       ├── messages/       # Message templates
│   │       │   ├── start_message.py
│   │       │   ├── balanceCommandIfUserExists.py
│   │       │   ├── balanceCommadIfUserNotExists.py
│   │       │   ├── deposit.py
│   │       │   ├── withdrawal.py
│   │       │   ├── depositLog.py
│   │       │   ├── withdrawLog.py
│   │       │   ├── referal.py
│   │       │   ├── referal_details.py
│   │       │   ├── contactUs.py
│   │       │   ├── term.py
│   │       │   ├── depositMessageToAdmin.py
│   │       │   ├── withdrawMessageToAdmin.py
│   │       │   ├── approveDepositAndWithdrawalFromAdmin.py
│   │       │   ├── rejectDepositFromAdmin.py
│   │       │   ├── problemInBot.py
│   │       │   ├── problemInWebsite.py
│   │       │   ├── crypto_entry_point.py
│   │       │   ├── money_order_withdrawal_entry_point.py
│   │       │   ├── ichancy_new_user_message.py
│   │       │   ├── ichancy_exist_user_message.py
│   │       │   └── guideMessages/ # Guide message templates
│   │       └── executing/       # Transaction execution
│   │           ├── executingInterface.py
│   │           └── executingFactory.py
│   ├── admin_db.sqlite3         # SQLite database for Django admin/auth
│   ├── django.log               # Django application logs
│   └── TELEGRAM_BOT_INTEGRATION.md # Integration documentation
├── requirements.txt             # Python dependencies
└── ichancy-env/                 # Python virtual environment
```

## Key Components

### 1. Django Application (`mm/`)

**Purpose**: Provides admin interface and database models for the bot.

**Key Files**:
- `mm/settings.py`: Django configuration with dual database setup (MySQL for data, SQLite for admin)
- `mm/myapp/models.py`: Django ORM models mapped to MySQL database tables (read-only)
- `mm/myapp/admin.py`: Django admin interface with read-only views for most models
- `mm/myapp/routers.py`: Database router separating admin/auth (SQLite) from business data (MySQL)
- `mm/myapp/signals.py`: Django signals that sync Settings model changes to bot configuration

**Database Setup**:
- **MySQL** (`default`): Main database with user and transaction data
- **SQLite** (`admin_db`): Django admin, auth, and sessions

### 2. Telegram Bot (`mm/myapp/ichancyBot/`)

**Purpose**: Main Telegram bot implementation using python-telegram-bot library.

**Architecture**:
- **Entry Point**: `bot.py` - Initializes bot, registers handlers, starts polling
- **Flows**: Conversation handlers organized by feature (deposit, withdrawal, etc.)
- **Models**: Internal data models for bot operations
- **API Client**: `iChancyAPI.py` - Communicates with iChancy platform API
- **Background Threads**: 
  - Referral handler
  - Crypto price tracker
  - Cookie refresh mechanism

**Key Features**:
- User registration and account management
- Multiple payment methods (crypto, mobile money, money orders)
- Deposit and withdrawal flows
- Gift system (send/receive)
- Admin approval workflows
- Referral system
- Balance checking
- Transaction history

### 3. Configuration System

**Settings Storage**: Database-driven (MySQL `settings` table)

**Configuration Files**:
- `config/settings.py`: Loads settings from database with caching
- `config/telegram.py`: Telegram bot configuration (token, admin IDs, channels)
- `config/database.py`: Database connection (from .env file)
- `config/ichancy.py`: iChancy API configuration
- `config/device.py`: User-agent and device headers
- Payment method configs: `crypto.py`, `bemo.py`, `syriatel.py`, `shamCash.py`, `orderMoney.py`

**Settings Sync**: Django signals automatically refresh bot config when Settings model is updated in admin.

### 4. Database Models

**Django Models** (in `mm/myapp/models.py`):
- `Users`: User accounts with Telegram integration
- `Transactions`: General transaction records
- `AccountTransactions`: Account-to-account transactions
- `BemoTransactions`: Bemo payment transactions
- `SyriatelTransactions`: Syriatel payment transactions
- `ShamCashTransactions`: ShamCash payment transactions
- `OrderMoneyTransactions`: Money order transactions
- `CryptoTransactions`: Cryptocurrency transactions
- `Gifts`: Gift code system
- `MessagesToAdmin`: User messages to administrators
- `Settings`: Bot configuration (only writable model)

**Note**: All models except `Settings` are read-only (`managed = False`).

### 5. Flow Architecture

Each bot feature follows a consistent flow pattern:

```
flow_name/
├── handler.py          # Conversation handler definition
├── entryPoint.py       # Entry point state
├── [state]State.py     # Individual conversation states
├── validation/         # Input validation functions
├── cancel.py           # Cancel handler
└── execute.py          # Final execution (if applicable)
```

**Example Flow Structure**:
- `depositAccount/`: Account deposit with amount validation
- `cryptoDeposit/`: Crypto deposit with wallet type, amount, transfer number
- `createAccount/`: Account creation with username and password

### 6. Background Services

**Thread Manager** (`threadManager.py`):
- Manages lifecycle of background threads
- Graceful shutdown handling

**Background Threads**:
1. **Referral Handler** (`referalHandler.py`): Processes referral rewards
2. **Crypto Prices** (`cryptoPrices.py`): Tracks cryptocurrency exchange rates
3. **Cookie Refresh** (`refreshingCookie.py` or `refreshingCookieFromFile.py`): Maintains valid iChancy session cookies

### 7. API Integration

**iChancy API Client** (`iChancyAPI.py`):
- Account registration
- Player ID lookup
- Balance queries (admin and player)
- Money transfers (deposit/withdraw)
- Cookie validation
- Cloudflare challenge detection

**Features**:
- Session management with cookies
- Cloudflare bypass handling
- Error handling and retry logic
- SOCKS proxy support (commented out)

## Technology Stack

- **Framework**: Django 4.1.13
- **Bot Library**: python-telegram-bot 22.5
- **Database**: MySQL (main), SQLite (admin)
- **HTTP Client**: requests, httpx
- **Other**: APScheduler, mysql-connector-python, python-dotenv

## Running the Application

### Django Admin
```bash
cd mm
python manage.py runserver
python manage.py createsuperuser  # First time setup
```

### Telegram Bot
The bot can be run directly:
```bash
cd mm/myapp/ichancyBot
python bot.py
```

**Note**: According to `TELEGRAM_BOT_INTEGRATION.md`, there should be a Django management command `run_telegram_bot`, but it doesn't appear to exist yet. The bot is currently run directly from `bot.py`.

## Configuration

### Environment Variables (`.env` file)
- `DB_HOST`: MySQL host
- `DB_PORT`: MySQL port
- `DB_USERNAME`: MySQL username
- `DB_PASSWORD`: MySQL password
- `DB_NAME`: MySQL database name

### Database Settings (MySQL `settings` table)
- `telegram_bot_token`: Telegram bot token
- `transactions_telegram_bot_token`: Secondary bot token for transactions
- `admin_telegram_id`: Admin Telegram user ID
- `admin_chat_id`: Admin chat ID
- `ichancy_cookie`: iChancy platform session cookie
- `cookie_from_group_id`: Group ID for cookie refresh
- `parent_id`: iChancy parent/affiliate ID
- `exchange_rate`: Currency exchange rate
- `telegram_channels`: Comma-separated channel IDs
- `telegram_groups`: Comma-separated group IDs
- Various payment method group IDs

## Key Features

1. **Multi-Payment Support**: Crypto, Bemo, Syriatel, ShamCash, Money Orders
2. **Account Management**: Registration, deposits, withdrawals
3. **Gift System**: Send and receive gift codes
4. **Referral System**: User referral tracking and rewards
5. **Admin Workflow**: Approval/rejection of deposits and withdrawals
6. **Transaction History**: Deposit and withdrawal logs
7. **Balance Management**: Account and admin balance tracking
8. **Cookie Management**: Automatic cookie refresh for iChancy API access

## Security Considerations

- Cookie-based authentication for iChancy API
- Cloudflare challenge detection
- Admin-only operations for sensitive actions
- Read-only database access for most models
- Settings stored in database (not hardcoded)

## Development Notes

- Most Django models are read-only (`managed = False`)
- Bot configuration is loaded from database, not environment variables
- Settings changes trigger automatic bot config refresh via Django signals
- Background threads require proper shutdown handling
- Cookie status is monitored and refreshed automatically

## Future Improvements

Based on `TELEGRAM_BOT_INTEGRATION.md`:
- Create Django management command for running bot
- Better integration between Django and bot
- Shared database access improvements
- Enhanced admin interface for bot management


