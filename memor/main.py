from os.path import basename
from sys import argv, exit, stderr


SUBCOMMANDS_MAP = {
    "+": "add",
    "-": "delete",
    "/": "search",
    "//": "jsearch",
    "./": "local_search",
    ".//": "local_jsearch",
    "e": "edit",
    "sub": "subscribe",
    "unsub": "unsubscribe",
}


def cli():
    try:
        subcommand = argv[1]
    except IndexError:
        bin_name = basename(argv[0])
        print(f"Usage: {bin_name} setup|+|delete|/", file=stderr)
        exit(10)

    args = argv[2:]

    if subcommand == "setup":
        from .setup import setup
        setup()
        exit(0)

    subcommand = SUBCOMMANDS_MAP.get(subcommand, subcommand)

    from memor import client  # NOQA:E402
    f = getattr(client, subcommand)
    f(*args)
