from getpass import getpass
from random import choice
from subprocess import run
from string import ascii_lowercase
from sys import exit, stderr

import requests

from .base_settings import (
    COLLECTION_FILE,
    DATA_DIR,
    LOCAL_DATA_FILE,
    MEMOR_URL,
    TOKEN_FILE
)


def random_string():
    return ''.join(choice(ascii_lowercase) for _ in range(0, 64))


def do_setup():
    if not DATA_DIR.is_dir():
        print(f"Creating DATA_DIR: {DATA_DIR}", file=stderr)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
    elif TOKEN_FILE.exists():
        print("You already have a token configured.")
        answer = input("Do you want to proceed with the setup and OVERWRITE it? (y/N) ")
        if answer.lower() not in ("y", "yes"):
            exit(30)

    print("Ensuring correct permissions for DATA_DIR...", file=stderr)
    run(["chmod", "og-rwx", str(DATA_DIR)])
    print()

    while True:
        # Private or public?
        answer = input("Do you intend to publish your collection (giving it a pretty name)? (y/N) ")
        if answer.lower() in ("y", "yes"):

            while True:
                # Collection slug:
                slug = input("Your personal collection slug: ")

                if len(slug) < 5:
                    print("Your collection slug should be longer than 5 characters")
                    continue
                else:
                    break
        else:
            slug = random_string()

        # Check if it already exists:
        response = requests.get(f"{MEMOR_URL}/collections/{slug}")

        if response.status_code == 400:
            print("Invalid slug! Try again.")
        elif response.status_code == 404:
            break
        elif response.status_code == 200:
            print("This collection already exists.")
            answer = input("Are you sure you want to use it? (y/N) ")
            if answer.lower() in ("y", "yes"):
                break
        else:
            print("Unknown status code:", response.status)
            print(response.content)

    while True:
        print()
        # Token:
        print("Your secret token.")
        print("Let it blank to auto-generate one.")
        token = getpass("token: ")
        if not token:
            token = random_string()
            break
        elif len(token) < 5:
            print("The secret token must be longer than 5 characters")
            continue
        else:
            break

    with COLLECTION_FILE.open("w") as f:
        f.write(slug)

    with TOKEN_FILE.open("w") as f:
        f.write(token)

    if not LOCAL_DATA_FILE.exists():
        LOCAL_DATA_FILE.touch(exist_ok=True)

    print()
    print("Setup complete.")


def setup():
    try:
        do_setup()
    except KeyboardInterrupt:
        print()
        print("Aborted.")
