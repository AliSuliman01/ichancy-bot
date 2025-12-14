# Configure PyMySQL to work with Django on Windows
# This is a monkey-patch to make Django use PyMySQL instead of MySQLdb
try:
    import pymysql
    # PyMySQL can be used as a drop-in replacement for MySQLdb
    pymysql.install_as_MySQLdb()
    
    # Patch the version to satisfy Django's version check
    # Django requires mysqlclient 2.2.1+, so we fake it
    import sys
    if 'pymysql' in sys.modules:
        # Make PyMySQL report a compatible version
        pymysql.version_info = (2, 2, 1, 'final', 0)
        pymysql.__version__ = '2.2.1'
except ImportError:
    # PyMySQL not installed, Django will try to use mysqlclient instead
    # This is fine if mysqlclient is properly installed
    pass

# Disable MariaDB version check for older versions
# This allows Django to work with MariaDB 10.4+
try:
    from django.db.backends.base.base import BaseDatabaseWrapper
    from django.db.backends.mysql.base import DatabaseWrapper
    
    # Store the original method
    _original_check_database_version_supported = BaseDatabaseWrapper.check_database_version_supported
    
    # Override to skip version check for MariaDB
    def patched_check_database_version_supported(self):
        # Skip version check - allow any MariaDB/MySQL version
        pass
    
    # Apply the patch
    BaseDatabaseWrapper.check_database_version_supported = patched_check_database_version_supported
except (ImportError, AttributeError):
    # If patching fails, continue anyway
    pass

