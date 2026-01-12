"""
Django signals for the myapp application.
"""
import sys
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Settings

# Add the ichancyBot directory to the path to import settings
# signals.py is in mm/myapp/, and ichancyBot is in mm/myapp/ichancyBot/
current_dir = os.path.dirname(os.path.abspath(__file__))
ichancy_bot_path = os.path.join(current_dir, 'ichancyBot')
if ichancy_bot_path not in sys.path:
    sys.path.insert(0, ichancy_bot_path)

try:
    from config.settings import refresh_settings
except ImportError as e:
    # If import fails, create a no-op function to prevent crashes
    def refresh_settings():
        pass
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f"Could not import refresh_settings from ichancyBot: {e}")


@receiver(post_save, sender=Settings)
def refresh_telegram_bot_settings(sender, instance, **kwargs):
    """
    Signal handler that refreshes the Telegram bot's settings cache
    whenever the Settings model is saved in Django.
    """
    try:
        # refresh_settings() takes no arguments
        refresh_settings()
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to refresh Telegram bot settings: {e}", exc_info=True)

