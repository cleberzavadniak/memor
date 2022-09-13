from sys import exit, stderr

from .base_settings import (  # NOQA:F401
    COLLECTION_FILE,
    DATA_DIR,
    LOCAL_DATA_FILE,
    MEMOR_URL,
    SUBSCRIPTIONS_DATA_FILE,
    SUBSCRIPTIONS_FILE,
    TOKEN_FILE
)

if not DATA_DIR.is_dir():
    print(
        f"DATA_DIR ({DATA_DIR}) does not exist. You must run `setup` subcommand first.",
        file=stderr
    )
    exit(2)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# TODO: check permissions of DATA_DIR! It should be `og-rwx`!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

if not TOKEN_FILE.is_file():
    print(f"{TOKEN_FILE} does not exist. You must run `setup` subcommand first.", file=stderr)
    exit(3)

if not COLLECTION_FILE.is_file():
    print(
        f"{COLLECTION_FILE} does not exist. You probably should run `setup` subcommand.",
        file=stderr
    )
    exit(4)


with TOKEN_FILE.open() as f:
    TOKEN = f.read()

with COLLECTION_FILE.open() as f:
    COLLECTION = f.read()

if not SUBSCRIPTIONS_FILE.exists():
    SUBSCRIPTIONS_FILE.touch()


if not SUBSCRIPTIONS_DATA_FILE.exists():
    SUBSCRIPTIONS_DATA_FILE.touch()
