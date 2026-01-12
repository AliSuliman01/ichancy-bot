import logging
import colorlog
import os
from pathlib import Path

LOGGER = None
API_LOGGER = None

def initializeLogger():
    # Create a colored formatter for console
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - [File:%(pathname)s] - [Line:%(lineno)d] - %(message)s%(reset)s',
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'green',
            'INFO': 'blue',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    
    # Create a file formatter (no colors)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [File:%(pathname)s] - [Line:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create a console handler with the colored formatter
    console_handler = colorlog.StreamHandler()
    console_handler.setFormatter(console_formatter)
    
    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent.parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # Create a file handler for general logs
    log_file = log_dir / 'bot.log'
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    
    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

def initializeAPILogger():
    """Initialize a dedicated logger for iChancy API failures"""
    global API_LOGGER
    
    if API_LOGGER is not None:
        return API_LOGGER
    
    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent.parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # Create a dedicated logger for API failures
    api_logger = logging.getLogger('iChancyAPI')
    api_logger.setLevel(logging.WARNING)  # Only log warnings and errors
    
    # Create file handler for API failures
    api_log_file = log_dir / 'ichancy_api_failures.log'
    api_file_handler = logging.FileHandler(api_log_file, encoding='utf-8')
    api_file_handler.setLevel(logging.WARNING)
    
    # Detailed formatter for API logs
    api_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - [Method:%(funcName)s] - [Line:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    api_file_handler.setFormatter(api_formatter)
    
    api_logger.addHandler(api_file_handler)
    api_logger.propagate = False  # Don't propagate to root logger
    
    API_LOGGER = api_logger
    return api_logger

def getLogger():
    global LOGGER
    if LOGGER == None:
        initializeLogger()
        LOGGER = logging.getLogger(__name__)
    return LOGGER

def getAPILogger():
    """Get the dedicated API logger for iChancy API failures"""
    return initializeAPILogger()