"""
Django management command to run the Telegram bot.

This command initializes and runs the Telegram bot as a long-running process.
It sets up all background threads and starts the bot's polling loop.
"""
import sys
import os
import signal
from django.core.management.base import BaseCommand
from django.conf import settings

# Add the ichancyBot directory to Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
ICHANCY_BOT_PATH = os.path.join(BASE_DIR, 'myapp', 'ichancyBot')
if ICHANCY_BOT_PATH not in sys.path:
    sys.path.insert(0, ICHANCY_BOT_PATH)

# Now import bot modules
try:
    import Logger
    import config.telegram
    from cryptoPrices import CryptoPrices
    from referalHandler import referalThread
    from refreshingCookie import RefreshingCookieThread
    from refreshingCookieFromFile import RefreshingCookieFromFileThread
    from threadManager import get_thread_manager
    from bot import main
    logger = Logger.getLogger()
except ImportError as e:
    print(f"Error importing bot modules: {e}")
    print(f"Looking for bot in: {ICHANCY_BOT_PATH}")
    sys.exit(1)


class Command(BaseCommand):
    help = 'Run the Telegram bot as a long-running process'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-threads',
            action='store_true',
            help='Run bot without background threads',
        )
        parser.add_argument(
            '--no-crypto-prices',
            action='store_true',
            help='Run bot without crypto prices thread',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Telegram Bot...'))
        
        # Check Python version
        if sys.version_info < (3, 8):
            self.stdout.write(self.style.ERROR('Python 3.8 or higher is required'))
            sys.exit(1)
        
        # Validate tokens
        try:
            config.telegram.validate_tokens()
        except (ValueError, AttributeError) as e:
            self.stdout.write(self.style.ERROR(f'Configuration error: {e}'))
            self.stdout.write(self.style.WARNING('Please configure settings in Django admin or database'))
            self.stdout.write(self.style.WARNING('Required settings: telegram_bot_token, admin_telegram_id or admin_chat_id'))
            sys.exit(1)
        
        # Get thread manager instance
        thread_manager = get_thread_manager()
        
        # Setup signal handlers for graceful shutdown
        def signal_handler(signum, frame):
            self.stdout.write(self.style.WARNING(f'\nReceived signal {signum}, shutting down gracefully...'))
            thread_manager.stop_all()
            sys.exit(0)
        
        # Register signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            if not options['no_threads']:
                # Create and register background threads
                self.stdout.write(self.style.SUCCESS('Initializing background threads...'))
                
                referal = referalThread()
                thread_manager.register_thread(referal, "ReferralThread")
                
                # if not options['no_crypto_prices']:
                #     cryptoPrices = CryptoPrices()
                #     thread_manager.register_thread(cryptoPrices, "CryptoPrices")
                # else:
                #     self.stdout.write(self.style.WARNING('Crypto prices thread disabled'))
                
                if config.telegram.ACTIVE_REFRESHING_COOKIE:
                    refreshingCookie = RefreshingCookieThread()
                    thread_manager.register_thread(refreshingCookie, "RefreshingCookieThread")
                    self.stdout.write(self.style.SUCCESS('Cookie refresh thread enabled'))
                elif config.telegram.ACTIVE_REFRESHING_COOKIE_FROM_FILE:
                    refreshingCookieFromFile = RefreshingCookieFromFileThread()
                    thread_manager.register_thread(refreshingCookieFromFile, "RefreshingCookieFromFileThread")
                    self.stdout.write(self.style.SUCCESS('Cookie refresh from file thread enabled'))
                
                # Start all threads
                thread_manager.start_all()
                self.stdout.write(self.style.SUCCESS('Background threads started'))
            else:
                self.stdout.write(self.style.WARNING('Running without background threads'))
            
            self.stdout.write(self.style.SUCCESS('Bot is running. Press Ctrl+C to stop.'))
            
            # Run main bot (run_polling handles async internally)
            main()
            
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nBot stopped by user'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Bot crashed: {e}'))
            logger.error(f"Bot crashed: {e}", exc_info=True)
            raise
        finally:
            # Ensure all threads are stopped
            self.stdout.write(self.style.WARNING('Shutting down all background threads...'))
            thread_manager.stop_all()
            self.stdout.write(self.style.SUCCESS('Bot shutdown complete'))

