import logging
import os
from datetime import datetime

# Create logs/ folder in project root (same level as src/)
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file name with timestamp
LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Logging format = what each log line looks like
LOG_FORMAT = "[%(asctime)s] %(levelname)s | %(name)s | %(message)s"

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format=LOG_FORMAT,
    level=logging.INFO
)

# This is what you import everywhere
logger = logging.getLogger("mlproject")