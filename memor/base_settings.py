from os import environ
from pathlib import Path


MEMOR_URL = environ.get("MEMOR_URL", "https://memor.cleber.solutions/api").rstrip("/")

HOME = Path(environ["HOME"])
DATA_DIR = Path(environ.get("MEMOR_DATA_DIR", HOME / ".config/memor/default"))

TOKEN_FILE = DATA_DIR / "token"
COLLECTION_FILE = DATA_DIR / "collection"
LOCAL_DATA_FILE = DATA_DIR / "local"
SUBSCRIPTIONS_FILE = DATA_DIR / "subscriptions"
SUBSCRIPTIONS_DATA_FILE = DATA_DIR / "subscriptions-data"
