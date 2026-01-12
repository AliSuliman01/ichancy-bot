#!/usr/bin/env python
"""Create Django superuser non-interactively"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mm.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Get credentials from environment or use defaults
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

# Check if user already exists
if User.objects.using('admin_db').filter(username=username).exists():
    print(f'User "{username}" already exists.')
else:
    User.objects.using('admin_db').create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f'Superuser "{username}" created successfully!')
    print(f'Username: {username}')
    print(f'Email: {email}')
    print(f'Password: {password}')
