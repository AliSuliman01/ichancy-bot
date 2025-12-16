import logging
import colorlog

LOGGER = None

def initializeLogger():
    # Create a colored formatter
    formatter = colorlog.ColoredFormatter(
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
    
    # Create a console handler with the colored formatter
    handler = colorlog.StreamHandler()
    handler.setFormatter(formatter)
    
    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

def getLogger():
    global LOGGER
    if LOGGER == None:
        initializeLogger()
        LOGGER = logging.getLogger(__name__)
    return LOGGER