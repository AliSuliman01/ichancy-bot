#!/usr/bin/env python
"""Create settings table in MySQL database if it doesn't exist"""
import os
import sys

# Try to use Django ORM, but fallback to direct MySQL if Django isn't ready
try:
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mm.settings')
    django.setup()
    use_django = True
except Exception as e:
    # Fallback to direct MySQL connection
    use_django = False
    try:
        from dotenv import load_dotenv
        load_dotenv()
        import mysql.connector
    except ImportError:
        print(f"Error: Cannot import required modules. {e}", file=sys.stderr)
        sys.exit(1)

def create_settings_table():
    """Create settings table if it doesn't exist"""
    try:
        if use_django:
            from django.db import connection
            cursor = connection.cursor()
        else:
            # Direct MySQL connection
            db = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=int(os.getenv('DB_PORT', '3306')),
                user=os.getenv('DB_USERNAME', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'cicp_bot')
            )
            cursor = db.cursor()
        
        # Check if table exists
        cursor.execute("SHOW TABLES LIKE 'settings'")
        result = cursor.fetchone()
        
        if not result:
            print("Creating settings table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_agent VARCHAR(500) NULL,
                    ichancy_cookie TEXT NULL,
                    admin_telegram_id VARCHAR(255) NULL,
                    parent_id VARCHAR(255) NULL,
                    exchange_rate DECIMAL(10,2) DEFAULT 1.00 NULL,
                    admin_chat_id VARCHAR(255) NULL,
                    telegram_bot_token VARCHAR(255) NULL,
                    transactions_telegram_bot_token VARCHAR(255) NULL,
                    telegram_channels VARCHAR(255) NULL,
                    telegram_groups VARCHAR(255) NULL,
                    bot_name VARCHAR(255) NULL,
                    cookie_from_group_id VARCHAR(255) NULL,
                    crypto_deposit_group VARCHAR(255) NULL,
                    crypto_withdraw_group VARCHAR(255) NULL,
                    bemo_deposit_group VARCHAR(255) NULL,
                    bemo_withdraw_group VARCHAR(255) NULL,
                    syriatel_deposit_group VARCHAR(255) NULL,
                    syriatel_withdraw_group VARCHAR(255) NULL,
                    shamcash_deposit_group VARCHAR(255) NULL,
                    shamcash_withdraw_group VARCHAR(255) NULL,
                    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
                    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)
            if not use_django:
                db.commit()
            print("Settings table created successfully.")
        else:
            print("Settings table already exists.")
        
        if not use_django:
            cursor.close()
            db.close()
    except Exception as e:
        print(f"Error checking/creating settings table: {e}", file=sys.stderr)
        if not use_django:
            try:
                db.close()
            except:
                pass
        # Don't raise - allow deployment to continue
        return False
    return True

if __name__ == '__main__':
    success = create_settings_table()
    sys.exit(0 if success else 1)
