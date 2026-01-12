#!/usr/bin/env python
"""Add or update settings record in the database"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mm.settings')
django.setup()

from myapp.models import Settings

# Get values from environment variables or use defaults/empty
settings_data = {
    'telegram_bot_token': os.environ.get('TELEGRAM_BOT_TOKEN', ''),
    'admin_telegram_id': os.environ.get('ADMIN_TELEGRAM_ID', ''),
    'ichancy_cookie': os.environ.get('ICHANCY_COOKIE', ''),
    'parent_id': os.environ.get('PARENT_ID', ''),
    'admin_chat_id': os.environ.get('ADMIN_CHAT_ID', ''),
    'exchange_rate': float(os.environ.get('EXCHANGE_RATE', '1.00')),
    'user_agent': os.environ.get('USER_AGENT', ''),
    'bot_name': os.environ.get('BOT_NAME', ''),
    'telegram_channels': os.environ.get('TELEGRAM_CHANNELS', ''),
    'telegram_groups': os.environ.get('TELEGRAM_GROUPS', ''),
    'transactions_telegram_bot_token': os.environ.get('TRANSACTIONS_TELEGRAM_BOT_TOKEN', ''),
    'cookie_from_group_id': os.environ.get('COOKIE_FROM_GROUP_ID', ''),
    'crypto_deposit_group': os.environ.get('CRYPTO_DEPOSIT_GROUP', ''),
    'crypto_withdraw_group': os.environ.get('CRYPTO_WITHDRAW_GROUP', ''),
    'bemo_deposit_group': os.environ.get('BEMO_DEPOSIT_GROUP', ''),
    'bemo_withdraw_group': os.environ.get('BEMO_WITHDRAW_GROUP', ''),
    'syriatel_deposit_group': os.environ.get('SYRIATEL_DEPOSIT_GROUP', ''),
    'syriatel_withdraw_group': os.environ.get('SYRIATEL_WITHDRAW_GROUP', ''),
    'shamcash_deposit_group': os.environ.get('SHAMCASH_DEPOSIT_GROUP', ''),
    'shamcash_withdraw_group': os.environ.get('SHAMCASH_WITHDRAW_GROUP', ''),
}

# Check if settings record already exists
existing = Settings.objects.first()

if existing:
    print('Settings record already exists. Updating...')
    for key, value in settings_data.items():
        if value:  # Only update non-empty values
            setattr(existing, key, value)
    existing.save()
    print('Settings record updated successfully!')
    print(f'Settings ID: {existing.id}')
else:
    print('Creating new settings record...')
    settings = Settings.objects.create(**settings_data)
    print('Settings record created successfully!')
    print(f'Settings ID: {settings.id}')

# Display current settings (masking sensitive data)
print('\nCurrent settings:')
settings = Settings.objects.first()
if settings:
    print(f'  Bot Name: {settings.bot_name or "Not set"}')
    print(f'  Admin Telegram ID: {settings.admin_telegram_id or "Not set"}')
    print(f'  Admin Chat ID: {settings.admin_chat_id or "Not set"}')
    print(f'  Telegram Bot Token: {"***" + settings.telegram_bot_token[-10:] if settings.telegram_bot_token else "Not set"}')
    print(f'  Parent ID: {settings.parent_id or "Not set"}')
    print(f'  Exchange Rate: {settings.exchange_rate}')
    print(f'  iChancy Cookie: {"Set" if settings.ichancy_cookie else "Not set"}')
    print(f'  Created: {settings.created_at}')
    print(f'  Updated: {settings.updated_at}')
    
    # Check required fields
    required_fields = {
        'telegram_bot_token': settings.telegram_bot_token,
        'admin_telegram_id': settings.admin_telegram_id,
        'ichancy_cookie': settings.ichancy_cookie,
        'parent_id': settings.parent_id,
    }
    
    missing = [key for key, value in required_fields.items() if not value]
    if missing:
        print(f'\nWARNING: Missing required fields: {", ".join(missing)}')
        print('   Please set these via environment variables or Django admin.')
    else:
        print('\nAll required fields are set!')
