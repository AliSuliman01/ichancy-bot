import logging
LOGGER = None
def initializeLogger():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

def getLogger():
    global LOGGER
    if LOGGER == None:
        initializeLogger()
        LOGGER = logging.getLogger(__name__)
    return LOGGER