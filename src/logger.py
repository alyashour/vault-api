import logging
from logging.handlers import RotatingFileHandler
import os 
from dotenv import load_dotenv

load_dotenv()

LOG_FILE = os.getenv('LOG_FILE')

# create rotating file handler (max 5MB, keep 3 backups)
handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)

formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)

# get the root loger
logger = logging.getLogger('notes_api')
logger.setLevel(logging.INFO)
logger.addHandler(handler)