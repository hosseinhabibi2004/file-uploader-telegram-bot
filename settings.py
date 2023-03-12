# ------------------------------- Import ------------------------------- #
import os
import logging
from distutils.util import strtobool
from dotenv import load_dotenv


# ---------------------------- Error Handler --------------------------- #
def error_handler(update, context):
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.error('update: \"%s\"\nerror: \n\t\"%s\"', update, context.error)


# ------------------------------- Config ------------------------------- #
load_dotenv()
class config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    OWNER = int(os.getenv('OWNER'))
    DEBUG = strtobool(os.getenv('DEBUG'))
    TG_ID = os.getenv('TG_ID')
    TG_NAME = os.getenv('TG_NAME')

