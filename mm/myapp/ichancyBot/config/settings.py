"""
Settings loader module that reads configuration from the database settings table.
This replaces the .env file approach.
"""
import mysql.connector
import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from database import Database
import Logger

logger = Logger.getLogger()

# Cache for settings to avoid repeated database queries
_settings_cache = None

def _load_settings():
    """Load settings from database and cache them."""
    global _settings_cache
    
    if _settings_cache is not None:
        return _settings_cache
    
    try:
        db = Database.getConnection()
        cursor = db.cursor(dictionary=True)
        
        # Get the first (and typically only) settings record
        cursor.execute("SELECT * FROM settings ORDER BY id LIMIT 1")
        settings = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        if settings is None:
            logger.warning("No settings record found in database. Using defaults.")
            _settings_cache = {}
        else:
            _settings_cache = settings
            
        return _settings_cache
    except Exception as e:
        logger.error(f"Failed to load settings from database: {e}")
        # Return empty dict to prevent crashes, but log the error
        return {}

def get_setting(field_name, default=None):
    """Get a setting value from the database."""
    settings = _load_settings()
    return settings.get(field_name, default)

def refresh_settings():
    """Clear the cache to force reload from database."""
    global _settings_cache
    _settings_cache = None
    logger.info(f"************* _settings_cache refreshed *************")
    

# Load settings on module import
_load_settings()

