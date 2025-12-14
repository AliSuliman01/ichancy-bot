"""
Django management command to run the Telegram bot.

Usage:
    python manage.py run_telegram_bot

This command runs the Telegram bot as a long-running process.
The bot will continue running until stopped with Ctrl+C or killed.
"""

import sys
import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Runs the Telegram bot as a long-running process'

    def add_arguments(self, parser):
        parser.add_argument(
            '--daemon',
            action='store_true',
            help='Run the bot in daemon mode (background)',
        )

    def handle(self, *args, **options):
        # Add the telegramBot directory to Python path
        # Get the project root (two levels up from this file)
        # Path structure: mm/myapp/management/commands/run_telegram_bot.py
        # We need to go up 5 levels to get to project root
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent.parent.parent
        
        telegram_bot_path = project_root / 'telegramBot' / 'ichancyBot'
        telegram_bot_parent = project_root / 'telegramBot'
        
        # Verify paths exist
        if not telegram_bot_path.exists():
            self.stdout.write(
                self.style.ERROR(
                    f'Telegram bot directory not found: {telegram_bot_path}\n'
                    f'Current file: {current_file}\n'
                    f'Project root: {project_root}'
                )
            )
            return
        
        # Change to the bot directory so relative imports work
        original_cwd = os.getcwd()
        os.chdir(str(telegram_bot_path))
        
        # Add paths to sys.path for imports
        if str(telegram_bot_path) not in sys.path:
            sys.path.insert(0, str(telegram_bot_path))
        
        if str(telegram_bot_parent) not in sys.path:
            sys.path.insert(0, str(telegram_bot_parent))
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting Telegram bot from: {telegram_bot_path}')
        )
        
        try:
            # Import and run the bot
            # We need to import the bot module and run its main function
            import bot
            
            # The bot's main execution is in the if __name__ == '__main__' block
            # We'll need to manually trigger the initialization
            import Logger
            logger = Logger.getLogger()
            
            logger.info("Initializing iChancy Account Manager Bot from Django...")
            
            # Check Python version
            if sys.version_info < (3, 8):
                logger.error("Python 3.8 or higher is required")
                self.stdout.write(
                    self.style.ERROR('Python 3.8 or higher is required')
                )
                return
            
            # Import bot dependencies
            import config.telegram
            from cryptoPrices import CryptoPrices
            from referalHandler import referalThread
            from refreshingCookie import RefreshingCookieThread
            from refreshingCookieFromFile import RefreshingCookieFromFileThread
            
            # Validate tokens
            try:
                config.telegram.validate_tokens()
            except ValueError as e:
                logger.error(str(e))
                self.stdout.write(
                    self.style.ERROR(f'Bot configuration error: {e}')
                )
                return
            
            # Start background threads
            referal = referalThread()
            referal.start()
            
            cryptoPrices = CryptoPrices()
            cryptoPrices.start()
            
            if config.telegram.ACTIVE_REFRESHING_COOKIE:
                refreshingCookie = RefreshingCookieThread()
                refreshingCookie.start()
            
            if config.telegram.ACTIVE_REFRESHING_COOKIE_FROM_FILE:
                refreshingCookieFromFile = RefreshingCookieFromFileThread()
                refreshingCookieFromFile.start()
            
            self.stdout.write(
                self.style.SUCCESS('Telegram bot is starting...')
            )
            self.stdout.write(
                self.style.WARNING('Press Ctrl+C to stop the bot')
            )
            
            # Run the bot's main function
            bot.main()
            
        except KeyboardInterrupt:
            if 'logger' in locals():
                logger.info("Bot stopped by user")
            self.stdout.write(
                self.style.WARNING('\nBot stopped by user')
            )
        except ImportError as e:
            self.stdout.write(
                self.style.ERROR(f'Import error: {e}')
            )
            self.stdout.write(
                self.style.WARNING(
                    'Make sure the telegramBot/ichancyBot directory exists '
                    'and all dependencies are installed.\n'
                    f'Python path: {sys.path[:3]}...'
                )
            )
            import traceback
            self.stdout.write(traceback.format_exc())
        except Exception as e:
            if 'logger' in locals():
                logger.error(f"Bot crashed: {e}", exc_info=True)
            self.stdout.write(
                self.style.ERROR(f'Bot crashed: {e}')
            )
            import traceback
            self.stdout.write(traceback.format_exc())
        finally:
            # Restore original working directory
            os.chdir(original_cwd)

