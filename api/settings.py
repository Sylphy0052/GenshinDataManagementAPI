import logging
import os

# ディレクトリ設定
SERVER_DIR = os.path.join("/", "app")
DATA_DIR = os.path.join(SERVER_DIR, "datas")
os.makedirs(DATA_DIR, exist_ok=True)

# DB設定
DB_PATH = os.path.join(DATA_DIR, "db.sqlite")
DB_URL = f"sqlite:///{DB_PATH}"
ASYNC_DB_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# LOG設定
LOG_DIR = os.path.join(DATA_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "app.log")
LOGGER_NAME = "uvicorn"
LOGGER_MODE = logging.DEBUG
LOGGER_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOGGER_MAX_SIZE = 1000000
LOGGER_BACKUP_COUNT = 100
